"""
ct_trader.py
============
اجرای مستقل CT + معامله + فیلتر FINAL_RULES

- برای هر ترکیب (نماد، تایم‌فریم) که در FINAL_RULES تعریف شده، درست بعد از بسته‌شدنِ
  هر کندل (مثل حلقه‌ی DTM در bot.py: boundary + چند ثانیه صبر) یک‌بار پردازش می‌کند.
  (قبلاً فقط ۴ دقیقه‌ی اول هر ساعت چک می‌شد؛ اگر سیکل ربات کند بود کل پنجره از دست می‌رفت.)
- CT روی «کندل‌های بسته‌شده» اجرا می‌شود (ct_wrapper کندل ناقص را حذف می‌کند).
- 🎯 فیلتر FINAL_RULES (kind/direction/timeframe/risk_pct/weekday/ADX/RSI) با
  زمان خودِ سیگنال و دیتای تا همان کندل سیگنال اعمال می‌شود.
- محاسبه‌ی سرمایه مثل DTM: BALANCE_USE_RATIO + LEVERAGE_MAP + MIN_ORDER_COST
- Anchor price از thetruetrade.io (و در نبودش Binance) برای exec_stop/exec_target
- ثبت کامل در trade_ledger
- لاگ تفصیلی + پیام تلگرام (مثل DTM)
- RF flag برای BTC (پیاده‌سازی عملی RF در نسخه بعدی)

هیچ‌چیز از منطق/محاسبات استراتژی (ct_strategy.py) یا فرمول سایزینگ تغییر نکرده است.
"""
import json as _json
import logging
import math
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path as _Path

import pandas as pd

# ⏰ زمان استارت ربات — فقط برای جلوگیری از معامله روی سیگنال‌های «قبل از استارت»
_BOT_START_MS = int(time.time() * 1000)

logger = logging.getLogger("CT_TRADER")

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

# ═══════════════════════════════════════════════════════════
# 🎯 فیلتر FINAL_RULES — import امن
# ═══════════════════════════════════════════════════════════
try:
    from filter_main import should_take_signal, get_risk_free_enabled
    from final_rules import FINAL_RULES
    _FILTER_AVAILABLE = True
    logger.info("[CT-TRADER] FINAL_RULES filter loaded ✅")
except ImportError as _e:
    # 🔧 قبلاً در این حالت فیلتر «باز» می‌شد (همه‌ی سیگنال‌ها قبول می‌شدند). چون فیلتر تعیین‌کننده‌ی
    # اینکه چه معامله‌ای مجاز است، حالت امن = رد کردن (و لاگ خطا).
    logger.error(f"[CT-TRADER] filter_main/final_rules not available ({_e}) — ALL CT signals will be rejected")
    _FILTER_AVAILABLE = False
    FINAL_RULES = {}

    def should_take_signal(signal, df):
        return False, "filter_not_available"

    def get_risk_free_enabled(symbol):
        return False


# ═══════════════════════════════════════════════════════════
# پیکربندی — مشابه DTM
# ═══════════════════════════════════════════════════════════
# فقط fallback وقتی FINAL_RULES در دسترس نیست؛ ترکیب‌های فعال از FINAL_RULES می‌آیند.
CT_TRADED_SYMBOLS = ["ETHUSDT", "BTCUSDT", "SOLUSDT", "BNBUSDT"]
CT_TIMEFRAMES = ["60", "240"]   # 1h, 4h

CT_BASE_CAPITAL = 1.5            # اگر bot.py مقدار نفرستد (bot از trade_ledger.BASE_CAPITAL می‌فرستد)
CT_BALANCE_USE_RATIO = 0.70

