import os
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
    "PUMPUSDT": {"mintick": 0.00001, "pricescale": 100000, "basecurrency": "PUMP"},
}

# حداقل نسبت ریسک به ریوارد قابل قبول
MIN_RR = 3.0

# پارامترهای جستجوی پیوت گسترده برای استاپ
STOP_SEARCH_WINDOW = 350   # حداکثر تعداد کندل به عقب که بررسی می‌شود
STOP_PIVOT_LEFT = 1        # تعداد کندل سمت چپ برای تایید پیوت (مطابق "سریع ۵/۳")
STOP_PIVOT_RIGHT = 1       # تعداد کندل سمت راست برای تایید پیوت


# ═══════════════════════════════════════════════════════════
# 🎯 فیلتر روش E: per-symbol blacklist بر اساس type
# =============================================================
# بک‌تست ۷ روزه (۱۲-۱۸ سپتامبر، با ریسک فری):
#   LTC  → CD+ و HD+  → Expectancy +0.250
#   DOGE → HD- فقط     → Expectancy +0.273
#   ETH  → همه ۴ نوع    → Expectancy +0.340
#   BNB  → همه ۴ نوع    → Expectancy +0.613
# نتیجه: Expectancy +0.571R، +61.72R در ۷ روز
# ═══════════════════════════════════════════════════════════
PER_SYMBOL_BLACKLIST = {
    "LTCUSDT":  ["CD-", "HD-"],
    "DOGEUSDT": ["CD-", "CD+", "HD+"],
    "ETHUSDT":  [],
    "BNBUSDT":  [],
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


# ═══════════════════════════════════════════════════════════
# 🆕 جستجوی پیوت گسترده برای تعیین استاپ نهایی
# ═══════════════════════════════════════════════════════════
def _is_confirmed_pivot_low(candles, i, leftbars, rightbars):
    """
    بررسی می‌کند آیا کندل با ایندکس i یک دره‌ی (Pivot Low) تایید شده است؛
    یعنی low آن کندل، پایین‌ترین low در بازه‌ی [i-leftbars, i+rightbars] باشد.
    """
    lo = i - leftbars
    hi = i + rightbars
    if lo < 0 or hi >= len(candles):
        return False
    pivot_low = candles[i].low
    for j in range(lo, i):
        if candles[j].low < pivot_low:
            return False
    for j in range(i + 1, hi + 1):
        if candles[j].low < pivot_low:
            return False
    return True


def _is_confirmed_pivot_high(candles, i, leftbars, rightbars):
    """
    بررسی می‌کند آیا کندل با ایندکس i یک قله‌ی (Pivot High) تایید شده است؛
    یعنی high آن کندل، بالاترین high در بازه‌ی [i-leftbars, i+rightbars] باشد.
    """
    lo = i - leftbars
    hi = i + rightbars
    if lo < 0 or hi >= len(candles):
        return False
    pivot_high = candles[i].high
    for j in range(lo, i):
        if candles[j].high > pivot_high:
            return False
    for j in range(i + 1, hi + 1):
        if candles[j].high > pivot_high:
            return False
    return True


def _find_extended_stop_pivot(candles, signal, older_pivot_bar, extreme_price,
                               buffer_abs, search_window=STOP_SEARCH_WINDOW,
                               leftbars=STOP_PIVOT_LEFT, rightbars=STOP_PIVOT_RIGHT):
    """
    از کندلِ قدیمی‌تر بین دو پیوت واگرایی (older_pivot_bar) به عقب حرکت می‌کند و
    نزدیک‌ترین پیوت تاییدشده (دره برای LONG، قله برای SHORT) را پیدا می‌کند که
    از extreme_price (پایین‌ترین/بالاترین قیمت بین دو پیوت واگرایی) هم فراتر رفته
    باشد (پایین‌تر برای LONG، بالاتر برای SHORT).

    حداکثر تا search_window کندل به عقب جستجو می‌کند و نزدیک‌ترین مورد را
    برمی‌گرداند (اولین موردی که در حرکت رو به عقب پیدا شود).

    خروجی: (stop_price, pivot_index) یا (None, None) اگر چیزی پیدا نشد.
    """
    if older_pivot_bar is None or extreme_price is None:
        return None, None

    older_pivot_bar = int(older_pivot_bar)
    search_start = max(0, older_pivot_bar - search_window)

    # حرکت رو به عقب از نزدیک‌ترین کندل قبل از older_pivot_bar
    for i in range(older_pivot_bar - 1, search_start - 1, -1):
        if signal == "LONG":
            if not _is_confirmed_pivot_low(candles, i, leftbars, rightbars):
                continue
            candidate_low = candles[i].low
            if candidate_low < extreme_price:
                return candidate_low - buffer_abs, i
        else:  # SHORT
            if not _is_confirmed_pivot_high(candles, i, leftbars, rightbars):
                continue
            candidate_high = candles[i].high
            if candidate_high > extreme_price:
                return candidate_high + buffer_abs, i

    return None, None


def _compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=2):
    """
    استاپ/تارگت سفارشی — کاملاً مستقل از منطق واگرایی strategy.py.

    ── تعیین استاپ (نسخه جدید) ──────────────────────────────
    به‌جای استفاده‌ی مستقیم از پایین‌ترین (LONG) / بالاترین (SHORT) دو پیوت
    واگرایی، ابتدا به عقب‌تر از پیوت قدیمی‌تر (older) دو پیوت واگرایی حرکت
    می‌کنیم (حداکثر تا ۳۵۰ کندل قبل) و نزدیک‌ترین دره/قلهٔ کاملاً تایید شده
    (پیوت واقعی کندل‌به‌کندل، نه صرفاً یک کندل ساده) را پیدا می‌کنیم که از
    هر دو پیوت واگرایی «فراتر» رفته باشد:
        LONG  → دره‌ای با low پایین‌تر از پایین‌ترین دو دره‌ی واگرایی
        SHORT → قله‌ای با high بالاتر از بالاترین دو قله‌ی واگرایی
    اگر چنین پیوتی پیدا شد، استاپ = آن سطح ± بافر.
    اگر پیدا نشد (در بازهٔ جستجو موجود نبود)، دقیقاً طبق منطق قبلی عمل
    می‌شود: استاپ = min/max دو پیوت واگرایی ± بافر (fallback ایمن).

    ── تعیین تارگت ───────────────────────────────────────────
    LONG:  تارگت خام = بالاترین قله بین دو دره واگرایی.
           اگر R:R < 3 → تارگت بالا برده می‌شود تا R:R = 3.
    SHORT: تارگت خام = پایین‌ترین دره بین دو قله واگرایی.
           اگر R:R < 3 → تارگت پایین برده می‌شود تا R:R = 3.

    خروجی چهارم (structural_level):
        LONG → بالاترین قلهٔ بین دو دره | SHORT → پایین‌ترین درهٔ بین دو قله
        (فقط برای محاسبهٔ نقطهٔ ریسک فری استفاده می‌شود)
    """
    def _valid(x):
        return x is not None and not (isinstance(x, float) and _math.isnan(x))

    entry = last_values.get("entry")
    if not _valid(entry):
        return None, None, None, None

    buffer_abs = buffer_ticks * mintick

    if signal == "LONG":
        low1 = last_values.get("previous_pivot_low_price")
        low2 = last_values.get("pivot_low_price")
        bar1 = last_values.get("previous_pivot_low_index")
        bar2 = last_values.get("pivot_low_index")

        if not (_valid(low1) and _valid(low2) and _valid(bar1) and _valid(bar2)):
            logger.warning(f"[SL/TP] LONG: missing pivot data low1={low1} low2={low2} bar1={bar1} bar2={bar2}")
            return None, None, None, None

        # ── استاپ: fallback (منطق قدیم) ──
        fallback_low = min(low1, low2)
        fallback_stop = fallback_low - buffer_abs

        # ── استاپ: جستجوی پیوت گسترده (منطق جدید) ──
        older_bar = min(int(bar1), int(bar2))
        extended_stop, pivot_idx = _find_extended_stop_pivot(
            candles, "LONG", older_bar, fallback_low, buffer_abs
        )

        if extended_stop is not None:
            stop = extended_stop
            logger.info(
                f"[SL/TP] LONG extended stop used | pivot_idx={pivot_idx} "
                f"({_fmt_time(candles, pivot_idx)}) | stop={stop} | fallback_would_be={fallback_stop}"
            )
        else:
            stop = fallback_stop
            logger.info(
                f"[SL/TP] LONG no extended pivot found within {STOP_SEARCH_WINDOW} bars "
                f"before bar={older_bar} → using fallback stop={stop}"
            )

        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None, None

        # پیدا کردن بالاترین قله بین دو دره
        mid_peak = max(c.high for c in candles[lo:hi + 1])

        risk = entry - stop
        if risk <= 0:
            return None, None, None, None

        rr = (mid_peak - entry) / risk
        target = mid_peak if rr >= MIN_RR else entry + MIN_RR * risk
        return stop, target, max(rr, MIN_RR), mid_peak

    elif signal == "SHORT":
        high1 = last_values.get("previous_pivot_high_price")
        high2 = last_values.get("pivot_high_price")
        bar1 = last_values.get("previous_pivot_high_index")
        bar2 = last_values.get("pivot_high_index")

        if not (_valid(high1) and _valid(high2) and _valid(bar1) and _valid(bar2)):
            logger.warning(f"[SL/TP] SHORT: missing pivot data high1={high1} high2={high2} bar1={bar1} bar2={bar2}")
            return None, None, None, None

        # ── استاپ: fallback (منطق قدیم) ──
        fallback_high = max(high1, high2)
        fallback_stop = fallback_high + buffer_abs

        # ── استاپ: جستجوی پیوت گسترده (منطق جدید) ──
        older_bar = min(int(bar1), int(bar2))
        extended_stop, pivot_idx = _find_extended_stop_pivot(
            candles, "SHORT", older_bar, fallback_high, buffer_abs
        )

        if extended_stop is not None:
            stop = extended_stop
            logger.info(
                f"[SL/TP] SHORT extended stop used | pivot_idx={pivot_idx} "
                f"({_fmt_time(candles, pivot_idx)}) | stop={stop} | fallback_would_be={fallback_stop}"
            )
        else:
            stop = fallback_stop
            logger.info(
                f"[SL/TP] SHORT no extended pivot found within {STOP_SEARCH_WINDOW} bars "
                f"before bar={older_bar} → using fallback stop={stop}"
            )

        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None, None

        # پیدا کردن پایین‌ترین دره بین دو قله
        mid_trough = min(c.low for c in candles[lo:hi + 1])

        risk = stop - entry
        if risk <= 0:
            return None, None, None, None

        rr = (entry - mid_trough) / risk
        target = mid_trough if rr >= MIN_RR else entry - MIN_RR * risk
        return stop, target, max(rr, MIN_RR), mid_trough

    return None, None, None, None


