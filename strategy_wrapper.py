"""
DTM Strategy Wrapper

This module is intentionally NOT a @pyne script.

strategy.py is loaded only through PyneCore ScriptRunner so that
PyneCore can perform its AST transformation and inject the required
persistent Series state (__state__) correctly.
"""

import logging
from pathlib import Path
from datetime import time as dt_time
import json
import traceback
import time as _time
import math as _math

from pynecore.core.ohlcv import OHLCV
from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
from pynecore.core.script_runner import ScriptRunner

logger = logging.getLogger("STRATEGY_WRAPPER")

STRATEGY_PATH = Path(__file__).resolve().parent / "strategy.py"

# مطابق TICK_SIZES / PRICE_PRECISION در bot.py
SYMBOL_TICK_INFO = {
    "LTCUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "LTC"},
    "DOGEUSDT": {"mintick": 0.00001, "pricescale": 100000, "basecurrency": "DOGE"},
    "ETHUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "ETH"},
    "BNBUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "BNB"},
}

# ============================================================
# تابع ارسال پیام به تلگرام (برای گزارش خطاهای حیاتی)
# ============================================================
def _send_telegram(text):
    """ارسال پیام به تلگرام برای دیباگ"""
    try:
        import requests
        TELEGRAM_BOT_TOKEN = "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE"
        TELEGRAM_CHAT_ID = "7402770612"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=15)
        return r.ok
    except Exception as e:
        logger.error(f"Failed to send telegram: {e}")
        return False


def _is_na(x):
    """بررسی NaN یا None"""
    return x is None or (isinstance(x, float) and _math.isnan(x))


def _compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=5):
    """
    استاپ/تارگت سفارشی — کاملاً مستقل از منطق واگرایی strategy.py.
    
    LONG:  استاپ = پایین‌ترین دره از ۲ دره واگرایی - بافر
           تارگت خام = بالاترین قله بین آن دو دره
           اگر R:R < 2 → تارگت بالا برده می‌شود تا R:R = 2
    
    SHORT: استاپ = بالاترین قله از ۲ قله واگرایی + بافر
           تارگت خام = پایین‌ترین دره بین آن دو قله
           اگر R:R < 2 → تارگت پایین برده می‌شود تا R:R = 2
    """
    def _valid(x):
        return x is not None and not (isinstance(x, float) and _math.isnan(x))

    entry = last_values.get("entry")
    if not _valid(entry):
        return None, None, None

    buffer_abs = buffer_ticks * mintick

    if signal == "LONG":
        low1 = last_values.get("previous_pivot_low_price")
        low2 = last_values.get("pivot_low_price")
        bar1 = last_values.get("previous_pivot_low_index")
        bar2 = last_values.get("pivot_low_index")
        
        if not (_valid(low1) and _valid(low2) and _valid(bar1) and _valid(bar2)):
            logger.warning(f"[SL/TP] LONG: missing pivot data low1={low1} low2={low2} bar1={bar1} bar2={bar2}")
            return None, None, None

        stop = min(low1, low2) - buffer_abs

        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None
        
        # پیدا کردن بالاترین قله بین دو دره
        mid_peak = max(c.high for c in candles[lo:hi + 1])

        risk = entry - stop
        if risk <= 0:
            return None, None, None

        rr = (mid_peak - entry) / risk
        target = mid_peak if rr >= 2 else entry + 2 * risk
        return stop, target, max(rr, 2.0)

    elif signal == "SHORT":
        high1 = last_values.get("previous_pivot_high_price")
        high2 = last_values.get("pivot_high_price")
        bar1 = last_values.get("previous_pivot_high_index")
        bar2 = last_values.get("pivot_high_index")
        
        if not (_valid(high1) and _valid(high2) and _valid(bar1) and _valid(bar2)):
            logger.warning(f"[SL/TP] SHORT: missing pivot data high1={high1} high2={high2} bar1={bar1} bar2={bar2}")
            return None, None, None

        stop = max(high1, high2) + buffer_abs

        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None
        
        # پیدا کردن پایین‌ترین دره بین دو قله
        mid_trough = min(c.low for c in candles[lo:hi + 1])

        risk = stop - entry
        if risk <= 0:
            return None, None, None

        rr = (entry - mid_trough) / risk
        target = mid_trough if rr >= 2 else entry - 2 * risk
        return stop, target, max(rr, 2.0)

    return None, None, None


