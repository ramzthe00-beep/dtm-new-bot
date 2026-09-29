"""
ct_trader.py
============
اجرای مستقل CT + معامله + فیلتر FINAL_RULES

- در هر چرخه، تایم‌فریم‌هایی که کندلشون تازه بسته شده رو چک می‌کنه
- سیگنال‌های CT رو استخراج می‌کنه
- 🎯 فیلتر FINAL_RULES (kind/direction/timeframe/risk_pct/weekday/ADX/RSI) رو اعمال می‌کنه
- محاسبه‌ی سرمایه مثل DTM: BALANCE_USE_RATIO + LEVERAGE_MAP + MIN_ORDER_COST
- Anchor price از thetruetrade.io برای exec_stop/exec_target
- ثبت کامل در trade_ledger
- لاگ تفصیلی + پیام تلگرام (مثل DTM)
- RF flag برای BTC (پیاده‌سازی عملی RF در نسخه بعدی)
"""
import math
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("CT_TRADER")

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

# ═══════════════════════════════════════════════════════════
# 🎯 فیلتر FINAL_RULES — import امن
# ═══════════════════════════════════════════════════════════
try:
    from filter_main import should_take_signal, get_risk_free_enabled
    _FILTER_AVAILABLE = True
    logger.info("[CT-TRADER] FINAL_RULES filter loaded ✅")
except ImportError as _e:
    logger.warning(f"[CT-TRADER] filter_main not available ({_e}) — filter disabled")
    _FILTER_AVAILABLE = False

    def should_take_signal(signal, df):
        return True, "filter_not_available"

    def get_risk_free_enabled(symbol):
        return False


# ═══════════════════════════════════════════════════════════
# پیکربندی — مشابه DTM
# ═══════════════════════════════════════════════════════════
CT_TRADED_SYMBOLS = ["ETHUSDT", "BTCUSDT", "SOLUSDT", "BNBUSDT"]
CT_TIMEFRAMES = ["60", "240"]   # 1h, 4h

CT_CHECK_WINDOW_MINUTES = 4

CT_BASE_CAPITAL = 1.5
CT_BALANCE_USE_RATIO = 0.70

# State
_last_processed_signal_ms = {}
_ct_trade_counter = 0


# ═══════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════
def _tf_label(tf):
    tf_min = int(tf)
    return f"{tf_min}m" if tf_min < 60 else f"{tf_min//60}h"


def should_check_timeframe(timeframe, now_utc):
    tf_min = int(timeframe)
    if tf_min < 60:
        return True

    minute = now_utc.minute
    hour = now_utc.hour

    if minute >= CT_CHECK_WINDOW_MINUTES:
        return False

    if tf_min == 60:
        return True
    elif tf_min == 240:
        return hour % 4 == 0
    elif tf_min == 1440:
        return hour == 0
    else:
        hours = tf_min // 60
        if hours <= 0:
            return True
        return hour % hours == 0


