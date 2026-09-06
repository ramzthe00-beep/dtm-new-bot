# -*- coding: utf-8 -*-
"""
backtest_report.py — نسخه نهایی v4 (HYBRID = پاریتی کامل با لایو)
=================================================================
منطق سیگنال = عیناً مسیر لایو:
  bot.py → fetch 500 کندل (شامل کندل در حال شکل‌گیری) → calculate_signals
  → حذف کندل ناقص → ScriptRunner روی 499 کندل → دیکشنری آخرین کندل = سیگنال
پس بک‌تست: پاس سریع برای کاندیدها → تأیید هر کاندید با پنجره سرد 499 کندلی.
سیگنالی بدون تأیید پنجره ثبت نمی‌شود ⇒ دقیقاً همان سیگنال‌هایی که لایو می‌گرفت.

اجرا:
    python backtest_report.py                  # 60 روز، کامل
    python backtest_report.py --mode both      # + تفکیک هر ارز/تایم‌فریم
    python backtest_report.py --tfs 5          # تست سریع
    python backtest_report.py --force          # نادیده‌گرفتن قفل روزانه
"""

import os, sys, json, math, time, argparse, logging, traceback
from pathlib import Path
from datetime import datetime, timedelta, timezone

import requests
import pandas as pd

# ============================ ثابت‌ها (کپی bot.py + strategy_wrapper) ============================
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
# tick از bot.py — منبع رسمی سفارش‌ها (PUMPUSDT = 0.000001)
TICK_SIZES = {"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01, "BNBUSDT": 0.01, "PUMPUSDT": 0.000001}
HISTORY_BARS = 500          # مثل bot.py
LIVE_WINDOW_BARS = HISTORY_BARS - 1   # 🔑 لایو بعد از حذف کندل ناقص، 499 کندل واقعی دارد
                                     # (مدرک: لاگ زنده Total results: 499 و bars=498)
BASE_CAPITAL = 2.0
DAYS_DEFAULT = 60
WARMUP_DAYS = 3
BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]
KLINE_LIMIT = 1000
REQUEST_SLEEP = 0.15
GENERIC_FALLBACK_TICK = 0.0001

STRATEGY_INPUTS = {
    "pivotMode": "سریع (5/3)", "rsiLen": 14, "macdFast": 12, "macdSlow": 26, "macdSig": 9,
    "trendLookback": 20, "trendSlopeMinPct": 0.05, "minConfirmations": "۳ تعییدیه (حداقل مجاز)",
    "enableHidden": True, "fibUse618": True, "fibUse786": True, "fibTolerancePct": 0.5,
    "fibTrendSearchBars": 100, "shadowToBodyRatio": 2.0, "maxOppositeShadowPct": 20.0,
    "minCandleATRRatio": 0.3, "bigCandleAvgLen": 14, "bigCandleMultiplier": 1.5,
}
SCORE_KEYS = {"CD-": "score_classic_bearish", "CD+": "score_classic_bullish",
              "HD+": "score_hidden_bullish", "HD-": "score_hidden_bearish"}
WD_FA = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
W = "━━━━━━━━━━━━━━━━━━━━"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BACKTEST")

def _tick_to_pricescale(tick):
    try:
        return max(1, round(1.0 / float(tick)))
    except Exception:
        return 100

SYMBOL_TICK_INFO = {s: {"mintick": t, "pricescale": _tick_to_pricescale(t),
                        "basecurrency": s.replace("USDT", "")} for s, t in TICK_SIZES.items()}

# ============================ ابزارها ============================
def _f(x):
    try:
        if x is None: return None
        v = float(x)
        return None if (math.isnan(v) or math.isinf(v)) else v
    except (TypeError, ValueError):
        return None