CT_BOUNDARY_SETTLE_SEC = 10      # بعد از بسته‌شدن کندل چند ثانیه صبر کن تا دیتا نهایی شود
CT_MAX_ATTEMPTS_PER_BOUNDARY = 6 # اگر دیتا/CT خطا داد، در همان کندل چندبار دوباره تلاش شود
CT_MAX_SIGNAL_AGE_BARS = 1       # سیگنال قدیمی‌تر از این (به‌تعداد کندل) دیگر با قیمت مارکت وارد نمی‌شود

# State
_last_processed_signal_ms = {}   # (symbol, tf) -> زمان آخرین سیگنال پردازش‌شده
_last_boundary = {}              # (symbol, tf) -> آخرین boundary پردازش‌شده (epoch sec)
_boundary_attempts = {}          # (symbol, tf, boundary) -> تعداد تلاش
_state_loaded = False

# ═══════════════════════════════════════════════════════════════
# 💾 Persistent State — برای ذخیره در فایل
# ═══════════════════════════════════════════════════════════════
_CT_STATE_FILE = _Path.home() / "ct_trader_state.json"


def _load_ct_state():
    """بارگذاری state از فایل (در ری‌استارت)"""
    if _CT_STATE_FILE.exists():
        try:
            data = _json.loads(_CT_STATE_FILE.read_text())
            return {tuple(k.split("|")): v for k, v in data.items()}
        except Exception as e:
            logger.warning(f"[CT-TRADER] state load failed: {e}")
            return {}
    return {}


def _save_ct_state(state):
    """ذخیره state در فایل"""
    try:
        data = {f"{k[0]}|{k[1]}": v for k, v in state.items()}
        _CT_STATE_FILE.write_text(_json.dumps(data))
    except Exception as e:
        logger.warning(f"[CT-TRADER] state save failed (در حافظه نگه داشته می‌شود): {e}")


_ct_trade_counter = 0


# ═══════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════
def _tf_label(tf):
    tf_min = int(tf)
    return f"{tf_min}m" if tf_min < 60 else f"{tf_min//60}h"


def _label_to_minutes(label):
    """'4h' → '240' ، '1h' → '60' ، '15m' → '15'"""
    label = str(label).strip().lower()
    if label.endswith("h"):
        return str(int(label[:-1]) * 60)
    if label.endswith("m"):
        return str(int(label[:-1]))
    return str(int(label))


def _active_combos():
    """
    ترکیب‌های (نماد، تایم‌فریم) که واقعاً در FINAL_RULES مجازند — فقط همین‌ها پردازش می‌شوند
    (قبلاً همه‌ی ۸ ترکیب fetch و اجرا می‌شد و ۶ تا همیشه توسط فیلتر رد می‌شد).
    """
    if FINAL_RULES:
        combos = []
        for sym, rule in FINAL_RULES.items():
            try:
                combos.append((sym, _label_to_minutes(rule["timeframe"])))
            except Exception as e:
                logger.error(f"[CT-TRADER] bad timeframe in FINAL_RULES[{sym}]: {e}")
        return combos
    return [(s, t) for s in CT_TRADED_SYMBOLS for t in CT_TIMEFRAMES]


def _is_valid_num(x):
    if x is None:
        return False
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return False
    return True


def _price_prec(price):
    """رقم اعشار مناسب برای نمایش قیمت (قیمت‌های کوچک مثل DOGE با ۴ رقم اشتباه نمایش داده نشوند)."""
    try:
        p = abs(float(price))
    except Exception:
        return 4
    if p >= 1000:
        return 2
    if p >= 1:
        return 4
    if p >= 0.01:
        return 5
    return 7


def _fmt_time_utc(ms):
    try:
        return datetime.fromtimestamp(ms/1000, tz=UTC_TZ).strftime("%H:%M:%S")
    except Exception:
        return "?"


def _fmt_time_iran(ms):
    try:
        return datetime.fromtimestamp(ms/1000, tz=UTC_TZ).astimezone(IRAN_TZ).strftime("%H:%M:%S")
    except Exception:
        return "?"


def _next_trade_id():
    global _ct_trade_counter
    _ct_trade_counter += 1
    return f"CT-{_ct_trade_counter:04d}"


