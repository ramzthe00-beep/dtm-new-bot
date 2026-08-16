#!/data/data/com.termux/files/usr/bin/bash

set +e

ROOT="$HOME/dtm-new-bot"
cd "$ROOT" || exit 1

OUT="parity_lab/FINAL_PIVOT_FORENSIC_AUDIT_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$OUT") 2>&1

echo "============================================================"
echo "        FINAL PIVOT FORENSIC PARITY AUDIT"
echo "============================================================"
echo "DATE: $(date)"
echo "ROOT: $ROOT"
echo

echo "============================================================"
echo "1. GIT STATE"
echo "============================================================"
git status --short --branch
echo
git log -3 --oneline
echo

echo "============================================================"
echo "2. ACTIVE PIVOT PARAMETERS"
echo "============================================================"
grep -nE 'LEFT_BARS|RIGHT_BARS' strategy.py
echo

echo "============================================================"
echo "3. ACTIVE PIVOT FUNCTIONS"
echo "============================================================"
sed -n '70,125p' strategy.py
echo

echo "============================================================"
echo "4. PIVOT CONFIRMATION / INDEXING LOGIC"
echo "============================================================"
grep -nE \
'last_confirmed|confirmation_idx|curr_pivot_pos|prev_pivot_pos|RIGHT_BARS|pivot_high|pivot_low' \
strategy.py
echo

echo "============================================================"
echo "5. CHECK FOR OLD DOUBLE-SHIFT PATTERNS"
echo "============================================================"

echo "--- last_confirmed patterns ---"
grep -nE \
'last_confirmed\s*=.*RIGHT_BARS.*RIGHT_BARS|last_confirmed\s*=.*2[[:space:]]*\*[[:space:]]*RIGHT_BARS' \
strategy.py || echo "PASS: No explicit double RIGHT_BARS subtraction"

echo
echo "--- confirmation_idx double shifts ---"
grep -nE \
'confirmation_idx.*RIGHT_BARS.*RIGHT_BARS|confirmation_idx.*2[[:space:]]*\*[[:space:]]*RIGHT_BARS' \
strategy.py || echo "PASS: No double shift on confirmation_idx"

echo
echo "--- pivot position double shifts ---"
grep -nE \
'curr_pivot_pos.*RIGHT_BARS.*RIGHT_BARS|prev_pivot_pos.*RIGHT_BARS.*RIGHT_BARS' \
strategy.py || echo "PASS: No explicit double shift in pivot positions"

echo
echo "============================================================"
echo "6. CHECK FOR VALID SINGLE CONFIRMATION OFFSET"
echo "============================================================"

grep -nE \
'confirmation_idx[[:space:]]*=[[:space:]]*n[[:space:]]*-[[:space:]]*1' \
strategy.py

if grep -qE \
'confirmation_idx[[:space:]]*=[[:space:]]*n[[:space:]]*-[[:space:]]*1' \
strategy.py
then
    echo "PASS: confirmation_idx is current/latest bar"
else
    echo "FAIL: confirmation_idx logic not found"
fi

echo
echo "--- actual pivot position ---"

grep -nE \
'curr_pivot_pos[[:space:]]*=.*confirmation_idx.*RIGHT_BARS|prev_pivot_pos[[:space:]]*=.*RIGHT_BARS' \
strategy.py

echo

echo "============================================================"
echo "7. CHECK PIVOT FUNCTION SEMANTICS"
echo "============================================================"

python - <<'PY'
import ast
from pathlib import Path

p = Path("strategy.py")
src = p.read_text()

tree = ast.parse(src)

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef) and node.name in ("pivot_high", "pivot_low"):
        print(f"FUNCTION: {node.name}")
        for i, line in enumerate(src.splitlines(), 1):
            if node.lineno <= i <= getattr(node, "end_lineno", node.lineno):
                print(f"{i}: {line}")
        print()
PY

echo

echo "============================================================"
echo "8. CHECK FOR Pine pivot semantics"
echo "============================================================"

if grep -qE \
'out\.iloc\[i[[:space:]]*\+[[:space:]]*right\][[:space:]]*=[[:space:]]*x' \
strategy.py
then
    echo "PASS: Pivot value is emitted on confirmation bar i + right"
else
    echo "FAIL: Expected i + right confirmation placement not found"
fi

if grep -qE \
'for i in range\(left,[[:space:]]*n[[:space:]]*-[[:space:]]*right\)' \
strategy.py
then
    echo "PASS: Pivot scan respects left/right confirmation window"
else
    echo "WARNING: Pivot scan loop differs from expected structure"
fi

echo

echo "============================================================"
echo "9. CHECK STRICT PIVOT COMPARISON"
echo "============================================================"

grep -nE \
'left_max|right_max|left_min|right_min|< x|> x' \
strategy.py

echo

echo "============================================================"
echo "10. CHECK DIVERGENCE INDEXING"
echo "============================================================"

sed -n '125,270p' strategy.py

echo

echo "============================================================"
echo "11. CHECK FOR FORBIDDEN SECOND SHIFT"
echo "============================================================"

python - <<'PY'
from pathlib import Path
import re

src = Path("strategy.py").read_text()

patterns = {
    "double_RIGHT_BARS":
        r'RIGHT_BARS\s*[-+].*RIGHT_BARS|RIGHT_BARS.*[-+].*RIGHT_BARS',

    "2x_RIGHT_BARS":
        r'2\s*\*\s*RIGHT_BARS|RIGHT_BARS\s*\*\s*2',

    "double_confirmation_shift":
        r'confirmation_idx.*RIGHT_BARS.*RIGHT_BARS',

    "double_pivot_shift":
        r'(curr_pivot_pos|prev_pivot_pos).*RIGHT_BARS.*RIGHT_BARS',
}

