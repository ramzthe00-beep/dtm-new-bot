# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
import ast
import re
import shutil
import hashlib
import subprocess
import json
import sys
import os

ROOT = Path.cwd()
LAB = ROOT / "parity_lab"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

BACKUP = LAB / f"ULTIMATE_BACKUP_{STAMP}"
REPORT = LAB / f"ULTIMATE_REPAIR_REPORT_{STAMP}.md"
LOG = LAB / f"ULTIMATE_REPAIR_LOG_{STAMP}.txt"

# ============================================================
# PROJECT SOURCE DISCOVERY
# ============================================================

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "parity_lab",
    "node_modules",
}

SOURCE_FILES = []

for p in ROOT.rglob("*.py"):
    if any(x in EXCLUDE_DIRS for x in p.parts):
        continue

    if p.name.startswith("AUTO_"):
        continue

    if p.name.startswith("ULTIMATE_"):
        continue

    if "REPAIR" in p.name.upper():
        continue

    SOURCE_FILES.append(p)

SOURCE_FILES = sorted(set(SOURCE_FILES))

# ============================================================
# LOGGING
# ============================================================

log = []
changes = []
issues = []
tests = []
rollback_events = []


def say(x=""):
    print(x)
    log.append(str(x))


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


# ============================================================
# BACKUP
# ============================================================

def backup_project():

    BACKUP.mkdir(parents=True, exist_ok=True)

    for p in SOURCE_FILES:

        dst = BACKUP / p.relative_to(ROOT)

        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(p, dst)

    say(f"[BACKUP CREATED] {BACKUP}")


def restore_project():

    for p in SOURCE_FILES:

        src = BACKUP / p.relative_to(ROOT)

        if src.exists():

            shutil.copy2(src, p)

    say("[ROLLBACK] COMPLETE")


# ============================================================
# AST INVENTORY
# ============================================================

def build_inventory():

    result = []

    for p in SOURCE_FILES:

        try:

            text = p.read_text(
                encoding="utf-8",
                errors="replace"
            )

            tree = ast.parse(text)

        except Exception as e:

            issues.append({
                "type": "AST",
                "file": str(p.relative_to(ROOT)),
                "error": str(e)
            })

            continue

        functions = []
        classes = []
        constants = []

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                functions.append(node.name)

            elif isinstance(node, ast.ClassDef):

                classes.append(node.name)

            elif isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(target, ast.Name):

                        if target.id.isupper():

                            constants.append(target.id)

        result.append({
            "file": str(p.relative_to(ROOT)),
            "functions": sorted(set(functions)),
            "classes": sorted(set(classes)),
            "constants": sorted(set(constants))
        })

    return result


# ============================================================
# SOURCE PATTERN ANALYSIS
# ============================================================

def analyze_source():

    findings = []

    for p in SOURCE_FILES:

        try:
            text = p.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except:
            continue

        name = str(p.relative_to(ROOT))

        patterns = {

            "PIVOT_RIGHT_SHIFT":
                r"(i\s*\+\s*right|RIGHT_BARS)",

            "PANDAS_SHIFT":
                r"\.shift\s*\(",

            "PIVOT_STATE":
                r"pivot_state",

            "PINE_STATE":
                r"_pine_load_previous_state",

            "RMA":
                r"\brma\b|calc_rma",

            "EMA":
                r"\bema\b|calc_ema",

            "RSI":
                r"\brsi\b|calc_rsi",

            "MACD":
                r"\bmacd\b|calc_macd",

            "ATR":
                r"\batr\b|calc_atr",

            "DIVERGENCE":
                r"diverg",

            "FIB":
                r"fib|FIB",

            "CANDLE":
                r"candle|shadow|body",

            "TIMESTAMP":
                r"timestamp|datetime|timezone",

            "OHLC":
                r"\bopen\b|\bhigh\b|\blow\b|\bclose\b",

        }

        for category, pattern in patterns.items():

            matches = list(
                re.finditer(
                    pattern,
                    text,
                    re.I
                )
            )

            if matches:

                findings.append({
                    "file": name,
                    "category": category,
                    "count": len(matches)
                })

    return findings


# ============================================================
# EXTERNAL PARITY TESTS
# ============================================================

