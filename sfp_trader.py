"""
sfp_trader.py
=============
اجرای خودکار استراتژی SFP — با همان فرمول سایزینگ، لنگر قیمت، حداقل سرمایه و ledger مربوط به DTM.

جریان (برای هر نماد/تایم‌فریم، یک‌بار به‌ازای هر کندل بسته‌شده، مثل حلقه‌ی DTM):
  boundary + ۵ ثانیه → کندل‌های Binance → sfp_wrapper.run_sfp_signals
  → اگر کندل SFP همین الآن بسته شده بود (تازه) →
     ثبت در ledger → پیام تلگرام → محاسبه‌ی سرمایه (عین DTM) → سفارش MARKET با SL/TP

فرمول سایزینگ (کپی عین‌به‌عین از bot.py/DTM):
  stop_pct = |entry-stop|/entry ; target_pct = |target-entry|/entry
  old_leverage = 1/stop_pct
  old_leverage > allowed_leverage → required_capital = (old_leverage/allowed_leverage)*BASE_CAPITAL (INCREASED)
  وگرنه required_capital = BASE_CAPITAL (BASE)
  balance < required_capital → capital = balance*BALANCE_USE_RATIO (REDUCED_98)
  وگرنه capital = required_capital (FULL)
"""
import json as _json
import logging
import math
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path as _Path

from sfp_wrapper import (
    run_sfp_signals, closed_candles_only, build_sfp_message, price_prec, _tick_info,
)

logger = logging.getLogger("SFP_TRADER")

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

_BOT_START_MS = int(time.time() * 1000)

SFP_BASE_CAPITAL = 1.5            # fallback اگر bot.py مقدار نفرستد
SFP_BALANCE_USE_RATIO = 0.70      # همان BALANCE_USE_RATIO در DTM
SFP_BOUNDARY_SETTLE_SEC = 5       # همان BOUNDARY_SETTLE_BUFFER_SEC در DTM
SFP_MAX_ATTEMPTS_PER_BOUNDARY = 6
SFP_MAX_SIGNAL_AGE_BARS = 1       # سیگنال قدیمی‌تر از یک کندل دیگر وارد نمی‌شود

_last_processed_signal_ms = {}    # (symbol, tf, direction) -> time_ms
_last_boundary = {}
_boundary_attempts = {}
_state_loaded = False
_sfp_trade_counter = 0

_STATE_FILE = _Path.home() / "sfp_trader_state.json"


# ───────────────────────── state ─────────────────────────
def _load_state():
    if _STATE_FILE.exists():
        try:
            data = _json.loads(_STATE_FILE.read_text())
            return {tuple(k.split("|")): v for k, v in data.items()}
        except Exception as e:
            logger.warning(f"[SFP-TRADER] state load failed: {e}")
    return {}


def _save_state(state):
    try:
        _STATE_FILE.write_text(_json.dumps({"|".join(k): v for k, v in state.items()}))
    except Exception as e:
        logger.warning(f"[SFP-TRADER] state save failed (kept in memory): {e}")


# ───────────────────────── helpers ─────────────────────────
def _valid(x):
    return x is not None and not (isinstance(x, float) and (math.isnan(x) or math.isinf(x)))


def _tf_label(tf):
    m = int(tf)
    return f"{m}m" if m < 60 else f"{m // 60}h"


def _next_trade_id():
    global _sfp_trade_counter
    _sfp_trade_counter += 1
    return f"SFP-{_sfp_trade_counter:04d}"


def _safe_send(fn, text):
    try:
        fn(text)
    except Exception as e:
        logger.error(f"[SFP-TRADER] telegram error: {e}")


