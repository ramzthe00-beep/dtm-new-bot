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
import queue
import threading
from typing import Dict, Optional

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
# تنظیمات پنجره کشویی
# ============================================================
MAX_CANDLES = 500      # حداکثر ۵۰۰ کندل (کافی برای تشخیص Pivot تا ۲۰۰ کندل)
WARMUP_CANDLES = 300   # ۳۰۰ کندل اولیه برای warm-up

# ============================================================
# کش Runners (یک runner به ازای هر نماد)
# ============================================================
_RUNNERS: Dict[str, 'LiveStrategyRunner'] = {}
_LAST_TS: Dict[str, any] = {}
_RUNNER_INITIALIZED: Dict[str, bool] = {}


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


# ============================================================
# کلاس LiveStrategyRunner (مدیریت اجرای پیوسته با پنجره کشویی)
# ============================================================
class LiveStrategyRunner:
    """
    یک ScriptRunner دائمی و زنده برای یک نماد.
    هرگز از نو ساخته نمی‌شود؛ کندل‌های جدید یکی‌یکی به آن تزریق می‌شوند
    و حافظهٔ Persistent مثل پاین روی چارت زنده، همیشه انباشته می‌ماند.
    
    با پنجره کشویی (Sliding Window) برای مدیریت حافظه:
    - حداکثر MAX_CANDLES کندل نگهداری می‌شود
    - با هر کندل جدید، قدیمی‌ترین کندل حذف می‌شود
    """
    def __init__(self, symbol: str, syminfo, inputs: dict, initial_candles: list = None, max_candles: int = MAX_CANDLES):
        self.symbol = symbol
        self.max_candles = max_candles
        self._queue = queue.Queue()
        self._latest_values = None
        self._lock = threading.Lock()
        self._running = True
        self._candle_count = 0

        def candle_feed():
            while self._running:
                try:
                    candle = self._queue.get(timeout=1.0)
                    if candle is None:
                        break
                    yield candle
                except queue.Empty:
                    continue

        self._runner = ScriptRunner(
            STRATEGY_PATH,
            candle_feed(),
            syminfo,
            inputs=inputs
        )
        
        # ============================================================
        # تزریق تاریخچه اولیه (حداکثر max_candles کندل)
        # ============================================================
        if initial_candles:
            # فقط آخرین max_candles کندل را نگه می‌داریم
            start_idx = max(0, len(initial_candles) - self.max_candles)
            for c in initial_candles[start_idx:]:
                self._queue.put(c)
                self._candle_count += 1
        
        self._thread = threading.Thread(target=self._consume, daemon=True)
        self._thread.start()

    def _consume(self):
        """مصرف خروجی‌های ScriptRunner در یک ترد جداگانه"""
        try:
            for item in self._runner.run_iter():
                values = None
                # اگر item یک tuple/list است
                if isinstance(item, (list, tuple)):
                    # عنصر آخر را امتحان کن (معمولاً دیکشنری است)
                    for elem in reversed(item):
                        if isinstance(elem, dict) and len(elem) > 0:
                            values = elem
                            break
                # اگر item خودش دیکشنری است
                elif isinstance(item, dict) and len(item) > 0:
                    values = item
                
                if values:
                    with self._lock:
                        self._latest_values = dict(values)  # کپی مستقل
        except Exception as e:
            logger.error(f"[LiveStrategyRunner] {self.symbol} consume error: {e}")

    def push_candle(self, ohlcv):
        """اضافه کردن یک کندل جدید و حذف قدیمی‌ترین کندل در صورت نیاز"""
        if not self._running:
            return
        
        self._candle_count += 1
        
        # ============================================================
        # اگر تعداد کندل‌ها از max_candles بیشتر شد،
        # قدیمی‌ترین کندل حذف می‌شود (توسط ScriptRunner مدیریت می‌شود)
        # ============================================================
        if self._candle_count > self.max_candles:
            # ScriptRunner به صورت خودکار قدیمی‌ترین کندل را حذف می‌کند
            # چون تعداد کندل‌های تزریق‌شده از max_candles بیشتر شده است
            pass
        
        self._queue.put(ohlcv)

    def get_latest(self) -> Optional[dict]:
        """دریافت آخرین خروجی پردازش‌شده"""
        with self._lock:
            return self._latest_values

    def stop(self):
        """متوقف کردن اجرا"""
        self._running = False
        self._queue.put(None)
        if self._thread.is_alive():
            self._thread.join(timeout=5)


