"""
sfp_parity_test.py — تست تطابق دوجهته: پایتون (sfp_strategy.py) در برابر لاگ Pine (CSV)
اجرا:  python3 sfp_parity_test.py "pine-logs-_اردر_.csv" SYMBOL
  (SYMBOL = همان نمادی که روی TradingView بوده؛ مثلاً LTCUSDT)
- کندل‌ها از Binance از 'اولین کندل چارت' (بار 0) تا آخرین بار لاگ گرفته می‌شود.
- قبل از مقایسه، OHLC داخل لاگ‌ها با کندل‌های دریافتی چک می‌شود تا منبع داده تأیید شود.
"""
import csv, re, sys, time, collections
import requests
from sfp_strategy import run_sfp

TOL = 1e-9


def num(x):
    return None if x == "na" else float(x)


def parse_state(s):
    g = re.search(r"swing=(\S+)@(\S+) oppos=(\S+)@(\S+) act=(\w+) conf=(\w+)", s)
    f = lambda v: None if v == "na" else int(v)
    return {"swing_prc": num(g[1]), "swing_bix": f(g[2]), "oppos_prc": num(g[3]),
            "oppos_bix": f(g[4]), "active": g[5] == "true", "confirmed": g[6] == "true"}


def parse_csv(path):
    rows = list(csv.reader(open(path, encoding="utf-8")))[1:]
    ev, ohlc, start_ms = [], {}, None
    for _, m in rows:
        kind = re.match(r"\[SFP_(\w+)\]", m)
        if not kind:
            continue
        k = kind[1]
        bar = int(re.search(r" bar=(\d+)", m)[1])
        ms = int(re.search(r" ms=(\d+)", m)[1])
        if start_ms is None:
            start_ms = ms - bar * 60000
        g = re.search(r" O=(\S+) H=(\S+) L=(\S+) C=(\S+) conf", m)
        if g:
            ohlc[bar] = tuple(float(g[i]) for i in range(1, 5))
        e = {"kind": k, "bar": bar}
        if k.startswith("PIV"):
            e["value"] = float(re.search(r"pivot(?:High|Low)=(\S+)", m)[1])
            e["pivotBar"] = int(re.search(r"pivotBar=(\d+)", m)[1])
            e["tieLeft"] = re.search(r"tieLeft=(\w+)", m)[1] == "true"
            e["tieRight"] = re.search(r"tieRight=(\w+)", m)[1] == "true"
            pv = re.search(r"prevSwing[HL]=(\S+)@(\S+)", m)
            e["prevSwing"] = (None if pv[2] == "na" else int(pv[2]), num(pv[1]))
        elif k.startswith("CHK"):
            sw = re.search(r"sw=(\S+)@(\S+) newPivThisBar=(\w+)", m)
            e.update(sw=float(sw[1]), bx=int(sw[2]), newPivThisBar=sw[3] == "true")
            fl = re.search(r"c1\(.*?\)=(\w+) c2\(.*?\)=(\w+) c3\(.*?\)=(\w+) => (\w+)", m)
            e.update(c1=fl[1] == "true", c2=fl[2] == "true", c3=fl[3] == "true", decision=fl[4])
        elif k.startswith("HIT"):
            sc = re.search(r"SCAN: from=1 to=(-?\d+) descending=(\w+) iters=(\d+) firstI=(\S+) lastI=(\S+) updates:(.*?)\| RESULT opposH?L?=(\S+)@(\d+)", m, re.S)
            fi = lambda v: None if v == "na" else int(v)
            e.update(loopTo=int(sc[1]), descending=sc[2] == "true", iters=int(sc[3]),
                     firstI=fi(sc[4]), lastI=fi(sc[5]),
                     updates=[(int(a), float(b), int(c)) for a, b, c in
                              re.findall(r"\[i=(\d+) (?:low|high)=(\S+) ->oppos@(\d+)\]", sc[6])],
                     oppos=float(sc[7]), opposBar=int(sc[8]))
            e["prev"] = parse_state(re.search(r"prevPiv[HL]: (.*?) deleted", m, re.S)[1])
            e["new"] = parse_state(re.search(r"newPiv[HL] : (.*)", m)[1])
            e["deletedPrev"] = re.search(r"deletedPrevDrawings=(\w+)", m)[1] == "true"
            sw = re.search(r"sw=(\S+)@(\d+) \| SCAN", m)
            e.update(sw=float(sw[1]), bx=int(sw[2]))
        elif k.startswith("CONF"):
            if "CONFIRMED" not in m:
                continue
            e["oppos"] = float(re.search(r"oppos=(\S+)@", m)[1])
            e["age"] = int(re.search(r"age=(\d+)", m)[1])
        elif k.startswith("CANCEL"):
            e["ageExpired"] = re.search(r"ageExpired\(>500\)=(\w+)", m)[1] == "true"
            e["crossed"] = re.search(r"close[<>]swing=(\w+)", m)[1] == "true"
            e["state"] = parse_state(m.split(" | ")[-1])
        ev.append(e)
    return ev, ohlc, start_ms


