"""
golden_portfolio.py — پرتفوی طلایی (۴ ترکیب تأییدشده)
- BNB 60m + SFP 15m Aati-Risky RR=10
- ETH 240m Aati-Risky RR=9
- BNB 240m Anni-FarEdge RR=9
- ETH 60m + SFP 15m Anni-FarEdge RR=6
"""
import os, json, time, math, logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from bisect import bisect_left, bisect_right
import numpy as np
import pandas as pd
import requests

from ct_wrapper import run_ct_strategy, CT_INPUTS_DEFAULT, closed_candles_only
from strategy_wrapper import SYMBOL_TICK_INFO

logger = logging.getLogger("GOLDEN_PORTFOLIO")

UTC = timezone.utc
IRAN = timezone(timedelta(hours=3, minutes=30))

STATE_FILE = Path.home() / "dtm-new-bot" / "golden_state.json"
LOG_DIR = Path.home() / "dtm-new-bot" / "golden_logs"
LOG_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════
# تعریف ۴ ترکیب پرتفوی طلایی
# ═══════════════════════════════════════════════════════════
GOLDEN_CONFIGS = [
    {
        "id": "G1",
        "symbol": "BNBUSDT",
        "ct_tf": "60",
        "mode": "Aati-Risky",
        "rr": 10,
        "sfp_tf": "15",
        "label": "BNB 60m + SFP 15m Aati-Risky RR=10",
        "expected_net": 79.59,
        "expected_n": 44,
        "expected_wr": 29.5,
    },
    {
        "id": "G2",
        "symbol": "ETHUSDT",
        "ct_tf": "240",
        "mode": "Aati-Risky",
        "rr": 9,
        "sfp_tf": None,
        "label": "ETH 240m Aati-Risky RR=9",
        "expected_net": 30.68,
        "expected_n": 35,
        "expected_wr": 22.9,
    },
    {
        "id": "G3",
        "symbol": "BNBUSDT",
        "ct_tf": "240",
        "mode": "Anni-FarEdge",
        "rr": 9,
        "sfp_tf": None,
        "label": "BNB 240m Anni-FarEdge RR=9",
        "expected_net": 27.28,
        "expected_n": 19,
        "expected_wr": 26.3,
    },
    {
        "id": "G4",
        "symbol": "ETHUSDT",
        "ct_tf": "60",
        "mode": "Anni-FarEdge",
        "rr": 6,
        "sfp_tf": "15",
        "label": "ETH 60m + SFP 15m Anni-FarEdge RR=6",
        "expected_net": 19.67,
        "expected_n": 18,
        "expected_wr": 33.3,
    },
]

# ═══════════════════════════════════════════════════════════
# State Management
# ═══════════════════════════════════════════════════════════
def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {"fired": {}, "trades": []}  # fired: {config_id: last_time_ms}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ═══════════════════════════════════════════════════════════
# Binance fetcher
# ═══════════════════════════════════════════════════════════
def fetch_klines(symbol, interval, limit=500):
    """دریافت کندل‌های جدید از Binance Spot"""
    url = "https://data-api.binance.vision/api/v3/klines"
    r = requests.get(url, params={
        "symbol": symbol, "interval": interval, "limit": limit
    }, timeout=15)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data, columns=[
        'ts','o','h','l','c','v','ct','q','n','a','b','i'
    ])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms', utc=True)
    for c in ['o','h','l','c','v']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.set_index('ts').sort_index()
    df = df.rename(columns={'o':'open','h':'high','l':'low','c':'close','v':'volume'})
    # فقط کندل‌های بسته‌شده
    return df.iloc[:-1]  # آخرین کندل ناقص است


# ═══════════════════════════════════════════════════════════
# SFP runner (mini)
# ═══════════════════════════════════════════════════════════
def run_sfp_events(o, h, l, c, left=5, right=1):
    N = len(c); events = []
    swing = {"H":[None,None],"L":[None,None]}
    for n in range(N):
        p = n - right
        if p < 0: continue
        ph = pl = None
        if p - left >= 0:
            lmax = max(h[p-left:p]); lmin = min(l[p-left:p])
            rmax = max(h[p+1:n+1]) if n > p else h[p]
            rmin = min(l[p+1:n+1]) if n > p else l[p]
            if h[p] >= lmax and h[p] > rmax: ph = h[p]
            if l[p] <= lmin and l[p] < rmin: pl = l[p]
        if ph is not None: swing["H"] = [p, ph]
        bx, sw = swing["H"]
        if sw is not None and h[n] > sw and o[n] < sw and c[n] < sw:
            events.append({"dir":"SHORT","bar":n})
        if pl is not None: swing["L"] = [p, pl]
        bx, sw = swing["L"]
        if sw is not None and l[n] < sw and o[n] > sw and c[n] > sw:
            events.append({"dir":"LONG","bar":n})
    return events


