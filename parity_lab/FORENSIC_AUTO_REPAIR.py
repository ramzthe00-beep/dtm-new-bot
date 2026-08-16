# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import hashlib
import re
import json
import csv
import difflib
import sys
import os

ROOT = Path.cwd()
LAB = ROOT / "parity_lab"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = LAB / f"FORENSIC_BACKUP_{STAMP}"
REPORT = LAB / f"FORENSIC_REPAIR_REPORT_{STAMP}.md"
CONSOLE = LAB / f"FORENSIC_REPAIR_LOG_{STAMP}.txt"

TARGETS = [
    ROOT / "strategy.py",
    ROOT / "dtm_bot.py",
    ROOT / "bot.py",
]

SYMBOLS = ["BNBUSDT", "DOGEUSDT", "ETHUSDT", "LTCUSDT"]

TOOLS = [
    LAB / "deep_analyzer.py",
    LAB / "pine_timestamp_ohlc_check.py",
    LAB / "pine_pivot_price_locator.py",
    LAB / "fast_spot_check.py",
]

events = []
changes = []
rejected = []
iterations = []

def say(x=""):
    print(x, flush=True)
    events.append(str(x))

def digest(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def snapshot():
    return {
        str(p): digest(p)
        for p in TARGETS
        if p.exists()
    }

def backup():
    BACKUP.mkdir(parents=True, exist_ok=True)

    for p in TARGETS:
        if p.exists():
            dst = BACKUP / p.relative_to(ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)

def restore():
    for p in TARGETS:
        src = BACKUP / p.relative_to(ROOT)
        if src.exists():
            shutil.copy2(src, p)

def run(cmd, timeout=180):
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=timeout,
        )
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except Exception as e:
        return 99, repr(e)

def run_tools(tag):
    outputs = []

    for tool in TOOLS:
        if not tool.exists():
            continue

        rc, out = run(f"python3 '{tool}'", 180)

        out_file = LAB / f"_FORENSIC_{tag}_{tool.stem}.txt"
        out_file.write_text(out, encoding="utf-8")

        outputs.append(out)

    return "\n".join(outputs)

def score(text):
    """
    Lower = better.

    We deliberately weight hard parity failures more heavily
    than ordinary textual warnings.
    """

    weights = {
        "MISMATCH": 20,
        "mismatch": 20,
        "PRICE IS NOT SAME-BAR": 20,
        "NOT SAME-BAR": 20,
        "FALSE": 10,
        "PIVOT MISMATCH": 30,
        "TIME MISMATCH": 30,
        "PRICE MISMATCH": 30,
        "OHLC MISMATCH": 30,
    }

    total = 0

    for pattern, weight in weights.items():
        total += len(re.findall(re.escape(pattern), text)) * weight

    return total

def source_text():
    result = {}

    for p in TARGETS:
        if p.exists():
            result[str(p)] = p.read_text(
                encoding="utf-8",
                errors="replace"
            )

    return result

def save_candidate(path, original):
    dst = BACKUP / "candidate" / path.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(original, encoding="utf-8")

def restore_candidate(path, original):
    path.write_text(original, encoding="utf-8")

def apply_candidate(path, new_text, reason, evidence):
    old_text = path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    if old_text == new_text:
        return False, None

    save_candidate(path, old_text)

    path.write_text(new_text, encoding="utf-8")

    rc, output = run_tools("candidate")

    new_score = score(output)

    if new_score <= CURRENT_SCORE[0]:
        change = {
            "file": str(path.relative_to(ROOT)),
            "reason": reason,
            "evidence": evidence,
            "before_score": CURRENT_SCORE[0],
            "after_score": new_score,
            "diff": "".join(
                difflib.unified_diff(
                    old_text.splitlines(True),
                    new_text.splitlines(True),
                    fromfile="BEFORE",
                    tofile="AFTER",
                )
            ),
        }

        changes.append(change)
        CURRENT_SCORE[0] = new_score

        say(
            f"[KEPT] {path.relative_to(ROOT)} "
            f"{CURRENT_SCORE[0]} <= previous"
        )

        return True, change

    restore_candidate(path, old_text)

    rejected.append({
        "file": str(path.relative_to(ROOT)),
        "reason": reason,
        "before_score": CURRENT_SCORE[0],
        "candidate_score": new_score,
    })

    say(
        f"[ROLLBACK] {path.relative_to(ROOT)} "
        f"{new_score} > {CURRENT_SCORE[0]}"
    )

    return False, None