def _ms_to_iran(ms):
    try: return datetime.fromtimestamp(int(ms) / 1000.0, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception: return None

def now_iran_str(): return datetime.now(UTC_TZ).astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")
def today_str(): return datetime.now(UTC_TZ).astimezone(IRAN_TZ).strftime("%Y-%m-%d")

def tg_send(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        return requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=30).ok
    except Exception as e:
        logger.error(f"[TG] {e}"); return False

def tg_send_long(text):
    text = str(text)
    ok = True
    for part in ([text[i:i + 3900] for i in range(0, len(text), 3900)] or [text]):
        sent = False
        for attempt in range(3):
            if tg_send(part): sent = True; break
            time.sleep(1 + attempt)
        ok = ok and sent
        time.sleep(0.4)
    return ok

# ============================ موتور استراتژی ============================
try:
    import strategy_wrapper as _sw
    try: _sw._send_telegram = lambda text: True
    except Exception: pass
    _compute_stop_target = _sw._compute_stop_target
    ENGINE_NAME = "strategy_wrapper (import شد)"
except Exception as e:
    logger.warning(f"[ENGINE] wrapper import نشد → fallback محلی: {e}")
    ENGINE_NAME = "fallback محلی"; _sw = None

try:
    from pynecore.core.ohlcv import OHLCV
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    from pynecore.core.script_runner import ScriptRunner
except Exception as e:
    logger.error(f"[FATAL] pynecore: {e}")
    tg_send(f"❌ backtest_report: pynecore نصب نیست:\n{e}"); sys.exit(1)

_LOCAL_SLTP_COPIED = False
if _sw is None:
    _LOCAL_SLTP_COPIED = True
    def _compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=2):
        def _v(x): return x is not None and not (isinstance(x, float) and math.isnan(x))
        entry = last_values.get("entry")
        if not _v(entry): return None, None, None, None
        b = buffer_ticks * mintick
        if signal == "LONG":
            l1, l2 = last_values.get("previous_pivot_low_price"), last_values.get("pivot_low_price")
            b1, b2 = last_values.get("previous_pivot_low_index"), last_values.get("pivot_low_index")
            if not (_v(l1) and _v(l2) and _v(b1) and _v(b2)): return None, None, None, None
            stop = min(l1, l2) - b
            lo, hi = sorted((int(b1), int(b2))); lo, hi = max(lo, 0), min(hi, len(candles) - 1)
            if hi < lo: return None, None, None, None
            mid = max(c.high for c in candles[lo:hi + 1]); risk = entry - stop
            if risk <= 0: return None, None, None, None
            rr = (mid - entry) / risk
            return stop, (mid if rr >= 2 else entry + 2 * risk), max(rr, 2.0), mid
        if signal == "SHORT":
            h1, h2 = last_values.get("previous_pivot_high_price"), last_values.get("pivot_high_price")
            b1, b2 = last_values.get("previous_pivot_high_index"), last_values.get("pivot_high_index")
            if not (_v(h1) and _v(h2) and _v(b1) and _v(b2)): return None, None, None, None
            stop = max(h1, h2) + b
            lo, hi = sorted((int(b1), int(b2))); lo, hi = max(lo, 0), min(hi, len(candles) - 1)
            if hi < lo: return None, None, None, None
            mid = min(c.low for c in candles[lo:hi + 1]); risk = stop - entry
            if risk <= 0: return None, None, None, None
            rr = (entry - mid) / risk
            return stop, (mid if rr >= 2 else entry - 2 * risk), max(rr, 2.0), mid
        return None, None, None, None

try:
    from trade_ledger import _hypothetical_pnl_usd as pnl_fn, BASE_CAPITAL as _BC
    BASE_CAPITAL = float(_BC)
except Exception:
    def pnl_fn(direction, entry, initial_stop, exit_price, leverage):
        try:
            if not entry or not initial_stop or entry <= 0: return None, None
            stop_pct = abs(entry - initial_stop) / entry
            if stop_pct <= 0: return None, None
            move_pct = (exit_price - entry) / entry if direction == "LONG" else (entry - exit_price) / entry
            lev = leverage if (leverage and leverage > 0) else 50
            old_lev = 1.0 / stop_pct
            capital = (old_lev / lev) * BASE_CAPITAL if old_lev > lev else BASE_CAPITAL
            return round(capital * lev * move_pct, 4), round(move_pct / stop_pct, 4)
        except Exception:
            return None, None

def _build_syminfo(symbol, timeframe):
    tick = SYMBOL_TICK_INFO.get(symbol, {"mintick": GENERIC_FALLBACK_TICK,
        "pricescale": _tick_to_pricescale(GENERIC_FALLBACK_TICK), "basecurrency": symbol.replace("USDT", "")})
    return SymInfo(prefix="", description=f"{symbol} {timeframe}m", ticker=symbol, currency="USDT",
        basecurrency=tick["basecurrency"], period=str(timeframe), type="crypto", volumetype="base",
        mintick=tick["mintick"], pricescale=tick["pricescale"], minmove=1, pointvalue=1.0, mincontract=0.0,
        opening_hours=[SymInfoInterval(day=0, start=datetime.min.time(), end=datetime.max.time())],
        session_starts=[SymInfoSession(day=0, time=datetime.min.time())],
        session_ends=[SymInfoSession(day=0, time=datetime.max.time())], timezone="UTC")

def buffer_ticks_for(symbol):
    if symbol in ("BNBUSDT", "ETHUSDT"): return 9
    if symbol in ("LTCUSDT", "DOGEUSDT"): return 3
    if symbol == "PUMPUSDT": return 1
    return 5

def compute_rf_pct(signal, entry, stop, structural_level):
    entry, stop, struct = _f(entry), _f(stop), _f(structural_level)
    if struct is None or stop is None or entry is None or entry <= 0: return None
    risk_pct = abs(entry - stop) / entry
    return max((struct - entry) / entry, risk_pct) if signal == "LONG" else -max((entry - struct) / entry, risk_pct)

def signal_type_of(lv):
    try:
        if lv.get("final_classic_bearish"): return "CD-"
        if lv.get("final_classic_bullish"): return "CD+"
        if lv.get("final_hidden_bullish"): return "HD+"
        if lv.get("final_hidden_bearish"): return "HD-"
    except Exception: pass
    return None