def compute_sizing(direction, entry, stop, target, balance, base_capital,
                   allowed_leverage, balance_use_ratio):
    """فرمول سایزینگ DTM — عین bot.py."""
    if direction == "LONG":
        stop_pct = abs(entry - stop) / entry if entry > 0 else 0
    else:
        stop_pct = abs(stop - entry) / entry if entry > 0 else 0

    if _valid(target) and target > 0:
        target_pct = abs(target - entry) / entry if direction == "LONG" else abs(entry - target) / entry
    else:
        target_pct = 0

    if stop_pct <= 0:
        return None

    old_leverage = 1.0 / stop_pct
    if old_leverage > allowed_leverage:
        required_capital = (old_leverage / allowed_leverage) * base_capital
        leverage_mode = "INCREASED"
    else:
        required_capital = base_capital
        leverage_mode = "BASE"

    if balance < required_capital:
        capital = balance * balance_use_ratio
        actual_stop_dollar = capital * stop_pct * allowed_leverage
        actual_profit_dollar = capital * target_pct * allowed_leverage if target_pct > 0 else None
        mode = "REDUCED_98"
    else:
        capital = required_capital
        actual_stop_dollar = base_capital
        actual_profit_dollar = (target_pct / stop_pct) * base_capital if target_pct > 0 else None
        mode = "FULL"

    return {
        "stop_pct": stop_pct, "target_pct": target_pct, "old_leverage": old_leverage,
        "required_capital": required_capital, "leverage_mode": leverage_mode,
        "capital": capital, "actual_stop_dollar": actual_stop_dollar,
        "actual_profit_dollar": actual_profit_dollar, "mode": mode,
        "balance": balance, "leverage": allowed_leverage,
        "r_value": (target_pct / stop_pct) if target_pct > 0 else None,
    }


def _anchor_price(public, symbol, df_signal):
    """زنجیره‌ی DTM: thetruetrade(1m) → Binance(1m/ df_signal) → None (یعنی قیمت خام سیگنال)."""
    try:
        d = public.fetch_ohlcv(symbol, "1")
        if d is not None and not d.empty:
            return float(d["close"].iloc[-1]), "thetruetrade"
    except Exception as e:
        logger.warning(f"[SFP-TRADER] {symbol}: anchor (thetruetrade) failed: {e}")
    try:
        if df_signal is not None and not df_signal.empty:
            return float(df_signal["close"].iloc[-1]), "binance"
    except Exception as e:
        logger.warning(f"[SFP-TRADER] {symbol}: anchor (binance) failed: {e}")
    return None, None


