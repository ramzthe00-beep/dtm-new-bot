#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest_report_final.py
نسخه نهایی و مستقل - بدون وابستگی به strategy_wrapper.py و trade_ledger.py
تمام منطق مورد نیاز به صورت inline پیاده‌سازی شده است.
"""

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
from typing import Optional, Callable

import requests
import pandas as pd
import numpy as np

# ============================================================
# مسیرها و ثابت‌ها
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
RESULTS_PATH = BASE_DIR / "backtest_results.json"
RUN_LOCK_FILE = BASE_DIR / ".backtest_run.lock"

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

# تلگرام
BACKTEST_TELEGRAM_BOT_TOKEN = os.getenv("BACKTEST_TELEGRAM_BOT_TOKEN", "8681448214:AAG4Ve-8GUTtQQS3wb5V9FDcuTeOoGbA4oM")
BACKTEST_TELEGRAM_CHAT_ID = os.getenv("BACKTEST_TELEGRAM_CHAT_ID", "7402770612")
_TELEGRAM_API_BASE = "https://api.telegram.org"
_TELEGRAM_MSG_LIMIT = 4000
_TELEGRAM_FILE_LIMIT_BYTES = 45 * 1024 * 1024

# ============================================================
# ارزها و تنظیمات
# ============================================================
SYMBOLS = ["ETHUSDT", "BNBUSDT"]
TIMEFRAMES = ["1"]

LEVERAGE_MAP = {
    "ETHUSDT": 50, "BNBUSDT": 75, "LTCUSDT": 75, "DOGEUSDT": 75,
    "XRPUSDT": 75, "ADAUSDT": 75, "DOTUSDT": 50, "PUMPUSDT": 75
}

TICK_SIZES = {
    "ETHUSDT": 0.01, "BNBUSDT": 0.01, "LTCUSDT": 0.01, "DOGEUSDT": 0.00001,
    "XRPUSDT": 0.0001, "ADAUSDT": 0.0001, "DOTUSDT": 0.001, "PUMPUSDT": 0.00001
}

HISTORY_BARS = 500
BASE_CAPITAL = 2.0
DAYS_DEFAULT = 365
BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]
KLINE_LIMIT = 1000
REQUEST_SLEEP = 0.15

# ============================================================
# 📊 INLINE: منطق trade_ledger (کپی دقیق از trade_ledger-1.py)
# ============================================================
LEDGER_BASE_CAPITAL = 2.0

def _safe_float(x):
    try:
        if x is None:
            return None
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (TypeError, ValueError):
        return None

def _hypothetical_pnl_usd(direction, entry, initial_stop, exit_price, leverage):
    """محاسبه PnL با استفاده از initial_stop (ریسک اولیه)"""
    try:
        if not entry or not initial_stop or entry <= 0:
            return None, None
        stop_pct = abs(entry - initial_stop) / entry
        if stop_pct <= 0:
            return None, None

        if direction == "LONG":
            move_pct = (exit_price - entry) / entry
        else:
            move_pct = (entry - exit_price) / entry

        r_multiple = move_pct / stop_pct

        lev = leverage if (leverage and leverage > 0) else 50
        old_leverage = 1.0 / stop_pct
        if old_leverage > lev:
            capital = (old_leverage / lev) * LEDGER_BASE_CAPITAL
        else:
            capital = LEDGER_BASE_CAPITAL

        pnl_usd = capital * lev * move_pct
        return round(pnl_usd, 4), round(r_multiple, 4)
    except Exception as e:
        return None, None

# ============================================================
# 🧠 INLINE: منطق strategy_wrapper (کپی دقیق از strategy_wrapper (22).py)
# ============================================================
try:
    from pynecore.core.ohlcv import OHLCV
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    from pynecore.core.script_runner import ScriptRunner
    PYNE_CORE_AVAILABLE = True
except ImportError as e:
    PYNE_CORE_AVAILABLE = False
    logging.error(f"❌ PyneCore در دسترس نیست: {e}")
    sys.exit(1)

STRATEGY_PATH = BASE_DIR / "strategy.py"

SYMBOL_TICK_INFO = {
    "LTCUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "LTC"},
    "DOGEUSDT": {"mintick": 0.00001, "pricescale": 100000, "basecurrency": "DOGE"},
    "ETHUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "ETH"},
    "BNBUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "BNB"},
    "PUMPUSDT": {"mintick": 0.00001, "pricescale": 100000, "basecurrency": "PUMP"},
}

def _is_na(x):
    return x is None or (isinstance(x, float) and math.isnan(x))

def _valid_num(x):
    return x is not None and not (isinstance(x, float) and x != x)

def _compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=2):
    """استاپ/تارگت سفارشی - مستقل از منطق واگرایی"""
    def _valid(x):
        return x is not None and not (isinstance(x, float) and math.isnan(x))

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
            return None, None, None, None

        stop = min(low1, low2) - buffer_abs
        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None, None
        
        mid_peak = max(c.high for c in candles[lo:hi + 1])
        risk = entry - stop
        if risk <= 0:
            return None, None, None, None

        rr = (mid_peak - entry) / risk
        target = mid_peak if rr >= 2 else entry + 2 * risk
        return stop, target, max(rr, 2.0), mid_peak

    elif signal == "SHORT":
        high1 = last_values.get("previous_pivot_high_price")
        high2 = last_values.get("pivot_high_price")
        bar1 = last_values.get("previous_pivot_high_index")
        bar2 = last_values.get("pivot_high_index")
        
        if not (_valid(high1) and _valid(high2) and _valid(bar1) and _valid(bar2)):
            return None, None, None, None

        stop = max(high1, high2) + buffer_abs
        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None, None
        
        mid_trough = min(c.low for c in candles[lo:hi + 1])
        risk = stop - entry
        if risk <= 0:
            return None, None, None, None

        rr = (entry - mid_trough) / risk
        target = mid_trough if rr >= 2 else entry - 2 * risk
        return stop, target, max(rr, 2.0), mid_trough

    return None, None, None, None

def calculate_signals(df, symbol="BNBUSDT", timeframe="1"):
    """محاسبه سیگنال با استفاده از PyneCore ScriptRunner"""
    logger = logging.getLogger("STRATEGY_WRAPPER")
    
    try:
        # تبدیل DataFrame به candles
        candles = []
        for idx, row in df.iterrows():
            ts = int(idx.timestamp() * 1000)
            candles.append(OHLCV(
                timestamp=ts,
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=float(row.get("volume", 0)),
                is_closed=True,
            ))

        # حذف کندل ناقص
        tf_minutes = int(timeframe)
        COMPLETION_SAFETY_BUFFER_SEC = 5
        completion_threshold_sec = tf_minutes * 60 + COMPLETION_SAFETY_BUFFER_SEC

        if len(candles) > 1:
            last_open_ts = candles[-1].timestamp / 1000.0
            candle_age = time.time() - last_open_ts
            if candle_age < completion_threshold_sec:
                candles = candles[:-1]
                logger.info(f"Removed incomplete candle | Remaining: {len(candles)}")

        if len(candles) < 50:
            return None, None, None, None, None, None

        signal_bar_ts_ms = candles[-1].timestamp if len(candles) > 0 else None

        # تنظیمات symbol
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
            opening_hours=[SymInfoInterval(day=0, start=datetime.min.time(), end=datetime.max.time())],
            session_starts=[SymInfoSession(day=0, time=datetime.min.time())],
            session_ends=[SymInfoSession(day=0, time=datetime.max.time())],
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

        # اجرا و دریافت نتایج
        last_values = None
        for result in runner.run_iter():
            if len(result) >= 2 and isinstance(result[1], dict) and len(result[1]) > 0:
                last_values = dict(result[1])

        if not last_values:
            return None, None, None, None, None, None

        signal = last_values.get("signal")
        entry = last_values.get("entry")
        
        if signal not in ("LONG", "SHORT"):
            signal = None

        # محاسبه استاپ و تارگت
        stop_price, target_price, rr_value, structural_level = None, None, None, None
        risk_free_pct = None

        if signal in ("LONG", "SHORT"):
            # تعیین buffer_ticks بر اساس نماد
            if symbol in ("BNBUSDT", "ETHUSDT"):
                buffer_ticks = 9
            elif symbol in ("LTCUSDT", "DOGEUSDT"):
                buffer_ticks = 3
            elif symbol == "PUMPUSDT":
                buffer_ticks = 1
            else:
                buffer_ticks = 5

            stop_price, target_price, rr_value, structural_level = _compute_stop_target(
                candles, signal, last_values, tick_info["mintick"], buffer_ticks=buffer_ticks
            )

            # محاسبه risk_free_pct
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

        return signal, entry, stop_price, target_price, signal_bar_ts_ms, risk_free_pct

    except Exception as e:
        logger.error(f"Error in calculate_signals: {e}")
        return None, None, None, None, None, None

# ============================================================
# ابزارهای تلگرام
# ============================================================
def notify_telegram(message: str) -> bool:
    if not (BACKTEST_TELEGRAM_BOT_TOKEN and BACKTEST_TELEGRAM_CHAT_ID):
        return False
    try:
        chunks = [message[i:i + _TELEGRAM_MSG_LIMIT] for i in range(0, len(message), _TELEGRAM_MSG_LIMIT)] or [message]
        for chunk in chunks:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{BACKTEST_TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": BACKTEST_TELEGRAM_CHAT_ID, "text": chunk},
                timeout=15,
            )
            if resp.status_code != 200:
                return False
        return True
    except Exception:
        return False

def notify_telegram_document(file_path, caption: str = "") -> bool:
    if not (BACKTEST_TELEGRAM_BOT_TOKEN and BACKTEST_TELEGRAM_CHAT_ID):
        return False
    try:
        size = Path(file_path).stat().st_size
        if size > _TELEGRAM_FILE_LIMIT_BYTES:
            notify_telegram(f"⚠️ فایل {Path(file_path).name} بیش از حد مجاز است ({size/1024/1024:.1f}MB)")
            return False
        with open(file_path, "rb") as f:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{BACKTEST_TELEGRAM_BOT_TOKEN}/sendDocument",
                data={"chat_id": BACKTEST_TELEGRAM_CHAT_ID, "caption": caption[:1024]},
                files={"document": (Path(file_path).name, f)},
                timeout=120,
            )
        return resp.status_code == 200
    except Exception as e:
        notify_telegram(f"⚠️ خطا در ارسال فایل: {e}")
        return False

# ============================================================
# مدیریت قفل
# ============================================================
def check_and_create_lock() -> bool:
    if RUN_LOCK_FILE.exists():
        return False
    RUN_LOCK_FILE.write_text(datetime.now(UTC_TZ).isoformat(), encoding="utf-8")
    return True

def release_lock() -> None:
    try:
        RUN_LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass

# ============================================================
# دریافت داده از Binance
# ============================================================
def fetch_klines(symbol, interval_min, start_ms, end_ms):
    interval_map = {
        "1": "1m", "3": "3m", "5": "5m", "15": "15m", "30": "30m",
        "60": "1h", "120": "2h", "240": "4h", "360": "6h", "480": "8h",
        "720": "12h", "1440": "1d"
    }
    interval = interval_map.get(str(interval_min), f"{interval_min}m")
    tf_ms = int(interval_min) * 60_000
    
    all_rows = {}
    cursor = start_ms
    session = requests.Session()
    
    while cursor <= end_ms:
        chunk = None
        last_err = None
        for attempt in range(3):
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
                    raise ValueError(f"Bad payload: {str(data)[:100]}")
                chunk = data
                break
            except Exception as e:
                last_err = e
                time.sleep(0.8 * (attempt + 1))
        
        if chunk is None:
            raise RuntimeError(f"Binance unreachable: {last_err}")
        if not chunk:
            break
            
        for row in chunk:
            try:
                ot = int(row[0])
                if ot not in all_rows:
                    all_rows[ot] = row
            except Exception:
                continue
                
        new_cursor = int(chunk[-1][0]) + tf_ms
        if new_cursor <= cursor:
            new_cursor = cursor + tf_ms
        cursor = new_cursor
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
    
    # حذف کندل ناقص آخر
    now_ms = int(time.time() * 1000)
    if rows and int(rows[-1][0]) + tf_ms > now_ms and len(df) > 0:
        df = df.iloc[:-1]
        
    return df

# ============================================================
# ساختارهای داده
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
    signal_type: str = ""
    score: int = 0

@dataclass
class TradeResult:
    event: SignalEvent
    exit_price: Optional[float] = None
    exit_time_ms: Optional[int] = None
    status: str = "OPEN"
    exit_reason: Optional[str] = None
    pnl_usd: Optional[float] = None
    pnl_r: Optional[float] = None
    bars_held: int = 0

# ============================================================
# تولید سیگنال‌ها (بازسازی دقیق لایو)
# ============================================================
def generate_signals_exact(df_full: pd.DataFrame, symbol: str, timeframe: str,
                            history_bars: int = HISTORY_BARS,
                            progress_cb: Optional[Callable] = None) -> list:
    n = len(df_full)
    if n < 50:
        return []
    
    events = []
    for i in range(history_bars, n):
        window = df_full.iloc[i-history_bars:i]
        if len(window) < 50:
            continue
            
        signal, entry, stop, target, signal_ts, rf_pct = calculate_signals(
            window, symbol, timeframe
        )
        
        if signal in ("LONG", "SHORT") and entry is not None and stop is not None:
            events.append(SignalEvent(
                symbol=symbol,
                timeframe=str(timeframe),
                signal=signal,
                entry=float(entry),
                stop=float(stop),
                target=float(target) if target is not None else None,
                signal_bar_ts_ms=int(signal_ts) if signal_ts else int(window.index[-1].timestamp() * 1000),
                risk_free_pct=float(rf_pct) if rf_pct is not None else None
            ))
            
        if progress_cb and i % 1000 == 0:
            progress_cb(i, n)
            
    return events

# ============================================================
# حل معامله (برخورد با استاپ/تارگت)
# ============================================================
def resolve_trade(ev: SignalEvent, df_full: pd.DataFrame, ts_to_idx: dict) -> TradeResult:
    res = TradeResult(event=ev)
    i0 = ts_to_idx.get(ev.signal_bar_ts_ms)
    if i0 is None:
        res.exit_reason = "NO_RESOLUTION"
        return res

    direction = ev.signal
    entry = ev.entry
    initial_stop = ev.stop
    stop = ev.stop
    target = ev.target
    risk_free_armed = False
    risk_free_pct = ev.risk_free_pct
    initial_risk = abs(entry - initial_stop)
    
    if initial_risk <= 0:
        res.exit_reason = "NO_RESOLUTION"
        return res

    n = len(df_full)
    bars_held = 0
    
    for i in range(i0 + 1, min(n, i0 + 10000)):
        bars_held += 1
        row = df_full.iloc[i]
        hi, lo = float(row["high"]), float(row["low"])
        candle_ts_ms = int(df_full.index[i].timestamp() * 1000)
        
        # چک ریسک فری
        if not risk_free_armed and risk_free_pct is not None:
            if direction == "LONG":
                rf_trigger = entry * (1 + risk_free_pct)
                if hi >= rf_trigger:
                    stop = entry
                    risk_free_armed = True
            else:
                rf_trigger = entry * (1 - abs(risk_free_pct))
                if lo <= rf_trigger:
                    stop = entry
                    risk_free_armed = True
        
        hit_stop = (lo <= stop) if direction == "LONG" else (hi >= stop)
        hit_target = (target is not None) and ((hi >= target) if direction == "LONG" else (lo <= target))
        
        # قانون محافظه‌کارانه: اگر هر دو لمس شدند، استاپ برنده است
        if hit_stop and hit_target:
            hit_target = False
            
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
    
    if res.status != "OPEN":
        res.pnl_usd, res.pnl_r = _hypothetical_pnl_usd(
            direction, entry, initial_stop, res.exit_price,
            LEVERAGE_MAP.get(ev.symbol, 50)
        )
    else:
        res.exit_reason = "STILL_OPEN"
        
    return res

# ============================================================
# متریک‌های پرتفوی
# ============================================================
def compute_metrics(trades: list) -> dict:
    closed = [t for t in trades if t.status in ("WIN", "LOSS") and t.pnl_usd is not None]
    if not closed:
        return {"n_closed": 0, "total_pnl_usd": 0, "win_rate": 0}
    
    wins = [t for t in closed if t.status == "WIN"]
    losses = [t for t in closed if t.status == "LOSS"]
    total_pnl = sum(t.pnl_usd for t in closed)
    win_rate = len(wins) / len(closed) * 100
    
    gross_win = sum(t.pnl_usd for t in wins if t.pnl_usd > 0)
    gross_loss = abs(sum(t.pnl_usd for t in losses if t.pnl_usd < 0))
    pf = gross_win / gross_loss if gross_loss > 0 else float('inf')
    
    return {
        "n_signals": len(trades),
        "n_closed": len(closed),
        "n_wins": len(wins),
        "n_losses": len(losses),
        "win_rate": win_rate,
        "total_pnl_usd": total_pnl,
        "profit_factor": pf,
        "avg_win": statistics.mean([t.pnl_usd for t in wins]) if wins else 0,
        "avg_loss": statistics.mean([t.pnl_usd for t in losses]) if losses else 0,
    }

# ============================================================
# اجرای اصلی
# ============================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--symbols", nargs="*", default=SYMBOLS)
    parser.add_argument("--tfs", nargs="*", default=TIMEFRAMES)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-send", action="store_true")
    args = parser.parse_args()
    
    lock_acquired = False
    try:
        if not args.force and not check_and_create_lock():
            notify_telegram("⏭️ قفل وجود دارد. از --force استفاده کنید.")
            return 0
        lock_acquired = True
        
        # شروع
        start_msg = f"🚀 شروع بک‌تست مستقل\n📅 {args.days} روز\n🎯 {args.symbols}"
        print(start_msg)
        if not args.no_send:
            notify_telegram(start_msg)
        
        end_ms = int(time.time() * 1000)
        start_ms = end_ms - args.days * 24 * 3600 * 1000
        
        all_trades = []
        
        for tf in args.tfs:
            for sym in args.symbols:
                print(f"در حال پردازش {sym} {tf}m...")
                
                # دریافت داده
                df = fetch_klines(sym, tf, start_ms - HISTORY_BARS*int(tf)*60*1000, end_ms)
                if df.empty or len(df) < HISTORY_BARS + 10:
                    print(f"⚠️ داده کافی نیست برای {sym}")
                    continue
                
                # تولید سیگنال
                events = generate_signals_exact(df, sym, tf)
                
                # حل معاملات
                ts_to_idx = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df.index)}
                trades = [resolve_trade(ev, df, ts_to_idx) for ev in events]
                all_trades.extend(trades)
                
                # گزارش جزئی
                metrics = compute_metrics(trades)
                msg = (f"✅ {sym} {tf}m: سیگنال={metrics['n_signals']} | "
                       f"بسته={metrics['n_closed']} | WinRate={metrics['win_rate']:.1f}% | "
                       f"PnL=${metrics['total_pnl_usd']:.2f}")
                print(msg)
                if not args.no_send:
                    notify_telegram(msg)
        
        # گزارش نهایی
        final_metrics = compute_metrics(all_trades)
        final_msg = (
            f"🏁 بک‌تست تمام شد\n"
            f"📊 کل سیگنال: {final_metrics['n_signals']}\n"
            f"💰 PnL کل: ${final_metrics['total_pnl_usd']:.2f}\n"
            f"🏆 Win Rate: {final_metrics['win_rate']:.1f}%\n"
            f"⚖️ Profit Factor: {final_metrics['profit_factor']:.2f}"
        )
        print(final_msg)
        if not args.no_send:
            notify_telegram(final_msg)
            
        # ذخیره نتایج
        results = {
            "meta": {"days": args.days, "symbols": args.symbols, "tfs": args.tfs},
            "metrics": final_metrics,
            "trades": [
                {
                    "symbol": t.event.symbol,
                    "tf": t.event.timeframe,
                    "dir": t.event.signal,
                    "entry": t.event.entry,
                    "stop": t.event.stop,
                    "target": t.event.target,
                    "exit": t.exit_price,
                    "pnl": t.pnl_usd,
                    "status": t.status,
                    "reason": t.exit_reason
                } for t in all_trades
            ]
        }
        with open(RESULTS_PATH, "w") as f:
            json.dump(results, f, indent=2)
            
        return 0
        
    except Exception as e:
        err_msg = f"❌ خطا: {e}"
        print(err_msg)
        notify_telegram(err_msg)
        return 1
    finally:
        if lock_acquired:
            release_lock()

if __name__ == "__main__":
    sys.exit(main())
