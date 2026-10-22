"""
fvg_standard.py — پایتونِ دقیقِ fvg_standard.pine (FVG استاندارد ICT، سیگنال روی کندل بسته)
===========================================================================================
تعریف:
  FVG صعودی : low[i] > high[i-2]  → زون [bottom=high[i-2], top=low[i]]  (کل شکاف)
  FVG نزولی : high[i] < low[i-2]  → زون [bottom=high[i],  top=low[i-2]]
  فیلتر اندازه: gap/قیمتِ مرجع*100 ≥ min_gap_pct  (مرجع: high[i-2] برای صعودی، low[i-2] برای نزولی)
ترتیب در هر کندل i (i ≥ 2) — دقیقاً مثل پاین:
  ۱) زون‌های موجود (born < i)، از آخر به اول:
       الف) اگر i - born > max_age → حذف (بدون mitigation)
       ب) ورود (entered): صعودی low ≤ top | نزولی high ≥ bottom ؛ اولین ورود → touched=True
          و اگر retest فعال و «رد قیمت» (صعودی close > top | نزولی close < bottom) → سیگنال RETEST
       ج) mitigation طبق mode → حذف
  ۲) FVG جدید (بعد از به‌روزرسانی؛ پس همان کندل روی زونِ جدید اثر ندارد)
modeها: "wick" (low ≤ bottom | high ≥ top)، "close" (close < bottom | close > top)،
        "touch" (= entered)، "ce" (low ≤ mid | high ≥ mid)
"""

MODES = ("wick", "close", "touch", "ce")


def run_fvg_std(o, h, l, c, mode="wick", min_gap_pct=0.0, max_age=300, show_retest=True):
    """
    ورودی: لیست‌های o,h,l,c (قدیمی → جدید، فقط کندل‌های بسته)
    خروجی: dict
      formed   : [{bar, dir:'BULL'|'BEAR', top, bottom}]
      retests  : [{bar, dir}]          (هر کندل/جهت یک‌بار، مثل plotshape)
      zones    : زون‌های باز در پایان
      mitigated: [{born, bar, bull}]
      expired  : [{born, bar, bull}]
    """
    assert mode in MODES
    n = len(c)
    zones, formed, retests, mitigated, expired = [], [], [], [], []

    for i in range(2, n):
        ret_bull = ret_bear = False

        # ۱) زون‌های موجود
        for j in range(len(zones) - 1, -1, -1):
            z = zones[j]
            bull, zt, zb = z["bull"], z["top"], z["bottom"]
            if i - z["born"] > max_age:
                expired.append({"born": z["born"], "bar": i, "bull": bull})
                del zones[j]
                continue

            entered = (l[i] <= zt) if bull else (h[i] >= zb)
            if entered and not z["touched"]:
                z["touched"] = True
                if show_retest:
                    if bull and c[i] > zt:
                        ret_bull = True
                    if (not bull) and c[i] < zb:
                        ret_bear = True

            mid = (zt + zb) / 2
            if mode == "wick":
                hit = (l[i] <= zb) if bull else (h[i] >= zt)
            elif mode == "close":
                hit = (c[i] < zb) if bull else (c[i] > zt)
            elif mode == "touch":
                hit = entered
            else:
                hit = (l[i] <= mid) if bull else (h[i] >= mid)
            if hit:
                mitigated.append({"born": z["born"], "bar": i, "bull": bull})
                del zones[j]

        # ۲) FVG جدید
        gap_bull = l[i] - h[i - 2]
        gap_bear = l[i - 2] - h[i]
        if gap_bull > 0 and (gap_bull / h[i - 2] * 100 >= min_gap_pct):
            zones.append({"born": i, "bull": True, "top": l[i], "bottom": h[i - 2], "touched": False})
            formed.append({"bar": i, "dir": "BULL", "top": l[i], "bottom": h[i - 2]})
        if gap_bear > 0 and (gap_bear / l[i - 2] * 100 >= min_gap_pct):
            zones.append({"born": i, "bull": False, "top": l[i - 2], "bottom": h[i], "touched": False})
            formed.append({"bar": i, "dir": "BEAR", "top": l[i - 2], "bottom": h[i]})

        if ret_bull:
            retests.append({"bar": i, "dir": "BULL"})
        if ret_bear:
            retests.append({"bar": i, "dir": "BEAR"})

    return {"formed": formed, "retests": retests, "zones": zones, "mitigated": mitigated, "expired": expired}


def latest_signals(o, h, l, c, **kw):
    """سیگنال‌های «آخرین کندل بسته‌شده»: (formed, retests) هر کدام لیست."""
    n = len(c)
    if n < 3:
        return [], []
    r = run_fvg_std(o, h, l, c, **kw)
    return ([s for s in r["formed"] if s["bar"] == n - 1], [s for s in r["retests"] if s["bar"] == n - 1])