def _safe_send(send_telegram_fn, text):
    try:
        send_telegram_fn(text)
    except Exception as e:
        logger.error(f"[CT-TRADER] telegram error: {e}")


def _send_signal_telegram(send_telegram_fn, symbol, tf_label, sig, entry, stop, target,
                           stop_pct, target_pct, rr, capital, leverage, mode,
                           actual_stop_dollar, actual_profit_dollar, trade_id, balance):
    direction = sig['direction']
    emoji = "🟢" if direction == "LONG" else "🔴"
    direction_fa = "خرید" if direction == "LONG" else "فروش"

    if rr >= 3:
        rr_status = "عالی 🚀"
    elif rr >= 2:
        rr_status = "خوب ✅"
    elif rr >= 1:
        rr_status = "متوسط ⚠️"
    else:
        rr_status = "ضعیف ❌"

    signal_type_fa = {
        "Anni-L": "Anni-L (آنی - لانگ)",
        "Anni-S": "Anni-S (آنی - شورت)",
        "Aati-L": "Aati-L (آتی - لانگ)",
        "Aati-S": "Aati-S (آتی - شورت)",
    }.get(sig['kind'], sig['kind'])

    now_utc_str = datetime.now(UTC_TZ).strftime("%H:%M:%S")
    now_ir_str = datetime.now(IRAN_TZ).strftime("%H:%M:%S")

    stop_distance = abs(stop - entry)
    target_distance = abs(target - entry)
    pp = _price_prec(entry)

    profit_str = f"{actual_profit_dollar:.4f}" if actual_profit_dollar is not None else "N/A"

    msg = f"""
{emoji} سیگنال CT {direction_fa} ({direction}) - {symbol} - {tf_label}
─────────────────────────────────────────
🆔 شماره: {trade_id}
🕐 زمان: {now_utc_str} UTC ({now_ir_str} تهران)
─────────────────────────────────────────
📊 ورود: {entry:.{pp}f}
🛑 حد ضرر: {stop:.{pp}f} ({stop_distance:.{pp}f}- | {stop_pct*100:.3f}%)
🎯 هدف: {target:.{pp}f} ({target_distance:.{pp}f}+ | {target_pct*100:.3f}%)
⭐ نسبت ریسک: 1 : {rr:.2f} ({rr_status})
📌 نوع: {signal_type_fa}
─────────────────────────────────────────
💰 موجودی: {balance:.4f} USDT
📊 حالت اهرم: {mode} | اهرم: {leverage}x
💵 سرمایه ارسالی: {capital:.4f} USDT
📉 استاپ دلاری: ${actual_stop_dollar:.4f}
📈 سود دلاری: ${profit_str}
─────────────────────────────────────────
🔒 وضعیت: {'✅ معتبر' if rr >= 2 else '⚠️ ریسک بالا'}
"""
    _safe_send(send_telegram_fn, msg)


def _fetch_anchor_price(public, symbol):
    """
    قیمت لنگر اجرا: اول thetruetrade.io (۱ دقیقه)، اگر نشد Binance (مثل زنجیره‌ی DTM در bot.py).
    خروجی: (price, source) یا (None, None)
    """
    for attempt in range(2):
        try:
            df_anchor = public.fetch_ohlcv(symbol, "1")
            if df_anchor is not None and not df_anchor.empty:
                return float(df_anchor['close'].iloc[-1]), "thetruetrade"
        except Exception as e:
            logger.warning(f"[CT-TRADER] {symbol}: anchor fetch (thetruetrade) attempt {attempt+1} failed: {e}")
    fetch_bn = getattr(public, "fetch_ohlcv_binance", None)
    if callable(fetch_bn):
        try:
            df_b = fetch_bn(symbol, "1")
            if df_b is not None and not df_b.empty:
                return float(df_b['close'].iloc[-1]), "binance"
        except Exception as e:
            logger.warning(f"[CT-TRADER] {symbol}: anchor fetch (binance) failed: {e}")
    return None, None


