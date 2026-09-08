#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest_report.py  (نسخه v8 — با قابلیت‌های پیشرفته اعتبارسنجی)
=======================================
بک‌تست مستقل استراتژی DTM روی داده‌های واقعی Binance Spot + گزارش کامل و تفکیکی
به تلگرام (همه در یک فایل).

🆕 v8: اضافه شدن قابلیت‌های پیشرفته از نسخه بازنویسی‌شده:
  • قفل تک‌اجرایی (RUN_LOCK_FILE) — فقط یک‌بار در هر استارت فرآیند
  • تلگرام مستقل از ربات لایو (BACKTEST_TELEGRAM_BOT_TOKEN/CHAT_ID)
  • حل ابهام استاپ/تارگت هم‌کندل با داده ۱دقیقه‌ای واقعی
  • لاگ کامل الگوریتمی هر سیگنال
  • متریک‌های پیشرفته: Sharpe, Sortino, Calmar, SQN, CAGR, Edge Ratio
  • برچسب اعتبار خودکار (GOOD/SUSPICIOUS/UNRELIABLE)
  • تحلیل سه‌بعدی: ارز × تایم‌فریم × نوع سیگنال
  • اعتبارسنجی نیم‌اول/نیم‌دوم (Half-Split Validation)
  • Monte Carlo Permutation Test (--robust)
  • Walk-Forward Validation (--robust)
  • تخمین زمان اجرا با کالیبراسیون واقعی
  • سیگنال‌های اخیر با بازه متناسب با تایم‌فریم
  • گزارش ۷ روزه اخیر تایم‌فریم ۱ دقیقه (txt + xlsx)
  • تنظیمات صریح pivotMode با مقادیر عددی leftBars/rightBars برای هر تایم‌فریم
  • پارامترهای جدید: --robust, --lookahead-check, --determinism-check, --min-samples

⚠️ فیلتر بهینه‌سازی سیگنال (HD+ و ۶ ترکیب زیان‌ده) همچنان فعال است.
   برای خاموش‌کردن: --no-signal-filter

اجرا:
    python backtest_report.py --days 365 --signal-dump 5000 --force
    python backtest_report.py --days 365 --robust --force
    python backtest_report.py --days 365 --no-signal-filter --force   # نسخه خام