# ───────────────────────── اجرای یک معامله ─────────────────────────
def _execute(sig, symbol, tf, df_signal, public, exchange, ledger, leverage_map,
             min_order_cost, send_fn, base_capital, balance_use_ratio):
    tf_label = _tf_label(tf)
    direction = sig["direction"]
    entry, stop, target = sig["entry"], sig["stop"], sig["target"]
    mintick = float(_tick_info(symbol)["mintick"])

    if not (_valid(entry) and _valid(stop) and _valid(target)):
        logger.warning(f"[SFP-TRADER] {symbol} {tf_label}: invalid signal numbers")
        return

    # ثبت در ledger (مثل DTM: entry/stop/target خودِ استراتژی؛ id جدا از DTM)
    try:
        ledger.record_signal(
            symbol=symbol, timeframe=tf, direction=direction,
            entry=entry, stop=stop, target=target,
            entry_time_ms=sig["time_ms"],
            leverage=leverage_map.get(symbol, 50),
            order_placed=None, order_reason="SFP", risk_free_pct=None,
            id_suffix=f"_{sig['kind']}",
            extra={"kind": sig["kind"], "dashed": sig["dashed"], "wick": sig["wick"],
                   "raw_target": sig["raw_target"]},
        )
    except Exception as e:
        logger.error(f"[SFP-TRADER] {symbol}: record_signal failed: {e}")

    try:
        balance = exchange.fetch_balance()
    except Exception as e:
        logger.error(f"[SFP-TRADER] {symbol}: fetch_balance failed: {e}")
        balance = 0.0

    allowed_leverage = leverage_map.get(symbol, 50)
    trade_id = _next_trade_id()

    if balance is None or balance <= 0:
        _safe_send(send_fn, build_sfp_message(sig, symbol, tf, trade_id, mintick))
        import tg_messages as tgm
        _safe_send(send_fn, tgm.not_executed_card(
            "SFP", direction, symbol, tf_label, "موجودی صفر یا نامشخص",
            [f"💰 موجودی: {tgm.code(balance)}", f"🛑 استاپ: {tgm.code(stop)}", f"📍 ورود: {tgm.code(entry)}"]))
        return

    sz = compute_sizing(direction, entry, stop, target, balance, base_capital,
                        allowed_leverage, balance_use_ratio)
    if sz is None:
        logger.warning(f"[SFP-TRADER] {symbol} {tf_label}: stop_pct<=0 — skipped")
        return

    stop_pct, target_pct = sz["stop_pct"], sz["target_pct"]
    profit_str = f"{sz['actual_profit_dollar']:.4f}" if sz["actual_profit_dollar"] else "N/A"
    r_str = f"{sz['r_value']:.2f}" if sz["r_value"] else "N/A"
    logger.info(
        f"[SFP-{tf_label}][{symbol}] سیگنال={direction} | ورود={entry}\n"
        f"  درصد استاپ={stop_pct:.6f} | درصد تارگت={target_pct:.6f}\n"
        f"  اهرم قدیمی={sz['old_leverage']:.2f} | اهرم مجاز={allowed_leverage}\n"
        f"  سرمایه موردنیاز={sz['required_capital']:.4f} | حالت اهرم={sz['leverage_mode']}\n"
        f"  موجودی={balance:.4f} | حالت سرمایه={sz['mode']}\n"
        f"  سرمایه ارسالی={sz['capital']:.4f}\n"
        f"  استاپ دلاری=${sz['actual_stop_dollar']:.4f}\n"
        f"  سود دلاری=${profit_str}\n"
        f"  R={r_str}"
    )

    # 📣 پیام سیگنال به تلگرام (به‌محض تأیید، مثل DTM)
    _safe_send(send_fn, build_sfp_message(sig, symbol, tf, trade_id, mintick, sizing=sz))

    if sz["capital"] < min_order_cost:
        logger.warning(f"[SFP-SKIP-LOW-BALANCE] {symbol} {direction}: {sz['capital']:.4f} < {min_order_cost}")
        import tg_messages as tgm
        _safe_send(send_fn, tgm.not_executed_card(
            "SFP", direction, symbol, tf_label, "سرمایه کمتر از حداقل سفارش",
            [f"💵 سرمایه محاسبه‌شده: {tgm.code(format(sz['capital'], '.4f'))} USDT",
             f"📏 حداقل مجاز: {tgm.code(min_order_cost)} USDT",
             f"💰 موجودی: {tgm.code(format(balance, '.4f'))} USDT"]))
        return

    # لنگر اجرا: درصدهای استاپ/تارگت روی قیمت لحظه‌ای اعمال می‌شود (عین DTM)
    exec_stop, exec_target = stop, target
    anchor, src = _anchor_price(public, symbol, df_signal)
    if anchor:
        if direction == "LONG":
            exec_stop = anchor * (1 - stop_pct)
            exec_target = anchor * (1 + target_pct) if target_pct > 0 else None
        else:
            exec_stop = anchor * (1 + stop_pct)
            exec_target = anchor * (1 - target_pct) if target_pct > 0 else None
        logger.info(f"[SFP-{tf_label}][{symbol}] لنگر({src})={anchor} | stop {stop}→{exec_stop} | "
                    f"target {target}→{exec_target}")
    else:
        logger.warning(f"[SFP-{tf_label}][{symbol}] anchor unavailable — using raw stop/target")

    try:
        result = exchange.create_order(symbol, direction, sz["capital"], allowed_leverage,
                                       take_profit=exec_target, stop_loss=exec_stop)
        logger.info(f"[SFP-TRADER] {symbol} {tf_label}: order {'placed ✅' if result is not None else 'failed ❌'}")
    except Exception as e:
        logger.exception(f"[SFP-TRADER] {symbol} {tf_label}: create_order exception: {e}")
        import tg_messages as tgm
        _safe_send(send_fn, tgm.alert_card(
            "error", "خطا در ارسال سفارش SFP",
            [f"🪙 {tgm.b(symbol)} · {tgm.b(direction)} · ⏱ {tgm.b(tf_label)}", f"🧯 {tgm.code(str(e)[:400])}"]))


# ───────────────────────── پردازش یک (نماد، تایم‌فریم) ─────────────────────────

