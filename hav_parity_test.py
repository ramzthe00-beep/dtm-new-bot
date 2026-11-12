"""
hav_parity_test.py — مقایسه‌ی پایتون با لاگ واقعی TradingView (اسکریپت پاین همراه با Parity Log)
===========================================================================================
استفاده:
    python hav_parity_test.py pine_log.txt                # لاگ‌های Pine Logs را در یک فایل متنی ذخیره کنید
    python hav_parity_test.py pine_log.txt --skip 800     # چند کندل اول پنجره را برای «گرم شدن» نادیده می‌گیرد
    python hav_parity_test.py --roundtrip                 # تست خودِ ابزار (بدون TradingView)

روش:
  • BARS = OHLC و ATR واقعیِ خود TradingView → پایتون روی همان داده اجرا می‌شود (اختلاف منبع داده حذف می‌شود)
  • ATR کندل اول پنجره از لاگ به‌عنوان seed داده می‌شود (RMA از آنجا دقیقاً ادامه پیدا می‌کند)
  • بافر پیوت و patterns_active (برای تشخیص تکراری) از ابتدای پنجره ساخته می‌شوند، پس مقایسه از
    `skip` کندل بعد از شروع پنجره آغاز می‌شود (پیش‌فرض ۸۰۰) تا حافظه‌ی قبل از پنجره خالی شود.
  • مقایسه: PIV, SCAN, DUP, WIN (وضعیت و نسبت‌ها), PRZ, SCORE, WINNER, FIRE
"""
import argparse
import math
import os
import re
import sys
import tempfile

from hav_strategy import HavConfig, run_hav, ORDER, LOG_KEY, PRZ_LOG_NAME

TOL_ABS, TOL_REL = 2e-9, 1e-9
KINDS = ("CFG", "BARS", "PIV", "SCAN", "DUP", "WIN", "PRZ", "SCORE", "WINNER", "FIRE")
LINE_RE = re.compile(r"(" + "|".join(KINDS) + r")\|(.*)$")


# ───────────────────────── قالب‌بندی (مثل f_fx در پاین) ─────────────────────────
def fx(x):
    if x is None or x != x:
        return "NaN"
    s = f"{x:.10f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def close(a, b):
    if a != a and b != b:
        return True
    if a != a or b != b:
        return False
    return abs(a - b) <= TOL_ABS + TOL_REL * abs(b)


# ───────────────────────── تولید لاگ از خروجی پایتون (برای تست خودِ ابزار) ─────────────────────────
def format_log(res, bars, cfg, tf="15", typ="crypto", from_bar=0):
    """bars: لیست (bar, time, o, h, l, c, atr). خطوط با همان قالب اسکریپت پاین."""
    out = [f"CFG|tf={tf}|type={typ}|len={cfg.length}|uselog={int(cfg.use_log)}|preset={cfg.preset}|minxa={fx(cfg.min_xa_atr)}"
           f"|atrp={cfg.atr_period}|minscore={int(cfg.min_score)}|minconf={cfg.min_conf}|penal={int(cfg.penalize_no_abcd)}"
           f"|border={int(cfg.show_borderline)}|bmin={fx(cfg.borderline_min_score)}|alertmin={fx(cfg.alert_min_score)}"
           f"|alerts={int(cfg.enable_alerts)}|maxact={cfg.max_active}|forming={int(cfg.forming)}"
           f"|scan={''.join(str(int(x)) for x in cfg.scan)}"]
    chunk = []
    for b in bars:
        chunk.append(",".join([str(b[0]), str(b[1]), fx(b[2]), fx(b[3]), fx(b[4]), fx(b[5]), fx(b[6])]))
        if len(chunk) == 12:
            out.append("BARS|" + ";".join(chunk) + ";"); chunk = []
    if chunk:
        out.append("BARS|" + ";".join(chunk) + ";")
    for e in res["events"]:
        if e["bar"] < from_bar:
            continue
        k = e["kind"]
        if k == "PIV":
            buf = "".join(f"{t}:{bi}:{fx(p)}:{'H' if h else 'L'};" for t, bi, p, h in e["buf"])
            out.append(f"PIV|bar={e['bar']}|ph={fx(e['ph'])}|pl={fx(e['pl'])}|new={int(e['new'])}|n={e['n']}|buf={buf}")
        elif k == "SCAN":
            out.append(f"SCAN|bar={e['bar']}|n={e['n']}|atr={fx(e['atr'])}")
        elif k == "DUP":
            out.append(f"DUP|bar={e['bar']}|start={e['start']}")
        elif k == "WIN":
            parts = "".join(f"|{LOG_KEY[p]}={e[LOG_KEY[p]][0]},{fx(e[LOG_KEY[p]][2])},{fx(e[LOG_KEY[p]][3])},"
                            f"{fx(e[LOG_KEY[p]][4])},{fx(e[LOG_KEY[p]][5])}" for p in ORDER)
            out.append(f"WIN|bar={e['bar']}|start={e['start']}|tX={e['tX']}|tA={e['tA']}|tB={e['tB']}|tC={e['tC']}|tD={e['tD']}" + parts)
        elif k == "PRZ":
            pr = "".join(f"{lab}:{fx(px)}:{int(i)}," for lab, px, i in e["projs"])
            out.append(f"PRZ|bar={e['bar']}|start={e['start']}|pat={e['pat']}|abcd={int(e['abcd'])}|{fx(e['top'])}|{fx(e['bot'])}|{e['conf']}|{pr}")
        elif k == "SCORE":
            out.append(f"SCORE|bar={e['bar']}|start={e['start']}|pat={e['pat']}|score={fx(e['score'])}|elig={int(e['elig'])}")
        elif k == "WINNER":
            out.append(f"WINNER|bar={e['bar']}|start={e['start']}|pat={e['pat']}|state={e['state']}|score={fx(e['score'])}"
                       f"|bull={int(e['bull'])}|abcd={int(e['abcd'])}|tX={e['tX']}|tD={e['tD']}")
        elif k == "FIRE":
            out.append(f"FIRE|bar={e['bar']}|pat={e['pat']}|score={fx(e['score'])}")
    return "\n".join(out)


