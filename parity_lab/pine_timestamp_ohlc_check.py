import pandas as pd
import re

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

pat_sig = re.compile(r"🔔\s*(CD\+|CD-|HD\+|HD-)")
pat_cur = re.compile(r"📌\s*کندل فعلی:\s*(\d+)")
pat_p1 = re.compile(
    r"Pivot اول:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
)
pat_p2 = re.compile(
    r"Pivot دوم:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
)

print("=" * 120)
print("PINE TIMESTAMP → RAW OHLC EXACT PIVOT TEST")
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
        .drop_duplicates("time")
        .reset_index(drop=True)
    )

    by_time = raw.set_index("time")

    pine = pd.read_csv(PINE[symbol], usecols=["Message"])

    total = 0

    p1_exact = 0
    p2_exact = 0

    p1_ohlc = 0
    p2_ohlc = 0

    p1_miss = []
    p2_miss = []

    for msg in pine["Message"].astype(str):

        sig = pat_sig.search(msg)
        cur = pat_cur.search(msg)
        p1 = pat_p1.search(msg)
        p2 = pat_p2.search(msg)

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

        # VERY IMPORTANT:
        # bar index is interpreted against the FULL pine-aligned dataset
        p1_row = raw.iloc[p1_bar]
        p2_row = raw.iloc[p2_bar]

        p1_time = p1_row["time"]
        p2_time = p2_row["time"]

        try:
            r1 = by_time.loc[p1_time]
            r2 = by_time.loc[p2_time]
        except KeyError:
            continue

        total += 1

        # Bearish divergence -> HIGH
        # Bullish divergence -> LOW
        if signal.endswith("-"):
            candidates1 = {
                "high": float(r1["high"]),
                "open": float(r1["open"]),
                "low": float(r1["low"]),
                "close": float(r1["close"]),
            }

            candidates2 = {
                "high": float(r2["high"]),
                "open": float(r2["open"]),
                "low": float(r2["low"]),
                "close": float(r2["close"]),
            }

            source = "HIGH"

        else:
            candidates1 = {
                "low": float(r1["low"]),
                "open": float(r1["open"]),
                "high": float(r1["high"]),
                "close": float(r1["close"]),
            }

            candidates2 = {
                "low": float(r2["low"]),
                "open": float(r2["open"]),
                "high": float(r2["high"]),
                "close": float(r2["close"]),
            }

            source = "LOW"

        raw_p1 = candidates1[source.lower()]
        raw_p2 = candidates2[source.lower()]

        d1 = raw_p1 - p1_price
        d2 = raw_p2 - p2_price

        tol1 = max(abs(p1_price) * 1e-9, 1e-12)
        tol2 = max(abs(p2_price) * 1e-9, 1e-12)

        ok1 = abs(d1) <= tol1
        ok2 = abs(d2) <= tol2

        if ok1:
            p1_exact += 1
        else:
            p1_miss.append(
                (
                    signal,
                    p1_bar,
                    p1_time,
                    p1_price,
                    raw_p1,
                    d1,
                    r1["open"],
                    r1["high"],
                    r1["low"],
                    r1["close"],
                )
            )

        if ok2:
            p2_exact += 1
        else:
            p2_miss.append(
                (
                    signal,
                    p2_bar,
                    p2_time,
                    p2_price,
                    raw_p2,
                    d2,
                    r2["open"],
                    r2["high"],
                    r2["low"],
                    r2["close"],
                )
            )

        if total <= 5:

            print()
            print("-" * 120)
            print("SIGNAL:", signal)

            print(
                "P1:",
                p1_price,
                "@ bar",
                p1_bar,
                "|",
                p1_time
            )

            print(
                "RAW P1:",
                source,
                "=",
                raw_p1,
                "DIFF=",
                d1
            )

            print(
                "P1 OHLC:",
                f"O={r1['open']}",
                f"H={r1['high']}",
                f"L={r1['low']}",
                f"C={r1['close']}"
            )

            print(
                "P2:",
                p2_price,
                "@ bar",
                p2_bar,
                "|",
                p2_time
            )

            print(
                "RAW P2:",
                source,
                "=",
                raw_p2,
                "DIFF=",
                d2
            )

            print(
                "P2 OHLC:",
                f"O={r2['open']}",
                f"H={r2['high']}",
                f"L={r2['low']}",
                f"C={r2['close']}"
            )

    print()
    print("=" * 120)
    print("RESULT")
    print("=" * 120)

    print("TOTAL SIGNALS:", total)

    print(
        "P1 EXACT:",
        p1_exact,
        "/",
        total
    )

    print(
        "P2 EXACT:",
        p2_exact,
        "/",
        total
    )

    print(
        "BOTH EXACT:",
        sum(
            1
            for a, b in zip(
                [x for x in p1_miss],
                [x for x in p2_miss]
            )
        )
        if False else "see above"
    )

    if p1_miss:

        print()
        print("FIRST P1 MISMATCHES")
        print("-" * 120)

        for x in p1_miss[:5]:
            print(
                "SIGNAL=", x[0],
                "| BAR=", x[1],
                "| TIME=", x[2],
                "| PINE=", x[3],
                "| RAW=", x[4],
                "| DIFF=", x[5],
                "| O=", x[6],
                "| H=", x[7],
                "| L=", x[8],
                "| C=", x[9],
            )

    if p2_miss:

        print()
        print("FIRST P2 MISMATCHES")
        print("-" * 120)

        for x in p2_miss[:5]:
            print(
                "SIGNAL=", x[0],
                "| BAR=", x[1],
                "| TIME=", x[2],
                "| PINE=", x[3],
                "| RAW=", x[4],
                "| DIFF=", x[5],
                "| O=", x[6],
                "| H=", x[7],
                "| L=", x[8],
                "| C=", x[9],
            )

print()
print("=" * 120)
print("FINISHED")
print("=" * 120)
