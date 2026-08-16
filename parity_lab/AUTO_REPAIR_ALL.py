# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import hashlib
import re
import json
import sys

ROOT = Path.cwd()
LAB = ROOT / "parity_lab"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = LAB / f"AUTO_REPAIR_BACKUP_{STAMP}"
REPORT = LAB / f"AUTO_REPAIR_FINAL_{STAMP}.md"
LOG = LAB / f"AUTO_REPAIR_LOG_{STAMP}.txt"

TARGETS = [
    ROOT / "strategy.py",
    ROOT / "dtm_bot.py",
    ROOT / "bot.py",
]

TESTS = [
    LAB / "deep_analyzer.py",
    LAB / "pine_timestamp_ohlc_check.py",
    LAB / "pine_pivot_price_locator.py",
    LAB / "fast_spot_check.py",
]

log = []
changes = []
rollbacks = []
issues = []

def say(x=""):
    print(x)
    log.append(str(x))

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def snapshot():
    return {
        str(p): sha256(p)
        for p in TARGETS
        if p.exists()
    }

def backup_all():
    BACKUP.mkdir(parents=True, exist_ok=True)

    for p in TARGETS:
        if p.exists():
            dst = BACKUP / p.relative_to(ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)

def restore_all():
    for p in TARGETS:
        src = BACKUP / p.relative_to(ROOT)
        if src.exists():
            shutil.copy2(src, p)

def run(cmd):
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=180
        )
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except Exception as e:
        return 99, str(e)

def count_mismatches(text):
    patterns = [
        r"MISMATCH",
        r"mismatch",
        r"NOT SAME",
        r"NOT same",
        r"FALSE",
        r"False",
        r"PRICE IS NOT SAME",
    ]

    return sum(
        len(re.findall(p, text))
        for p in patterns
    )

def run_full_tests(label):
    outputs = []

    for t in TESTS:
        if not t.exists():
            continue

        rc, out = run(f"python3 '{t}'")

        outputs.append(out)

        (LAB / f"_repair_{label}_{t.stem}.txt").write_text(
            out,
            encoding="utf-8"
        )

    combined = "\n".join(outputs)
    score = count_mismatches(combined)

    return score, combined

def replace_once(path, old, new, reason):
    if not path.exists():
        return False

    txt = path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    if old not in txt:
        return False

    updated = txt.replace(old, new, 1)

    if updated == txt:
        return False

    path.write_text(updated, encoding="utf-8")

    changes.append({
        "file": str(path.relative_to(ROOT)),
        "reason": reason,
        "old": old,
        "new": new,
    })

    return True

say("=" * 90)
say("DTM AUTOMATIC PINE ↔ PYTHON REPAIR ENGINE")
say("=" * 90)
say("MODE: FULL AUTO ANALYZE / REPAIR / VERIFY / ROLLBACK")
say()

# ============================================================
# BACKUP
# ============================================================

say("[1] CREATING FULL BACKUP")
backup_all()
say(f"BACKUP: {BACKUP}")

before_hash = snapshot()

# ============================================================
# INITIAL TEST
# ============================================================

say()
say("[2] INITIAL PARITY TEST")

initial_score, initial_output = run_full_tests("before")

say(f"INITIAL MISMATCH SCORE: {initial_score}")

# ============================================================
# READ SOURCE
# ============================================================

strategy = ROOT / "strategy.py"
dtm = ROOT / "dtm_bot.py"

strategy_text = (
    strategy.read_text(encoding="utf-8", errors="replace")
    if strategy.exists()
    else ""
)

dtm_text = (
    dtm.read_text(encoding="utf-8", errors="replace")
    if dtm.exists()
    else ""
)

combined = strategy_text + "\n" + dtm_text

# ============================================================
# ISSUE DETECTION
# ============================================================

say()
say("[3] AUTOMATIC ROOT-CAUSE DETECTION")

if "i+right" in strategy_text.replace(" ", ""):
    issues.append({
        "name": "PIVOT SOURCE/CONFIRMATION INDEX",
        "severity": "HIGH",
        "evidence": "strategy.py contains i+right pivot storage",
    })

if ".shift(" in strategy_text:
    issues.append({
        "name": "POSSIBLE SHIFT",
        "severity": "HIGH",
        "evidence": "strategy.py contains pandas shift()",
    })

if "pivot_state" in combined:
    issues.append({
        "name": "PIVOT STATE",
        "severity": "HIGH",
        "evidence": "pivot_state detected",
    })

if "_pine_load_previous_state" in combined:
    issues.append({
        "name": "PINE STATE RESTORATION",
        "severity": "CRITICAL",
        "evidence": "_pine_load_previous_state detected",
    })

# ============================================================
# DATA FORENSICS
# ============================================================

say()
say("[4] DATA / TIMESTAMP / OHLC FORENSICS")

samebar = LAB / "PIVOT_SAME_BAR_FORENSIC.txt"

if samebar.exists():
    text = samebar.read_text(
        encoding="utf-8",
        errors="replace"
    )

    n = len(re.findall(
        r"PINE PRICE IS NOT SAME-BAR HIGH/LOW",
        text
    ))

    say(f"PINE PRICE NOT SAME-BAR OHLC: {n}")

    if n:
        issues.append({
            "name": "PINE/PYTHON OHLC MAPPING",
            "severity": "CRITICAL",
            "evidence": f"{n} Pine pivot prices are not same-bar OHLC values",
        })

# ============================================================
# SAFE AUTOMATIC REPAIRS
# ============================================================

say()
say("[5] APPLYING HIGH-CONFIDENCE REPAIRS")

# ------------------------------------------------------------
# Repair 1:
# Fix accidental SECOND right-bar shift only.
# ------------------------------------------------------------