# ───────────────────────── پارس لاگ ─────────────────────────
def _kv(payload):
    d = {}
    for part in payload.split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k] = v
    return d


def parse_log(text):
    cfg, bars, ev = None, [], []
    for raw in text.splitlines():
        m = LINE_RE.search(raw)
        if not m:
            continue
        kind, pl = m.group(1), m.group(2).strip()
        if kind == "CFG":
            cfg = _kv(pl)
        elif kind == "BARS":
            for item in pl.split(";"):
                if item.strip():
                    p = item.split(",")
                    bars.append((int(p[0]), int(p[1]), float(p[2]), float(p[3]), float(p[4]), float(p[5]), float(p[6])))
        elif kind == "PIV":
            d = _kv(pl)
            buf = []
            for q in d.get("buf", "").split(";"):
                if q.strip():
                    t, bi, px, hl = q.split(":")
                    buf.append((int(t), int(bi), float(px), hl == "H"))
            ev.append({"kind": "PIV", "bar": int(d["bar"]), "ph": float(d["ph"]), "pl": float(d["pl"]),
                       "new": d["new"] == "1", "n": int(d["n"]), "buf": buf})
        elif kind == "SCAN":
            d = _kv(pl)
            ev.append({"kind": "SCAN", "bar": int(d["bar"]), "n": int(d["n"]), "atr": float(d["atr"])})
        elif kind == "DUP":
            d = _kv(pl)
            ev.append({"kind": "DUP", "bar": int(d["bar"]), "start": int(d["start"])})
        elif kind == "WIN":
            d = _kv(pl)
            e = {"kind": "WIN", "bar": int(d["bar"]), "start": int(d["start"])}
            for k in ("tX", "tA", "tB", "tC", "tD"):
                e[k] = int(d[k])
            for p in ORDER:
                s = d[LOG_KEY[p]].split(",")
                e[LOG_KEY[p]] = (int(s[0]), None, float(s[1]), float(s[2]), float(s[3]), float(s[4]))
            ev.append(e)
        elif kind == "PRZ":
            parts = pl.split("|")
            d = _kv("|".join(parts[:4]))
            projs = []
            for q in parts[7].split(","):
                if q.strip():
                    lab, px, i = q.rsplit(":", 2)
                    projs.append((lab, float(px), i == "1"))
            ev.append({"kind": "PRZ", "bar": int(d["bar"]), "start": int(d["start"]), "pat": d["pat"],
                       "abcd": d["abcd"] == "1", "top": float(parts[4]), "bot": float(parts[5]),
                       "conf": int(parts[6]), "projs": projs})
        elif kind == "SCORE":
            d = _kv(pl)
            ev.append({"kind": "SCORE", "bar": int(d["bar"]), "start": int(d["start"]), "pat": d["pat"],
                       "score": float(d["score"]), "elig": d["elig"] == "1"})
        elif kind == "WINNER":
            d = _kv(pl)
            ev.append({"kind": "WINNER", "bar": int(d["bar"]), "start": int(d["start"]), "pat": d["pat"],
                       "state": d["state"], "score": float(d["score"]), "bull": d["bull"] == "1",
                       "abcd": d["abcd"] == "1", "tX": int(d["tX"]), "tD": int(d["tD"])})
        elif kind == "FIRE":
            d = _kv(pl)
            ev.append({"kind": "FIRE", "bar": int(d["bar"]), "pat": d["pat"], "score": float(d["score"])})
    return cfg, bars, ev


