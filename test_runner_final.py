#!/usr/bin/env python3
from pathlib import Path
from pynecore.core.script_runner import ScriptRunner
from pynecore.core.ohlcv import OHLCV
from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
from datetime import time as dt_time
import requests
import pandas as pd
import time

symbol = "ETHUSDT"
now = int(time.time())
from_ts = now - 500 * 60 - 60
url = f"https://apiv2.thetruetrade.io/futures/udf/history?symbol={symbol}&resolution=1&from={from_ts}&to={now}&countback=500"
d = requests.get(url).json()

df = pd.DataFrame({
    'open': pd.to_numeric(d['o']),
    'high': pd.to_numeric(d['h']),
    'low': pd.to_numeric(d['l']),
    'close': pd.to_numeric(d['c']),
})
df.index = pd.to_datetime(d['t'], unit='s')
df = df.dropna()

candles = []
for idx, row in df.iterrows():
    ts = int(idx.timestamp() * 1000)
    candles.append(OHLCV(
        timestamp=ts,
        open=float(row['open']),
        high=float(row['high']),
        low=float(row['low']),
        close=float(row['close']),
        volume=0.0
    ))

syminfo = SymInfo(
    prefix="", description=symbol, ticker=symbol,
    currency="USDT", basecurrency="BTC", period="1",
    type="crypto", volumetype="base", mintick=0.01, pricescale=100,
    minmove=1, pointvalue=1.0, mincontract=0.0,
    opening_hours=[SymInfoInterval(day=0, start=dt_time(0,0), end=dt_time(23,59,59))],
    session_starts=[SymInfoSession(day=0, time=dt_time(0,0))],
    session_ends=[SymInfoSession(day=0, time=dt_time(23,59,59))],
    timezone="UTC"
)

inputs = {
    "pivotMode": "سریع (5/3)",
    "rsiLen": 14,
    "macdFast": 12,
    "macdSlow": 26,
    "macdSig": 9,
    "trendLookback": 20,
    "trendSlopeMinPct": 0.05,
    "minConfirmations": "۳ تعییدیه (حداقل مجاز)",
    "enableHidden": True,
    "fibUse618": True,
    "fibUse786": True,
    "fibTolerancePct": 0.5,
    "fibTrendSearchBars": 100,
    "shadowToBodyRatio": 2.0,
    "maxOppositeShadowPct": 20.0,
    "minCandleATRRatio": 0.3,
    "bigCandleAvgLen": 14,
    "bigCandleMultiplier": 1.5,
}

def candle_iterator():
    for c in candles:
        yield c

strategy_path = Path("strategy.py").resolve()

runner = ScriptRunner(
    strategy_path,
    candle_iterator(),
    syminfo,
    last_bar_index=len(candles) - 1,
    inputs=inputs,
)

last_signal = None
last_entry = None

for candle, plot_data, new_trades in runner.run_iter():
    if isinstance(plot_data, dict):
        if plot_data.get("signal") is not None:
            last_signal = plot_data.get("signal")
            last_entry = plot_data.get("entry")
            print(f"✅ signal={last_signal}, entry={last_entry}")

print(f"📈 آخرین سیگنال: {last_signal}")
print(f"💰 آخرین قیمت ورود: {last_entry}")
