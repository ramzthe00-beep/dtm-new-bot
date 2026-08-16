#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import math
import subprocess
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path.home() / "dtm-new-bot"
OUT = ROOT / "parity_lab" / "DEEP_ANALYSIS_REPORT.md"

PY_FILES = list(ROOT.glob("*.py")) + list((ROOT / "parity_lab").glob("*.py"))
CSV_FILES = sorted(ROOT.glob("pine_*.csv"))

def run(cmd):
    try:
        p = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        return p.stdout
    except Exception as e:
        return f"[COMMAND ERROR] {e}"

def section(title):
    return f"\n\n{'='*80}\n{title}\n{'='*80}\n"

report = []

report.append("# DTM — DEEP PINE ↔ PYTHON PARITY ANALYSIS")
report.append("\n**MODE: READ-ONLY / NO CODE MODIFICATION**\n")

# ------------------------------------------------------------
# 1. Project inventory
# ------------------------------------------------------------

report.append(section("1. PROJECT INVENTORY"))

report.append("## Python files\n")
for p in PY_FILES:
    try:
        report.append(f"- `{p.relative_to(ROOT)}` ({p.stat().st_size} bytes)")
    except:
        pass

report.append("\n## Pine CSV files\n")
for p in CSV_FILES:
    report.append(f"- `{p.name}` ({p.stat().st_size} bytes)")

# ------------------------------------------------------------
# 2. Exact pivot/state/shift search
# ------------------------------------------------------------

report.append(section("2. PIVOT / STATE / SHIFT STATIC ANALYSIS"))

patterns = [
    "pivot",
    "_pine_load_previous_state",
    "pivot_state",
    "bar_index",
    "shift",
    "RIGHT_BARS",
    "LEFT_BARS",
    "pivothigh",
    "pivotlow",
]

for pat in patterns:
    report.append(f"\n### SEARCH: `{pat}`\n")
    out = run([
        "rg", "-n", "-i",
        "--glob", "*.py",
        pat,
        "."
    ])
    report.append("```text\n" + out + "\n```")

# ------------------------------------------------------------
# 3. strategy.py exact source
# ------------------------------------------------------------

strategy = ROOT / "strategy.py"

if strategy.exists():
    report.append(section("3. strategy.py SOURCE"))

    lines = strategy.read_text(encoding="utf-8", errors="replace").splitlines()

    for i, line in enumerate(lines, 1):
        report.append(f"{i:04d}: {line}")

# ------------------------------------------------------------
# 4. CSV structural analysis
# ------------------------------------------------------------

report.append(section("4. PINE CSV STRUCTURAL ANALYSIS"))

for csv in CSV_FILES:
    report.append(f"\n## {csv.name}\n")

    try:
        import pandas as pd

        df = pd.read_csv(csv)

        report.append(f"- rows: `{len(df)}`")
        report.append(f"- columns: `{list(df.columns)}`")

        report.append("\n### dtypes\n")
        report.append("```text\n")
        report.append(str(df.dtypes))
        report.append("\n```\n")

        report.append("\n### first rows\n")
        report.append("```text\n")
        report.append(df.head(3).to_string())
        report.append("\n```\n")

        report.append("\n### last rows\n")
        report.append("```text\n")
        report.append(df.tail(3).to_string())
        report.append("\n```\n")

    except Exception as e:
        report.append(f"CSV ERROR: `{e}`")

# ------------------------------------------------------------
# 5. Timestamp/index analysis
# ------------------------------------------------------------

report.append(section("5. TIMESTAMP / INDEX / BAR ALIGNMENT ANALYSIS"))

for csv in CSV_FILES:
    try:
        import pandas as pd

        df = pd.read_csv(csv)

        report.append(f"\n## {csv.name}\n")

        for c in df.columns:
            lc = c.lower()

            if (
                "time" in lc
                or "timestamp" in lc
                or "date" in lc
                or "bar" in lc
                or "index" in lc
            ):
                report.append(f"\n### Column `{c}`\n")
                report.append(f"- dtype: `{df[c].dtype}`")
                report.append(f"- unique: `{df[c].nunique(dropna=False)}`")
                report.append(f"- nulls: `{df[c].isna().sum()}`")

        # duplicate rows
        report.append(
            f"\n- duplicate rows: `{df.duplicated().sum()}`"
        )

    except Exception as e:
        report.append(f"ERROR: {e}")

# ------------------------------------------------------------
# 6. Numeric precision analysis
# ------------------------------------------------------------

report.append(section("6. NUMERIC PRECISION / OHLC ANALYSIS"))

