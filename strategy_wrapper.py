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
        # مهم: حذف کندل آخر (درحال‌شکل‌گیری)
        # ============================================================
        # آخرین ردیف df معمولاً کندل درحال‌شکل‌گیری (هنوز نبسته) است،
        # چون fetch_ohlcv با to=now صدا زده می‌شود. ta.pivothigh/pivotlow به
        # rightBars کندلِ *بعد* از پیوت نیاز دارند که شامل همین کندل جاری هم
        # می‌شود؛ اگر این کندل هنوز نهایی نشده باشد، تأیید/رد Pivot می‌تواند
        # هر بار polling نتیجه‌ی متفاوتی بدهد. Pine واقعی فقط روی کندل بسته‌شده
        # (alert.freq_once_per_bar_close) قضاوت می‌کند، پس ما هم باید همین کار
        # را بکنیم: آخرین کندل ناقص را کنار می‌گذاریم.
        if len(candles) > 1:
            candles = candles[:-1]
            logger.info(f"Removed last (incomplete) candle. Remaining candles: {len(candles)}")
        else:
            logger.warning("Only one candle available, cannot remove last candle")

        if len(candles) < 50:
            msg = f"Too few candles: {len(candles)}"
            logger.warning(msg)
            _send_telegram(f"⚠️ WARNING: {msg}")
            return None, None

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
            return None, None

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
        # گزارش نتیجه نهایی
        # ============================================================
        result_msg = f"""
✅ calculate_signals result:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Symbol: {symbol}
  Signal: {signal}
  Entry: {entry}
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

        return signal, entry

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
        return None, None