TEST_NAMES = [
    "deep_analyzer.py",
    "pine_timestamp_ohlc_check.py",
    "pine_pivot_price_locator.py",
    "fast_spot_check.py",
]


def run_test(path):

    if not path.exists():

        return {
            "name": path.name,
            "returncode": -1,
            "output": "MISSING"
        }

    try:

        p = subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=300
        )

        return {
            "name": path.name,
            "returncode": p.returncode,
            "output": p.stdout
        }

    except subprocess.TimeoutExpired:

        return {
            "name": path.name,
            "returncode": 124,
            "output": "TIMEOUT"
        }

    except Exception as e:

        return {
            "name": path.name,
            "returncode": 99,
            "output": str(e)
        }


def run_parity():

    results = []

    for name in TEST_NAMES:

        result = run_test(
            LAB / name
        )

        results.append(result)

    return results


def score(results):

    total = 0

    for r in results:

        text = r["output"]

        patterns = [
            r"MISMATCH",
            r"NOT SAME",
            r"NOT same",
            r"FALSE",
            r"False",
            r"PRICE IS NOT SAME",
            r"ERROR",
            r"CRITICAL",
        ]

        for pattern in patterns:

            total += len(
                re.findall(
                    pattern,
                    text,
                    re.I
                )
            )

    return total


# ============================================================
# SAFE REPAIR RULES
# ============================================================

def safe_repairs():

    """
    فقط اصلاحاتی مجاز هستند که:
    1. الگوی دقیق دارند.
    2. semantics آنها قطعی است.
    3. قبل/بعد تست می‌شود.
    """

    applied = []

    for p in SOURCE_FILES:

        try:

            text = p.read_text(
                encoding="utf-8",
                errors="replace"
            )

        except:
            continue

        original = text

        # ----------------------------------------------------
        # DOUBLE RIGHT-BAR SHIFT
        # ----------------------------------------------------

        patterns = [

            (
                r"n\s*-\s*1\s*-\s*RIGHT_BARS\s*-\s*RIGHT_BARS",
                "n - 1 - RIGHT_BARS",
                "Remove explicit double RIGHT_BARS subtraction"
            ),

            (
                r"n\s*-\s*1\s*-\s*2\s*\*\s*RIGHT_BARS",
                "n - 1 - RIGHT_BARS",
                "Remove explicit 2*RIGHT_BARS subtraction"
            ),

        ]

        for pattern, replacement, reason in patterns:

            new_text, count = re.subn(
                pattern,
                replacement,
                text,
                count=1
            )

            if count:

                text = new_text

                applied.append({
                    "file": str(p.relative_to(ROOT)),
                    "reason": reason,
                    "old": pattern,
                    "new": replacement
                })

        # ----------------------------------------------------
        # WRITE ONLY IF CHANGED
        # ----------------------------------------------------

        if text != original:

            p.write_text(
                text,
                encoding="utf-8"
            )

    return applied


# ============================================================
# REPORT
# ============================================================

