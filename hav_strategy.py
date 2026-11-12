"""
hav_strategy.py — پیاده‌سازی پایتون «Harmonic Auto-Validator [GBB] v1.1» (حالت Confirmed/Borderline)
=========================================================================================
ترجمه‌ی خط‌به‌خط پاین؛ ترتیب اجرا در هر کندل بسته‌شده دقیقاً مثل اسکریپت:
  ۱) ATR  = ta.atr(period)  (RMA با seed=SMA اولین `period` مقدار TR؛ TR کندل اول = high-low)
  ۲) پیوت = ta.pivothigh/low(L, L)  → سمت چپ تساوی مجاز (>=)، سمت راست تساوی غیرمجاز (strict)
     (قاعده‌ی تساوی از لاگ‌های واقعی Pine در پروژه‌ی SFP استخراج شده)
  ۳) بافر پیوت (حداکثر ۱۲، تناوب اکید H/L، جایگزینی پیوت هم‌جهتِ افراطی‌تر)
  ۴) اگر پیوت جدید اضافه/عوض شد و ≥۶ پیوت داریم: برای هر پنجره‌ی ۵پیوتی (X..D) اسکن:
       اعتبارسنج هر الگو → ساخت PRZ → امتیاز → انتخاب برنده (اولین با بیشترین امتیاز؛ تساوی = اولی)
  ۵) patterns_active با حذف FIFO (حداکثر max_active) — روی تشخیص تکراری اثر دارد
غیرفعال (عمداً): Forming Mode پیاده نشده است. در پاین، مسیر Forming هنگام چک تکراری به `ex.pD.t`
(که برای الگوی Forming برابر na است) دسترسی دارد؛ رفتار آن بدون لاگ قطعی نیست. با forming=True خطا می‌دهد.

خروجی run_hav یک لیست events است که هر کدام معادل یک خط لاگ پاین (SCAN/DUP/WIN/PRZ/SCORE/WINNER/FIRE/PIV)
است تا با hav_parity_test.py مقایسه شود.
"""
import math
from dataclasses import dataclass, field

NAN = float("nan")


# ───────────────────────── تنظیمات (معادل inputها) ─────────────────────────
@dataclass
class HavConfig:
    length: int = 5                 # length_eff (Auto: ≤30m→5 ، ≤4h→8 ، D→13 ، W→21)
    use_log: bool = False
    preset: str = "Standard"        # Strict | Standard | Lenient
    min_xa_atr: float = 2.0
    atr_period: int = 14
    min_score: float = 6
    min_conf: int = 2
    penalize_no_abcd: bool = True
    show_borderline: bool = False
    borderline_min_score: float = 4.0
    enable_alerts: bool = True
    alert_min_score: float = 6.0
    max_active: int = 30
    forming: bool = False
    scan: tuple = (True, True, True, True, True, True)   # Gartley, Bat, AltBat, Butterfly, Crab, DeepCrab


def auto_length(tf_minutes):
    return 5 if tf_minutes <= 30 else 8 if tf_minutes <= 240 else 13 if tf_minutes <= 1440 else 21


# ───────────────────────── ابزارهای معادل Pine ─────────────────────────
def pine_round(x):
    """math.round در Pine: نزدیک‌ترین عدد صحیح، تساوی به سمت بالا."""
    return math.floor(x + 0.5)


def pmin(a, b):
    return NAN if (a != a or b != b) else (a if a < b else b)


def pmax(a, b):
    return NAN if (a != a or b != b) else (a if a > b else b)


def pine_atr(h, l, c, n, seed0=None):
    """
    ta.atr(n) = rma(tr, n). RMA: مقدار اول = SMA(n مقدار اول TR) در کندل n-1، بعد بازگشتی با alpha=1/n.
    seed0: اگر داده‌ی ابتدای چارت را نداریم، ATR واقعیِ کندل اول پنجره (از لاگ) را بدهید.
    """
    N = len(c)
    out = [NAN] * N
    tr = [0.0] * N
    for i in range(N):
        tr[i] = (h[i] - l[i]) if i == 0 else max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
    if seed0 is not None:
        prev = seed0
        out[0] = prev
        for i in range(1, N):
            prev = (1.0 / n) * tr[i] + (1 - 1.0 / n) * prev      # alpha*src + (1-alpha)*prev
            out[i] = prev
        return out
    prev = None
    for i in range(N):
        if i < n - 1:
            continue
        if prev is None:
            prev = sum(tr[:n]) / n
        else:
            prev = (1.0 / n) * tr[i] + (1 - 1.0 / n) * prev
        out[i] = prev
    return out