"""

from __future__ import annotations

import os
import sys
import json
import math
import time
import argparse
import logging
import traceback
import statistics
import contextlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import Optional

import requests
import pandas as pd
import numpy as np

# ============================================================
# مسیرها و ثابت‌ها
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
STRATEGY_PATH = BASE_DIR / "strategy.py"
RESULTS_PATH = BASE_DIR / "backtest_results.json"
MARKER_PATH = BASE_DIR / "backtest_report_state.json"
TICK_CACHE_PATH = BASE_DIR / "backtest_tick_cache.json"
RUN_LOCK_FILE = BASE_DIR / ".backtest_run.lock"

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

# 🆕 تلگرام مستقل از ربات لایو
BACKTEST_TELEGRAM_BOT_TOKEN = os.getenv("BACKTEST_TELEGRAM_BOT_TOKEN", "8681448214:AAG4Ve-8GUTtQQS3wb5V9FDcuTeOoGbA4oM")
BACKTEST_TELEGRAM_CHAT_ID = os.getenv("BACKTEST_TELEGRAM_CHAT_ID", "7402770612")
_TELEGRAM_API_BASE = "https://api.telegram.org"
_TELEGRAM_MSG_LIMIT = 4000

# ============================================================
# ✅ ارزهای اصلی
# ============================================================
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "LTCUSDT", "TRXUSDT",
    "BNBUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT", "DOTUSDT"
]

TIMEFRAMES = ["1", "15", "30", "60"]

LEVERAGE_MAP = {
    "BTCUSDT": 150, "ETHUSDT": 50, "LTCUSDT": 75, "TRXUSDT": 75,
    "BNBUSDT": 75, "XRPUSDT": 75, "DOGEUSDT": 75, "ADAUSDT": 75,
    "DOTUSDT": 50,
}

TICK_SIZES = {
    "BTCUSDT": 0.1, "ETHUSDT": 0.01, "LTCUSDT": 0.01, "TRXUSDT": 0.00001,
    "BNBUSDT": 0.01, "XRPUSDT": 0.0001, "DOGEUSDT": 0.00001,
    "ADAUSDT": 0.0001, "DOTUSDT": 0.001,
}

HISTORY_BARS = 500
MIN_ORDER_COST_USDT = 5.0
LIVE_BASE_CAPITAL = 1.5
LIVE_BALANCE_USE_RATIO = 0.70

BASE_CAPITAL = 2.0
DAYS_DEFAULT = 365
BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]
KLINE_LIMIT = 1000
REQUEST_SLEEP = 0.15
MAX_FETCH_ITER = 20000

GENERIC_FALLBACK_TICK = 0.0001

# ============================================================
# 🆕 تنظیمات صریح pivotMode با مقادیر عددی برای هر تایم‌فریم
# ============================================================
PIVOT_MODE_CONFIG = {
    "1": {"leftBars": 5, "rightBars": 3},
    "5": {"leftBars": 5, "rightBars": 3},
    "15": {"leftBars": 5, "rightBars": 5},
    "30": {"leftBars": 5, "rightBars": 5},
    "60": {"leftBars": 5, "rightBars": 5},
    "120": {"leftBars": 5, "rightBars": 5},
    "240": {"leftBars": 5, "rightBars": 5},
    "360": {"leftBars": 5, "rightBars": 5},
    "480": {"leftBars": 5, "rightBars": 5},
    "720": {"leftBars": 5, "rightBars": 5},
    "1440": {"leftBars": 5, "rightBars": 5},
}

STRATEGY_INPUTS = {
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

SCORE_KEYS = {
    "CD-": "score_classic_bearish",
    "CD+": "score_classic_bullish",
    "HD+": "score_hidden_bullish",
    "HD-": "score_hidden_bearish",
}
WD_FA = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
W = "━━━━━━━━━━━━━━━━━━━━"

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BACKTEST")


def get_strategy_inputs(timeframe):
    """دریافت تنظیمات استراتژی با pivotMode صریح و عددی برای هر تایم‌فریم."""
    base = dict(STRATEGY_INPUTS)
    tf_str = str(timeframe)
    pivot_config = PIVOT_MODE_CONFIG.get(tf_str, {"leftBars": 5, "rightBars": 5})
    base["pivotMode"] = {
        "leftBars": pivot_config["leftBars"],
        "rightBars": pivot_config["rightBars"]
    }
    return base


# ============================================================
# فیلتر بهینه‌سازی سیگنال
# ============================================================
EXCLUDED_SIGNAL_TYPES = {"HD+"}

EXCLUDED_SYMBOL_SIGNAL_COMBOS = {
    ("DOTUSDT", "CD+"),
    ("XRPUSDT", "CD+"),
    ("ADAUSDT", "CD-"),
    ("TRXUSDT", "CD-"),
    ("DOGEUSDT", "HD-"),
    ("BTCUSDT", "HD-"),
}


def is_signal_allowed(symbol, signal_type):
    if not signal_type:
        return True
    if signal_type in EXCLUDED_SIGNAL_TYPES:
        return False
    if (symbol, signal_type) in EXCLUDED_SYMBOL_SIGNAL_COMBOS:
        return False
    return True


# ============================================================
# ابزارهای ایمن
# ============================================================
def _f(x):
    try:
        if x is None:
            return None
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except (TypeError, ValueError):
        return None


def _ms_to_iran(ms):
    try:
        return datetime.fromtimestamp(int(ms) / 1000.0, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception:
        return None


def now_iran_str():
    return datetime.now(UTC_TZ).astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")


def today_str():
    return datetime.now(UTC_TZ).astimezone(IRAN_TZ).strftime("%Y-%m-%d")


def utc_ms(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC_TZ)
    return int(dt.astimezone(UTC_TZ).timestamp() * 1000)


def ms_to_dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000.0, tz=UTC_TZ)


def _parse_kv_overrides(items):
    out = {}
    for it in items or []:
        if "=" not in it:
            continue
        k, v = it.split("=", 1)
        k = k.strip().upper()
        try:
            out[k] = float(v.strip())
        except ValueError:
            logger.warning(f"[ARGS] مقدار نامعتبر نادیده گرفته شد: {it}")
    return out


# ============================================================
# 🆕 تلگرام مستقل از ربات لایو
# ============================================================
_telegram_config_warned = False


def _telegram_configured() -> bool:
    global _telegram_config_warned
    ok = bool(BACKTEST_TELEGRAM_BOT_TOKEN and BACKTEST_TELEGRAM_CHAT_ID)
    if not ok and not _telegram_config_warned:
        logger.warning(
            "⚠️ BACKTEST_TELEGRAM_BOT_TOKEN و/یا BACKTEST_TELEGRAM_CHAT_ID تنظیم نشده؛ "
            "هیچ پیامی به تلگرام ارسال نمی‌شود."
        )
        _telegram_config_warned = True
    return ok


def notify_telegram(message: str) -> bool:
    """ارسال پیام به ربات تلگرام مستقل از ربات لایو."""
    if not _telegram_configured():
        return False
    ok_all = True
    chunks = [message[i:i + _TELEGRAM_MSG_LIMIT] for i in range(0, len(message), _TELEGRAM_MSG_LIMIT)] or [message]
    for chunk in chunks:
        try:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{BACKTEST_TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": BACKTEST_TELEGRAM_CHAT_ID, "text": chunk},
                timeout=15,
            )
            if resp.status_code != 200:
                logger.warning(f"ارسال پیام تلگرام شکست خورد ({resp.status_code})")
                ok_all = False
        except Exception as e:
            logger.warning(f"ارسال پیام تلگرام شکست خورد: {e}")
            ok_all = False
    return ok_all


def notify_telegram_document(file_path, caption: str = "") -> bool:
    """ارسال فایل به ربات تلگرام مستقل."""
    if not _telegram_configured():
        return False
    try:
        with open(file_path, "rb") as f:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{BACKTEST_TELEGRAM_BOT_TOKEN}/sendDocument",
                data={"chat_id": BACKTEST_TELEGRAM_CHAT_ID, "caption": caption[:1024]},
                files={"document": (Path(file_path).name, f)},
                timeout=60,
            )
        if resp.status_code != 200:
            logger.warning(f"ارسال فایل به تلگرام شکست خورد ({resp.status_code})")
            return False
        return True
    except Exception as e:
        logger.warning(f"ارسال فایل به تلگرام شکست خورد: {e}")
        return False


# ============================================================
# 🆕 قفل تک‌اجرایی
# ============================================================
def check_and_create_lock() -> bool:
    if RUN_LOCK_FILE.exists():
        try:
            prev_ts = RUN_LOCK_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            prev_ts = "نامشخص"
        logger.warning(f"⏭️ قفل اجرا وجود دارد (زمان شروع قبلی: {prev_ts})")
        return False
    RUN_LOCK_FILE.write_text(datetime.now(UTC_TZ).isoformat(), encoding="utf-8")
    return True


# ============================================================
# 🆕 نگاشت تایم‌فریم به Binance interval
# ============================================================
BINANCE_INTERVAL_MAP = {
    "1": "1m", "3": "3m", "5": "5m", "15": "15m", "30": "30m",
    "60": "1h", "120": "2h", "240": "4h", "360": "6h", "480": "8h",
    "720": "12h", "1440": "1d", "4320": "3d", "10080": "1w",
}


def to_binance_interval(timeframe: str) -> str:
    tf = str(timeframe)
    if tf in BINANCE_INTERVAL_MAP:
        return BINANCE_INTERVAL_MAP[tf]
    logger.warning(f"⚠️ تایم‌فریم {tf} در BINANCE_INTERVAL_MAP نیست؛ حدس '{tf}m' استفاده می‌شود.")
    return f"{tf}m"


UNMAPPED_TIMEFRAME_GUESSES: set[str] = set()


def to_binance_interval_tracked(timeframe: str) -> str:
    tf = str(timeframe)
    if tf not in BINANCE_INTERVAL_MAP:
        UNMAPPED_TIMEFRAME_GUESSES.add(tf)
    return to_binance_interval(tf)


# ============================================================
# 🆕 بازه سیگنال‌های اخیر متناسب با تایم‌فریم
# ============================================================
RECENT_SIGNALS_CALENDAR_DAYS_CONFIRMED = {"1": 7, "5": 22}
RECENT_SIGNALS_CALENDAR_DAYS_PROPOSED = {
    "1": 7, "5": 22, "15": 45, "30": 75, "60": 120, "240": 240,
}


def recent_window_days(timeframe: str) -> tuple[int, bool]:
    tf = str(timeframe)
    if tf in RECENT_SIGNALS_CALENDAR_DAYS_CONFIRMED:
        return RECENT_SIGNALS_CALENDAR_DAYS_CONFIRMED[tf], True
    if tf in RECENT_SIGNALS_CALENDAR_DAYS_PROPOSED:
        return RECENT_SIGNALS_CALENDAR_DAYS_PROPOSED[tf], False
    try:
        tf_min = int(tf)
        x1, y1 = 1.0, 7.0
        x5, y5 = 5.0, 22.0
        slope = (math.log(y5) - math.log(y1)) / (math.log(x5) - math.log(x1))
        days = math.exp(math.log(y1) + slope * (math.log(tf_min) - math.log(x1)))
        return max(1, round(days)), False
    except Exception:
        return 30, False


# ============================================================
# 🆕 کش داده ۱-دقیقه‌ای برای حل ابهام استاپ/تارگت
# ============================================================
_ONE_MIN_CACHE: dict[str, pd.DataFrame] = {}


def get_1m_slice(symbol: str, start_ms: int, end_ms: int) -> Optional[pd.DataFrame]:
    day_key = f"{symbol}:{ms_to_dt(start_ms).strftime('%Y-%m-%d')}"
    day_start = int(datetime(
        ms_to_dt(start_ms).year, ms_to_dt(start_ms).month, ms_to_dt(start_ms).day,
        tzinfo=UTC_TZ
    ).timestamp() * 1000)
    day_end = day_start + 24 * 3600 * 1000

    if day_key not in _ONE_MIN_CACHE:
        try:
            df_day = fetch_klines(symbol, 1, day_start, day_end)
        except Exception as e:
            logger.warning(f"[{symbol}] دریافت داده ۱m برای {day_key} شکست خورد: {e}")
            df_day = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        _ONE_MIN_CACHE[day_key] = df_day
        if len(_ONE_MIN_CACHE) > 400:
            oldest = sorted(_ONE_MIN_CACHE.keys())[0]
            _ONE_MIN_CACHE.pop(oldest, None)

    df_day = _ONE_MIN_CACHE[day_key]
    if df_day.empty:
        return None
    idx_ms = (df_day.index.values.astype("datetime64[ns]").view("int64") // 10 ** 6)
    mask = (idx_ms >= start_ms) & (idx_ms < end_ms)
    sub = df_day.loc[mask]
    return sub if not sub.empty else None


# ============================================================
# 🆕 لاگ کامل الگوریتمی
# ============================================================
class _ListLogHandler(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.records: list[str] = []

    def emit(self, record):
        try:
            self.records.append(self.format(record))
        except Exception:
            pass


@contextlib.contextmanager
def capture_algo_log():
    handler = _ListLogHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
    target_logger = logging.getLogger("STRATEGY_WRAPPER")
    prev_level = target_logger.level
    target_logger.addHandler(handler)
    target_logger.setLevel(logging.DEBUG)
    try:
        yield handler
    finally:
        target_logger.removeHandler(handler)
        target_logger.setLevel(prev_level)


# ============================================================
# موتور استراتژی
# ============================================================
try:
    import strategy_wrapper as _sw
    import trade_ledger as _tl

    from trade_ledger import _hypothetical_pnl_usd as ledger_pnl_usd
    from trade_ledger import BASE_CAPITAL

    _original_send_telegram = getattr(_sw, "_send_telegram", None)
    _sw._send_telegram = lambda *a, **k: True

    for _sym, _tick in TICK_SIZES.items():
        if _sym not in _sw.SYMBOL_TICK_INFO:
            _sw.SYMBOL_TICK_INFO[_sym] = {
                "mintick": _tick,
                "pricescale": int(round(1 / _tick)),
                "basecurrency": _sym.replace("USDT", ""),
            }

    _compute_stop_target = _sw._compute_stop_target
    ENGINE_NAME = "strategy_wrapper (import شد)"
    LOGIC_SOURCE_OK = True
except Exception as e:
    LOGIC_SOURCE_OK = False
    logger.error(f"❌ import از strategy_wrapper/trade_ledger شکست خورد: {e}")
    sys.exit(1)


def _build_syminfo(symbol, timeframe):
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    tick = TICK_SIZES.get(symbol, GENERIC_FALLBACK_TICK)
    return SymInfo(
        prefix="", description=f"{symbol} {timeframe}m", ticker=symbol,
        currency="USDT", basecurrency=symbol.replace("USDT", ""), period=str(timeframe),
        type="crypto", volumetype="base", mintick=tick, pricescale=100,
        minmove=1, pointvalue=1.0, mincontract=0.0,
        opening_hours=[SymInfoInterval(day=0, start=datetime.min.time(), end=datetime.max.time())],
        session_starts=[SymInfoSession(day=0, time=datetime.min.time())],
        session_ends=[SymInfoSession(day=0, time=datetime.max.time())],
        timezone="UTC",
    )


def buffer_ticks_for(symbol):
    if symbol in ("BNBUSDT", "ETHUSDT"):
        return 9
    if symbol in ("LTCUSDT", "DOGEUSDT"):
        return 3
    return 5


def compute_rf_pct(signal, entry, stop, structural_level):
    entry, stop = _f(entry), _f(stop)
    structural_level = _f(structural_level)
    if structural_level is None or stop is None or entry is None or entry <= 0:
        return None
    risk_pct = abs(entry - stop) / entry
    if signal == "LONG":
        return max((structural_level - entry) / entry, risk_pct)
    return -max((entry - structural_level) / entry, risk_pct)


def signal_type_of(lv):
    try:
        if lv.get("final_classic_bearish"):
            return "CD-"
        if lv.get("final_classic_bullish"):
            return "CD+"
        if lv.get("final_hidden_bullish"):
            return "HD+"
        if lv.get("final_hidden_bearish"):
            return "HD-"
    except Exception:
        pass
    return None


def _score_of(lv, st):
    if not st:
        return 0
    v = _f(lv.get(SCORE_KEYS.get(st, "")))
    if v is None:
        return 0
    return int(max(0, min(5, round(v))))


# ============================================================
# دریافت دیتا از Binance Spot
# ============================================================
def fetch_klines(symbol, interval_min, start_ms, end_ms):
    interval = to_binance_interval_tracked(str(interval_min))
    tf_ms = int(interval_min) * 60_000
    all_rows = {}
    cursor = start_ms
    session = requests.Session()
    iters = 0
    while cursor <= end_ms:
        iters += 1
        if iters > MAX_FETCH_ITER:
            raise RuntimeError(f"صفحه‌بندی Binance بیش از {MAX_FETCH_ITER} تکرار طول کشید")
        chunk, last_err = None, None
        for attempt in range(4):
            base = BINANCE_BASES[attempt % len(BINANCE_BASES)]
            try:
                url = (f"{base}/api/v3/klines?symbol={symbol.upper()}&interval={interval}"
                       f"&startTime={cursor}&endTime={end_ms}&limit={KLINE_LIMIT}")
                r = session.get(url, timeout=20)
                if r.status_code in (418, 429):
                    time.sleep(2 ** attempt + 1)
                    continue
                r.raise_for_status()
                data = r.json()
                if not isinstance(data, list):
                    raise ValueError(f"bad payload: {str(data)[:100]}")
                chunk = data
                break
            except Exception as e:
                last_err = e
                time.sleep(0.8 * (attempt + 1))
        if chunk is None:
            raise RuntimeError(f"Binance unreachable {symbol} {interval} @ {cursor}: {last_err}")
        if not chunk:
            break
        added = 0
        for row in chunk:
            try:
                ot = int(row[0])
            except Exception:
                continue
            if ot not in all_rows:
                all_rows[ot] = row
                added += 1
        new_cursor = int(chunk[-1][0]) + tf_ms
        if new_cursor <= cursor:
            new_cursor = cursor + tf_ms
        cursor = new_cursor
        if added == 0 and len(chunk) < KLINE_LIMIT:
            break
        time.sleep(REQUEST_SLEEP)
    if not all_rows:
        return pd.DataFrame()
    rows = sorted(all_rows.values(), key=lambda x: int(x[0]))
    t = [r[0] / 1000.0 for r in rows]
    df = pd.DataFrame({
        "open": pd.to_numeric([r[1] for r in rows], errors="coerce"),
        "high": pd.to_numeric([r[2] for r in rows], errors="coerce"),
        "low": pd.to_numeric([r[3] for r in rows], errors="coerce"),
        "close": pd.to_numeric([r[4] for r in rows], errors="coerce"),
        "volume": pd.to_numeric([r[5] for r in rows], errors="coerce"),
    }, index=pd.to_datetime(t, unit="s", utc=True))
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    df = df.dropna(subset=["open", "high", "low", "close"])
    now_ms = int(time.time() * 1000)
    if rows and int(rows[-1][0]) + tf_ms > now_ms and len(df) > 0:
        df = df.iloc[:-1]
    return df


def df_to_candles(df):
    from pynecore.core.ohlcv import OHLCV
    candles = []
    for idx, row in df.iterrows():
        candles.append(OHLCV(
            timestamp=int(idx.timestamp() * 1000),
            open=float(row["open"]), high=float(row["high"]),
            low=float(row["low"]), close=float(row["close"]),
            volume=float(row.get("volume", 0) or 0), is_closed=True,
        ))
    return candles


def _candles_to_tuples(candles):
    return [(c.timestamp, c.open, c.high, c.low, c.close, c.volume) for c in candles]


def _tuples_to_candles(tuples):
    from pynecore.core.ohlcv import OHLCV
    return [OHLCV(timestamp=t[0], open=t[1], high=t[2], low=t[3], close=t[4], volume=t[5], is_closed=True)
            for t in tuples]


def _extract_hit_from_last_values(lv, i):
    sig = lv.get("signal")
    if sig not in ("LONG", "SHORT"):
        return None
    entry = _f(lv.get("entry"))
    if entry is None or entry <= 0:
        return None
    return (i, lv, sig, entry)


# ============================================================
# 🆕 موتور exact/event-driven (بازسازی دقیق لایو)
# ============================================================
@dataclass
class SignalEvent:
    symbol: str
    timeframe: str
    signal: str
    entry: float
    stop: float
    target: Optional[float]
    signal_bar_ts_ms: int
    risk_free_pct: Optional[float]
    algo_log: str = ""
    window_len: int = 0
    signal_type: str = ""
    score: int = 0


@dataclass
class TradeResult:
    event: SignalEvent
    exit_price: Optional[float] = None
    exit_time_ms: Optional[int] = None
    status: str = "OPEN"
    exit_reason: Optional[str] = None
    resolution_method: str = "no_ambiguity"
    risk_free_armed: bool = False
    risk_free_armed_ms: Optional[int] = None
    pnl_usd: Optional[float] = None
    pnl_r: Optional[float] = None
    mae_pct: Optional[float] = None
    mfe_pct: Optional[float] = None
    bars_held: int = 0


def _build_ohlcv_window(df_full: pd.DataFrame, end_idx: int, history_bars: int) -> pd.DataFrame:
    start_idx = max(0, end_idx - history_bars + 1)
    return df_full.iloc[start_idx:end_idx + 1]


def _run_calculate_signals_capture(df_window: pd.DataFrame, symbol: str, timeframe: str):
    with capture_algo_log() as handler:
        try:
            result = _sw.calculate_signals(df_window, symbol=symbol, timeframe=timeframe)
        except Exception:
            tb = traceback.format_exc()
            handler.records.append(f"EXCEPTION در calculate_signals:\n{tb}")
            result = (None, None, None, None, None, None)
        algo_log = "\n".join(handler.records)
    return result, algo_log


def _process_single_bar(df_full: pd.DataFrame, i: int, symbol: str, timeframe: str,
                         history_bars: int, keep_log: bool = True,
                         apply_signal_filter: bool = True) -> Optional[SignalEvent]:
    window = _build_ohlcv_window(df_full, i, history_bars)
    if len(window) < 50:
        return None

    (signal, entry, stop, target, signal_bar_ts_ms, risk_free_pct), algo_log = \
        _run_calculate_signals_capture(window, symbol, timeframe)

    if signal not in ("LONG", "SHORT") or entry is None or stop is None:
        return None

    return SignalEvent(
        symbol=symbol, timeframe=str(timeframe), signal=signal,
        entry=float(entry), stop=float(stop),
        target=float(target) if target is not None else None,
        signal_bar_ts_ms=int(signal_bar_ts_ms) if signal_bar_ts_ms is not None else int(window.index[-1].timestamp() * 1000),
        risk_free_pct=float(risk_free_pct) if risk_free_pct is not None else None,
        algo_log=algo_log if keep_log else "",
        window_len=len(window),
    )


def _worker_process_range(pickled_args):
    (df_full, lo, hi, symbol, timeframe, history_bars, keep_log, apply_signal_filter) = pickled_args
    out = []
    for i in range(lo, hi):
        ev = _process_single_bar(df_full, i, symbol, timeframe, history_bars, keep_log, apply_signal_filter)
        if ev is not None:
            out.append(ev)
    return out


def generate_signals_exact(df_full: pd.DataFrame, symbol: str, timeframe: str,
                            history_bars: int = HISTORY_BARS,
                            workers: int = 1, keep_log: bool = True,
                            apply_signal_filter: bool = True) -> list[SignalEvent]:
    n = len(df_full)
    if n < 50:
        return []

    if workers and workers > 1:
        try:
            chunks = []
            chunk_size = max(1, math.ceil(n / workers))
            for lo in range(0, n, chunk_size):
                hi = min(n, lo + chunk_size)
                chunks.append((df_full, lo, hi, symbol, timeframe, history_bars, keep_log, apply_signal_filter))
            events: list[SignalEvent] = []
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futures = [ex.submit(_worker_process_range, c) for c in chunks]
                for fut in as_completed(futures):
                    events.extend(fut.result())
            events.sort(key=lambda e: e.signal_bar_ts_ms)
            return events
        except Exception as e:
            logger.warning(f"[{symbol} {timeframe}m] موازی‌سازی شکست خورد ({e})؛ سقوط به تک‌پردازه‌ای.")

    events = []
    for i in range(n):
        ev = _process_single_bar(df_full, i, symbol, timeframe, history_bars, keep_log, apply_signal_filter)
        if ev is not None:
            events.append(ev)
    return events


# ============================================================
# 🆕 حل ابهام استاپ/تارگت هم‌کندل
# ============================================================
def _resolve_ambiguous_candle(symbol: str, candle_ts_ms: int, tf_minutes: int,
                               direction: str, stop: float, target: Optional[float]) -> tuple[Optional[str], str]:
    if tf_minutes <= 1:
        return None, "conservative_assumption"

    start_ms = candle_ts_ms
    end_ms = candle_ts_ms + tf_minutes * 60 * 1000
    sub = get_1m_slice(symbol, start_ms, end_ms)
    if sub is None or sub.empty:
        return None, "conservative_assumption"

    for _, row in sub.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        stop_hit = (lo <= stop) if direction == "LONG" else (hi >= stop)
        target_hit = (target is not None) and ((hi >= target) if direction == "LONG" else (lo <= target))
        if stop_hit and target_hit:
            return "STOP", "intrabar_verified"
        if stop_hit:
            return "STOP", "intrabar_verified"
        if target_hit:
            return "TARGET", "intrabar_verified"
    return None, "intrabar_verified"


def resolve_trade(ev: SignalEvent, df_full: pd.DataFrame, ts_to_idx: dict,
                   max_bars_forward: int = 100000) -> TradeResult:
    res = TradeResult(event=ev)
    i0 = ts_to_idx.get(ev.signal_bar_ts_ms)
    if i0 is None:
        res.exit_reason = "NO_RESOLUTION"
        return res

    tf_minutes = int(ev.timeframe)
    direction = ev.signal
    entry = ev.entry
    initial_stop = ev.stop
    stop = ev.stop
    target = ev.target
    risk_free_armed = False
    risk_free_pct = ev.risk_free_pct

    mae = 0.0
    mfe = 0.0
    initial_risk = abs(entry - initial_stop)
    if initial_risk <= 0:
        res.exit_reason = "NO_RESOLUTION"
        return res

    n = len(df_full)
    end = min(n, i0 + 1 + max_bars_forward)
    bars_held = 0

    for i in range(i0 + 1, end):
        bars_held += 1
        row = df_full.iloc[i]
        hi, lo = float(row["high"]), float(row["low"])
        candle_ts_ms = int(df_full.index[i].timestamp() * 1000)

        if direction == "LONG":
            adverse = (entry - lo) / initial_risk
            favorable = (hi - entry) / initial_risk
        else:
            adverse = (hi - entry) / initial_risk
            favorable = (entry - lo) / initial_risk
        mae = max(mae, adverse)
        mfe = max(mfe, favorable)

        if not risk_free_armed and risk_free_pct is not None:
            if direction == "LONG":
                rf_trigger = entry * (1 + risk_free_pct)
                rf_crossed = hi >= rf_trigger
            else:
                rf_trigger = entry * (1 - abs(risk_free_pct))
                rf_crossed = lo <= rf_trigger
            if rf_crossed:
                stop = entry
                risk_free_armed = True
                res.risk_free_armed = True
                res.risk_free_armed_ms = candle_ts_ms

        hit_stop = (lo <= stop) if direction == "LONG" else (hi >= stop)
        hit_target = (target is not None) and ((hi >= target) if direction == "LONG" else (lo <= target))

        if hit_stop and hit_target:
            outcome, method = _resolve_ambiguous_candle(
                ev.symbol, candle_ts_ms, tf_minutes, direction, stop, target
            )
            res.resolution_method = method
            if outcome == "TARGET":
                hit_stop, hit_target = False, True
            else:
                hit_stop, hit_target = True, False

        if hit_stop:
            res.status = "WIN" if risk_free_armed else "LOSS"
            res.exit_reason = "RISK_FREE_STOP" if risk_free_armed else "STOP_LOSS"
            res.exit_price = stop
            res.exit_time_ms = candle_ts_ms
            break
        if hit_target:
            res.status = "WIN"
            res.exit_reason = "TARGET"
            res.exit_price = target
            res.exit_time_ms = candle_ts_ms
            break

    res.bars_held = bars_held
    res.mae_pct = round(mae * 100, 3)
    res.mfe_pct = round(mfe * 100, 3)

    if res.status != "OPEN":
        pnl_usd, pnl_r = ledger_pnl_usd(
            direction, entry, initial_stop, res.exit_price,
            LEVERAGE_MAP.get(ev.symbol, 50)
        )
        res.pnl_usd = pnl_usd
        res.pnl_r = pnl_r
    else:
        res.exit_reason = res.exit_reason or "STILL_OPEN_AT_END_OF_DATA"

    return res


# ============================================================
# 🆕 متریک‌های سطح پرتفوی
# ============================================================
def _closed(trades: list[TradeResult]) -> list[TradeResult]:
    return [t for t in trades if t.status in ("WIN", "LOSS") and t.pnl_usd is not None]


def compute_equity_curve(trades: list[TradeResult]) -> pd.Series:
    closed = sorted(_closed(trades), key=lambda t: t.exit_time_ms or 0)
    if not closed:
        return pd.Series(dtype=float)
    times = [ms_to_dt(t.exit_time_ms) for t in closed]
    pnl = [t.pnl_usd for t in closed]
    equity = BASE_CAPITAL + pd.Series(pnl, index=pd.DatetimeIndex(times)).cumsum()
    return equity


def max_drawdown(equity: pd.Series) -> dict:
    if equity.empty:
        return {"max_dd_pct": 0.0, "max_dd_usd": 0.0, "peak_time": None, "valley_time": None}
    running_max = equity.cummax()
    dd_usd = equity - running_max
    dd_pct = dd_usd / running_max.replace(0, np.nan) * 100
    valley_idx = dd_usd.idxmin() if not dd_usd.empty else None
    peak_idx = running_max.loc[:valley_idx].idxmax() if valley_idx is not None else None
    return {
        "max_dd_pct": float(dd_pct.min()) if not dd_pct.empty else 0.0,
        "max_dd_usd": float(dd_usd.min()) if not dd_usd.empty else 0.0,
        "peak_time": peak_idx,
        "valley_time": valley_idx,
    }


def sharpe_sortino_calmar(trades: list[TradeResult], equity: pd.Series) -> dict:
    closed = _closed(trades)
    if len(closed) < 2:
        return {"sharpe": None, "sortino": None, "calmar": None}
    pnl = np.array([t.pnl_usd for t in closed], dtype=float)
    mean, std = pnl.mean(), pnl.std(ddof=1)
    sharpe = (mean / std) * math.sqrt(len(pnl)) if std > 0 else None

    downside = pnl[pnl < 0]
    dstd = downside.std(ddof=1) if len(downside) > 1 else None
    sortino = (mean / dstd) * math.sqrt(len(pnl)) if dstd else None

    dd = max_drawdown(equity)
    total_return_pct = ((equity.iloc[-1] - BASE_CAPITAL) / BASE_CAPITAL * 100) if not equity.empty else 0.0
    calmar = (total_return_pct / abs(dd["max_dd_pct"])) if dd["max_dd_pct"] not in (0, None) else None

    return {"sharpe": sharpe, "sortino": sortino, "calmar": calmar}


def sqn(trades: list[TradeResult]) -> Optional[float]:
    closed = _closed(trades)
    r_values = [t.pnl_r for t in closed if t.pnl_r is not None]
    if len(r_values) < 2:
        return None
    arr = np.array(r_values, dtype=float)
    if arr.std(ddof=1) == 0:
        return None
    return float((arr.mean() / arr.std(ddof=1)) * math.sqrt(len(arr)))


def expectancy(trades: list[TradeResult]) -> dict:
    closed = _closed(trades)
    if not closed:
        return {"expectancy_usd": None, "expectancy_r": None, "win_rate": None, "avg_win": None, "avg_loss": None}
    wins = [t for t in closed if t.status == "WIN"]
    losses = [t for t in closed if t.status == "LOSS"]
    win_rate = len(wins) / len(closed) * 100
    avg_win = statistics.mean([t.pnl_usd for t in wins]) if wins else 0.0
    avg_loss = statistics.mean([t.pnl_usd for t in losses]) if losses else 0.0
    exp_usd = (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)
    r_vals = [t.pnl_r for t in closed if t.pnl_r is not None]
    exp_r = statistics.mean(r_vals) if r_vals else None
    return {
        "expectancy_usd": exp_usd, "expectancy_r": exp_r, "win_rate": win_rate,
        "avg_win": avg_win, "avg_loss": avg_loss,
    }


def profit_factor(trades: list[TradeResult]) -> Optional[float]:
    closed = _closed(trades)
    gross_win = sum(t.pnl_usd for t in closed if t.pnl_usd and t.pnl_usd > 0)
    gross_loss = abs(sum(t.pnl_usd for t in closed if t.pnl_usd and t.pnl_usd < 0))
    if gross_loss == 0:
        return None if gross_win == 0 else float("inf")
    return gross_win / gross_loss


def cagr(equity: pd.Series) -> Optional[float]:
    if equity.empty or len(equity) < 2:
        return None
    days = (equity.index[-1] - equity.index[0]).total_seconds() / 86400.0
    if days <= 0:
        return None
    total_return = equity.iloc[-1] / BASE_CAPITAL
    if total_return <= 0:
        return None
    years = days / 365.25
    return (total_return ** (1 / years) - 1) * 100 if years > 0 else None


def exposure_time(trades: list[TradeResult], total_start_ms: int, total_end_ms: int) -> float:
    closed = _closed(trades)
    if not closed or total_end_ms <= total_start_ms:
        return 0.0
    covered = 0
    for t in sorted(closed, key=lambda t: t.event.signal_bar_ts_ms):
        covered += max(0, (t.exit_time_ms or t.event.signal_bar_ts_ms) - t.event.signal_bar_ts_ms)
    return min(100.0, covered / (total_end_ms - total_start_ms) * 100)


def benchmark_buy_hold(df_full: pd.DataFrame) -> Optional[float]:
    if df_full.empty or len(df_full) < 2:
        return None
    first, last = float(df_full["close"].iloc[0]), float(df_full["close"].iloc[-1])
    if first <= 0:
        return None
    return (last - first) / first * 100


def validity_label(metrics: dict) -> tuple[str, list[str]]:
    reasons = []
    sharpe = metrics.get("sharpe")
    pf = metrics.get("profit_factor")
    win_rate = metrics.get("win_rate")
    n_closed = metrics.get("n_closed", 0)

    label = "GOOD"
    if n_closed < 30:
        label = "UNRELIABLE"
        reasons.append(f"تعداد معاملات بسته‌شده خیلی کم است ({n_closed} < 30)")
    if sharpe is not None and sharpe > 10:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Sharpe غیرعادی بالاست ({sharpe:.2f} > 10)")
    if pf is not None and pf != float("inf") and pf > 100:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Profit Factor غیرعادی بالاست ({pf:.1f} > 100)")
    if pf == float("inf"):
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append("Profit Factor = ∞ (هیچ معامله بازنده‌ای ثبت نشده)")
    if win_rate is not None and win_rate > 95:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Win Rate غیرعادی بالاست ({win_rate:.1f}% > 95%)")
    if not reasons:
        reasons.append("هیچ الگوی مشکوک شناخته‌شده‌ای یافت نشد.")
    return label, reasons


def compute_portfolio_metrics(trades: list[TradeResult], df_full: pd.DataFrame,
                               total_start_ms: int, total_end_ms: int) -> dict:
    closed = _closed(trades)
    equity = compute_equity_curve(trades)
    dd = max_drawdown(equity)
    ssc = sharpe_sortino_calmar(trades, equity)
    exp = expectancy(trades)
    pf = profit_factor(trades)

    win_durations = [t.bars_held for t in closed if t.status == "WIN"]
    loss_durations = [t.bars_held for t in closed if t.status == "LOSS"]

    metrics = {
        "n_signals_total": len(trades),
        "n_closed": len(closed),
        "n_open_at_end": len([t for t in trades if t.status == "OPEN"]),
        "n_wins": len([t for t in closed if t.status == "WIN"]),
        "n_losses": len([t for t in closed if t.status == "LOSS"]),
        "n_target_wins": len([t for t in closed if t.exit_reason == "TARGET"]),
        "n_risk_free_wins": len([t for t in closed if t.exit_reason == "RISK_FREE_STOP"]),
        "win_rate": exp["win_rate"],
        "total_pnl_usd": sum(t.pnl_usd for t in closed if t.pnl_usd is not None),
        "expectancy_usd": exp["expectancy_usd"],
        "expectancy_r": exp["expectancy_r"],
        "avg_win_usd": exp["avg_win"],
        "avg_loss_usd": exp["avg_loss"],
        "profit_factor": pf,
        "sharpe": ssc["sharpe"],
        "sortino": ssc["sortino"],
        "calmar": ssc["calmar"],
        "sqn": sqn(trades),
        "cagr_pct": cagr(equity),
        "max_dd_pct": dd["max_dd_pct"],
        "max_dd_usd": dd["max_dd_usd"],
        "max_dd_peak_time": dd["peak_time"],
        "max_dd_valley_time": dd["valley_time"],
        "exposure_pct": exposure_time(trades, total_start_ms, total_end_ms),
        "benchmark_buy_hold_pct": benchmark_buy_hold(df_full),
        "avg_win_duration_bars": statistics.mean(win_durations) if win_durations else None,
        "avg_loss_duration_bars": statistics.mean(loss_durations) if loss_durations else None,
        "avg_mae_pct": statistics.mean([t.mae_pct for t in closed if t.mae_pct is not None]) if closed else None,
        "avg_mfe_pct": statistics.mean([t.mfe_pct for t in closed if t.mfe_pct is not None]) if closed else None,
        "intrabar_verified_count": len([t for t in trades if t.resolution_method == "intrabar_verified"]),
        "conservative_assumption_count": len([t for t in trades if t.resolution_method == "conservative_assumption"]),
        "no_ambiguity_count": len([t for t in trades if t.resolution_method == "no_ambiguity"]),
    }
    metrics["edge_ratio"] = (
        metrics["avg_mfe_pct"] / metrics["avg_mae_pct"]
        if metrics["avg_mae_pct"] not in (None, 0) and metrics["avg_mfe_pct"] is not None
        else None
    )
    label, reasons = validity_label(metrics)
    metrics["validity_label"] = label
    metrics["validity_reasons"] = reasons
    metrics["equity_curve"] = equity
    return metrics


# ============================================================
# 🆕 تحلیل سه‌بعدی و اعتبارسنجی
# ============================================================
MIN_SAMPLE_SIZE_DEFAULT = 30


def _signal_type_from_log(algo_log: str) -> str:
    for line in algo_log.splitlines():
        if "[SIGNAL_TRACE]" in line and "signal=" in line:
            try:
                part = line.split("signal=", 1)[1]
                return part.split("|", 1)[0].strip()
            except Exception:
                continue
    return "UNKNOWN"


def three_dim_breakdown(all_trades: list[TradeResult], min_samples: int = MIN_SAMPLE_SIZE_DEFAULT) -> list[dict]:
    buckets: dict[tuple, list[TradeResult]] = {}
    for t in _closed(all_trades):
        stype = _signal_type_from_log(t.event.algo_log)
        key = (t.event.symbol, t.event.timeframe, stype)
        buckets.setdefault(key, []).append(t)

    rows = []
    for (symbol, tf, stype), trs in buckets.items():
        n = len(trs)
        wins = [t for t in trs if t.status == "WIN"]
        win_rate = len(wins) / n * 100 if n else 0.0
        total_pnl = sum(t.pnl_usd for t in trs if t.pnl_usd is not None)
        exp_r_vals = [t.pnl_r for t in trs if t.pnl_r is not None]
        exp_r = statistics.mean(exp_r_vals) if exp_r_vals else None
        gross_win = sum(t.pnl_usd for t in trs if t.pnl_usd and t.pnl_usd > 0)
        gross_loss = abs(sum(t.pnl_usd for t in trs if t.pnl_usd and t.pnl_usd < 0))
        pf = (gross_win / gross_loss) if gross_loss > 0 else (float("inf") if gross_win > 0 else None)
        rows.append({
            "symbol": symbol, "timeframe": tf, "signal_type": stype,
            "n": n, "win_rate": win_rate, "total_pnl_usd": total_pnl,
            "expectancy_r": exp_r, "profit_factor": pf,
            "reliable_sample": n >= min_samples,
            "recommendation": (
                "نگه‌داشتن" if (n >= min_samples and total_pnl > 0) else
                "حذف/بررسی بیشتر" if (n >= min_samples and total_pnl <= 0) else
                "نمونه کم — محافظه‌کارانه نگه‌داشته شود"
            ),
        })
    rows.sort(key=lambda r: (r["total_pnl_usd"] if r["total_pnl_usd"] is not None else 0))
    return rows


def half_split_validation(all_trades: list[TradeResult], breakdown: list[dict]) -> list[dict]:
    by_key: dict[tuple, list[TradeResult]] = {}
    for t in _closed(all_trades):
        stype = _signal_type_from_log(t.event.algo_log)
        key = (t.event.symbol, t.event.timeframe, stype)
        by_key.setdefault(key, []).append(t)

    out = []
    for row in breakdown:
        key = (row["symbol"], row["timeframe"], row["signal_type"])
        trs = sorted(by_key.get(key, []), key=lambda t: t.event.signal_bar_ts_ms)
        if len(trs) < min(10, MIN_SAMPLE_SIZE_DEFAULT):
            out.append({**row, "half1_pnl": None, "half2_pnl": None, "consistent": None})
            continue
        mid = len(trs) // 2
        h1, h2 = trs[:mid], trs[mid:]
        pnl1 = sum(t.pnl_usd for t in h1 if t.pnl_usd is not None)
        pnl2 = sum(t.pnl_usd for t in h2 if t.pnl_usd is not None)
        consistent = (pnl1 > 0) == (pnl2 > 0)
        out.append({**row, "half1_pnl": pnl1, "half2_pnl": pnl2, "consistent": consistent})
    return out


def monte_carlo_permutation_test(trades: list[TradeResult], n_permutations: int = 1000, seed: int = 42) -> dict:
    closed = _closed(trades)
    pnls = np.array([t.pnl_usd for t in closed], dtype=float)
    if len(pnls) < 10:
        return {"p_value": None, "note": "نمونه خیلی کم برای Monte Carlo."}
    rng = np.random.default_rng(seed)
    real_total = pnls.sum()
    count_ge = 0
    for _ in range(n_permutations):
        shuffled = rng.permutation(pnls)
        signs = rng.choice([-1, 1], size=len(shuffled))
        sim_total = (np.abs(shuffled) * signs).sum()
        if sim_total >= real_total:
            count_ge += 1
    p_value = count_ge / n_permutations
    return {"p_value": p_value, "n_permutations": n_permutations, "real_total_pnl": real_total}


def walk_forward_validation(df_full: pd.DataFrame, symbol: str, timeframe: str,
                             history_bars: int, workers: int, n_folds: int = 3,
                             apply_signal_filter: bool = True) -> dict:
    n = len(df_full)
    if n < 200:
        return {"folds": [], "note": "داده برای walk-forward کافی نیست."}
    fold_size = n // n_folds
    folds_out = []
    for f in range(n_folds):
        lo = f * fold_size
        hi = n if f == n_folds - 1 else (f + 1) * fold_size
        df_fold = df_full.iloc[lo:hi]
        if len(df_fold) < 60:
            continue
        events = generate_signals_exact(df_fold, symbol, timeframe, history_bars,
                                        workers=workers, keep_log=False,
                                        apply_signal_filter=apply_signal_filter)
        ts_to_idx_fold = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_fold.index)}
        trades = [resolve_trade(ev, df_fold, ts_to_idx_fold) for ev in events]
        closed = _closed(trades)
        total_pnl = sum(t.pnl_usd for t in closed if t.pnl_usd is not None)
        folds_out.append({
            "fold": f + 1,
            "start": str(df_fold.index[0]), "end": str(df_fold.index[-1]),
            "n_signals": len(events), "n_closed": len(closed), "total_pnl_usd": total_pnl,
        })
    profitable_folds = sum(1 for r in folds_out if r["total_pnl_usd"] > 0)
    return {"folds": folds_out, "profitable_folds": profitable_folds, "total_folds": len(folds_out)}


def determinism_check(df_full: pd.DataFrame, symbol: str, timeframe: str,
                       history_bars: int, sample_size: int = 20,
                       apply_signal_filter: bool = True) -> dict:
    n = len(df_full)
    if n < 60:
        return {"checked": 0, "mismatches": 0, "ok": True, "note": "داده کافی برای چک نبود."}
    import random
    random.seed(1234)
    idxs = random.sample(range(50, n), min(sample_size, n - 50))
    mismatches = []
    for i in idxs:
        first, _log1 = _run_calculate_signals_capture(_build_ohlcv_window(df_full, i, history_bars), symbol, timeframe)
        second, _log2 = _run_calculate_signals_capture(_build_ohlcv_window(df_full, i, history_bars), symbol, timeframe)
        if first[:4] != second[:4]:
            mismatches.append({"bar_index": i, "run1": first[:4], "run2": second[:4]})
    return {
        "checked": len(idxs),
        "mismatches": len(mismatches),
        "ok": len(mismatches) == 0,
        "details": mismatches[:10],
    }


def lookahead_check(df_full: pd.DataFrame, events: list[SignalEvent], symbol: str,
                     timeframe: str, history_bars: int, max_checks: int = 200,
                     apply_signal_filter: bool = True) -> dict:
    ts_to_idx = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_full.index)}
    suspicious = []
    checked = 0
    shorter_hist = max(60, int(history_bars * 0.8))
    for ev in events[:max_checks]:
        i = ts_to_idx.get(ev.signal_bar_ts_ms)
        if i is None:
            continue
        alt_window = _build_ohlcv_window(df_full, i, shorter_hist)
        if len(alt_window) < 50:
            continue
        (sig_alt, entry_alt, stop_alt, target_alt, _, _), _ = \
            _run_calculate_signals_capture(alt_window, symbol, timeframe)
        checked += 1
        direction_flipped = sig_alt != ev.signal
        if direction_flipped:
            suspicious.append({
                "bar_ts_ms": ev.signal_bar_ts_ms,
                "original_signal": ev.signal,
                "signal_with_shorter_history": sig_alt,
                "note": f"جهت سیگنال با تاریخچه {shorter_hist} کندلی به‌جای {history_bars} عوض شد.",
            })
    return {
        "checked": checked, "suspicious": len(suspicious), "details": suspicious[:10],
        "caveat": "این چک فقط تغییر جهت سیگنال را می‌سنجد، نه لوک‌اِهد واقعی را اثبات می‌کند.",
    }


# ============================================================
# 🆕 تخمین زمان اجرا با کالیبراسیون واقعی
# ============================================================
def estimate_total_runtime(symbols: list[str], timeframes: list[str],
                            start_dt: datetime, end_dt: datetime,
                            workers: int, history_bars: int) -> tuple[float, int]:
    total_bars_est = 0
    minutes_span = (end_dt - start_dt).total_seconds() / 60.0
    for tf in timeframes:
        try:
            tf_min = int(tf)
        except Exception:
            tf_min = 1
        total_bars_est += int(minutes_span / max(tf_min, 1)) * len(symbols)

    if not symbols or not timeframes or total_bars_est <= 0:
        return 0.0, 0

    calib_symbol, calib_tf = symbols[0], timeframes[0]
    calib_bars_target = 40
    sec_per_bar_single_core = 0.05

    try:
        calib_tf_min = int(calib_tf)
        calib_fetch_start = start_dt - timedelta(minutes=calib_tf_min * (history_bars + calib_bars_target) * 1.2 + 60)
        calib_fetch_end = start_dt + timedelta(minutes=calib_tf_min * calib_bars_target)
        df_calib = fetch_klines(calib_symbol, calib_tf_min,
                                utc_ms(calib_fetch_start), utc_ms(calib_fetch_end))
        if df_calib.empty or len(df_calib) < 60:
            raise ValueError("داده کالیبراسیون ناکافی بود.")
        n_calib = min(calib_bars_target, len(df_calib) - 50)
        n_calib = max(n_calib, 5)
        t0 = time.time()
        _ = generate_signals_exact(df_calib.iloc[-(n_calib + 50):], calib_symbol, calib_tf,
                                    history_bars, workers=1, keep_log=False)
        elapsed = time.time() - t0
        sec_per_bar_single_core = elapsed / max(n_calib, 1)
    except Exception as e:
        logger.warning(f"کالیبراسیون تخمین زمان شکست خورد ({e})")

    effective_workers = max(1, workers)
    est_seconds = (total_bars_est * sec_per_bar_single_core) / (effective_workers * 0.8)
    est_seconds += len(symbols) * len(timeframes) * 15.0
    return max(0.0, est_seconds), total_bars_est


# ============================================================
# 🆕 ساخت فایل دامپ سیگنال‌ها (CSV)
# ============================================================
def build_signal_dump_file(trades, symbol, timeframe, last_n=5000):
    try:
        if not trades or last_n <= 0:
            return None, 0

        sorted_trades = sorted(trades, key=lambda t: t.get("entry_time_ms", 0))
        subset = sorted_trades[-int(last_n):]

        p = BASE_DIR / f"backtest_signals_{symbol}_{timeframe}m.csv"
        lines = [
            "ENTRY_TIME_UTC,ENTRY_TIME_IRAN,EXIT_TIME_UTC,EXIT_TIME_IRAN,DIRECTION,ENTRY,STOP,TARGET,SIGNAL_TYPE,SCORE,EXIT_REASON,PNL_R,PNL_USD,STATUS,RESOLUTION_METHOD,MAE_PCT,MFE_PCT,BARS_HELD",
        ]

        for t in subset:
            entry_dt = _ms_to_iran(t.get("entry_time_ms"))
            entry_str = entry_dt.strftime("%Y-%m-%d %H:%M") if entry_dt else "?"

            exit_dt = _ms_to_iran(t.get("exit_time_ms"))
            exit_str = exit_dt.strftime("%Y-%m-%d %H:%M") if exit_dt else "?"

            entry_price = t.get('entry', 0)
            stop_price = t.get('stop', 0)
            target_price = t.get('target', 0)

            entry_str_p = f"{entry_price:.8f}" if symbol in ["DOGEUSDT", "TRXUSDT"] else f"{entry_price:.4f}"
            stop_str_p = f"{stop_price:.8f}" if symbol in ["DOGEUSDT", "TRXUSDT"] else f"{stop_price:.4f}"
            target_str_p = f"{target_price:.8f}" if symbol in ["DOGEUSDT", "TRXUSDT"] else f"{target_price:.4f}"

            pnl_r = t.get('pnl_r', 0)
            pnl_usd = t.get('pnl_usd', 0)

            lines.append(
                f"{t.get('entry_time_ms', 0)},{entry_str},"
                f"{t.get('exit_time_ms', 0) or ''},{exit_str},"
                f"{t.get('direction', '')},"
                f"{entry_str_p},{stop_str_p},{target_str_p},"
                f"{t.get('signal_type', '?')},"
                f"{t.get('score', 0)},"
                f"{t.get('exit_reason', '')},"
                f"{pnl_r:.2f},{pnl_usd:.2f},"
                f"{t.get('status', '')},"
                f"{t.get('resolution_method', 'no_ambiguity')},"
                f"{t.get('mae_pct', 0):.1f},{t.get('mfe_pct', 0):.1f},"
                f"{t.get('bars_held', 0)}"
            )

        p.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"[SIGNAL-DUMP] {symbol} {timeframe}m: {len(subset)} سیگنال کامل → {p.name}")
        return str(p), len(subset)
    except Exception as e:
        logger.warning(f"[SIGNAL-DUMP] {symbol} {timeframe}m ناموفق: {e}")
        return None, 0


# ============================================================
# 🆕 ساخت بخش سیگنال‌های اخیر
# ============================================================
def build_recent_signals_section(events: list[SignalEvent], trades: dict[int, TradeResult],
                                  timeframe: str, now_ms: int) -> str:
    days, confirmed = recent_window_days(timeframe)
    cutoff_ms = now_ms - days * 86400 * 1000
    recent = [e for e in events if e.signal_bar_ts_ms >= cutoff_ms]
    recent.sort(key=lambda e: e.signal_bar_ts_ms, reverse=True)

    lines = []
    conf_note = "✅ تاییدشده توسط کاربر" if confirmed else "⚠️ برون‌یابی‌شده — نیازمند تایید نهایی"
    lines.append(f"### سیگنال‌های اخیر — تایم‌فریم {timeframe} دقیقه (بازه {days} روز, {conf_note})")
    lines.append(f"تعداد سیگنال در این بازه: {len(recent)}")
    lines.append("")

    for ev in recent:
        key = ev.signal_bar_ts_ms
        tr = trades.get(key)
        ts_str = ms_to_dt(ev.signal_bar_ts_ms).astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"--- {ev.symbol} | {ev.signal} | {ts_str} (تهران) ---")
        lines.append(f"  ورود={ev.entry} | استاپ={ev.stop} | تارگت={ev.target} | ریسک‌فری%={ev.risk_free_pct}")
        if tr:
            lines.append(
                f"  نتیجه: {tr.status} ({tr.exit_reason}) | خروج={tr.exit_price} | "
                f"PnL=${tr.pnl_usd} ({tr.pnl_r}R) | روش حل ابهام={tr.resolution_method} | "
                f"MAE={tr.mae_pct}% MFE={tr.mfe_pct}%"
            )
        else:
            lines.append("  نتیجه: (هنوز محاسبه نشده)")
        if ev.algo_log:
            lines.append("  لاگ کامل الگوریتمی:")
            for logline in (ev.algo_log or "").splitlines()[:30]:
                lines.append(f"    {logline}")
        lines.append("")
    return "\n".join(lines)


# ============================================================
# گزارش کامل
# ============================================================
def _fmt(x, nd=2, suffix=""):
    if x is None:
        return "N/A"
    if x == float("inf"):
        return "∞"
    try:
        return f"{x:.{nd}f}{suffix}"
    except Exception:
        return str(x)


def build_capabilities_message(args, symbols: list[str], timeframes: list[str]) -> str:
    lines = ["🧩 کارهایی که در این اجرا انجام می‌شود:"]
    lines.append(f"• موتور سیگنال: exact/event-driven (بازسازی دقیق لایو)")
    lines.append(f"• نمادها: {', '.join(symbols)}")
    lines.append(f"• تایم‌فریم‌ها: {', '.join(timeframes)} دقیقه")
    lines.append(f"• بازه زمانی: {args.days} روز")
    lines.append(f"• تعداد پردازه‌های موازی: {args.workers}")
    lines.append("• حل ابهام استاپ/تارگت هم‌کندل با داده ۱ دقیقه‌ای: همیشه فعال")
    lines.append("• شبیه‌سازی ریسک‌فری با فرمول trade_ledger: همیشه فعال")
    lines.append(f"• فیلتر بهینه‌سازی سیگنال: {'فعال (حذف HD+ + ۶ ترکیب زیان‌ده)' if not args.no_signal_filter else 'غیرفعال'}")
    lines.append(f"• چک Determinism: {'فعال' if args.determinism_check else 'غیرفعال'}")
    lines.append(f"• چک خودتشخیصی لوک‌اِهد: {'فعال' if args.lookahead_check else 'غیرفعال'}")
    lines.append(f"• اعتبارسنجی سنگین (--robust): {'فعال' if args.robust else 'غیرفعال'}")
    lines.append("• پس از پایان: آمار کلی سبد + تفکیک نماد/تایم‌فریم + تحلیل سه‌بعدی + اعتبارسنجی نیم‌اول/نیم‌دوم")
    return "\n".join(lines)


def render_report(args, run_meta: dict, per_symbol_tf: dict, portfolio_metrics: dict,
                   breakdown: list[dict], half_split: list[dict],
                   recent_sections: list[str], robust_extra: dict,
                   symbols: list[str], timeframes: list[str]) -> str:
    out = []
    out.append("=" * 78)
    out.append("📊 گزارش کامل بک‌تست استراتژی DTM")
    out.append("=" * 78)
    out.append(f"🗓 بازه: {run_meta['start_date']} تا {run_meta['end_date']} ({args.days} روز — تهران)")
    out.append(f"📡 دیتا: Binance Spot | تایم‌فریم: {', '.join(tf + 'm' for tf in timeframes)}")
    out.append(f"💱 نمادها: {', '.join(symbols)}")
    out.append(f"🕐 تولید گزارش: {run_meta['generated_at']}")
    out.append(f"⚙️ موتور سیگنال: exact/event-driven (بازسازی دقیق لایو)")
    out.append(f"🆕 فیلتر بهینه‌سازی سیگنال: {'فعال ✅' if not args.no_signal_filter else 'غیرفعال ⭕'}")
    label = portfolio_metrics.get("validity_label", "N/A")
    out.append(f"🏷️ برچسب اعتبار کلی: {label}")
    for r in portfolio_metrics.get("validity_reasons", []):
        out.append(f"  - {r}")
    out.append("")

    out.append("── ۱) آمار کلی سبد ─────────────────────────────────────────")
    m = portfolio_metrics
    out.append(f"تعداد کل سیگنال: {m['n_signals_total']}  |  بسته‌شده: {m['n_closed']}  |  هنوز باز: {m['n_open_at_end']}")
    out.append(f"برد: {m['n_wins']} (تارگت={m['n_target_wins']}, ریسک‌فری={m['n_risk_free_wins']})  |  باخت: {m['n_losses']}")
    out.append(f"🏆 نرخ برد: {_fmt(m['win_rate'], 1, '%')}")
    out.append(f"💰 سود/زیان کل: ${_fmt(m['total_pnl_usd'], 4)} (سرمایه پایه ${BASE_CAPITAL:.0f})")
    out.append(f"⚖️ Profit Factor: {_fmt(m['profit_factor'], 3)}")
    out.append(f"📊 Expectancy: ${_fmt(m['expectancy_usd'], 4)}  |  Expectancy (R): {_fmt(m['expectancy_r'], 3)}R")
    out.append(f"📊 میانگین برد: ${_fmt(m['avg_win_usd'], 4)}  |  میانگین باخت: ${_fmt(m['avg_loss_usd'], 4)}")
    out.append(f"📈 Sharpe: {_fmt(m['sharpe'], 3)}  |  Sortino: {_fmt(m['sortino'], 3)}  |  Calmar: {_fmt(m['calmar'], 3)}")
    out.append(f"📈 SQN: {_fmt(m['sqn'], 3)}  |  CAGR: {_fmt(m['cagr_pct'], 2, '%')}")
    out.append(f"📉 Max Drawdown: {_fmt(m['max_dd_pct'], 2, '%')} (${_fmt(m['max_dd_usd'], 4)})")
    out.append(f"  اوج افت: {m['max_dd_peak_time']}  →  کف افت: {m['max_dd_valley_time']}")
    out.append(f"⏱ Exposure Time: {_fmt(m['exposure_pct'], 2, '%')}")
    out.append(f"📊 Benchmark Buy&Hold: {_fmt(m['benchmark_buy_hold_pct'], 2, '%')}")
    out.append(f"⏱ میانگین طول معامله برنده: {_fmt(m['avg_win_duration_bars'], 1)} کندل  |  بازنده: {_fmt(m['avg_loss_duration_bars'], 1)} کندل")
    out.append(f"📊 میانگین MAE: {_fmt(m['avg_mae_pct'], 2, '%')}  |  MFE: {_fmt(m['avg_mfe_pct'], 2, '%')}  |  Edge Ratio: {_fmt(m['edge_ratio'], 3)}")
    out.append(
        f"🔍 حل ابهام استاپ/تارگت: intrabar_verified={m['intrabar_verified_count']} | "
        f"conservative_assumption={m['conservative_assumption_count']} | no_ambiguity={m['no_ambiguity_count']}"
    )
    out.append("")

    out.append("── ۲) تفکیک بر اساس نماد/تایم‌فریم ─────────────────────────")
    for (symbol, tf), sub_m in per_symbol_tf.items():
        out.append(
            f"{symbol} {tf}m: سیگنال={sub_m['n_signals_total']} | بسته={sub_m['n_closed']} | "
            f"WinRate={_fmt(sub_m['win_rate'],1,'%')} | PnL=${_fmt(sub_m['total_pnl_usd'],4)} | "
            f"PF={_fmt(sub_m['profit_factor'],2)} | Exp(R)={_fmt(sub_m['expectancy_r'],3)}"
        )
    out.append("")

    out.append("── ۳) تحلیل سه‌بعدی خودکار (ارز × تایم‌فریم × نوع سیگنال) ──")
    out.append(f"{'symbol':<10}{'tf':<6}{'type':<8}{'n':<6}{'winRate':<10}{'PnL($)':<12}{'Exp(R)':<10}{'PF':<8}{'reliable':<10}{'recommendation'}")
    for row in breakdown:
        out.append(
            f"{row['symbol']:<10}{row['timeframe']:<6}{row['signal_type']:<8}{row['n']:<6}"
            f"{_fmt(row['win_rate'],1):<10}{_fmt(row['total_pnl_usd'],2):<12}"
            f"{_fmt(row['expectancy_r'],3):<10}{_fmt(row['profit_factor'],2):<8}"
            f"{'بله' if row['reliable_sample'] else 'خیر':<10}{row['recommendation']}"
        )
    out.append("")

    out.append("── ۴) اعتبارسنجی نیم‌اول/نیم‌دوم ──────────────────────────")
    for row in half_split:
        cons = "سازگار ✅" if row["consistent"] else ("ناسازگار ⚠️" if row["consistent"] is False else "نمونه کم")
        out.append(
            f"{row['symbol']} {row['timeframe']}m {row['signal_type']}: "
            f"نیمه اول=${_fmt(row['half1_pnl'],2)} | نیمه دوم=${_fmt(row['half2_pnl'],2)} | {cons}"
        )
    out.append("")

    if robust_extra:
        out.append("── ۵) اعتبارسنجی سنگین (--robust) ───────────────────────")
        if "monte_carlo" in robust_extra:
            mc = robust_extra["monte_carlo"]
            out.append(f"Monte Carlo Permutation Test: p-value ≈ {_fmt(mc.get('p_value'), 4)}")
        if "walk_forward" in robust_extra:
            for (symbol, tf), wf in robust_extra["walk_forward"].items():
                out.append(f"Walk-Forward {symbol} {tf}m: {wf['profitable_folds']}/{wf['total_folds']} فولد سودآور")
                for f in wf["folds"]:
                    out.append(f"   فولد {f['fold']}: {f['start']}→{f['end']} | سیگنال={f['n_signals']} | PnL=${_fmt(f['total_pnl_usd'],2)}")
        out.append("")

    if run_meta.get("determinism"):
        out.append("── ۶) چک Determinism ──────────────────────────────────")
        for (symbol, tf), d in run_meta["determinism"].items():
            status = "✅ سازگار" if d["ok"] else f"❌ {d['mismatches']} ناسازگاری یافت شد"
            out.append(f"{symbol} {tf}m: {d['checked']} نمونه بررسی شد — {status}")
        out.append("")

    if run_meta.get("lookahead"):
        out.append("── ۷) چک خودتشخیصی لوک‌اِهد ────────────────────────────")
        for (symbol, tf), la in run_meta["lookahead"].items():
            out.append(f"{symbol} {tf}m: {la['checked']} سیگنال بررسی شد — {la['suspicious']} مورد مشکوک")
        out.append("")

    out.append("── ۸) سیگنال‌های اخیر + لاگ کامل الگوریتمی ───────────────")
    for sec in recent_sections:
        out.append(sec)
        out.append("")

    out.append("── ۹) روش‌شناسی و محدودیت‌ها ─────────────────────────────")
    out.append(
        "- سیگنال، استاپ/تارگت، و PnL مستقیماً از strategy_wrapper.calculate_signals و "
        "trade_ledger._hypothetical_pnl_usd (import شده) محاسبه شده‌اند."
    )
    out.append(
        f"- هر کندل بسته‌شده با یک اجرای تازه ScriptRunner روی آخرین {HISTORY_BARS} کندل پردازش شده"
    )
    out.append(
        "- ابهام استاپ/تارگت هم‌کندل: در صورت وجود داده ۱-دقیقه‌ای حل شده (intrabar_verified)؛ "
        "در غیر این صورت با قاعده محافظه‌کارانه (conservative_assumption)"
    )
    out.append(
        "- ریسک‌فری با منطق trade_ledger.update_open_trades شبیه‌سازی شده"
    )
    out.append(
        f"- اعلان‌های تلگرام به ربات مستقل ارسال می‌شوند (BACKTEST_TELEGRAM_*)"
    )
    out.append(
        f"- قفل تک‌اجرایی ({RUN_LOCK_FILE.name}): فقط یک‌بار در هر استارت فرآیند"
    )
    out.append(
        f"- تنظیمات صریح pivotMode: leftBars/rightBars برای هر تایم‌فریم به‌صورت عددی تعیین شده‌اند"
    )
    if args.robust:
        out.append("- Monte Carlo Permutation Test و Walk-Forward اجرا شدند.")
    if not args.determinism_check:
        out.append("- چک Determinism غیرفعال بود.")
    if args.lookahead_check:
        out.append("- چک خودتشخیصی لوک‌اِهد اجرا شد.")
    out.append("⚠️ نتایج فرضی است (بدون اسلیپیج/کارمزد واقعی) — صرفاً برای ارزیابی استراتژی.")
    out.append("=" * 78)
    return "\n".join(out)


# ============================================================
# بک‌تست یک ترکیب ارز/تایم‌فریم
# ============================================================
def backtest_combo(symbol, timeframe, start_ms, end_ms,
                    history_bars=HISTORY_BARS, workers=1, risk_free_fee_usd=0.0,
                    progress_cb=None, window_clamp=HISTORY_BARS, verify_sample_n=0,
                    signal_dump_n=5000, apply_signal_filter=True,
                    keep_log=True, determinism_check_flag=True,
                    lookahead_check_flag=False, robust_flag=False) -> tuple:
    tf_minutes = int(timeframe)
    warmup_ms = history_bars * tf_minutes * 60_000 + 3 * 86_400_000
    fetch_start = start_ms - warmup_ms
    df = fetch_klines(symbol, tf_minutes, fetch_start, end_ms)
    if df is None or df.empty:
        raise RuntimeError("دیتای خالی از Binance")
    if len(df) < history_bars + 50:
        raise RuntimeError(f"کندل کافی برای پنجره {history_bars}-تایی نیست: {len(df)}")

    df_full = df
    candles = df_to_candles(df)
    n = len(candles)
    timestamps = [int(c.timestamp) for c in candles]
    idx_from = next((k for k, ts in enumerate(timestamps) if ts >= start_ms), n)
    idx_to = n

    events = generate_signals_exact(
        df_full, symbol, timeframe, history_bars,
        workers=workers, keep_log=keep_log,
        apply_signal_filter=apply_signal_filter
    )

    events = [e for e in events if start_ms <= e.signal_bar_ts_ms <= end_ms]

    ts_to_idx = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_full.index)}
    trades = [resolve_trade(ev, df_full, ts_to_idx) for ev in events]

    diag = {
        "total_events": len(events),
        "trades": len(trades),
        "gaps": df.attrs.get("gaps", []),
    }

    if signal_dump_n and signal_dump_n > 0:
        trade_dicts = []
        for tr in trades:
            td = {
                "entry_time_ms": tr.event.signal_bar_ts_ms,
                "exit_time_ms": tr.exit_time_ms,
                "direction": tr.event.signal,
                "entry": tr.event.entry,
                "stop": tr.event.stop,
                "target": tr.event.target,
                "signal_type": _signal_type_from_log(tr.event.algo_log),
                "score": 0,
                "exit_reason": tr.exit_reason,
                "pnl_r": tr.pnl_r,
                "pnl_usd": tr.pnl_usd,
                "status": tr.status,
                "resolution_method": tr.resolution_method,
                "mae_pct": tr.mae_pct,
                "mfe_pct": tr.mfe_pct,
                "bars_held": tr.bars_held,
            }
            trade_dicts.append(td)
        dump_path, dump_count = build_signal_dump_file(trade_dicts, symbol, timeframe, signal_dump_n)
        diag["signal_dump_path"] = dump_path
        diag["signal_dump_count"] = dump_count

    if determinism_check_flag:
        diag["determinism"] = determinism_check(df_full, symbol, timeframe, history_bars, apply_signal_filter=apply_signal_filter)

    if lookahead_check_flag and events:
        diag["lookahead"] = lookahead_check(df_full, events, symbol, timeframe, history_bars, apply_signal_filter=apply_signal_filter)

    if robust_flag and events:
        diag["walk_forward"] = walk_forward_validation(df_full, symbol, timeframe, history_bars, workers, apply_signal_filter=apply_signal_filter)

    return trades, n, events, diag


# ============================================================
# ارسال گزارش به تلگرام
# ============================================================
def send_reports(trades, meta, mode, do_send):
    texts = []
    if mode in ("full", "both"):
        texts.append(("📊 گزارش کامل", meta.get("report_text", "")))
    if mode in ("breakdown", "both"):
        groups = {}
        for t in trades:
            key = (t.event.symbol, t.event.timeframe)
            groups.setdefault(key, []).append(t)
        for (sym, tf), trs in groups.items():
            st = compute_portfolio_metrics(trs, pd.DataFrame(), 0, 0)
            lines = [f"📋 {sym} {tf}m", W]
            lines.append(f"سیگنال: {len(trs)} | بسته: {st['n_closed']} | نرخ برد: {_fmt(st['win_rate'],1,'%')} | PnL: ${_fmt(st['total_pnl_usd'],4)}")
            texts.append((f"📋 {sym} {tf}m", "\n".join(lines)))

    full_text = "\n\n" + ("═" * 40) + "\n\n".join(f"{h}\n{b}" for h, b in texts)

    report_path = BASE_DIR / f"backtest_full_report_{datetime.now(UTC_TZ).strftime('%Y%m%d_%H%M%S')}.txt"
    report_path.write_text(full_text, encoding="utf-8")
    logger.info(f"[REPORT] فایل گزارش کامل در {report_path.name} ذخیره شد")

    _build_recent_1m_report(trades, meta)

    if not do_send:
        print(full_text)
        return True

    try:
        return notify_telegram_document(report_path, caption=f"📊 گزارش کامل بک‌تست ({meta['days']} روز)")
    except Exception as e:
        logger.error(f"[SEND] ارسال فایل گزارش ناموفق: {e}")
        return False


def _build_recent_1m_report(trades, meta):
    try:
        trades_1m = [t for t in trades if t.event.timeframe == "1"]
        if not trades_1m:
            logger.warning("⚠️ برای گزارش ۷روزه تایم‌فریم ۱ دقیقه سیگنالی یافت نشد.")
            return

        days, confirmed = recent_window_days("1")
        cutoff_ms = meta.get("end_ms", int(time.time() * 1000)) - days * 86400 * 1000
        recent = [t for t in trades_1m if t.event.signal_bar_ts_ms >= cutoff_ms]

        if not recent:
            logger.warning(f"⚠️ در {days} روز اخیر تایم‌فریم ۱ دقیقه سیگنالی یافت نشد.")
            return

        lines = [
            f"گزارش سیگنال‌های {days} روز اخیر — تایم‌فریم ۱ دقیقه",
            f"تولیدشده در: {now_iran_str()} (تهران)",
            "=" * 60
        ]
        for tr in sorted(recent, key=lambda t: t.event.signal_bar_ts_ms, reverse=True):
            lines.append(
                f"{ms_to_dt(tr.event.signal_bar_ts_ms).astimezone(IRAN_TZ).strftime('%Y-%m-%d %H:%M')} | "
                f"{tr.event.symbol} | {tr.event.signal} | PnL=${tr.pnl_usd} ({tr.pnl_r}R) | {tr.status}"
            )

        txt_path = BASE_DIR / f"recent_{days}d_1m_report_{datetime.now(UTC_TZ).strftime('%Y%m%d_%H%M%S')}.txt"
        txt_path.write_text("\n".join(lines), encoding="utf-8")
        notify_telegram_document(txt_path, caption=f"📄 گزارش {days} روز اخیر — تایم‌فریم ۱ دقیقه (txt)")

        try:
            rows = []
            for tr in recent:
                rows.append({
                    "symbol": tr.event.symbol,
                    "signal": tr.event.signal,
                    "entry_time": ms_to_dt(tr.event.signal_bar_ts_ms).astimezone(IRAN_TZ),
                    "entry": tr.event.entry,
                    "stop": tr.event.stop,
                    "target": tr.event.target,
                    "status": tr.status,
                    "exit_reason": tr.exit_reason,
                    "exit_price": tr.exit_price,
                    "exit_time": ms_to_dt(tr.exit_time_ms).astimezone(IRAN_TZ) if tr.exit_time_ms else None,
                    "pnl_usd": tr.pnl_usd,
                    "pnl_r": tr.pnl_r,
                    "resolution_method": tr.resolution_method,
                    "mae_pct": tr.mae_pct,
                    "mfe_pct": tr.mfe_pct,
                    "bars_held": tr.bars_held,
                })
            if rows:
                df_recent = pd.DataFrame(rows)
                xlsx_path = BASE_DIR / f"recent_{days}d_1m_report_{datetime.now(UTC_TZ).strftime('%Y%m%d_%H%M%S')}.xlsx"
                df_recent.to_excel(xlsx_path, index=False)
                notify_telegram_document(xlsx_path, caption=f"📊 نسخه اکسل {days} روز اخیر — ۱ دقیقه")
        except Exception as e:
            logger.warning(f"ساخت فایل اکسل گزارش ۷روزه شکست خورد: {e}")
    except Exception as e:
        logger.warning(f"ساخت گزارش ۷روزه شکست خورد: {e}")


# ============================================================
# main
# ============================================================
def parse_args():
    p = argparse.ArgumentParser(description="بک‌تست و گزارش استراتژی DTM — نسخه v8 با قابلیت‌های پیشرفته")
    p.add_argument("--days", type=int, default=DAYS_DEFAULT,
                   help="تعداد روزهای بک‌تست (پیش‌فرض ۳۶۵ = ۱ سال)")
    p.add_argument("--symbols", nargs="*", default=SYMBOLS,
                   help="نمادها — می‌تواند شامل نمادهایی باشد که فعلاً در bot.py لایو نیستند")
    p.add_argument("--tfs", nargs="*", default=TIMEFRAMES,
                   help="تایم‌فریم‌ها به‌دقیقه — هر مقدار پشتیبانی‌شده توسط Binance")
    p.add_argument("--mode", choices=["full", "breakdown", "both"], default="both")
    p.add_argument("--window-clamp", type=int, default=HISTORY_BARS,
                   help="حداکثر عمر مجاز پیوت‌ها به کندل (پیش‌فرض ۵۰۰ مثل پنجره لایو | 0 = خاموش)")
    p.add_argument("--verify-sample", type=int, default=0,
                   help="نمونه‌گیری کنترلی: هر N-مین کندلِ غیرکاندید با پنجره سرد چک می‌شود (0 = خاموش)")
    p.add_argument("--signal-dump", type=int, default=5000,
                   help="آخرین N سیگنالِ هر ترکیب به‌صورت فایل CSV به تلگرام ارسال شود (0 = خاموش)")
    p.add_argument("--history-bars", type=int, default=HISTORY_BARS,
                   help=f"طول پنجره‌ی غلتان (پیش‌فرض = {HISTORY_BARS})")
    p.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2) - 1)),
                   help="تعداد پردازه‌های موازی")
    p.add_argument("--leverage", nargs="*", default=[],
                   help="بازنویسی اهرم برای نماد: SYMBOL=VALUE")
    p.add_argument("--tick", nargs="*", default=[],
                   help="بازنویسی tick size قیمت برای نماد: SYMBOL=VALUE")
    p.add_argument("--risk-free-fee-usd", type=float, default=0.0,
                   help="کارمزد تقریبی (دلار) برای نزدیک‌ترکردن ریسک‌فری به رفتار واقعی صرافی")
    p.add_argument("--account-sim", type=float, default=None,
                   help="اگر ست شود، یک شبیه‌سازی تکمیلی با موجودی شروع داده‌شده اجرا می‌شود")
    p.add_argument("--no-signal-filter", action="store_true",
                   help="خاموش‌کردن فیلتر بهینه‌سازی سیگنال (پیش‌فرض: فیلتر روشن است)")
    p.add_argument("--force", action="store_true", help="نادیده‌گرفتن قفل روزانه")
    p.add_argument("--resend", action="store_true", help="ارسال مجدد از نتایج ذخیره‌شده")
    p.add_argument("--no-send", action="store_true", help="فقط چاپ/ذخیره، بدون تلگرام")
    p.add_argument("--keep-log", action="store_true", default=True,
                   help="ضبط لاگ کامل الگوریتمی هر سیگنال (پیش‌فرض روشن)")
    p.add_argument("--no-keep-log", dest="keep_log", action="store_false")
    p.add_argument("--determinism-check", action="store_true", default=True,
                   help="چک determinism روی نمونه کوچک (پیش‌فرض روشن)")
    p.add_argument("--no-determinism-check", dest="determinism_check", action="store_false")
    p.add_argument("--lookahead-check", action="store_true",
                   help="اجرای ابزار خودتشخیصی لوک‌اِهد (سنگین)")
    p.add_argument("--robust", action="store_true",
                   help="فعال‌سازی Monte Carlo Permutation Test و Walk-Forward (سنگین)")
    p.add_argument("--min-samples", type=int, default=MIN_SAMPLE_SIZE_DEFAULT,
                   help="حداقل نمونه آماری اجباری برای هر سلول فیلترشونده")
    return p.parse_args()


def save_results(trades, meta):
    try:
        trade_dicts = []
        for tr in trades:
            td = {
                "symbol": tr.event.symbol,
                "timeframe": tr.event.timeframe,
                "direction": tr.event.signal,
                "entry": tr.event.entry,
                "stop": tr.event.stop,
                "target": tr.event.target,
                "entry_time_ms": tr.event.signal_bar_ts_ms,
                "risk_free_pct": tr.event.risk_free_pct,
                "signal_type": _signal_type_from_log(tr.event.algo_log),
                "algo_log": tr.event.algo_log,
                "exit_price": tr.exit_price,
                "exit_time_ms": tr.exit_time_ms,
                "status": tr.status,
                "exit_reason": tr.exit_reason,
                "resolution_method": tr.resolution_method,
                "risk_free_armed": tr.risk_free_armed,
                "pnl_usd": tr.pnl_usd,
                "pnl_r": tr.pnl_r,
                "mae_pct": tr.mae_pct,
                "mfe_pct": tr.mfe_pct,
                "bars_held": tr.bars_held,
            }
            trade_dicts.append(td)

        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "trades": trade_dicts}, f, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"[SAVE] {e}")
        return False


def load_results():
    try:
        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("trades", []), data.get("meta", {})
    except Exception as e:
        logger.error(f"[LOAD] {e}")
        return [], {}


def main():
    args = parse_args()

    if not args.force and not args.resend and not check_and_create_lock():
        notify_telegram("⏭️ بک‌تست اجرا نشد: قفل اجرا وجود دارد. برای اجرای مجدد: --force")
        return 0

    symbols = [s.upper() for s in args.symbols]
    tfs = [str(t) for t in args.tfs]
    leverage_overrides = _parse_kv_overrides(args.leverage)
    tick_overrides = _parse_kv_overrides(args.tick)
    history_bars = int(args.history_bars)
    apply_signal_filter = not args.no_signal_filter

    for sym, val in leverage_overrides.items():
        LEVERAGE_MAP[sym] = val
    for sym, val in tick_overrides.items():
        TICK_SIZES[sym] = val
        if sym in _sw.SYMBOL_TICK_INFO:
            _sw.SYMBOL_TICK_INFO[sym]["mintick"] = val

    try:
        if args.resend:
            trades, meta = load_results()
            if not trades:
                logger.error("نتایج ذخیره‌شده‌ای پیدا نشد")
                return 1
            logger.info(f"Resend از فایل ذخیره‌شده ({len(trades)} معامله)...")
            send_reports(trades, meta, args.mode, do_send=not args.no_send)
            return 0

        for tf in tfs:
            try:
                to_binance_interval(tf)
            except Exception as e:
                logger.error(f"تایم‌فریم نامعتبر: {tf}")
                notify_telegram(f"❌ تایم‌فریم نامعتبر: {tf}")
                return 1

        now_ir = datetime.now(UTC_TZ).astimezone(IRAN_TZ)
        today_mid = now_ir.replace(hour=0, minute=0, second=0, microsecond=0)
        start_ir = today_mid - timedelta(days=max(1, args.days) - 1)
        start_ms = int(start_ir.timestamp() * 1000)
        end_ms = int(time.time() * 1000)

        meta = {
            "days": args.days, "symbols": symbols, "tfs": tfs,
            "start_date": start_ir.strftime("%Y-%m-%d"),
            "end_date": now_ir.strftime("%Y-%m-%d"),
            "generated_at": now_iran_str(),
            "window_clamp": args.window_clamp,
            "history_bars": history_bars,
            "signal_filter_enabled": apply_signal_filter,
            "end_ms": end_ms,
            "combos": [], "errors": [],
        }

        est_seconds, est_bars = estimate_total_runtime(
            symbols, tfs, start_ir, now_ir, args.workers, history_bars
        )

        start_msg = (
            f"🚀 شروع بک‌تست استراتژی DTM\n"
            f"🗓 {meta['start_date']} تا {meta['end_date']} ({args.days} روز — تهران)\n"
            f"📡 {len(symbols)} ارز × {len(tfs)} تایم‌فریم\n"
            f"📈 تخمین کندل‌ها: ~{est_bars:,}\n"
            f"⚙️ موتور: exact/event-driven (بازسازی دقیق لایو)"
        )
        logger.info(start_msg.replace("\n", " | "))
        if not args.no_send:
            notify_telegram(start_msg)

        if est_seconds > 0:
            eta_msg = (
                f"⏱️ تخمین زمان پایان: "
                f"{(datetime.now(UTC_TZ) + timedelta(seconds=est_seconds)).astimezone(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')} (تهران)\n"
                f"⚠️ این فقط یک تخمین تقریبی است."
            )
            if not args.no_send:
                notify_telegram(eta_msg)

        caps_msg = build_capabilities_message(args, symbols, tfs)
        if not args.no_send:
            notify_telegram(caps_msg)

        all_trades = []
        all_events = []
        per_symbol_tf = {}
        recent_sections = []
        robust_extra = {}
        run_meta = {"determinism": {}, "lookahead": {}, "gaps": {}}

        total = len(tfs) * len(symbols)
        done = 0

        for tf in tfs:
            for sym in symbols:
                done += 1
                t0 = time.time()
                try:
                    trades, n_bars, events, diag = backtest_combo(
                        sym, tf, start_ms, end_ms,
                        history_bars=history_bars,
                        workers=args.workers,
                        risk_free_fee_usd=args.risk_free_fee_usd,
                        window_clamp=args.window_clamp,
                        verify_sample_n=args.verify_sample,
                        signal_dump_n=args.signal_dump,
                        apply_signal_filter=apply_signal_filter,
                        keep_log=args.keep_log,
                        determinism_check_flag=args.determinism_check,
                        lookahead_check_flag=args.lookahead_check,
                        robust_flag=args.robust,
                    )

                    elapsed = time.time() - t0
                    all_trades.extend(trades)
                    all_events.extend(events)

                    sub_metrics = compute_portfolio_metrics(trades, pd.DataFrame(), start_ms, end_ms)
                    per_symbol_tf[(sym, tf)] = sub_metrics

                    run_meta["determinism"][(sym, tf)] = diag.get("determinism", {})
                    run_meta["lookahead"][(sym, tf)] = diag.get("lookahead", {})
                    run_meta["gaps"][(sym, tf)] = diag.get("gaps", [])
                    if args.robust and "walk_forward" in diag:
                        robust_extra.setdefault("walk_forward", {})[(sym, tf)] = diag["walk_forward"]

                    trades_by_bar = {t.event.signal_bar_ts_ms: t for t in trades}
                    recent_sections.append(
                        build_recent_signals_section(events, trades_by_bar, tf, end_ms)
                    )

                    if args.signal_dump and diag.get("signal_dump_path"):
                        if not args.no_send:
                            notify_telegram_document(
                                diag["signal_dump_path"],
                                caption=f"📊 {sym} {tf}m — {diag.get('signal_dump_count', 0)} سیگنال اخیر (CSV)",
                            )

                    meta["combos"].append({
                        "symbol": sym, "tf": tf, "bars": n_bars,
                        "signals": len(trades),
                        "elapsed_sec": elapsed,
                        "signal_dump_path": diag.get("signal_dump_path"),
                        "signal_dump_count": diag.get("signal_dump_count", 0),
                    })

                    msg = f"✅ [{done}/{total}] {sym} {tf}m ✓ | کندل: {n_bars:,} | سیگنال: {len(events)} | معاملات: {len(trades)} | {elapsed:.0f}s"
                    logger.info(msg)
                    if not args.no_send:
                        notify_telegram(msg)

                except Exception as e:
                    meta["errors"].append(f"{sym} {tf}m: {e}")
                    logger.error(f"[COMBO] {sym} {tf}m failed: {e}\n{traceback.format_exc()}")
                    msg = f"❌ [{done}/{total}] {sym} {tf}m ✗ | {e}"
                    if not args.no_send:
                        notify_telegram(msg)

        portfolio_metrics = compute_portfolio_metrics(all_trades, pd.DataFrame(), start_ms, end_ms)

        breakdown = three_dim_breakdown(all_trades, min_samples=args.min_samples)
        half_split = half_split_validation(all_trades, breakdown)

        if args.robust and len(_closed(all_trades)) >= 10:
            robust_extra["monte_carlo"] = monte_carlo_permutation_test(all_trades)

        meta["report_text"] = render_report(
            args, run_meta, per_symbol_tf, portfolio_metrics,
            breakdown, half_split, recent_sections, robust_extra,
            symbols, tfs
        )

        save_results(all_trades, meta)

        sent_ok = send_reports(all_trades, meta, args.mode, do_send=not args.no_send)

        if sent_ok and not args.no_send:
            final_msg = (
                f"🏁 بک‌تست تمام شد.\n"
                f"کل سیگنال: {portfolio_metrics['n_signals_total']} | "
                f"بسته‌شده: {portfolio_metrics['n_closed']} | "
                f"Win Rate: {_fmt(portfolio_metrics['win_rate'], 1, '%')} | "
                f"PnL کل: ${_fmt(portfolio_metrics['total_pnl_usd'], 2)}\n"
                f"برچسب اعتبار: {portfolio_metrics.get('validity_label', 'N/A')}"
            )
            notify_telegram(final_msg)

        return 0

    except KeyboardInterrupt:
        notify_telegram("⏹ بک‌تست توسط کاربر متوقف شد.")
        return 130
    except Exception as e:
        err = f"❌ خطای کلی بک‌تست: {type(e).__name__}: {e}\n{traceback.format_exc()[:1500]}"
        logger.error(err)
        notify_telegram(err)
        return 1


if __name__ == "__main__":
    try:
        import multiprocessing as mp
        if mp.get_start_method(allow_none=True) is None:
            mp.set_start_method("fork" if sys.platform != "win32" else "spawn")
    except Exception:
        pass
    sys.exit(main())
