import pandas as pd
import re
import numpy as np

RAW = {
    "BNBUSDT": "parity_lab/raw_data/BNBUSDT_1m_pine_aligned.csv",
    "LTCUSDT": "parity_lab/raw_data/LTCUSDT_1m_pine_aligned.csv",
    "DOGEUSDT": "parity_lab/raw_data/DOGEUSDT_1m_pine_aligned.csv",
    "ETHUSDT": "parity_lab/raw_data/ETHUSDT_1m_pine_aligned.csv",
}

PINE = {
    "BNBUSDT": "parity_lab/pine_logs/pine_10.csv",
    "LTCUSDT": "parity_lab/pine_logs/pine_11.csv",
    "DOGEUSDT": "parity_lab/pine_logs/pine_12.csv",
    "ETHUSDT": "parity_lab/pine_logs/pine_13.csv",
}

PAT_SIG = re.compile(r"🔔\s*(CD\+|CD-|HD\+|HD-)")
PAT_CUR = re.compile(r"📌\s*کندل فعلی:\s*(\d+)")
PAT_P1 = re.compile(
    r"Pivot اول:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
)
PAT_P2 = re.compile(
    r"Pivot دوم:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
)


def nearest_price(raw, price, center, radius=30):

    lo = max(0, center - radius)
    hi = min(len(raw), center + radius + 1)

    best = None

    for idx in range(lo, hi):

        r = raw.iloc[idx]

        for field in ["open", "high", "low", "close"]:

            value = float(r[field])
            diff = abs(value - price)

            item = {
                "idx": idx,
                "offset": idx - center,
                "time": str(r["time"]),
                "field": field,
                "value": value,
                "diff": diff,
            }

            if best is None or diff < best["diff"]:
                best = item

    return best


print("=" * 120)
print("PINE PIVOT PRICE LOCATOR")
print("=" * 120)

for symbol in RAW:

    print("\n" + "=" * 120)
    print(symbol)
    print("=" * 120)

    raw = pd.read_csv(RAW[symbol])

    raw["time"] = pd.to_datetime(raw["time"], utc=True)

    raw = (
        raw
        .sort_values("time")
        .reset_index(drop=True)
    )

    pine = pd.read_csv(
        PINE[symbol],
        usecols=["Message"]
    )

    results = []

    for msg in pine["Message"].astype(str):

        sig = PAT_SIG.search(msg)
        cur = PAT_CUR.search(msg)
        p1 = PAT_P1.search(msg)
        p2 = PAT_P2.search(msg)

        if not (sig and cur and p1 and p2):
            continue

        signal = sig.group(1)

        cur_bar = int(cur.group(1))

        p1_price = float(p1.group(1))
        p1_bar = int(p1.group(2))

        p2_price = float(p2.group(1))
        p2_bar = int(p2.group(2))

        if not (
            0 <= cur_bar < len(raw)
            and 0 <= p1_bar < len(raw)
            and 0 <= p2_bar < len(raw)
        ):
            continue

        n1 = nearest_price(raw, p1_price, p1_bar)
        n2 = nearest_price(raw, p2_price, p2_bar)

        results.append({
            "signal": signal,
            "cur_bar": cur_bar,

            "p1_price": p1_price,
            "p1_bar": p1_bar,
            "p1_time": str(raw.iloc[p1_bar]["time"]),
            "p1_near": n1,

            "p2_price": p2_price,
            "p2_bar": p2_bar,
            "p2_time": str(raw.iloc[p2_bar]["time"]),
            "p2_near": n2,
        })

    print("SIGNALS:", len(results))

    print()
    print("-" * 120)
    print("FIRST 10 PIVOT PRICE LOCATIONS")
    print("-" * 120)

    for r in results[:10]:

        n1 = r["p1_near"]
        n2 = r["p2_near"]

        print()
        print(
            f"{r['signal']} | "
            f"P1 Pine={r['p1_price']} "
            f"bar={r['p1_bar']} "
            f"time={r['p1_time']}"
        )

        print(
            f"   P1 NEAREST: "
            f"bar={n1['idx']} "
            f"offset={n1['offset']:+d} "
            f"time={n1['time']} "
            f"{n1['field'].upper()}={n1['value']} "
            f"diff={n1['diff']}"
        )

        print(
            f"{r['signal']} | "
            f"P2 Pine={r['p2_price']} "
            f"bar={r['p2_bar']} "
            f"time={r['p2_time']}"
        )

        print(
            f"   P2 NEAREST: "
            f"bar={n2['idx']} "
            f"offset={n2['offset']:+d} "
            f"time={n2['time']} "
            f"{n2['field'].upper()}={n2['value']} "
            f"diff={n2['diff']}"
        )

    # --------------------------------------------------
    # بررسی اینکه Pine price دقیقاً در کندل دیگری وجود دارد
    # --------------------------------------------------

    print()
    print("-" * 120)
    print("OFFSET SUMMARY")
    print("-" * 120)

    offsets_p1 = []
    offsets_p2 = []

    for r in results:

        n1 = r["p1_near"]
        n2 = r["p2_near"]

        if n1["diff"] <= max(abs(r["p1_price"]) * 1e-7, 1e-12):
            offsets_p1.append(n1["offset"])

        if n2["diff"] <= max(abs(r["p2_price"]) * 1e-7, 1e-12):
            offsets_p2.append(n2["offset"])

    print("P1 EXACT PRICE FOUND:", len(offsets_p1), "/", len(results))
    print("P2 EXACT PRICE FOUND:", len(offsets_p2), "/", len(results))

    if offsets_p1:
        print("P1 OFFSETS:", offsets_p1)

    if offsets_p2:
        print("P2 OFFSETS:", offsets_p2)

print()
print("=" * 120)
print("LOCATOR FINISHED")
print("=" * 120)
