# -*- coding: utf-8 -*-
"""
backtest_report.py
==================
بک‌تست مستقل استراتژی DTM روی داده‌های واقعی Binance Spot برای N روز گذشته
(پیش‌فرض ۶۰ روز ≈ ۲ ماه) + گزارش کامل و تفکیکی به تلگرام.

• هیچ دست‌زدنی به bot.py / trade_ledger.jsonl ندارد و سفارشی روی صرافی ثبت نمی‌کند.
• سیگنال‌ها: عیناً strategy.py از طریق PyneCore ScriptRunner (یک پاس کامل روی کل تاریخچه)
• استاپ/تارگت: عیناً همان _compute_stop_target در strategy_wrapper
• PnL و شبیه‌سازی ریسک‌فری: عیناً همان فرمول trade_ledger (سرمایه پایه ۲$، استاپ برنده در همان کندل)

اجرا:
    python backtest_report.py                  → گزارش کامل ۶۰ روزه (روزی فقط ۱ بار ارسال)
    python backtest_report.py --mode both      → گزارش کامل + تفکیک هر ارز در هر تایم‌فریم
    python backtest_report.py --mode breakdown → فقط گزارش‌های تفکیکی ارز/تایم‌فریم
    python backtest_report.py --days 30        → بازه ۳۰ روزه
    python backtest_report.py --tfs 5          → فقط تایم‌فریم ۵ دقیقه (سریع‌تر)
    python backtest_report.py --force          → نادیده‌گرفتن قفل روزانه
    python backtest_report.py --resend         → ارسال مجدد از نتایج ذخیره‌شده (بدون محاسبه)
    python backtest_report.py --no-send        → فقط چاپ/ذخیره، بدون تلگرام
"""

import os
import sys
import json
import math
import time
import argparse
import logging
import traceback
from pathlib import Path
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd

# ============================================================
# مسیرها و ثابت‌ها
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
STRATEGY_PATH = BASE_DIR / "strategy.py"
RESULTS_PATH = BASE_DIR / "backtest_results.json"
MARKER_PATH = BASE_DIR / "backtest_report_state.json"

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")

SYMBOLS = ["LTCUSDT", "DOGEUSDT", "ETHUSDT", "BNBUSDT", "PUMPUSDT"]
TIMEFRAMES = ["1", "5"]
LEVERAGE_MAP = {"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50, "BNBUSDT": 75, "PUMPUSDT": 75}
BASE_CAPITAL = 2.0
DAYS_DEFAULT = 60
WARMUP_DAYS = 2          # روزهای گرم‌کردن اندیکاتورها (محاسبه نمی‌شوند، فقط state می‌سازند)
BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]
KLINE_LIMIT = 1000
REQUEST_SLEEP = 0.15

# mintick — عیناً همان SYMBOL_TICK_INFO در strategy_wrapper (منبع رسمی SL/TP سیگنال)
SYMBOL_TICK_INFO = {
    "LTCUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "LTC"},
    "DOGEUSDT": {"mintick": 0.00001, "pricescale": 100000, "basecurrency": "DOGE"},
    "ETHUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "ETH"},
    "BNBUSDT":  {"mintick": 0.01,    "pricescale": 100,    "basecurrency": "BNB"},
    "PUMPUSDT": {"mintick": 0.00001, "pricescale": 100000, "basecurrency": "PUMP"},
}

# ورودی‌های استراتژی — عیناً همان مقادیر strategy_wrapper
STRATEGY_INPUTS = {
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

SCORE_KEYS = {
    "CD-": "score_classic_bearish",
    "CD+": "score_classic_bullish",
    "HD+": "score_hidden_bullish",
    "HD-": "score_hidden_bearish",
}
WD_FA = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
W = "━━━━━━━━━━━━━━━━━━━━"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BACKTEST")


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


# ============================================================
# تلگرام — هرگز Exception بالا نمی‌اندازد
# ============================================================
def tg_send(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=30)
        return r.ok
    except Exception as e:
        logger.error(f"[TG] send error: {e}")
        return False


def tg_send_long(text):
    text = str(text)
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)] or [text]
    ok = True
    for part in chunks:
        sent = False
        for attempt in range(3):
            if tg_send(part):
                sent = True
                break
            time.sleep(1 + attempt)
        if not sent:
            ok = False
        time.sleep(0.4)
    return ok


