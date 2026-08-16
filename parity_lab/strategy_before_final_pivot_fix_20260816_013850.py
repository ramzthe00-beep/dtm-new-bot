# -*- coding: utf-8 -*-
"""
DTM Signal Engine — ریاضی معادل PyneCore (بدون وابستگی)
"""
import pandas as pd
import numpy as np

LEFT_BARS = 5
RIGHT_BARS = 3
RSI_LEN = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIG = 9

def rma(s, length):
    out = pd.Series(np.nan, index=s.index)
    vals = s.to_numpy(dtype=float)
    valid = ~np.isnan(vals)
    if valid.sum() < length:
        return out
    seed_idx = np.where(valid)[0][length - 1]
    seed = vals[seed_idx - length + 1: seed_idx + 1].mean()
    out.iloc[seed_idx] = seed
    alpha = 1.0 / length
    prev = seed
    for i in range(seed_idx + 1, len(vals)):
        if np.isnan(vals[i]):
            out.iloc[i] = prev
        else:
            prev = alpha * vals[i] + (1 - alpha) * prev
            out.iloc[i] = prev
    return out

def ema(s, length):
    out = pd.Series(np.nan, index=s.index)
    vals = s.to_numpy(dtype=float)
    valid = ~np.isnan(vals)
    if valid.sum() < length:
        return out
    seed_idx = np.where(valid)[0][length - 1]
    seed = vals[seed_idx - length + 1: seed_idx + 1].mean()
    out.iloc[seed_idx] = seed
    alpha = 2.0 / (length + 1)
    prev = seed
    for i in range(seed_idx + 1, len(vals)):
        if np.isnan(vals[i]):
            out.iloc[i] = prev
        else:
            prev = alpha * vals[i] + (1 - alpha) * prev
            out.iloc[i] = prev
    return out

def rsi(close, length=RSI_LEN):
    diff = close.diff()
    gain = diff.clip(lower=0)
    loss = -diff.clip(upper=0)
    ag = rma(gain, length)
    al = rma(loss, length)
    rs = ag / al.replace(0, np.nan)
    out = 100 - (100 / (1 + rs))
    out = out.mask((al == 0) & (ag > 0), 100)
    out = out.mask((ag == 0) & (al > 0), 0)
    return out

def macd(close, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIG):
    ef = ema(close, fast)
    es = ema(close, slow)
    line = ef - es
    sig = ema(line, signal)
    hist = line - sig
    return line, sig, hist