@dataclass
class Pivot:
    t: int
    price: float
    bi: int
    is_high: bool


@dataclass
class Projection:
    label: str
    price: float
    in_prz: bool = False


@dataclass
class PRZ:
    top: float
    bot: float
    projections: list
    confluence_count: int


@dataclass
class Pattern:
    pattern_type: str
    is_bullish: bool
    pX: Pivot
    pA: Pivot
    pB: Pivot
    pC: Pivot
    pD: Pivot
    prz: PRZ
    score: float
    abcd_converges: bool
    state: str
    r_AB: float
    r_BC: float
    r_CD: float
    r_XD: float


# ───────────────────────── جدول بازه‌های تلورانس: (strict, lenient, standard) ─────────────────────────
_BC = ((0.382, 0.886), (0.300, 0.950), (0.382, 0.886))

TOL = {
    "Gartley": dict(B=((0.598, 0.638), (0.518, 0.718), (0.558, 0.678)), BC=_BC,
                    CD=((1.130, 1.618), (1.000, 1.800), (1.130, 1.618)),
                    D=((0.766, 0.806), (0.686, 0.886), (0.726, 0.846))),
    "Bat": dict(B=((0.480, 0.520), (0.400, 0.600), (0.440, 0.560)), BC=_BC,
                CD=((1.618, 2.618), (1.500, 2.900), (1.618, 2.618)),
                D=((0.866, 0.906), (0.786, 0.986), (0.826, 0.946))),
    "Alt Bat": dict(B=((0.362, 0.402), (0.282, 0.482), (0.322, 0.442)), BC=_BC,
                    CD=((2.200, 3.400), (1.618, 4.000), (2.000, 3.618)),
                    D=((1.110, 1.150), (1.030, 1.230), (1.070, 1.190))),
    "Butterfly": dict(B=((0.766, 0.806), (0.686, 0.886), (0.726, 0.846)), BC=_BC,
                      CD=((1.618, 2.618), (1.500, 2.900), (1.618, 2.618)),
                      D=((1.252, 1.292), (1.172, 1.372), (1.212, 1.332))),
    "Crab": dict(B=((0.480, 0.520), (0.400, 0.618), (0.440, 0.560)), BC=_BC,
                 CD=((2.618, 3.618), (2.400, 4.000), (2.618, 3.618)),
                 D=((1.598, 1.638), (1.518, 1.718), (1.558, 1.678))),
    "Deep Crab": dict(B=((0.866, 0.906), (0.786, 0.986), (0.826, 0.946)), BC=_BC,
                      CD=((2.618, 3.618), (2.400, 4.000), (2.618, 3.618)),
                      D=((1.598, 1.638), (1.518, 1.718), (1.558, 1.678))),
}

# نوع ساختار: retrace = D بین X و C ، extension = D فراتر از X
FAMILY = {"Gartley": "retrace", "Bat": "retrace", "Alt Bat": "ext", "Butterfly": "ext",
          "Crab": "ext", "Deep Crab": "ext"}

# ایده‌آل‌های امتیازدهی (B, D)
IDEAL = {"Gartley": (0.618, 0.786), "Bat": (0.500, 0.886), "Alt Bat": (0.382, 1.130),
         "Butterfly": (0.786, 1.272), "Crab": (0.500, 1.618), "Deep Crab": (0.886, 1.618)}

# پروجکشن‌های PRZ: (label, kind, k) — kind: xa | bc | abcd
PRZ_SPEC = {
    "Gartley": [("0.786 XA", "xa", 0.786), ("1.27 BC", "bc", 1.27), ("1.618 BC", "bc", 1.618), ("AB=CD", "abcd", 1.0)],
    "Bat": [("0.886 XA", "xa", 0.886), ("1.618 BC", "bc", 1.618), ("2.618 BC", "bc", 2.618),
            ("AB=CD", "abcd", 1.0), ("1.27 AB=CD", "abcd", 1.27)],
    "Alt Bat": [("1.13 XA", "xa", 1.130), ("2.0 BC", "bc", 2.000), ("3.618 BC", "bc", 3.618),
                ("1.27 AB=CD", "abcd", 1.27)],
    "Butterfly": [("1.272 XA", "xa", 1.272), ("1.618 BC", "bc", 1.618), ("2.618 BC", "bc", 2.618),
                  ("1.27 AB=CD", "abcd", 1.27)],
    "Crab": [("1.618 XA", "xa", 1.618), ("2.618 BC", "bc", 2.618), ("3.618 BC", "bc", 3.618),
             ("1.27 AB=CD", "abcd", 1.27)],
}
PRZ_SPEC["Deep Crab"] = PRZ_SPEC["Crab"]          # Deep Crab همان PRZ Crab را دارد

