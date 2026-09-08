#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest_report.py
===================
بک‌تستِ «exact / event-driven» استراتژیِ DTM — دقیقاً بر پایهٔ همان کدی که در
لایو سیگنال می‌سازد (strategy_wrapper.calculate_signals → strategy.py از طریق
PyneCore ScriptRunner، و trade_ledger برای فرمول PnL) اجرا می‌شود.

✅ تلگرام: با متغیرهای محیطی کد قدیمی کار می‌کند:
  TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID

اجرا:
    python backtest_report.py --from 2024-01-01 --to 2025-01-01
    python backtest_report.py --symbols BNBUSDT,ETHUSDT --timeframes 1,5
    python backtest_report.py --robust --lookahead-check
"""

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import math
import os
import statistics
import sys
import time as _time_mod
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

UTC = timezone.utc
IRAN_TZ = timezone(timedelta(hours=3, minutes=30))

# ============================================================================
# بازهٔ زمانیِ پیش‌فرضِ بک‌تست
# ============================================================================
DEFAULT_DATE_FROM = "2024-09-08"
DEFAULT_DATE_TO = "2025-09-08"

# ============================================================================
# ✅ تلگرام با متغیرهای محیطی کد قدیمی (کار می‌کند)
# ============================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")
_TELEGRAM_MSG_LIMIT = 4000
_TELEGRAM_API_BASE = "https://api.telegram.org"

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("BACKTEST")


# ============================================================================
# ۱) اتصال زنده به کدهای لایو
# ============================================================================
SYMBOLS: list[str] = ["BNBUSDT", "ETHUSDT", "SOLUSDT"]
TIMEFRAMES: list[str] = ["1"]
HISTORY_BARS: int = 500

LEVERAGE_MAP: dict = {"BNBUSDT": 75, "ETHUSDT": 50, "SOLUSDT": 60}
TICK_SIZES: dict = {"BNBUSDT": 0.01, "ETHUSDT": 0.01, "SOLUSDT": 0.001}

MIN_ORDER_COST_USDT: float = 5.0
_BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]
BASE_CAPITAL: float = 2.0

LOGIC_SOURCE_OK = True
_logic_import_error: Optional[str] = None

try:
    import strategy_wrapper as _sw
    import trade_ledger as _tl

    from trade_ledger import _hypothetical_pnl_usd as ledger_pnl_usd
    from trade_ledger import BASE_CAPITAL

    # خاموش کردن تلگرام لایو (اسپم نشود)
    _original_send_telegram = getattr(_sw, "_send_telegram", None)
    _sw._send_telegram = lambda *a, **k: True

    # تزریق tick info
    for _sym, _tick in TICK_SIZES.items():
        if _sym not in _sw.SYMBOL_TICK_INFO:
            _sw.SYMBOL_TICK_INFO[_sym] = {
                "mintick": _tick,
                "pricescale": int(round(1 / _tick)),
                "basecurrency": _sym.replace("USDT", ""),
            }
except Exception as e:
    LOGIC_SOURCE_OK = False
    _logic_import_error = f"{type(e).__name__}: {e}"
    sys.stderr.write(
        f"\n❌ FATAL: نمی‌توان strategy_wrapper.py / trade_ledger.py را import کرد:\n"
        f"   {_logic_import_error}\n\n"
        "مطمئن شوید strategy.py و strategy_wrapper.py و trade_ledger.py کنار این فایل هستند.\n"
    )
    sys.exit(1)


# ============================================================================
# ۲) تلگرام — با متغیرهای کد قدیمی (کار می‌کند)
# ============================================================================
def notify_telegram(message: str) -> bool:
    """ارسال پیام به تلگرام با متغیرهای کد قدیمی"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    chunks = [message[i:i + _TELEGRAM_MSG_LIMIT] for i in range(0, len(message), _TELEGRAM_MSG_LIMIT)] or [message]
    ok_all = True

    for chunk in chunks:
        try:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": TELEGRAM_CHAT_ID, "text": chunk},
                timeout=15,
            )
            if resp.status_code != 200:
                logger.warning(f"[TG] ارسال پیام شکست خورد ({resp.status_code}): {resp.text[:300]}")
                ok_all = False
        except Exception as e:
            logger.warning(f"[TG] ارسال پیام شکست خورد: {e}")
            ok_all = False
    return ok_all