# ═══════════════════════════════════════════════════════════
# بررسی یک ترکیب
# ═══════════════════════════════════════════════════════════
def check_config_signals(config, df_ct, df_sfp=None):
    """
    بررسی سیگنال‌های جدید برای یک ترکیب.
    فقط سیگنال‌هایی که روی آخرین کندل بسته‌شده صادر شده‌اند.
    """
    symbol = config["symbol"]
    ct_tf = config["ct_tf"]
    mode = config["mode"]
    rr = config["rr"]
    sfp_tf = config["sfp_tf"]
    config_id = config["id"]

    # تنظیم inputs
    inputs = dict(CT_INPUTS_DEFAULT)
    if mode.startswith("Anni"):
        inputs["anni_stop_mode"] = "Far Edge (لبه دور ابر)" if "FarEdge" in mode else "Mid-Cloud (وسط ابر)"
    else:
        inputs["aati_stop_mode"] = "Safe (امن)" if "Safe" in mode else "Risky (ریسکی)"
    inputs["enable_rf_second_touch"] = False
    inputs["enable_rf_reversal_candle"] = False
    inputs["enable_log"] = False

    # اجرای CT
    try:
        ct_signals = [s for s in run_ct_strategy(df_ct, symbol, ct_tf, inputs=inputs) if s]
    except Exception as e:
        logger.error(f"{config_id} CT failed: {e}")
        return []

    kind_prefix = "Anni" if mode.startswith("Anni") else "Aati"
    ct_signals = [s for s in ct_signals if s['kind'].startswith(kind_prefix)]
    ct_signals = [s for s in ct_signals if is_valid_signal(s)]

    if not ct_signals:
        return []

    # SFP filter
    if sfp_tf and df_sfp is not None:
        o = df_sfp['open'].to_numpy(float); h = df_sfp['high'].to_numpy(float)
        l = df_sfp['low'].to_numpy(float); c = df_sfp['close'].to_numpy(float)
        sfp_events = run_sfp_events(o, h, l, c)
        sfp_ts = [int(t.timestamp()*1000) for t in df_sfp.index]
        by_time = {}
        for ev in sfp_events:
            by_time.setdefault(sfp_ts[ev['bar']], []).append(ev)
        sfp_times = sorted(by_time.keys())
        tf_ms = {"15": 900_000, "60": 3_600_000, "240": 14_400_000}[sfp_tf]

        filtered = []
        for sig in ct_signals:
            lo = sig['time_ms'] - 8 * tf_ms
            hi = sig['time_ms']
            i_lo = bisect_left(sfp_times, lo)
            i_hi = bisect_right(sfp_times, hi)
            found = False
            for i in range(i_lo, i_hi):
                for e in by_time[sfp_times[i]]:
                    if e['dir'] == sig['direction']:
                        found = True; break
                if found: break
            if found: filtered.append(sig)
        ct_signals = filtered

    # فقط آخرین کندل
    last_bar_time = int(df_ct.index[-1].timestamp() * 1000)
    ct_signals = [s for s in ct_signals if s['time_ms'] == last_bar_time]

    # اضافه کردن target بر اساس RR
    result = []
    for sig in ct_signals:
        D = abs(sig['entry'] - sig['stop'])
        if D <= 0: continue
        target = sig['entry'] + rr * D if sig['direction'] == "LONG" else sig['entry'] - rr * D
        result.append({
            "config_id": config_id,
            "symbol": symbol,
            "ct_tf": ct_tf,
            "mode": mode,
            "rr": rr,
            "direction": sig['direction'],
            "kind": sig['kind'],
            "entry": sig['entry'],
            "stop": sig['stop'],
            "target": target,
            "time_ms": sig['time_ms'],
            "time_utc": pd.Timestamp(sig['time_ms'], unit='ms', tz='UTC'),
        })
    return result


def is_valid_signal(sig):
    e = sig.get('entry'); s = sig.get('stop'); t = sig.get('target')
    if e is None or s is None or t is None:
        return False
    try:
        if any(math.isnan(x) or math.isinf(x) for x in [e, s, t]):
            return False
    except:
        return False
    if sig['direction'] == "LONG":
        if s >= e or t <= e: return False
    else:
        if s <= e or t >= e: return False
    sp = abs(e - s) / e * 100
    return 0.3 <= sp <= 5.0


# ═══════════════════════════════════════════════════════════
# اجرای همه ترکیب‌ها — تابع اصلی
# ═══════════════════════════════════════════════════════════
def check_all_signals():
    """
    روی همه ترکیب‌های طلایی چک کن.
    فقط سیگنال‌های جدید (نسبت به state) را برمی‌گرداند.
    """
    state = load_state()
    all_new_signals = []

    # گروه‌بندی بر اساس symbol (برای کاهش fetch)
    by_symbol = {}
    for cfg in GOLDEN_CONFIGS:
        by_symbol.setdefault(cfg["symbol"], []).append(cfg)

    for symbol, configs in by_symbol.items():
        # دریافت داده
        try:
            df_1m = fetch_klines(symbol, "1m", limit=1000)
        except Exception as e:
            logger.error(f"fetch {symbol} 1m failed: {e}")
            continue

        # Resample
        needed_tfs = set()
        for cfg in configs:
            needed_tfs.add(cfg["ct_tf"])
            if cfg["sfp_tf"]:
                needed_tfs.add(cfg["sfp_tf"])

        dfs = {}
        for tf in needed_tfs:
            rule = {"15": "15min", "60": "1h", "240": "4h"}[tf]
            df_r = df_1m.resample(rule).agg({
                'open':'first','high':'max','low':'min',
                'close':'last','volume':'sum'
            }).dropna()
            dfs[tf] = df_r

        # چک هر ترکیب
        for cfg in configs:
            df_ct = dfs[cfg["ct_tf"]]
            df_sfp = dfs[cfg["sfp_tf"]] if cfg["sfp_tf"] else None

            signals = check_config_signals(cfg, df_ct, df_sfp)

            for sig in signals:
                key = f"{cfg['id']}_{sig['time_ms']}"
                if key in state["fired"]:
                    continue  # قبلاً fire شده
                state["fired"][key] = sig['time_ms']
                all_new_signals.append(sig)

    save_state(state)
    return all_new_signals