ABCD_LABELS = {"Gartley": ("AB=CD",), "Bat": ("AB=CD", "1.27 AB=CD"), "Alt Bat": ("1.27 AB=CD",),
               "Butterfly": ("1.27 AB=CD",), "Crab": ("1.27 AB=CD",), "Deep Crab": ("1.27 AB=CD",)}

ORDER = ["Gartley", "Bat", "Alt Bat", "Butterfly", "Crab", "Deep Crab"]     # اولویت در تساوی امتیاز
LOG_KEY = {"Gartley": "gart", "Bat": "bat", "Alt Bat": "abat", "Butterfly": "bfly", "Crab": "crab", "Deep Crab": "dcrab"}
PRZ_LOG_NAME = {"Gartley": "Gartley", "Bat": "Bat", "Alt Bat": "AltBat", "Butterfly": "Butterfly",
                "Crab": "Crab", "Deep Crab": "DeepCrab"}


class _Ctx:
    def __init__(self, cfg, atr):
        self.cfg = cfg
        self.atr = atr                      # ATR کندل جاری
        self.band_idx = 0 if cfg.preset == "Strict" else 1 if cfg.preset == "Lenient" else 2

    def LP(self, p):
        return math.log(p) if self.cfg.use_log else p

    def FP(self, p):
        return math.exp(p) if self.cfg.use_log else p

    def ratio(self, far, near, pt):
        af, an, pp = self.LP(far), self.LP(near), self.LP(pt)
        return abs(af - pp) / abs(af - an)

    def band(self, pat, key):
        return TOL[pat][key][self.band_idx]


# ───────────────────────── اعتبارسنج (status 0..7) ─────────────────────────
def validate(ctx, pat, pX, pA, pB, pC, pD):
    """خروجی: (status, bullish, r_AB, r_BC, r_CD, r_XD)"""
    dir_ok = (pX.is_high != pA.is_high) and (pA.is_high != pB.is_high) and \
             (pB.is_high != pC.is_high) and (pC.is_high != pD.is_high)
    bullish = not pX.is_high
    X, A, B, C, D = pX.price, pA.price, pB.price, pC.price, pD.price
    ext = FAMILY[pat] == "ext"

    if bullish:
        struct_ok = (X < A and B > X and B < A and C > B and C < A and
                     ((D < X) if ext else (D > X and D < C)))
    else:
        struct_ok = (X > A and B < X and B > A and C < B and C > A and
                     ((D > X) if ext else (D < X and D > C)))

    xa_abs = abs(A - X)
    xa_big = xa_abs >= ctx.cfg.min_xa_atr * ctx.atr        # na → False

    status, rAB, rBC, rCD, rXD = 0, 0.0, 0.0, 0.0, 0.0
    if not dir_ok:
        status = 1
    elif not struct_ok:
        status = 2
    elif not xa_big:
        status = 3
    else:
        rAB = ctx.ratio(A, X, B)
        rBC = ctx.ratio(B, A, C)
        rCD = ctx.ratio(C, B, D)
        rXD = ctx.ratio(A, X, D)
        ab_lo, ab_hi = ctx.band(pat, "B")
        bc_lo, bc_hi = ctx.band(pat, "BC")
        cd_lo, cd_hi = ctx.band(pat, "CD")
        d_lo, d_hi = ctx.band(pat, "D")
        if not (rAB >= ab_lo and rAB <= ab_hi):
            status = 4
        elif not (rBC >= bc_lo and rBC <= bc_hi):
            status = 5
        elif not (rCD >= cd_lo and rCD <= cd_hi):
            status = 6
        elif not (rXD >= d_lo and rXD <= d_hi):
            status = 7
    return status, bullish, rAB, rBC, rCD, rXD