def atr(high, low, close, length=14):
    prev_close = close.shift(1)
    tr = pd.concat([high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return rma(tr, length)

def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
    """
    Pine ta.pivothigh(high, left, right) semantics.

    The pivot is CONFIRMED on bar i + right, but its value belongs
    to the original pivot bar i.  We therefore store the value on
    the confirmation bar, exactly like Pine's returned series.
    """
    out = pd.Series(np.nan, index=high.index, dtype=float)
    n = len(high)

    for i in range(left, n - right):
        x = high.iloc[i]

        left_max = high.iloc[i-left:i].max()
        right_max = high.iloc[i+1:i+right+1].max()

        if left_max < x and right_max < x:
            out.iloc[i + right] = x

    return out


def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
    """
    Pine ta.pivotlow(low, left, right) semantics.
    Returned value appears on the confirmation bar i + right,
    while the actual pivot price belongs to bar i.
    """
    out = pd.Series(np.nan, index=low.index, dtype=float)
    n = len(low)

    for i in range(left, n - right):
        x = low.iloc[i]

        left_min = low.iloc[i-left:i].min()
        right_min = low.iloc[i+1:i+right+1].min()

        if left_min > x and right_min > x:
            out.iloc[i + right] = x

    return out


def calculate_signals(df):
    close = df['close']
    high = df['high']
    low = df['low']

    rsi_val = rsi(close)
    macd_line, signal_line, hist_line = macd(close)
    atr_val = atr(high, low, close)

    ph = pivot_high(high)
    pl = pivot_low(low)

    n = len(df)

    if n <= RIGHT_BARS:
        return None, None

    # IMPORTANT:
    # ph/pl are Pine-style SERIES.
    # A newly confirmed pivot exists on the CURRENT bar (-1).
    # Do NOT subtract RIGHT_BARS again.
    confirmation_idx = n - 1

    new_ph = not pd.isna(ph.iloc[confirmation_idx])
    new_pl = not pd.isna(pl.iloc[confirmation_idx])

    # ---------------------------------------------------------
    # PIVOT HIGH / BEARISH DIVERGENCE
    # ---------------------------------------------------------
    if new_ph:
        ph_prev = ph.iloc[:confirmation_idx].dropna()

        if len(ph_prev) >= 1:
            prev_confirmation_idx = ph_prev.index[-1]

            curr_ph_price = float(ph.iloc[confirmation_idx])
            prev_ph_price = float(ph.loc[prev_confirmation_idx])

            # The actual pivot bar is RIGHT_BARS bars BEFORE
            # the confirmation bar.
            curr_pivot_pos = confirmation_idx - RIGHT_BARS
            prev_confirmation_pos = df.index.get_loc(prev_confirmation_idx)
            prev_pivot_pos = prev_confirmation_pos - RIGHT_BARS

            if curr_pivot_pos >= 0 and prev_pivot_pos >= 0:

                price_higher_high = curr_ph_price > prev_ph_price

                rsi_lower = (
                    rsi_val.iloc[curr_pivot_pos]
                    < rsi_val.iloc[prev_pivot_pos]
                )

                macd_lower = (
                    macd_line.iloc[curr_pivot_pos]
                    < macd_line.iloc[prev_pivot_pos]
                )

                hist_lower = (
                    hist_line.iloc[curr_pivot_pos]
                    < hist_line.iloc[prev_pivot_pos]
                )

                both_green = (
                    hist_line.iloc[curr_pivot_pos] > 0
                    and hist_line.iloc[prev_pivot_pos] > 0
                )

                color_changed = False

                start = prev_pivot_pos + 1
                end = curr_pivot_pos

                for j in range(start, end):
                    if hist_line.iloc[j] < 0:
                        color_changed = True
                        break

                if (
                    price_higher_high
                    and rsi_lower
                    and macd_lower
                    and hist_lower
                    and both_green
                    and color_changed
                ):
                    return "SELL", float(close.iloc[-1])

    # ---------------------------------------------------------
    # PIVOT LOW / BULLISH DIVERGENCE
    # ---------------------------------------------------------
    if new_pl:
        pl_prev = pl.iloc[:confirmation_idx].dropna()

        if len(pl_prev) >= 1:
            prev_confirmation_idx = pl_prev.index[-1]

            curr_pl_price = float(pl.iloc[confirmation_idx])
            prev_pl_price = float(pl.loc[prev_confirmation_idx])

            # Actual pivot bars.
            curr_pivot_pos = confirmation_idx - RIGHT_BARS
            prev_confirmation_pos = df.index.get_loc(prev_confirmation_idx)
            prev_pivot_pos = prev_confirmation_pos - RIGHT_BARS

            if curr_pivot_pos >= 0 and prev_pivot_pos >= 0:

                price_lower_low = curr_pl_price < prev_pl_price

                rsi_higher = (
                    rsi_val.iloc[curr_pivot_pos]
                    > rsi_val.iloc[prev_pivot_pos]
                )

                macd_higher = (
                    macd_line.iloc[curr_pivot_pos]
                    > macd_line.iloc[prev_pivot_pos]
                )

                hist_higher = (
                    hist_line.iloc[curr_pivot_pos]
                    > hist_line.iloc[prev_pivot_pos]
                )

                both_red = (
                    hist_line.iloc[curr_pivot_pos] < 0
                    and hist_line.iloc[prev_pivot_pos] < 0
                )

                color_changed = False

                start = prev_pivot_pos + 1
                end = curr_pivot_pos

                for j in range(start, end):
                    if hist_line.iloc[j] > 0:
                        color_changed = True
                        break

                if (
                    price_lower_low
                    and rsi_higher
                    and macd_higher
                    and hist_higher
                    and both_red
                    and color_changed
                ):
                    return "BUY", float(close.iloc[-1])

    return None, None
