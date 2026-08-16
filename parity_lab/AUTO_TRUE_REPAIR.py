# -*- coding: utf-8 -*-

from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import hashlib
import re
import json
import ast
import sys
import os

ROOT = Path.cwd()
LAB = ROOT / "parity_lab"

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

BACKUP = LAB / f"TRUE_REPAIR_BACKUP_{STAMP}"
REPORT = LAB / f"TRUE_REPAIR_REPORT_{STAMP}.md"
LOG = LAB / f"TRUE_REPAIR_LOG_{STAMP}.txt"

# ------------------------------------------------------------
# SAFETY
# ------------------------------------------------------------

EXCLUDE = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}

# Source files that can contain the actual implementation.
SOURCE_EXTENSIONS = {".py", ".pine"}

# Never modify data, logs, reports, CSVs or the repair engines themselves.
PROTECTED_NAMES = {
    "AUTO_TRUE_REPAIR.py",
    "AUTO_REPAIR_ALL.py",
    "ULTIMATE_PARITY_REPAIR.py",
}

log = []
changes = []
rollbacks = []
tests = []


def say(x=""):
    print(x)
    log.append(str(x))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_files():
    result = []

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue

        if any(x in EXCLUDE for x in p.parts):
            continue

        if p.name in PROTECTED_NAMES:
            continue

        if p.suffix.lower() in SOURCE_EXTENSIONS:
            result.append(p)

    return sorted(result)


def snapshot():
    return {
        str(p): sha256(p)
        for p in source_files()
    }


def backup_all():
    BACKUP.mkdir(parents=True, exist_ok=True)

    for p in source_files():
        dst = BACKUP / p.relative_to(ROOT)
        dst.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(p, dst)
        except Exception as e:
            say(f"[BACKUP WARNING] {p}: {e}")

    say(f"[BACKUP] {BACKUP}")


def restore_file(path):
    src = BACKUP / path.relative_to(ROOT)

    if src.exists():
        shutil.copy2(src, path)
        return True

    return False


def run(cmd, timeout=300):
    say(f"$ {cmd}")

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
        return 99, str(e)


# ------------------------------------------------------------
# PARITY TEST DISCOVERY
# ------------------------------------------------------------

def parity_tools():
    candidates = [
        LAB / "deep_analyzer.py",
        LAB / "pine_timestamp_ohlc_check.py",
        LAB / "pine_pivot_price_locator.py",
        LAB / "fast_spot_check.py",
    ]

    return [x for x in candidates if x.exists()]


def parity_test(label):
    outputs = []

    for tool in parity_tools():

        rc, out = run(
            f"python3 '{tool}'",
            timeout=300
        )

        outputs.append(out)

        (LAB / f"_true_repair_{label}_{tool.stem}.txt").write_text(
            out,
            encoding="utf-8"
        )

    combined = "\n".join(outputs)

    # Strong indicators of mismatch.
    score = 0

    patterns = [
        r"MISMATCH",
        r"mismatch",
        r"NOT SAME",
        r"NOT same",
        r"PRICE IS NOT SAME",
        r"FALSE",
        r"False",
    ]

    for pattern in patterns:
        score += len(re.findall(pattern, combined))

    tests.append({
        "label": label,
        "score": score,
    })

    return score, combined


# ------------------------------------------------------------
# AST INVENTORY
# ------------------------------------------------------------

def build_inventory():

    inventory = []

    for path in source_files():

        if path.suffix != ".py":
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace"
            )

            tree = ast.parse(text)

        except Exception:
            continue

        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                args = []

                for arg in node.args.args:
                    args.append(arg.arg)

                inventory.append({
                    "file": str(path.relative_to(ROOT)),
                    "function": node.name,
                    "line": node.lineno,
                    "parameters": args,
                })

    return inventory


# ------------------------------------------------------------
# STATIC ROOT-CAUSE ANALYSIS
# ------------------------------------------------------------