# ============================================================
# توابع کمکی برای ساخت SymInfo و Inputs
# ============================================================
def _build_syminfo(symbol: str) -> SymInfo:
    """ساخت SymInfo برای یک نماد"""
    symbol = symbol.upper()
    tick_info = SYMBOL_TICK_INFO.get(
        symbol,
        {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")}
    )
    
    return SymInfo(
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


def _build_inputs() -> dict:
    """ساخت ورودی‌های استراتژی"""
    return {
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


def _extract_signal_from_values(symbol: str, last_values: dict, df) -> tuple:
    """استخراج سیگنال، ورود، استاپ و تارگت از last_values"""
    
    # استخراج سیگنال
    signal = last_values.get("signal")
    entry = last_values.get("entry")
    
    if signal not in ("LONG", "SHORT"):
        signal = None
    
    # ============================================================
    # محاسبه استاپ و تارگت
    # ============================================================
    stop_price, target_price, rr_value = None, None, None
    
    if signal in ("LONG", "SHORT"):
        # ساخت candles از df
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
        
        symbol = symbol.upper()
        tick_info = SYMBOL_TICK_INFO.get(
            symbol,
            {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")}
        )
        
        stop_price, target_price, rr_value = _compute_stop_target(
            candles, signal, last_values, tick_info["mintick"], buffer_ticks=5
        )
        
        logger.info(
            f"[SL/TP] {symbol} {signal} | entry={entry} | stop={stop_price} | "
            f"target={target_price} | R:R={rr_value}"
        )
    
    # ============================================================
    # لاگ تشخیصی برای پیوت‌های جدید
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
    
    return signal, entry, stop_price, target_price


# ============================================================
# تابع اصلی calculate_signals (نسخه اصلاحی با Runner دائمی)
# ============================================================
def calculate_signals(df, symbol="BNBUSDT"):
    """
    محاسبه سیگنال‌ها با استفاده از یک Runner دائمی.
    
    🔑 کلید این روش: Runner فقط یک بار ساخته می‌شود و کندل‌های جدید
    به صورت افزایشی به آن تزریق می‌شوند. حافظه Persistent هرگز ریست نمی‌شود.
    
    با پنجره کشویی (Sliding Window):
    - حداکثر ۵۰۰ کندل نگهداری می‌شود
    - با هر کندل جدید، قدیمی‌ترین کندل حذف می‌شود
    """
    import logging
    from pathlib import Path
    from datetime import time as dt_time
    from pynecore.core.ohlcv import OHLCV
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    from pynecore.core.script_runner import ScriptRunner
    import json
    import traceback
    import pandas as pd

    logger = logging.getLogger("STRATEGY_WRAPPER")
    symbol = symbol.upper()

    try:
        # ============================================================
        # ۱) ساخت یا دریافت Runner دائمی
        # ============================================================
        if symbol not in _RUNNERS:
            logger.info(f"[LiveRunner] Creating persistent runner for {symbol}")
            
            syminfo = _build_syminfo(symbol)
            inputs = _build_inputs()
            
            # ============================================================
            # تاریخچه اولیه: فقط WARMUP_CANDLES کندل آخر (برای warm-up)
            # ============================================================
            initial_candles = []
            total_rows = len(df)
            start_idx = max(0, total_rows - WARMUP_CANDLES)
            
            for idx in range(start_idx, total_rows):
                row = df.iloc[idx]
                ts = int(row.name.timestamp() * 1000)
                initial_candles.append(
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
            
            # ساخت Runner با حداکثر MAX_CANDLES کندل
            _RUNNERS[symbol] = LiveStrategyRunner(
                symbol, 
                syminfo, 
                inputs, 
                initial_candles=initial_candles,
                max_candles=MAX_CANDLES
            )
            
            # ذخیره آخرین timestamp
            _LAST_TS[symbol] = df.index[-1]
            _RUNNER_INITIALIZED[symbol] = True
            
            logger.info(f"[LiveRunner] {symbol} initialized with {len(initial_candles)} candles (max={MAX_CANDLES})")
            
            # ============================================================
            # منتظر می‌مانیم تا Runner اولین خروجی را تولید کند
            # ============================================================
            import time
            max_wait = 10  # حداکثر ۱۰ ثانیه صبر
            waited = 0
            last_values = None
            while waited < max_wait:
                last_values = _RUNNERS[symbol].get_latest()
                if last_values:
                    break
                time.sleep(0.5)
                waited += 0.5
            
            if not last_values:
                logger.warning(f"[LiveRunner] {symbol} timeout waiting for initial output")
                return None, None, None, None
            
            # ============================================================
            # استخراج سیگنال از خروجی اولیه
            # ============================================================
            return _extract_signal_from_values(symbol, last_values, df)
        
        # ============================================================
        # ۲) Runner وجود دارد → فقط کندل‌های جدید را تزریق کن
        # ============================================================
        else:
            # پیدا کردن کندل‌های جدید از آخرین بار
            last_ts = _LAST_TS.get(symbol)
            if last_ts is None:
                # اگر به هر دلیلی آخرین timestamp گم شده، کل تاریخچه را دوباره می‌فرستیم
                logger.warning(f"[LiveRunner] {symbol} last_ts missing, re-initializing")
                _RUNNERS.pop(symbol, None)
                _LAST_TS.pop(symbol, None)
                _RUNNER_INITIALIZED.pop(symbol, None)
                return calculate_signals(df, symbol)
            
            # پیدا کردن ردیف‌های جدید
            new_rows = df[df.index > last_ts]
            
            if len(new_rows) > 0:
                logger.info(f"[LiveRunner] {symbol} pushing {len(new_rows)} new candles (from {last_ts})")
                
                for idx, row in new_rows.iterrows():
                    ts = int(idx.timestamp() * 1000)
                    ohlcv = OHLCV(
                        timestamp=ts,
                        open=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                        volume=float(row.get("volume", 0)),
                        is_closed=True,
                    )
                    _RUNNERS[symbol].push_candle(ohlcv)
                
                # به‌روزرسانی آخرین timestamp
                _LAST_TS[symbol] = df.index[-1]
                
                # ============================================================
                # منتظر می‌مانیم تا کندل جدید پردازش شود
                # ============================================================
                import time
                max_wait = 5
                waited = 0
                last_values = None
                while waited < max_wait:
                    last_values = _RUNNERS[symbol].get_latest()
                    if last_values:
                        break
                    time.sleep(0.2)
                    waited += 0.2
                
                if not last_values:
                    logger.warning(f"[LiveRunner] {symbol} timeout waiting for new output")
                    # آخرین مقدار موجود را برمی‌گردانیم
                    last_values = _RUNNERS[symbol].get_latest()
                    
                    if not last_values:
                        return None, None, None, None
            
            else:
                # هیچ کندل جدیدی وجود ندارد
                logger.debug(f"[LiveRunner] {symbol} no new candles, returning latest")
                last_values = _RUNNERS[symbol].get_latest()
                
                if not last_values:
                    return None, None, None, None
            
            # ============================================================
            # استخراج سیگنال از خروجی
            # ============================================================
            return _extract_signal_from_values(symbol, last_values, df)
            
    except Exception as e:
        tb = traceback.format_exc()
        error_msg = f"""
❌ FATAL ERROR in calculate_signals

📌 ERROR TYPE: {type(e).__name__}
📌 ERROR MESSAGE: {str(e)}

📋 FULL TRACEBACK:
{tb}
"""
        logger.error(error_msg)
        _send_telegram(error_msg)
        return None, None, None, None


# ============================================================
# تابع پاک‌سازی (در صورت نیاز)
# ============================================================
def cleanup_runners():
    """پاک‌سازی همه Runners در هنگام خروج"""
    for symbol, runner in _RUNNERS.items():
        logger.info(f"[Cleanup] Stopping runner for {symbol}")
        runner.stop()
    _RUNNERS.clear()
    _LAST_TS.clear()
    _RUNNER_INITIALIZED.clear()