for csv in CSV_FILES:
    try:
        import pandas as pd
        import numpy as np

        df = pd.read_csv(csv)

        report.append(f"\n## {csv.name}\n")

        for c in ["open", "high", "low", "close"]:
            if c in df.columns:
                s = pd.to_numeric(df[c], errors="coerce")

                report.append(
                    f"- `{c}`: rows={s.notna().sum()}, "
                    f"min={s.min()}, max={s.max()}, "
                    f"unique={s.nunique()}"
                )

                # decimal precision distribution
                vals = s.dropna().astype(str)

                precision = []
                for v in vals.head(5000):
                    if "." in v:
                        precision.append(len(v.split(".")[1]))
                    else:
                        precision.append(0)

                if precision:
                    report.append(
                        f"  - decimal precision: "
                        f"{Counter(precision).most_common(10)}"
                    )

    except Exception as e:
        report.append(f"ERROR: {e}")

# ------------------------------------------------------------
# 7. Pivot implementation mathematical inspection
# ------------------------------------------------------------

report.append(section("7. PIVOT MATHEMATICAL INSPECTION"))

if strategy.exists():

    text = strategy.read_text(
        encoding="utf-8",
        errors="replace"
    )

    checks = {
        "pivot_high_storage": r"out\.iloc\[i\+right\]\s*=",
        "pivot_low_storage": r"out\.iloc\[i\+right\]\s*=",
        "last_confirmed_minus_right": r"n\s*-\s*1\s*-\s*RIGHT_BARS",
        "shift_usage": r"\.shift\s*\(",
        "bar_index_usage": r"bar_index",
        "state_usage": r"pivot_state|_pine_load_previous_state",
    }

    for name, pattern in checks.items():
        found = bool(re.search(pattern, text, re.I))
        report.append(f"- `{name}` → **{'FOUND' if found else 'NOT FOUND'}**")

    report.append("""
### Interpretation rules

The analyzer must distinguish:

1. Pivot source bar
2. Pivot confirmation bar
3. Storage location
4. Read location
5. Previous-pivot location
6. State-restored location

A `+RIGHT_BARS` during storage is not automatically wrong.

A `-RIGHT_BARS` during read is not automatically wrong.

The question is whether the two operations together reproduce Pine's
series semantics exactly.

Therefore no fix is declared from pattern matching alone.
""")

# ------------------------------------------------------------
# 8. Run existing parity tools
# ------------------------------------------------------------

report.append(section("8. EXISTING PARITY LAB RESULTS"))

tools = [
    "parity_lab/pine_pivot_price_locator.py",
    "parity_lab/pine_timestamp_ohlc_check.py",
    "parity_lab/fast_spot_check.py",
]

for tool in tools:

    p = ROOT / tool

    if not p.exists():
        continue

    report.append(f"\n## `{tool}`\n")

    out = run(["python", str(p)])

    report.append("```text\n")
    report.append(out[-20000:])
    report.append("\n```\n")

# ------------------------------------------------------------
# 9. Git diff / modification detection
# ------------------------------------------------------------

report.append(section("9. CURRENT WORKTREE STATE"))

report.append("```text\n")
report.append(run(["git", "status", "--short"]))
report.append("\n```\n")

report.append("```text\n")
report.append(run(["git", "diff", "--", "*.py"]))
report.append("\n```\n")

# ------------------------------------------------------------
# 10. Required root-cause classification
# ------------------------------------------------------------

report.append(section("10. ROOT-CAUSE CLASSIFICATION"))

report.append("""
The final diagnosis must classify each discrepancy as one of:

P0 — DATA SOURCE / CANDLE ALIGNMENT
P0 — PIVOT INDEXING / CONFIRMATION SEMANTICS
P0 — STATE RESTORATION / DOUBLE SHIFT

P1 — RSI/RMA/EMA initialization
P1 — MACD semantics
P1 — divergence comparison
P1 — NaN propagation

P2 — signal timing
P2 — candle confirmation
P2 — precision/tolerance

For every claimed root cause provide:

- exact file
- exact line
- exact expression
- expected Pine behavior
- actual Python behavior
- concrete evidence
- affected symbols
- affected bars
- confidence percentage

NO CODE CHANGES ARE PERMITTED DURING THIS ANALYSIS.
""")

# ------------------------------------------------------------
# 11. Final recommendation
# ------------------------------------------------------------

report.append(section("11. FINAL VERDICT"))

report.append("""
Do not recommend a fix until the evidence establishes the first point
where Pine and Python diverge.

The correct debugging order is:

DATA
→ INDEX/BAR ALIGNMENT
→ PIVOT SOURCE/CONFIRMATION
→ PIVOT STATE
→ P1/P2 SELECTION
→ INDICATORS
→ DIVERGENCE
→ SIGNAL

The first mathematically proven divergence is the root-cause candidate.
Later differences may simply be downstream consequences.
""")

OUT.write_text("\n".join(report), encoding="utf-8")

print("=" * 80)
print("DEEP ANALYSIS FINISHED")
print("=" * 80)
print(f"REPORT: {OUT}")
print()
print("NO PROJECT FILE WAS MODIFIED.")