def analyze_source():

    findings = []

    for path in source_files():

        if path.suffix != ".py":
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except Exception:
            continue

        relative = str(path.relative_to(ROOT))

        checks = [

            (
                "PIVOT_INDEX",
                r"i\s*\+\s*right",
                "Pivot source/confirmation index must remain explicit."
            ),

            (
                "DOUBLE_SHIFT",
                r"RIGHT_BARS.*RIGHT_BARS",
                "Possible second pivot displacement."
            ),

            (
                "PANDAS_SHIFT",
                r"\.shift\s*\(",
                "Potential Pine/Python indexing mismatch."
            ),

            (
                "PIVOT_STATE",
                r"pivot_state",
                "Persistent pivot state requires Pine-equivalent update order."
            ),

            (
                "PINE_STATE",
                r"_pine_load_previous_state",
                "State restoration can affect historical pivot identity."
            ),

            (
                "RMA",
                r"\bRMA\b|calc_rma|ta\.rma",
                "Wilder/RMA seed and update semantics must match Pine."
            ),

            (
                "EMA",
                r"\bEMA\b|calc_ema|ta\.ema",
                "EMA initialization and recurrence must match Pine."
            ),

            (
                "RSI",
                r"\bRSI\b|calc_rsi|ta\.rsi",
                "RSI source and smoothing semantics must match Pine."
            ),

            (
                "MACD",
                r"\bMACD\b|calc_macd|ta\.macd",
                "MACD components and EMA seeds must match Pine."
            ),

            (
                "ATR",
                r"\bATR\b|calc_atr|ta\.atr",
                "ATR/RMA semantics must match Pine."
            ),

            (
                "DIVERGENCE",
                r"diverg",
                "Divergence must consume identical pivot identities."
            ),

            (
                "FIBONACCI",
                r"fib|FIB",
                "Fibonacci source swing and tolerance must match Pine."
            ),

            (
                "CANDLE",
                r"candle|pin.?bar|marubozu|shadow",
                "Candle calculations must use identical OHLC and indexing."
            ),

            (
                "SIGNAL",
                r"signal|finalScore|score",
                "Final signal must consume identical upstream values."
            ),
        ]

        for name, pattern, reason in checks:

            if re.search(pattern, text, re.I):

                findings.append({
                    "file": relative,
                    "category": name,
                    "reason": reason,
                })

    return findings


# ------------------------------------------------------------
# DETERMINISTIC REPAIR ENGINE
# ------------------------------------------------------------

def deterministic_repairs():

    applied = 0

    for path in source_files():

        if path.suffix != ".py":
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except Exception:
            continue

        original = text

        # ----------------------------------------------------
        # Explicit mathematical double-shift corrections
        # ----------------------------------------------------

        replacements = [

            (
                r"n\s*-\s*1\s*-\s*RIGHT_BARS\s*-\s*RIGHT_BARS",
                "n - 1 - RIGHT_BARS",
                "Remove explicit second RIGHT_BARS displacement."
            ),

            (
                r"n\s*-\s*1\s*-\s*2\s*\*\s*RIGHT_BARS",
                "n - 1 - RIGHT_BARS",
                "Remove explicit double RIGHT_BARS displacement."
            ),
        ]

        for pattern, replacement, reason in replacements:

            new_text, count = re.subn(
                pattern,
                replacement,
                text,
                count=1
            )

            if count:

                text = new_text

                changes.append({
                    "file": str(path.relative_to(ROOT)),
                    "reason": reason,
                    "old": original,
                    "new": text,
                })

                applied += 1

        if text != original:

            path.write_text(
                text,
                encoding="utf-8"
            )

    return applied


# ------------------------------------------------------------
# REPAIR WITH VALIDATION
# ------------------------------------------------------------

