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

        runner = ScriptRunner(
            STRATEGY_PATH,
            candle_iterator(),
            syminfo,
            last_bar_index=len(candles) - 1,
            inputs=inputs,
        )

        last_values = None
        result_count = 0
        debug_info = []

        for result in runner.run_iter():
            result_count += 1
            
            # ============================================================
            # دیباگ کامل برای ۵ کندل اول و هر ۱۰۰ کندل
            # ============================================================
            if result_count <= 5 or result_count % 100 == 0:
                debug_info.append({
                    "index": result_count,
                    "len": len(result),
                    "types": [type(x).__name__ for x in result],
                    "result_1_type": type(result[1]).__name__ if len(result) >= 2 else "N/A",
                    "result_1_is_dict": isinstance(result[1], dict) if len(result) >= 2 else False,
                    "result_1_is_not_none": result[1] is not None if len(result) >= 2 else False,
                    "result_1_value": str(result[1])[:200] if len(result) >= 2 and result[1] is not None else "None/Empty",
                })
            
            if len(result) >= 2 and result[1]:
                if isinstance(result[1], dict):
                    last_values = result[1]
                else:
                    # اگر dict-like است ولی زیرکلاس dict نیست، سعی می‌کنیم به دیکشنری تبدیل کنیم
                    try:
                        # برخی از اشیاء dict-like متد to_dict دارند
                        if hasattr(result[1], 'to_dict'):
                            last_values = result[1].to_dict()
                        else:
                            # سعی می‌کنیم با vars() یا dir() اطلاعات بگیریم
                            last_values = dict(result[1]) if hasattr(result[1], '__dict__') else result[1]
                    except Exception as conv_err:
                        logger.warning(f"Could not convert result[1] to dict: {conv_err}")
                        last_values = result[1]

        # ============================================================
        # گزارش کامل دیباگ
        # ============================================================
        logger.info(f"Total results from run_iter: {result_count}")
        
        if not last_values:
            error_msg = f"""
🔴 ERROR: ScriptRunner returned no values

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 STATISTICS:
  - Total results: {result_count}
  - Symbol: {symbol}
  - Candles: {len(candles)}
  - Last values: {last_values}

📋 DEBUG INFO (first 5 results):
{json.dumps(debug_info[:5], indent=2, ensure_ascii=False)}

🔧 POSSIBLE CAUSES:
  1. result[1] is None for all iterations
  2. result[1] is not a dict-like object
  3. ScriptRunner is not producing any output
  4. Strategy.py is not returning a dictionary
  5. Input parameters are not being passed correctly

📁 CHECK:
  - Check strategy.py return statement
  - Check if @script.strategy decorator is correct
  - Check if inputs match strategy parameters
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

This may indicate that result[1] is not a dict-like object.
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
  Last Values Keys: {list(last_values.keys())[:10] if isinstance(last_values, dict) else 'N/A'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        logger.info(result_msg)
        _send_telegram(result_msg)

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
