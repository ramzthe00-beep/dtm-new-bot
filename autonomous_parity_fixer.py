#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autonomous Pine/Python parity fixer
-----------------------------------
هدف:
1) بررسی خودکار پروژه
2) پیدا کردن خطاهای قطعی و قابل تشخیص
3) اعمال patchهای محافظه‌کارانه
4) تست بعد از هر patch
5) نگه داشتن patch فقط در صورت بهبود
6) rollback خودکار در صورت بدتر شدن
7) پردازش حداکثر 100 اصلاح در هر batch

این ابزار عمداً اصلاحات حدسی و پرریسک معاملاتی را انجام نمی‌دهد.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Optional


ROOT = Path(__file__).resolve().parent

MAX_PATCHES_PER_BATCH = 100
MAX_BATCHES = 100

PYTHON_EXTENSIONS = {".py"}

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

LOG_DIR = ROOT / "autofix_logs"
BACKUP_DIR = ROOT / "autofix_backups"
STATE_FILE = ROOT / ".autofix_state.json"

LOG_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)


@dataclass
class PatchCandidate:
    rule_id: str
    file: str
    description: str
    before_hash: str
    after_hash: str = ""
    status: str = "candidate"
    score_before: int = 0
    score_after: int = 0
    details: str = ""


def log(msg: str) -> None:
    print(msg, flush=True)


def run(
    cmd: list[str],
    timeout: int = 120,
    cwd: Path = ROOT,
) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s: {' '.join(cmd)}"
    except Exception as e:
        return 125, f"EXECUTION ERROR: {e}"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_available() -> bool:
    rc, _ = run(["git", "--version"], timeout=10)
    return rc == 0


def git_clean_snapshot() -> str:
    if not git_available():
        return ""

    rc, out = run(["git", "status", "--porcelain"], timeout=20)
    if rc != 0:
        return ""

    return out.strip()


def git_checkpoint(label: str) -> bool:
    if not git_available():
        return True

    # فقط stash موقت، نه commit دائمی.
    tag = f"autofix-{label}-{int(time.time())}"

    rc, _ = run(["git", "add", "-A"], timeout=30)
    if rc != 0:
        return False

    rc, _ = run(
        ["git", "stash", "push", "-u", "-m", tag],
        timeout=60,
    )

    # اگر چیزی برای stash نباشد باز هم ادامه می‌دهیم.
    return rc == 0


def git_restore_last_stash() -> bool:
    if not git_available():
        return False

    rc, _ = run(["git", "stash", "pop"], timeout=60)
    return rc == 0


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {
            "batch": 0,
            "accepted": 0,
            "rejected": 0,
            "last_files": [],
        }

    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "batch": 0,
            "accepted": 0,
            "rejected": 0,
            "last_files": [],
        }


def save_state(state: dict) -> None:
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def python_files() -> list[Path]:
    """
    Return only real project Python files.

    IMPORTANT:
    Never scan or modify virtual environments, installed packages,
    caches, generated backups, or tool artifacts.
    """
    result = []

    forbidden_dirs = set(EXCLUDED_DIRS) | {
        "parity_env",
        "venv",
        ".venv",
        "env",
        ".env",
        "site-packages",
        "__pycache__",
        ".git",
        "autofix_backups",
        "autofix_logs",
    }

    for path in ROOT.rglob("*.py"):
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            continue

        # Never enter or repair virtual environments / dependencies.
        if any(part in forbidden_dirs for part in rel.parts):
            continue

        # Never repair Python cache/compiled files.
        if path.name.endswith((".pyc", ".pyo")):
            continue

        result.append(path)

    return sorted(result)


# ----------------------------------------------------------------------
# Scoring
# ----------------------------------------------------------------------

def score_compile() -> tuple[int, list[str]]:
    errors = []
    score = 0

    for path in python_files():
        rc, out = run(
            [sys.executable, "-m", "py_compile", str(path)],
            timeout=30,
        )

        if rc != 0:
            score -= 100
            errors.append(f"[COMPILE] {path}: {out[-3000:]}")
        else:
            score += 5

    return score, errors


def discover_tests() -> list[list[str]]:
    candidates = [
        ["pytest", "-q"],
        [sys.executable, "-m", "pytest", "-q"],
    ]

    for c in candidates:
        rc, _ = run(c, timeout=20)
        if rc != 127:
            return [c]

    return []