# ═══════════════════════════════════════════════════════════
# 🎯 Pine-Exact Parity (100% match with Pine Script)
# ═══════════════════════════════════════════════════════════
HIST_TOLERANCE = 0.03  # tolerance for near-zero hist

def _py_check_color_change(hist_series, bar_index_current, bar_start, bar_end, need_red):
    """
    Shobeh-sazi-e daghigh-e checkColorChange-e Pine ba tolerance.
    hist nazdik-e sefr (|h| <= 0.03) = sefr dar nazar gerefte mishe.
    """
    if bar_start is None or bar_end is None:
        return False
    try:
        bar_start = int(bar_start)
        bar_end = int(bar_end)
    except (ValueError, TypeError):
        return False
    if bar_end <= bar_start:
        return False
    start_offset = bar_index_current - (bar_end - 1)
    end_offset = bar_index_current - (bar_start + 1)
    if start_offset < 0 or end_offset > 5000 or end_offset < start_offset:
        return False
    for j in range(start_offset, end_offset + 1):
        idx = bar_index_current - j
        if idx < 0 or idx >= len(hist_series):
            continue
        h = hist_series[idx]
        if h is None:
            continue
        if abs(h) <= HIST_TOLERANCE:
            continue
        if need_red and h < 0:
            return True
        if not need_red and h > 0:
            return True
    return False


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
        # ============================================================
        tf_minutes = int(timeframe)
        COMPLETION_SAFETY_BUFFER_SEC = 5
        completion_threshold_sec = tf_minutes * 60 + COMPLETION_SAFETY_BUFFER_SEC

        if len(candles) > 1:
            last_open_ts = candles[-1].timestamp / 1000.0
            candle_age = _time.time() - last_open_ts

            if candle_age < completion_threshold_sec:
                dropped_ts = candles[-1].timestamp
                candles = candles[:-1]
                logger.info(
                    f"Removed last (incomplete) candle | tf={tf_minutes}m | age={candle_age:.1f}s | "
                    f"threshold={completion_threshold_sec}s | dropped_open_ts={dropped_ts} | "
                    f"Remaining: {len(candles)}"
                )
            else:
                logger.info(
                    f"Last candle already closed | tf={tf_minutes}m | age={candle_age:.1f}s | "
                    f"threshold={completion_threshold_sec}s — NOT dropping. "
                    f"Remaining: {len(candles)}"
                )
        else:
            logger.warning("Only one candle available, cannot remove last candle")

        signal_bar_ts_ms = candles[-1].timestamp if len(candles) > 0 else None

        if len(candles) < 50:
            msg = f"Too few candles: {len(candles)}"
            logger.warning(msg)
            _send_telegram(f"⚠️ WARNING: {msg}")
            return None, None, None, None, None, None

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
        # 📌 نمایش نسخه نصب شده و اجرایی PyneCore
        # ============================================================
        try:
            from importlib.metadata import version
            runtime_version = version("pynesys-pynecore")
            logger.info(f"📌 PyneCore Runtime Version: {runtime_version}")
        except Exception:
            try:
                import pkg_resources
                runtime_version = pkg_resources.get_distribution("pynesys-pynecore").version
                logger.info(f"📌 PyneCore Runtime Version: {runtime_version}")
            except Exception:
                runtime_version = None
                logger.warning("⚠️ Could not detect PyneCore runtime version")

        try:
            import subprocess
            result = subprocess.run(
                ["pip", "show", "pynesys-pynecore"],
                capture_output=True, text=True
            )
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    installed_version = line.split(":")[1].strip()
                    logger.info(f"📦 PyneCore Installed Version: {installed_version}")
                    break
        except Exception:
            installed_version = None
            logger.warning("⚠️ Could not detect PyneCore installed version")

        if runtime_version and installed_version and runtime_version != installed_version:
            logger.warning(f"⚠️ VERSION MISMATCH! Runtime={runtime_version}, Installed={installed_version}")

        # ============================================================
        # 🔍 تست pine_range — فقط برای دیباگ
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

        # ─── Load Pine HL lookup ───
        try:
            import pine_hl_lookup as _phl
            _log_path = os.getenv("PINE_HL_LOG", "").strip()
            _offset = int(os.getenv("PINE_HL_OFFSET", "400"))
            if _log_path:
                _n = _phl.load(_log_path, offset=_offset)
                _trend_log = os.getenv("PINE_HL_TREND_LOG", _log_path).strip()
                if _trend_log:
                    _tn = _phl.load_trend(_trend_log)
                    logger.info(f"[PINE-HL] trend loaded {_tn} entries")
                logger.info(f"[PINE-HL] loaded {_n} entries (offset={_offset})")
            else:
                logger.info("[PINE-HL] PINE_HL_LOG not set — fallback to reference")
        except Exception as _e:
            logger.warning(f"[PINE-HL] load failed: {_e}")

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
        found_valid = False
        result_count = 0
        empty_count = 0
        empty_indices = []
        debug_info = []

        # 🎯 Pine-Exact: hist history for checkColorChange
        hist_history = []

        for result in runner.run_iter():
            result_count += 1

            is_valid_dict = (
                len(result) >= 2
                and isinstance(result[1], dict)
                and len(result[1]) > 0
            )

            if is_valid_dict:
                last_values = dict(result[1])
                found_valid = True
                hist_history.append(result[1].get("macd_histogram"))
            elif len(result) >= 2 and isinstance(result[1], dict):
                empty_count += 1
                if len(empty_indices) < 20:
                    empty_indices.append(result_count)

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

        if not found_valid:
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
            return None, None, None, None, None, None

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

        # ═══════════════════════════════════════════════════════════
        # 🎯 Pine-Exact Parity: checkColorChange filter (tolerance=0.03)
        # ═══════════════════════════════════════════════════════════
        if signal in ("LONG", "SHORT") and found_valid and hist_history:
            try:
                if signal == "SHORT":
                    b1 = last_values.get("previous_pivot_high_index")
                    b2 = last_values.get("pivot_high_index")
                    need_red = True
                else:
                    b1 = last_values.get("previous_pivot_low_index")
                    b2 = last_values.get("pivot_low_index")
                    need_red = False
                bar_idx = len(hist_history) - 1
                ok = _py_check_color_change(hist_history, bar_idx, b1, b2, need_red)
                if not ok:
                    logger.info(f"[PARITY] checkColorChange filtered: {signal} (b1={b1} b2={b2})")
                    signal = None
                    entry = None
            except Exception as e:
                logger.warning(f"[PARITY] checkColorChange error: {e}")

        # ============================================================
        # لاگ تشخیصی DIVCHECK
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
                    symbol,
                    last_values.get("previous_pivot_high_price"),
                    _fmt_time(candles, b1),
                    last_values.get("pivot_high_price"),
                    _fmt_time(candles, b2),
                    last_values.get("ph_rsi_1"),
                    last_values.get("ph_rsi_2"),
                    last_values.get("ph_macdline_1"),
                    last_values.get("ph_macdline_2"),
                    last_values.get("ph_hist_1"),
                    last_values.get("ph_hist_2"),
                    last_values.get("both_peaks_green"),
                    last_values.get("macd_color_changed_highs"),
                    last_values.get("trend_bearish_ok"),
                    last_values.get("classic_bearish_base"),
                    last_values.get("hidden_bearish_base"),
                    (signal == "SHORT"),
                    prom,
                    last_values.get("ph1_open"),
                    last_values.get("ph1_high"),
                    last_values.get("ph1_low"),
                    last_values.get("ph1_close"),
                    last_values.get("ph2_open"),
                    last_values.get("ph2_high"),
                    last_values.get("ph2_low"),
                    last_values.get("ph2_close"),
                    last_values.get("total_bars_fed"),
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
                    symbol,
                    last_values.get("previous_pivot_low_price"),
                    _fmt_time(candles, b1),
                    last_values.get("pivot_low_price"),
                    _fmt_time(candles, b2),
                    last_values.get("pl_rsi_1"),
                    last_values.get("pl_rsi_2"),
                    last_values.get("pl_macdline_1"),
                    last_values.get("pl_macdline_2"),
                    last_values.get("pl_hist_1"),
                    last_values.get("pl_hist_2"),
                    last_values.get("both_troughs_red"),
                    last_values.get("macd_color_changed_lows"),
                    last_values.get("trend_bullish_ok"),
                    last_values.get("classic_bullish_base"),
                    last_values.get("hidden_bullish_base"),
                    (signal == "LONG"),
                    prom,
                    last_values.get("pl1_open"),
                    last_values.get("pl1_high"),
                    last_values.get("pl1_low"),
                    last_values.get("pl1_close"),
                    last_values.get("pl2_open"),
                    last_values.get("pl2_high"),
                    last_values.get("pl2_low"),
                    last_values.get("pl2_close"),
                    last_values.get("total_bars_fed"),
                )
        except Exception as e:
            logger.warning(f"[DIVCHECK] Failed to log: {e}")
            pass

        # ============================================================
        # 🔬 لاگ تشخیصی فوق‌تخصصی
        # ============================================================
        signal_type = None  # 🆕 برای استفاده در ادامه (فیلتر E)
        try:
            signal_type = None
            if last_values.get("final_classic_bearish"):
                signal_type = "CD-"
            elif last_values.get("final_classic_bullish"):
                signal_type = "CD+"
            elif last_values.get("final_hidden_bullish"):
                signal_type = "HD+"
            elif last_values.get("final_hidden_bearish"):
                signal_type = "HD-"

            score_cd_minus = last_values.get("score_classic_bearish", "N/A")
            score_cd_plus = last_values.get("score_classic_bullish", "N/A")
            score_hd_plus = last_values.get("score_hidden_bullish", "N/A")
            score_hd_minus = last_values.get("score_hidden_bearish", "N/A")

            score_detail_cd_minus = last_values.get("score_cd_minus_detail", {})
            score_detail_cd_plus = last_values.get("score_cd_plus_detail", {})
            score_detail_hd_plus = last_values.get("score_hd_plus_detail", {})
            score_detail_hd_minus = last_values.get("score_hd_minus_detail", {})

            base_cd_minus = last_values.get("classic_bearish_base", False)
            base_cd_plus = last_values.get("classic_bullish_base", False)
            base_hd_plus = last_values.get("hidden_bullish_base", False)
            base_hd_minus = last_values.get("hidden_bearish_base", False)

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

            fib_bearish = last_values.get("fib_bearish", False)
            fib_bullish = last_values.get("fib_bullish", False)

            pa_bullish = last_values.get("price_action_bullish", False)
            pa_bearish = last_values.get("price_action_bearish", False)

            min_conf = last_values.get("min_confirmations", "N/A")

            ph2 = last_values.get("pivot_high_price")
            ph1 = last_values.get("previous_pivot_high_price")
            pl2 = last_values.get("pivot_low_price")
            pl1 = last_values.get("previous_pivot_low_price")

            ph2_bar = last_values.get("pivot_high_index")
            ph1_bar = last_values.get("previous_pivot_high_index")
            pl2_bar = last_values.get("pivot_low_index")
            pl1_bar = last_values.get("previous_pivot_low_index")

            prom_high = last_values.get("prominence_high")
            prom_low = last_values.get("prominence_low")

            new_ph = not _is_na(last_values.get("pivot_high"))
            new_pl = not _is_na(last_values.get("pivot_low"))

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

            if signal_type and not (new_ph or new_pl):
                logger.warning(
                    "[SIGNAL_ANOMALY] %s | tf=%s | signal=%s BUT newPH=%s newPL=%s | "
                    "THIS SIGNAL WAS TRIGGERED WITHOUT A NEW PIVOT! | "
                    "ph2=%s ph1=%s pl2=%s pl1=%s",
                    symbol, timeframe if 'timeframe' in locals() else "1",
                    signal_type, new_ph, new_pl,
                    ph2, ph1, pl2, pl1,
                )

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
        stop_price, target_price, rr_value, structural_level = None, None, None, None
        risk_free_pct = None

        if signal in ("LONG", "SHORT"):
            if symbol == "BNBUSDT" or symbol == "ETHUSDT":
                buffer_ticks = 9
            elif symbol == "LTCUSDT" or symbol == "DOGEUSDT":
                buffer_ticks = 3
            elif symbol == "PUMPUSDT":
                buffer_ticks = 1
            else:
                buffer_ticks = 5

            stop_price, target_price, rr_value, structural_level = _compute_stop_target(
                candles, signal, last_values, tick_info["mintick"], buffer_ticks=buffer_ticks
            )
            logger.info(
                f"[SL/TP] {symbol} {signal} | entry={entry} | stop={stop_price} | "
                f"target={target_price} | R:R={rr_value} | buffer={buffer_ticks}"
            )

            # 🛡️ نقطهٔ ریسک فری
            if (structural_level is not None and stop_price is not None
                    and _valid_num(entry) and entry > 0):
                risk_abs = abs(entry - stop_price)
                risk_pct = risk_abs / entry
                if signal == "LONG":
                    struct_pct = (structural_level - entry) / entry
                    risk_free_pct = max(struct_pct, risk_pct)
                else:
                    struct_pct = (entry - structural_level) / entry
                    risk_free_pct = -max(struct_pct, risk_pct)
                logger.info(
                    f"[RISK-FREE] {symbol} {signal} | structural={structural_level} | "
                    f"rf_pct={risk_free_pct:.6f}"
                )

        # ═══════════════════════════════════════════════════════════════
        # 🎯 فیلتر روش E: per-symbol blacklist (قبل از ارسال تلگرام)
        # ═══════════════════════════════════════════════════════════════
        if signal in ("LONG", "SHORT"):
            signal_type_pre = None
            if last_values.get("final_classic_bearish"):
                signal_type_pre = "CD-"
            elif last_values.get("final_classic_bullish"):
                signal_type_pre = "CD+"
            elif last_values.get("final_hidden_bullish"):
                signal_type_pre = "HD+"
            elif last_values.get("final_hidden_bearish"):
                signal_type_pre = "HD-"

            _bl = PER_SYMBOL_BLACKLIST.get(symbol.upper(), [])
            if signal_type_pre in _bl:
                logger.info(f"[FILTER-E] {symbol.upper()} {signal_type_pre} rejected (per-symbol blacklist)")
                return None, None, None, None, None, None

        # ============================================================
        # 📊 گزارش نهایی — قالب حرفه‌ای و خوانا
        # ============================================================
        if signal in ("LONG", "SHORT"):
            emoji = "🟢" if signal == "LONG" else "🔴"
            direction = "خرید" if signal == "LONG" else "فروش"

            stop_distance = abs(stop_price - entry) if stop_price else 0
            target_distance = abs(target_price - entry) if target_price else 0
            stop_pct = (stop_distance / entry * 100) if entry else 0
            target_pct = (target_distance / entry * 100) if entry else 0

            if rr_value and rr_value >= 4:
                rr_status = "عالی 🚀"
            elif rr_value and rr_value >= 3:
                rr_status = "خوب ✅"
            elif rr_value and rr_value >= 2:
                rr_status = "متوسط ⚠️"
            else:
                rr_status = "ضعیف ❌"

            signal_type_map = {
                "CD-": "CD- (واگرایی کلاسیک نزولی)",
                "CD+": "CD+ (واگرایی کلاسیک صعودی)",
                "HD+": "HD+ (واگرایی مخفی صعودی)",
                "HD-": "HD- (واگرایی مخفی نزولی)",
            }
            signal_type_fa = signal_type_map.get(signal_type, signal_type)

            if not hasattr(calculate_signals, "_counter"):
                calculate_signals._counter = 0
            calculate_signals._counter += 1
            trade_id = f"#{calculate_signals._counter:04d}"

            from datetime import datetime, timedelta
            now_utc = datetime.utcnow()
            now_tehran = now_utc + timedelta(hours=3, minutes=30)

            score = 0
            if signal_type == "CD-":
                score = last_values.get("score_classic_bearish", 0)
            elif signal_type == "CD+":
                score = last_values.get("score_classic_bullish", 0)
            elif signal_type == "HD+":
                score = last_values.get("score_hidden_bullish", 0)
            elif signal_type == "HD-":
                score = last_values.get("score_hidden_bearish", 0)

            stars = "⭐" * score + "☆" * (5 - score)

            result_msg = f"""
{emoji} سیگنال {direction} ({signal}) - {symbol} - {timeframe} دقیقه
─────────────────────────────────────────
🆔 شماره: {trade_id}
🕐 زمان: {now_utc.strftime('%H:%M:%S')} UTC ({now_tehran.strftime('%H:%M:%S')} تهران)
─────────────────────────────────────────
📊 ورود: {entry:.2f}
🛑 حد ضرر: {stop_price:.2f} ({stop_distance:.2f}- | {stop_pct:.2f}%)
🎯 هدف: {target_price:.2f} ({target_distance:.2f}+ | {target_pct:.2f}%)
⭐ نسبت ریسک: 1 : {rr_value:.2f} ({rr_status})
📌 نوع: {signal_type_fa}
🏆 امتیاز: {score}/5 {stars}
─────────────────────────────────────────
🔒 وضعیت: {'✅ معتبر' if rr_value and rr_value >= MIN_RR else '⚠️ ریسک بالا'}
"""
            logger.info(result_msg)
            _send_telegram(result_msg)

        else:
            if result_count % 10 == 0:
                status_msg = f"🔄 {symbol} {timeframe}دقیقه | {result_count} کندل پردازش شد | وضعیت: {'✅ سالم' if found_valid else '❌ خطا'}"
                logger.info(status_msg)

        # ============================================================
        # 📤 برگرداندن ۶ مقدار
        # ============================================================
        return signal, entry, stop_price, target_price, signal_bar_ts_ms, risk_free_pct

    except Exception as e:
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
        return None, None, None, None, None, None
