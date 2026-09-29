# ═══════════════════════════════════════════════════════════
# final_rules.py — قوانین نهایی ربات
# بر اساس تست ۲۴ ماه (۲۰۲۵ + ۲۰۲۶)
# نتیجه: +547.4R | ماهانه +22.81R | ریسک 5U: +114 USDT/ماه
# ═══════════════════════════════════════════════════════════

FINAL_RULES = {
    "BTCUSDT": {
        "kind": "Anni-L",
        "direction": "LONG",
        "timeframe": "4h",
        "min_stop_pct": 0.3,
        "max_stop_pct": 2.0,
        "min_adx": 25,
        "avoid_rsi_div": False,
        "weekdays": [0, 1, 2, 3, 4],   # Mon-Fri (0=Monday)
        "enable_risk_free": True,
    },
    "ETHUSDT": {
        "kind": "Anni-S",
        "direction": "SHORT",
        "timeframe": "1h",
        "min_stop_pct": 0.0,
        "max_stop_pct": 100.0,
        "min_adx": None,
        "avoid_rsi_div": True,
        "weekdays": [0, 1, 2, 3, 4],
        "enable_risk_free": False,
    },
    "BNBUSDT": {
        "kind": "Aati-L",
        "direction": "LONG",
        "timeframe": "1h",
        "min_stop_pct": 0.3,
        "max_stop_pct": 2.0,
        "min_adx": 20,
        "avoid_rsi_div": False,
        "weekdays": None,
        "enable_risk_free": False,
    },
    "SOLUSDT": {
        "kind": "Aati-L",
        "direction": "LONG",
        "timeframe": "1h",
        "min_stop_pct": 0.0,
        "max_stop_pct": 2.0,
        "min_adx": None,
        "avoid_rsi_div": True,
        "weekdays": None,
        "enable_risk_free": False,
    },
}