def score_project() -> tuple[int, list[str]]:
    score, errors = score_compile()

    # تست‌های موجود پروژه
    tests = discover_tests()

    for cmd in tests:
        rc, out = run(cmd, timeout=180)

        if rc == 0:
            score += 100
        else:
            score -= 50
            errors.append(f"[TEST] {' '.join(cmd)}\n{out[-5000:]}")

    # ruff در صورت نصب بودن
    rc, _ = run(["ruff", "--version"], timeout=10)

    if rc == 0:
        rc, out = run(["ruff", "check", "."], timeout=60)

        if rc == 0:
            score += 30
        else:
            score -= 20
            errors.append(f"[RUFF]\n{out[-4000:]}")

    return score, errors


# ----------------------------------------------------------------------
# Safe deterministic repair rules
# ----------------------------------------------------------------------

def repair_duplicate_imports(path: Path, text: str):
    lines = text.splitlines(True)

    seen = set()
    new_lines = []
    changed = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("import ") or stripped.startswith("from "):
            if stripped in seen:
                changed = True
                continue
            seen.add(stripped)

        new_lines.append(line)

    if not changed:
        return None

    return "".join(new_lines), "remove duplicate imports"


def repair_trailing_whitespace(path: Path, text: str):
    lines = text.splitlines(True)
    new_lines = []
    changed = False

    for line in lines:
        nl = "\n" if line.endswith("\n") else ""
        body = line[:-1] if nl else line

        fixed = body.rstrip() + nl

        if fixed != line:
            changed = True

        new_lines.append(fixed)

    if not changed:
        return None

    return "".join(new_lines), "remove trailing whitespace"


def repair_multiple_blank_lines(path: Path, text: str):
    fixed = re.sub(r"\n{4,}", "\n\n\n", text)

    if fixed == text:
        return None

    return fixed, "normalize excessive blank lines"


def repair_obvious_bool_comparisons(path: Path, text: str):
    patterns = [
        (r"([A-Za-z_][A-Za-z0-9_]*)\s*==\s*True\b", r"\1"),
        (r"([A-Za-z_][A-Za-z0-9_]*)\s*==\s*False\b", r"not \1"),
    ]

    fixed = text

    for pat, repl in patterns:
        fixed = re.sub(pat, repl, fixed)

    if fixed == text:
        return None

    return fixed, "simplify explicit boolean comparisons"


def repair_obvious_none_comparisons(path: Path, text: str):
    fixed = re.sub(
        r"([A-Za-z_][A-Za-z0-9_\.\[\]]*)\s*==\s*None\b",
        r"\1 is None",
        text,
    )

    fixed = re.sub(
        r"([A-Za-z_][A-Za-z0-9_\.\[\]]*)\s*!=\s*None\b",
        r"\1 is not None",
        fixed,
    )

    if fixed == text:
        return None

    return fixed, "normalize None comparisons"


SAFE_RULES: list[tuple[str, Callable]] = [
    ("R001_DUP_IMPORTS", repair_duplicate_imports),
    ("R002_TRAILING_WS", repair_trailing_whitespace),
    ("R003_BLANK_LINES", repair_multiple_blank_lines),
    ("R004_BOOL_COMPARE", repair_obvious_bool_comparisons),
    ("R005_NONE_COMPARE", repair_obvious_none_comparisons),
]


# ----------------------------------------------------------------------
# Backup / restore
# ----------------------------------------------------------------------

def backup_file(path: Path) -> Path:
    rel = path.relative_to(ROOT)
    target = BACKUP_DIR / rel
    target.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(path, target)
    return target


def restore_file(path: Path, backup: Path) -> None:
    shutil.copy2(backup, path)


# ----------------------------------------------------------------------
# Syntax safety
# ----------------------------------------------------------------------

def syntax_ok(path: Path) -> bool:
    try:
        ast.parse(path.read_text(encoding="utf-8"))
        return True
    except Exception:
        return False


# ----------------------------------------------------------------------
# Generate candidates
# ----------------------------------------------------------------------

def generate_candidates(limit: int = MAX_PATCHES_PER_BATCH):
    candidates: list[tuple[Path, str, Callable, str]] = []

    for path in python_files():
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        for rule_id, rule in SAFE_RULES:
            try:
                proposal = rule(path, text)
            except Exception:
                continue

            if proposal is None:
                continue

            _, description = proposal

            candidates.append(
                (
                    path,
                    rule_id,
                    rule,
                    description,
                )
            )

            if len(candidates) >= limit:
                return candidates

    return candidates


# ----------------------------------------------------------------------
# Apply one patch
# ----------------------------------------------------------------------