def _score_of(lv, st):
    if not st: return 0
    v = _f(lv.get(SCORE_KEYS.get(st, "")))
    return int(max(0, min(5, round(v)))) if v is not None else 0

# ============================ دیتا از Binance ============================
def fetch_klines(symbol, interval_min, start_ms, end_ms):
    interval = f"{int(interval_min)}m" if int(interval_min) < 60 else \
        {60: "1h", 120: "2h", 240: "4h", 1440: "1d"}.get(int(interval_min))
    if not interval:
        raise ValueError(f"تایم‌فریم {interval_min} پشتیبانی نمی‌شود")
    tf_ms = int(interval_min) * 60_000
    rows, cursor, session = {}, start_ms, requests.Session()
    while cursor <= end_ms:
        chunk = None
        for attempt in range(4):
            base = BINANCE_BASES[attempt % 2]
            try:
                url = (f"{base}/api/v3/klines?symbol={symbol}&interval={interval}"
                       f"&startTime={cursor}&endTime={end_ms}&limit={KLINE_LIMIT}")
                r = session.get(url, timeout=20)
                if r.status_code in (418, 429): time.sleep(2 ** attempt + 1); continue
                r.raise_for_status(); chunk = r.json(); break
            except Exception:
                time.sleep(0.8 * (attempt + 1))
        if chunk is None: raise RuntimeError(f"Binance unreachable {symbol} {interval} @ {cursor}")
        if not chunk: break
        for row in chunk:
            try: rows[int(row[0])] = row
            except Exception: pass
        nc = int(chunk[-1][0]) + tf_ms
        cursor = nc if nc > cursor else cursor + tf_ms
        if len(chunk) < KLINE_LIMIT: break
        time.sleep(REQUEST_SLEEP)
    if not rows: return pd.DataFrame()
    rs = [rows[k] for k in sorted(rows)]
    df = pd.DataFrame({
        "open": pd.to_numeric([r[1] for r in rs], errors="coerce"),
        "high": pd.to_numeric([r[2] for r in rs], errors="coerce"),
        "low": pd.to_numeric([r[3] for r in rs], errors="coerce"),
        "close": pd.to_numeric([r[4] for r in rs], errors="coerce"),
        "volume": pd.to_numeric([r[5] for r in rs], errors="coerce"),
    }, index=pd.to_datetime([r[0] / 1000.0 for r in rs], unit="s", utc=True))
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")].dropna(subset=["open", "high", "low", "close"])
    now_ms = int(time.time() * 1000)
    if rs and int(rs[-1][0]) + tf_ms > now_ms:   # حذف کندل ناقص انتهایی
        df = df.iloc[:-1]
    return df

def df_to_candles(df):
    return [OHLCV(timestamp=int(idx.timestamp() * 1000), open=float(r["open"]), high=float(r["high"]),
                  low=float(r["low"]), close=float(r["close"]), volume=float(r.get("volume", 0) or 0),
                  is_closed=True) for idx, r in df.iterrows()]

def _candles_to_tuples(candles):
    return [(c.timestamp, c.open, c.high, c.low, c.close, c.volume) for c in candles]

def _tuples_to_candles(tuples):
    return [OHLCV(timestamp=t[0], open=t[1], high=t[2], low=t[3], close=t[4], volume=t[5], is_closed=True)
            for t in tuples]

# ============================ موتور HYBRID ============================
def run_strategy_pass_fast(candles, symbol, timeframe):
    """پاس سریع روی کل تاریخچه — فقط برای یافتن «کاندیدها»."""
    runner = ScriptRunner(STRATEGY_PATH, iter(candles), _build_syminfo(symbol, timeframe),
                          last_bar_index=len(candles) - 1, inputs=dict(STRATEGY_INPUTS))
    hits, stats = [], {"bars": 0, "dicts": 0, "raw": 0, "errors": 0}
    logging.disable(logging.INFO)
    try:
        for i, result in enumerate(runner.run_iter()):
            stats["bars"] += 1
            try:
                if result is None or len(result) < 2: continue
                raw = result[1]
                if not (isinstance(raw, dict) and len(raw) > 0): continue
                lv = dict(raw)                       # 🔴 کپی فوری (باگ رفرنس PyneCore)
                stats["dicts"] += 1
                sig = lv.get("signal")
                if sig not in ("LONG", "SHORT"): continue
                entry = _f(lv.get("entry"))
                if entry is None or entry <= 0: continue
                stats["raw"] += 1
                hits.append((i, lv, sig, entry))
            except Exception:
                stats["errors"] += 1
    finally:
        logging.disable(logging.NOTSET)
    return hits, stats