# ═══════════════════════════════════════════════════════════
# اجرای یک معامله CT
# ═══════════════════════════════════════════════════════════
def _execute_ct_trade(
    sig, symbol, timeframe, public, exchange, ledger,
    leverage_map, min_order_cost, send_telegram_fn,
    enable_rf=False, base_capital=None,
):
    base_cap = base_capital if (base_capital and base_capital > 0) else CT_BASE_CAPITAL

    direction = sig['direction']
    signal_entry = sig['entry']
    signal_stop = sig['stop']
    signal_target = sig['target']
    signal_ms = sig['time_ms']
    kind = sig['kind']
    tf_label = _tf_label(timeframe)

    # چک پایه
    if not (_is_valid_num(signal_entry) and _is_valid_num(signal_stop) and _is_valid_num(signal_target)):
        logger.warning(f"[CT-TRADER] {symbol} {tf_label}: invalid signal numbers")
        return

    # محاسبه‌ی درصدها
    if direction == "LONG":
        if signal_entry <= signal_stop:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label}: invalid LONG (entry<=stop)")
            return
        stop_pct = (signal_entry - signal_stop) / signal_entry
        target_pct = (signal_target - signal_entry) / signal_entry
    else:
        if signal_stop <= signal_entry:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label}: invalid SHORT (stop<=entry)")
            return
        stop_pct = (signal_stop - signal_entry) / signal_entry
        target_pct = (signal_entry - signal_target) / signal_entry

    if stop_pct <= 0:
        logger.warning(f"[CT-TRADER] {symbol} {tf_label}: stop_pct<=0")
        return

    # anchor price
    exec_anchor_price, anchor_src = _fetch_anchor_price(public, symbol)
    if exec_anchor_price is None:
        logger.error(f"[CT-TRADER] {symbol} {tf_label}: cannot fetch anchor price — trade NOT placed")
        _safe_send(
            send_telegram_fn,
            f"⚠️ سیگنال CT {kind} برای {symbol} ({tf_label}) تأیید شد ولی قیمت لحظه‌ای "
            f"دریافت نشد؛ سفارش ارسال نشد."
        )
        return

    if direction == "LONG":
        exec_stop = exec_anchor_price * (1 - stop_pct)
        exec_target = exec_anchor_price * (1 + target_pct)
    else:
        exec_stop = exec_anchor_price * (1 + stop_pct)
        exec_target = exec_anchor_price * (1 - target_pct)

    logger.info(
        f"[CT-TRADER] {symbol} {tf_label} anchor={exec_anchor_price:.6f} ({anchor_src}) "
        f"stop={exec_stop:.6f} target={exec_target:.6f} | RF={enable_rf}"
    )

    rr = (target_pct / stop_pct) if stop_pct > 0 else 0.0

    # ثبت در ledger (همه‌ی سیگنال‌های تأییدشده، صرف‌نظر از موجودی/موفقیت سفارش)
    try:
        ledger.record_signal(
            symbol=symbol,
            timeframe=timeframe,
            direction=direction,
            entry=exec_anchor_price,
            stop=exec_stop,
            target=exec_target,
            entry_time_ms=signal_ms,
            leverage=leverage_map.get(symbol, 50),
            order_placed=None,
            order_reason=f"CT-{kind}{'|RF' if enable_rf else ''}",
            risk_free_pct=None,
        )
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol}: record_signal failed: {e}")

    # دریافت balance
    try:
        balance = exchange.fetch_balance()
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol}: fetch_balance failed: {e}")
        balance = 0.0

    if balance is None or balance <= 0:
        logger.warning(f"[CT-TRADER] {symbol} {tf_label}: balance<=0 ({balance})")
        _safe_send(
            send_telegram_fn,
            f"⚠️ سیگنال CT {kind} برای {symbol} ({tf_label}) تأیید شد ولی موجودی قابل‌استفاده "
            f"صفر/نامشخص است ({balance}); سفارش ارسال نشد."
        )
        return

    # محاسبه‌ی capital (همان فرمول قبلی/DTM)
    allowed_leverage = leverage_map.get(symbol, 50)
    old_leverage = 1.0 / stop_pct

    if old_leverage > allowed_leverage:
        required_capital = (old_leverage / allowed_leverage) * base_cap
        leverage_mode = "INCREASED"
    else:
        required_capital = base_cap
        leverage_mode = "BASE"

    if balance < required_capital:
        capital = balance * CT_BALANCE_USE_RATIO
        actual_stop_dollar = capital * stop_pct * allowed_leverage
        actual_profit_dollar = capital * target_pct * allowed_leverage if target_pct > 0 else None
        mode = "REDUCED_98"
    else:
        capital = required_capital
        actual_stop_dollar = base_cap
        actual_profit_dollar = (target_pct / stop_pct) * base_cap if target_pct > 0 else None
        mode = "FULL"

    # لاگ تفصیلی
    profit_str = f"{actual_profit_dollar:.4f}" if actual_profit_dollar else "N/A"
    logger.info(
        f"[CT-{tf_label}][{symbol}] سیگنال={kind} {direction} | ورود={exec_anchor_price:.6f}\n"
        f"  درصد استاپ={stop_pct:.6f} | درصد تارگت={target_pct:.6f}\n"
        f"  اهرم قدیمی={old_leverage:.2f} | اهرم مجاز={allowed_leverage}\n"
        f"  سرمایه موردنیاز={required_capital:.4f} | حالت اهرم={leverage_mode}\n"
        f"  موجودی={balance:.4f} | حالت سرمایه={mode}\n"
        f"  سرمایه ارسالی={capital:.4f}\n"
        f"  استاپ دلاری=${actual_stop_dollar:.4f}\n"
        f"  سود دلاری=${profit_str}\n"
        f"  R={rr:.2f} | RF={enable_rf}"
    )

    # 📣 پیام سیگنال تأییدشده به تلگرام (مثل DTM: به‌محض تأیید، نه فقط بعد از موفقیت سفارش)
    trade_id = _next_trade_id()
    _send_signal_telegram(
        send_telegram_fn, symbol, tf_label, sig,
        exec_anchor_price, exec_stop, exec_target,
        stop_pct, target_pct, rr, capital, allowed_leverage, mode,
        actual_stop_dollar, actual_profit_dollar, trade_id, balance,
    )

    # چک MIN_ORDER_COST
    if capital < min_order_cost:
        logger.warning(
            f"[CT-SKIP-LOW-BALANCE] {symbol} {kind} {direction}: "
            f"capital {capital:.4f} USDT < min {min_order_cost} USDT"
        )
        _safe_send(
            send_telegram_fn,
            f"⚠️ سیگنال CT {kind} برای {symbol} ({tf_label}) اجرا نشد\n"
            f"سرمایه محاسبه‌شده: {capital:.4f} USDT\n"
            f"حداقل مجاز: {min_order_cost} USDT\n"
            f"موجودی: {balance:.4f} USDT"
        )
        return

    # ارسال سفارش
    try:
        result = exchange.create_order(
            symbol,
            direction,
            capital,
            allowed_leverage,
            take_profit=exec_target,
            stop_loss=exec_stop,
        )

        if result is not None:
            logger.info(f"[CT-TRADER] {symbol} {tf_label} {kind}: order placed ✅")
        else:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label} {kind}: order failed ❌")

    except Exception as e:
        logger.exception(f"[CT-TRADER] {symbol} {tf_label}: create_order exception: {e}")
        _safe_send(send_telegram_fn, f"❌ خطا در ارسال سفارش CT {kind} {symbol} ({tf_label}): {e}")


