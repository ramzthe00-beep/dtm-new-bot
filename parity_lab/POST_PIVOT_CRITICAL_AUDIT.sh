#!/data/data/com.termux/files/usr/bin/bash

set +e

cd ~/dtm-new-bot || exit 1

OUT="parity_lab/POST_PIVOT_CRITICAL_AUDIT_$(date +%Y%m%d_%H%M%S).txt"

exec > >(tee "$OUT") 2>&1

echo "============================================================"
echo " POST-PIVOT CRITICAL FORENSIC AUDIT"
echo " Priority: DIVERGENCE INDEXING"
echo "============================================================"
echo "DATE: $(date)"
echo

echo "============================================================"
echo "1. WHY THIS AUDIT IS CRITICAL"
echo "============================================================"
echo "Pivot structural audit has already PASSed."
echo
echo "The next critical parity risk is:"
echo
echo "Pivot confirmation"
echo "        -> actual pivot position"
echo "        -> RSI/MACD/Histogram sampling"
echo "        -> previous pivot sampling"
echo "        -> divergence comparison"
echo "        -> signal generation"
echo
echo "A structurally correct Pivot can still produce wrong signals"
echo "if indicators are sampled on the confirmation bar instead of"
echo "the ORIGINAL pivot bar."
echo

echo "============================================================"
echo "2. ACTIVE DIVERGENCE CODE"
echo "============================================================"
sed -n '125,270p' strategy.py
echo

echo "============================================================"
echo "3. ALL INDEXING REFERENCES"
echo "============================================================"
grep -nE \
'confirmation_idx|curr_pivot_pos|prev_pivot_pos|RIGHT_BARS|iloc\[|loc\[' \
strategy.py
echo

echo "============================================================"
echo "4. CHECK CURRENT PIVOT -> INDICATOR INDEXING"
echo "============================================================"

if grep -qE \
'curr_pivot_pos[[:space:]]*=[[:space:]]*confirmation_idx[[:space:]]*-[[:space:]]*RIGHT_BARS' \
strategy.py
then
    echo "PASS: current pivot maps back from confirmation to original pivot"
else
    echo "FAIL: current pivot does NOT clearly map back by RIGHT_BARS"
fi

echo

echo "============================================================"
echo "5. CHECK PREVIOUS PIVOT -> INDICATOR INDEXING"
echo "============================================================"

if grep -qE \
'prev_pivot_pos[[:space:]]*=.*-[[:space:]]*RIGHT_BARS' \
strategy.py
then
    echo "PASS: previous pivot maps back from confirmation to original pivot"
else
    echo "FAIL: previous pivot mapping is missing or suspicious"
fi

echo

echo "============================================================"
echo "6. RSI INDEXING"
echo "============================================================"

grep -nE \
'rsi_val.*curr_pivot_pos|rsi_val.*prev_pivot_pos' \
strategy.py

if grep -qE \
'rsi_val\.iloc\[curr_pivot_pos\]' \
strategy.py &&
grep -qE \
'rsi_val\.iloc\[prev_pivot_pos\]' \
strategy.py
then
    echo "PASS: RSI is sampled at actual pivot positions"
else
    echo "FAIL: RSI is not clearly sampled at actual pivot positions"
fi

echo

echo "============================================================"
echo "7. MACD INDEXING"
echo "============================================================"

grep -nE \
'macd_line.*curr_pivot_pos|macd_line.*prev_pivot_pos' \
strategy.py

if grep -qE \
'macd_line\.iloc\[curr_pivot_pos\]' \
strategy.py &&
grep -qE \
'macd_line\.iloc\[prev_pivot_pos\]' \
strategy.py
then
    echo "PASS: MACD line is sampled at actual pivot positions"
else
    echo "FAIL: MACD line indexing requires investigation"
fi

echo

echo "============================================================"
echo "8. HISTOGRAM INDEXING"
echo "============================================================"

grep -nE \
'hist_line.*curr_pivot_pos|hist_line.*prev_pivot_pos' \
strategy.py

if grep -qE \
'hist_line\.iloc\[curr_pivot_pos\]' \
strategy.py &&
grep -qE \
'hist_line\.iloc\[prev_pivot_pos\]' \
strategy.py
then
    echo "PASS: MACD histogram is sampled at actual pivot positions"
else
    echo "FAIL: Histogram indexing requires investigation"
fi

echo

echo "============================================================"
echo "9. CHECK FOR CONFIRMATION-BAR SAMPLING BUG"
echo "============================================================"

python - <<'PY'
from pathlib import Path
import re

src = Path("strategy.py").read_text()

dangerous = []

patterns = [
    r'rsi_val\.iloc\[confirmation_idx\]',
    r'macd_line\.iloc\[confirmation_idx\]',
    r'hist_line\.iloc\[confirmation_idx\]',
]

for p in patterns:
    for m in re.finditer(p, src):
        line = src[:m.start()].count("\n") + 1
        dangerous.append((line, m.group(0)))

if dangerous:
    print("FAIL: Indicator sampled directly on confirmation_idx")
    for line, text in dangerous:
        print(f"  line {line}: {text}")
else:
    print("PASS: No direct RSI/MACD/Histogram sampling at confirmation_idx")
PY

echo

echo "============================================================"
echo "10. CHECK FOR SECONDARY SHIFT AFTER curr_pivot_pos"
echo "============================================================"

python - <<'PY'
from pathlib import Path
import re

