import os, re, csv, glob, math
from pathlib import Path

ROOT = Path.cwd()
LAB = ROOT / "parity_lab"

print("=" * 80)
print("DTM — AUTOMATIC PINE ↔ PYTHON PARITY AUDITOR")
print("=" * 80)
print("MODE: READ-ONLY ANALYSIS")
print("NO PROJECT FILE WILL BE MODIFIED")
print()

issues = []
warnings = []
checks = []

def issue(severity, area, problem, evidence, cause, fix):
    issues.append({
        "severity": severity,
        "area": area,
        "problem": problem,
        "evidence": evidence,
        "cause": cause,
        "fix": fix,
    })

def read(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def check_file(path):
    if path.exists():
        checks.append(f"[OK] {path.relative_to(ROOT)}")
        return True
    checks.append(f"[MISS] {path.relative_to(ROOT)}")
    return False

# ---------------------------------------------------------------------
# 1. INVENTORY
# ---------------------------------------------------------------------

print("[1/9] PROJECT INVENTORY")

python_files = list(ROOT.glob("*.py")) + list(LAB.glob("*.py"))
pine_files = list(ROOT.rglob("*.pine"))
csv_files = list(LAB.rglob("*.csv"))

for f in python_files:
    print(f"  PYTHON : {f.relative_to(ROOT)}")

for f in pine_files:
    print(f"  PINE   : {f.relative_to(ROOT)}")

for f in csv_files:
    print(f"  CSV    : {f.relative_to(ROOT)}")

print()

# ---------------------------------------------------------------------
# 2. SOURCE CODE STATIC AUDIT
# ---------------------------------------------------------------------

print("[2/9] PYTHON STATIC SEMANTIC AUDIT")

strategy = ROOT / "strategy.py"
dtm = ROOT / "dtm_bot.py"

strategy_text = read(strategy)
dtm_text = read(dtm)

combined = strategy_text + "\n" + dtm_text

# Pivot settings
lb = re.search(r'LEFT_BARS\s*=\s*(\d+)', combined)
rb = re.search(r'RIGHT_BARS\s*=\s*(\d+)', combined)

left = int(lb.group(1)) if lb else None
right = int(rb.group(1)) if rb else None

print(f"  LEFT_BARS  = {left}")
print(f"  RIGHT_BARS = {right}")

if left != 5:
    issue(
        "HIGH", "PIVOT",
        "LEFT_BARS differs from expected Pine setting",
        f"Python LEFT_BARS={left}",
        "Pivot window is not identical to Pine configuration",
        "Set LEFT_BARS to the exact Pine value."
    )

if right != 3:
    issue(
        "HIGH", "PIVOT",
        "RIGHT_BARS differs from expected Pine setting",
        f"Python RIGHT_BARS={right}",
        "Pivot confirmation window differs",
        "Set RIGHT_BARS to the exact Pine value."
    )

# Detect storage shift
if re.search(r'out\.iloc\[i\+right\]\s*=\s*x', strategy_text):
    issue(
        "HIGH", "PIVOT INDEX",
        "Pivot value is stored on confirmation bar",
        "strategy.py contains out.iloc[i+right] = x",
        "This can be correct only if every downstream consumer treats the value as a confirmed pivot while preserving source-bar identity. Mixing source and confirmation indices causes systematic shift.",
        "Keep source index and confirmation index explicitly separate. Never apply another right-bar shift later."
    )

# Detect pandas shift
if re.search(r'\.shift\s*\(', strategy_text):
    print("  [INFO] pandas shift() detected")

# Detect previous-state patterns
for pat, name in [
    (r'_pine_load_previous_state', "previous Pine state loader"),
    (r'pivot_state', "pivot state"),
    (r'bar_index', "bar_index"),
]:
    if re.search(pat, combined):
        print(f"  [FOUND] {name}")

# ---------------------------------------------------------------------
# 3. INDICATOR SEMANTICS
# ---------------------------------------------------------------------

print()
print("[3/9] INDICATOR SEMANTICS AUDIT")

expected = {
    "RSI_LEN": 14,
    "MACD_FAST": 12,
    "MACD_SLOW": 26,
    "MACD_SIG": 9,
}

for name, value in expected.items():
    m = re.search(rf'{name}\s*=\s*(\d+)', combined)
    actual = int(m.group(1)) if m else None
    print(f"  {name}: Python={actual} expected={value}")
    if actual != value:
        issue(
            "HIGH", "INDICATORS",
            f"{name} mismatch",
            f"Python={actual}, expected={value}",
            "Indicator parameters are not identical",
            f"Set {name} exactly to {value}."
        )

if "def rma" in strategy_text:
    print("  [FOUND] custom RMA")
else:
    issue(
        "HIGH", "RMA",
        "No custom RMA implementation found",
        "strategy.py does not contain def rma",
        "Pine ta.rma is Wilder smoothing and cannot safely be replaced with arbitrary pandas rolling/ewm semantics.",
        "Implement and validate exact Pine ta.rma behavior."
    )

if "def ema" in strategy_text:
    print("  [FOUND] custom EMA")
else:
    issue(
        "HIGH", "EMA",
        "No custom EMA implementation found",
        "strategy.py does not contain def ema",
        "EMA seeding can create persistent differences.",
        "Implement exact Pine EMA initialization and recurrence."
    )

# ---------------------------------------------------------------------
# 4. DATA FILE AUDIT
# ---------------------------------------------------------------------

print()
print("[4/9] DATA / ALIGNMENT AUDIT")

raw = sorted((LAB / "raw_data").glob("*.csv"))
pine_logs = sorted((LAB / "pine_logs").glob("*.csv"))
python_logs = sorted((LAB / "python_logs").glob("*.csv"))
results = sorted((LAB / "results").glob("*.csv"))

print(f"  Raw CSVs     : {len(raw)}")
print(f"  Pine logs    : {len(pine_logs)}")
print(f"  Python logs  : {len(python_logs)}")
print(f"  Result CSVs  : {len(results)}")

def rows(path):
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

for f in raw:
    n = rows(f)
    print(f"  RAW {f.name}: {n} lines")

for f in pine_logs:
    print(f"  PINE {f.name}: {rows(f)} lines")

for f in python_logs:
    print(f"  PY {f.name}: {rows(f)} lines")

# Detect suspicious alignment sizes
for f in raw:
    if "aligned" in f.name.lower():
        n = rows(f)
        if n != 5000 and n != 8222:
            warnings.append(
                f"Suspicious aligned dataset size: {f.name}={n}"
            )

# ---------------------------------------------------------------------
# 5. CSV STRUCTURE / TIMESTAMP AUDIT
# ---------------------------------------------------------------------

print()
print("[5/9] CSV TIMESTAMP / OHLC AUDIT")

def csv_header(path):
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            return next(csv.reader(f), [])
    except Exception:
        return []

for f in raw:
    h = csv_header(f)
    low = [x.lower().strip() for x in h]

    has_time = any(x in low for x in [
        "timestamp", "time", "datetime", "open_time", "bar_time"
    ])

    has_ohlc = all(x in low for x in ["open", "high", "low", "close"])

    if not has_time:
        issue(
            "HIGH", "DATA ALIGNMENT",
            f"No recognizable timestamp column in {f.name}",
            str(h),
            "Without a stable bar identity, Pine and Python can compare different candles while appearing aligned.",
            "Use the exact exchange/Pine bar timestamp as the primary key."
        )

    if not has_ohlc:
        issue(
            "HIGH", "DATA OHLC",
            f"Missing OHLC columns in {f.name}",
            str(h),
            "Indicator and pivot parity cannot be guaranteed without identical OHLC.",
            "Normalize both datasets to timestamp/open/high/low/close."
        )

# ---------------------------------------------------------------------
# 6. PIVOT PARITY RESULTS
# ---------------------------------------------------------------------

print()
print("[6/9] PIVOT PARITY RESULTS")

pivot_results = sorted((LAB / "results").glob("*pivot*parity*.csv"))

if not pivot_results:
    issue(
        "CRITICAL", "PIVOT PARITY",
        "No pivot parity result was found",
        "No *pivot*parity*.csv",
        "The current evidence cannot prove Pine and Python pivot identity.",
        "Run the pivot parity generator before modifying trading logic."
    )
else:
    for f in pivot_results:
        n = rows(f)
        print(f"  {f.name}: {n} lines")

        try:
            with f.open("r", encoding="utf-8", errors="replace") as fh:
                reader = csv.DictReader(fh)
                headers = reader.fieldnames or []

                print("    columns:", ", ".join(headers))

                status_cols = [
                    x for x in headers
                    if any(k in x.lower() for k in
                           ["status", "match", "equal", "diff", "parity"])
                ]

                for row in reader:
                    text = " ".join(str(v) for v in row.values()).lower()

                    bad = any(k in text for k in [
                        "mismatch", "different", "false", "fail", "wrong"
                    ])

                    if bad:
                        issue(
                            "CRITICAL", "PIVOT PARITY",
                            "Pivot mismatch detected in parity result",
                            str(row),
                            "Python pivot source/confirmation/state does not match Pine for at least one bar.",
                            "Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%."
                        )
        except Exception as e:
            warnings.append(f"Could not parse {f.name}: {e}")

# ---------------------------------------------------------------------
# 7. SIGNAL DENSITY AUDIT
# ---------------------------------------------------------------------

print()
print("[7/9] SIGNAL OUTPUT AUDIT")

for f in python_logs:
    if "signals" in f.name.lower():
        n = max(0, rows(f) - 1)
        print(f"  {f.name}: approximately {n} signal rows")

        if n <= 1:
            warnings.append(
                f"{f.name} has extremely low signal count ({n}); "
                "this may indicate an upstream parity failure rather than a valid strategy result."
            )

# ---------------------------------------------------------------------
# 8. AUTOMATIC ROOT-CAUSE CLASSIFICATION
# ---------------------------------------------------------------------

print()
print("[8/9] ROOT-CAUSE CLASSIFICATION")

categories = {
    "PIVOT": 0,
    "DATA ALIGNMENT": 0,
    "INDICATORS": 0,
    "RMA": 0,
    "EMA": 0,
    "PIVOT INDEX": 0,
    "PIVOT PARITY": 0,
}

for x in issues:
    area = x["area"]
    if area in categories:
        categories[area] += 1

for k, v in categories.items():
    print(f"  {k:20s}: {v}")

# Highest priority root cause
if categories["PIVOT PARITY"] or categories["PIVOT INDEX"] or categories["PIVOT"]:
    root = "PIVOT / INDEXING / STATE"
    root_reason = (
        "Pivot identity is upstream of divergence, Fibonacci, scoring and final signals. "
        "If pivot source/confirmation indexing is wrong, every downstream signal can move or disappear."
    )
elif categories["DATA ALIGNMENT"]:
    root = "DATA / TIMESTAMP ALIGNMENT"
    root_reason = (
        "If Pine and Python do not operate on the exact same candle identity, "
        "all indicator and signal comparisons become invalid."
    )
elif categories["RMA"] or categories["EMA"] or categories["INDICATORS"]:
    root = "INDICATOR SEMANTICS"
    root_reason = (
        "Indicator initialization/smoothing differences can propagate into divergence and signals."
    )
else:
    root = "NO STATIC ROOT CAUSE PROVEN"
    root_reason = (
        "Static analysis did not prove a single root cause. Dynamic per-bar comparison is required."
    )

# ---------------------------------------------------------------------
# 9. FINAL REPORT
# ---------------------------------------------------------------------

report = LAB / "AUTO_PARITY_AUDIT_REPORT.md"

with report.open("w", encoding="utf-8") as out:
    out.write("# DTM — AUTOMATIC PINE ↔ PYTHON PARITY AUDIT\n\n")
    out.write("MODE: READ-ONLY\n\n")

    out.write("## FINAL VERDICT\n\n")
    out.write(f"**PRIMARY ROOT CAUSE: {root}**\n\n")
    out.write(f"{root_reason}\n\n")

    out.write("## ISSUES\n\n")

    if not issues:
        out.write("No static issues were proven.\n\n")
    else:
        for i, x in enumerate(issues, 1):
            out.write(f"### {i}. [{x['severity']}] {x['area']}\n\n")
            out.write(f"**Problem:** {x['problem']}\n\n")
            out.write(f"**Evidence:** `{x['evidence']}`\n\n")
            out.write(f"**Likely cause:** {x['cause']}\n\n")
            out.write(f"**Required correction:** {x['fix']}\n\n")

    out.write("## WARNINGS\n\n")
    for w in warnings:
        out.write(f"- {w}\n")

    out.write("\n## PROJECT FILES\n\n")
    for c in checks:
        out.write(f"- {c}\n")

    out.write("\n## RECOMMENDED ORDER OF CORRECTION\n\n")
    order = [
        "1. Verify exact timestamp/bar identity.",
        "2. Verify Pine pivot source bar versus confirmation bar.",
        "3. Verify pivot state persistence and eliminate any second shift.",
        "4. Re-run pivot parity until it is 100%.",
        "5. Compare RMA/EMA/RSI/MACD per bar.",
        "6. Compare divergence inputs.",
        "7. Compare Fibonacci and candle filters.",
        "8. Compare final score and signal.",
    ]
    for x in order:
        out.write(x + "\n")

print()
print("=" * 80)
print("FINAL VERDICT")
print("=" * 80)
print("PRIMARY ROOT CAUSE:", root)
print(root_reason)
print()

if issues:
    print("ISSUES FOUND:", len(issues))
    for i, x in enumerate(issues, 1):
        print()
        print(f"{i}. [{x['severity']}] {x['area']}")
        print("   PROBLEM :", x["problem"])
        print("   EVIDENCE:", x["evidence"])
        print("   CAUSE   :", x["cause"])
        print("   FIX     :", x["fix"])
else:
    print("NO STATIC ISSUES PROVEN.")

print()
print("WARNINGS:", len(warnings))
for w in warnings:
    print(" -", w)

print()
print("=" * 80)
print("REPORT:", report)
print("NO PROJECT FILE WAS MODIFIED.")
print("=" * 80)