# ============================================================
# موتور استراتژی — عیناً strategy_wrapper (با fallback محلی)
# ============================================================
try:
    import strategy_wrapper as _sw
    try:
        _sw._send_telegram = lambda text: True  # خفه‌کردن تلگرامِ wrapper در بک‌تست
    except Exception:
        pass
    _compute_stop_target = _sw._compute_stop_target
    SYMBOL_TICK_INFO = getattr(_sw, "SYMBOL_TICK_INFO", SYMBOL_TICK_INFO)
    ENGINE_NAME = "strategy_wrapper (import شد)"
except Exception as e:
    logger.warning(f"[ENGINE] strategy_wrapper import نشد → fallback محلی: {e}")
    ENGINE_NAME = "fallback محلی"
    _sw = None

try:
    from pynecore.core.ohlcv import OHLCV
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    from pynecore.core.script_runner import ScriptRunner
except Exception as e:
    logger.error(f"[FATAL] pynecore در دسترس نیست: {e}")
    tg_send(f"❌ backtest_report: pynecore نصب نیست یا خراب است:\n{e}")
    sys.exit(1)


def _local_compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=2):
    """کپی عیناً از strategy_wrapper — فقط وقتی import نشد."""
    def _v(x):
        return x is not None and not (isinstance(x, float) and math.isnan(x))
    entry = last_values.get("entry")
    if not _v(entry):
        return None, None, None, None
    buffer_abs = buffer_ticks * mintick
    if signal == "LONG":
        low1 = last_values.get("previous_pivot_low_price")
        low2 = last_values.get("pivot_low_price")
        bar1 = last_values.get("previous_pivot_low_index")
        bar2 = last_values.get("pivot_low_index")
        if not (_v(low1) and _v(low2) and _v(bar1) and _v(bar2)):
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
        if not (_v(high1) and _v(high2) and _v(bar1) and _v(bar2)):
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


if _sw is None:
    _compute_stop_target = _local_compute_stop_target


try:
    from trade_ledger import _hypothetical_pnl_usd as pnl_fn
    from trade_ledger import BASE_CAPITAL as _BC
    BASE_CAPITAL = float(_BC)
except Exception as e:
    logger.warning(f"[LEDGER] trade_ledger import نشد → فرمول محلی: {e}")

    def pnl_fn(direction, entry, initial_stop, exit_price, leverage):
        try:
            if not entry or not initial_stop or entry <= 0:
                return None, None
            stop_pct = abs(entry - initial_stop) / entry
            if stop_pct <= 0:
                return None, None
            move_pct = (exit_price - entry) / entry if direction == "LONG" else (entry - exit_price) / entry
            r_multiple = move_pct / stop_pct
            lev = leverage if (leverage and leverage > 0) else 50
            old_leverage = 1.0 / stop_pct
            capital = (old_leverage / lev) * BASE_CAPITAL if old_leverage > lev else BASE_CAPITAL
            return round(capital * lev * move_pct, 4), round(r_multiple, 4)
        except Exception:
            return None, None