def _verify_window_signal(candle_tuples, symbol, timeframe, i):
    """تأیید کاندید با پنجره سرد LIVE_WINDOW_BARS=499 کندلی — عیناً مسیر لایو."""
    lo = max(0, i - (LIVE_WINDOW_BARS - 1))
    window = _tuples_to_candles(candle_tuples[lo:i + 1])
    if len(window) < 50:
        return None, "too_short"
    try:
        runner = ScriptRunner(STRATEGY_PATH, iter(window), _build_syminfo(symbol, timeframe),
                              last_bar_index=len(window) - 1, inputs=dict(STRATEGY_INPUTS))
    except Exception as e:
        return None, f"runner_init:{type(e).__name__}"
    last_values = None
    logging.disable(logging.INFO)
    try:
        for result in runner.run_iter():
            if result is None or len(result) < 2: continue
            raw = result[1]
            if isinstance(raw, dict) and len(raw) > 0:
                last_values = dict(raw)              # 🔴 کپی فوری
    except Exception as e:
        return None, f"run_iter:{type(e).__name__}"
    finally:
        logging.disable(logging.NOTSET)
    if not last_values: return None, "empty_last_dict"
    sig = last_values.get("signal")
    if sig not in ("LONG", "SHORT"): return None, "no_signal_in_window"
    entry = _f(last_values.get("entry"))
    if entry is None or entry <= 0: return None, "bad_entry"
    return (i, last_values, sig, entry), None

def run_strategy_hybrid(candles, symbol, timeframe, idx_from, idx_to, progress_cb=None):
    candidates, fast_stats = run_strategy_pass_fast(candles, symbol, timeframe)
    cand = [h for h in candidates if idx_from <= h[0] < idx_to]
    tuples = _candles_to_tuples(candles)
    verified, rejects = [], {}
    for k, (i, _lv, _sig, _e) in enumerate(cand):
        hit, why = _verify_window_signal(tuples, symbol, timeframe, i)
        if hit is not None:
            verified.append(hit)
        else:
            key = why.split(":")[0]
            rejects[key] = rejects.get(key, 0) + 1
        if progress_cb and (k + 1) % 50 == 0:
            progress_cb(k + 1, len(cand))
    stats = {"bars": len(candles), "candidates": len(cand), "raw": len(verified),
             "rejected": rejects, "errors": sum(rejects.get(x, 0) for x in ("runner_init", "run_iter")),
             "fast_raw": fast_stats.get("raw", 0)}
    return verified, stats

# ============================ شبیه‌سازی معامله (عیناً trade_ledger) ============================
def simulate_trade(tr, candles, n):
    try:
        entry, initial_stop = tr["entry"], tr["stop"]
        target, direction, rf = tr["target"], tr["direction"], tr.get("rf_pct")
        stop, risk_free = initial_stop, False
        for j in range(tr["entry_idx"] + 1, n):
            c = candles[j]
            high, low, ts = float(c.high), float(c.low), int(c.timestamp)
            if not risk_free and rf is not None:
                crossed = high >= entry * (1 + abs(rf)) if direction == "LONG" else low <= entry * (1 - abs(rf))
                if crossed:
                    risk_free, stop = True, entry      # سربه‌سر (تقریب trade_ledger)
            if direction == "LONG":
                hit_stop, hit_target = low <= stop, (target is not None and high >= target)
            else:
                hit_stop, hit_target = high >= stop, (target is not None and low <= target)
            if hit_stop:
                tr["status"] = "WIN" if risk_free else "LOSS"
                tr["exit_reason"] = "RISK_FREE_STOP" if risk_free else "STOP_LOSS"
                tr["exit_price"], tr["exit_time_ms"] = stop, ts
                break
            if hit_target:
                tr["status"], tr["exit_reason"], tr["exit_price"], tr["exit_time_ms"] = "WIN", "TARGET", target, ts
                break
        tr["risk_free"] = risk_free
        if tr["status"] != "OPEN":
            pnl, r = pnl_fn(direction, entry, initial_stop, tr["exit_price"], tr["leverage"])
            tr["pnl_usd"], tr["pnl_r"] = pnl, r
    except Exception as e:
        logger.warning(f"[SIM] {tr.get('symbol')}: {e}")
        tr["status"] = "OPEN"