def _fetch_exec_history(public, symbol, tf, bars):
    """کندل‌های اجرایی (thetruetrade) با countback بزرگ‌تر — برای بازیابی معاملاتی که مدتی بررسی نشده‌اند."""
    try:
        now = int(time.time())
        from_ts = now - bars * int(tf) * 60 * 2 - 60
        uri = (f"/futures/udf/history?symbol={symbol.upper()}&resolution={tf}"
               f"&from={from_ts}&to={now}&countback={bars}")
        r = public.session.get(f"{public.base}{uri}", timeout=25)
        r.raise_for_status()
        data = r.json()
        if data.get("s") != "ok" or not data.get("t"):
            return None
        import pandas as pd
        df = pd.DataFrame({
            "open": pd.to_numeric(data["o"], errors="coerce"), "high": pd.to_numeric(data["h"], errors="coerce"),
            "low": pd.to_numeric(data["l"], errors="coerce"), "close": pd.to_numeric(data["c"], errors="coerce"),
        }, index=pd.to_datetime(data["t"], unit="s", utc=True)).sort_index()
        df = df[~df.index.duplicated(keep="last")].dropna()
        return df
    except Exception as e:
        logger.warning(f"[SFP-TRADER] {symbol}: history catch-up fetch failed: {e}")
        return None


def _update_ledger_for(symbol, tf, tf_ms, public, ledger):
    """
    به‌روزرسانی نتیجه‌ی معاملات باز (تارگت/استاپ) این نماد.
    فقط وقتی معامله‌ی باز دارد fetch می‌کند؛ اگر قدیمی‌ترین معامله‌ی باز از پنجره‌ی ۵۰۰ کندلی بیرون
    افتاده باشد، تاریخچه‌ی بلندتر می‌گیرد تا نتیجه از همان لحظه‌ی ورود بررسی شود.
    """
    tf_label = _tf_label(tf)
    try:
        count, oldest_ms = (ledger.open_rows_info(symbol, tf)
                            if hasattr(ledger, "open_rows_info") else (1, None))
        if count == 0:
            return
        df_exec = public.fetch_ohlcv(symbol, tf)
        if df_exec is None or df_exec.empty:
            logger.warning(f"[SFP-TRADER] {symbol} {tf_label}: exec data empty — ledger not updated")
            return
        if oldest_ms is not None:
            first_ms = int(df_exec.index[0].timestamp() * 1000)
            if oldest_ms < first_ms:
                need = int((time.time() * 1000 - oldest_ms) / tf_ms) + 10
                bars = min(need, 1500)
                longer = _fetch_exec_history(public, symbol, tf, bars)
                if longer is not None and not longer.empty:
                    got_first = int(longer.index[0].timestamp() * 1000)
                    if got_first > oldest_ms + 2 * tf_ms:
                        logger.warning(f"[SFP-TRADER] {symbol} {tf_label}: history only reaches back "
                                       f"{(time.time()*1000 - got_first)/3600000:.1f}h; older open trades may resolve late")
                    df_exec = longer
                    logger.info(f"[SFP-TRADER] {symbol} {tf_label}: catch-up with {len(longer)} candles "
                                f"for {count} open trade(s)")
        ledger.update_open_trades(symbol, tf, df_exec)
    except Exception as e:
        logger.error(f"[SFP-TRADER] {symbol} {tf_label}: update_open_trades: {e}")


