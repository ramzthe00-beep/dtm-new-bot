import inspect
from pynecore.lib import ta

print("=" * 70)
print("  PYNECORE TA FUNCTIONS — EXACT SIGNATURES")
print("=" * 70)

for fn_name in ["rsi", "macd", "atr", "sma", "linreg", "lowest", "highest",
                "pivothigh", "pivotlow", "valuewhen"]:
    fn = getattr(ta, fn_name, None)
    if fn is None:
        print(f"{fn_name}: NOT FOUND")
        continue
    try:
        sig = inspect.signature(fn)
        print(f"{fn_name}: {sig}")
    except (TypeError, ValueError) as e:
        print(f"{fn_name}: signature not introspectable — {e}")