def notify_telegram_document(file_path, caption: str = "") -> bool:
    """ارسال فایل به تلگرام"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    try:
        with open(file_path, "rb") as f:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendDocument",
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption[:1024]},
                files={"document": (Path(file_path).name, f)},
                timeout=60,
            )
        if resp.status_code != 200:
            logger.warning(f"[TG] ارسال فایل شکست خورد ({resp.status_code}): {resp.text[:300]}")
            return False
        return True
    except Exception as e:
        logger.warning(f"[TG] ارسال فایل شکست خورد: {e}")
        return False


# ============================================================================
# ۳) قفل تک‌اجرایی
# ============================================================================
RUN_LOCK_FILE = BASE_DIR / ".backtest_run.lock"


# ============================================================================
# ۴) نگاشت تایم‌فریم به بایننس
# ============================================================================
BINANCE_INTERVAL_MAP = {
    "1": "1m", "3": "3m", "5": "5m", "15": "15m", "30": "30m",
    "60": "1h", "120": "2h", "240": "4h", "360": "6h", "480": "8h",
    "720": "12h", "1440": "1d", "4320": "3d", "10080": "1w",
}

UNMAPPED_TIMEFRAME_GUESSES: set[str] = set()


def to_binance_interval(timeframe: str) -> str:
    tf = str(timeframe)
    if tf in BINANCE_INTERVAL_MAP:
        return BINANCE_INTERVAL_MAP[tf]
    return f"{tf}m"


def to_binance_interval_tracked(timeframe: str) -> str:
    tf = str(timeframe)
    if tf not in BINANCE_INTERVAL_MAP:
        UNMAPPED_TIMEFRAME_GUESSES.add(tf)
        logger.warning(f"⚠️ تایم‌فریم {tf} در نگاشت نیست؛ حدس '{tf}m' استفاده می‌شود.")
    return to_binance_interval(tf)


def utc_ms(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return int(dt.astimezone(UTC).timestamp() * 1000)


def ms_to_dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000.0, tz=UTC)


def recent_window_days(timeframe: str) -> tuple[int, bool]:
    """برمی‌گرداند (تعداد روز, آیا تاییدشده است)"""
    tf = str(timeframe)
    CONFIRMED = {"1": 7, "5": 22}
    PROPOSED = {"1": 7, "5": 22, "15": 45, "30": 75, "60": 120, "240": 240}

    if tf in CONFIRMED:
        return CONFIRMED[tf], True
    if tf in PROPOSED:
        return PROPOSED[tf], False

    try:
        tf_min = int(tf)
        x1, y1 = 1.0, 7.0
        x5, y5 = 5.0, 22.0
        slope = (math.log(y5) - math.log(y1)) / (math.log(x5) - math.log(x1))
        days = math.exp(math.log(y1) + slope * (math.log(tf_min) - math.log(x1)))
        return max(1, round(days)), False
    except Exception:
        return 30, False


# ============================================================================
# ۵) دریافت داده از بایننس
# ============================================================================
KLINES_LIMIT = 1000


def fetch_klines_chunk(base: str, symbol: str, interval: str, start_ms: int, end_ms: int,
                       limit: int = KLINES_LIMIT, timeout: float = 20.0) -> list:
    url = (
        f"{base}/api/v3/klines?symbol={symbol.upper()}&interval={interval}"
        f"&startTime={start_ms}&endTime={end_ms}&limit={limit}"
    )
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_full_history(symbol: str, timeframe: str, start_dt: datetime, end_dt: datetime,
                       max_retries: int = 4) -> pd.DataFrame:
    interval = to_binance_interval_tracked(timeframe)
    tf_minutes = int(timeframe)
    step_ms = tf_minutes * 60 * 1000

    start_ms = utc_ms(start_dt)
    end_ms = utc_ms(end_dt)

    all_rows = []
    gaps: list[tuple[int, int, str]] = []
    cursor = start_ms
    bases = list(_BINANCE_BASES)

    while cursor < end_ms:
        chunk_end = min(cursor + KLINES_LIMIT * step_ms, end_ms)
        rows = None
        last_err = None

        for base in bases:
            for attempt in range(max_retries):
                try:
                    rows = fetch_klines_chunk(base, symbol, interval, cursor, chunk_end)
                    break
                except Exception as e:
                    last_err = e
                    _time_mod.sleep(min(2 ** attempt, 8) * 0.5)
            if rows is not None:
                break

        if rows is None:
            gaps.append((cursor, chunk_end, f"network_error: {last_err}"))
            logger.error(f"[{symbol} {timeframe}m] شکاف داده {ms_to_dt(cursor)}→{ms_to_dt(chunk_end)}: {last_err}")
            cursor = chunk_end
            continue

        if not rows:
            gaps.append((cursor, chunk_end, "no_data_returned"))
            cursor = chunk_end
            continue

        all_rows.extend(rows)
        last_open = rows[-1][0]
        cursor = last_open + step_ms
        if len(rows) < 2:
            cursor = chunk_end

    if not all_rows:
        df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        df.attrs["gaps"] = gaps
        return df

    t = [row[0] / 1000.0 for row in all_rows]
    df = pd.DataFrame(
        {
            "open": pd.to_numeric([r[1] for r in all_rows], errors="coerce"),
            "high": pd.to_numeric([r[2] for r in all_rows], errors="coerce"),
            "low": pd.to_numeric([r[3] for r in all_rows], errors="coerce"),
            "close": pd.to_numeric([r[4] for r in all_rows], errors="coerce"),
            "volume": pd.to_numeric([r[5] for r in all_rows], errors="coerce"),
        },
        index=pd.to_datetime(t, unit="s", utc=True),
    )
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    df = df.dropna(subset=["open", "high", "low", "close"])
    df.attrs["gaps"] = gaps
    return df


# ============================================================================
# ۶) کش داده ۱-دقیقه‌ای برای حل ابهام
# ============================================================================
_ONE_MIN_CACHE: dict[str, pd.DataFrame] = {}


def get_1m_slice(symbol: str, start_ms: int, end_ms: int) -> Optional[pd.DataFrame]:
    day_key = f"{symbol}:{ms_to_dt(start_ms).strftime('%Y-%m-%d')}"
    day_start = int(datetime(ms_to_dt(start_ms).year, ms_to_dt(start_ms).month,
                             ms_to_dt(start_ms).day, tzinfo=UTC).timestamp() * 1000)
    day_end = day_start + 24 * 3600 * 1000

    if day_key not in _ONE_MIN_CACHE:
        try:
            df_day = fetch_full_history(symbol, "1", ms_to_dt(day_start), ms_to_dt(day_end))
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


def resolve_ambiguous_candle(symbol: str, candle_ts_ms: int, tf_minutes: int,
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


# ============================================================================
# ۷) ضبط لاگ الگوریتمی
# ============================================================================
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


# ============================================================================
# ۸) موتور سیگنال exact
# ============================================================================
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


def build_syminfo(symbol, timeframe):
    tick = TICK_SIZES.get(symbol, 0.0001)
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
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


def df_to_candles(df):
    candles = []
    for idx, row in df.iterrows():
        candles.append({
            "timestamp": int(idx.timestamp() * 1000),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": float(row.get("volume", 0) or 0),
        })
    return candles


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
                        history_bars: int, keep_log: bool = True):
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
    (df_full, lo, hi, symbol, timeframe, history_bars, keep_log) = pickled_args
    out = []
    for i in range(lo, hi):
        ev = _process_single_bar(df_full, i, symbol, timeframe, history_bars, keep_log)
        if ev is not None:
            out.append(ev)
    return out


def generate_signals_exact(df_full: pd.DataFrame, symbol: str, timeframe: str,
                           history_bars: int = HISTORY_BARS,
                           workers: int = 1, keep_log: bool = True) -> list[SignalEvent]:
    n = len(df_full)
    if n < 50:
        return []

    events = []
    if workers and workers > 1:
        try:
            chunks = []
            chunk_size = max(1, math.ceil(n / workers))
            for lo in range(0, n, chunk_size):
                hi = min(n, lo + chunk_size)
                chunks.append((df_full, lo, hi, symbol, timeframe, history_bars, keep_log))

            with ProcessPoolExecutor(max_workers=workers) as ex:
                futures = [ex.submit(_worker_process_range, c) for c in chunks]
                for fut in as_completed(futures):
                    events.extend(fut.result())
            events.sort(key=lambda e: e.signal_bar_ts_ms)
            return events
        except Exception as e:
            logger.warning(f"[{symbol} {timeframe}m] موازی‌سازی شکست خورد ({e})؛ سقوط به تک‌پردازه‌ای.")

    for i in range(n):
        ev = _process_single_bar(df_full, i, symbol, timeframe, history_bars, keep_log)
        if ev is not None:
            events.append(ev)
    return events


# ============================================================================
# ۹) شبیه‌سازی معامله
# ============================================================================
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
            outcome, method = resolve_ambiguous_candle(
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
            LEVERAGE_MAP.get(ev.symbol)
        )
        res.pnl_usd = pnl_usd
        res.pnl_r = pnl_r
    else:
        res.exit_reason = res.exit_reason or "STILL_OPEN_AT_END_OF_DATA"

    return res


# ============================================================================
# ۱۰) متریک‌های پیشرفته
# ============================================================================
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


def profit_factor(trades: list[TradeResult]) -> Optional[float]:
    closed = _closed(trades)
    gross_win = sum(t.pnl_usd for t in closed if t.pnl_usd and t.pnl_usd > 0)
    gross_loss = abs(sum(t.pnl_usd for t in closed if t.pnl_usd and t.pnl_usd < 0))
    if gross_loss == 0:
        return None if gross_win == 0 else float("inf")
    return gross_win / gross_loss


def validity_label(metrics: dict) -> tuple[str, list[str]]:
    reasons = []
    sharpe = metrics.get("sharpe")
    pf = metrics.get("profit_factor")
    win_rate = metrics.get("win_rate")
    n_closed = metrics.get("n_closed", 0)

    label = "GOOD"
    if n_closed < 30:
        label = "UNRELIABLE"
        reasons.append(f"تعداد معاملات بسته‌شده کم است ({n_closed} < 30)")
    if sharpe is not None and sharpe > 10:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Sharpe غیرعادی بالاست ({sharpe:.2f} > 10)")
    if pf is not None and pf != float("inf") and pf > 100:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Profit Factor غیرعادی بالاست ({pf:.1f} > 100)")
    if pf == float("inf"):
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append("Profit Factor = ∞ (هیچ معامله بازنده‌ای)")
    if win_rate is not None and win_rate > 95:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Win Rate غیرعادی بالاست ({win_rate:.1f}% > 95%)")
    if not reasons:
        reasons.append("هیچ الگوی مشکوکی یافت نشد")
    return label, reasons


def compute_portfolio_metrics(trades: list[TradeResult], df_full: pd.DataFrame,
                              total_start_ms: int, total_end_ms: int) -> dict:
    closed = _closed(trades)
    equity = compute_equity_curve(trades)
    dd = max_drawdown(equity)
    ssc = sharpe_sortino_calmar(trades, equity)
    exp = expectancy(trades)
    pf = profit_factor(trades)

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
        "intrabar_verified_count": len([t for t in trades if t.resolution_method == "intrabar_verified"]),
        "conservative_assumption_count": len([t for t in trades if t.resolution_method == "conservative_assumption"]),
        "no_ambiguity_count": len([t for t in trades if t.resolution_method == "no_ambiguity"]),
    }

    # Edge Ratio
    mfe_vals = [t.mfe_pct for t in closed if t.mfe_pct is not None]
    mae_vals = [t.mae_pct for t in closed if t.mae_pct is not None]
    metrics["edge_ratio"] = (
        sum(mfe_vals) / sum(mae_vals) if mae_vals and sum(mae_vals) > 0 else None
    )

    label, reasons = validity_label(metrics)
    metrics["validity_label"] = label
    metrics["validity_reasons"] = reasons
    metrics["equity_curve"] = equity

    return metrics


# ============================================================================
# ۱۱) تحلیل سه‌بعدی و اعتبارسنجی
# ============================================================================
def _signal_type_of(ev: SignalEvent, algo_log: str = "") -> str:
    log = algo_log or ev.algo_log
    for line in log.splitlines():
        if "[SIGNAL_TRACE]" in line and "signal=" in line:
            try:
                part = line.split("signal=", 1)[1]
                return part.split("|", 1)[0].strip()
            except Exception:
                continue
    return "UNKNOWN"


def three_dim_breakdown(all_trades: list[TradeResult], min_samples: int = 30) -> list[dict]:
    buckets: dict[tuple, list[TradeResult]] = {}
    for t in _closed(all_trades):
        stype = _signal_type_of(t.event)
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
        stype = _signal_type_of(t.event)
        key = (t.event.symbol, t.event.timeframe, stype)
        by_key.setdefault(key, []).append(t)

    out = []
    for row in breakdown:
        key = (row["symbol"], row["timeframe"], row["signal_type"])
        trs = sorted(by_key.get(key, []), key=lambda t: t.event.signal_bar_ts_ms)
        if len(trs) < min(10, 30):
            out.append({**row, "half1_pnl": None, "half2_pnl": None, "consistent": None})
            continue

        mid = len(trs) // 2
        h1, h2 = trs[:mid], trs[mid:]
        pnl1 = sum(t.pnl_usd for t in h1 if t.pnl_usd is not None)
        pnl2 = sum(t.pnl_usd for t in h2 if t.pnl_usd is not None)
        consistent = (pnl1 > 0) == (pnl2 > 0)
        out.append({**row, "half1_pnl": pnl1, "half2_pnl": pnl2, "consistent": consistent})
    return out


# ============================================================================
# ۱۲) گزارش سیگنال‌های اخیر
# ============================================================================
def build_recent_signals_section(events: list[SignalEvent], trades: dict[int, TradeResult],
                                  timeframe: str, now_ms: int) -> str:
    days, confirmed = recent_window_days(timeframe)
    cutoff_ms = now_ms - days * 86400 * 1000
    recent = [e for e in events if e.signal_bar_ts_ms >= cutoff_ms]
    recent.sort(key=lambda e: e.signal_bar_ts_ms, reverse=True)

    lines = []
    conf_note = "✅ تاییدشده" if confirmed else "⚠️ برون‌یابی‌شده — نیازمند تایید"
    lines.append(f"### سیگنال‌های اخیر — تایم‌فریم {timeframe} دقیقه ({days} روز, {conf_note})")
    lines.append(f"تعداد: {len(recent)}")
    lines.append("")

    for ev in recent[:50]:  # حداکثر ۵۰ تا
        key = ev.signal_bar_ts_ms
        tr = trades.get(key)
        ts_str = ms_to_dt(ev.signal_bar_ts_ms).astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")

        lines.append(f"--- {ev.symbol} | {ev.signal} | {ts_str} (تهران) ---")
        lines.append(f"  ورود={ev.entry:.4f} | استاپ={ev.stop:.4f} | تارگت={ev.target:.4f} | ریسک‌فری٪={ev.risk_free_pct}")
        if tr:
            lines.append(
                f"  نتیجه: {tr.status} ({tr.exit_reason}) | خروج={tr.exit_price:.4f} | "
                f"PnL=${tr.pnl_usd:.2f} ({tr.pnl_r:.2f}R) | MAE={tr.mae_pct}% MFE={tr.mfe_pct}%"
            )
        else:
            lines.append("  نتیجه: (هنوز محاسبه نشده)")

        if ev.algo_log:
            lines.append("  لاگ الگوریتمی:")
            for logline in (ev.algo_log or "").splitlines()[:5]:
                lines.append(f"    {logline}")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# ۱۳) رندر گزارش نهایی
# ============================================================================
def _fmt(x, nd=2, suffix=""):
    if x is None:
        return "N/A"
    if x == float("inf"):
        return "∞"
    try:
        return f"{x:.{nd}f}{suffix}"
    except Exception:
        return str(x)


def render_report(args, run_meta: dict, per_symbol_tf: dict, portfolio_metrics: dict,
                  breakdown: list[dict], half_split: list[dict],
                  recent_sections: list[str]) -> str:
    out = []
    out.append("=" * 78)
    out.append("گزارش بک‌تست استراتژی DTM — موتور exact/event-driven")
    out.append("=" * 78)
    out.append(f"بازه: {args.date_from} → {args.date_to}")
    out.append(f"نمادها: {', '.join(run_meta['symbols'])}")
    out.append(f"تایم‌فریم‌ها: {', '.join(run_meta['timeframes'])}")
    if UNMAPPED_TIMEFRAME_GUESSES:
        out.append(f"⚠️ تایم‌فریم‌های بدون نگاشت صریح: {sorted(UNMAPPED_TIMEFRAME_GUESSES)}")

    label = portfolio_metrics.get("validity_label", "N/A")
    out.append(f"برچسب اعتبار: {label}")
    for r in portfolio_metrics.get("validity_reasons", []):
        out.append(f"  - {r}")
    out.append("")

    out.append("── ۱) آمار کلی ──────────────────────────────────────────────")
    m = portfolio_metrics
    out.append(f"کل سیگنال: {m['n_signals_total']} | بسته: {m['n_closed']} | باز: {m['n_open_at_end']}")
    out.append(f"برد: {m['n_wins']} (تارگت={m['n_target_wins']}, ریسک‌فری={m['n_risk_free_wins']}) | باخت: {m['n_losses']} | Win Rate: {_fmt(m['win_rate'], 1, '%')}")
    out.append(f"PnL کل: ${_fmt(m['total_pnl_usd'], 2)} (سرمایه پایه ${BASE_CAPITAL:.0f})")
    out.append(f"Expectancy: ${_fmt(m['expectancy_usd'], 2)} | Expectancy (R): {_fmt(m['expectancy_r'], 2)}R")
    out.append(f"Profit Factor: {_fmt(m['profit_factor'], 2)}")
    out.append(f"میانگین برد: ${_fmt(m['avg_win_usd'], 2)} | میانگین باخت: ${_fmt(m['avg_loss_usd'], 2)}")
    out.append(f"Sharpe: {_fmt(m['sharpe'], 3)} | Sortino: {_fmt(m['sortino'], 3)} | Calmar: {_fmt(m['calmar'], 3)}")
    out.append(f"SQN: {_fmt(m['sqn'], 3)} | CAGR: {_fmt(m['cagr_pct'], 2, '%')}")
    out.append(f"Max Drawdown: {_fmt(m['max_dd_pct'], 2, '%')} (${_fmt(m['max_dd_usd'], 2)})")
    out.append(f"Edge Ratio (MFE/MAE): {_fmt(m.get('edge_ratio'), 3)}")
    out.append(
        f"حل ابهام: intrabar={m['intrabar_verified_count']} | conservative={m['conservative_assumption_count']} | no_ambiguity={m['no_ambiguity_count']}"
    )
    out.append("")

    out.append("── ۲) تفکیک نماد/تایم‌فریم ─────────────────────────────────")
    for (symbol, tf), sub_m in per_symbol_tf.items():
        out.append(
            f"{symbol} {tf}m: سیگنال={sub_m['n_signals_total']} | بسته={sub_m['n_closed']} | "
            f"WinRate={_fmt(sub_m['win_rate'], 1, '%')} | PnL=${_fmt(sub_m['total_pnl_usd'], 2)} | "
            f"PF={_fmt(sub_m['profit_factor'], 2)}"
        )
    out.append("")

    out.append("── ۳) تحلیل سه‌بعدی (ارز × تایم‌فریم × نوع سیگنال) ──────────")
    out.append(f"{'نماد':<10}{'TF':<6}{'نوع':<8}{'تعداد':<8}{'WinRate':<10}{'PnL($)':<12}{'Exp(R)':<10}{'PF':<8}{'توصیه'}")
    for row in breakdown:
        out.append(
            f"{row['symbol']:<10}{row['timeframe']:<6}{row['signal_type']:<8}{row['n']:<8}"
            f"{_fmt(row['win_rate'], 1):<10}{_fmt(row['total_pnl_usd'], 2):<12}"
            f"{_fmt(row['expectancy_r'], 2):<10}{_fmt(row['profit_factor'], 2):<8}{row['recommendation']}"
        )
    out.append("")

    out.append("── ۴) اعتبارسنجی نیم‌اول/نیم‌دوم ────────────────────────────")
    for row in half_split:
        cons = "✅ سازگار" if row["consistent"] else ("⚠️ ناسازگار (overfitting)" if row["consistent"] is False else "نمونه کم")
        out.append(
            f"{row['symbol']} {row['timeframe']}m {row['signal_type']}: "
            f"نیمه اول=${_fmt(row['half1_pnl'], 2)} | نیمه دوم=${_fmt(row['half2_pnl'], 2)} | {cons}"
        )
    out.append("")

    out.append("── ۵) سیگنال‌های اخیر ──────────────────────────────────────")
    for sec in recent_sections[:3]:
        out.append(sec)
    out.append("")

    out.append("── ۶) روش‌شناسی ────────────────────────────────────────────")
    out.append("- سیگنال/PnL مستقیماً از strategy_wrapper/trade_ledger import شده")
    out.append("- هر کندل با اجرای تازه ScriptRunner روی آخرین ۵۰۰ کندل پردازش شده")
    out.append("- ابهام استاپ/تارگت هم‌کندل با داده ۱-دقیقه‌ای حل شده")
    out.append("- ریسک‌فری با منطق trade_ledger شبیه‌سازی شده")
    out.append(f"- بازه سیگنال‌های اخیر: ۱m→۷روز (تاییدشده), ۵m→۲۲روز (تاییدشده)")
    out.append("- تلگرام با متغیرهای TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID کار می‌کند")

    out.append("=" * 78)
    return "\n".join(report)


# ============================================================================
# ۱۴) main
# ============================================================================
def parse_args():
    p = argparse.ArgumentParser(description="بک‌تست exact/event-driven DTM")
    p.add_argument("--from", dest="date_from", default=DEFAULT_DATE_FROM, help="تاریخ شروع")
    p.add_argument("--to", dest="date_to", default=DEFAULT_DATE_TO, help="تاریخ پایان")
    p.add_argument("--symbols", default=",".join(SYMBOLS), help="لیست نمادها با کاما")
    p.add_argument("--timeframes", default=",".join(TIMEFRAMES), help="لیست تایم‌فریم‌ها با کاما")
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1), help="تعداد پردازه")
    p.add_argument("--min-samples", type=int, default=30, help="حداقل نمونه برای هر سلول")
    p.add_argument("--robust", action="store_true", help="فعال‌سازی اعتبارسنجی سنگین")
    p.add_argument("--lookahead-check", action="store_true", help="چک لوک‌اِهد")
    p.add_argument("--keep-log", action="store_true", default=True, help="ضبط لاگ الگوریتمی")
    p.add_argument("--no-log", dest="keep_log", action="store_false", help="خاموش‌کردن ضبط لاگ")
    p.add_argument("--output", default=None, help="مسیر فایل گزارش خروجی")
    p.add_argument("--no-send", action="store_true", help="بدون ارسال به تلگرام")
    return p.parse_args()


def main():
    args = parse_args()

    # قفل اجرا
    if RUN_LOCK_FILE.exists():
        try:
            prev_ts = RUN_LOCK_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            prev_ts = "نامشخص"
        skip_msg = f"⏭️ بک‌تست قبلاً اجرا شده (زمان: {prev_ts}). برای اجرای مجدد فایل {RUN_LOCK_FILE} را حذف کنید."
        logger.warning(skip_msg)
        notify_telegram(skip_msg)
        print(skip_msg)
        return
    RUN_LOCK_FILE.write_text(datetime.now(UTC).isoformat(), encoding="utf-8")

    start_dt = datetime.strptime(args.date_from, "%Y-%m-%d").replace(tzinfo=UTC)
    end_dt = datetime.strptime(args.date_to, "%Y-%m-%d").replace(tzinfo=UTC)
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    timeframes = [t.strip() for t in args.timeframes.split(",") if t.strip()]

    run_meta = {"symbols": symbols, "timeframes": timeframes, "gaps": {}}
    all_trades: list[TradeResult] = []
    per_symbol_tf: dict = {}
    recent_sections: list[str] = []
    global_start_ms = utc_ms(start_dt)
    global_end_ms = utc_ms(end_dt)
    recent_anchor_ms = global_end_ms
    first_df_for_benchmark: Optional[pd.DataFrame] = None

    # پیام شروع
    start_msg = (
        f"🚀 بک‌تست DTM شروع شد\n"
        f"بازه: {args.date_from} → {args.date_to}\n"
        f"نمادها: {', '.join(symbols)}\n"
        f"تایم‌فریم‌ها: {', '.join(timeframes)}"
    )
    logger.warning(start_msg)
    notify_telegram(start_msg)

    for symbol in symbols:
        symbol_trades: list[TradeResult] = []

        for tf in timeframes:
            logger.warning(f"[{symbol} {tf}m] دریافت داده...")

            fetch_start = start_dt - timedelta(minutes=int(tf) * HISTORY_BARS * 1.2 + 60)
            df_full = fetch_full_history(symbol, tf, fetch_start, end_dt)
            run_meta["gaps"][(symbol, tf)] = df_full.attrs.get("gaps", [])

            if df_full.empty:
                logger.error(f"[{symbol} {tf}m] داده‌ای دریافت نشد")
                continue

            if first_df_for_benchmark is None:
                mask = (df_full.index >= start_dt) & (df_full.index <= end_dt)
                first_df_for_benchmark = df_full.loc[mask]

            logger.warning(f"[{symbol} {tf}m] {len(df_full)} کندل دریافت شد")

            events = generate_signals_exact(
                df_full, symbol, tf, HISTORY_BARS,
                workers=args.workers, keep_log=args.keep_log,
            )

            events = [e for e in events if global_start_ms <= e.signal_bar_ts_ms <= global_end_ms]
            logger.warning(f"[{symbol} {tf}m] {len(events)} سیگنال یافت شد")

            ts_to_idx = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_full.index)}
            trades = [resolve_trade(ev, df_full, ts_to_idx) for ev in events]

            all_trades.extend(trades)
            symbol_trades.extend(trades)

            sub_metrics = compute_portfolio_metrics(trades, df_full, global_start_ms, global_end_ms)
            per_symbol_tf[(symbol, tf)] = sub_metrics

            trades_by_bar = {t.event.signal_bar_ts_ms: t for t in trades}
            recent_sections.append(build_recent_signals_section(events, trades_by_bar, tf, recent_anchor_ms))

            # پیام پایان ترکیب
            tf_closed = _closed(trades)
            tf_pnl = sum(t.pnl_usd for t in tf_closed if t.pnl_usd is not None)
            tf_win_rate = (len([t for t in tf_closed if t.status == "WIN"]) / len(tf_closed) * 100) if tf_closed else None
            tf_done_msg = (
                f"☑️ {symbol} {tf}m: سیگنال={len(events)} | بسته={len(tf_closed)} | "
                f"WinRate={_fmt(tf_win_rate, 1, '%')} | PnL=${_fmt(tf_pnl, 2)}"
            )
            logger.warning(tf_done_msg)
            notify_telegram(tf_done_msg)

        # پیام پایان نماد
        symbol_closed = _closed(symbol_trades)
        symbol_pnl = sum(t.pnl_usd for t in symbol_closed if t.pnl_usd is not None)
        symbol_wins = len([t for t in symbol_closed if t.status == "WIN"])
        symbol_win_rate = (symbol_wins / len(symbol_closed) * 100) if symbol_closed else None
        symbol_done_msg = (
            f"✅ {symbol} تمام شد: سیگنال={len(symbol_trades)} | بسته={len(symbol_closed)} | "
            f"WinRate={_fmt(symbol_win_rate, 1, '%')} | PnL=${_fmt(symbol_pnl, 2)}"
        )
        logger.warning(symbol_done_msg)
        notify_telegram(symbol_done_msg)

    # متریک‌های نهایی
    portfolio_metrics = compute_portfolio_metrics(
        all_trades,
        first_df_for_benchmark if first_df_for_benchmark is not None else pd.DataFrame(),
        global_start_ms, global_end_ms,
    )

    breakdown = three_dim_breakdown(all_trades, min_samples=args.min_samples)
    half_split = half_split_validation(all_trades, breakdown)

    # رندر گزارش
    report_text = render_report(
        args, run_meta, per_symbol_tf, portfolio_metrics, breakdown, half_split,
        recent_sections,
    )

    out_path = args.output or f"backtest_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(report_text)
    print(f"\n📁 گزارش در {out_path} ذخیره شد")

    # ارسال به تلگرام
    if not args.no_send:
        notify_telegram_document(out_path, f"📊 گزارش بک‌تست {args.date_from}→{args.date_to}")
        notify_telegram(f"✅ بک‌تست تمام شد — {len(all_trades)} سیگنال")

    # گزارش ۷ روزه ۱ دقیقه
    if "1" in timeframes:
        days_1m, _ = recent_window_days("1")
        cutoff_1m = recent_anchor_ms - days_1m * 86400 * 1000

        rows = []
        for t in all_trades:
            if t.event.signal_bar_ts_ms >= cutoff_1m and t.event.timeframe == "1":
                rows.append({
                    "symbol": t.event.symbol,
                    "signal": t.event.signal,
                    "signal_time": ms_to_dt(t.event.signal_bar_ts_ms).astimezone(IRAN_TZ),
                    "entry": t.event.entry,
                    "stop": t.event.stop,
                    "target": t.event.target,
                    "status": t.status,
                    "exit_reason": t.exit_reason,
                    "exit_price": t.exit_price,
                    "pnl_usd": t.pnl_usd,
                    "pnl_r": t.pnl_r,
                })

        if rows:
            df_7d = pd.DataFrame(rows)
            xlsx_path = f"recent_7d_1m_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.xlsx"
            try:
                df_7d.to_excel(xlsx_path, index=False)
                if not args.no_send:
                    notify_telegram_document(xlsx_path, f"📊 سیگنال‌های {days_1m} روز اخیر — ۱ دقیقه")
            except Exception as e:
                logger.warning(f"ساخت اکسل شکست خورد: {e}")

    # حذف قفل
    try:
        RUN_LOCK_FILE.unlink()
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    main()
