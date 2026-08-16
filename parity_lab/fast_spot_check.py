import pandas as pd
import re
import os
from pathlib import Path

RAW = {
    "BNBUSDT": "parity_lab/raw_data/BNBUSDT_1m_binance_spot.csv",
    "LTCUSDT": "parity_lab/raw_data/LTCUSDT_1m_binance_spot.csv",
    "DOGEUSDT": "parity_lab/raw_data/DOGEUSDT_1m_binance_spot.csv",
    "ETHUSDT": "parity_lab/raw_data/ETHUSDT_1m_binance_spot.csv",
}

PINE = {
    "BNBUSDT": "parity_lab/pine_logs/pine_10.csv",
    "LTCUSDT": "parity_lab/pine_logs/pine_11.csv",
    "DOGEUSDT": "parity_lab/pine_logs/pine_12.csv",
    "ETHUSDT": "parity_lab/pine_logs/pine_13.csv",
}

SIG = re.compile(r"🔔\s*(CD\+|CD-|HD\+|HD-)")
CUR = re.compile(r"📌\s*کندل فعلی:\s*(\d+)")
P1 = re.compile(r"Pivot اول:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)")
P2 = re.compile(r"Pivot دوم:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)")

print("=" * 100)
print("PINE <-> BINANCE SPOT RAW OHLC DIAGNOSTIC")
print("=" * 100)

for symbol in RAW:

    print("\n" + "=" * 100)
    print(symbol)
    print("=" * 100)

    raw = pd.read_csv(
        RAW[symbol],
        usecols=["time", "open", "high", "low", "close"]
    )

    raw["time"] = pd.to_datetime(raw["time"], utc=True)
    raw = raw.sort_values("time").reset_index(drop=True)

    times = raw["time"].to_numpy()
    opens = raw["open"].to_numpy()
    highs = raw["high"].to_numpy()
    lows = raw["low"].to_numpy()
    closes = raw["close"].to_numpy()

    pine = pd.read_csv(PINE[symbol], usecols=["Message"])

    records = []

    for msg in pine["Message"].astype(str):

        sig = SIG.search(msg)
        cur = CUR.search(msg)
        p1 = P1.search(msg)
        p2 = P2.search(msg)

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

        if signal.endswith("-"):
            source = "HIGH"
            raw_p1 = float(highs[p1_bar])
            raw_p2 = float(highs[p2_bar])
        else:
            source = "LOW"
            raw_p1 = float(lows[p1_bar])
            raw_p2 = float(lows[p2_bar])

        records.append({
            "signal": signal,

            "cur_bar": cur_bar,
            "cur_time": str(times[cur_bar]),

            "p1_bar": p1_bar,
            "p1_time": str(times[p1_bar]),
            "pine_p1": p1_price,
            "raw_p1": raw_p1,
            "diff_p1": raw_p1 - p1_price,

            "p2_bar": p2_bar,
            "p2_time": str(times[p2_bar]),
            "pine_p2": p2_price,
            "raw_p2": raw_p2,
            "diff_p2": raw_p2 - p2_price,

            "source": source
        })

    print("RAW ROWS       :", len(raw))
    print("PINE SIGNALS   :", len(records))

    if not records:
        print("NO PARSED SIGNALS")
        continue

    df = pd.DataFrame(records)

    df["abs_p1"] = df["diff_p1"].abs()
    df["abs_p2"] = df["diff_p2"].abs()

    print()
    print("FIRST 10")
    print("-" * 100)

    for _, r in df.head(10).iterrows():

        print(
            f"{r['signal']:4s} "
            f"P1 bar={int(r['p1_bar']):5d} "
            f"{r['p1_time']} "
            f"PINE={r['pine_p1']:.12f} "
            f"RAW={r['raw_p1']:.12f} "
            f"DIFF={r['diff_p1']:+.12f}"
        )

        print(
            f"     "
            f"P2 bar={int(r['p2_bar']):5d} "
            f"{r['p2_time']} "
            f"PINE={r['pine_p2']:.12f} "
            f"RAW={r['raw_p2']:.12f} "
            f"DIFF={r['diff_p2']:+.12f}"
        )

    print()
    print("STATISTICS")
    print("-" * 100)

    print(
        "P1 <= 1e-8 :",
        int((df["abs_p1"] <= 1e-8).sum()),
        "/",
        len(df)
    )

    print(
        "P2 <= 1e-8 :",
        int((df["abs_p2"] <= 1e-8).sum()),
        "/",
        len(df)
    )

    print(
        "P1 EXACT   :",
        int((df["abs_p1"] == 0).sum()),
        "/",
        len(df)
    )

    print(
        "P2 EXACT   :",
        int((df["abs_p2"] == 0).sum()),
        "/",
        len(df)
    )

    print(
        "P1 DIFF MIN/MAX:",
        df["diff_p1"].min(),
        df["diff_p1"].max()
    )

    print(
        "P2 DIFF MIN/MAX:",
        df["diff_p2"].min(),
        df["diff_p2"].max()
    )

    out = Path("parity_lab/results")
    out.mkdir(parents=True, exist_ok=True)

    outfile = out / f"{symbol}_spot_raw_comparison.csv"

    df.to_csv(outfile, index=False)

    print("SAVED:", outfile)

print()
print("=" * 100)
print("DIAGNOSTIC FINISHED")
print("=" * 100)