def cfg_from_log(c):
    scan = tuple(ch == "1" for ch in c.get("scan", "111111"))
    return HavConfig(length=int(c["len"]), use_log=c["uselog"] == "1", preset=c["preset"],
                     min_xa_atr=float(c["minxa"]), atr_period=int(c["atrp"]), min_score=float(c["minscore"]),
                     min_conf=int(c["minconf"]), penalize_no_abcd=c["penal"] == "1",
                     show_borderline=c["border"] == "1", borderline_min_score=float(c["bmin"]),
                     enable_alerts=c["alerts"] == "1", alert_min_score=float(c["alertmin"]),
                     max_active=int(c["maxact"]), forming=c["forming"] == "1", scan=scan)


# ───────────────────────── مقایسه ─────────────────────────
def key_of(e):
    k = e["kind"]
    if k in ("PIV", "SCAN"):
        return (k, e["bar"])
    if k in ("DUP", "WIN", "WINNER"):
        return (k, e["bar"], e["start"])
    if k in ("PRZ", "SCORE"):
        return (k, e["bar"], e["start"], e["pat"])
    return (k, e["bar"], e["pat"])


def diff_event(a, b):
    """a=پایتون، b=Pine → لیست اختلاف‌ها."""
    k, bad = a["kind"], []

    def chk(name, x, y, num=False):
        ok = close(x, y) if num else x == y
        if not ok:
            bad.append(f"{name}: py={x} pine={y}")

    if k == "PIV":
        chk("ph", a["ph"] if a["ph"] is not None else float("nan"), b["ph"], True)
        chk("pl", a["pl"] if a["pl"] is not None else float("nan"), b["pl"], True)
        chk("new", a["new"], b["new"]); chk("n", a["n"], b["n"])
        if len(a["buf"]) != len(b["buf"]):
            bad.append(f"buf len py={len(a['buf'])} pine={len(b['buf'])}")
        else:
            for i, (x, y) in enumerate(zip(a["buf"], b["buf"])):
                if x[0] != y[0] or x[1] != y[1] or x[3] != y[3] or not close(x[2], y[2]):
                    bad.append(f"buf[{i}] py={x} pine={y}")
    elif k == "SCAN":
        chk("n", a["n"], b["n"]); chk("atr", a["atr"], b["atr"], True)
    elif k == "WIN":
        for f in ("tX", "tA", "tB", "tC", "tD"):
            chk(f, a[f], b[f])
        for p in ORDER:
            x, y = a[LOG_KEY[p]], b[LOG_KEY[p]]
            chk(f"{LOG_KEY[p]}.status", x[0], y[0])
            for j, nm in ((2, "rAB"), (3, "rBC"), (4, "rCD"), (5, "rXD")):
                chk(f"{LOG_KEY[p]}.{nm}", x[j], y[j], True)
    elif k == "PRZ":
        chk("abcd", a["abcd"], b["abcd"]); chk("conf", a["conf"], b["conf"])
        chk("top", a["top"], b["top"], True); chk("bot", a["bot"], b["bot"], True)
        if len(a["projs"]) != len(b["projs"]):
            bad.append("projs len")
        else:
            for x, y in zip(a["projs"], b["projs"]):
                if x[0] != y[0] or x[2] != y[2] or not close(x[1], y[1]):
                    bad.append(f"proj py={x} pine={y}")
    elif k == "SCORE":
        chk("score", a["score"], b["score"], True); chk("elig", a["elig"], b["elig"])
    elif k == "WINNER":
        for f in ("state", "bull", "abcd", "tX", "tD"):
            chk(f, a[f], b[f])
        chk("score", a["score"], b["score"], True)
    elif k == "FIRE":
        chk("score", a["score"], b["score"], True)
    return bad


