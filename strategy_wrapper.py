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


def _valid_num(x):
    return x is not None and not (isinstance(x, float) and x != x)


def _fmt_time(candles, idx):
    if idx is None or not _valid_num(idx):
        return "NA"
    i = int(idx)
    if 0 <= i < len(candles):
        return str(candles[i].timestamp)
    return "OUT_OF_RANGE"


def _compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=2):
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


def calculate_signals(df, symbol="BNBUSDT", timeframe="1"):
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

        # ===========================================================
        # تشخیص کندل ناقص بر اساس timestamp — آستانه متناسب با تایم‌فریم
        # (قبلاً همیشه ۶۰ ثانیه بود؛ برای تایم‌فریم‌های ۵/۱۵ دقیقه‌ای همین باعث می‌شد
        #  کندلی که هنوز کاملاً باز است اشتباهاً «بسته‌شده» تلقی شود و به استراتژی برسد)
        # ============================================================
        tf_minutes = int(timeframe)
        COMPLETION_SAFETY_BUFFER_SEC = 5  # تأخیر مجاز برای نهایی‌شدن/انتشار کندل توسط صرافی
        completion_threshold_sec = tf_minutes * 60 + COMPLETION_SAFETY_BUFFER_SEC

        if len(candles) > 1:
            last_open_ts = candles[-1].timestamp / 1000.0  # unix seconds — زمان بازشدن آخرین کندل
            candle_age = _time.time() - last_open_ts

            if candle_age < completion_threshold_sec:
                # واقعاً هنوز کامل نشده (نسبت به طول عمر این تایم‌فریم)
                dropped_ts = candles[-1].timestamp
                candles = candles[:-1]
                logger.info(
                    f"Removed last (incomplete) candle | tf={tf_minutes}m | age={candle_age:.1f}s | "
                    f"threshold={completion_threshold_sec}s | dropped_open_ts={dropped_ts} | "
                    f"Remaining: {len(candles)}"
                )
            else:
                # صرافی خودش کندل ناقص رو برنگردونده — نباید دوباره حذفش کنیم
                logger.info(
                    f"Last candle already closed | tf={tf_minutes}m | age={candle_age:.1f}s | "
                    f"threshold={completion_threshold_sec}s — NOT dropping. "
                    f"Remaining: {len(candles)}"
                )
        else:
            logger.warning("Only one candle available, cannot remove last candle")

        # timestamp (ms) کندل بسته‌ی نهایی که واقعاً به استراتژی داده می‌شود —
        # همان کندلی است که هر سیگنالی روی آن محاسبه می‌شود (نه df.index[-1] خام در bot.py،
        # که ممکن است دقیقاً همان کندلی باشد که در بالا به‌عنوان ناقص حذف شد)
        signal_bar_ts_ms = candles[-1].timestamp if len(candles) > 0 else None

        if len(candles) < 50:
            msg = f"Too few candles: {len(candles)}"
            logger.warning(msg)
            _send_telegram(f"⚠️ WARNING: {msg}")
            return None, None, None, None, None

        symbol = symbol.upper()
        tick_info = SYMBOL_TICK_INFO.get(
            symbol,
            {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")}
        )

        syminfo = SymInfo(
            prefix="",
            description=f"{symbol} {timeframe}m",
            ticker=symbol,
            currency="USDT",
            basecurrency=tick_info["basecurrency"],
            period=timeframe,
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
            return None, None, None, None, None

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
        # لاگ تشخیصی DIVCHECK — دقیقاً هم‌ساختار با پاین
        # ============================================================
        # ============================================================
        #        لاگ تشخیصی DIVCHECK — دقیقاً هم‌ساختار با پاین
        # ============================================================
        # ============================================================
        try:
            if not _is_na(last_values.get("pivot_high")):
                b1 = last_values.get("previous_pivot_high_index")
                b2 = last_values.get("pivot_high_index")
                prom = last_values.get("prominence_high")
                logger.info(
                    "[DIVCHECK] %s type=H p1=%s@%s p2=%s@%s rsi1=%s rsi2=%s macd1=%s macd2=%s "
                    "hist1=%s hist2=%s bothPeaksGreen=%s colorChgHigh=%s trendOkBear=%s "
                    "CD-base=%s HD-base=%s final=%s prom=%s "
                    "ph1_o=%s ph1_h=%s ph1_l=%s ph1_c=%s ph2_o=%s ph2_h=%s ph2_l=%s ph2_c=%s bars=%s",
                    symbol,                                                    # 1
                    last_values.get("previous_pivot_high_price"),             # 2
                    _fmt_time(candles, b1),                                   # 3
                    last_values.get("pivot_high_price"),                     # 4
                    _fmt_time(candles, b2),                                   # 5
                    last_values.get("ph_rsi_1"),                             # 6
                    last_values.get("ph_rsi_2"),                             # 7
                    last_values.get("ph_macdline_1"),                        # 8
                    last_values.get("ph_macdline_2"),                        # 9
                    last_values.get("ph_hist_1"),                            # 10
                    last_values.get("ph_hist_2"),                            # 11
                    last_values.get("both_peaks_green"),                     # 12
                    last_values.get("macd_color_changed_highs"),             # 13
                    last_values.get("trend_bearish_ok"),                     # 14
                    last_values.get("classic_bearish_base"),                 # 15
                    last_values.get("hidden_bearish_base"),                  # 16
                    (signal == "SHORT"),                                     # 17
                    prom,                                                    # 18
                    last_values.get("ph1_open"),                             # 19
                    last_values.get("ph1_high"),                             # 20
                    last_values.get("ph1_low"),                              # 21
                    last_values.get("ph1_close"),                            # 22
                    last_values.get("ph2_open"),                             # 23
                    last_values.get("ph2_high"),                             # 24
                    last_values.get("ph2_low"),                              # 25
                    last_values.get("ph2_close"),                            # 26
                    last_values.get("total_bars_fed"), # 27        
                )
            if not _is_na(last_values.get("pivot_low")):
                b1 = last_values.get("previous_pivot_low_index")
                b2 = last_values.get("pivot_low_index")
                prom = last_values.get("prominence_low")
                logger.info(
                    "[DIVCHECK] %s type=L p1=%s@%s p2=%s@%s rsi1=%s rsi2=%s macd1=%s macd2=%s "
                    "hist1=%s hist2=%s bothTroughsRed=%s colorChgLow=%s trendOkBull=%s "
                    "CD+base=%s HD+base=%s final=%s prom=%s "
                    "pl1_o=%s pl1_h=%s pl1_l=%s pl1_c=%s pl2_o=%s pl2_h=%s pl2_l=%s pl2_c=%s bars=%s",
                    symbol,                                                    # 1
                    last_values.get("previous_pivot_low_price"),              # 2
                    _fmt_time(candles, b1),                                   # 3
                    last_values.get("pivot_low_price"),                      # 4
                    _fmt_time(candles, b2),                                   # 5
                    last_values.get("pl_rsi_1"),                             # 6
                    last_values.get("pl_rsi_2"),                             # 7
                    last_values.get("pl_macdline_1"),                        # 8
                    last_values.get("pl_macdline_2"),                        # 9
                    last_values.get("pl_hist_1"),                            # 10
                    last_values.get("pl_hist_2"),                            # 11
                    last_values.get("both_troughs_red"),                     # 12
                    last_values.get("macd_color_changed_lows"),              # 13
                    last_values.get("trend_bullish_ok"),                     # 14
                    last_values.get("classic_bullish_base"),                 # 15
                    last_values.get("hidden_bullish_base"),                  # 16
                    (signal == "LONG"),                                      # 17
                    prom,                                                    # 18
                    last_values.get("pl1_open"),                             # 19
                    last_values.get("pl1_high"),                             # 20
                    last_values.get("pl1_low"),                              # 21
                    last_values.get("pl1_close"),                            # 22
                    last_values.get("pl2_open"),                             # 23
                    last_values.get("pl2_high"),                             # 24
                    last_values.get("pl2_low"),                              # 25
                    last_values.get("pl2_close"),                            # 26
                    last_values.get("total_bars_fed"),                       # 27
                )
        except Exception as e:
            logger.warning(f"[DIVCHECK] Failed to log: {e}")
            pass






        

        # ============================================================
        # 🔬 لاگ تشخیصی فوق‌تخصصی — برای پیدا کردن منشأ سیگنال‌های متفرقه
        # ============================================================
        try:
            # --- A. بررسی ساختار سیگنال نهایی ---
            signal_type = None
            if last_values.get("final_classic_bearish"):
                signal_type = "CD-"
            elif last_values.get("final_classic_bullish"):
                signal_type = "CD+"
            elif last_values.get("final_hidden_bullish"):
                signal_type = "HD+"
            elif last_values.get("final_hidden_bearish"):
                signal_type = "HD-"

            # --- B. بررسی امتیازدهی ---
            score_cd_minus = last_values.get("score_classic_bearish", "N/A")
            score_cd_plus = last_values.get("score_classic_bullish", "N/A")
            score_hd_plus = last_values.get("score_hidden_bullish", "N/A")
            score_hd_minus = last_values.get("score_hidden_bearish", "N/A")

            # --- C. بررسی جزئیات امتیاز ---
            score_detail_cd_minus = last_values.get("score_cd_minus_detail", {})
            score_detail_cd_plus = last_values.get("score_cd_plus_detail", {})
            score_detail_hd_plus = last_values.get("score_hd_plus_detail", {})
            score_detail_hd_minus = last_values.get("score_hd_minus_detail", {})

            # --- D. بررسی شرایط پایه (Base3) ---
            base_cd_minus = last_values.get("classic_bearish_base", False)
            base_cd_plus = last_values.get("classic_bullish_base", False)
            base_hd_plus = last_values.get("hidden_bullish_base", False)
            base_hd_minus = last_values.get("hidden_bearish_base", False)

            # --- E. بررسی شرایط جداگانه ---
            # CD- conditions
            cd_minus_price_hh = last_values.get("pivot_high_price") and last_values.get("previous_pivot_high_price") and \
                                (last_values.get("pivot_high_price") > last_values.get("previous_pivot_high_price"))
            cd_minus_rsi_lh = last_values.get("ph_rsi_2") is not None and last_values.get("ph_rsi_1") is not None and \
                              (last_values.get("ph_rsi_2") < last_values.get("ph_rsi_1"))
            cd_minus_macd_lh = last_values.get("ph_macdline_2") is not None and last_values.get("ph_macdline_1") is not None and \
                               (last_values.get("ph_macdline_2") < last_values.get("ph_macdline_1"))
            cd_minus_hist_lh = last_values.get("ph_hist_2") is not None and last_values.get("ph_hist_1") is not None and \
                               (last_values.get("ph_hist_2") < last_values.get("ph_hist_1"))
            cd_minus_both_green = last_values.get("both_peaks_green", False)
            cd_minus_color_chg = last_values.get("macd_color_changed_highs", False)
            cd_minus_trend_ok = last_values.get("trend_bearish_ok", False)

            # CD+ conditions
            cd_plus_price_ll = last_values.get("pivot_low_price") and last_values.get("previous_pivot_low_price") and \
                               (last_values.get("pivot_low_price") < last_values.get("previous_pivot_low_price"))
            cd_plus_rsi_hl = last_values.get("pl_rsi_2") is not None and last_values.get("pl_rsi_1") is not None and \
                             (last_values.get("pl_rsi_2") > last_values.get("pl_rsi_1"))
            cd_plus_macd_hl = last_values.get("pl_macdline_2") is not None and last_values.get("pl_macdline_1") is not None and \
                              (last_values.get("pl_macdline_2") > last_values.get("pl_macdline_1"))
            cd_plus_hist_hl = last_values.get("pl_hist_2") is not None and last_values.get("pl_hist_1") is not None and \
                              (last_values.get("pl_hist_2") > last_values.get("pl_hist_1"))
            cd_plus_both_red = last_values.get("both_troughs_red", False)
            cd_plus_color_chg = last_values.get("macd_color_changed_lows", False)
            cd_plus_trend_ok = last_values.get("trend_bullish_ok", False)

            # --- F. بررسی فیبوناچی ---
            fib_bearish = last_values.get("fib_bearish", False)
            fib_bullish = last_values.get("fib_bullish", False)

            # --- G. بررسی پرایس‌اکشن ---
            pa_bullish = last_values.get("price_action_bullish", False)
            pa_bearish = last_values.get("price_action_bearish", False)

            # --- H. بررسی minConfirmations ---
            min_conf = last_values.get("min_confirmations", "N/A")

            # --- I. بررسی Pivotها ---
            ph2 = last_values.get("pivot_high_price")
            ph1 = last_values.get("previous_pivot_high_price")
            pl2 = last_values.get("pivot_low_price")
            pl1 = last_values.get("previous_pivot_low_price")

            ph2_bar = last_values.get("pivot_high_index")
            ph1_bar = last_values.get("previous_pivot_high_index")
            pl2_bar = last_values.get("pivot_low_index")
            pl1_bar = last_values.get("previous_pivot_low_index")

            # --- J. بررسی Prominence ---
            prom_high = last_values.get("prominence_high")
            prom_low = last_values.get("prominence_low")

            # --- K. بررسی newPivot ---
            new_ph = not _is_na(last_values.get("pivot_high"))
            new_pl = not _is_na(last_values.get("pivot_low"))

            # ============================================================
            # 📝 لاگ نهایی تشخیصی
            # ============================================================
            logger.info(
                "[SIGNAL_TRACE] %s | tf=%s | signal=%s | score_CD-=%s | score_CD+=%s | score_HD+=%s | score_HD-=%s | "
                "base_CD-=%s | base_CD+=%s | base_HD+=%s | base_HD-=%s | "
                "final_CD-=%s | final_CD+=%s | final_HD+=%s | final_HD-=%s | "
                "minConf=%s | fib_bear=%s | fib_bull=%s | pa_bear=%s | pa_bull=%s | "
                "newPH=%s | newPL=%s | "
                "ph2=%s | ph1=%s | pl2=%s | pl1=%s | "
                "ph2_bar=%s | ph1_bar=%s | pl2_bar=%s | pl1_bar=%s | "
                "prom_high=%s | prom_low=%s | "
                "cd-:priceHH=%s rsiLH=%s macdLH=%s histLH=%s bothGreen=%s colorChg=%s trend=%s | "
                "cd+:priceLL=%s rsiHL=%s macdHL=%s histHL=%s bothRed=%s colorChg=%s trend=%s",
                symbol, timeframe if 'timeframe' in locals() else "1",
                signal_type,
                score_cd_minus, score_cd_plus, score_hd_plus, score_hd_minus,
                base_cd_minus, base_cd_plus, base_hd_plus, base_hd_minus,
                last_values.get("final_classic_bearish"), last_values.get("final_classic_bullish"),
                last_values.get("final_hidden_bullish"), last_values.get("final_hidden_bearish"),
                min_conf, fib_bearish, fib_bullish, pa_bearish, pa_bullish,
                new_ph, new_pl,
                ph2, ph1, pl2, pl1,
                ph2_bar, ph1_bar, pl2_bar, pl1_bar,
                prom_high, prom_low,
                cd_minus_price_hh, cd_minus_rsi_lh, cd_minus_macd_lh, cd_minus_hist_lh, cd_minus_both_green, cd_minus_color_chg, cd_minus_trend_ok,
                cd_plus_price_ll, cd_plus_rsi_hl, cd_plus_macd_hl, cd_plus_hist_hl, cd_plus_both_red, cd_plus_color_chg, cd_plus_trend_ok,
            )

            # ============================================================
            # 🚨 لاگ هشدار برای سیگنال‌های متفرقه (بدون newPivot)
            # ============================================================
            if signal_type and not (new_ph or new_pl):
                logger.warning(
                    "[SIGNAL_ANOMALY] %s | tf=%s | signal=%s BUT newPH=%s newPL=%s | "
                    "THIS SIGNAL WAS TRIGGERED WITHOUT A NEW PIVOT! | "
                    "ph2=%s ph1=%s pl2=%s pl1=%s",
                    symbol, timeframe if 'timeframe' in locals() else "1",
                    signal_type, new_ph, new_pl,
                    ph2, ph1, pl2, pl1,
                )

            # ============================================================
            # 🚨 لاگ هشدار برای سیگنال با امتیاز پایین
            # ============================================================
            if signal_type and score_cd_minus != "N/A" and score_cd_minus < 3 and signal_type == "CD-":
                logger.warning(
                    "[LOW_SCORE] %s | tf=%s | signal=%s | score=%s/5 | "
                    "detail=%s | This signal has LOW score!",
                    symbol, timeframe if 'timeframe' in locals() else "1",
                    signal_type, score_cd_minus, score_detail_cd_minus,
                )

            if signal_type and score_cd_plus != "N/A" and score_cd_plus < 3 and signal_type == "CD+":
                logger.warning(
                    "[LOW_SCORE] %s | tf=%s | signal=%s | score=%s/5 | "
                    "detail=%s | This signal has LOW score!",
                    symbol, timeframe if 'timeframe' in locals() else "1",
                    signal_type, score_cd_plus, score_detail_cd_plus,
                )

        except Exception as e:
            logger.warning(f"[SIGNAL_TRACE] Failed to log: {e}")
            pass
        # ============================================================
        # محاسبه استاپ و تارگت
        # ============================================================
        stop_price, target_price, rr_value = None, None, None

        if signal in ("LONG", "SHORT"):
            # تنظیم buffer_ticks بر اساس نماد
            if symbol == "BNBUSDT" or symbol == "ETHUSDT":
                buffer_ticks = 9
            elif symbol == "LTCUSDT" or symbol == "DOGEUSDT":
                buffer_ticks = 3
            else:
                buffer_ticks = 5  # پیش‌فرض برای سایر ارزها
    
            stop_price, target_price, rr_value = _compute_stop_target(
                candles, signal, last_values, tick_info["mintick"], buffer_ticks=buffer_ticks
            )
            logger.info(
                f"[SL/TP] {symbol} {signal} | entry={entry} | stop={stop_price} | "
                f"target={target_price} | R:R={rr_value} | buffer={buffer_ticks}"
            )
        

        # ============================================================
        # گزارش نتیجه نهایی
        # ============================================================
        result_msg = f"""
✅ calculate_signals result:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Symbol: {symbol}
  Timeframe: {timeframe}m
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

        return signal, entry, stop_price, target_price, signal_bar_ts_ms

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
        return None, None, None, None, None
