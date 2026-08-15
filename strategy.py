# -*- coding: utf-8 -*-
"""
DTM Signal Engine — ریاضی معادل PyneCore (بدون state)
"""
import pandas as pd
import numpy as np

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

def rma(s, length):
    """RMA (Pine)"""
    out = pd.Series(np.nan, index=s.index)
    vals = s.to_numpy(dtype=float)
    if len(vals) < length:
        return out
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
    """EMA (Pine)"""
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
    out = pd.Series(np.nan, index=high.index, dtype=float)
    n = len(high)
    for i in range(left, n - right):
        x = high.iloc[i]
        if high.iloc[i - left:i].max() < x and high.iloc[i + 1:i + right + 1].max() < x:
            out.iloc[i + right] = x
    return out

def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
    out = pd.Series(np.nan, index=low.index, dtype=float)
    n = len(low)
    for i in range(left, n - right):
        x = low.iloc[i]
        if low.iloc[i - left:i].min() > x and low.iloc[i + 1:i + right + 1].min() > x:
            out.iloc[i + right] = x
    return out

def calculate_signals(df):
    close = df["close"]
    high = df["high"]
    low = df["low"]

    rsi_val = rsi(close)
    macd_line, signal_line, hist_line = macd(close)
    atr_val = atr(high, low, close)

    ph = pivot_high(high)
    pl = pivot_low(low)

    # آخرین کندل تأییدشده
    n = len(df)
    last_confirmed = n - 1 - RIGHT_BARS
    if last_confirmed < 0:
        return None, None

    new_ph = not pd.isna(ph.iloc[last_confirmed])
    new_pl = not pd.isna(pl.iloc[last_confirmed])

    if new_ph:
        # یافتن پیوت قبلی
        ph_prev = ph.loc[:last_confirmed-1].dropna()
        if not ph_prev.empty:
            prev_idx = ph_prev.index[-1]
            if close.iloc[-1] > ph.iloc[last_confirmed] and rsi_val.iloc[-1] < rsi_val.loc[prev_idx]:
                # ساده‌شده: در این مرحله فقط احتمال سیگنال
                pass

    if new_pl:
        pl_prev = pl.loc[:last_confirmed-1].dropna()
        if not pl_prev.empty:
            prev_idx = pl_prev.index[-1]
            if close.iloc[-1] < pl.iloc[last_confirmed] and rsi_val.iloc[-1] > rsi_val.loc[prev_idx]:
                pass

    # این نسخه به‌عنوان placeholder است و بعداً تکمیل می‌شود
    return None, None