def apply_candidate(
    path: Path,
    rule_id: str,
    rule: Callable,
    description: str,
) -> PatchCandidate:

    before = path.read_text(encoding="utf-8")
    before_hash = hashlib.sha256(before.encode()).hexdigest()

    backup = backup_file(path)

    proposal = rule(path, before)

    if proposal is None:
        return PatchCandidate(
            rule_id=rule_id,
            file=str(path.relative_to(ROOT)),
            description=description,
            before_hash=before_hash,
            status="skipped",
        )

    after, _ = proposal

    if after == before:
        return PatchCandidate(
            rule_id=rule_id,
            file=str(path.relative_to(ROOT)),
            description=description,
            before_hash=before_hash,
            status="skipped",
        )

    path.write_text(after, encoding="utf-8")

    candidate = PatchCandidate(
        rule_id=rule_id,
        file=str(path.relative_to(ROOT)),
        description=description,
        before_hash=before_hash,
        after_hash=hashlib.sha256(after.encode()).hexdigest(),
    )

    # اول syntax
    if not syntax_ok(path):
        restore_file(path, backup)
        candidate.status = "rejected_syntax"
        candidate.details = "AST parse failed"
        return candidate

    # سپس score
    before_score, before_errors = score_project()
    after_score, after_errors = score_project()

    candidate.score_before = before_score
    candidate.score_after = after_score

    if after_score > before_score:
        candidate.status = "accepted"
        candidate.details = (
            f"score {before_score} -> {after_score}"
        )
        return candidate

    restore_file(path, backup)

    candidate.status = "rejected"
    candidate.details = (
        f"score {before_score} -> {after_score}"
    )

    return candidate


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

def main():
    state = load_state()

    log("")
    log("=" * 70)
    log(" AUTONOMOUS PARITY FIXER")
    log("=" * 70)
    log(f"PROJECT : {ROOT}")
    log(f"BATCH   : max {MAX_PATCHES_PER_BATCH} patches")
    log("=" * 70)
    log("")

    # وضعیت اولیه
    initial_score, initial_errors = score_project()

    log(f"[BASELINE SCORE] {initial_score}")

    if initial_errors:
        log("")
        log("FIRST DIAGNOSTICS:")
        for e in initial_errors[:10]:
            log(e)

    total_accepted = 0
    total_rejected = 0

    for batch_no in range(
        state.get("batch", 0) + 1,
        MAX_BATCHES + 1,
    ):
        log("")
        log("=" * 70)
        log(f" BATCH {batch_no}/{MAX_BATCHES}")
        log("=" * 70)

        candidates = generate_candidates(MAX_PATCHES_PER_BATCH)

        if not candidates:
            log("NO MORE SAFE DETERMINISTIC PATCHES FOUND.")
            break

        batch_results = []

        for index, (
            path,
            rule_id,
            rule,
            description,
        ) in enumerate(candidates, start=1):

            log("")
            log(
                f"[{index}/{len(candidates)}] "
                f"{rule_id} :: {path.relative_to(ROOT)}"
            )
            log(f"  {description}")

            try:
                result = apply_candidate(
                    path,
                    rule_id,
                    rule,
                    description,
                )
            except Exception as e:
                result = PatchCandidate(
                    rule_id=rule_id,
                    file=str(path.relative_to(ROOT)),
                    description=description,
                    before_hash="",
                    status="error",
                    details=str(e),
                )

            batch_results.append(asdict(result))

            log(
                f"  STATUS={result.status} "
                f"SCORE={result.score_before}->{result.score_after}"
            )

            if result.status == "accepted":
                total_accepted += 1
            elif result.status.startswith("rejected"):
                total_rejected += 1

        state["batch"] = batch_no
        state["accepted"] = state.get("accepted", 0) + total_accepted
        state["rejected"] = state.get("rejected", 0) + total_rejected
        state["last_files"] = [x["file"] for x in batch_results]

        save_state(state)

        log_file = (
            LOG_DIR /
            f"batch_{batch_no:03d}.json"
        )

        log_file.write_text(
            json.dumps(
                {
                    "batch": batch_no,
                    "results": batch_results,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        final_score, final_errors = score_project()

        log("")
        log(f"[BATCH SCORE] {initial_score} -> {final_score}")

        if final_score < initial_score:
            log("!!! GLOBAL SCORE WORSENED - STOPPING SAFELY !!!")
            break

        if final_score == initial_score:
            log("No measurable improvement in this batch.")
            break

        initial_score = final_score

    log("")
    log("=" * 70)
    log(" FINISHED")
    log("=" * 70)
    log(f"Accepted : {total_accepted}")
    log(f"Rejected : {total_rejected}")
    log(f"Logs     : {LOG_DIR}")
    log(f"Backups  : {BACKUP_DIR}")
    log("=" * 70)


if __name__ == "__main__":
    main()