def _build_syminfo(symbol, timeframe):
    tick = SYMBOL_TICK_INFO.get(
        symbol, {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")}
    )
    return SymInfo(
        prefix="", description=f"{symbol} {timeframe}m", ticker=symbol,
        currency="USDT", basecurrency=tick["basecurrency"], period=str(timeframe),
        type="crypto", volumetype="base", mintick=tick["mintick"], pricescale=tick["pricescale"],
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
    if symbol == "PUMPUSDT":
        return 1
    return 5


def compute_rf_pct(signal, entry, stop, structural_level):
    """عیناً همان منطق strategy_wrapper برای rf_pct."""
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
# دریافت دیتا از Binance Spot — صفحه‌بندی‌شده و مقاوم
# ============================================================
def fetch_klines(symbol, interval_min, start_ms, end_ms):
    interval = f"{int(interval_min)}m"
    tf_ms = int(interval_min) * 60_000
    all_rows = {}
    cursor = start_ms
    session = requests.Session()

    while cursor <= end_ms:
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

    # حذف کندلِ ناقص انتهایی (اگر هنوز باز است)
    now_ms = int(time.time() * 1000)
    if rows and int(rows[-1][0]) + tf_ms > now_ms and len(df) > 0:
        df = df.iloc[:-1]
    return df


def df_to_candles(df):
    candles = []
    for idx, row in df.iterrows():
        candles.append(OHLCV(
            timestamp=int(idx.timestamp() * 1000),
            open=float(row["open"]), high=float(row["high"]),
            low=float(row["low"]), close=float(row["close"]),
            volume=float(row.get("volume", 0) or 0), is_closed=True,
        ))
    return candles


# ============================================================
# یک پاس کامل استراتژی روی کل تاریخچه (به‌جای پنجره‌های لغزان)
# هر بارِ تاییدِ پیوت = یک سیگنال — دقیقاً مثل لایو
# ============================================================
def run_strategy_pass(candles, symbol, timeframe):
    syminfo = _build_syminfo(symbol, timeframe)
    runner = ScriptRunner(
        STRATEGY_PATH, iter(candles), syminfo,
        last_bar_index=len(candles) - 1, inputs=dict(STRATEGY_INPUTS),
    )
    hits = []
    logging.disable(logging.INFO)  # خفه‌کردن لاگ‌های حجیم strategy.py حین اجرا
    try:
        for i, result in enumerate(runner.run_iter()):
            try:
                if not (isinstance(result, (tuple, list)) and len(result) >= 2):
                    continue
                lv = result[1]
                if not (isinstance(lv, dict) and len(lv) > 0):
                    continue
                sig = lv.get("signal")
                if sig not in ("LONG", "SHORT"):
                    continue
                entry = _f(lv.get("entry"))
                if entry is None or entry <= 0:
                    continue
                hits.append((i, lv, sig, entry))
            except Exception:
                continue
    finally:
        logging.disable(logging.NOTSET)
    return hits


# ============================================================
# شبیه‌سازی هر معامله — عیناً منطق trade_ledger.update_open_trades
# (ریسک‌فری: استاپ → ورود؛ در یک کندل اگر هم استاپ هم تارگت → استاپ برنده)
# ============================================================
def simulate_trade(tr, candles, n):
    try:
        entry, initial_stop = tr["entry"], tr["stop"]
        target, direction = tr["target"], tr["direction"]
        rf = tr.get("rf_pct")
        stop, risk_free = initial_stop, False

        for j in range(tr["entry_idx"] + 1, n):   # کندل ورود خودش چک نمی‌شود (مثل لایو)
            c = candles[j]
            high, low = float(c.high), float(c.low)
            ts = int(c.timestamp)

            if not risk_free and rf is not None:
                if direction == "LONG":
                    crossed = high >= entry * (1 + abs(rf))
                else:
                    crossed = low <= entry * (1 - abs(rf))
                if crossed:
                    risk_free = True
                    stop = entry  # سربه‌سر (تقریب بدون کارمزد — مثل trade_ledger)

            if direction == "LONG":
                hit_stop = low <= stop
                hit_target = (target is not None) and high >= target
            else:
                hit_stop = high >= stop
                hit_target = (target is not None) and low <= target

            if hit_stop:
                tr["status"] = "WIN" if risk_free else "LOSS"
                tr["exit_reason"] = "RISK_FREE_STOP" if risk_free else "STOP_LOSS"
                tr["exit_price"], tr["exit_time_ms"] = stop, ts
                break
            if hit_target:
                tr["status"], tr["exit_reason"] = "WIN", "TARGET"
                tr["exit_price"], tr["exit_time_ms"] = target, ts
                break

        tr["risk_free"] = risk_free
        if tr["status"] != "OPEN":
            pnl, r = pnl_fn(direction, entry, initial_stop, tr["exit_price"], tr["leverage"])
            tr["pnl_usd"], tr["pnl_r"] = pnl, r
    except Exception as e:
        logger.warning(f"[SIM] {tr.get('symbol')} error: {e}")
        tr["status"] = "OPEN"


# ============================================================
# بک‌تست یک ترکیب ارز/تایم‌فریم
# ============================================================
def backtest_combo(symbol, timeframe, start_ms, end_ms):
    fetch_start = start_ms - WARMUP_DAYS * 86_400_000
    df = fetch_klines(symbol, int(timeframe), fetch_start, end_ms)
    if df is None or df.empty:
        raise RuntimeError("دیتای خالی از Binance")
    if len(df) < 300:
        raise RuntimeError(f"کندل کافی نیست: {len(df)}")

    candles = df_to_candles(df)
    n = len(candles)
    mintick = SYMBOL_TICK_INFO.get(symbol, {"mintick": 0.01})["mintick"]
    raw_hits = run_strategy_pass(candles, symbol, timeframe)

    seen, trades = set(), []
    for (i, lv, sig, entry) in raw_hits:
        try:
            ts = int(candles[i].timestamp)
            if ts < start_ms or ts > end_ms:      # کندل‌های warmup حساب نمی‌شوند
                continue
            key = (symbol, str(timeframe), ts, sig)
            if key in seen:                        # ضدتکرار ایمنی
                continue
            seen.add(key)

            stop, target, rr, struct = None, None, None, None
            try:
                stop, target, rr, struct = _compute_stop_target(
                    candles, sig, lv, mintick, buffer_ticks=buffer_ticks_for(symbol)
                )
            except Exception:
                stop = None
            if stop is None or target is None or abs(entry - stop) <= 0:
                continue  # مثل لایو: سیگنال بدون استاپِ معتبر ثبت نمی‌شود

            tr = {
                "symbol": symbol, "timeframe": str(timeframe), "direction": sig,
                "entry": float(entry), "stop": float(stop), "target": float(target),
                "entry_time_ms": ts, "entry_idx": int(i),
                "leverage": LEVERAGE_MAP.get(symbol, 50),
                "signal_type": signal_type_of(lv) or "?", "score": _score_of(lv, signal_type_of(lv)),
                "rf_pct": compute_rf_pct(sig, entry, stop, struct),
                "rr_planned": _f(rr),
                "status": "OPEN", "exit_reason": None, "exit_price": None,
                "exit_time_ms": None, "pnl_usd": None, "pnl_r": None, "risk_free": False,
            }
            simulate_trade(tr, candles, n)
            trades.append(tr)
        except Exception as e:
            logger.warning(f"[BT] {symbol} {timeframe}m bar {i}: {e}")
            continue

    return trades, n, len(raw_hits)


# ============================================================
# آمار و گزارش
# ============================================================
def stats_of(trades):
    s = {"total": len(trades)}
    wins = [t for t in trades if t.get("status") == "WIN"]
    losses = [t for t in trades if t.get("status") == "LOSS"]
    opens = [t for t in trades if t.get("status") == "OPEN"]
    closed = wins + losses
    s.update(wins=len(wins), losses=len(losses), opens=len(opens), closed=len(closed))
    s["rf_wins"] = sum(1 for t in wins if t.get("exit_reason") == "RISK_FREE_STOP")
    s["tp_wins"] = sum(1 for t in wins if t.get("exit_reason") == "TARGET")
    s["winrate"] = (len(wins) / len(closed) * 100) if closed else 0.0

    pnls = [t["pnl_usd"] for t in closed if t.get("pnl_usd") is not None]
    s["pnl_total"] = sum(pnls)
    gw = sum(p for p in pnls if p > 0)
    gl = sum(p for p in pnls if p < 0)
    s["pf"] = (gw / abs(gl)) if gl < 0 else (float("inf") if gw > 0 else 0.0)
    s["avg_win"] = gw / len(wins) if wins else 0.0
    s["avg_loss"] = gl / len(losses) if losses else 0.0

    rs = [t["pnl_r"] for t in closed if t.get("pnl_r") is not None]
    s["avg_r"] = sum(rs) / len(rs) if rs else 0.0
    rrs = [t["rr_planned"] for t in trades if t.get("rr_planned")]
    s["avg_rr"] = sum(rrs) / len(rrs) if rrs else 0.0

    seq = sorted([t for t in closed if t.get("pnl_usd") is not None],
                 key=lambda t: t.get("exit_time_ms") or t["entry_time_ms"])
    streak = best_streak = 0
    cum = peak = 0.0
    dd = 0.0
    for t in seq:
        if t["status"] == "LOSS":
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            streak = 0
        cum += t["pnl_usd"]
        peak = max(peak, cum)
        dd = min(dd, cum - peak)
    s["max_consec_loss"] = best_streak
    s["max_dd"] = dd

    durs = [(t["exit_time_ms"] - t["entry_time_ms"]) / 60000.0
            for t in closed if t.get("exit_time_ms")]
    s["avg_hold_min"] = sum(durs) / len(durs) if durs else 0.0
    return s


def fmt_money(x):
    return f"{x:+.2f}$" if x is not None else "—"


def fmt_pf(pf):
    return "∞" if pf == float("inf") else f"{pf:.2f}"


def group_dict(items, keyfn):
    d = {}
    for it in items:
        d.setdefault(keyfn(it), []).append(it)
    return d


def fmt_trade_line(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    ts = dt.strftime("%m-%d %H:%M") if dt else "?"
    emoji = {"WIN": "✅", "LOSS": "❌", "OPEN": "⏳"}.get(t.get("status"), "•")
    if t.get("exit_reason") == "RISK_FREE_STOP":
        emoji = "🛡️"
    r = t.get("pnl_r")
    r_str = f"{r:+.2f}R" if r is not None else "—"
    return f"  {emoji} {ts} | {t['timeframe']}m | {t.get('signal_type','?')} S{t.get('score',0)} | {r_str} {fmt_money(t.get('pnl_usd'))}"


def _section(lines, title, trades, keyfn):
    g = group_dict(trades, keyfn)
    if not g:
        return
    lines.append(W)
    lines.append(title)
    for k in sorted(g.keys(), key=str):
        stg = stats_of(g[k])
        lines.append(f"  • {k}: {stg['total']} سیگنال | ✅{stg['wins']} ❌{stg['losses']} ⏳{stg['opens']} "
                     f"| نرخ {stg['winrate']:.0f}٪ | {fmt_money(stg['pnl_total'])}")


def hour_bucket(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    return f"{(dt.hour // 4) * 4:02d}-{(dt.hour // 4) * 4 + 3:02d}" if dt else "?"


def weekday_fa(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    return WD_FA[dt.weekday()] if dt else "?"


def build_insights(trades):
    lines = ["🧠 بینش‌ها و پیشنهاد بهینه‌سازی:"]
    closed = [t for t in trades if t.get("status") in ("WIN", "LOSS")]
    if len(closed) < 10:
        lines.append("  • معاملات بسته‌شده کم است؛ بینش معنادار نیست.")
        return lines
    base = stats_of(trades)
    lines.append(f"  • ساختار R ثابت است: ضرر −1R | ریسک‌فری 0R | تارگت ≥ +2R → سربه‌سر ≈ ۳۳٪ نرخ برد")
    lines.append(f"  • نرخ برد پایه: {base['winrate']:.1f}٪ | PF: {fmt_pf(base['pf'])}")

    combos = group_dict(trades, lambda t: f"{t['symbol']} {t['timeframe']}m")
    qualified = [(k, stats_of(v)) for k, v in combos.items() if stats_of(v)["closed"] >= 5]
    if qualified:
        best = max(qualified, key=lambda kv: kv[1]["pnl_total"])
        worst = min(qualified, key=lambda kv: kv[1]["pnl_total"])
        lines.append(f"  • بهترین ترکیب: {best[0]} → {fmt_money(best[1]['pnl_total'])} (نرخ {best[1]['winrate']:.0f}٪)")
        lines.append(f"  • ضعیف‌ترین ترکیب: {worst[0]} → {fmt_money(worst[1]['pnl_total'])} (نرخ {worst[1]['winrate']:.0f}٪)")

    types = [(k, stats_of(v)) for k, v in group_dict(trades, lambda t: t.get("signal_type", "?")).items()
             if stats_of(v)["closed"] >= 5]
    if types:
        bt = max(types, key=lambda kv: kv[1]["pnl_total"])
        lines.append(f"  • بهترین نوع سیگنال: {bt[0]} → {fmt_money(bt[1]['pnl_total'])} (نرخ {bt[1]['winrate']:.0f}٪)")

    for s in (4, 3):
        sub = [t for t in closed if (t.get("score") or 0) >= s]
        if len(sub) >= 10:
            stg = stats_of(sub)
            better = "بهتر" if stg["winrate"] > base["winrate"] else "بدتر"
            lines.append(f"  • فیلتر امتیاز ≥ {s}: نرخ {stg['winrate']:.1f}٪ و {fmt_money(stg['pnl_total'])} "
                         f"در {stg['closed']} معامله → {better} از پایه ({base['winrate']:.1f}٪)")
            break

    buckets = [(k, stats_of(v)) for k, v in group_dict(trades, hour_bucket).items()
               if stats_of(v)["closed"] >= 8]
    if len(buckets) >= 2:
        bb = max(buckets, key=lambda kv: kv[1]["pnl_total"])
        bw = min(buckets, key=lambda kv: kv[1]["pnl_total"])
        lines.append(f"  • بهترین بازه ساعتی (تهران): {bb[0]} → {fmt_money(bb[1]['pnl_total'])}")
        lines.append(f"  • بدترین بازه ساعتی (تهران): {bw[0]} → {fmt_money(bw[1]['pnl_total'])}")

    wds = [(k, stats_of(v)) for k, v in group_dict(trades, weekday_fa).items()
           if stats_of(v)["closed"] >= 8]
    if len(wds) >= 2:
        ww = min(wds, key=lambda kv: kv[1]["pnl_total"])
        lines.append(f"  • بدترین روز هفته: {ww[0]} → {fmt_money(ww[1]['pnl_total'])}")
    return lines


def build_overall_report(trades, meta):
    st = stats_of(trades)
    L = ["📊 گزارش کامل بک‌تست استراتژی DTM", W]
    L.append(f"🗓 بازه: {meta['start_date']} تا {meta['end_date']} ({meta['days']} روز — تهران)")
    L.append(f"📡 دیتا: Binance Spot | تایم‌فریم: {', '.join(tf + 'm' for tf in meta['tfs'])}")
    L.append(f"🕐 تولید گزارش: {meta['generated_at']} (تهران)")
    L.append(f"⚙️ موتور سیگنال: {meta['engine']}")
    L.append(W)
    L.append(f"📈 کل سیگنال‌ها: {st['total']}")
    L.append(f"✅ برنده: {st['wins']}  (🎯 تارگت: {st['tp_wins']} | 🛡️ ریسک‌فری: {st['rf_wins']})")
    L.append(f"❌ بازنده: {st['losses']}")
    L.append(f"⏳ هنوز باز: {st['opens']}")
    L.append(f"🏆 نرخ برد: {st['winrate']:.1f}٪ (از {st['closed']} معامله بسته‌شده)")
    L.append(f"💰 سود/زیان فرضی کل: {fmt_money(st['pnl_total'])} (سرمایه پایه {BASE_CAPITAL:.0f}$)")
    L.append(f"⚖️ پروفیت فکتور: {fmt_pf(st['pf'])}")
    L.append(f"📊 میانگین R: {st['avg_r']:.2f} | میانگین برد: {fmt_money(st['avg_win'])} | میانگین باخت: {fmt_money(st['avg_loss'])}")
    L.append(f"🎯 میانگین R:R برنامه‌ریزی‌شده: 1:{st['avg_rr']:.2f}")
    L.append(f"⏱ میانگین طول معامله: {st['avg_hold_min']:.0f} دقیقه")
    L.append(f"🔥 حداکثر باخت متوالی: {st['max_consec_loss']}")
    L.append(f"📉 حداکثر افت سرمایه: {fmt_money(st['max_dd'])}")

    _section(L, "💼 به تفکیک ارز:", trades, lambda t: t["symbol"])
    _section(L, "🕐 به تفکیک تایم‌فریم:", trades, lambda t: f"{t['timeframe']}m")
    _section(L, "🔀 به تفکیک نوع سیگنال:", trades, lambda t: t.get("signal_type", "?"))
    _section(L, "⭐ به تفکیک امتیاز:", trades, lambda t: f"امتیاز {t.get('score', 0)}")

    cs = sorted([t for t in trades if t.get("pnl_usd") is not None], key=lambda t: t["pnl_usd"])
    if cs:
        L.append(W)
        L.append("🏅 ۵ معامله برتر:")
        for t in cs[-5:][::-1]:
            L.append(fmt_trade_line(t))
        L.append("💥 ۵ معامله ضعیف:")
        for t in cs[:5]:
            L.append(fmt_trade_line(t))

    L.append(W)
    L.extend(build_insights(trades))

    if meta.get("combos"):
        L.append(W)
        L.append("🧮 جزئیات اجرا:")
        for c in meta["combos"]:
            L.append(f"  • {c['symbol']} {c['tf']}m | کندل: {c['bars']} | سیگنال خام: {c['raw_hits']} | معاملات: {c['signals']}")
    if meta.get("errors"):
        L.append(W)
        L.append("⚠️ خطاهای بک‌تست:")
        for e in meta["errors"][:20]:
            L.append(f"  • {e}")
    L.append(W)
    L.append("⚠️ نتایج فرضی است (بدون اسلیپیج/کارمزد واقعی) — صرفاً برای ارزیابی استراتژی.")
    return "\n".join(L)


def build_combo_report(sym, tf, trades):
    st = stats_of(trades)
    L = [f"📋 گزارش تفکیکی {sym} — {tf} دقیقه", W]
    if st["total"] == 0:
        L.append("در این بازه هیچ سیگنالی ثبت نشد.")
        return "\n".join(L)
    L.append(f"📈 سیگنال‌ها: {st['total']} | ✅{st['wins']} (🎯{st['tp_wins']} 🛡️{st['rf_wins']}) | ❌{st['losses']} | ⏳{st['opens']}")
    L.append(f"🏆 نرخ برد: {st['winrate']:.1f}٪ | 💰 {fmt_money(st['pnl_total'])} | PF: {fmt_pf(st['pf'])}")
    L.append(f"📊 میانگین R: {st['avg_r']:.2f} | 🔥 باخت متوالی: {st['max_consec_loss']} | 📉 افت: {fmt_money(st['max_dd'])}")
    L.append(W)
    items = sorted(trades, key=lambda t: t["entry_time_ms"])
    if len(items) <= 25:
        L.append("🧾 همه معاملات:")
        for t in items:
            L.append(fmt_trade_line(t))
    else:
        cs = sorted([t for t in items if t.get("pnl_usd") is not None], key=lambda t: t["pnl_usd"])
        L.append("🏅 ۵ معامله برتر:")
        for t in cs[-5:][::-1]:
            L.append(fmt_trade_line(t))
        L.append("💥 ۵ معامله ضعیف:")
        for t in cs[:5]:
            L.append(fmt_trade_line(t))
        L.append(f"  … و {len(items) - 10} معامله دیگر")
    return "\n".join(L)


# ============================================================
# ذخیره/بارگذاری نتایج و قفل روزانه
# ============================================================
def save_results(trades, meta):
    try:
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "trades": trades}, f, ensure_ascii=False)
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


def marker_already_sent(mode):
    try:
        data = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
        return data.get(mode) == today_str()
    except Exception:
        return False


def marker_set(mode):
    try:
        data = {}
        if MARKER_PATH.exists():
            data = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
        data[mode] = today_str()
        MARKER_PATH.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.error(f"[MARKER] {e}")


def save_report_backup(text):
    try:
        p = BASE_DIR / f"backtest_report_{datetime.now(UTC_TZ).strftime('%Y%m%d_%H%M')}.txt"
        p.write_text(text, encoding="utf-8")
        logger.info(f"[BACKUP] گزارش در {p.name} ذخیره شد")
    except Exception as e:
        logger.error(f"[BACKUP] {e}")


# ============================================================
# ارسال گزارش‌ها
# ============================================================
def send_reports(trades, meta, mode, do_send):
    texts = []
    if mode in ("full", "both"):
        texts.append(("📊 گزارش کامل", build_overall_report(trades, meta)))
    if mode in ("breakdown", "both"):
        groups = group_dict(trades, lambda t: (t["symbol"], t["timeframe"]))
        order = {(s, tf) for s in meta.get("symbols", SYMBOLS) for tf in meta.get("tfs", TIMEFRAMES)}
        keys = sorted(set(groups.keys()) | order, key=lambda k: (k[0], int(k[1])))
        for (sym, tf) in keys:
            texts.append((f"📋 {sym} {tf}m", build_combo_report(sym, tf, groups.get((sym, tf), []))))

    full_text = "\n\n" + ("═" * 30) + "\n\n".join(f"{h}\n{b}" for h, b in texts)
    save_report_backup(full_text)

    if not do_send:
        print(full_text)
        return True

    ok = True
    for header, body in texts:
        ok = tg_send_long(f"{header}\n\n{body}") and ok
        time.sleep(1)
    if not ok:
        logger.error("[SEND] ارسال تلگرام ناقص بود — با --resend دوباره بفرست")
    return ok


# ============================================================
# main
# ============================================================
def parse_args():
    p = argparse.ArgumentParser(description="بک‌تست و گزارش استراتژی DTM")
    p.add_argument("--days", type=int, default=DAYS_DEFAULT)
    p.add_argument("--symbols", nargs="*", default=SYMBOLS)
    p.add_argument("--tfs", nargs="*", default=TIMEFRAMES)
    p.add_argument("--mode", choices=["full", "breakdown", "both"], default="full")
    p.add_argument("--force", action="store_true", help="نادیده‌گرفتن قفل روزانه")
    p.add_argument("--resend", action="store_true", help="ارسال مجدد از نتایج ذخیره‌شده")
    p.add_argument("--no-send", action="store_true", help="فقط چاپ/ذخیره، بدون تلگرام")
    return p.parse_args()


def main():
    args = parse_args()
    symbols = [s.upper() for s in args.symbols]
    tfs = [str(t) for t in args.tfs]

    try:
        if args.resend:
            trades, meta = load_results()
            if not trades:
                logger.error("نتایج ذخیره‌شده‌ای پیدا نشد")
                return 1
            logger.info(f"Resend از فایل ذخیره‌شده ({len(trades)} معامله)...")
            send_reports(trades, meta, args.mode, do_send=not args.no_send)
            return 0

        # قفل روزانه: گزارشِ هر mode روزی فقط یک‌بار ارسال می‌شود
        if (not args.force) and (not args.no_send) and marker_already_sent(args.mode):
            logger.info(f"گزارش '{args.mode}' امروز ({today_str()}) قبلاً ارسال شده. برای اجرای مجدد: --force")
            return 0

        now_ir = datetime.now(UTC_TZ).astimezone(IRAN_TZ)
        today_mid = now_ir.replace(hour=0, minute=0, second=0, microsecond=0)
        start_ir = today_mid - timedelta(days=max(1, args.days) - 1)
        start_ms = int(start_ir.timestamp() * 1000)
        end_ms = int(time.time() * 1000)
        meta = {
            "days": args.days, "symbols": symbols, "tfs": tfs,
            "start_date": start_ir.strftime("%Y-%m-%d"), "end_date": now_ir.strftime("%Y-%m-%d"),
            "generated_at": now_ir_str(), "engine": ENGINE_NAME,
            "combos": [], "errors": [],
        }

        est_bars = sum(int(args.days) * 1440 // int(tf) for tf in tfs) * len(symbols)
        intro = (f"🚀 شروع بک‌تست استراتژی DTM\n"
                 f"🗓 {meta['start_date']} تا {meta['end_date']} | 📡 {len(symbols)} ارز × {len(tfs)} تایم‌فریم\n"
                 f"📈 تخمین کندل‌ها: ~{est_bars:,}\n"
                 f"⏳ ممکن است چند دقیقه طول بکشد...")
        logger.info(intro.replace("\n", " | "))
        if not args.no_send:
            tg_send(intro)

        all_trades = []
        total = len(tfs) * len(symbols)
        done = 0
        for tf in tfs:
            for sym in symbols:
                done += 1
                t0 = time.time()
                try:
                    trades, n_bars, raw_hits = backtest_combo(sym, tf, start_ms, end_ms)
                    all_trades.extend(trades)
                    meta["combos"].append({
                        "symbol": sym, "tf": tf, "bars": n_bars,
                        "raw_hits": raw_hits, "signals": len(trades),
                    })
                    msg = (f"⏳ [{done}/{total}] {sym} {tf}m ✓ | "
                           f"کندل: {n_bars:,} | سیگنال: {len(trades)} | {time.time() - t0:.0f}s")
                except Exception as e:
                    meta["errors"].append(f"{sym} {tf}m: {e}")
                    logger.error(f"[COMBO] {sym} {tf}m failed: {e}\n{traceback.format_exc()}")
                    msg = f"⚠️ [{done}/{total}] {sym} {tf}m ✗ | {e}"
                logger.info(msg)
                if not args.no_send:
                    tg_send(msg)

        save_results(all_trades, meta)
        sent_ok = send_reports(all_trades, meta, args.mode, do_send=not args.no_send)
        if sent_ok and not args.no_send:
            marker_set(args.mode)
            tg_send(f"✅ بک‌تست تمام شد — {len(all_trades)} سیگنال پردازش شد.")
        return 0

    except KeyboardInterrupt:
        tg_send("⏹ بک‌تست توسط کاربر متوقف شد.")
        return 130
    except Exception as e:
        err = f"❌ خطای کلی بک‌تست: {type(e).__name__}: {e}\n{traceback.format_exc()[:1500]}"
        logger.error(err)
        tg_send(err)
        return 1


if __name__ == "__main__":
    sys.exit(main())

