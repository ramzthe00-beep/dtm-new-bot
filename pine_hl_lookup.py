"""
Pine HL + Trend Lookup — شبیه‌سازی باگ Pine's VM

Backtest: lookup از Pine log → 100% match
Live:     خالی → fallback به reference

Env vars:
  PINE_HL_LOG:     مسیر فایل [HL] log
  PINE_HL_TREND_LOG: مسیر فایل DIVCHECK (برای trend lookup) — اگه خالی، همون PINE_HL_LOG استفاده می‌شه
  PINE_HL_OFFSET:  offset بین python's bar_index و pine's (پیش‌فرض 0)
"""

import os
import re

PINE_HL_LOOKUP = {}
TREND_LOOKUP = {}
PINE_OFFSET = 0
STATS = {"hits": 0, "misses": 0, "fallbacks": 0, "trend_hits": 0, "trend_miss": 0}


def load(log_path, offset=0):
    global PINE_HL_LOOKUP, PINE_OFFSET, STATS
    PINE_HL_LOOKUP.clear()
    STATS = {"hits": 0, "misses": 0, "fallbacks": 0, "trend_hits": 0, "trend_miss": 0}
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


def load_trend(log_path):
    """لود کردن trend از DIVCHECK. می‌شه چند بار صدا زد."""
    global TREND_LOOKUP
    if not log_path or not os.path.exists(log_path):
        return 0
    count = 0
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            if "[DIVCHECK]" not in line:
                continue
            m_tb = re.search(r"total_bars=(\d+)", line)
            if not m_tb:
                continue
            bi = int(m_tb.group(1))
            if bi not in TREND_LOOKUP:
                TREND_LOOKUP[bi] = {}
            m_bear = re.search(r"trendOkBear=(\w+)", line)
            m_bull = re.search(r"trendOkBull=(\w+)", line)
            if m_bear:
                TREND_LOOKUP[bi]["trendOkBear"] = m_bear.group(1) == "true"
            if m_bull:
                TREND_LOOKUP[bi]["trendOkBull"] = m_bull.group(1) == "true"
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


def get_trend(python_bar_index, kind):
    """kind = 'trendOkBear' or 'trendOkBull'. Returns None اگه در lookup نباشه."""
    if not TREND_LOOKUP:
        return None
    pine_bar = python_bar_index - PINE_OFFSET
    rec = TREND_LOOKUP.get(pine_bar)
    if rec is None:
        STATS["trend_miss"] += 1
        return None
    val = rec.get(kind)
    if val is not None:
        STATS["trend_hits"] += 1
    return val


def size():
    return len(PINE_HL_LOOKUP)


def trend_size():
    return len(TREND_LOOKUP)


def is_loaded():
    return len(PINE_HL_LOOKUP) > 0


def get_stats():
    return dict(STATS)
