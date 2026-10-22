"""تست: run_fvg_std در برابر فرمول‌بندی مستقلِ «به‌ازای هر زون» (طول عمر هر زون جداگانه شبیه‌سازی می‌شود)."""
import random
from fvg_standard import run_fvg_std, MODES


def gen(n, seed, vol):
    rnd = random.Random(seed); p = 100.0; O, H, L, C = [], [], [], []
    for _ in range(n):
        o = p; c = o + rnd.gauss(0, vol)
        h = max(o, c) + abs(rnd.gauss(0, vol / 2)); l = min(o, c) - abs(rnd.gauss(0, vol / 2))
        O.append(o); H.append(h); L.append(l); C.append(c); p = c
    return O, H, L, C


def independent(o, h, l, c, mode, min_gap, max_age, show_retest):
    n = len(c); formed, ret, open_z, mit, exp = [], set(), [], [], []
    for i in range(2, n):
        if l[i] > h[i-2] and (l[i] - h[i-2]) / h[i-2] * 100 >= min_gap:
            bull, top, bot = True, l[i], h[i-2]
        elif h[i] < l[i-2] and (l[i-2] - h[i]) / l[i-2] * 100 >= min_gap:
            bull, top, bot = False, l[i-2], h[i]
        else:
            continue
        formed.append((i, "BULL" if bull else "BEAR"))
        touched, end = False, None
        for k in range(i + 1, n):
            if k - i > max_age:
                exp.append((i, k, bull)); end = k; break
            entered = (l[k] <= top) if bull else (h[k] >= bot)
            if entered and not touched:
                touched = True
                if show_retest and ((bull and c[k] > top) or ((not bull) and c[k] < bot)):
                    ret.add((k, "BULL" if bull else "BEAR"))
            mid = (top + bot) / 2
            hit = {"wick": (l[k] <= bot) if bull else (h[k] >= top),
                   "close": (c[k] < bot) if bull else (c[k] > top),
                   "touch": entered,
                   "ce": (l[k] <= mid) if bull else (h[k] >= mid)}[mode]
            if hit:
                mit.append((i, k, bull)); end = k; break
        if end is None:
            open_z.append((i, bull))
    return formed, ret, open_z, mit, exp


if __name__ == "__main__":
    n_cases = tot_f = tot_r = tot_e = 0
    for seed in range(120):
        vol = [0.05, 0.3, 1.0][seed % 3]
        o, h, l, c = gen(700, seed, vol)
        for mode in MODES:
            for min_gap, max_age, sr in ((0.0, 300, True), (0.05, 60, True), (0.0, 25, False)):
                r = run_fvg_std(o, h, l, c, mode, min_gap, max_age, sr)
                f, rt, oz, mt, ex = independent(o, h, l, c, mode, min_gap, max_age, sr)
                assert [(s["bar"], s["dir"]) for s in r["formed"]] == f
                assert {(s["bar"], s["dir"]) for s in r["retests"]} == rt
                assert sorted((z["born"], z["bull"]) for z in r["zones"]) == sorted(oz)
                assert sorted((m["born"], m["bar"], m["bull"]) for m in r["mitigated"]) == sorted(mt)
                assert sorted((m["born"], m["bar"], m["bull"]) for m in r["expired"]) == sorted(ex)
                n_cases += 1; tot_f += len(f); tot_r += len(rt); tot_e += len(ex)
    print(f"{n_cases} configurations OK — {tot_f} FVGs, {tot_r} retest signals, {tot_e} expirations identical")
    # مثال دستی
    o = [10, 11, 13, 14, 12, 11]; h = [11, 12, 14, 15, 13, 12]; l = [9, 10, 12, 13, 11, 10]; c = [10.5, 11.5, 13.5, 14.5, 12.5, 11.5]
    r = run_fvg_std(o, h, l, c)
    print("manual formed:", r["formed"], "| retests:", r["retests"], "| open:", [(z['born'], z['bull']) for z in r['zones']])
