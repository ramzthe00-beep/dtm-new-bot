"""
sfp_strategy.py — پیاده‌سازی عین‌به‌عین «SFP (All Swings - No Filter)» (LuxAlgo, Pine v5)
Pure Python، بدون PyneCore؛ state صریح، ترتیب اجرا دقیقاً مطابق Pine:
  هر بار (کندل بسته‌شده n):
    1) تشخیص پیوت (leftbars=len, rightbars=1) → پیوت روی کندل n-1
    2) بلوک Bearish: به‌روزرسانی swingH → بررسی SFP → تأیید → لغو
    3) بلوک Bullish: همان با swingL
قوانین استخراج‌شده از لاگ Pine (۹۶۸۳ کندل):
  - پیوت: سمت چپ تساوی مجاز (>=)، سمت راست تساوی غیرمجاز (strict)
  - شرط SFP: همه مقایسه‌ها strict
  - تأیید می‌تواند روی همان کندل SFP هم رخ دهد (پس از ساخت pivH)
  - لغو: age > 500 یا عبور close از swing؛ فقط وقتی active بود اثر دارد
  - حلقهٔ oppos: for i = 1 to n-bx-1 (در Pine اگر حد بالا <1 باشد نزولی است؛
    اینجا هم پیاده شده، هرچند اثبات می‌شود هرگز اتفاق نمی‌افتد)
"""

AGE_LIMIT = 500


def _new_piv():
    return {"swing_prc": None, "swing_bix": None, "oppos_prc": None,
            "oppos_bix": None, "active": False, "confirmed": False}


def _snap(p):
    return dict(p)


def run_sfp(opens, highs, lows, closes, length=5, bull=True, bear=True, log_all=False):
    """
    ورودی: لیست‌های هم‌طول (کندل‌های بسته‌شده، index = bar_index).
    خروجی: لیست رویدادها (dict) به ترتیب اجرا، با کلید 'kind':
      PIV_H, PIV_L, CHK_H, CHK_L, HIT_H, HIT_L, CONF_H, CONF_L, CANCEL_H, CANCEL_L
    """
    N = len(closes)
    ev = []
    swing = {"H": [None, None], "L": [None, None]}   # [bix, prc]
    piv = {"H": _new_piv(), "L": _new_piv()}

    for n in range(N):
        o, h, l, c = opens[n], highs[n], lows[n], closes[n]
        p = n - 1

        # ───────── 1) پیوت‌ها (ta.pivothigh/pivotlow(len, 1)) ─────────
        ph = pl = None
        if p - length >= 0:
            lmax = max(highs[p - length:p])
            lmin = min(lows[p - length:p])
            if highs[p] >= lmax and highs[p] > h:
                ph = highs[p]
                ev.append({"kind": "PIV_H", "bar": n, "value": ph, "pivotBar": p,
                           "tieLeft": lmax == highs[p], "tieRight": h == highs[p],
                           "prevSwing": (swing["H"][0], swing["H"][1])})
            if lows[p] <= lmin and lows[p] < l:
                pl = lows[p]
                ev.append({"kind": "PIV_L", "bar": n, "value": pl, "pivotBar": p,
                           "tieLeft": lmin == lows[p], "tieRight": l == lows[p],
                           "prevSwing": (swing["L"][0], swing["L"][1])})

        # ───────── 2) Bearish (swingH / pivH) ─────────
        if bear:
            _side("H", n, o, h, l, c, ph, p, swing["H"], piv["H"],
                  lows, highs, ev, log_all)
        # ───────── 3) Bullish (swingL / pivL) ─────────
        if bull:
            _side("L", n, o, h, l, c, pl, p, swing["L"], piv["L"],
                  lows, highs, ev, log_all)
    return ev


def _side(side, n, o, h, l, c, pivot_val, p, sw_state, pv, lows, highs, ev, log_all):
    bear = (side == "H")

    # به‌روزرسانی swing (فقط وقتی پیوت جدید باشد) — قبل از بررسی SFP
    if pivot_val is not None:
        sw_state[0] = p          # swing.bix = n-1
        sw_state[1] = pivot_val  # swing.prc
    bx, sw = sw_state[0], sw_state[1]

    # شرط‌های SFP (همه strict؛ با sw=None هر مقایسه false است)
    if sw is None:
        c1 = c2 = c3 = False
    elif bear:
        c1, c2, c3 = (h > sw), (o < sw), (c < sw)
    else:
        c1, c2, c3 = (l < sw), (o > sw), (c > sw)
    hit = c1 and c2 and c3
    near = (sw is not None) and c1 and (log_all or c2 or c3)
    if near:
        ev.append({"kind": "CHK_" + side, "bar": n, "sw": sw, "bx": bx,
                   "newPivThisBar": pivot_val is not None,
                   "c1": c1, "c2": c2, "c3": c3, "decision": "HIT" if hit else "REJECT"})

    # ───── SFP تشخیص داده شد ─────
    if hit:
        oppos = sw
        oppos_b = n
        to = n - bx - 1
        idxs = range(1, to + 1) if to >= 1 else range(1, to - 1, -1)  # نزولی مثل Pine
        iters = 0
        first_i = last_i = None
        updates = []
        for i in idxs:
            iters += 1
            if first_i is None:
                first_i = i
            last_i = i
            b = n - i
            if b < 0:
                continue  # na در Pine → مقایسه false
            v = lows[b] if bear else highs[b]
            if (v < oppos) if bear else (v > oppos):
                oppos = v
                oppos_b = n - i
                updates.append((i, v, n - i))
        prev = _snap(pv)
        pv.update({"swing_prc": sw, "swing_bix": bx, "oppos_prc": oppos,
                   "oppos_bix": oppos_b, "active": True, "confirmed": False})
        ev.append({"kind": "HIT_" + side, "bar": n, "sw": sw, "bx": bx,
                   "loopTo": to, "descending": to < 1, "iters": iters,
                   "firstI": first_i, "lastI": last_i, "updates": updates,
                   "oppos": oppos, "opposBar": oppos_b,
                   "prev": prev, "new": _snap(pv),
                   "deletedPrev": not prev["confirmed"]})

    # ───── تأیید (روی همان کندل SFP هم اجرا می‌شود) ─────
    if pv["active"] and not pv["confirmed"]:
        cf = (c < pv["oppos_prc"]) if bear else (c > pv["oppos_prc"])
        if cf:
            pv["confirmed"] = True
            ev.append({"kind": "CONF_" + side, "bar": n, "oppos": pv["oppos_prc"],
                       "age": n - pv["swing_bix"]})
        elif log_all:
            ev.append({"kind": "CONF_" + side, "bar": n, "oppos": pv["oppos_prc"],
                       "age": n - pv["swing_bix"], "pending": True})

    # ───── لغو ─────
    was_act = pv["active"]
    age_exp = (pv["swing_bix"] is not None) and (n - pv["swing_bix"] > AGE_LIMIT)
    if pv["swing_prc"] is None:
        crossed = False
    else:
        crossed = (c > pv["swing_prc"]) if bear else (c < pv["swing_prc"])
    if was_act and (age_exp or crossed):
        ev.append({"kind": "CANCEL_" + side, "bar": n, "ageExpired": age_exp,
                   "crossed": crossed, "state": _snap(pv)})
    if age_exp or crossed:
        pv["active"] = False


def last_bar_events(opens, highs, lows, closes, **kw):
    """رویدادهای آخرین کندل بسته‌شده (برای استفاده در ربات)."""
    ev = run_sfp(opens, highs, lows, closes, **kw)
    last = len(closes) - 1
    return [e for e in ev if e["bar"] == last]
