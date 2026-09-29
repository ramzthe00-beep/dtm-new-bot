# ═══════════════════════════════════════════════════════════
# filter_utils.py — محاسبه ADX و RSI و بررسی RSI Divergence
# ═══════════════════════════════════════════════════════════
import pandas as pd
import numpy as np


def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def compute_adx(df, period=14):
    """محاسبه ADX روی dataframe با ستون‌های high, low, close"""
    h, l, c = df['high'], df['low'], df['close']
    pc = c.shift(1)
    tr = pd.concat([(h - l), (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    atr = tr.ewm(span=period, adjust=False).mean()

    up = h.diff()
    dn = -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index)

    atr_s = atr.replace(0, np.nan)
    pdi = 100 * ema(pdm, period) / atr_s
    mdi = 100 * ema(mdm, period) / atr_s
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return dx.ewm(span=period, adjust=False).mean()


def compute_rsi(df, period=14):
    """محاسبه RSI روی dataframe با ستون close"""
    c = df['close']
    delta = c.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    rs = ema(gain, period) / ema(loss, period).replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def check_rsi_divergence(df, signal_direction, lookback=14):
    """
    بررسی واگرایی RSI در 14 کندل اخیر
    برمی‌گرداند: True اگر واگرایی مضر باشد (سیگنال باید رد شود)
    """
    if len(df) < lookback + 2:
        return False

    rsi = compute_rsi(df)
    recent = df.iloc[-lookback:]
    rsi_recent = rsi.iloc[-lookback:]

    price_slope = recent['close'].iloc[-1] - recent['close'].iloc[0]
    rsi_slope = rsi_recent.iloc[-1] - rsi_recent.iloc[0]

    # واگرایی نزولی: قیمت بالا، RSI پایین → برای LONG مضر
    if signal_direction == "LONG":
        return (price_slope > 0) and (rsi_slope < 0)

    # واگرایی صعودی: قیمت پایین، RSI بالا → برای SHORT مضر
    if signal_direction == "SHORT":
        return (price_slope < 0) and (rsi_slope > 0)

    return False