def _is_valid_num(x):
    if x is None:
        return False
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return False
    return True


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

    profit_str = f"{actual_profit_dollar:.4f}" if actual_profit_dollar is not None else "N/A"

    msg = f"""
{emoji} سیگنال CT {direction_fa} ({direction}) - {symbol} - {tf_label}
─────────────────────────────────────────
🆔 شماره: {trade_id}
🕐 زمان: {now_utc_str} UTC ({now_ir_str} تهران)
─────────────────────────────────────────
📊 ورود: {entry:.4f}
🛑 حد ضرر: {stop:.4f} ({stop_distance:.4f}- | {stop_pct*100:.3f}%)
🎯 هدف: {target:.4f} ({target_distance:.4f}+ | {target_pct*100:.3f}%)
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
    try:
        send_telegram_fn(msg)
    except Exception as e:
        logger.error(f"[CT-TRADER] telegram error: {e}")


# ═══════════════════════════════════════════════════════════
# اجرای یک معامله CT
# ═══════════════════════════════════════════════════════════
def _execute_ct_trade(
    sig, symbol, timeframe, public, exchange, ledger,
    leverage_map, min_order_cost, send_telegram_fn,
    enable_rf=False,
):
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

    # دریافت balance
    try:
        balance = exchange.fetch_balance()
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol}: fetch_balance failed: {e}")
        return

    if balance <= 0:
        logger.warning(f"[CT-TRADER] {symbol} {tf_label}: balance<=0")
        return

    # anchor price
    df_anchor = public.fetch_ohlcv(symbol, "1")
    if df_anchor is None or df_anchor.empty:
        logger.warning(f"[CT-TRADER] {symbol}: cannot fetch anchor price")
        return

    exec_anchor_price = float(df_anchor['close'].iloc[-1])
    if direction == "LONG":
        exec_stop = exec_anchor_price * (1 - stop_pct)
        exec_target = exec_anchor_price * (1 + target_pct)
    else:
        exec_stop = exec_anchor_price * (1 + stop_pct)
        exec_target = exec_anchor_price * (1 - target_pct)

    logger.info(
        f"[CT-TRADER] {symbol} {tf_label} anchor={exec_anchor_price:.4f} "
        f"stop={exec_stop:.4f} target={exec_target:.4f} | RF={enable_rf}"
    )

    # محاسبه‌ی capital
    allowed_leverage = leverage_map.get(symbol, 50)
    old_leverage = 1.0 / stop_pct

    if old_leverage > allowed_leverage:
        required_capital = (old_leverage / allowed_leverage) * CT_BASE_CAPITAL
        leverage_mode = "INCREASED"
    else:
        required_capital = CT_BASE_CAPITAL
        leverage_mode = "BASE"

    if balance < required_capital:
        capital = balance * CT_BALANCE_USE_RATIO
        actual_stop_dollar = capital * stop_pct * allowed_leverage
        actual_profit_dollar = capital * target_pct * allowed_leverage if target_pct > 0 else None
        mode = "REDUCED_98"
    else:
        capital = required_capital
        actual_stop_dollar = CT_BASE_CAPITAL
        actual_profit_dollar = (target_pct / stop_pct) * CT_BASE_CAPITAL if target_pct > 0 else None
        mode = "FULL"

    rr = (target_pct / stop_pct) if stop_pct > 0 else 0.0

    # لاگ تفصیلی
    profit_str = f"{actual_profit_dollar:.4f}" if actual_profit_dollar else "N/A"
    logger.info(
        f"[CT-{tf_label}][{symbol}] سیگنال={kind} {direction} | ورود={exec_anchor_price:.4f}\n"
        f"  درصد استاپ={stop_pct:.6f} | درصد تارگت={target_pct:.6f}\n"
        f"  اهرم قدیمی={old_leverage:.2f} | اهرم مجاز={allowed_leverage}\n"
        f"  سرمایه موردنیاز={required_capital:.4f} | حالت اهرم={leverage_mode}\n"
        f"  موجودی={balance:.4f} | حالت سرمایه={mode}\n"
        f"  سرمایه ارسالی={capital:.4f}\n"
        f"  استاپ دلاری=${actual_stop_dollar:.4f}\n"
        f"  سود دلاری=${profit_str}\n"
        f"  R={rr:.2f} | RF={enable_rf}"
    )

    # ثبت در ledger
    try:
        ledger.record_signal(
            symbol=symbol,
            timeframe=timeframe,
            direction=direction,
            entry=exec_anchor_price,
            stop=exec_stop,
            target=exec_target,
            entry_time_ms=signal_ms,
            leverage=allowed_leverage,
            order_placed=None,
            order_reason=f"CT-{kind}{'|RF' if enable_rf else ''}",
            risk_free_pct=None,
        )
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol}: record_signal failed: {e}")

    # چک MIN_ORDER_COST
    if capital < min_order_cost:
        logger.warning(
            f"[CT-SKIP-LOW-BALANCE] {symbol} {kind} {direction}: "
            f"capital {capital:.4f} USDT < min {min_order_cost} USDT"
        )
        try:
            send_telegram_fn(
                f"⚠️ سیگنال CT {kind} برای {symbol} ({tf_label}) اجرا نشد\n"
                f"سرمایه محاسبه‌شده: {capital:.4f} USDT\n"
                f"حداقل مجاز: {min_order_cost} USDT\n"
                f"موجودی: {balance:.4f} USDT"
            )
        except Exception:
            pass
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

            trade_id = _next_trade_id()
            _send_signal_telegram(
                send_telegram_fn, symbol, tf_label, sig,
                exec_anchor_price, exec_stop, exec_target,
                stop_pct, target_pct, rr, capital, allowed_leverage, mode,
                actual_stop_dollar, actual_profit_dollar, trade_id, balance,
            )
        else:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label} {kind}: order failed ❌")

    except Exception as e:
        logger.exception(f"[CT-TRADER] {symbol} {tf_label}: create_order exception: {e}")


# ═══════════════════════════════════════════════════════════
# پردازش سیگنال‌های CT در یک چرخه
# ═══════════════════════════════════════════════════════════
def process_ct_signals(
    public, exchange, ledger, leverage_map, send_telegram_fn,
    base_capital=None, min_order_cost=5.0,
):
    """
    پردازش سیگنال‌های CT. از loop اصلی bot.py صدا زده می‌شه.
    """
    from ct_wrapper import run_ct_strategy

    now_utc = datetime.now(timezone.utc)

    for symbol in CT_TRADED_SYMBOLS:
        for tf in CT_TIMEFRAMES:
            if not should_check_timeframe(tf, now_utc):
                continue

            tf_label = _tf_label(tf)
            key = (symbol, tf)

            try:
                # دریافت داده
                df = public.fetch_ohlcv(symbol, tf)
                if df is None or df.empty:
                    continue

                # به‌روزرسانی معاملات باز
                try:
                    ledger.update_open_trades(symbol, tf, df)
                except Exception as e:
                    logger.error(f"[CT-TRADER] {symbol} {tf_label}: update_open_trades: {e}")

                # اجرای CT
                signals = run_ct_strategy(df, symbol, tf)
                signals = [s for s in signals if s is not None]
                if not signals:
                    continue

                signals.sort(key=lambda x: x['time_ms'] or 0)
                last_signal_ms = signals[-1]['time_ms'] or 0

                # اولین بار: seed
                if key not in _last_processed_signal_ms:
                    _last_processed_signal_ms[key] = last_signal_ms
                    logger.info(
                        f"[CT-TRADER] {symbol} {tf_label}: seeded at ms={last_signal_ms}"
                    )
                    continue

                # سیگنال‌های جدید
                threshold_ms = _last_processed_signal_ms[key]
                new_signals = [s for s in signals if (s['time_ms'] or 0) > threshold_ms]

                if not new_signals:
                    continue

                logger.info(
                    f"[CT-TRADER] {symbol} {tf_label}: {len(new_signals)} new signal(s)"
                )

                for s in new_signals:
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

                        signal_dict = {
                            "symbol": symbol,
                            "kind": s['kind'],
                            "direction": s['direction'],
                            "timeframe": tf_label,
                            "risk_pct": risk_pct,
                            "time_utc": now_utc,
                        }

                        take, reason = should_take_signal(signal_dict, df)

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
                            enable_rf=enable_rf,
                        )
                    except Exception as e:
                        logger.exception(f"[CT-TRADER] {symbol} {tf_label}: trade error: {e}")

                _last_processed_signal_ms[key] = last_signal_ms

            except Exception as e:
                logger.exception(f"[CT-TRADER] {symbol} {tf_label}: cycle error: {e}")