def _process_one(symbol, tf, public, exchange, ledger, leverage_map, send_fn,
                 base_capital, min_order_cost, balance_use_ratio, update_ledger):
    tf_label = _tf_label(tf)
    tf_ms = int(tf) * 60 * 1000

    if update_ledger:  # فقط برای جفت‌هایی که حلقه‌ی DTM خودش به‌روز نمی‌کند (مثلاً نمادهای فقط-SFP)
        _update_ledger_for(symbol, tf, tf_ms, public, ledger)   # مستقل از داده‌ی Binance

    df = public.fetch_ohlcv_binance(symbol, tf)
    if df is None or df.empty:
        logger.warning(f"[SFP-TRADER] {symbol} {tf_label}: no data (will retry)")
        return False

    signals = run_sfp_signals(df, symbol, tf)
    signals.sort(key=lambda s: s["time_ms"])
    now_ms = int(time.time() * 1000)

    fresh = []
    for s in signals:
        key = (symbol, tf, s["direction"])
        thr = max(_last_processed_signal_ms.get(key, 0), _BOT_START_MS - tf_ms)
        if s["time_ms"] <= thr:
            continue
        age_ms = now_ms - (s["time_ms"] + tf_ms)
        if age_ms <= SFP_MAX_SIGNAL_AGE_BARS * tf_ms:
            fresh.append(s)
        else:
            logger.info(f"[SFP-TRADER] {symbol} {tf_label}: SKIP stale {s['kind']} (too old for market entry)")
        _last_processed_signal_ms[key] = max(_last_processed_signal_ms.get(key, 0), s["time_ms"])
    if signals:
        _save_state(_last_processed_signal_ms)

    # دو جهت مخالف روی یک کندل (کندل خیلی بزرگ) → معامله نمی‌شود
    by_bar = {}
    for s in fresh:
        by_bar.setdefault(s["time_ms"], []).append(s)
    for ms_, group in by_bar.items():
        if len(group) > 1:
            logger.warning(f"[SFP-TRADER] {symbol} {tf_label}: opposite SFPs on one bar — skipped")
            fresh = [x for x in fresh if x["time_ms"] != ms_]

    logger.info(f"[SFP-TRADER] {symbol} {tf_label}: signals_total={len(signals)} fresh={len(fresh)}")

    for s in fresh:
        try:
            _execute(s, symbol, tf, df, public, exchange, ledger, leverage_map,
                     min_order_cost, send_fn, base_capital, balance_use_ratio)
        except Exception as e:
            logger.exception(f"[SFP-TRADER] {symbol} {tf_label}: trade error: {e}")
    return True


def process_sfp_signals(public, exchange, ledger, leverage_map, send_telegram_fn,
                        symbols, timeframes, base_capital=None, min_order_cost=5.0,
                        balance_use_ratio=SFP_BALANCE_USE_RATIO, dtm_timeframes=(), dtm_symbols=None):
    """از حلقه‌ی اصلی bot.py در هر چرخه صدا زده می‌شود؛ هر (نماد، تایم‌فریم) یک‌بار به‌ازای هر کندل بسته."""
    global _state_loaded
    if not _state_loaded:
        _state_loaded = True
        loaded = _load_state()
        if loaded:
            _last_processed_signal_ms.update(loaded)
            logger.info(f"[SFP-TRADER] LOADED {len(loaded)} state entries")

    if hasattr(ledger, "set_event_callback") and not ledger.has_event_callback():
        import tg_messages as _tgm

        def _on_event(ev, row, fresh):          # اعلان نتیجه‌ی معامله (فقط رویدادهای تازه)
            if fresh and ev != "RISK_FREE":
                _safe_send(send_telegram_fn, _tgm.trade_update_card(ev, row))
        ledger.set_event_callback(_on_event)

    base_cap = base_capital if (base_capital and base_capital > 0) else SFP_BASE_CAPITAL
    now_ts = time.time()

    for tf in timeframes:
        tf_sec = int(tf) * 60
        boundary = int(now_ts // tf_sec) * tf_sec
        for symbol in symbols:
            key = (symbol, tf)
            try:
                if now_ts < boundary + SFP_BOUNDARY_SETTLE_SEC:
                    continue
                if boundary <= _last_boundary.get(key, 0):
                    continue
                att = (symbol, tf, boundary)
                _boundary_attempts[att] = _boundary_attempts.get(att, 0) + 1

                done = _process_one(symbol, tf, public, exchange, ledger, leverage_map,
                                    send_telegram_fn, base_cap, min_order_cost,
                                    balance_use_ratio,
                                    update_ledger=not (dtm_symbols is not None
                                                       and str(tf) in {str(x) for x in dtm_timeframes}
                                                       and symbol in set(dtm_symbols)))
                if done or _boundary_attempts[att] >= SFP_MAX_ATTEMPTS_PER_BOUNDARY:
                    if not done:
                        logger.error(f"[SFP-TRADER] {symbol} {_tf_label(tf)}: giving up on boundary {boundary}")
                    _last_boundary[key] = boundary
                    for k in [k for k in _boundary_attempts if k[0] == symbol and k[1] == tf and k[2] <= boundary]:
                        _boundary_attempts.pop(k, None)
            except Exception as e:
                logger.exception(f"[SFP-TRADER] {symbol} {_tf_label(tf)}: cycle error: {e}")