# ============================================================
# START
# ============================================================

say("=" * 100)
say("DTM FORENSIC AUTOMATIC PINE <-> PYTHON REPAIR ENGINE")
say("=" * 100)
say("ANALYZE -> HYPOTHESIS -> CANDIDATE -> TEST -> KEEP/ROLLBACK")
say()

say("[1] FULL BACKUP")
backup()
say(f"BACKUP = {BACKUP}")

# ============================================================
# BASELINE
# ============================================================

say()
say("[2] BASELINE ANALYSIS")

baseline_output = run_tools("baseline")
baseline_score = score(baseline_output)

CURRENT_SCORE = [baseline_score]

say(f"BASELINE SCORE = {baseline_score}")

# ============================================================
# READ FORENSIC DATA
# ============================================================

samebar_file = LAB / "PIVOT_SAME_BAR_FORENSIC.txt"
locator_file = LAB / "PIVOT_PRICE_FORENSIC.txt"

samebar = (
    samebar_file.read_text(
        encoding="utf-8",
        errors="replace"
    )
    if samebar_file.exists()
    else ""
)

locator = (
    locator_file.read_text(
        encoding="utf-8",
        errors="replace"
    )
    if locator_file.exists()
    else ""
)

# ============================================================
# ROOT CAUSE DISCOVERY
# ============================================================

say()
say("[3] ROOT CAUSE DISCOVERY")

root_causes = []

if "PINE PRICE IS NOT SAME-BAR HIGH/LOW" in samebar:
    root_causes.append(
        "Pine pivot price does not map to same-timestamp OHLC."
    )

if "i+right" in source_text().get(
    str(ROOT / "strategy.py"),
    ""
).replace(" ", ""):
    root_causes.append(
        "strategy.py stores pivot value using confirmation-bar indexing."
    )

if ".shift(" in source_text().get(
    str(ROOT / "strategy.py"),
    ""
):
    root_causes.append(
        "strategy.py contains explicit pandas shift operation."
    )

combined = "\n".join(source_text().values())

if "pivot_state" in combined:
    root_causes.append(
        "Pivot state persistence is present."
    )

if "_pine_load_previous_state" in combined:
    root_causes.append(
        "Pine previous-state restoration is present."
    )

for r in root_causes:
    say("[ROOT CAUSE] " + r)

# ============================================================
# CANDIDATE REPAIR GENERATION
# ============================================================

say()
say("[4] GENERATING REPAIR CANDIDATES")

strategy = ROOT / "strategy.py"

if strategy.exists():

    original = strategy.read_text(
        encoding="utf-8",
        errors="replace"
    )

    # --------------------------------------------------------
    # CANDIDATE A
    # Remove only an EXPLICIT second RIGHT_BARS shift.
    # --------------------------------------------------------

    candidates = []

    candidates.append((
        r"last_confirmed\s*=\s*n\s*-\s*1\s*-\s*RIGHT_BARS\s*-\s*RIGHT_BARS",
        "last_confirmed = n - 1 - RIGHT_BARS",
        "Remove explicit double RIGHT_BARS shift.",
    ))

    candidates.append((
        r"last_confirmed\s*=\s*n\s*-\s*1\s*-\s*2\s*\*\s*RIGHT_BARS",
        "last_confirmed = n - 1 - RIGHT_BARS",
        "Remove explicit 2*RIGHT_BARS shift.",
    ))

    for pattern, replacement, reason in candidates:

        current = strategy.read_text(
            encoding="utf-8",
            errors="replace"
        )

        m = re.search(pattern, current)

        if not m:
            continue

        new_text = re.sub(
            pattern,
            replacement,
            current,
            count=1
        )

        say("[CANDIDATE] Explicit double-shift correction")

        apply_candidate(
            strategy,
            new_text,
            reason,
            f"Matched exact expression: {m.group(0)}"
        )

# ============================================================
# PIVOT SEMANTICS REPAIR
# ============================================================

say()
say("[5] PIVOT SOURCE/CONFIRMATION FORENSICS")