def attempt_repair():

    global changes

    before_snapshot = snapshot()

    before_score, _ = parity_test("before_repair")

    say(f"[BASELINE SCORE] {before_score}")

    applied = deterministic_repairs()

    if applied == 0:

        say("[INFO] No deterministic mathematical repair was safe.")

        return before_score

    after_score, _ = parity_test("after_repair")

    say(f"[AFTER SCORE] {after_score}")

    if after_score > before_score:

        say("[ROLLBACK] Repair made parity worse.")

        for p in source_files():

            old_hash = before_snapshot.get(str(p))

            if old_hash and sha256(p) != old_hash:
                restore_file(p)

        rollbacks.append({
            "reason": "Parity became worse.",
            "before": before_score,
            "after": after_score,
        })

        return before_score

    say("[PASS] Repair did not worsen parity.")

    return after_score


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

say("=" * 90)
say("DTM TRUE AUTOMATIC PARITY REPAIR ENGINE")
say("=" * 90)
say("ANALYZE -> IDENTIFY -> REPAIR -> TEST -> KEEP/ROLLBACK")
say()

say("[1] SOURCE INVENTORY")

files = source_files()

say(f"SOURCE FILES: {len(files)}")

say()
say("[2] FULL BACKUP")

backup_all()

say()
say("[3] AST INVENTORY")

inventory = build_inventory()

say(f"FUNCTIONS: {len(inventory)}")

say()
say("[4] ROOT-CAUSE ANALYSIS")

findings = analyze_source()

say(f"FINDINGS: {len(findings)}")

say()
say("[5] INITIAL PARITY")

initial_score, _ = parity_test("initial")

say(f"INITIAL SCORE: {initial_score}")

say()
say("[6] AUTOMATIC DETERMINISTIC REPAIR")

final_score = attempt_repair()

say()
say("[7] FINAL PARITY")

final_score, final_output = parity_test("final")

say(f"FINAL SCORE: {final_score}")

# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

report = []

report.append("# DTM TRUE AUTOMATIC PARITY REPAIR REPORT")
report.append("")
report.append(f"Generated: {datetime.now().isoformat()}")
report.append("")

report.append("## RESULT")
report.append("")
report.append(f"- Source files scanned: **{len(files)}**")
report.append(f"- Functions discovered: **{len(inventory)}**")
report.append(f"- Root-cause findings: **{len(findings)}**")
report.append(f"- Initial parity score: **{initial_score}**")
report.append(f"- Final parity score: **{final_score}**")
report.append(f"- Repairs applied: **{len(changes)}**")
report.append(f"- Rollbacks: **{len(rollbacks)}**")
report.append("")

report.append("## ROOT-CAUSE FINDINGS")
report.append("")

for f in findings:

    report.append(
        f"- **{f['category']}** — `{f['file']}` — {f['reason']}"
    )

report.append("")
report.append("## ACTUAL REPAIRS")
report.append("")

if changes:

    for i, c in enumerate(changes, 1):

        report.append(f"### Repair #{i}")
        report.append("")
        report.append(f"**FILE:** `{c['file']}`")
        report.append("")
        report.append(f"**REASON:** {c['reason']}")
        report.append("")

else:

    report.append(
        "No deterministic repair was mathematically safe enough to apply automatically."
    )

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
report.append("## FINAL PARITY OUTPUT")
report.append("")
report.append("```text")
report.append(final_output[-20000:])
report.append("```")
report.append("")
report.append("## BACKUP")
report.append("")
report.append(str(BACKUP))

REPORT.write_text(
    "\n".join(report),
    encoding="utf-8"
)

LOG.write_text(
    "\n".join(log),
    encoding="utf-8"
)

say()
say("=" * 90)
say("REPAIR FINISHED")
say("=" * 90)
say(f"REPORT    : {REPORT}")
say(f"BACKUP    : {BACKUP}")
say(f"INITIAL   : {initial_score}")
say(f"FINAL     : {final_score}")
say(f"REPAIRS   : {len(changes)}")
say(f"ROLLBACKS : {len(rollbacks)}")
say("=" * 90)