def calculate_signals(df, symbol="BNBUSDT"):
    import logging
    from pathlib import Path
    from datetime import time as dt_time
    from pynecore.core.ohlcv import OHLCV
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    from pynecore.core.script_runner import ScriptRunner
    import json
    import traceback

    logger = logging.getLogger("STRATEGY_WRAPPER")

    try:
        candles = []

        for idx, row in df.iterrows():
            ts = int(idx.timestamp() * 1000)

            candles.append(
                OHLCV(
                    timestamp=ts,
                    open=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"]),
                    volume=float(row.get("volume", 0)),
                    is_closed=True,
                )
            )

        # ============================================================
        # تشخیص کندل ناقص بر اساس timestamp (نه حذف کورکورانه)
        # ============================================================
        if len(candles) > 1:
            last_open_ts = candles[-1].timestamp / 1000.0  # unix seconds — زمان بازشدن آخرین کندل
            candle_age = _time.time() - last_open_ts

            if candle_age < 60:
                # واقعاً هنوز کامل نشده
                dropped_ts = candles[-1].timestamp
                candles = candles[:-1]
                logger.info(
                    f"Removed last (incomplete) candle | age={candle_age:.1f}s | "
                    f"dropped_open_ts={dropped_ts} | Remaining: {len(candles)}"
                )
            else:
                # صرافی خودش کندل ناقص رو برنگردونده — نباید دوباره حذفش کنیم
                logger.info(
                    f"Last candle already closed (age={candle_age:.1f}s) — NOT dropping. "
                    f"Remaining: {len(candles)}"
                )
        else:
            logger.warning("Only one candle available, cannot remove last candle")

        if len(candles) < 50:
            msg = f"Too few candles: {len(candles)}"
            logger.warning(msg)
            _send_telegram(f"⚠️ WARNING: {msg}")
            return None, None, None, None

        symbol = symbol.upper()
        tick_info = SYMBOL_TICK_INFO.get(
            symbol,
            {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")}
        )

        syminfo = SymInfo(
            prefix="",
            description=symbol,
            ticker=symbol,
            currency="USDT",
            basecurrency=tick_info["basecurrency"],
            period="1",
            type="crypto",
            volumetype="base",
            mintick=tick_info["mintick"],
            pricescale=tick_info["pricescale"],
            minmove=1,
            pointvalue=1.0,
            mincontract=0.0,
            opening_hours=[
                SymInfoInterval(
                    day=0,
                    start=dt_time(0, 0),
                    end=dt_time(23, 59, 59),
                )
            ],
            session_starts=[
                SymInfoSession(day=0, time=dt_time(0, 0))
            ],
            session_ends=[
                SymInfoSession(day=0, time=dt_time(23, 59, 59))
            ],
            timezone="UTC",
        )

        inputs = {
            "pivotMode": "سریع (5/3)",
            "rsiLen": 14,
            "macdFast": 12,
            "macdSlow": 26,
            "macdSig": 9,
            "trendLookback": 20,
            "trendSlopeMinPct": 0.05,
            "minConfirmations": "۳ تعییدیه (حداقل مجاز)",
            "enableHidden": True,
            "fibUse618": True,
            "fibUse786": True,
            "fibTolerancePct": 0.5,
            "fibTrendSearchBars": 100,
            "shadowToBodyRatio": 2.0,
            "maxOppositeShadowPct": 20.0,
            "minCandleATRRatio": 0.3,
            "bigCandleAvgLen": 14,
            "bigCandleMultiplier": 1.5,
        }

        def candle_iterator():
            yield from candles

        # ============================================================
        # 🔍 تست pine_range — فقط برای دیباگ (قابل حذف بعد از تست)
        # ============================================================
        try:
            from pynecore import pine_range
            test_result = list(pine_range(2, 5))
            logger.info(f"🔍 TEST pine_range(2, 5) = {test_result}")
            if test_result == [2, 3, 4, 5]:
                logger.info("✅ pine_range is INCLUSIVE (like Pine Script)")
            else:
                logger.warning(f"⚠️ pine_range is NOT inclusive! Expected [2,3,4,5], got {test_result}")
        except Exception as e:
            logger.warning(f"⚠️ Could not test pine_range: {e}")

        runner = ScriptRunner(
            STRATEGY_PATH,
            candle_iterator(),
            syminfo,
            last_bar_index=len(candles) - 1,
            inputs=inputs,
        )

        # ============================================================
        # حلقه تشخیصی با کپی مستقل از دیکشنری
        # ============================================================
        last_values = None
        found_valid = False          # پرچم مستقل، به‌جای تکیه بر truthiness دیکشنری
        result_count = 0
        empty_count = 0
        empty_indices = []
        debug_info = []

        for result in runner.run_iter():
            result_count += 1

            # ============================================================
            # تشخیص دیکشنری معتبر (نه None و نه خالی)
            # ============================================================
            is_valid_dict = (
                len(result) >= 2
                and isinstance(result[1], dict)
                and len(result[1]) > 0
            )

            if is_valid_dict:
                # کپیِ مستقل (snapshot)، نه رفرنس زنده
                last_values = dict(result[1])
                found_valid = True
            elif len(result) >= 2 and isinstance(result[1], dict):
                # دیکشنری هست ولی خالی {}
                empty_count += 1
                if len(empty_indices) < 20:
                    empty_indices.append(result_count)

            # ============================================================
            # دیباگ برای کندل‌های خاص
            # ============================================================
            if result_count <= 5 or result_count % 100 == 0 or result_count > 495:
                debug_info.append({
                    "index": result_count,
                    "len": len(result),
                    "result_1_type": type(result[1]).__name__ if len(result) >= 2 else "N/A",
                    "result_1_len": len(result[1]) if len(result) >= 2 and isinstance(result[1], dict) else "N/A",
                    "result_1_value": str(result[1])[:200] if len(result) >= 2 and result[1] else "EMPTY/None",
                })

        # ============================================================
        # گزارش کامل
        # ============================================================
        logger.info(f"Total results: {result_count} | Empty dicts: {empty_count} | Empty at indices (first 20): {empty_indices} | Found valid: {found_valid}")

        if not found_valid:            # به‌جای `if not last_values:`
            error_msg = f"""
🔴 ERROR: No valid dictionary found in ScriptRunner output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 STATISTICS:
  - Total results: {result_count}
  - Empty dicts: {empty_count}
  - Empty indices (first 20): {empty_indices}
  - Found valid: {found_valid}
  - Symbol: {symbol}
  - Candles: {len(candles)}

📋 DEBUG INFO:
{json.dumps(debug_info, indent=2, ensure_ascii=False)}

🔧 INTERPRETATION:
  - If found_valid is False, but debug_info shows valid dicts:
    → The dict object was cleared after the loop (reference issue).
    → Fixed by using `dict(result[1])` to create an independent copy.

  - If empty_count > 1:
    → An error occurred inside main() (e.g., index out of range).
    → PyneCore returned {{}} instead of raising an exception.
    → Check strategy.py for index bounds.

  - If empty_count == 0:
    → No issue found.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            logger.warning(error_msg)
            _send_telegram(error_msg)
            return None, None, None, None

        # ============================================================
        # استخراج سیگنال از last_values
        # ============================================================
        signal = None
        entry = None
        
        if isinstance(last_values, dict):
            signal = last_values.get("signal")
            entry = last_values.get("entry")
        else:
            error_msg = f"""
⚠️ WARNING: last_values is not a dictionary

Type: {type(last_values).__name__}
Value: {str(last_values)[:500]}
"""
            logger.warning(error_msg)
            _send_telegram(error_msg)

        if signal not in ("LONG", "SHORT"):
            signal = None

        # ============================================================
        # لاگ تشخیصی برای پیوت‌های جدید (چرا سیگنال نمی‌ده)
        # ============================================================
        try:
            if not _is_na(last_values.get("pivot_low")) or not _is_na(last_values.get("pivot_high")):
                logger.info(
                    "[PIVOT DEBUG] %s | new_low=%s new_high=%s | "
                    "CD+base=%s HD+base=%s trend_up_ok=%s | "
                    "CD-base=%s HD-base=%s trend_down_ok=%s | final_signal=%s",
                    symbol,
                    last_values.get("pivot_low"), last_values.get("pivot_high"),
                    last_values.get("classic_bullish_base"), last_values.get("hidden_bullish_base"),
                    last_values.get("trend_bullish_ok"),
                    last_values.get("classic_bearish_base"), last_values.get("hidden_bearish_base"),
                    last_values.get("trend_bearish_ok"),
                    signal,
                )
        except Exception as e:
            logger.warning(f"[PIVOT DEBUG] Failed to log: {e}")

        # ============================================================
        # محاسبه استاپ و تارگت
        # ============================================================
        stop_price, target_price, rr_value = None, None, None
        
        if signal in ("LONG", "SHORT"):
            stop_price, target_price, rr_value = _compute_stop_target(
                candles, signal, last_values, tick_info["mintick"], buffer_ticks=5
            )
            logger.info(
                f"[SL/TP] {symbol} {signal} | entry={entry} | stop={stop_price} | "
                f"target={target_price} | R:R={rr_value}"
            )

        # ============================================================
        # گزارش نتیجه نهایی
        # ============================================================
        result_msg = f"""
✅ calculate_signals result:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Symbol: {symbol}
  Signal: {signal}
  Entry: {entry}
  Stop Loss: {stop_price}
  Take Profit: {target_price}
  R:R: {rr_value}
  Total Results: {result_count}
  Empty dicts: {empty_count}
  Empty indices (first 20): {empty_indices}
  Found valid: {found_valid}
  Last Values Keys: {list(last_values.keys())[:10] if isinstance(last_values, dict) else 'N/A'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        logger.info(result_msg)
        
        # ارسال به تلگرام فقط برای ۴ بار اول
        if not hasattr(calculate_signals, "_telegram_counter"):
            calculate_signals._telegram_counter = 0
        
        if calculate_signals._telegram_counter < 4:
            _send_telegram(result_msg)
            calculate_signals._telegram_counter += 1

        return signal, entry, stop_price, target_price

    except Exception as e:
        # ============================================================
        # گزارش کامل خطا با traceback
        # ============================================================
        tb = traceback.format_exc()
        error_msg = f"""
❌ FATAL ERROR in calculate_signals

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ERROR TYPE: {type(e).__name__}
📌 ERROR MESSAGE: {str(e)}

📋 FULL TRACEBACK:
{tb}

🔧 POSSIBLE CAUSES:
  1. ScriptRunner initialization failed
  2. Strategy.py has syntax errors
  3. PyneCore version mismatch
  4. Input parameters are incorrect
  5. Symbol info is invalid
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        logger.error(error_msg)
        _send_telegram(error_msg)
        return None, None, None, None