src = Path("strategy.py").read_text()

patterns = [
    r'curr_pivot_pos\s*[-+]\s*RIGHT_BARS',
    r'prev_pivot_pos\s*[-+]\s*RIGHT_BARS',
    r'curr_pivot_pos\s*[-+]\s*2',
    r'prev_pivot_pos\s*[-+]\s*2',
]

found = False

for p in patterns:
    for m in re.finditer(p, src):
        found = True
        line = src[:m.start()].count("\n") + 1
        print(f"WARNING: line {line}: {m.group(0)}")

if not found:
    print("PASS: No obvious secondary shift after pivot positions")
PY

echo

echo "============================================================"
echo "11. PREVIOUS PIVOT ORDERING"
echo "============================================================"

grep -nE \
'ph_prev|pl_prev|prev_confirmation_idx|dropna|iloc\[:confirmation_idx\]' \
strategy.py

echo

echo "============================================================"
echo "12. BEARISH DIVERGENCE CONDITIONS"
echo "============================================================"

grep -nE \
'price_higher_high|rsi_lower|macd_lower|hist_lower|hist_line.*> 0' \
strategy.py

echo

echo "============================================================"
echo "13. BULLISH DIVERGENCE CONDITIONS"
echo "============================================================"

grep -nE \
'price_lower_low|rsi_higher|macd_higher|hist_higher|hist_line.*< 0' \
strategy.py

echo

echo "============================================================"
echo "14. CRITICAL QUESTION"
echo "============================================================"
echo
echo "For every divergence comparison, verify:"
echo
echo "CURRENT PRICE = price at ORIGINAL pivot bar"
echo "PREVIOUS PRICE = price at ORIGINAL previous pivot bar"
echo "CURRENT RSI = RSI at ORIGINAL pivot bar"
echo "PREVIOUS RSI = RSI at ORIGINAL previous pivot bar"
echo "CURRENT MACD = MACD at ORIGINAL pivot bar"
echo "PREVIOUS MACD = MACD at ORIGINAL previous pivot bar"
echo "CURRENT HIST = histogram at ORIGINAL pivot bar"
echo "PREVIOUS HIST = histogram at ORIGINAL previous pivot bar"
echo
echo "NOT:"
echo "confirmation bar values."
echo

echo "============================================================"
echo "15. SEARCH PARITY DOCUMENTATION / PREVIOUS FINDINGS"
echo "============================================================"

grep -RniE \
'divergence indexing|confirmation bar|pivot bar|indicator indexing|RSI.*pivot|MACD.*pivot|double shift' \
parity_lab \
--exclude='POST_PIVOT_CRITICAL_AUDIT_*.txt' \
2>/dev/null | head -250

echo

echo "============================================================"
echo "16. PYTHON COMPILE"
echo "============================================================"

python -m py_compile strategy.py

if [ $? -eq 0 ]; then
    echo "PASS: strategy.py compiles"
else
    echo "FAIL: strategy.py compilation failed"
fi

echo

echo "============================================================"
echo "17. FINAL PRIORITY VERDICT"
echo "============================================================"

FAIL=0

if ! grep -qE \
'curr_pivot_pos[[:space:]]*=[[:space:]]*confirmation_idx[[:space:]]*-[[:space:]]*RIGHT_BARS' \
strategy.py
then
    echo "FAIL: Current pivot indexing is not explicitly confirmation - RIGHT_BARS"
    FAIL=$((FAIL+1))
else
    echo "PASS: Current pivot indexing"
fi

if ! grep -qE \
'prev_pivot_pos[[:space:]]*=.*-[[:space:]]*RIGHT_BARS' \
strategy.py
then
    echo "FAIL: Previous pivot indexing is not explicitly shifted back"
    FAIL=$((FAIL+1))
else
    echo "PASS: Previous pivot indexing"
fi

if grep -qE 'rsi_val\.iloc\[confirmation_idx\]' strategy.py; then
    echo "FAIL: RSI confirmation-bar sampling detected"
    FAIL=$((FAIL+1))
else
    echo "PASS: No RSI confirmation-bar sampling"
fi

if grep -qE 'macd_line\.iloc\[confirmation_idx\]' strategy.py; then
    echo "FAIL: MACD confirmation-bar sampling detected"
    FAIL=$((FAIL+1))
else
    echo "PASS: No MACD confirmation-bar sampling"
fi

if grep -qE 'hist_line\.iloc\[confirmation_idx\]' strategy.py; then
    echo "FAIL: Histogram confirmation-bar sampling detected"
    FAIL=$((FAIL+1))
else
    echo "PASS: No Histogram confirmation-bar sampling"
fi

echo

if [ "$FAIL" -eq 0 ]; then
    echo "============================================================"
    echo "POST-PIVOT STRUCTURAL RESULT = PASS"
    echo "============================================================"
    echo
    echo "No immediate structural divergence-indexing defect detected."
    echo
    echo "NEXT REQUIRED STEP:"
    echo "DATA-LEVEL Pine vs Python divergence parity."
else
    echo "============================================================"
    echo "POST-PIVOT STRUCTURAL RESULT = FAIL"
    echo "============================================================"
    echo
    echo "CRITICAL FAILURES: $FAIL"
    echo
    echo "Do NOT repair automatically."
    echo "Inspect the exact failing lines."
fi

echo
echo "AUDIT FILE:"
echo "$OUT"
echo
echo "============================================================"
echo "END"
echo "============================================================"