# ───────────────────────── PRZ ─────────────────────────
def _median(vals):
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def build_prz(ctx, pat, pX, pA, pB, pC):
    LP, FP = ctx.LP, ctx.FP
    projs = []
    for label, kind, k in PRZ_SPEC[pat]:
        if kind == "xa":
            price = FP(LP(pA.price) - k * (LP(pA.price) - LP(pX.price)))
        elif kind == "bc":
            price = FP(LP(pC.price) - k * (LP(pC.price) - LP(pB.price)))
        else:
            ab_vec = LP(pB.price) - LP(pA.price)
            price = FP(LP(pC.price) + k * ab_vec)
        projs.append(Projection(label, price, False))

    med = _median([p.price for p in projs])
    top = bot = None
    conf = 0
    for p in projs:
        if abs(p.price - med) <= 3.0 * ctx.atr:
            p.in_prz = True
            conf += 1
            top = p.price if top is None else max(top, p.price)
            bot = p.price if bot is None else min(bot, p.price)
    if top is None:
        for p in projs:
            top = p.price if top is None else max(top, p.price)
            bot = p.price if bot is None else min(bot, p.price)
    return PRZ(top, bot, projs, conf)


def abcd_converges(pat, prz):
    return any(p.label in ABCD_LABELS[pat] and p.in_prz for p in prz.projections)


# ───────────────────────── امتیاز ─────────────────────────
def score(ctx, pat, rAB, rXD, prz, abcd_conv):
    ideal_b, ideal_d = IDEAL[pat]
    ab_norm = 1.0 - pmin(abs(rAB - ideal_b) / 0.100, 1.0)
    xd_norm = 1.0 - pmin(abs(rXD - ideal_d) / 0.100, 1.0)
    ratio_score = (ab_norm + xd_norm) * 2.0
    zone_h = prz.top - prz.bot
    tightness = 1.0 - pmin(zone_h / (ctx.atr * 3.0), 1.0)
    tight_score = tightness * 3.0
    conf_score = pmin(float(prz.confluence_count), 3.0)
    total = ratio_score + tight_score + conf_score
    if (not abcd_conv) and ctx.cfg.penalize_no_abcd:
        total = pmax(0.0, total - 2.0)
    return pine_round(total * 10.0) / 10.0