# ============================ بک‌تست یک ترکیب ============================
def backtest_combo(symbol, timeframe, start_ms, end_ms, engine="hybrid", progress_cb=None):
    tf_min = int(timeframe)
    warmup_ms = LIVE_WINDOW_BARS * tf_min * 60_000 + WARMUP_DAYS * 86_400_000
    df = fetch_klines(symbol, tf_min, start_ms - warmup_ms, end_ms)
    if df is None or df.empty: raise RuntimeError("دیتای خالی از Binance")
    if len(df) < LIVE_WINDOW_BARS + 50: raise RuntimeError(f"کندل کافی نیست: {len(df)}")
    candles = df_to_candles(df); n = len(candles)
    mintick = SYMBOL_TICK_INFO.get(symbol, {"mintick": GENERIC_FALLBACK_TICK})["mintick"]
    idx_from = next((k for k, c in enumerate(candles) if int(c.timestamp) >= start_ms), n)

    if engine == "fast":
        raw_hits, diag = run_strategy_pass_fast(candles, symbol, timeframe)
    else:
        raw_hits, diag = run_strategy_hybrid(candles, symbol, timeframe, idx_from, n, progress_cb=progress_cb)

    seen, trades = set(), []
    drop = {"out_of_range": 0, "bad_sltp": 0, "dup": 0}
    for (i, lv, sig, entry) in raw_hits:
        try:
            ts = int(candles[i].timestamp)
            if ts < start_ms or ts > end_ms:
                drop["out_of_range"] += 1; continue
            key = (symbol, str(timeframe), ts, sig)
            if key in seen:
                drop["dup"] += 1; continue
            seen.add(key)
            try:
                stop, target, rr, struct = _compute_stop_target(
                    candles, sig, lv, mintick, buffer_ticks=buffer_ticks_for(symbol))
            except Exception as e:
                logger.warning(f"[SL/TP] {symbol} {timeframe}m bar {i}: {e}")
                stop = None
            if stop is None or target is None or abs(entry - stop) <= 0:
                drop["bad_sltp"] += 1; continue
            st = signal_type_of(lv)
            tr = {"symbol": symbol, "timeframe": str(timeframe), "direction": sig,
                  "entry": float(entry), "stop": float(stop), "target": float(target),
                  "entry_time_ms": ts, "entry_idx": int(i),
                  "leverage": LEVERAGE_MAP.get(symbol, 50), "signal_type": st or "?",
                  "score": _score_of(lv, st), "rf_pct": compute_rf_pct(sig, entry, stop, struct),
                  "rr_planned": _f(rr), "status": "OPEN", "exit_reason": None, "exit_price": None,
                  "exit_time_ms": None, "pnl_usd": None, "pnl_r": None, "risk_free": False}
            simulate_trade(tr, candles, n)
            trades.append(tr)
        except Exception as e:
            logger.warning(f"[BT] {symbol} {timeframe}m bar {i}: {e}")
    diag.update(drop); diag["trades"] = len(trades); diag["engine"] = engine
    return trades, n, diag

# ============================ آمار و گزارش ============================
def stats_of(trades):
    s = {"total": len(trades)}
    wins = [t for t in trades if t.get("status") == "WIN"]
    losses = [t for t in trades if t.get("status") == "LOSS"]
    closed = wins + losses
    s.update(wins=len(wins), losses=len(losses),
             opens=sum(1 for t in trades if t.get("status") == "OPEN"), closed=len(closed))
    s["rf_wins"] = sum(1 for t in wins if t.get("exit_reason") == "RISK_FREE_STOP")
    s["tp_wins"] = sum(1 for t in wins if t.get("exit_reason") == "TARGET")
    s["winrate"] = (len(wins) / len(closed) * 100) if closed else 0.0
    pnls = [t["pnl_usd"] for t in closed if t.get("pnl_usd") is not None]
    s["pnl_total"] = sum(pnls)
    gw, gl = sum(p for p in pnls if p > 0), sum(p for p in pnls if p < 0)
    s["pf"] = (gw / abs(gl)) if gl < 0 else (float("inf") if gw > 0 else 0.0)
    s["avg_win"] = gw / len(wins) if wins else 0.0
    s["avg_loss"] = gl / len(losses) if losses else 0.0
    rs = [t["pnl_r"] for t in closed if t.get("pnl_r") is not None]
    s["avg_r"] = sum(rs) / len(rs) if rs else 0.0
    rrs = [t["rr_planned"] for t in trades if t.get("rr_planned")]
    s["avg_rr"] = sum(rrs) / len(rrs) if rrs else 0.0
    seq = sorted([t for t in closed if t.get("pnl_usd") is not None],
                 key=lambda t: t.get("exit_time_ms") or t["entry_time_ms"])
    streak = best = 0; cum = peak = 0.0; dd = 0.0
    for t in seq:
        streak = streak + 1 if t["status"] == "LOSS" else 0
        best = max(best, streak)
        cum += t["pnl_usd"]; peak = max(peak, cum); dd = min(dd, cum - peak)
    s["max_consec_loss"], s["max_dd"] = best, dd
    durs = [(t["exit_time_ms"] - t["entry_time_ms"]) / 60000.0 for t in closed if t.get("exit_time_ms")]
    s["avg_hold_min"] = sum(durs) / len(durs) if durs else 0.0
    return s

def fmt_money(x): return f"{x:+.2f}$" if x is not None else "—"
def fmt_pf(pf): return "∞" if pf == float("inf") else f"{pf:.2f}"
def group_dict(items, keyfn):
    d = {}
    for it in items: d.setdefault(keyfn(it), []).append(it)
    return d

