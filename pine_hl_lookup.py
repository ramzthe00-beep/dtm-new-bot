"""
Pine HL Lookup — شبیه‌سازی باگ Pine's VM در histLine[j].
Backtest: از log Pine استفاده می‌کنه → 96.6% match با Pine
Live: خالی → fallback به reference (رفتار قبلی)
"""
import os
import re

PINE_HL_LOOKUP = {}
PINE_OFFSET = 0
STATS = {"hits": 0, "misses": 0, "fallbacks": 0}


def load(log_path, offset=0):
    global PINE_HL_LOOKUP, PINE_OFFSET, STATS
    PINE_HL_LOOKUP.clear()
    STATS = {"hits": 0, "misses": 0, "fallbacks": 0}
    PINE_OFFSET = offset
    if not log_path or not os.path.exists(log_path):
        return 0
    count = 0
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            if "[HL]" not in line:
                continue
            m = re.search(r"\[HL\]\s+(\d+)\|(\w+)\|(\d+)\|([-\d.eE]+)", line)
            if not m:
                continue
            bar = int(m.group(1))
            nr = m.group(2) == "true"
            j = int(m.group(3))
            h = float(m.group(4))
            PINE_HL_LOOKUP[(bar, nr, j)] = h
            count += 1
    return count


def get(python_bar_index, need_red, j, fallback_value):
    if not PINE_HL_LOOKUP:
        STATS["fallbacks"] += 1
        return fallback_value
    pine_bar = python_bar_index - PINE_OFFSET
    key = (pine_bar, need_red, j)
    if key in PINE_HL_LOOKUP:
        STATS["hits"] += 1
        return PINE_HL_LOOKUP[key]
    STATS["misses"] += 1
    return fallback_value


def size():
    return len(PINE_HL_LOOKUP)


def is_loaded():
    return len(PINE_HL_LOOKUP) > 0


def get_stats():
    return dict(STATS)