def fetch(symbol, start_ms, n_bars):
    out, cur = [], start_ms
    end_ms = start_ms + n_bars * 60000
    while cur < end_ms:
        r = requests.get("https://data-api.binance.vision/api/v3/klines",
                         params={"symbol": symbol, "interval": "1m", "startTime": cur,
                                 "endTime": end_ms, "limit": 1000}, timeout=20)
        r.raise_for_status()
        d = r.json()
        if not d:
            break
        out += d
        cur = int(d[-1][0]) + 60000
        time.sleep(0.2)
    return out


def close_(a, b):
    if isinstance(a, dict):
        return all(close_(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(close_(x, y) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        return a is not None and b is not None and abs(a - b) <= TOL
    return a == b


def key(e):
    return (e["kind"], e["bar"])


def main():
    path = sys.argv[1]
    symbol = sys.argv[2] if len(sys.argv) > 2 else "LTCUSDT"
    pine, ohlc, start_ms = parse_csv(path)
    last_bar = max(ohlc) if ohlc else max(e["bar"] for e in pine)
    last_bar = max(last_bar, max(e["bar"] for e in pine))
    print(f"Pine events: {len(pine)} | start_ms={start_ms} | last_bar={last_bar}")

    kl = fetch(symbol, start_ms, last_bar + 1)
    kl = kl[:last_bar + 1]
    print(f"candles fetched: {len(kl)} (needed {last_bar + 1}) first_ts={kl[0][0]} (expected {start_ms})")
    if int(kl[0][0]) != start_ms or len(kl) < last_bar + 1:
        sys.exit("❌ شروع/تعداد کندل‌ها با چارت Pine نمی‌خواند (نماد یا بازه را چک کنید)")
    o = [float(k[1]) for k in kl]; h = [float(k[2]) for k in kl]
    l = [float(k[3]) for k in kl]; c = [float(k[4]) for k in kl]

    # ۱) اعتبارسنجی منبع داده با OHLCِ داخل لاگ‌ها
    bad = [(b, v, (o[b], h[b], l[b], c[b])) for b, v in ohlc.items()
           if any(abs(x - y) > 1e-9 for x, y in zip(v, (o[b], h[b], l[b], c[b])))]
    print(f"OHLC check: {len(ohlc) - len(bad)}/{len(ohlc)} match")
    for b in bad[:5]:
        print("   ✗ OHLC mismatch bar", b[0], "pine", b[1], "binance", b[2])
    if len(bad) > 0.01 * max(len(ohlc), 1):
        print("⚠️ منبع داده با TradingView یکی نیست؛ نتیجهٔ مقایسه معتبر نیست.")

    # ۲) اجرای پایتون و مقایسهٔ دوجهته
    py = run_sfp(o, h, l, c)
    pine_d = collections.defaultdict(list); py_d = collections.defaultdict(list)
    for e in pine: pine_d[key(e)].append(e)
    for e in py:
        if e["kind"].startswith("CONF") and e.get("pending"):
            continue
        py_d[key(e)].append(e)
    kinds = sorted({k[0] for k in pine_d} | {k[0] for k in py_d})
    total_bad = 0
    print("\n== مقایسه به تفکیک نوع رویداد ==")
    for kd in kinds:
        P = {k for k in pine_d if k[0] == kd}; Y = {k for k in py_d if k[0] == kd}
        miss = sorted(P - Y); extra = sorted(Y - P); common = sorted(P & Y)
        field_bad = []
        for k in common:
            a, b = pine_d[k][0], py_d[k][0]
            diff = [f for f in a if f not in ("kind", "bar") and f in b and not close_(a[f], b[f])]
            if diff:
                field_bad.append((k, diff))
        total_bad += len(miss) + len(extra) + len(field_bad)
        print(f"{kd:10s} pine={len(P):5d} py={len(Y):5d} common={len(common):5d} "
              f"MISSED(pine has, py not)={len(miss)} EXTRA(py has, pine not)={len(extra)} fieldDiff={len(field_bad)}")
        for k in miss[:5]: print("    MISSED", k)
        for k in extra[:5]: print("    EXTRA ", k)
        for k, d in field_bad[:5]: print("    DIFF  ", k, d)
    print("\nنتیجه:", "🎉 تطابق ۱۰۰٪" if total_bad == 0 else f"⚠️ {total_bad} اختلاف")


if __name__ == "__main__":
    main()
