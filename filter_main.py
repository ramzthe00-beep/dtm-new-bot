# ═══════════════════════════════════════════════════════════
# filter_main.py — بررسی اینکه آیا سیگنال باید گرفته شود
# ═══════════════════════════════════════════════════════════
import pandas as pd
from datetime import datetime, timezone
from final_rules import FINAL_RULES
from filter_utils import compute_adx, check_rsi_divergence


def should_take_signal(signal, ohlcv_df):
    """
    بررسی می‌کند آیا سیگنال باید گرفته شود.

    signal = {
        "symbol": "BTCUSDT",
        "kind": "Anni-L",
        "direction": "LONG",
        "timeframe": "4h",
        "risk_pct": 1.2,           # درصد استاپ
        "time_utc": datetime,      # زمان سیگنال (UTC)
    }

    ohlcv_df = dataframe با ستون‌های open, high, low, close
               (تایم‌فریم مطابق signal["timeframe"])

    Returns: (bool: take?, str: reason)
    """
    sym = signal["symbol"]

    # ۱) نماد در لیست فعال است؟
    if sym not in FINAL_RULES:
        return False, f"{sym} در قوانین نهایی نیست"

    rule = FINAL_RULES[sym]

    # ۲) بررسی شرط‌های پایه
    if signal["kind"] != rule["kind"]:
        return False, f"kind: {signal['kind']} ≠ {rule['kind']}"

    if signal["direction"] != rule["direction"]:
        return False, f"direction: {signal['direction']} ≠ {rule['direction']}"

    if signal["timeframe"] != rule["timeframe"]:
        return False, f"timeframe: {signal['timeframe']} ≠ {rule['timeframe']}"

    # ۳) بررسی risk_pct
    rp = signal["risk_pct"]
    if rp < rule["min_stop_pct"]:
        return False, f"risk {rp:.3f}% < min {rule['min_stop_pct']}%"

    if rp > rule["max_stop_pct"]:
        return False, f"risk {rp:.3f}% > max {rule['max_stop_pct']}%"

    # ۴) بررسی روز هفته
    if rule["weekdays"] is not None:
        wd = signal["time_utc"].weekday()  # 0=Mon, 6=Sun
        if wd not in rule["weekdays"]:
            return False, f"weekday {wd} غیرمجاز"

    # ۵) بررسی ADX (اگر لازم باشد)
    if rule["min_adx"] is not None:
        adx_series = compute_adx(ohlcv_df)
        current_adx = adx_series.iloc[-1]
        if pd.isna(current_adx):
            return False, "ADX نامعتبر"
        if current_adx < rule["min_adx"]:
            return False, f"ADX {current_adx:.1f} < {rule['min_adx']}"

    # ۶) بررسی RSI Divergence (اگر لازم باشد)
    if rule["avoid_rsi_div"]:
        if check_rsi_divergence(ohlcv_df, signal["direction"]):
            return False, "RSI واگرایی مضر"

    # ✅ همه شرط‌ها پاس شد
    return True, "OK"


def get_risk_free_enabled(symbol):
    """بررسی اینکه RF برای این نماد فعال است یا نه"""
    if symbol not in FINAL_RULES:
        return False
    return FINAL_RULES[symbol]["enable_risk_free"]