# ───────────────────────── اجرای اصلی ─────────────────────────
def run_hav(o, h, l, c, t, cfg=None, atr_seed=None, bi0=0):
    """
    o,h,l,c,t: لیست‌های کندل‌های «بسته‌شده» (قدیمی → جدید)؛ t = زمان باز شدن کندل (ms).
    atr_seed: ATR واقعی کندل اول پنجره (اگر پنجره از اول چارت نیست).
    bi0: bar_index کندل اول (برای هم‌خوانی با لاگ Pine).
    خروجی: dict(events, patterns, pivots, atr)
    """
    cfg = cfg or HavConfig()
    if cfg.forming:
        raise NotImplementedError("Forming Mode پیاده نشده (رفتار na در پاین بدون لاگ قطعی نیست)")
    N = len(c)
    L = cfg.length
    atr = pine_atr(h, l, c, cfg.atr_period, atr_seed)

    pivot_buf = []
    last_pivot_bi = -1
    patterns_active = []
    events = []

    def push_pivot(p):
        if not pivot_buf:
            pivot_buf.append(p)
        else:
            last = pivot_buf[-1]
            if last.is_high == p.is_high:
                more = (p.price > last.price) if p.is_high else (p.price < last.price)
                if more:
                    pivot_buf[-1] = p
            else:
                pivot_buf.append(p)
        while len(pivot_buf) > 12:
            pivot_buf.pop(0)

    for n in range(N):
        bar = bi0 + n
        ctx = _Ctx(cfg, atr[n])

        # ── پیوت‌ها: ta.pivothigh/pivotlow(L, L) → پیوت روی کندل p = n-L
        piv_h = piv_l = None
        p = n - L
        if p - L >= 0:
            lmax = max(h[p - L:p])
            rmax = max(h[p + 1:n + 1])
            lmin = min(l[p - L:p])
            rmin = min(l[p + 1:n + 1])
            if h[p] >= lmax and h[p] > rmax:
                piv_h = h[p]
            if l[p] <= lmin and l[p] < rmin:
                piv_l = l[p]
        if piv_h is not None:
            push_pivot(Pivot(t[p], piv_h, bi0 + p, True))
        if piv_l is not None:
            push_pivot(Pivot(t[p], piv_l, bi0 + p, False))

        cur_last_bi = pivot_buf[-1].bi if pivot_buf else -1
        new_pivot_added = cur_last_bi != last_pivot_bi
        last_pivot_bi = cur_last_bi

        if piv_h is not None or piv_l is not None:
            events.append({"kind": "PIV", "bar": bar, "ph": piv_h, "pl": piv_l, "new": new_pivot_added,
                           "n": len(pivot_buf),
                           "buf": [(q.t, q.bi, q.price, q.is_high) for q in pivot_buf]})

        # ── اسکن الگوها
        if any(cfg.scan) and new_pivot_added and len(pivot_buf) >= 6:
            events.append({"kind": "SCAN", "bar": bar, "n": len(pivot_buf), "atr": atr[n]})
            for start in range(0, len(pivot_buf) - 6 + 1):
                pX, pA, pB, pC, pD = pivot_buf[start:start + 5]

                duplicate = any(ex.pX.t == pX.t and ex.pD.t == pD.t for ex in patterns_active)
                if duplicate:
                    events.append({"kind": "DUP", "bar": bar, "start": start})
                    continue

                res = {}
                for idx, pat in enumerate(ORDER):
                    res[pat] = validate(ctx, pat, pX, pA, pB, pC, pD) if cfg.scan[idx] else (-1, False, 0.0, 0.0, 0.0, 0.0)

                events.append({"kind": "WIN", "bar": bar, "start": start,
                               "tX": pX.t, "tA": pA.t, "tB": pB.t, "tC": pC.t, "tD": pD.t,
                               **{LOG_KEY[pat]: res[pat] for pat in ORDER}})

                winner = None            # (type, state, score, prz, abcd, bull, rAB, rBC, rCD, rXD)
                winner_score = -1.0
                for pat in ORDER:
                    status, bull, rAB, rBC, rCD, rXD = res[pat]
                    if status != 0:
                        continue
                    prz = build_prz(ctx, pat, pX, pA, pB, pC)
                    conv = abcd_converges(pat, prz)
                    events.append({"kind": "PRZ", "bar": bar, "start": start, "pat": PRZ_LOG_NAME[pat],
                                   "abcd": conv, "top": prz.top, "bot": prz.bot, "conf": prz.confluence_count,
                                   "projs": [(q.label, q.price, q.in_prz) for q in prz.projections]})
                    if prz.confluence_count < cfg.min_conf:
                        continue
                    sc = score(ctx, pat, rAB, rXD, prz, conv)
                    eligible = sc >= cfg.min_score or (cfg.show_borderline and sc >= cfg.borderline_min_score)
                    events.append({"kind": "SCORE", "bar": bar, "start": start, "pat": PRZ_LOG_NAME[pat],
                                   "score": sc, "elig": eligible})
                    if not eligible:
                        continue
                    if sc > winner_score:
                        winner_score = sc
                        winner = (pat, "Confirmed" if sc >= cfg.min_score else "Borderline",
                                  sc, prz, conv, bull, rAB, rBC, rCD, rXD)

                if winner is not None:
                    pat, state, sc, prz, conv, bull, rAB, rBC, rCD, rXD = winner
                    events.append({"kind": "WINNER", "bar": bar, "start": start, "pat": pat, "state": state,
                                   "score": sc, "bull": bull, "abcd": conv, "tX": pX.t, "tD": pD.t})
                    patterns_active.append(Pattern(pat, bull, pX, pA, pB, pC, pD, prz, sc, conv, state,
                                                   rAB, rBC, rCD, rXD))
                    if state == "Confirmed" and cfg.enable_alerts and sc >= cfg.alert_min_score:
                        events.append({"kind": "FIRE", "bar": bar, "pat": pat, "score": sc})

        # ── FIFO
        while len(patterns_active) > cfg.max_active:
            patterns_active.pop(0)

    return {"events": events, "patterns": patterns_active, "pivots": pivot_buf, "atr": atr}


def latest_confirmed(o, h, l, c, t, cfg=None, atr_seed=None, bi0=0):
    """الگوهای Confirmed که روی «آخرین کندل بسته‌شده» تأیید شده‌اند (معادل FIRE/alertcondition)."""
    res = run_hav(o, h, l, c, t, cfg, atr_seed, bi0)
    last = bi0 + len(c) - 1
    return [e for e in res["events"] if e["kind"] == "WINNER" and e["bar"] == last and e["state"] == "Confirmed"]
