#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dtm_parity_logger.py
====================
اجرای «خالص» DTM (بدون فیلتر CT، بدون سفارش، بدون تلگرام) با لاگ بسیار کامل،
برای سنجش تطابق ۱۰۰٪ پایتون (PyneCore) با Pine Script.

این فایل هیچ‌چیز از strategy.py / strategy_wrapper.py را تغییر نمی‌دهد و کد آن‌ها را کپی هم نمی‌کند:
  • خودِ strategy_wrapper.calculate_signals اجرا می‌شود و خروجی ScriptRunner (همان دیکشنری
    ~۱۷۰ مقداری که strategy.py در هر کندل برمی‌گرداند) در همان اجرا «ضبط» می‌شود.
  • مراحل بعد از استراتژی (checkColorChange با تلرانس، استاپ/تارگت، ریسک‌فری، فیلتر E)
    برای «هر کندل» با همان توابع خودِ wrapper دوباره اجرا و با جزئیات کامل ردیابی می‌شود.
  • برای اطمینان از اینکه این پردازش کندل‌به‌کندل با رفتار واقعی ربات یکی است، روی چند کندل
    (به‌خصوص کندل‌های سیگنال) calculate_signals واقعی دوباره اجرا و نتیجه‌ها مقایسه می‌شود.

خروجی‌ها (در پوشه‌ی --out-dir):
  <prefix>_full.log          لاگ کامل: محیط، ورودی‌ها، هر کندل، رویدادها، خلاصه
  <prefix>_signals.log       ردیابی کامل زنجیره‌ی هر سیگنال (امتیازها، رنگ MACD، جستجوی استاپ، R:R)
  <prefix>_bars.csv          همه‌ی مقادیر هر کندل با دقت کامل (۱۷ رقم) + ستون‌های py_*
  <prefix>_pine_format.log   خطوط [HL] و [DIVCHECK] با همان فرمتی که pine_hl_lookup.py می‌خواند
  <prefix>_signals.csv       جدول سیگنال‌های نهایی
  <prefix>_ohlcv.csv         دقیقاً همان کندل‌هایی که استفاده شد (برای مقایسه‌ی داده با TradingView)
  compare_report.txt / compare_mismatches.csv   (فقط با --pine-csv)

نمونه:
  python dtm_parity_logger.py --symbol ETHUSDT --tf 5 --source binance --bars 1500
  python dtm_parity_logger.py --symbol ETHUSDT --tf 5 --source csv --csv tv_export_ohlcv.csv
  python dtm_parity_logger.py --symbol ETHUSDT --tf 5 --source csv --csv data.csv --pine-csv tv_plots.csv
  python dtm_parity_logger.py --compare-only parity_logs/ETHUSDT_5m_bars.csv --pine-csv tv_plots.csv --tf 5