strategy_now = (
    strategy.read_text(
        encoding="utf-8",
        errors="replace"
    )
    if strategy.exists()
    else ""
)

# Find pivot functions.
pivot_functions = re.findall(
    r"def\s+pivot_(?:high|low)\s*\([^)]*\):.*?(?=\ndef\s+|\Z)",
    strategy_now,
    flags=re.S
)

for fn in pivot_functions:

    say()
    say("[PIVOT FUNCTION FOUND]")
    say(fn[:1500])

    # Critical rule:
    # Do not blindly change i+right.
    #
    # Instead check whether caller later shifts it again.

# ============================================================
# SEARCH ALL PYTHON FOR SECONDARY PIVOT SHIFTS
# ============================================================

say()
say("[6] SEARCHING FOR SECONDARY PIVOT SHIFTS")

for p in ROOT.rglob("*.py"):

    if "AUTO_REPAIR_BACKUP" in str(p):
        continue

    try:
        txt = p.read_text(
            encoding="utf-8",
            errors="replace"
        )
    except Exception:
        continue

    lines = txt.splitlines()

    for n, line in enumerate(lines, 1):

        low = line.lower()

        if (
            "pivot" in low
            and (
                "shift(" in low
                or "+right" in low
                or "-right" in low
                or "right_bars" in low
            )
        ):

            say(
                f"[PIVOT TRACE] "
                f"{p.relative_to(ROOT)}:{n}: {line.strip()}"
            )

# ============================================================
# TIMESTAMP FORENSICS
# ============================================================

say()
say("[7] TIMESTAMP / OHLC FORENSICS")

not_same = re.findall(
    r"([A-Z]+USDT).*?Pine bar=.*?Pine time=.*?Pine price=.*?"
    r".*?RESULT\s+:\s+PINE PRICE IS NOT SAME-BAR HIGH/LOW",
    samebar,
    flags=re.S
)

say(f"NON-SAME-BAR PIVOTS = {len(not_same)}")

# ============================================================
# LOCATOR OFFSET ANALYSIS
# ============================================================

say()
say("[8] PIVOT PRICE OFFSET ANALYSIS")

offset_lines = re.findall(
    r"(P1 OFFSETS|P2 OFFSETS):\s*\[([^\]]*)\]",
    locator
)

offset_values = []

for _, values in offset_lines:

    for x in values.split(","):

        x = x.strip()

        if not x:
            continue

        try:
            offset_values.append(int(x))
        except Exception:
            pass

if offset_values:

    positive = sum(x > 0 for x in offset_values)
    negative = sum(x < 0 for x in offset_values)
    zero = sum(x == 0 for x in offset_values)

    say(f"OFFSET ZERO     = {zero}")
    say(f"OFFSET POSITIVE = {positive}")
    say(f"OFFSET NEGATIVE = {negative}")

    if positive > 0 and negative > 0:
        say(
            "[FINDING] Offsets are not a constant shift. "
            "A single +N/-N correction would be invalid."
        )

# ============================================================
# INDICATOR SEMANTICS
# ============================================================

say()
say("[9] INDICATOR IMPLEMENTATION AUDIT")

indicator_patterns = {
    "RMA": r"\brma\s*\(",
    "EMA": r"\bema\s*\(",
    "RSI": r"\brsi\s*\(",
    "MACD": r"\bmacd\s*\(",
    "ATR": r"\batr\s*\(",
}

for name, pattern in indicator_patterns.items():

    found = False

    for p, txt in source_text().items():

        if re.search(pattern, txt, re.I):

            say(
                f"[FOUND] {name} implementation/reference "
                f"in {Path(p).relative_to(ROOT)}"
            )

            found = True

    if not found:
        say(f"[NOT FOUND] {name}")

# ============================================================
# STATE AUDIT
# ============================================================

say()
say("[10] STATE / PERSISTENCE AUDIT")

for p, txt in source_text().items():

    for pattern in [
        "pivot_state",
        "_pine_load_previous_state",
        "json.load",
        "json.dump",
        "state_file",
    ]:

        if pattern.lower() in txt.lower():

            say(
                f"[STATE] {Path(p).relative_to(ROOT)} "
                f"contains {pattern}"
            )

# ============================================================
# SIGNAL DEPENDENCY AUDIT
# ============================================================