def write_report(
    inventory,
    findings,
    before_results,
    after_results
):

    report = []

    report.append(
        "# DTM ULTIMATE PINE ↔ PYTHON PARITY REPAIR REPORT"
    )

    report.append("")

    report.append(
        f"Generated: {datetime.now().isoformat()}"
    )

    report.append("")

    report.append("## RESULT")

    report.append("")

    before_score = score(before_results)
    after_score = score(after_results)

    report.append(
        f"- Source Python files analyzed: **{len(SOURCE_FILES)}**"
    )

    report.append(
        f"- Initial parity score: **{before_score}**"
    )

    report.append(
        f"- Final parity score: **{after_score}**"
    )

    report.append(
        f"- Changes applied: **{len(changes)}**"
    )

    report.append(
        f"- Rollbacks: **{len(rollback_events)}**"
    )

    report.append("")

    report.append("## ROOT-CAUSE CATEGORIES")

    report.append("")

    counts = {}

    for x in findings:

        c = x["category"]

        counts[c] = counts.get(c, 0) + x["count"]

    for k, v in sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        report.append(
            f"- **{k}**: {v}"
        )

    report.append("")

    report.append("## FUNCTIONS / CLASSES / PARAMETERS")

    report.append("")

    for item in inventory:

        report.append(
            f"### `{item['file']}`"
        )

        if item["classes"]:

            report.append(
                "**Classes:** " +
                ", ".join(item["classes"])
            )

        if item["functions"]:

            report.append(
                "**Functions:** " +
                ", ".join(item["functions"])
            )

        if item["constants"]:

            report.append(
                "**Parameters:** " +
                ", ".join(item["constants"])
            )

        report.append("")

    report.append("## APPLIED REPAIRS")

    report.append("")

    if changes:

        for i, c in enumerate(changes, 1):

            report.append(
                f"### REPAIR {i}"
            )

            report.append(
                f"- File: `{c['file']}`"
            )

            report.append(
                f"- Reason: {c['reason']}"
            )

            report.append(
                f"- Old: `{c['old']}`"
            )

            report.append(
                f"- New: `{c['new']}`"
            )

    else:

        report.append(
            "No high-confidence automatic repair was applied."
        )

    report.append("")

    report.append("## IMPORTANT")

    report.append("")

    report.append(
        "Automatic repair intentionally refuses to modify "
        "pivot/timestamp/state semantics unless the replacement "
        "is deterministic and verified."
    )

    report.append("")

    report.append(
        f"Backup: `{BACKUP}`"
    )

    REPORT.write_text(
        "\n".join(report),
        encoding="utf-8"
    )


# ============================================================
# MAIN
# ============================================================

say("=" * 90)
say("DTM ULTIMATE PINE ↔ PYTHON PARITY ENGINE")
say("=" * 90)

say("")
say("[1] PROJECT SOURCE DISCOVERY")

say(
    f"SOURCE FILES: {len(SOURCE_FILES)}"
)

say("")
say("[2] FULL BACKUP")

backup_project()

say("")
say("[3] BUILDING REAL AST INVENTORY")

inventory = build_inventory()

total_functions = sum(
    len(x["functions"])
    for x in inventory
)

total_classes = sum(
    len(x["classes"])
    for x in inventory
)

total_constants = sum(
    len(x["constants"])
    for x in inventory
)

say(
    f"FUNCTIONS: {total_functions}"
)

say(
    f"CLASSES: {total_classes}"
)

say(
    f"PARAMETERS: {total_constants}"
)

say("")
say("[4] ROOT-CAUSE SOURCE ANALYSIS")

findings = analyze_source()

issues.extend(findings)

say(
    f"FINDINGS: {len(findings)}"
)

say("")
say("[5] INITIAL PARITY")

before_results = run_parity()

before_score = score(
    before_results
)

say(
    f"INITIAL SCORE: {before_score}"
)

say("")
say("[6] APPLYING ONLY DETERMINISTIC REPAIRS")

changes.extend(
    safe_repairs()
)

say(
    f"REPAIRS APPLIED: {len(changes)}"
)

say("")
say("[7] POST-REPAIR PARITY")

after_results = run_parity()

after_score = score(
    after_results
)

say(
    f"FINAL SCORE: {after_score}"
)

if after_score > before_score:

    say(
        "[ROLLBACK] Parity became worse."
    )

    restore_project()

    rollback_events.append({
        "before": before_score,
        "after": after_score
    })

    changes.clear()

    after_results = run_parity()

    after_score = score(
        after_results
    )

else:

    if after_score < before_score:

        say(
            "[PASS] Parity improved."
        )

    else:

        say(
            "[INFO] Parity unchanged."
        )

say("")
say("[8] WRITING COMPLETE REPORT")

write_report(
    inventory,
    findings,
    before_results,
    after_results
)

Path(LOG).write_text(
    "\n".join(log),
    encoding="utf-8"
)

say("")
say("=" * 90)
say("ULTIMATE PARITY ANALYSIS / REPAIR FINISHED")
say("=" * 90)
say(f"REPORT : {REPORT}")
say(f"BACKUP : {BACKUP}")
say(f"INITIAL: {before_score}")
say(f"FINAL  : {after_score}")
say(f"CHANGES: {len(changes)}")
say(f"ROLLBACKS: {len(rollback_events)}")
say("=" * 90)