# ═══════════════════════════════════════════════════════════
# پردازش یک (نماد، تایم‌فریم) برای یک boundary
# خروجی: True اگر boundary «تمام‌شده» حساب شود (موفق)، False اگر باید دوباره تلاش شود
# ═══════════════════════════════════════════════════════════
def _process_one(symbol, tf, public, exchange, ledger, leverage_map,
                 send_telegram_fn, base_capital, min_order_cost):
    from ct_wrapper import run_ct_strategy, closed_candles_only

    tf_label = _tf_label(tf)
    tf_ms = int(tf) * 60 * 1000
    key = (symbol, tf)

    df = public.fetch_ohlcv(symbol, tf)
    if df is None or df.empty:
        logger.warning(f"[CT-TRADER] {symbol} {tf_label}: no data (will retry)")
        return False

    # به‌روزرسانی معاملات باز (ledger فقط کندل‌های بسته‌شده را بررسی می‌کند)
    try:
        ledger.update_open_trades(symbol, tf, df)
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol} {tf_label}: update_open_trades: {e}")

    # اجرای CT (کندل ناقص داخل run_ct_strategy حذف می‌شود)
    signals = run_ct_strategy(df, symbol, tf)
    signals = [s for s in signals if s is not None]
    signals.sort(key=lambda x: x['time_ms'] or 0)

    df_closed = closed_candles_only(df, tf)
    last_bar_ms = int(df_closed.index[-1].timestamp() * 1000) if len(df_closed) else 0

    # آستانه: هرگز سیگنالی که «قبل از استارت» بسته شده یا قبلاً پردازش شده دوباره پردازش نشود.
    # سیگنال در «پایان» کندلش معنی دارد، پس مبنا زمان بسته‌شدن کندل (time_ms + tf) است.
    thr = max(_last_processed_signal_ms.get(key, 0), _BOT_START_MS - tf_ms)
    unseen = [s for s in signals if (s['time_ms'] or 0) > thr]

    now_ms = int(time.time() * 1000)
    fresh, stale = [], []
    for s in unseen:
        age_ms = now_ms - ((s['time_ms'] or 0) + tf_ms)
        (fresh if age_ms <= CT_MAX_SIGNAL_AGE_BARS * tf_ms else stale).append(s)

    logger.info(
        f"[CT-TRADER] {symbol} {tf_label}: last_closed_bar={_fmt_time_utc(last_bar_ms)}Z "
        f"signals_total={len(signals)} unseen={len(unseen)} fresh={len(fresh)} stale={len(stale)}"
    )

    for s in stale:
        logger.info(
            f"[CT-TRADER] {symbol} {tf_label}: SKIP stale {s['kind']} {s['direction']} "
            f"@ bar {_fmt_time_utc(s['time_ms'])}Z (too old to enter at market)"
        )

    if unseen:
        _last_processed_signal_ms[key] = max((s['time_ms'] or 0) for s in unseen)
        _save_ct_state(_last_processed_signal_ms)

    for s in fresh:
        try:
            # ═══════════════════════════════════════════════════════
            # 🎯 فیلتر FINAL_RULES
            # ═══════════════════════════════════════════════════════
            entry_px = s.get('entry')
            stop_px = s.get('stop')

            if not (_is_valid_num(entry_px) and _is_valid_num(stop_px)) or entry_px <= 0:
                logger.warning(
                    f"[CT-FILTER] {symbol} {tf_label}: invalid entry/stop "
                    f"(entry={entry_px}, stop={stop_px})"
                )
                continue

            risk_pct = abs(entry_px - stop_px) / entry_px * 100

            sig_time_utc = s.get('time_utc') or datetime.now(UTC_TZ)

            signal_dict = {
                "symbol": symbol,
                "kind": s['kind'],
                "direction": s['direction'],
                "timeframe": tf_label,
                "risk_pct": risk_pct,
                # 🔧 زمان خودِ سیگنال (قبلاً «الان» پاس داده می‌شد؛ فیلتر روز هفته باید روی روز سیگنال باشد)
                "time_utc": sig_time_utc,
            }

            # 🔧 ADX/RSI باید روی کندل سیگنال محاسبه شود، نه آخرین کندل (که ممکن است ناقص/جدیدتر باشد)
            try:
                df_for_filter = df_closed[df_closed.index <= pd.Timestamp(sig_time_utc)]
                if df_for_filter.empty:
                    df_for_filter = df_closed
            except Exception:
                df_for_filter = df_closed

            take, reason = should_take_signal(signal_dict, df_for_filter)

            if not take:
                logger.info(
                    f"[CT-FILTER] {symbol} {s['kind']} {s['direction']} @ {tf_label} "
                    f"REJECTED: {reason} | risk_pct={risk_pct:.3f}%"
                )
                continue

            enable_rf = get_risk_free_enabled(symbol)

            logger.info(
                f"[CT-FILTER] {symbol} {s['kind']} {s['direction']} @ {tf_label} "
                f"ACCEPTED | risk_pct={risk_pct:.3f}% | enable_rf={enable_rf}"
            )

            # اجرای معامله
            _execute_ct_trade(
                s, symbol, tf, public, exchange, ledger,
                leverage_map, min_order_cost, send_telegram_fn,
                enable_rf=enable_rf, base_capital=base_capital,
            )
        except Exception as e:
            logger.exception(f"[CT-TRADER] {symbol} {tf_label}: trade error: {e}")

    return True


