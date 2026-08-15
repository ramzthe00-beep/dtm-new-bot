# -*- coding: utf-8 -*-
"""
DTM Strategy — PyneCore (exact, no MTF)
"""
from pynecore import pine_range
from pynecore.lib import (
    bar_index, close, high, low, math, na, ta
)
from pynecore.types import Persistent, Series

LEFT_BARS = 5
RIGHT_BARS = 3

RSI_LEN = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIG = 9
TREND_LOOKBACK = 20
TREND_SLOPE_MIN_PCT = 0.05
FIB_TREND_SEARCH_BARS = 100
FIB_TOLERANCE_PCT = 0.5
FIB_USE_618 = True
FIB_USE_786 = True
ENABLE_HIDDEN = True

def calculate_signals(df):
    """Run PyneCore logic on DataFrame and return last bar signals."""
    close_vals = df["close"].to_numpy()
    high_vals = df["high"].to_numpy()
    low_vals = df["low"].to_numpy()

    rsi_val = ta.rsi(close_vals, RSI_LEN)
    macd_line, signal_line, hist_line = ta.macd(close_vals, MACD_FAST, MACD_SLOW, MACD_SIG)
    atr14 = ta.atr(14)

    pivot_high = ta.pivothigh(high_vals, LEFT_BARS, RIGHT_BARS)
    pivot_low = ta.pivotlow(low_vals, LEFT_BARS, RIGHT_BARS)

    rsi_at_ph = ta.valuewhen(~na(pivot_high), rsi_val[RIGHT_BARS], 0)
    rsi_at_pl = ta.valuewhen(~na(pivot_low), rsi_val[RIGHT_BARS], 0)
    macd_at_ph = ta.valuewhen(~na(pivot_high), macd_line[RIGHT_BARS], 0)
    macd_at_pl = ta.valuewhen(~na(pivot_low), macd_line[RIGHT_BARS], 0)
    hist_at_ph = ta.valuewhen(~na(pivot_high), hist_line[RIGHT_BARS], 0)
    hist_at_pl = ta.valuewhen(~na(pivot_low), hist_line[RIGHT_BARS], 0)

    # Track last two pivots
    ph_price_1 = None
    ph_price_2 = None
    ph_rsi_1 = None
    ph_rsi_2 = None
    ph_macd_1 = None
    ph_macd_2 = None
    ph_hist_1 = None
    ph_hist_2 = None
    ph_bar_1 = None
    ph_bar_2 = None

    pl_price_1 = None
    pl_price_2 = None
    pl_rsi_1 = None
    pl_rsi_2 = None
    pl_macd_1 = None
    pl_macd_2 = None
    pl_hist_1 = None
    pl_hist_2 = None
    pl_bar_1 = None
    pl_bar_2 = None

    current_bar = len(df) - 1
    new_ph = not pd_isna(pivot_high[-1])
    new_pl = not pd_isna(pivot_low[-1])

    if new_ph:
        ph_price_1 = ph_price_2
        ph_rsi_1 = ph_rsi_2
        ph_macd_1 = ph_macd_2
        ph_hist_1 = ph_hist_2
        ph_bar_1 = ph_bar_2

        ph_price_2 = float(pivot_high[-1])
        ph_bar_2 = current_bar - RIGHT_BARS
        ph_rsi_2 = float(rsi_at_ph)
        ph_macd_2 = float(macd_at_ph)
        ph_hist_2 = float(hist_at_ph)

    if new_pl:
        pl_price_1 = pl_price_2
        pl_rsi_1 = pl_rsi_2
        pl_macd_1 = pl_macd_2
        pl_hist_1 = pl_hist_2
        pl_bar_1 = pl_bar_2

        pl_price_2 = float(pivot_low[-1])
        pl_bar_2 = current_bar - RIGHT_BARS
        pl_rsi_2 = float(rsi_at_pl)
        pl_macd_2 = float(macd_at_pl)
        pl_hist_2 = float(hist_at_pl)

    # Classic Bearish
    if new_ph and ph_bar_1 is not None:
        price_higher_high = ph_price_2 > ph_price_1
        rsi_lower_high = ph_rsi_2 < ph_rsi_1
        macd_lower_high = ph_macd_2 < ph_macd_1
        hist_lower_high = ph_hist_2 < ph_hist_1
        both_peaks_green = ph_hist_1 > 0 and ph_hist_2 > 0

        # color change check
        color_changed = False
        start = int(ph_bar_1) + 1
        end = int(ph_bar_2)
        for i in range(start, end + 1):
            if i < len(hist_line) and hist_line[i] < 0:
                color_changed = True
                break

        if price_higher_high and rsi_lower_high and macd_lower_high and hist_lower_high and both_peaks_green and color_changed:
            return "SELL", float(close_vals[-1])

    # Classic Bullish
    if new_pl and pl_bar_1 is not None:
        price_lower_low = pl_price_2 < pl_price_1
        rsi_higher_low = pl_rsi_2 > pl_rsi_1
        macd_higher_low = pl_macd_2 > pl_macd_1
        hist_higher_low = pl_hist_2 > pl_hist_1
        both_troughs_red = pl_hist_1 < 0 and pl_hist_2 < 0

        color_changed = False
        start = int(pl_bar_1) + 1
        end = int(pl_bar_2)
        for i in range(start, end + 1):
            if i < len(hist_line) and hist_line[i] > 0:
                color_changed = True
                break

        if price_lower_low and rsi_higher_low and macd_higher_low and hist_higher_low and both_troughs_red and color_changed:
            return "BUY", float(close_vals[-1])

    return None, None

def pd_isna(x):
    try:
        import pandas as pd
        return pd.isna(x)
    except ImportError:
        return x is None or (isinstance(x, float) and math.isnan(x))