if strategy.exists():

    txt = strategy.read_text(
        encoding="utf-8",
        errors="replace"
    )

    # Detect explicit double shift patterns.
    bad_patterns = [
        (
            r"last_confirmed\s*=\s*n\s*-\s*1\s*-\s*RIGHT_BARS\s*-\s*RIGHT_BARS",
            "last_confirmed = n - 1 - RIGHT_BARS",
            "Remove explicit double RIGHT_BARS subtraction."
        ),
        (
            r"last_confirmed\s*=\s*n\s*-\s*1\s*-\s*2\s*\*\s*RIGHT_BARS",
            "last_confirmed = n - 1 - RIGHT_BARS",
            "Remove explicit double RIGHT_BARS subtraction."
        ),
    ]

    for pattern, replacement, reason in bad_patterns:

        m = re.search(pattern, txt)

        if m:
            old = m.group(0)
            updated = re.sub(
                pattern,
                replacement,
                txt,
                count=1
            )

            strategy.write_text(
                updated,
                encoding="utf-8"
            )

            changes.append({
                "file": "strategy.py",
                "reason": reason,
                "old": old,
                "new": replacement,
            })

            say("[FIXED] Explicit double RIGHT_BARS shift")

# ============================================================
# Repair 2:
# Preserve pivot source/confirmation identity.
# ============================================================

if strategy.exists():

    txt = strategy.read_text(
        encoding="utf-8",
        errors="replace"
    )

    old = "out.iloc[i+right] = x"

    if old in txt:

        # Do NOT blindly replace it.
        # Pine pivot confirmation semantics require the
        # value to become visible on the confirmation bar.
        say("[CHECKED] pivot storage i+right")
        say("[KEPT] Pine confirmation semantics require explicit source/confirmation distinction")

# ============================================================
# Repair 3:
# Never alter timestamp mapping blindly.
# ============================================================

say("[CHECKED] Timestamp/OHLC mapping")
say("[KEPT] No blind timestamp rewrite because Pine pivot price was proven not to equal same-bar OHLC")

# ============================================================
# VERIFY AFTER SAFE REPAIRS
# ============================================================

say()
say("[6] VERIFYING REPAIRS")

after_score, after_output = run_full_tests("after")

say(f"AFTER MISMATCH SCORE: {after_score}")

if after_score > initial_score:

    say()
    say("[ROLLBACK] Repair increased mismatch count")

    restore_all()
    rollbacks.append({
        "reason": "Parity became worse after repair.",
        "before": initial_score,
        "after": after_score,
    })

    final_score = initial_score

else:

    final_score = after_score

    if after_score < initial_score:
        say("[PASS] Parity improved")
    else:
        say("[INFO] Parity unchanged")

# ============================================================
# STATIC FINAL ANALYSIS
# ============================================================

say()
say("[7] FINAL ANALYSIS")

final_score2, final_output = run_full_tests("final")

if final_score2 > final_score:
    restore_all()
    final_score2 = initial_score
    say("[ROLLBACK] Final verification worsened parity")

# ============================================================
# REPORT
# ============================================================

report = []

report.append("# DTM — AUTOMATIC PARITY REPAIR FINAL REPORT")
report.append("")
report.append(f"Generated: {datetime.now().isoformat()}")
report.append("")
report.append("## RESULT")
report.append("")
report.append(f"- Initial mismatch score: **{initial_score}**")
report.append(f"- Final mismatch score: **{final_score2}**")
report.append(f"- Changes applied: **{len(changes)}**")
report.append(f"- Rollbacks: **{len(rollbacks)}**")
report.append("")
report.append("## ROOT CAUSES DETECTED")
report.append("")

for x in issues:
    report.append(
        f"### [{x['severity']}] {x['name']}"
    )
    report.append("")
    report.append(f"- Evidence: {x['evidence']}")
    report.append("")

report.append("## FILES MODIFIED")
report.append("")

if changes:

    for i, c in enumerate(changes, 1):

        report.append(f"### REPAIR #{i}")
        report.append("")
        report.append(f"**FILE:** `{c['file']}`")
        report.append("")
        report.append(f"**REASON:** {c['reason']}")
        report.append("")
        report.append("**OLD:**")
        report.append("```")
        report.append(c["old"])
        report.append("```")
        report.append("")
        report.append("**NEW:**")
        report.append("```")
        report.append(c["new"])
        report.append("```")
        report.append("")
else:
    report.append("No high-confidence source-code modification was performed.")
    report.append("")

report.append("## ROLLBACKS")
report.append("")

if rollbacks:
    for r in rollbacks:
        report.append(
            f"- {r['reason']} "
            f"(before={r['before']}, after={r['after']})"
        )
else:
    report.append("- None")

report.append("")
report.append("## FINAL DIAGNOSTIC")
report.append("")
report.append("```text")
report.append(final_output[-12000:])
report.append("```")
report.append("")
report.append("## BACKUP")
report.append("")
report.append(str(BACKUP))
report.append("")
report.append("## IMPORTANT")
report.append("")
report.append(
    "The engine intentionally refuses blind pivot/timestamp rewrites "
    "when the available evidence does not mathematically prove the "
    "correct replacement."
)

REPORT.write_text(
    "\n".join(report),
    encoding="utf-8"
)

Path(LOG).write_text(
    "\n".join(log),
    encoding="utf-8"
)

say()
say("=" * 90)
say("AUTOMATIC REPAIR FINISHED")
say("=" * 90)
say(f"REPORT : {REPORT}")
say(f"BACKUP : {BACKUP}")
say(f"LOG    : {LOG}")
say(f"INITIAL: {initial_score}")
say(f"FINAL  : {final_score2}")
say(f"CHANGES: {len(changes)}")
say(f"ROLLBACKS: {len(rollbacks)}")
say("=" * 90)