found = False

for name, pattern in patterns.items():
    matches = list(re.finditer(pattern, src, re.I))
    if matches:
        found = True
        print(f"FAIL: {name}")
        for m in matches:
            line = src[:m.start()].count("\n") + 1
            print(f"  line {line}: {m.group(0)}")
    else:
        print(f"PASS: {name}")

if not found:
    print()
    print("RESULT: No explicit double RIGHT_BARS pattern found.")
PY

echo

echo "============================================================"
echo "12. CHECK ALL PIVOT REFERENCES IN ACTIVE CODE"
echo "============================================================"

grep -nEi \
'pivot|RIGHT_BARS|LEFT_BARS|confirmation' \
strategy.py

echo

echo "============================================================"
echo "13. CHECK BACKUPS / OLD VERSIONS FOR COMPARISON"
echo "============================================================"

find parity_lab -type f \( \
-name "*.py" -o \
-name "*.txt" -o \
-name "*.pine" \
\) 2>/dev/null | grep -Ei \
'pivot|repair|backup|strategy|audit' | head -300

echo

echo "============================================================"
echo "14. SEARCH FOR OLD PIVOT BUG SIGNATURES"
echo "============================================================"

grep -RniE \
'last_confirmed[[:space:]]*=.*RIGHT_BARS.*RIGHT_BARS|2[[:space:]]*\*[[:space:]]*RIGHT_BARS|double shift|double-shift|DOUBLE SHIFT|second RIGHT_BARS|second shift' \
--exclude-dir='.git' \
--exclude='FINAL_PIVOT_FORENSIC_AUDIT_*.txt' \
. 2>/dev/null | head -300

echo

echo "============================================================"
echo "15. PYTHON COMPILE"
echo "============================================================"

python -m py_compile strategy.py

if [ $? -eq 0 ]; then
    echo "PASS: strategy.py compiles successfully"
else
    echo "FAIL: strategy.py compilation failed"
fi

echo

echo "============================================================"
echo "16. AST / FUNCTION STRUCTURE CHECK"
echo "============================================================"

python - <<'PY'
import ast
from pathlib import Path

p = Path("strategy.py")

try:
    tree = ast.parse(p.read_text())
    funcs = [
        n.name for n in ast.walk(tree)
        if isinstance(n, ast.FunctionDef)
    ]

    print("PASS: AST parse successful")
    print("Functions:")
    for f in funcs:
        print("  -", f)

except Exception as e:
    print("FAIL:", repr(e))
PY

echo

echo "============================================================"
echo "17. FINAL AUTOMATIC VERDICT"
echo "============================================================"

FAIL_COUNT=0

if ! grep -qE \
'LEFT_BARS[[:space:]]*=[[:space:]]*5' strategy.py
then
    echo "FAIL: LEFT_BARS is not 5"
    FAIL_COUNT=$((FAIL_COUNT+1))
else
    echo "PASS: LEFT_BARS = 5"
fi

if ! grep -qE \
'RIGHT_BARS[[:space:]]*=[[:space:]]*3' strategy.py
then
    echo "FAIL: RIGHT_BARS is not 3"
    FAIL_COUNT=$((FAIL_COUNT+1))
else
    echo "PASS: RIGHT_BARS = 3"
fi

if ! grep -qE \
'confirmation_idx[[:space:]]*=[[:space:]]*n[[:space:]]*-[[:space:]]*1' \
strategy.py
then
    echo "FAIL: confirmation_idx does not appear to use current bar"
    FAIL_COUNT=$((FAIL_COUNT+1))
else
    echo "PASS: confirmation_idx = n - 1"
fi

if ! grep -qE \
'out\.iloc\[i[[:space:]]*\+[[:space:]]*right\][[:space:]]*=[[:space:]]*x' \
strategy.py
then
    echo "FAIL: pivot confirmation placement i + right not found"
    FAIL_COUNT=$((FAIL_COUNT+1))
else
    echo "PASS: pivot value emitted at i + right"
fi

if grep -qE \
'last_confirmed\s*=.*RIGHT_BARS.*RIGHT_BARS|2[[:space:]]*\*[[:space:]]*RIGHT_BARS' \
strategy.py
then
    echo "FAIL: explicit double RIGHT_BARS shift detected"
    FAIL_COUNT=$((FAIL_COUNT+1))
else
    echo "PASS: no explicit double RIGHT_BARS shift"
fi

echo

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "============================================================"
    echo "FINAL RESULT: PIVOT STRUCTURAL AUDIT = PASS"
    echo "============================================================"
    echo
    echo "No known structural Pivot / RIGHT_BARS / confirmation"
    echo "double-shift defect was detected in active strategy.py."
    echo
    echo "IMPORTANT:"
    echo "This proves structural correctness only."
    echo "It does NOT yet prove numerical Pine/Python parity."
    echo "A data-level parity test is still required."
else
    echo "============================================================"
    echo "FINAL RESULT: PIVOT STRUCTURAL AUDIT = FAIL"
    echo "============================================================"
    echo
    echo "FAILURES DETECTED: $FAIL_COUNT"
    echo "Do NOT make another repair automatically."
    echo "Inspect the exact FAIL lines above first."
fi

echo
echo "AUDIT FILE:"
echo "$OUT"
echo
echo "============================================================"
echo "END OF FINAL PIVOT FORENSIC AUDIT"
echo "============================================================"

