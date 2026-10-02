# ═══════════════════════════════════════════════════════════
# final_rules.py — قوانین نهایی ربات (تأییدشده)
# نتیجه: +580.4R در 24 ماه | 770 معامله
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
        "weekdays": [0, 1, 2, 3, 4],
        "enable_risk_free": True,
    },  # n=69, R_net=+88.2

    "ETHUSDT": {
        "kind": "Anni-L",
        "direction": "LONG",
        "timeframe": "4h",
        "min_stop_pct": 0.0,
        "max_stop_pct": 100.0,
        "min_adx": None,
        "avoid_rsi_div": False,
        "weekdays": None,
        "enable_risk_free": False,
    },  # n=110, R_net=+212.7

    "BNBUSDT": {
        "kind": "Aati-L",
        "direction": "LONG",
        "timeframe": "1h",
        "min_stop_pct": 0.5,
        "max_stop_pct": 2.0,
        "min_adx": 20,
        "avoid_rsi_div": False,
        "weekdays": None,
        "enable_risk_free": False,
    },  # n=238, R_net=+161.6

    "SOLUSDT": {
        "kind": "Aati-L",
        "direction": "LONG",
        "timeframe": "1h",
        "min_stop_pct": 0.0,
        "max_stop_pct": 2.0,
        "min_adx": None,
        "avoid_rsi_div": False,
        "weekdays": None,
        "enable_risk_free": False,
    },  # n=353, R_net=+117.8
}