# ═══════════════════════════════════════════════════════════
# پردازش سیگنال‌های CT در یک چرخه
# ═══════════════════════════════════════════════════════════
def process_ct_signals(
    public, exchange, ledger, leverage_map, send_telegram_fn,
    base_capital=None, min_order_cost=5.0,
):
    """
    پردازش سیگنال‌های CT. از loop اصلی bot.py در هر چرخه صدا زده می‌شود؛
    هر (نماد، تایم‌فریم) فقط یک‌بار به‌ازای هر کندل بسته‌شده واقعاً پردازش می‌شود.
    """
    global _state_loaded

    # ═══ 💾 بارگذاری state از فایل (برای ری‌استارت) ═══
    if not _state_loaded:
        _state_loaded = True
        loaded = _load_ct_state()
        if loaded:
            _last_processed_signal_ms.update(loaded)
            logger.info(f"[CT-TRADER] LOADED {len(loaded)} state entries from file")

    now_ts = time.time()

    for symbol, tf in _active_combos():
        key = (symbol, tf)
        try:
            tf_sec = int(tf) * 60
            boundary = int(now_ts // tf_sec) * tf_sec

            if now_ts < boundary + CT_BOUNDARY_SETTLE_SEC:
                continue
            if boundary <= _last_boundary.get(key, 0):
                continue

            att_key = (symbol, tf, boundary)
            _boundary_attempts[att_key] = _boundary_attempts.get(att_key, 0) + 1

            done = _process_one(
                symbol, tf, public, exchange, ledger, leverage_map,
                send_telegram_fn, base_capital, min_order_cost,
            )

            if done or _boundary_attempts[att_key] >= CT_MAX_ATTEMPTS_PER_BOUNDARY:
                if not done:
                    logger.error(
                        f"[CT-TRADER] {symbol} {_tf_label(tf)}: giving up on boundary {boundary} "
                        f"after {_boundary_attempts[att_key]} attempts"
                    )
                _last_boundary[key] = boundary
                # پاک‌سازی شمارنده‌های قدیمی
                for k in [k for k in _boundary_attempts if k[0] == symbol and k[1] == tf and k[2] <= boundary]:
                    _boundary_attempts.pop(k, None)

        except Exception as e:
            logger.exception(f"[CT-TRADER] {symbol} {_tf_label(tf)}: cycle error: {e}")