"""
import argparse
import csv
import hashlib
import json
import logging
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

UTC = timezone.utc
log = logging.getLogger("DTM_PARITY")
slog = logging.getLogger("DTM_PARITY.SIGNAL")      # لاگ ردیابی سیگنال‌ها (فایل جدا + داخل لاگ کامل)
plog = logging.getLogger("DTM_PARITY.PINEFMT")     # خطوط با فرمت Pine

KINDS = ("CD-", "CD+", "HD+", "HD-")


# ═══════════════════════════════════════════════════════════════
# ابزارهای کوچک
# ═══════════════════════════════════════════════════════════════
def _isnan(x):
    return x is None or (isinstance(x, float) and x != x)


def fnum(x):
    """تبدیل به رشته با دقت کامل (برای مقایسه‌ی دقیق با Pine)."""
    if x is None:
        return ""
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, float):
        if x != x:
            return ""
        if math.isinf(x):
            return "inf" if x > 0 else "-inf"
        return repr(x)
    return str(x)


def ts_str(ms):
    try:
        return datetime.fromtimestamp(ms / 1000.0, tz=UTC).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "?"


def parse_time_ms(v):
    s = str(v).strip()
    try:
        f = float(s)
        return int(f) if f > 1e12 else int(f * 1000)
    except ValueError:
        pass
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return int(dt.timestamp() * 1000)


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def _clone_result(res):
    """کپی مستقل از خروجی ScriptRunner (wrapper هم به همین دلیل dict(...) می‌گیرد)."""
    try:
        d = res[1]
        if isinstance(d, dict):
            d = {k: (dict(v) if isinstance(v, dict) else v) for k, v in d.items()}
        return (res[0], d)
    except Exception:
        return res


def _W():
    import strategy_wrapper as W
    return W


# ═══════════════════════════════════════════════════════════════
# بارگذاری داده
# ═══════════════════════════════════════════════════════════════
def _df_from_rows(rows):
    import pandas as pd
    idx = pd.to_datetime([r[0] for r in rows], unit="ms", utc=True)
    df = pd.DataFrame(
        {"open": [r[1] for r in rows], "high": [r[2] for r in rows], "low": [r[3] for r in rows],
         "close": [r[4] for r in rows], "volume": [r[5] for r in rows]},
        index=idx,
    )
    df = df[~df.index.duplicated(keep="last")].sort_index()
    return df


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        rd.fieldnames = [h.strip().lower() for h in rd.fieldnames]
        need = {"time", "open", "high", "low", "close"}
        if not need.issubset(set(rd.fieldnames)):
            raise SystemExit(f"CSV باید ستون‌های {sorted(need)} (و اختیاری volume) داشته باشد؛ یافت شد: {rd.fieldnames}")
        rows = []
        for r in rd:
            rows.append((parse_time_ms(r["time"]), float(r["open"]), float(r["high"]), float(r["low"]),
                         float(r["close"]), float(r.get("volume") or 0.0)))
    return _df_from_rows(rows)


def load_binance(symbol, tf, bars):
    import requests
    iv = {"1": "1m", "3": "3m", "5": "5m", "15": "15m", "30": "30m", "60": "1h", "240": "4h", "1440": "1d"}[str(tf)]
    out, end = [], None
    while len(out) < bars:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={iv}&limit=1000"
        if end:
            url += f"&endTime={end}"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        k = r.json()
        if not k:
            break
        out = [(int(x[0]), float(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5])) for x in k] + out
        end = int(k[0][0]) - 1
        if len(k) < 1000:
            break
    return _df_from_rows(out[-bars:])


def load_thetruetrade(symbol, tf):
    try:
        import bot  # نیاز به API_KEY/API_SECRET در محیط دارد
        return bot.PublicData().fetch_ohlcv(symbol, str(tf))
    except Exception as e:
        raise SystemExit(f"خواندن از thetruetrade ممکن نشد: {e}")


def fingerprint(df):
    h = hashlib.sha256()
    for ts, row in df.iterrows():
        h.update(f"{int(ts.timestamp()*1000)},{row['open']!r},{row['high']!r},{row['low']!r},{row['close']!r},{row.get('volume', 0)!r}\n".encode())
    return h.hexdigest()


def sha256_file(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except Exception:
        return "N/A"


# ═══════════════════════════════════════════════════════════════
# ضبط خروجی ScriptRunner (بدون دست‌زدن به wrapper)
# ═══════════════════════════════════════════════════════════════
class Capture:
    def __init__(self):
        self.candles, self.results = [], []
        self.inputs = self.last_bar_index = self.script_path = None


_CAP = {"cur": None}


def install_runner_proxy():
    import pynecore.core.script_runner as sr
    real = sr.ScriptRunner

    class RecordingRunner:
        def __init__(self, script_path, candles_iter, syminfo, *a, **k):
            cap = _CAP["cur"]
            self._cap = cap
            if cap is not None:
                cap.inputs = k.get("inputs")
                cap.last_bar_index = k.get("last_bar_index")
                cap.script_path = script_path

                _orig_iter = candles_iter   # نام جدا؛ وگرنه closure به خودِ tee() اشاره می‌کند

                def tee():
                    for c in _orig_iter:
                        cap.candles.append(c)
                        yield c
                candles_iter = tee()
            self._real = real(script_path, candles_iter, syminfo, *a, **k)

        def run_iter(self, *a, **k):
            for res in self._real.run_iter(*a, **k):
                if self._cap is not None:
                    self._cap.results.append(_clone_result(res))
                yield res

        def __getattr__(self, name):
            return getattr(self._real, name)

    sr.ScriptRunner = RecordingRunner
    return lambda: setattr(sr, "ScriptRunner", real)


def run_wrapper_captured(df, symbol, tf):
    """calculate_signals واقعی را اجرا می‌کند و همه‌ی خروجی‌های کندل‌به‌کندل را برمی‌گرداند."""
    W = _W()
    cap = Capture()
    _CAP["cur"] = cap
    try:
        ret = W.calculate_signals(df, symbol, str(tf), silent=True)
    finally:
        _CAP["cur"] = None
    return ret, cap


# ═══════════════════════════════════════════════════════════════
# ردیابی توابع wrapper (بازتولید گام‌به‌گام + تطبیق با نتیجه‌ی خودِ تابع)
# ═══════════════════════════════════════════════════════════════
def kind_of(d):
    if d.get("final_classic_bearish"):
        return "CD-"
    if d.get("final_classic_bullish"):
        return "CD+"
    if d.get("final_hidden_bullish"):
        return "HD+"
    if d.get("final_hidden_bearish"):
        return "HD-"
    return None


def _idx_time(cs, idx):
    try:
        i = int(idx)
        return ts_str(cs[i].timestamp) if 0 <= i < len(cs) else "OUT_OF_RANGE"
    except Exception:
        return "NA"


def raw_color_change_hl(hist, bar_idx, b1, b2, need_red):
    """
    بازتولید checkColorChange خودِ strategy.py (بدون تلرانس) از روی هیستوگرام ضبط‌شده.
    خروجی: (found, [(j, h), ...])  — همان j و h که در لاگ‌های [HL] Pine می‌آید.
    """
    pairs, found = [], False
    if _isnan(b1) or _isnan(b2):
        return found, pairs
    b1, b2 = int(b1), int(b2)
    if not (b2 > b1):
        return found, pairs
    start_off = bar_idx - (b2 - 1)
    end_off = bar_idx - (b1 + 1)
    if start_off >= 0 and end_off <= 5000 and end_off >= start_off:
        for j in range(start_off, end_off + 1):
            idx = bar_idx - j
            h = hist[idx] if 0 <= idx < len(hist) else None
            pairs.append((j, h))
            if h is None:
                continue
            if need_red and h < 0:
                found = True
                break
            if (not need_red) and h > 0:
                found = True
                break
    return found, pairs


def trace_color_change_tol(hist, bar_idx, b1, b2, need_red, tol):
    """بازتولید _py_check_color_change (با تلرانس wrapper) + لاگ تصمیم هر j."""
    L = [f"checkColorChange[wrapper+tol] need_red={need_red} bar_idx={bar_idx} b1={b1} b2={b2} tol={tol}"]
    if b1 is None or b2 is None:
        return False, L + ["  → b1/b2 None ⇒ False"]
    try:
        b1, b2 = int(b1), int(b2)
    except (ValueError, TypeError):
        return False, L + ["  → b1/b2 غیرعددی ⇒ False"]
    if b2 <= b1:
        return False, L + [f"  → b2<=b1 ({b2}<={b1}) ⇒ False"]
    so, eo = bar_idx - (b2 - 1), bar_idx - (b1 + 1)
    L.append(f"  startOffset={so} endOffset={eo}")
    if so < 0 or eo > 5000 or eo < so:
        return False, L + ["  → offset نامعتبر ⇒ False"]
    for j in range(so, eo + 1):
        idx = bar_idx - j
        if idx < 0 or idx >= len(hist):
            L.append(f"  j={j} idx={idx} خارج از محدوده → رد")
            continue
        h = hist[idx]
        if h is None:
            L.append(f"  j={j} idx={idx} hist=None → رد")
            continue
        if abs(h) <= tol:
            L.append(f"  j={j} idx={idx} hist={h!r} |h|<=tol → صفر حساب شد، رد")
            continue
        hit = (need_red and h < 0) or ((not need_red) and h > 0)
        L.append(f"  j={j} idx={idx} hist={h!r} {'MATCH ⇒ True' if hit else 'رنگ نامناسب، ادامه'}")
        if hit:
            return True, L
    return False, L + ["  → هیچ کندل مناسبی نبود ⇒ False"]


def trace_extended_scan(cs, signal, older_bar, extreme, buf, W):
    """بازتولید _find_extended_stop_pivot با لاگ کاندیدها."""
    L = []
    if older_bar is None or extreme is None:
        return None, None, ["  extended-scan: ورودی None"]
    win, lb, rb = W.STOP_SEARCH_WINDOW, W.STOP_PIVOT_LEFT, W.STOP_PIVOT_RIGHT
    older_bar = int(older_bar)
    start = max(0, older_bar - win)
    L.append(f"  extended-scan: از {older_bar - 1} تا {start} (window={win}, left={lb}, right={rb}) extreme={extreme!r} buf={buf!r}")
    unconfirmed = 0
    for i in range(older_bar - 1, start - 1, -1):
        if signal == "LONG":
            ok = W._is_confirmed_pivot_low(cs, i, lb, rb)
        else:
            ok = W._is_confirmed_pivot_high(cs, i, lb, rb)
        if not ok:
            unconfirmed += 1
            continue
        cand = cs[i].low if signal == "LONG" else cs[i].high
        beyond = (cand < extreme) if signal == "LONG" else (cand > extreme)
        L.append(f"    کاندید پیوت idx={i} ({_idx_time(cs, i)}) قیمت={cand!r} فراتر از extreme؟ {beyond}")
        if beyond:
            res = (cand - buf) if signal == "LONG" else (cand + buf)
            L.append(f"    ✔ انتخاب شد → stop={res!r} (کاندیدهای تاییدنشده‌ی ردشده: {unconfirmed})")
            return res, i, L
    L.append(f"  extended-scan: چیزی پیدا نشد (تاییدنشده‌ها: {unconfirmed}) ⇒ fallback")
    return None, None, L


def trace_stop_target(cs, signal, d, mintick, buffer_ticks, W):
    """بازتولید _compute_stop_target با لاگ کامل. خروجی: (lines, (stop, target, rr, structural))"""
    L = []
    ok = lambda x: x is not None and not (isinstance(x, float) and math.isnan(x))
    entry = d.get("entry")
    buf = buffer_ticks * mintick
    L.append(f"stop/target: signal={signal} entry={entry!r} mintick={mintick!r} buffer_ticks={buffer_ticks} buffer_abs={buf!r} MIN_RR={W.MIN_RR}")
    if not ok(entry):
        return L + ["  entry نامعتبر ⇒ (None×4)"], (None, None, None, None)
    long_ = signal == "LONG"
    keys = (("previous_pivot_low_price", "pivot_low_price", "previous_pivot_low_index", "pivot_low_index") if long_
            else ("previous_pivot_high_price", "pivot_high_price", "previous_pivot_high_index", "pivot_high_index"))
    p1, p2, b1, b2 = (d.get(k) for k in keys)
    L.append(f"  پیوت‌ها: p1={p1!r}@{b1} ({_idx_time(cs, b1) if ok(b1) else 'NA'}) | p2={p2!r}@{b2} ({_idx_time(cs, b2) if ok(b2) else 'NA'})")
    if not (ok(p1) and ok(p2) and ok(b1) and ok(b2)):
        return L + ["  داده‌ی پیوت ناقص ⇒ (None×4)"], (None, None, None, None)
    fb_ext = min(p1, p2) if long_ else max(p1, p2)
    fb_stop = (fb_ext - buf) if long_ else (fb_ext + buf)
    older = min(int(b1), int(b2))
    L.append(f"  fallback: extreme={fb_ext!r} stop={fb_stop!r} | older_bar={older}")
    ext, pidx, sl = trace_extended_scan(cs, signal, older, fb_ext, buf, W)
    L += sl
    stop = ext if ext is not None else fb_stop
    L.append(f"  stop نهایی={stop!r} ({'extended' if ext is not None else 'fallback'})")
    lo, hi = sorted((int(b1), int(b2)))
    lo, hi = max(lo, 0), min(hi, len(cs) - 1)
    if hi < lo:
        return L + ["  hi<lo ⇒ (None×4)"], (None, None, None, None)
    if long_:
        mid = max(c.high for c in cs[lo:hi + 1])
        risk = entry - stop
        L.append(f"  بازه [{lo},{hi}] بالاترین قله mid_peak={mid!r} | risk=entry-stop={risk!r}")
        if risk <= 0:
            return L + ["  risk<=0 ⇒ (None×4)"], (None, None, None, None)
        rr = (mid - entry) / risk
        target = mid if rr >= W.MIN_RR else entry + W.MIN_RR * risk
    else:
        mid = min(c.low for c in cs[lo:hi + 1])
        risk = stop - entry
        L.append(f"  بازه [{lo},{hi}] پایین‌ترین دره mid_trough={mid!r} | risk=stop-entry={risk!r}")
        if risk <= 0:
            return L + ["  risk<=0 ⇒ (None×4)"], (None, None, None, None)
        rr = (entry - mid) / risk
        target = mid if rr >= W.MIN_RR else entry - W.MIN_RR * risk
    L.append(f"  rr_raw={rr!r} → target={target!r} ({'ساختاری' if rr >= W.MIN_RR else 'اصلاح‌شده تا R:R=MIN_RR'}) rr_final={max(rr, W.MIN_RR)!r}")
    return L, (stop, target, max(rr, W.MIN_RR), mid)


def buffer_ticks_for(symbol):
    """همان قاعده‌ی داخل calculate_signals (در آن تابع جدا نیست؛ با --verify-* تطبیقش چک می‌شود)."""
    if symbol in ("BNBUSDT", "ETHUSDT"):
        return 9
    if symbol in ("LTCUSDT", "DOGEUSDT"):
        return 3
    if symbol == "PUMPUSDT":
        return 1
    return 5


# ═══════════════════════════════════════════════════════════════
# پردازش یک کندل — همان ترتیب مراحل calculate_signals
# ═══════════════════════════════════════════════════════════════
def post_process(i, cs, hist, d, valid, symbol, tick_info, want_trace=True):
    W = _W()
    out = dict(signal_raw=None, signal_type=None, color_tol=None, parity_filtered=False,
               filterE=False, signal_final=None, entry_final=None, stop=None, target=None,
               rr=None, structural=None, risk_free_pct=None, wrapper_crash=False)
    T = []
    if not valid:
        return out, T
    signal, entry = d.get("signal"), d.get("entry")
    if signal not in ("LONG", "SHORT"):
        out["entry_final"] = entry      # wrapper در کندل بدون سیگنال هم entry=close را برمی‌گرداند
        return out, T
    out["signal_raw"] = signal
    kind = kind_of(d)
    out["signal_type"] = kind

    # ── (۱) checkColorChange با تلرانس (Pine-Exact parity) ──
    if signal == "SHORT":
        b1, b2, need_red = d.get("previous_pivot_high_index"), d.get("pivot_high_index"), True
        raw_cc = d.get("macd_color_changed_highs")
    else:
        b1, b2, need_red = d.get("previous_pivot_low_index"), d.get("pivot_low_index"), False
        raw_cc = d.get("macd_color_changed_lows")
    try:
        ok_real = W._py_check_color_change(hist[:i + 1], i, b1, b2, need_red)
    except Exception as e:
        ok_real = True   # wrapper در خطا فیلتر نمی‌کند
        T.append(f"[PARITY] checkColorChange خطا داد ({e}) → wrapper فیلتر نمی‌کند")
    ok_tr, ctl = trace_color_change_tol(hist, i, b1, b2, need_red, W.HIST_TOLERANCE)
    out["color_tol"] = ok_real
    if want_trace:
        T += ctl
        T.append(f"  strategy.py (بدون تلرانس) macd_color_changed = {raw_cc!r} | wrapper (با تلرانس) = {ok_real}")
        if ok_tr != ok_real:
            T.append("  ‼ TRACE-MISMATCH: ردیابی با تابع واقعی wrapper یکی نیست!")
    if not ok_real:
        out["parity_filtered"] = True
        T.append(f"[PARITY] checkColorChange filtered: {signal} (b1={b1} b2={b2}) ⇒ سیگنال حذف شد")
        return out, T

    # ── (۲) استاپ/تارگت ──
    buf_ticks = buffer_ticks_for(symbol)
    stop, target, rr, structural = W._compute_stop_target(cs[:i + 1], signal, d, tick_info["mintick"], buffer_ticks=buf_ticks)
    if want_trace:
        sl, tr = trace_stop_target(cs[:i + 1], signal, d, tick_info["mintick"], buf_ticks, W)
        T += sl
        if tr != (stop, target, rr, structural):
            T.append(f"  ‼ TRACE-MISMATCH: ردیابی={tr} ≠ تابع واقعی={(stop, target, rr, structural)}")
    out.update(stop=stop, target=target, rr=rr, structural=structural)

    # ── (۳) نقطه‌ی ریسک‌فری ──
    rf = None
    if structural is not None and stop is not None and W._valid_num(entry) and entry > 0:
        risk_pct = abs(entry - stop) / entry
        if signal == "LONG":
            sp = (structural - entry) / entry
            rf = max(sp, risk_pct)
        else:
            sp = (entry - structural) / entry
            rf = -max(sp, risk_pct)
        T.append(f"[RISK-FREE] structural={structural!r} struct_pct={sp!r} risk_pct={risk_pct!r} ⇒ rf_pct={rf!r}")
    out["risk_free_pct"] = rf

    # ── (۴) فیلتر E (لیست سیاه نماد) ──
    bl = W.PER_SYMBOL_BLACKLIST.get(symbol.upper(), [])
    if kind in bl:
        out["filterE"] = True
        T.append(f"[FILTER-E] {symbol} {kind} در blacklist={bl} ⇒ رد شد")
        return out, T
    T.append(f"[FILTER-E] blacklist={bl} ⇒ عبور")
    if stop is None or target is None or rr is None:
        # در calculate_signals پیام تلگرام با f"{stop_price:.{_pp}f}" ساخته می‌شود؛ با None
        # TypeError می‌دهد → except کلی → «FATAL ERROR» و برگشت (None×7).
        out["wrapper_crash"] = True
        T.append(f"[WRAPPER] ‼ stop={stop!r} target={target!r} rr={rr!r} ⇒ ساخت پیام TypeError می‌دهد؛ "
                 f"calculate_signals پیام FATAL ERROR می‌فرستد و (None×7) برمی‌گرداند ⇒ سیگنال از بین می‌رود")
        return out, T
    out.update(signal_final=signal, entry_final=entry)
    return out, T


# ═══════════════════════════════════════════════════════════════
# لاگ هر کندل
# ═══════════════════════════════════════════════════════════════
def bar_line(i, c, d):
    g = lambda k: fnum(d.get(k)) if not isinstance(d.get(k), float) else f"{d.get(k):.6g}"
    return (f"[BAR] i={i} t={ts_str(c.timestamp)} O={c.open!r} H={c.high!r} L={c.low!r} C={c.close!r} V={getattr(c, 'volume', 0)!r} | "
            f"rsi={g('rsi')} macd={g('macd_line')} sig={g('macd_signal_line')} hist={g('macd_histogram')} atr={g('atr')} | "
            f"PH={g('pivot_high')} PL={g('pivot_low')} | "
            f"score CD-/CD+/HD+/HD-={g('score_classic_bearish')}/{g('score_classic_bullish')}/{g('score_hidden_bullish')}/{g('score_hidden_bearish')} | "
            f"signal={d.get('signal')}")


def is_event(d):
    if not _isnan(d.get("pivot_high")) or not _isnan(d.get("pivot_low")):
        return True
    for k in ("classic_bullish_base", "classic_bearish_base", "hidden_bullish_base", "hidden_bearish_base",
              "final_classic_bullish", "final_classic_bearish", "final_hidden_bullish", "final_hidden_bearish"):
        if d.get(k):
            return True
    return d.get("signal") in ("LONG", "SHORT")


def dump_full(i, c, d):
    flat = flatten(d)
    log.info(f"[EVENT] ─── کندل i={i} t={ts_str(c.timestamp)} | همه‌ی مقادیر strategy.py ───")
    w = max((len(k) for k in flat), default=10)
    for k, v in flat.items():
        log.info(f"[EVENT]   {k:<{w}} = {fnum(v)}")


# ═══════════════════════════════════════════════════════════════
# پردازش کل ضبط‌شده
# ═══════════════════════════════════════════════════════════════
def process_capture(cap, symbol, verbose_bars):
    W = _W()
    tick_info = W.SYMBOL_TICK_INFO.get(symbol, {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")})
    cs, res = cap.candles, cap.results
    if len(cs) != len(res):
        log.warning(f"تعداد کندل‌ها ({len(cs)}) با تعداد نتیجه‌ها ({len(res)}) برابر نیست — کوتاه‌ترین استفاده می‌شود")
    n = min(len(cs), len(res))
    valid_flags, ds, hist = [], [], []
    for r in res[:n]:
        d = r[1] if (len(r) >= 2 and isinstance(r[1], dict)) else {}
        v = len(d) > 0
        valid_flags.append(v)
        ds.append(d)
        hist.append(d.get("macd_histogram") if v else None)

    rows, signals = [], []
    for i in range(n):
        c, d, v = cs[i], ds[i], valid_flags[i]
        if not v:
            log.warning(f"[BAR] i={i} t={ts_str(c.timestamp)} نتیجه‌ی خالی (خطای داخلی main در strategy.py؟)")
        elif verbose_bars:
            dump_full(i, c, d)
        else:
            log.info(bar_line(i, c, d))
            if is_event(d):
                dump_full(i, c, d)

        # فرمت Pine برای pine_hl_lookup
        if v:
            for key, need_red in (("pivot_high", True), ("pivot_low", False)):
                if not _isnan(d.get(key)):
                    b1 = d.get("previous_pivot_high_index" if need_red else "previous_pivot_low_index")
                    b2 = d.get("pivot_high_index" if need_red else "pivot_low_index")
                    _, pairs = raw_color_change_hl(hist, i, b1, b2, need_red)
                    for j, h in pairs:
                        plog.info(f"[HL] {i}|{'true' if need_red else 'false'}|{j}|{fnum(h)} ts={ts_str(c.timestamp)}")
            if not _isnan(d.get("pivot_high")) or not _isnan(d.get("pivot_low")):
                plog.info(f"[DIVCHECK] bar_index={i} ts={ts_str(c.timestamp)} total_bars={i} "
                          f"trendOkBear={'true' if d.get('trend_bearish_ok') else 'false'} "
                          f"trendOkBull={'true' if d.get('trend_bullish_ok') else 'false'}")

        out, T = post_process(i, cs, hist, d, v, symbol, tick_info, want_trace=True)
        if d.get("signal") in ("LONG", "SHORT") or out["signal_raw"]:
            slog.info("═" * 100)
            slog.info(f"سیگنال خام کندل i={i} t={ts_str(c.timestamp)} {out['signal_raw']} نوع={out['signal_type']} entry={d.get('entry')!r}")
            slog.info(f"  امتیازها CD-={d.get('score_classic_bearish')} CD+={d.get('score_classic_bullish')} "
                      f"HD+={d.get('score_hidden_bullish')} HD-={d.get('score_hidden_bearish')} | minConfirmations={d.get('min_confirmations')!r}")
            for k in ("score_cd_minus_detail", "score_cd_plus_detail", "score_hd_plus_detail", "score_hd_minus_detail"):
                if isinstance(d.get(k), dict) and d.get(k):
                    slog.info(f"  {k}: " + " ".join(f"{a}={fnum(b)}" for a, b in d[k].items()))
            slog.info(f"  bases: CD-={d.get('classic_bearish_base')} CD+={d.get('classic_bullish_base')} "
                      f"HD+={d.get('hidden_bullish_base')} HD-={d.get('hidden_bearish_base')} | "
                      f"fib bear/bull={d.get('fib_bearish')}/{d.get('fib_bullish')} | PA bear/bull={d.get('price_action_bearish')}/{d.get('price_action_bullish')}")
            slog.info(f"  trend ok bear/bull={d.get('trend_bearish_ok')}/{d.get('trend_bullish_ok')} | "
                      f"prominence H/L={fnum(d.get('prominence_high'))}/{fnum(d.get('prominence_low'))}")
            for ln in T:
                slog.info(ln)
            slog.info(f"⇒ نتیجه‌ی نهایی: signal={out['signal_final']} entry={out['entry_final']!r} stop={out['stop']!r} "
                      f"target={out['target']!r} rr={out['rr']!r} rf_pct={out['risk_free_pct']!r} "
                      f"(parity_filtered={out['parity_filtered']} filterE={out['filterE']})")
            if out["signal_final"]:
                signals.append(dict(i=i, ts_ms=c.timestamp, time=ts_str(c.timestamp), signal=out["signal_final"],
                                    kind=out["signal_type"], entry=out["entry_final"], stop=out["stop"],
                                    target=out["target"], rr=out["rr"], risk_free_pct=out["risk_free_pct"]))

        row = {"bar_index": i, "ts_ms": c.timestamp, "time_utc": ts_str(c.timestamp), "open": c.open, "high": c.high,
               "low": c.low, "close": c.close, "volume": getattr(c, "volume", 0.0), "valid": v}
        row.update(flatten(d))
        row.update({f"py_{k}": val for k, val in out.items()})
        rows.append({k: fnum(val) for k, val in row.items()})
    return rows, signals, (cs, ds, hist, valid_flags, tick_info)


def write_rows_csv(path, rows):
    cols = []
    seen = set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ═══════════════════════════════════════════════════════════════
# تأیید تطابق با calculate_signals واقعی
# ═══════════════════════════════════════════════════════════════
def _same(a, b):
    if a is None or b is None:
        return a is None and b is None
    try:
        return a == b or (isinstance(a, float) and isinstance(b, float) and a != a and b != b)
    except Exception:
        return False


def verify_with_real_wrapper(df, symbol, tf, rows, signals, n_last, n_signals):
    """
    روی چند کندل، calculate_signals واقعی (روی داده‌ی بریده‌شده تا همان کندل) اجرا و
    با (الف) پردازش آفلاین همین فایل و (ب) ردیف همان کندل در اجرای اصلی مقایسه می‌شود.
    """
    W = _W()
    n = len(rows)
    targets = set(range(max(0, n - n_last), n))
    raw_idx = [int(r["bar_index"]) for r in rows if r.get("py_signal_raw")]
    crash_idx = [int(r["bar_index"]) for r in rows if r.get("py_wrapper_crash") == "true"]
    if n_signals:
        targets.update(raw_idx[-n_signals:])
        targets.update(crash_idx[-2:])
    by_ts = {r["ts_ms"]: r for r in rows}
    problems = 0
    log.info("═" * 100)
    log.info(f"تأیید با calculate_signals واقعی روی {len(targets)} کندل: {sorted(targets)}")
    for i in sorted(targets):
        df_i = df.iloc[:i + 1]
        ret, cap = run_wrapper_captured(df_i, symbol, tf)
        if not cap.candles:
            log.warning(f"  i={i}: ضبطی انجام نشد (داده کم؟)")
            continue
        sig, entry, stop, target, ts_ms, rf, _ = ret
        cs, ds, hist = cap.candles, [r[1] if isinstance(r[1], dict) else {} for r in cap.results], []
        hist = [d.get("macd_histogram") if d else None for d in ds]
        j = len(cs) - 1
        tick = W.SYMBOL_TICK_INFO.get(symbol, {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")})
        off, _T = post_process(j, cs, hist, ds[j], bool(ds[j]), symbol, tick, want_trace=False)
        real = (sig, entry, stop, target, ts_ms, rf)
        mine = (off["signal_final"], off["entry_final"], off["stop"], off["target"], cs[j].timestamp, off["risk_free_pct"])
        if off.get("wrapper_crash"):
            mine = (None,) * 6          # wrapper در این حالت (None×7) برمی‌گرداند
        ok1 = all(_same(a, b) for a, b in zip(real, mine))
        row = by_ts.get(cs[j].timestamp)
        ok2 = True
        if row is not None:
            main = (row.get("py_signal_final", ""), row.get("py_stop", ""), row.get("py_target", ""))
            cur = (fnum(sig) if sig else "", fnum(stop), fnum(target))
            ok2 = main == cur
        tag = "OK " if (ok1 and ok2) else "MISMATCH"
        log.info(f"  [{tag}] i={i} t={ts_str(cs[j].timestamp)} real={real} | offline={mine} | "
                 f"{'همان ردیف اجرای اصلی' if ok2 else 'با ردیف اجرای اصلی فرق دارد (وابسته به طول تاریخچه؟)'}")
        if not (ok1 and ok2):
            problems += 1
    log.info(f"نتیجه‌ی تأیید: {'همه‌ی کندل‌ها یکسان ✅' if problems == 0 else f'{problems} ناهمخوانی ❌'}")
    return problems


# ═══════════════════════════════════════════════════════════════
# مقایسه با خروجی TradingView / Pine
# ═══════════════════════════════════════════════════════════════
def norm_col(c):
    c = c.strip().lower().replace("+", "plus").replace("-", "minus")
    return re.sub(r"[^a-z0-9]", "", c)


def _num(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "" or s.lower() in ("nan", "na", "null", "none"):
        return None
    if s.lower() == "true":
        return 1.0
    if s.lower() == "false":
        return 0.0
    try:
        return float(s)
    except ValueError:
        return s


def compare_with_pine(py_rows, pine_path, tf, out_dir, tol, shift_bars, na_as_zero, max_show):
    tf_ms = int(tf) * 60 * 1000
    py = {int(r["ts_ms"]): r for r in py_rows}
    py_cols = {}
    for r in py_rows[:1]:
        for k in r:
            py_cols.setdefault(norm_col(k), k)
    with open(pine_path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        heads = [h.strip() for h in rd.fieldnames]
        tcol = next((h for h in heads if h.lower() == "time"), None)
        if tcol is None:
            raise SystemExit("در فایل Pine ستون time پیدا نشد")
        pine_rows = {}
        for r in rd:
            r = {k.strip(): v for k, v in r.items()}
            pine_rows[parse_time_ms(r[tcol]) + shift_bars * tf_ms] = r
    pine_cols = {norm_col(h): h for h in heads if h != tcol}
    common = [c for c in pine_cols if c in py_cols and c not in ("tsms", "timeutc", "barindex")]
    common_ts = sorted(set(py) & set(pine_rows))
    lines = []
    P = lambda s="": lines.append(s)
    P("گزارش مقایسه‌ی پایتون ↔ Pine")
    P(f"فایل Pine: {pine_path} | shift={shift_bars} کندل | tol={tol} | na_as_zero={na_as_zero}")
    P(f"کندل پایتون={len(py)} | کندل Pine={len(pine_rows)} | مشترک={len(common_ts)}")
    if common_ts:
        P(f"بازه‌ی مشترک: {ts_str(common_ts[0])} تا {ts_str(common_ts[-1])}")
    P(f"ستون‌های مشترک ({len(common)}): {', '.join(pine_cols[c] for c in common)}")
    P(f"فقط در Pine: {', '.join(pine_cols[c] for c in pine_cols if c not in py_cols) or '—'}")
    P("")
    order = [c for c in common if c in ("open", "high", "low", "close", "volume")] + [c for c in common if c not in ("open", "high", "low", "close", "volume")]
    mism_rows, total_mis, data_mis = [], 0, 0
    for c in order:
        pc, yc = pine_cols[c], py_cols[c]
        n_cmp = n_ok = 0
        maxd = 0.0
        shown = 0
        for t in common_ts:
            a, b = _num(py[t].get(yc)), _num(pine_rows[t].get(pc))
            if na_as_zero:
                a = 0.0 if a is None else a
                b = 0.0 if b is None else b
            n_cmp += 1
            if a is None and b is None:
                ok = True
            elif isinstance(a, float) and isinstance(b, float):
                ok = math.isclose(a, b, rel_tol=1e-9, abs_tol=tol)
                if not ok:
                    maxd = max(maxd, abs(a - b))
            else:
                ok = (a == b)
            if ok:
                n_ok += 1
            else:
                mism_rows.append({"column": pc, "time_utc": ts_str(t), "python": py[t].get(yc), "pine": pine_rows[t].get(pc)})
                if shown < max_show:
                    P(f"    ✗ {pc} @ {ts_str(t)}: python={py[t].get(yc)!r} pine={pine_rows[t].get(pc)!r}")
                    shown += 1
        total_mis += n_cmp - n_ok
        if c in ("open", "high", "low", "close", "volume"):
            data_mis += n_cmp - n_ok
        P(f"[{'OK ' if n_cmp == n_ok else 'DIFF'}] {pc}: {n_ok}/{n_cmp} یکسان" + (f" | بیشینه اختلاف عددی={maxd:.3g}" if maxd else ""))
    P("")
    if data_mis:
        P("⚠️ کندل‌های OHLCV پایتون و Pine یکی نیستند؛ تا داده یکی نشود، مقایسه‌ی بقیه معنی ندارد.")
    verdict = (len(common) > 0 and total_mis == 0)
    P("نتیجه: " + ("تطابق ۱۰۰٪ روی همه‌ی ستون‌های مشترک ✅" if verdict else
                   ("ستون مشترکی پیدا نشد (نام ستون‌های Pine با کلیدهای پایتون یکی نیست)" if not common else f"{total_mis} اختلاف ❌")))
    rep = "\n".join(lines)
    Path(out_dir, "compare_report.txt").write_text(rep, encoding="utf-8")
    if mism_rows:
        with open(Path(out_dir, "compare_mismatches.csv"), "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["column", "time_utc", "python", "pine"])
            w.writeheader()
            w.writerows(mism_rows)
    print(rep)
    return 0 if verdict else 1


# ═══════════════════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════════════════
class _ConsoleFilter(logging.Filter):
    """کنسول فقط خلاصه را نشان می‌دهد؛ جزئیات هر کندل/رویداد/ردیابی فقط در فایل‌ها می‌رود."""
    def filter(self, record):
        if record.levelno >= logging.WARNING:
            return True
        if record.name.startswith("DTM_PARITY.SIGNAL") or record.name != "DTM_PARITY":
            return False
        m = record.getMessage()
        return not (m.startswith("[BAR]") or m.startswith("[EVENT]"))


def setup_logging(out_dir, prefix, console_level, console_all=False):
    fmt = logging.Formatter("%(asctime)s.%(msecs)03d | %(levelname)-7s | %(name)s | %(message)s", "%H:%M:%S")
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.setLevel(logging.DEBUG)
    fh = logging.FileHandler(Path(out_dir, f"{prefix}_full.log"), "w", encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(logging.DEBUG)
    root.addHandler(fh)
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(console_level)
    if not console_all:
        ch.addFilter(_ConsoleFilter())
    root.addHandler(ch)
    sh = logging.FileHandler(Path(out_dir, f"{prefix}_signals.log"), "w", encoding="utf-8")
    sh.setFormatter(fmt)
    slog.addHandler(sh)
    ph = logging.FileHandler(Path(out_dir, f"{prefix}_pine_format.log"), "w", encoding="utf-8")
    ph.setFormatter(logging.Formatter("%(message)s"))
    plog.addHandler(ph)
    plog.propagate = False


def main():
    ap = argparse.ArgumentParser(description="DTM parity logger (بدون فیلتر CT، بدون سفارش)")
    ap.add_argument("--symbol", default="ETHUSDT")
    ap.add_argument("--tf", default="5", help="تایم‌فریم به دقیقه (1/5/15/60/240)")
    ap.add_argument("--source", choices=["binance", "csv", "thetruetrade"], default="binance")
    ap.add_argument("--csv", help="فایل OHLCV (ستون‌ها: time,open,high,low,close[,volume])")
    ap.add_argument("--bars", type=int, default=1500, help="تعداد کندل (binance)")
    ap.add_argument("--out-dir", default="parity_logs")
    ap.add_argument("--verbose-bars", action="store_true", help="همه‌ی مقادیر را برای «هر» کندل در لاگ بریز (پیش‌فرض: فقط رویدادها)")
    ap.add_argument("--verify-last", type=int, default=2, help="تعداد آخرین کندل‌ها برای تأیید با wrapper واقعی")
    ap.add_argument("--verify-signals", type=int, default=3, help="تعداد آخرین کندل‌های سیگنال برای تأیید")
    ap.add_argument("--use-pine-lookup", action="store_true",
                    help="⚠️ خواندن HL/trend از لاگ Pine (تطابق را کاذب می‌کند؛ فقط برای شبیه‌سازی بک‌تست)")
    ap.add_argument("--pine-hl-log", help="مسیر لاگ Pine (فقط با --use-pine-lookup)")
    ap.add_argument("--pine-csv", help="خروجی CSV تریدینگ‌ویو برای مقایسه")
    ap.add_argument("--pine-shift-bars", type=int, default=0, help="جابه‌جایی ردیف‌های Pine به‌تعداد کندل (مثلاً offset=-rightBars در plotshape)")
    ap.add_argument("--tol", type=float, default=1e-8)
    ap.add_argument("--na-as-zero", action="store_true", help="در مقایسه، خالی/NaN را برابر ۰ بگیر (برای plotshape)")
    ap.add_argument("--max-show", type=int, default=10)
    ap.add_argument("--compare-only", help="فقط مقایسه‌ی یک *_bars.csv قبلی با --pine-csv (بدون اجرای استراتژی)")
    ap.add_argument("--quiet", action="store_true", help="روی کنسول فقط WARNING به بالا")
    ap.add_argument("--console-all", action="store_true", help="همه‌ی لاگ‌ها (هر کندل) روی کنسول هم چاپ شود")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    symbol, tf = args.symbol.upper(), str(args.tf)
    prefix = f"{symbol}_{tf}m"

    if args.compare_only:
        if not args.pine_csv:
            raise SystemExit("--compare-only نیاز به --pine-csv دارد")
        with open(args.compare_only, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        sys.exit(compare_with_pine(rows, args.pine_csv, tf, out_dir, args.tol, args.pine_shift_bars, args.na_as_zero, args.max_show))

    setup_logging(out_dir, prefix, logging.WARNING if args.quiet else logging.INFO, args.console_all)
    t0 = time.time()

    # ── کنترل pine_hl_lookup: پیش‌فرض خاموش تا تطابق «واقعی» سنجیده شود ──
    for k in ("PINE_HL_LOG", "PINE_HL_TREND_LOG"):
        if not args.use_pine_lookup:
            os.environ.pop(k, None)
    if args.use_pine_lookup:
        if not args.pine_hl_log:
            raise SystemExit("--use-pine-lookup نیاز به --pine-hl-log دارد")
        os.environ["PINE_HL_LOG"] = args.pine_hl_log
    try:
        import pine_hl_lookup as PHL
        PHL.PINE_HL_LOOKUP.clear()
        PHL.TREND_LOOKUP.clear()
    except Exception:
        PHL = None

    W = _W()
    W._send_telegram = lambda text: (log.warning("[TELEGRAM-SUPPRESSED] " + str(text).replace("\n", " ⏎ ")[:600]) or False)

    # ── محیط ──
    log.info("═" * 100)
    log.info("DTM PARITY LOGGER — اجرای خالص DTM (بدون فیلتر CT / بدون سفارش / بدون تلگرام)")
    log.info(f"زمان اجرا (UTC): {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')} | symbol={symbol} tf={tf}m | python={sys.version.split()[0]}")
    try:
        from importlib.metadata import version
        log.info(f"PyneCore: {version('pynesys-pynecore')}")
    except Exception:
        log.info("PyneCore: نسخه قابل تشخیص نیست")
    log.info(f"strategy.py        : {W.STRATEGY_PATH} sha256={sha256_file(W.STRATEGY_PATH)}")
    log.info(f"strategy_wrapper.py: {W.__file__} sha256={sha256_file(W.__file__)}")
    log.info(f"ثابت‌های wrapper: MIN_RR={W.MIN_RR} HIST_TOLERANCE={W.HIST_TOLERANCE} STOP_SEARCH_WINDOW={W.STOP_SEARCH_WINDOW} "
             f"STOP_PIVOT_LEFT/RIGHT={W.STOP_PIVOT_LEFT}/{W.STOP_PIVOT_RIGHT} PER_SYMBOL_BLACKLIST={W.PER_SYMBOL_BLACKLIST}")
    log.info(f"tick_info[{symbol}]: {W.SYMBOL_TICK_INFO.get(symbol, 'پیش‌فرض 0.01')} | buffer_ticks={buffer_ticks_for(symbol)}")
    if args.use_pine_lookup:
        log.warning("‼‼ pine_hl_lookup فعال است: HL و trend از لاگ Pine خوانده می‌شود ⇒ تطابق مستقل نیست ‼‼")
    else:
        log.info("pine_hl_lookup: خاموش (محاسبه‌ی خالص پایتون)")

    # ── داده ──
    if args.source == "csv":
        if not args.csv:
            raise SystemExit("--source csv نیاز به --csv دارد")
        df = load_csv(args.csv)
    elif args.source == "binance":
        df = load_binance(symbol, tf, args.bars)
    else:
        df = load_thetruetrade(symbol, tf)
    if df is None or len(df) == 0:
        raise SystemExit("داده‌ای دریافت نشد")
    log.info(f"داده: منبع={args.source} کندل={len(df)} اول={df.index[0]} آخر={df.index[-1]} sha256={fingerprint(df)}")
    df_out = df.copy()
    df_out.insert(0, "time", [int(t.timestamp()) for t in df.index])
    df_out.to_csv(out_dir / f"{prefix}_ohlcv.csv", index=False)

    # ── اجرای اصلی (calculate_signals واقعی + ضبط) ──
    restore = install_runner_proxy()
    try:
        log.info("─" * 100)
        log.info("اجرای strategy_wrapper.calculate_signals واقعی (لاگ‌های خود wrapper/strategy در ادامه می‌آیند)")
        ret, cap = run_wrapper_captured(df, symbol, tf)
        if not cap.results:
            raise SystemExit("هیچ نتیجه‌ای از ScriptRunner ضبط نشد (wrapper زود برگشت یا ساختار آن تغییر کرده)")
        log.info(f"خروجی واقعی calculate_signals (کندل آخر): signal={ret[0]} entry={ret[1]} stop={ret[2]} target={ret[3]} "
                 f"signal_bar_ts_ms={ret[4]} ({ts_str(ret[4]) if ret[4] else '—'}) risk_free_pct={ret[5]}")
        log.info("ورودی‌های استراتژی (inputs):\n" + json.dumps(cap.inputs, ensure_ascii=False, indent=2, default=str))
        log.info(f"last_bar_index={cap.last_bar_index} | کندل‌های داده‌شده به استراتژی={len(cap.candles)} | نتایج={len(cap.results)}")

        log.info("─" * 100)
        log.info("پردازش کندل‌به‌کندل (استراتژی + مراحل wrapper)")
        rows, signals, ctx = process_capture(cap, symbol, args.verbose_bars)
        write_rows_csv(out_dir / f"{prefix}_bars.csv", rows)
        with open(out_dir / f"{prefix}_signals.csv", "w", encoding="utf-8", newline="") as f:
            cols = ["i", "ts_ms", "time", "signal", "kind", "entry", "stop", "target", "rr", "risk_free_pct"]
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for s in signals:
                w.writerow({k: fnum(s[k]) for k in cols})

        problems = 0
        if args.verify_last or args.verify_signals:
            problems = verify_with_real_wrapper(df, symbol, tf, rows, signals, args.verify_last, args.verify_signals)
    finally:
        restore()

    # ── خلاصه ──
    log.info("═" * 100)
    log.info("خلاصه")
    log.info(f"کندل‌های پردازش‌شده={len(rows)} | کندل با نتیجه‌ی خالی={sum(1 for r in rows if r.get('valid') == 'false')}")
    raw = sum(1 for r in rows if r.get("py_signal_raw"))
    log.info(f"سیگنال خام استراتژی={raw} | حذف‌شده با checkColorChange={sum(1 for r in rows if r.get('py_parity_filtered') == 'true')} | "
             f"حذف‌شده با فیلتر E={sum(1 for r in rows if r.get('py_filterE') == 'true')} | "
             f"crash در wrapper (stop/target/rr=None)={sum(1 for r in rows if r.get('py_wrapper_crash') == 'true')} | نهایی={len(signals)}")
    for s in signals[-20:]:
        log.info(f"  {s['time']} {s['signal']:<5} {s['kind']} entry={s['entry']!r} stop={s['stop']!r} target={s['target']!r} rr={s['rr']!r}")
    if PHL is not None:
        log.info(f"آمار pine_hl_lookup: {PHL.STATS} | HL={PHL.size()} trend={PHL.trend_size()}")
        if not args.use_pine_lookup and (PHL.size() or PHL.trend_size()):
            log.warning("‼ lookup در حالت خاموش هم داده دارد؟ تطابق را معتبر ندانید")
    log.info(f"مدت اجرا: {time.time() - t0:.1f}s | خروجی‌ها در: {out_dir.resolve()}")
    print(f"\n✅ پایان. فایل‌ها در {out_dir.resolve()} با پیشوند {prefix}_*")

    rc = 2 if problems else 0
    if args.pine_csv:
        rc = max(rc, compare_with_pine(rows, args.pine_csv, tf, out_dir, args.tol, args.pine_shift_bars, args.na_as_zero, args.max_show))
    sys.exit(rc)


if __name__ == "__main__":
    main()
