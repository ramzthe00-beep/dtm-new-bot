"""hav_selftest.py — تست‌های سلامت منطقی (جایگزین مقایسه با لاگ واقعی نیست؛ آن را hav_parity_test.py انجام می‌دهد)."""
import math, random
from hav_strategy import (HavConfig, run_hav, pine_atr, pine_round, validate, build_prz, _Ctx, Pivot,
                          score, abcd_converges)


def zigzag(points, bars_per_leg=30, noise=0.0, seed=0):
    """OHLC از یک زیگزاگ خطی؛ هر پای zigzag بین نقاط، bars_per_leg کندل."""
    rnd = random.Random(seed)
    closes = []
    for (a, b) in zip(points[:-1], points[1:]):
        for k in range(bars_per_leg):
            closes.append(a + (b - a) * k / bars_per_leg)
    closes.append(points[-1])
    o, h, l, c, t = [], [], [], [], []
    for i, x in enumerate(closes):
        x += rnd.uniform(-noise, noise)
        prev = c[-1] if c else x
        o.append(prev); c.append(x)
        h.append(max(prev, x) + 0.3); l.append(min(prev, x) - 0.3)
        t.append(1_700_000_000_000 + i * 60_000)
    return o, h, l, c, t


# ── ۱) ATR: seed=SMA و بازگشتی RMA ──
h = [10 + i % 3 for i in range(60)]; l = [9 + (i % 3) * 0.5 for i in range(60)]; c = [9.5 + (i % 4) * 0.3 for i in range(60)]
a = pine_atr(h, l, c, 14)
assert all(math.isnan(x) for x in a[:13]) and not math.isnan(a[13])
tr = [h[0] - l[0]] + [max(h[i] - l[i], abs(h[i] - c[i-1]), abs(l[i] - c[i-1])) for i in range(1, 60)]
assert abs(a[13] - sum(tr[:14]) / 14) < 1e-12
assert abs(a[14] - ((1/14) * tr[14] + (1 - 1/14) * a[13])) < 1e-12
aw = pine_atr(h[30:], l[30:], c[30:], 14, seed0=a[30])   # پنجره از وسط چارت، با ATR واقعیِ اولین کندل
assert all(abs(aw[k] - a[30 + k]) < 1e-12 for k in range(30)), "seed باید ATR کامل را بازتولید کند"
print("ATR OK")

# ── ۲) pine_round ──
assert pine_round(2.5) == 3 and pine_round(3.5) == 4 and pine_round(2.4) == 2 and pine_round(0.5) == 1
print("round OK")

# ── ۳) پیوت: چپ تساوی مجاز، راست تساوی غیرمجاز ──
from hav_strategy import run_hav as _r
def pivots_of(hs, ls, L=2):
    n = len(hs); o = c = [(x + y) / 2 for x, y in zip(hs, ls)]; t = list(range(n))
    r = _r(o, hs, ls, c, t, HavConfig(length=L))
    return [(e["bar"], e["ph"], e["pl"]) for e in r["events"] if e["kind"] == "PIV"]
hs = [1, 2, 5, 3, 2, 1, 1, 1, 1]; ls = [x - 0.5 for x in hs]
assert any(ph == 5 for _, ph, _ in pivots_of(hs, ls)), "پیوت واضح باید تشخیص داده شود"
hs_tie_left = [1, 5, 5, 3, 2, 1, 1, 1]; ls = [x - 0.5 for x in hs_tie_left]    # چپ مساوی (۵ و ۵): پیوت روی دومی مجاز
assert any(ph == 5 for _, ph, _ in pivots_of(hs_tie_left, ls))
hs_tie_right = [1, 2, 5, 5, 2, 1, 1, 1]; ls = [x - 0.5 for x in hs_tie_right]  # راست مساوی: پیوت اولی غیرمجاز
got = [bar for bar, ph, _ in pivots_of(hs_tie_right, ls) if ph == 5]
assert len(got) == 1, got            # فقط پیوت دومی (که سمت چپش مساوی است) قبول می‌شود
print("pivot tie rules OK")

# ── ۴) Gartley صعودی ساخته‌شده با نسبت‌های دقیق ──
X, A = 100.0, 200.0
B = A - 0.618 * (A - X)           # 138.2
C = B + 0.5 * (A - B)             # BC = 0.5
D = A - 0.786 * (A - X)           # 121.4
E = 150.0                          # پیوت ششم (تأیید D)
pts = [X + 40, X, A, B, C, D, E, E - 30]
o, h, l, c, t = zigzag([X + 20, X, A, B, C, D, E, E - 25], bars_per_leg=25)
cfg = HavConfig(length=5, min_score=0, min_conf=0, min_xa_atr=0.5)
res = run_hav(o, h, l, c, t, cfg)
wins = [e for e in res["events"] if e["kind"] == "WIN"]
winners = [e for e in res["events"] if e["kind"] == "WINNER"]
print("windows:", len(wins), "| winners:", [(w["pat"], w["state"], w["score"]) for w in winners])
g = [w for w in wins if w["gart"][0] == 0]
assert g, "یک پنجره‌ی Gartley معتبر باید پیدا شود: " + str([w["gart"] for w in wins])
st, bull, rAB, rBC, rCD, rXD = g[0]["gart"]
assert bull and abs(rAB - 0.618) < 0.02 and abs(rXD - 0.786) < 0.03, (rAB, rXD)
print(f"Gartley detected: rAB={rAB:.3f} rBC={rBC:.3f} rCD={rCD:.3f} rXD={rXD:.3f}")

# ── ۵) تشخیص تکراری + FIFO ──
# هر پنجره فقط یک‌بار برنده می‌شود حتی اگر پیوت‌های جدید بیایند
keys = [(w["tX"], w["tD"]) for w in winners]
assert len(keys) == len(set(keys)), "هر (X,D) فقط یک‌بار باید برنده شود"
cfg2 = HavConfig(length=5, min_score=0, min_conf=0, min_xa_atr=0.5, max_active=1)
rnd = random.Random(3)
pp = [100]
for _ in range(80):
    pp.append(pp[-1] + rnd.choice([-1, 1]) * rnd.uniform(20, 60))
o2, h2, l2, c2, t2 = zigzag([max(x, 5) for x in pp], bars_per_leg=12, noise=0.5, seed=1)
r2 = run_hav(o2, h2, l2, c2, t2, cfg2)
assert len(r2["patterns"]) <= 1
print("FIFO OK | random zigzag winners:", sum(1 for e in r2["events"] if e["kind"] == "WINNER"))

# ── ۶) پایداری روی داده‌ی تصادفی بلند (بدون خطا + ساختار eventها) ──
rnd = random.Random(7)
p, O, H, Lo, Cc, T = 100.0, [], [], [], [], []
for i in range(6000):
    o_ = p; c_ = o_ * (1 + rnd.gauss(0, 0.004)); h_ = max(o_, c_) * (1 + abs(rnd.gauss(0, 0.002))); l_ = min(o_, c_) * (1 - abs(rnd.gauss(0, 0.002)))
    O.append(o_); H.append(h_); Lo.append(l_); Cc.append(c_); T.append(i * 900_000); p = c_
for preset in ("Strict", "Standard", "Lenient"):
    r = run_hav(O, H, Lo, Cc, T, HavConfig(length=5, preset=preset, show_borderline=True))
    kinds = {}
    for e in r["events"]:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print(preset, kinds)
print("ALL OK")