say()
say("[11] DOWNSTREAM SIGNAL DEPENDENCY AUDIT")

for p, txt in source_text().items():

    checks = [
        "divergence",
        "fibonacci",
        "fib",
        "score",
        "signal",
        "pivot",
        "candle",
    ]

    found = [
        x for x in checks
        if x in txt.lower()
    ]

    if found:
        say(
            f"{Path(p).relative_to(ROOT)} -> "
            + ", ".join(found)
        )

# ============================================================
# RE-RUN AFTER ALL VERIFIED CANDIDATES
# ============================================================

say()
say("[12] FINAL PARITY VERIFICATION")

final_output = run_tools("final")
final_score = score(final_output)

say(f"BASELINE SCORE = {baseline_score}")
say(f"FINAL SCORE    = {final_score}")

if final_score > baseline_score:

    say("[FATAL] FINAL SCORE WORSE -> RESTORING FULL BACKUP")

    restore()

    final_output = run_tools("restored")
    final_score = score(final_output)

    say(f"RESTORED SCORE = {final_score}")

# ============================================================
# REPORT
# ============================================================

say()
say("[13] WRITING COMPLETE REPORT")

report = []

report.append("# DTM FORENSIC AUTOMATIC REPAIR REPORT")
report.append("")
report.append(f"Date: {datetime.now().isoformat()}")
report.append("")
report.append("## FINAL RESULT")
report.append("")
report.append(f"- Baseline score: **{baseline_score}**")
report.append(f"- Final score: **{final_score}**")
report.append(f"- Accepted repairs: **{len(changes)}**")
report.append(f"- Rejected repairs: **{len(rejected)}**")
report.append("")

report.append("## ROOT CAUSES")
report.append("")

if root_causes:
    for r in root_causes:
        report.append(f"- {r}")
else:
    report.append("- No root cause detected by current forensic evidence.")

report.append("")
report.append("## ACCEPTED REPAIRS")
report.append("")

if changes:

    for i, c in enumerate(changes, 1):

        report.append(f"### REPAIR {i}")
        report.append("")
        report.append(f"**FILE:** `{c['file']}`")
        report.append("")
        report.append(f"**REASON:** {c['reason']}")
        report.append("")
        report.append(f"**EVIDENCE:** {c['evidence']}")
        report.append("")
        report.append(
            f"**PARITY:** {c['before_score']} -> {c['after_score']}"
        )
        report.append("")
        report.append("```diff")
        report.append(c["diff"])
        report.append("```")
        report.append("")

else:
    report.append(
        "No source-code repair was mathematically validated."
    )
    report.append("")

report.append("## REJECTED CANDIDATES")
report.append("")

if rejected:

    for r in rejected:

        report.append(
            f"- `{r['file']}` — {r['reason']} — "
            f"{r['before_score']} -> {r['candidate_score']}"
        )

else:
    report.append("- None")

report.append("")
report.append("## PIVOT FORENSICS")
report.append("")
report.append(
    "The engine does NOT assume that Pine pivot price must equal "
    "the High/Low of the candle carrying the logged pivot timestamp."
)
report.append("")
report.append(
    "Source-bar identity and confirmation-bar identity are treated "
    "as separate concepts."
)

report.append("")
report.append("## FILES THAT WERE ANALYZED")
report.append("")

for p in TARGETS:

    if p.exists():
        report.append(
            f"- `{p.relative_to(ROOT)}`"
        )

report.append("")
report.append("## BACKUP")
report.append("")
report.append(str(BACKUP))
report.append("")
report.append("## FINAL TEST OUTPUT")
report.append("")
report.append("```text")
report.append(final_output[-20000:])
report.append("```")

REPORT.write_text(
    "\n".join(report),
    encoding="utf-8"
)

Path(CONSOLE).write_text(
    "\n".join(events),
    encoding="utf-8"
)

say()
say("=" * 100)
say("FORENSIC AUTOMATIC REPAIR COMPLETE")
say("=" * 100)
say(f"REPORT     : {REPORT}")
say(f"BACKUP     : {BACKUP}")
say(f"BASELINE   : {baseline_score}")
say(f"FINAL      : {final_score}")
say(f"REPAIRS    : {len(changes)}")
say(f"REJECTED   : {len(rejected)}")
say("=" * 100)