def fmt_trade_line(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    ts = dt.strftime("%m-%d %H:%M") if dt else "?"
    emoji = {"WIN": "✅", "LOSS": "❌", "OPEN": "⏳"}.get(t.get("status"), "•")
    if t.get("exit_reason") == "RISK_FREE_STOP": emoji = "🛡️"
    r = t.get("pnl_r")
    return (f"  {emoji} {ts} | {t['timeframe']}m | {t.get('signal_type','?')} S{t.get('score',0)} | "
            f"{f'{r:+.2f}R' if r is not None else '—'} {fmt_money(t.get('pnl_usd'))}")

def _section(L, title, trades, keyfn):
    g = group_dict(trades, keyfn)
    if not g: return
    L.append(W); L.append(title)
    for k in sorted(g.keys(), key=str):
        stg = stats_of(g[k])
        L.append(f"  • {k}: {stg['total']} سیگنال | ✅{stg['wins']} ❌{stg['losses']} ⏳{stg['opens']} "
                 f"| نرخ {stg['winrate']:.0f}٪ | {fmt_money(stg['pnl_total'])}")

def hour_bucket(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    return f"{(dt.hour // 4) * 4:02d}-{(dt.hour // 4) * 4 + 3:02d}" if dt else "?"

def weekday_fa(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    return WD_FA[dt.weekday()] if dt else "?"

def build_insights(trades):
    L = ["🧠 بینش‌ها:"]
    closed = [t for t in trades if t.get("status") in ("WIN", "LOSS")]
    if len(closed) < 10:
        L.append("  • معاملات بسته‌شده کم است؛ بینش معنادار نیست."); return L
    base = stats_of(trades)
    L.append(f"  • نرخ برد پایه: {base['winrate']:.1f}٪ | PF: {fmt_pf(base['pf'])} | سربه‌سر ≈ {100/3:.0f}٪")
    combos = [(k, stats_of(v)) for k, v in group_dict(trades, lambda t: f"{t['symbol']} {t['timeframe']}m").items()
              if stats_of(v)["closed"] >= 5]
    if combos:
        L.append(f"  • بهترین ترکیب: {max(combos, key=lambda kv: kv[1]['pnl_total'])[0]}")
        L.append(f"  • ضعیف‌ترین: {min(combos, key=lambda kv: kv[1]['pnl_total'])[0]}")
    types = [(k, stats_of(v)) for k, v in group_dict(trades, lambda t: t.get("signal_type", "?")).items()
             if stats_of(v)["closed"] >= 5]
    if types:
        bt = max(types, key=lambda kv: kv[1]["pnl_total"])
        L.append(f"  • بهترین نوع سیگنال: {bt[0]} (نرخ {bt[1]['winrate']:.0f}٪)")
    for s in (4, 3):
        sub = [t for t in closed if (t.get("score") or 0) >= s]
        if len(sub) >= 10:
            stg = stats_of(sub)
            L.append(f"  • فیلتر امتیاز ≥ {s}: نرخ {stg['winrate']:.1f}٪ ({better_sym(stg['winrate'], base['winrate'])} از پایه)")
            break
    buckets = [(k, stats_of(v)) for k, v in group_dict(trades, hour_bucket).items() if stats_of(v)["closed"] >= 8]
    if len(buckets) >= 2:
        L.append(f"  • بهترین بازه ساعتی (تهران): {max(buckets, key=lambda kv: kv[1]['pnl_total'])[0]}")
    return L

def better_sym(a, b): return "بهتر" if a > b else "بدتر"

def build_overall_report(trades, meta):
    st = stats_of(trades)
    L = ["📊 گزارش کامل بک‌تست استراتژی DTM", W,
         f"🗓 بازه: {meta['start_date']} تا {meta['end_date']} ({meta['days']} روز — تهران)",
         f"📡 Binance Spot | تایم‌فریم: {', '.join(t + 'm' for t in meta['tfs'])}",
         f"🕐 تولید: {meta['generated_at']} | ⚙️ موتور: {meta.get('engine_mode','hybrid')} | پنجره لایو: {LIVE_WINDOW_BARS} کندل",
         W,
         f"📈 کل سیگنال‌های تأییدشده (لایو-معادل): {st['total']}",
         f"✅ برنده: {st['wins']} (🎯 {st['tp_wins']} | 🛡️ {st['rf_wins']})  ❌ باخت: {st['losses']}  ⏳ باز: {st['opens']}",
         f"🏆 نرخ برد: {st['winrate']:.1f}٪ (از {st['closed']} بسته‌شده)",
         f"💰 سود/زیان فرضی: {fmt_money(st['pnl_total'])} (سرمایه پایه {BASE_CAPITAL:.0f}$ — فرمول trade_ledger)",
         f"⚖️ PF: {fmt_pf(st['pf'])} | 📊 میانگین R: {st['avg_r']:.2f} | 🎯 RR برنامه: 1:{st['avg_rr']:.2f}",
         f"⏱ میانگین طول: {st['avg_hold_min']:.0f} دقیقه | 🔥 حداکثر باخت متوالی: {st['max_consec_loss']} | 📉 افت: {fmt_money(st['max_dd'])}"]
    _section(L, "💼 به تفکیک ارز:", trades, lambda t: t["symbol"])
    _section(L, "🕐 به تفکیک تایم‌فریم:", trades, lambda t: f"{t['timeframe']}m")
    _section(L, "🔀 به تفکیک نوع سیگنال:", trades, lambda t: t.get("signal_type", "?"))
    _section(L, "⭐ به تفکیک امتیاز:", trades, lambda t: f"امتیاز {t.get('score', 0)}")
    cs = sorted([t for t in trades if t.get("pnl_usd") is not None], key=lambda t: t["pnl_usd"])
    if cs:
        L.append(W); L.append("🏅 ۵ معامله برتر:")
        L += [fmt_trade_line(t) for t in cs[-5:][::-1]]
        L.append("💥 ۵ معامله ضعیف:")
        L += [fmt_trade_line(t) for t in cs[:5]]
    L.append(W); L += build_insights(trades)
    if meta.get("combos"):
        L.append(W); L.append("🧮 جزئیات اجرا (پاریتی):")
        for c in meta["combos"]:
            rej = c.get("rejected", {})
            rej_s = ", ".join(f"{k}:{v}" for k, v in rej.items()) if rej else "—"
            L.append(f"  • {c['symbol']} {c['tf']}m | کندل: {c['bars']:,} | کاندید: {c.get('candidates', 0)} "
                     f"| تأیید: {c['signals']} | رد: {rej_s}")
    if meta.get("errors"):
        L.append(W); L.append("⚠️ خطاها:")
        L += [f"  • {e}" for e in meta["errors"][:20]]
    L.append(W)
    L.append("⚠️ فرضی/بدون کارمزد و اسلیپیج — سیگنال‌ها = دقیقاً مسیر لایو (پنجره ۴۹۹ کندلی سرد).")
    return "\n".join(L)

def build_combo_report(sym, tf, trades):
    st = stats_of(trades)
    L = [f"📋 {sym} — {tf} دقیقه", W]
    if st["total"] == 0:
        L.append("در این بازه هیچ سیگنال تأییدشده‌ای نبود."); return "\n".join(L)
    L += [f"📈 سیگنال‌ها: {st['total']} | ✅{st['wins']} (🎯{st['tp_wins']} 🛡️{st['rf_wins']}) | ❌{st['losses']} | ⏳{st['opens']}",
          f"🏆 نرخ برد: {st['winrate']:.1f}٪ | 💰 {fmt_money(st['pnl_total'])} | PF: {fmt_pf(st['pf'])} | 📊 R: {st['avg_r']:.2f}",
          W]
    items = sorted(trades, key=lambda t: t["entry_time_ms"])
    if len(items) <= 25:
        L.append("🧾 همه معاملات:")
        L += [fmt_trade_line(t) for t in items]
    else:
        cs = sorted([t for t in items if t.get("pnl_usd") is not None], key=lambda t: t["pnl_usd"])
        L.append("🏅 ۵ برتر:"); L += [fmt_trade_line(t) for t in cs[-5:][::-1]]
        L.append("💥 ۵ ضعیف:"); L += [fmt_trade_line(t) for t in cs[:5]]
        L.append(f"  … و {len(items) - 10} معامله دیگر")
    return "\n".join(L)

# ============================ ذخیره / قفل / ارسال ============================
def save_results(trades, meta):
    try:
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "trades": trades}, f, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"[SAVE] {e}"); return False

def load_results():
    try:
        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d.get("trades", []), d.get("meta", {})
    except Exception:
        return [], {}

def marker_already_sent(mode):
    try: return json.loads(MARKER_PATH.read_text(encoding="utf-8")).get(mode) == today_str()
    except Exception: return False

def marker_set(mode):
    try:
        data = {}
        if MARKER_PATH.exists(): data = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
        data[mode] = today_str()
        MARKER_PATH.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.error(f"[MARKER] {e}")

def save_report_backup(text):
    try:
        p = BASE_DIR / f"backtest_report_{datetime.now(UTC_TZ).strftime('%Y%m%d_%H%M')}.txt"
        p.write_text(text, encoding="utf-8")
    except Exception as e:
        logger.error(f"[BACKUP] {e}")

def send_reports(trades, meta, mode, do_send):
    texts = []
    if mode in ("full", "both"):
        texts.append(("📊 گزارش کامل", build_overall_report(trades, meta)))
    if mode in ("breakdown", "both"):
        groups = group_dict(trades, lambda t: (t["symbol"], t["timeframe"]))
        order = {(s, tf) for s in meta.get("symbols", SYMBOLS) for tf in meta.get("tfs", TIMEFRAMES)}
        for (sym, tf) in sorted(set(groups) | order, key=lambda k: (k[0], int(k[1]))):
            texts.append((f"📋 {sym} {tf}m", build_combo_report(sym, tf, groups.get((sym, tf), []))))
    full = "\n\n".join(f"{h}\n{b}" for h, b in texts)
    save_report_backup(full)
    if not do_send:
        print(full); return True
    ok = True
    for h, b in texts:
        ok = tg_send_long(f"{h}\n\n{b}") and ok
        time.sleep(1)
    return ok

# ============================ main ============================
def parse_args():
    p = argparse.ArgumentParser(description="بک‌تست DTM — موتور Hybrid (پاریتی لایو)")
    p.add_argument("--days", type=int, default=DAYS_DEFAULT)
    p.add_argument("--symbols", nargs="*", default=SYMBOLS)
    p.add_argument("--tfs", nargs="*", default=TIMEFRAMES)
    p.add_argument("--mode", choices=["full", "breakdown", "both"], default="full")
    p.add_argument("--engine", choices=["hybrid", "fast"], default="hybrid")
    p.add_argument("--force", action="store_true")
    p.add_argument("--resend", action="store_true")
    p.add_argument("--no-send", action="store_true")
    return p.parse_args()

def main():
    args = parse_args()
    symbols = [s.upper() for s in args.symbols]
    tfs = [str(t) for t in args.tfs]
    try:
        if args.resend:
            trades, meta = load_results()
            if not trades:
                logger.error("نتایج ذخیره‌شده پیدا نشد"); return 1
            send_reports(trades, meta, args.mode, do_send=not args.no_send); return 0
        if (not args.force) and (not args.no_send) and marker_already_sent(args.mode):
            logger.info(f"گزارش '{args.mode}' امروز ارسال شده — با --force مجدد")
            return 0

        now_ir = datetime.now(UTC_TZ).astimezone(IRAN_TZ)
        start_ir = now_ir.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=max(1, args.days) - 1)
        start_ms = int(start_ir.timestamp() * 1000)
        end_ms = int(time.time() * 1000)
        meta = {"days": args.days, "symbols": symbols, "tfs": tfs,
                "start_date": start_ir.strftime("%Y-%m-%d"), "end_date": now_ir.strftime("%Y-%m-%d"),
                "generated_at": now_iran_str(), "engine_mode": args.engine,
                "live_window_bars": LIVE_WINDOW_BARS, "combos": [], "errors": []}

        intro = (f"🚀 شروع بک‌تست DTM (موتور {args.engine} — پاریتی لایو)\n"
                 f"🗓 {meta['start_date']} تا {meta['end_date']} | 📡 {len(symbols)} ارز × {len(tfs)} تایم‌فریم\n"
                 f"🔧 هر سیگنال با پنجره سرد {LIVE_WINDOW_BARS} کندلی تأیید می‌شود (عیناً مسیر لایو)")
        logger.info(intro.replace("\n", " | "))
        if not args.no_send: tg_send(intro)

        all_trades, total, done = [], len(tfs) * len(symbols), 0
        for tf in tfs:
            for sym in symbols:
                done += 1; t0 = time.time()
                try:
                    trades, n_bars, diag = backtest_combo(sym, tf, start_ms, end_ms, engine=args.engine)
                    elapsed = time.time() - t0
                    all_trades.extend(trades)
                    meta["combos"].append({"symbol": sym, "tf": tf, "bars": n_bars,
                                           "candidates": diag.get("candidates", 0), "signals": len(trades),
                                           "rejected": diag.get("rejected", {}),
                                           "out_of_range": diag.get("out_of_range", 0),
                                           "bad_sltp": diag.get("bad_sltp", 0)})
                    msg = (f"⏳ [{done}/{total}] {sym} {tf}m ✓ | کندل: {n_bars:,} | "
                           f"کاندید: {diag.get('candidates', 0)} | تأیید: {len(trades)} | {elapsed:.0f}s")
                except Exception as e:
                    meta["errors"].append(f"{sym} {tf}m: {e}")
                    logger.error(f"[COMBO] {sym} {tf}m: {e}\n{traceback.format_exc()}")
                    msg = f"⚠️ [{done}/{total}] {sym} {tf}m ✗ | {e}"
                logger.info(msg)
                if not args.no_send: tg_send(msg)

        # 🛡️ پایان صفرِ بی‌صدا: اگر همه چیز صفر بود، دلیلش را اعلام کن
        if not all_trades:
            warn = "⚠️ هیچ معامله‌ای تأیید نشد!\n" + "\n".join(
                f"• {c['symbol']} {c['tf']}m | کاندید: {c.get('candidates', 0)} | رد: {c.get('rejected', {})}"
                for c in meta["combos"][:10]) + \
                "\n→ runner_init/run_iter = خطای PyneCore | no_signal_in_window = پاریتی درست است و لایو هم نمی‌گرفت"
            logger.warning(warn)
            if not args.no_send: tg_send(warn)

        save_results(all_trades, meta)
        sent_ok = send_reports(all_trades, meta, args.mode, do_send=not args.no_send)
        if sent_ok and not args.no_send:
            marker_set(args.mode)
            tg_send(f"✅ بک‌تست تمام شد — {len(all_trades)} سیگنال لایو-معادل پردازش شد.")
        return 0
    except KeyboardInterrupt:
        tg_send("⏹ متوقف شد."); return 130
    except Exception as e:
        err = f"❌ خطای کلی بک‌تست: {type(e).__name__}: {e}\n{traceback.format_exc()[:1500]}"
        logger.error(err); tg_send(err); return 1

if __name__ == "__main__":
    sys.exit(main())