def compare(text, skip=800, verbose=10):
    cfg_d, bars, pine_ev = parse_log(text)
    if cfg_d is None or not bars:
        sys.exit("CFG/BARS در لاگ پیدا نشد؛ لاگ ناقص است (احتمالاً ۱۰٬۰۰۰ خطِ اول پنل Logs پریده است).")
    bars.sort()
    for i in range(1, len(bars)):
        if bars[i][0] != bars[i - 1][0] + 1:
            sys.exit(f"BARS پیوسته نیست (bar {bars[i - 1][0]} → {bars[i][0]}). بازه‌ی لاگ را کوتاه‌تر کنید.")
    cfg = cfg_from_log(cfg_d)
    b0 = bars[0][0]
    o, h, l, c, t = ([b[k] for b in bars] for k in (2, 3, 4, 5, 1))
    res = run_hav(o, h, l, c, t, cfg, atr_seed=bars[0][6], bi0=b0)

    # ATR
    worst = max((abs(res["atr"][i] - bars[i][6]) for i in range(len(bars))), default=0.0)
    print(f"ATR: بیشترین اختلاف پایتون و TradingView = {worst:.3e}")

    lo = b0 + skip
    hi = bars[-1][0]
    py = {key_of(e): e for e in res["events"] if lo <= e["bar"] <= hi}
    pi = {key_of(e): e for e in pine_ev if lo <= e["bar"] <= hi}
    missing = sorted(set(pi) - set(py))      # در Pine هست، در پایتون نیست
    extra = sorted(set(py) - set(pi))        # در پایتون هست، در Pine نیست
    bad_fields = []
    for k in sorted(set(py) & set(pi)):
        d = diff_event(py[k], pi[k])
        if d:
            bad_fields.append((k, d))

    from collections import Counter
    cnt = Counter(k[0] for k in pi)
    print(f"بازه‌ی مقایسه: bar {lo} … {hi} (skip={skip}) | رویدادهای Pine: {dict(cnt)}")
    print(f"کم در پایتون: {len(missing)} | اضافه در پایتون: {len(extra)} | اختلاف فیلد: {len(bad_fields)}")
    for k in missing[:verbose]:
        print("  MISSING(py):", k)
    for k in extra[:verbose]:
        print("  EXTRA(py):  ", k)
    for k, d in bad_fields[:verbose]:
        print("  DIFF:", k, "→", "; ".join(d[:4]))
    ok = not (missing or extra or bad_fields) and worst < 1e-6
    print("نتیجه:", "✅ تطابق ۱۰۰٪" if ok else "❌ اختلاف وجود دارد")
    return ok


# ───────────────────────── تست خودِ ابزار ─────────────────────────
def roundtrip():
    import random
    rnd = random.Random(11)
    p, O, H, L, C, T = 100.0, [], [], [], [], []
    for i in range(7000):
        o_ = p
        c_ = o_ * (1 + rnd.gauss(0, 0.004))
        h_ = max(o_, c_) * (1 + abs(rnd.gauss(0, 0.002)))
        l_ = min(o_, c_) * (1 - abs(rnd.gauss(0, 0.002)))
        O.append(o_); H.append(h_); L.append(l_); C.append(c_); T.append(1_700_000_000_000 + i * 900_000); p = c_
    for preset, border in (("Standard", False), ("Lenient", True)):
        cfg = HavConfig(length=5, preset=preset, show_borderline=border)
        full = run_hav(O, H, L, C, T, cfg)                      # «چارت» کامل (از اول)
        w0 = 2500                                              # پنجره‌ی لاگ از کندل ۲۵۰۰ شروع می‌شود
        bars = [(i, T[i], O[i], H[i], L[i], C[i], full["atr"][i]) for i in range(w0, len(C))]
        text = format_log(full, bars, cfg, from_bar=w0)
        ok = compare(text, skip=800)
        n_win = sum(1 for e in full["events"] if e["kind"] == "WINNER" and e["bar"] >= w0 + 800)
        print(f"[{preset}] WINNER در بازه‌ی مقایسه: {n_win}\n")
        assert ok
    print("roundtrip OK (این تست فقط درستی خودِ ابزار را نشان می‌دهد، نه تطابق با TradingView)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("log", nargs="?")
    ap.add_argument("--skip", type=int, default=800)
    ap.add_argument("--roundtrip", action="store_true")
    a = ap.parse_args()
    if a.roundtrip:
        roundtrip()
    elif a.log:
        sys.exit(0 if compare(open(a.log, encoding="utf-8").read(), a.skip) else 1)
    else:
        ap.print_help()
