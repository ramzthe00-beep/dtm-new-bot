"""
ct_trader.py
============
اجرای مستقل CT + معامله

- در هر چرخه، فقط تایم‌فریم‌هایی که کندلشون تازه بسته شده رو چک می‌کنه
- سیگنال‌های CT رو استخراج و برای هر سیگنال جدید یک سفارش ارسال می‌کنه
- از trade_ledger برای ثبت استفاده می‌کنه
- از thetruetrade.io داده می‌گیره (همون‌طور که خواستی)
"""
import logging
from datetime import datetime, timezone

logger = logging.getLogger("CT_TRADER")

# ═══════════════════════════════════════════════════════════
# پیکربندی
# ═══════════════════════════════════════════════════════════
CT_TRADED_SYMBOLS = ["ETHUSDT", "BTCUSDT", "SOLUSDT", "BNBUSDT"]
CT_TIMEFRAMES = ["60", "240"]   # 1h, 4h

# پنجره‌ی چک بعد از بسته شدن کندل (دقیقه‌های 0 تا این عدد)
CT_CHECK_WINDOW_MINUTES = 4

# State
_last_processed_signal_ms = {}   # {(symbol, timeframe): last_signal_ms}


def _tf_label(tf):
    tf_min = int(tf)
    return f"{tf_min}m" if tf_min < 60 else f"{tf_min//60}h"


def should_check_timeframe(timeframe, now_utc):
    """آیا الان باید این تایم‌فریم رو چک کنیم؟"""
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
    elif tf_min == 1440:  # 1d
        return hour == 0
    else:
        hours = tf_min // 60
        if hours <= 0:
            return True
        return hour % hours == 0


def _execute_ct_trade(sig, symbol, timeframe, public, exchange, ledger,
                      leverage_map, base_capital, min_order_cost):
    """اجرای یک معامله CT"""
    direction = sig['direction']   # "LONG" / "SHORT"
    entry = sig['entry']
    stop = sig['stop']
    target = sig['target']
    signal_ms = sig['time_ms']
    kind = sig['kind']
    tf_label = _tf_label(timeframe)

    # ─── محاسبه RISK_PCT از سیگنال ───
    if direction == "LONG":
        if entry <= stop:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label}: invalid LONG (entry<=stop)")
            return
        stop_pct = (entry - stop) / entry
        target_pct = (target - entry) / entry
    else:
        if stop <= entry:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label}: invalid SHORT (stop<=entry)")
            return
        stop_pct = (stop - entry) / entry
        target_pct = (entry - target) / entry

    if stop_pct <= 0 or target_pct <= 0:
        logger.warning(f"[CT-TRADER] {symbol} {tf_label}: invalid pct")
        return

    # ─── قیمت لحظه‌ای برای اجرا (از thetruetrade.io) ───
    df_now = public.fetch_ohlcv(symbol, "1")
    if df_now is None or df_now.empty:
        logger.warning(f"[CT-TRADER] {symbol}: cannot fetch current price")
        return
    current_price = float(df_now['close'].iloc[-1])

    # ─── exec prices (درصدی از قیمت لحظه‌ای) ───
    if direction == "LONG":
        exec_stop = current_price * (1 - stop_pct)
        exec_target = current_price * (1 + target_pct)
    else:
        exec_stop = current_price * (1 + stop_pct)
        exec_target = current_price * (1 - target_pct)

    # ─── محاسبه capital ───
    allowed_leverage = leverage_map.get(symbol, 50)
    old_leverage = 1.0 / stop_pct
    if old_leverage > allowed_leverage:
        required_capital = (old_leverage / allowed_leverage) * base_capital
        mode = "INCREASED"
    else:
        required_capital = base_capital
        mode = "BASE"

    # ─── ثبت در ledger ───
    try:
        ledger.record_signal(
            symbol=symbol,
            timeframe=timeframe,
            direction=direction,
            entry=current_price,
            stop=exec_stop,
            target=exec_target,
            entry_time_ms=signal_ms,
            leverage=allowed_leverage,
            order_placed=None,
            order_reason=f"CT-{kind}",
        )
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol}: record_signal failed: {e}")

    # ─── Balance check ───
    try:
        balance = exchange.fetch_balance()
    except Exception as e:
        logger.error(f"[CT-TRADER] {symbol}: fetch_balance failed: {e}")
        return

    if balance < required_capital:
        logger.warning(
            f"[CT-TRADER] {symbol} {tf_label} {kind} {direction}: "
            f"insufficient balance ({balance:.4f} < {required_capital:.4f})"
        )
        return

    capital = required_capital

    if capital < min_order_cost:
        logger.warning(
            f"[CT-TRADER] {symbol} {tf_label} {kind} {direction}: "
            f"capital {capital:.4f} < min {min_order_cost}"
        )
        return

    # ─── ارسال سفارش ───
    logger.info(
        f"[CT-TRADER] {symbol} {tf_label} {kind} {direction}: "
        f"price={current_price:.4f} SL={exec_stop:.4f} TP={exec_target:.4f} "
        f"stop_pct={stop_pct*100:.3f}% capital={capital:.4f} "
        f"leverage={allowed_leverage} mode={mode}"
    )

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
            logger.info(f"[CT-TRADER] {symbol} {tf_label}: order placed ✅")
        else:
            logger.warning(f"[CT-TRADER] {symbol} {tf_label}: order failed ❌")
    except Exception as e:
        logger.exception(f"[CT-TRADER] {symbol} {tf_label}: create_order exception: {e}")


def process_ct_signals(public, exchange, ledger, leverage_map, base_capital, min_order_cost):
    """
    پردازش سیگنال‌های CT در یک چرخه.
    این تابع از loop اصلی bot.py صدا زده می‌شه.
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
                # ─── دریافت داده از thetruetrade.io ───
                df = public.fetch_ohlcv(symbol, tf)
                if df is None or df.empty:
                    continue

                # ─── به‌روزرسانی معاملات باز CT ───
                try:
                    ledger.update_open_trades(symbol, tf, df)
                except Exception as e:
                    logger.error(f"[CT-TRADER] {symbol} {tf_label}: update_open_trades failed: {e}")

                # ─── اجرای CT ───
                signals = run_ct_strategy(df, symbol, tf)
                signals = [s for s in signals if s is not None]
                if not signals:
                    continue

                signals.sort(key=lambda x: x['time_ms'] or 0)
                last_signal_ms = signals[-1]['time_ms'] or 0

                # ─── اولین بار: seed (بدون معامله) ───
                if key not in _last_processed_signal_ms:
                    _last_processed_signal_ms[key] = last_signal_ms
                    logger.info(
                        f"[CT-TRADER] {symbol} {tf_label}: seeded at ms={last_signal_ms}"
                    )
                    continue

                # ─── پیدا کردن سیگنال‌های جدید ───
                threshold_ms = _last_processed_signal_ms[key]
                new_signals = [s for s in signals if (s['time_ms'] or 0) > threshold_ms]

                if not new_signals:
                    continue

                logger.info(
                    f"[CT-TRADER] {symbol} {tf_label}: {len(new_signals)} new signal(s)"
                )

                for s in new_signals:
                    try:
                        _execute_ct_trade(
                            s, symbol, tf, public, exchange, ledger,
                            leverage_map, base_capital, min_order_cost
                        )
                    except Exception as e:
                        logger.exception(f"[CT-TRADER] {symbol} {tf_label}: trade failed: {e}")

                _last_processed_signal_ms[key] = last_signal_ms

            except Exception as e:
                logger.exception(f"[CT-TRADER] {symbol} {tf_label}: error: {e}")