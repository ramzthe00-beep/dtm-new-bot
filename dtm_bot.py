# -*- coding: utf-8 -*-
"""
DTM Bot — PyneCore Strategy (exact, no MTF)
"""
import os
import sys
import json
import time
import hmac
import hashlib
import logging
import threading
import signal
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import pandas as pd
import numpy as np
from flask import Flask

# PyneCore imports
from pynecore import pine_range
from pynecore.lib import (
    bar_index, barmerge, close, color, high, input, location, low, math, na,
    open, plotshape, request, script, shape, size, strategy, syminfo, ta
)
from pynecore.types import Persistent, Series
from pynecore.core.script_runner import ScriptRunner
from pynecore.core.ohlcv import OHLCV
from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession

# ===== Config =====
API_KEY = os.getenv("API_KEY", "pXJ3uOI3y7iPHxIgefQJ30PikXHqbQyVV9Ouj-_K")
API_SECRET = os.getenv("API_SECRET", "4cd23e00385ea761250034b420c86f40c4edb8e27c285c21572dbadf7e927b09")
BASE_URL = os.getenv("BASE_URL", "https://apiv2.thetruetrade.io")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")

SYMBOLS = ["LTCUSDT", "DOGEUSDT", "ETHUSDT"]
TIMEFRAME = "1m"
HISTORY_BARS = 400
LIVE_BUFFER_SIZE = 400

RSI_LEN = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIG = 9
TREND_LOOKBACK = 20
TREND_SLOPE_MIN_PCT = 0.05
MIN_CONFIRMATIONS = "۳ تعییدیه (حداقل مجاز)"
ENABLE_HIDDEN = True
FIB_USE_618 = True
FIB_USE_786 = True
FIB_TOLERANCE_PCT = 0.5
FIB_TREND_SEARCH_BARS = 100
SHADOW_TO_BODY_RATIO = 2.0
MAX_OPPOSITE_SHADOW_PCT = 20.0
MIN_CANDLE_ATR_RATIO = 0.3
BIG_CANDLE_AVG_LEN = 14
BIG_CANDLE_MULTIPLIER = 1.5
ENABLE_MTF = False
MTF_TIMEFRAME = "240"

LEFT_BARS = 5
RIGHT_BARS = 3

TICK_SIZES = {"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01}
PRICE_PRECISION = {"LTCUSDT": 2, "DOGEUSDT": 5, "ETHUSDT": 2}
LEVERAGE_MAP = {"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50}

def _ignore_sigterm(signum, frame):
    print(f"Ignoring SIGTERM ({signum}), keeping process alive...", flush=True)

signal.signal(signal.SIGTERM, _ignore_sigterm)
signal.signal(signal.SIGINT, _ignore_sigterm)

logger = logging.getLogger("DTM")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=15)
        return r.ok
    except Exception as e:
        logger.error(f"[TG] {e}")
        return False

def format_iran_time():
    return (datetime.now(timezone.utc) + timedelta(hours=3, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# DTM ADDITIVE SIGNAL REPORTING
# Existing Telegram messages are intentionally untouched.
# These helpers never call create_order() and never run strategy
# calculations. They consume one immutable PyneCore snapshot.
# ============================================================

_SIGNAL_REPORT_SENT = set()
_SIGNAL_REPORT_LOCK = threading.Lock()


def _report_clean(value):
    """Safe representation for Telegram plain-text mode."""
    if value is None:
        return "N/A"
    try:
        if isinstance(value, (float, np.floating)):
            if not np.isfinite(float(value)):
                return "N/A"
            return f"{float(value):.12g}"
        if isinstance(value, (int, np.integer)):
            return str(int(value))
        if isinstance(value, (bool, np.bool_)):
            return "TRUE" if bool(value) else "FALSE"
    except Exception:
        pass

    text = str(value)
    if text.lower() in ("nan", "none", "nat"):
        return "N/A"

    # New messages deliberately use Telegram plain text:
    # no Markdown/HTML entity parsing can fail.
    return text


def _report_bool(value):
    if value is None:
        return "N/A"
    try:
        return "TRUE" if bool(value) else "FALSE"
    except Exception:
        return "N/A"


def _report_value(snapshot, key):
    return _report_clean(snapshot.get(key))


def _signal_report_key(symbol, timeframe, signal, candle_ts):
    return (
        str(symbol).upper(),
        str(timeframe),
        str(signal).upper(),
        int(candle_ts) if candle_ts is not None else None,
    )


def _build_trade_signal_message(symbol, timeframe, snapshot, bar):
    signal = _report_value(snapshot, "signal")
    entry = _report_value(snapshot, "entry")

    return "\n".join([
        "🚨 DTM TRADE SIGNAL",
        "━━━━━━━━━━━━━━━━━━",
        f"{'🟢 LONG' if signal == 'LONG' else '🔴 SHORT'}",
        f"💎 SYMBOL: {_report_clean(symbol)}",
        f"⏱ TIMEFRAME: {_report_clean(timeframe)}",
        f"🕐 SIGNAL TIME: {_report_clean(format_iran_time())}",
        "━━━━━━━━━━━━━━━━━━",
        "💰 TRADE PLAN",
        "━━━━━━━━━━━━━━━━━━",
        f"📍 ENTRY: {entry}",
        "🛑 STOP LOSS: N/A",
        "🎯 TP1: N/A",
        "🎯 TP2: N/A",
        "🎯 TP3: N/A",
        "⚖️ RISK / REWARD: N/A",
        "⚠️ RISK: N/A",
        "━━━━━━━━━━━━━━━━━━",
        "⭐ SIGNAL QUALITY",
        "━━━━━━━━━━━━━━━━━━",
        f"⭐ SCORE: N/A",
        f"📈 TREND: {'BULLISH' if bool(snapshot.get('trend_bullish_ok')) else 'BEARISH' if bool(snapshot.get('trend_bearish_ok')) else 'N/A'}",
        f"🔥 MOMENTUM: N/A",
        "━━━━━━━━━━━━━━━━━━",
        f"🧠 FINAL SIGNAL: {signal}",
    ])


def _build_calculation_report(symbol, timeframe, snapshot, bar):
    signal = _report_value(snapshot, "signal")
    ts = getattr(bar, "timestamp", None)

    def v(k):
        return _report_value(snapshot, k)

    def b(k):
        return _report_bool(snapshot.get(k))

    open_v = getattr(bar, "open", None)
    high_v = getattr(bar, "high", None)
    low_v = getattr(bar, "low", None)
    close_v = getattr(bar, "close", None)
    volume_v = getattr(bar, "volume", None)

    bullish_base = bool(snapshot.get("classic_bullish_base")) or bool(snapshot.get("hidden_bullish_base"))
    bearish_base = bool(snapshot.get("classic_bearish_base")) or bool(snapshot.get("hidden_bearish_base"))

    lines = [
        "🔬 DTM SIGNAL CALCULATION REPORT",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📌 SIGNAL IDENTITY",
        f"Symbol: {_report_clean(symbol)}",
        f"Timeframe: {_report_clean(timeframe)}",
        f"Signal: {signal}",
        f"Signal timestamp: {_report_clean(ts)}",
        f"Candle timestamp: {_report_clean(ts)}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🕯 RAW CANDLE DATA",
        f"Open: {_report_clean(open_v)}",
        f"High: {_report_clean(high_v)}",
        f"Low: {_report_clean(low_v)}",
        f"Close: {_report_clean(close_v)}",
        f"Volume: {_report_clean(volume_v)}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📊 INDICATOR CALCULATIONS",
        f"RSI: {v('rsi')}",
        f"RSI Length: {v('rsi_len')}",
        f"RSI condition: N/A",
        f"MACD Fast: {v('macd_fast')}",
        f"MACD Slow: {v('macd_slow')}",
        f"MACD Signal: {v('macd_signal_len')}",
        f"MACD Line: {v('macd_line')}",
        f"MACD Signal Line: {v('macd_signal_line')}",
        f"MACD Histogram: {v('macd_histogram')}",
        f"MACD condition: N/A",
        f"ATR: {v('atr')}",
        f"ATR Length: {v('atr_len')}",
        f"ATR Value: {v('atr')}",
        "Momentum: N/A",
        "Momentum Percent: N/A",
        "Momentum condition: N/A",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📈 TREND CALCULATION",
        f"Trend Lookback: {v('trend_lookback')}",
        "Trend Slope: N/A",
        "Trend Slope %: N/A",
        f"Minimum Trend Slope: {v('trend_slope_min_pct')}",
        f"Trend Direction: {'UP' if bool(snapshot.get('trend_bearish_ok')) else 'DOWN' if bool(snapshot.get('trend_bullish_ok')) else 'N/A'}",
        "Price vs Trend: N/A",
        f"Trend Condition: {'TRUE' if bullish_base and signal == 'LONG' else 'TRUE' if bearish_base and signal == 'SHORT' else 'N/A'}",
        f"Trend Filter Result: {'TRUE' if (snapshot.get('trend_bullish_ok') if signal == 'LONG' else snapshot.get('trend_bearish_ok')) else 'FALSE'}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🔄 PIVOT CALCULATION",
        f"Left Bars: {v('left_bars')}",
        f"Right Bars: {v('right_bars')}",
        f"Pivot High: {v('pivot_high')}",
        f"Pivot High Price: {v('pivot_high_price')}",
        f"Pivot High Index: {v('pivot_high_index')}",
        f"Pivot Low: {v('pivot_low')}",
        f"Pivot Low Price: {v('pivot_low_price')}",
        f"Pivot Low Index: {v('pivot_low_index')}",
        "Pivot Search Range: N/A",
        "Bars Between Pivots: N/A",
        "Pivot Validity: N/A",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🔀 DIVERGENCE CALCULATION",
        f"RSI Divergence: {'TRUE' if (snapshot.get('classic_bullish_rsi') or snapshot.get('classic_bearish_rsi') or snapshot.get('hidden_bullish_rsi') or snapshot.get('hidden_bearish_rsi')) else 'FALSE'}",
        f"MACD Divergence: {'TRUE' if (snapshot.get('classic_bullish_macd') or snapshot.get('classic_bearish_macd') or snapshot.get('hidden_bullish_macd') or snapshot.get('hidden_bearish_macd')) else 'FALSE'}",
        f"Classic Bullish: {b('classic_bullish_base')}",
        f"Classic Bearish: {b('classic_bearish_base')}",
        f"Hidden Bullish: {b('hidden_bullish_base')}",
        f"Hidden Bearish: {b('hidden_bearish_base')}",
        f"Previous Pivot High: {v('previous_pivot_high_price')}",
        f"Current Pivot High: {v('pivot_high_price')}",
        f"Previous Pivot Low: {v('previous_pivot_low_price')}",
        f"Current Pivot Low: {v('pivot_low_price')}",
        "Previous Indicator Value: N/A",
        "Current Indicator Value: N/A",
        "Price Relationship: N/A",
        "Indicator Relationship: N/A",
        f"Divergence Result: {'TRUE' if bullish_base or bearish_base else 'FALSE'}",
        f"Final Divergence Type: {'CLASSIC BULLISH' if snapshot.get('classic_bullish_base') else 'HIDDEN BULLISH' if snapshot.get('hidden_bullish_base') else 'CLASSIC BEARISH' if snapshot.get('classic_bearish_base') else 'HIDDEN BEARISH' if snapshot.get('hidden_bearish_base') else 'NONE'}",
        f"Divergence Confirmed: {'TRUE' if bullish_base or bearish_base else 'FALSE'}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📐 FIBONACCI CALCULATION",
        f"Fib 0.618 Enabled: {b('fib_use_618')}",
        f"Fib 0.786 Enabled: {b('fib_use_786')}",
        "Swing High: N/A",
        "Swing Low: N/A",
        "Range: N/A",
        "0.618 Level: N/A",
        "0.786 Level: N/A",
        "Distance to 0.618: N/A",
        "Distance to 0.786: N/A",
        f"Tolerance: {v('fib_tolerance_pct')}",
        f"Tolerance %: {v('fib_tolerance_pct')}",
        f"0.618 Valid: N/A",
        f"0.786 Valid: N/A",
        f"Bullish Fib Score: {b('fib_bullish')}",
        f"Bearish Fib Score: {b('fib_bearish')}",
        f"Final Fibonacci Result: {'TRUE' if (snapshot.get('fib_bullish') if signal == 'LONG' else snapshot.get('fib_bearish')) else 'FALSE'}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🕯 PRICE ACTION / CANDLE ANALYSIS",
        f"Candle Body: {v('candle_body')}",
        f"Upper Shadow: {v('upper_shadow')}",
        f"Lower Shadow: {v('lower_shadow')}",
        "Body Percentage: N/A",
        "Shadow/Body Ratio: N/A",
        f"Bullish Candle: {b('price_action_bullish')}",
        f"Bearish Candle: {b('price_action_bearish')}",
        f"Pin Bar: {b('bullish_wick')}",
        "Hammer: N/A",
        "Shooting Star: N/A",
        "Marubozu: N/A",
        "Other Pattern: N/A",
        f"Minimum Candle ATR Ratio: {v('size_ok')}",
        f"Big Candle Average: {v('avg_body')}",
        "Big Candle Multiplier: N/A",
        f"Big Candle Result: {'TRUE' if snapshot.get('big_green_candle') or snapshot.get('big_red_candle') else 'FALSE'}",
        f"Price Action Confirmation: {'TRUE' if snapshot.get('price_action_bullish') or snapshot.get('price_action_bearish') else 'FALSE'}",
        "Price Action Score: N/A",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📊 VOLUME ANALYSIS",
        f"Current Volume: {_report_clean(volume_v)}",
        "Average Volume: N/A",
        "Volume Ratio: N/A",
        "Volume Threshold: N/A",
        "Volume Bullish: N/A",
        "Volume Bearish: N/A",
        "Volume Confirmation: N/A",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🌐 MTF FILTER",
    ]

    if not snapshot.get("mtf_enabled"):
        lines += ["MTF: NOT USED"]
    else:
        lines += [
            f"Higher Timeframe: {v('mtf_timeframe')}",
            "HTF Signal: N/A",
            "HTF Trend: N/A",
            "HTF RSI: N/A",
            "HTF MACD: N/A",
            "HTF Divergence: N/A",
            f"MTF Filter Result: {'TRUE' if (snapshot.get('mtf_bullish_ok') if signal == 'LONG' else snapshot.get('mtf_bearish_ok')) else 'FALSE'}",
        ]

    lines += [
        "━━━━━━━━━━━━━━━━━━━━━━",
        "⭐ CONFIRMATION / SCORE TRACE",
        f"Classic Bullish Base: {b('classic_bullish_base')}",
        f"Classic Bearish Base: {b('classic_bearish_base')}",
        f"Hidden Bullish Base: {b('hidden_bullish_base')}",
        f"Hidden Bearish Base: {b('hidden_bearish_base')}",
        "RSI Confirmation: N/A",
        "MACD Confirmation: N/A",
        f"Trend Confirmation: {'TRUE' if (snapshot.get('trend_bullish_ok') if signal == 'LONG' else snapshot.get('trend_bearish_ok')) else 'FALSE'}",
        f"Fibonacci Confirmation: {'TRUE' if (snapshot.get('fib_bullish') if signal == 'LONG' else snapshot.get('fib_bearish')) else 'FALSE'}",
        f"Price Action Confirmation: {'TRUE' if (snapshot.get('price_action_bullish') if signal == 'LONG' else snapshot.get('price_action_bearish')) else 'FALSE'}",
        "Volume Confirmation: N/A",
        "Pivot Confirmation: N/A",
        f"Divergence Confirmation: {'TRUE' if bullish_base or bearish_base else 'FALSE'}",
        f"MTF Confirmation: {'TRUE' if not snapshot.get('mtf_enabled') else 'N/A'}",
        "Bullish Score: N/A",
        "Bearish Score: N/A",
        f"Minimum Requirement: {v('min_confirmations')}",
        f"Minimum Requirement Result: {'TRUE' if (snapshot.get('minimum_requirement_bullish') if signal == 'LONG' else snapshot.get('minimum_requirement_bearish')) else 'FALSE'}",
        f"Final Bullish: {b('final_classic_bullish') if not snapshot.get('final_hidden_bullish') else 'TRUE'}",
        f"Final Bearish: {b('final_classic_bearish') if not snapshot.get('final_hidden_bearish') else 'TRUE'}",
        "Final Score: N/A",
        f"Final Signal: {signal}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "🧠 EXACT DECISION TRACE",
        f"Trend Condition = {'TRUE' if (snapshot.get('trend_bullish_ok') if signal == 'LONG' else snapshot.get('trend_bearish_ok')) else 'FALSE'}",
        "RSI Condition = N/A",
        "MACD Condition = N/A",
        f"Divergence Condition = {'TRUE' if bullish_base or bearish_base else 'FALSE'}",
        f"Fibonacci Condition = {'TRUE' if (snapshot.get('fib_bullish') if signal == 'LONG' else snapshot.get('fib_bearish')) else 'FALSE'}",
        f"Price Action Condition = {'TRUE' if (snapshot.get('price_action_bullish') if signal == 'LONG' else snapshot.get('price_action_bearish')) else 'FALSE'}",
        "Volume Condition = N/A",
        f"MTF Condition = {'TRUE' if not snapshot.get('mtf_enabled') else 'N/A'}",
        f"Minimum Requirement = {'TRUE' if (snapshot.get('minimum_requirement_bullish') if signal == 'LONG' else snapshot.get('minimum_requirement_bearish')) else 'FALSE'}",
        f"Final Bullish = {b('final_classic_bullish') or b('final_hidden_bullish')}",
        f"Final Bearish = {b('final_classic_bearish') or b('final_hidden_bearish')}",
        f"FINAL SIGNAL = {signal}",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "📋 FINAL SNAPSHOT",
        f"Signal: {signal}",
        f"Entry: {v('entry')}",
        "Stop Loss: N/A",
        "TP1: N/A",
        "TP2: N/A",
        "TP3: N/A",
        "Score: N/A",
        "Risk: N/A",
        "Risk/Reward: N/A",
        f"Trend: {'TRUE' if (snapshot.get('trend_bullish_ok') if signal == 'LONG' else snapshot.get('trend_bearish_ok')) else 'FALSE'}",
        "RSI: N/A",
        "MACD: N/A",
        f"Divergence: {'TRUE' if bullish_base or bearish_base else 'FALSE'}",
        f"Fibonacci: {'TRUE' if (snapshot.get('fib_bullish') if signal == 'LONG' else snapshot.get('fib_bearish')) else 'FALSE'}",
        "Pivot: N/A",
        f"Price Action: {'TRUE' if (snapshot.get('price_action_bullish') if signal == 'LONG' else snapshot.get('price_action_bearish')) else 'FALSE'}",
        "Volume: N/A",
        f"MTF: {'NOT USED' if not snapshot.get('mtf_enabled') else 'N/A'}",
        f"FINAL DECISION: {signal}",
    ]
    return "\n".join(lines)


def send_dtm_signal_reports(symbol, timeframe, snapshot, bar):
    """Send the two additive reports exactly once per signal identity."""
    signal_value = snapshot.get("signal")
    if signal_value not in ("LONG", "SHORT"):
        return False

    candle_ts = getattr(bar, "timestamp", None)
    key = _signal_report_key(symbol, timeframe, signal_value, candle_ts)

    with _SIGNAL_REPORT_LOCK:
        if key in _SIGNAL_REPORT_SENT:
            return False
        _SIGNAL_REPORT_SENT.add(key)

    try:
        # Both messages are built from THIS SAME snapshot.
        msg1 = _build_trade_signal_message(symbol, timeframe, snapshot, bar)
        msg2 = _build_calculation_report(symbol, timeframe, snapshot, bar)

        # Plain text only: no Telegram entity parsing.
        ok1 = send_telegram_message(msg1)
        ok2 = send_telegram_message(msg2)

        if not (ok1 and ok2):
            logger.error(
                "[DTM REPORT] Telegram report failed | "
                "symbol=%s signal=%s candle=%s",
                symbol, signal_value, candle_ts
            )
        return bool(ok1 and ok2)

    except Exception:
        logger.exception("[DTM REPORT] unexpected reporting failure")
        return False

# ===== Exchange =====
class TrueTradePublicData:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()

    def fetch_ohlcv(self, symbol, timeframe="1m", limit=HISTORY_BARS):
        res = {"1m":"1","5m":"5","15m":"15","30m":"30","1h":"60","4h":"240","1d":"1D"}
        resolution = res.get(timeframe, "1")
        seconds_per_bar = {"1":60,"5":300,"15":900,"30":1800,"60":3600,"240":14400,"1D":86400}.get(resolution, 60)
        now = int(time.time())
        from_ts = now - (limit * seconds_per_bar) - seconds_per_bar
        uri = f"/futures/udf/history?symbol={symbol.upper()}&resolution={resolution}&from={from_ts}&to={now}&countback={limit}"
        try:
            r = self.session.get(f"{self.base_url}{uri}", timeout=20)
            if not r.ok:
                return pd.DataFrame()
            data = r.json()
            if not isinstance(data, dict) or str(data.get("s","")).lower() != "ok":
                return pd.DataFrame()
            t = data.get("t", [])
            o = data.get("o", [])
            h = data.get("h", [])
            l = data.get("l", [])
            c = data.get("c", [])
            v = data.get("v", [])
            n = min(len(t), len(o), len(h), len(l), len(c))
            if n < 50:
                return pd.DataFrame()
            df = pd.DataFrame({"time": t[:n], "open": o[:n], "high": h[:n], "low": l[:n], "close": c[:n], "volume": v[:n] if len(v)>=n else [0]*n})
            df["time"] = pd.to_datetime(pd.to_numeric(df["time"]), unit="s", utc=True)
            for col in ["open","high","low","close","volume"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            df = df.dropna().drop_duplicates("time").sort_values("time").set_index("time")
            return df.tail(limit)
        except Exception as e:
            logger.error(f"[PUB] {e}")
            return pd.DataFrame()

class TrueTradePrivateExchange:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.connected = False
        self._last_response = None

    def _sign(self, method, uri, ts):
        payload = f"{ts}{method.upper()}{uri}"
        return hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

    def _request(self, method, uri, data=None):
        ts = str(int(time.time()*1000))
        sig = self._sign(method, uri, ts)

        headers = {
            "X-API-Key": self.api_key,
            "X-Timestamp": ts,
            "X-Signature": sig,
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}{uri}"

        # ===== FULL EXCHANGE REQUEST LOG =====
        logger.info(
            "[EXCHANGE REQUEST] %s %s | DATA=%s",
            method.upper(),
            url,
            json.dumps(data, ensure_ascii=False) if data else None
        )

        try:
            r = self.session.request(
                method,
                url,
                headers=headers,
                json=data,
                timeout=15
            )

            self._last_response = r

            # ===== FULL EXCHANGE RESPONSE LOG =====
            logger.info(
                "[EXCHANGE RESPONSE] %s %s | HTTP=%s | BODY=%s",
                method.upper(),
                uri,
                r.status_code,
                r.text
            )

            if not r.ok:
                self.connected = False

                logger.error(
                    "[EXCHANGE ERROR] %s %s | HTTP=%s | BODY=%s",
                    method.upper(),
                    uri,
                    r.status_code,
                    r.text
                )

                r.raise_for_status()

            self.connected = True

            try:
                return r.json()
            except ValueError:
                return {"raw": r.text}

        except Exception as e:
            logger.error(
                "[EXCHANGE REQUEST EXCEPTION] %s %s | ERROR=%s",
                method.upper(),
                uri,
                repr(e)
            )
            raise

    def test_connection(self):
        try:
            self._request("GET", "/futures/positions")
            return True
        except Exception:
            return False

    def fetch_balance(self):
        try:
            data = self._request("GET", "/futures/assets")
            assets = data.get("assets", []) if isinstance(data, dict) else data
            if isinstance(assets, dict):
                assets = [assets]
            for a in assets or []:
                if str(a.get("symbol","")).upper() == "USDT":
                    return float(a.get("availableBalance", a.get("totalAssets", a.get("available",0))) or 0)
            return 0.0
        except Exception:
            return None

    def fetch_open_positions(self):
        try:
            d = self._request("GET", "/futures/positions?active=true")
            return d if isinstance(d, list) else (d.get("positions", []) if isinstance(d, dict) else [])
        except Exception:
            return []

    def _round_price(self, price, symbol):
        tick = TICK_SIZES.get(symbol.upper(), 0.01)
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        return round(round(float(price)/tick)*tick, prec)

    def create_order(self, symbol, side, capital, params=None):
        params = params or {}
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        
        # تبدیل side به فرمت مورد نیاز API
        side_upper = str(side).upper().strip()
        
        # لاگ مقدار ورودی برای دیباگ
        logger.info(f"[CREATE ORDER] Symbol: {symbol}, Input side: '{side}', Capital: {capital}")
        
        if side_upper in ("BUY", "LONG"):
            api_side = "LONG"
        elif side_upper in ("SELL", "SHORT"):
            api_side = "SHORT"
        else:
            api_side = side_upper
            
        logger.info(f"[CREATE ORDER] API side: '{api_side}'")
        
        # استفاده از اهرم مناسب برای هر نماد
        leverage = params.get("leverage", LEVERAGE_MAP.get(symbol.upper(), 1))
        
        # ساختار صحیح بر اساس کتابچه
        od = {
            "symbol": str(symbol).upper(),
            "side": api_side,
            "tradeType": "MARKET",
            "leverage": int(leverage),
            "cost": f"{float(capital):.{prec}f}",
            "walletType": "debit"
        }
        
        # لاگ کامل بدنه درخواست
        logger.info(f"[CREATE ORDER] Request body: {json.dumps(od, ensure_ascii=False, indent=2)}")
        
        # افزودن حد ضرر و حد سود اگر موجود باشند
        if "stopLoss" in params and params["stopLoss"]:
            od["stopLoss"] = f"{self._round_price(params['stopLoss'], symbol):.{prec}f}"
        if "takeProfit" in params and params["takeProfit"]:
            od["takeProfit"] = f"{self._round_price(params['takeProfit'], symbol):.{prec}f}"
            
        # ارسال اطلاعات کامل درخواست به تلگرام
        request_info = (
            f"📤 ثبت سفارش — {symbol} {api_side}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🔹 Side: {api_side}\n"
            f"🔹 Trade Type: MARKET\n"
            f"🔹 Leverage: {od['leverage']}\n"
            f"🔹 Cost: {od['cost']} USDT\n"
            f"🔹 Wallet Type: {od['walletType']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📋 Body: {json.dumps(od, ensure_ascii=False)}"
        )
        send_telegram_message(request_info)
        
        try:
            # امضای صحیح: timestamp + METHOD + URI (بدون body)
            result = self._request("POST", "/futures/positions", od)
            
            # پاسخ موفقیت‌آمیز شامل positionId است
            position_id = result.get("positionId") if isinstance(result, dict) else None
            
            success_msg = (
                f"📥 سفارش ثبت شد — {symbol} {api_side}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"✅ Position ID: {position_id}"
            )
            send_telegram_message(success_msg)
            return {"id": position_id}
            
        except Exception as e:
            # نمایش خطای دقیق از پاسخ API
            error_text = ""
            if self._last_response is not None:
                try:
                    error_data = self._last_response.json()
                    if "errors" in error_data:
                        error_messages = []
                        for error in error_data["errors"]:
                            field = error.get("field", "unknown")
                            message = error.get("message", "unknown error")
                            error_messages.append(f"• {field}: {message}")
                        error_text = "\n".join(error_messages)
                    else:
                        error_text = f"HTTP {self._last_response.status_code}: {self._last_response.text[:500]}"
                except ValueError:
                    error_text = f"HTTP {self._last_response.status_code}: {self._last_response.text[:500]}"
            else:
                error_text = str(e)
            
            # ارسال خطای کامل به تلگرام
            error_msg = (
                f"❌ خطای سفارش {symbol} {api_side}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"📋 Body ارسالی:\n{json.dumps(od, ensure_ascii=False, indent=2)}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🔴 خطا:\n{error_text}"
            )
            send_telegram_message(error_msg)
            raise

# ===== Main loop =====
app = Flask(__name__)

@app.route("/")
def health():
    return "OK", 200

@app.route("/health")
def health_check():
    return "OK", 200

def run_trading_loop():
    """
    STAGE 2 — TRUE LIVE PYNECORE STREAM

    Architecture:
        initial API fetch -> rolling warmup buffer
        -> one persistent ScriptRunner per symbol
        -> one persistent run_iter() per symbol
        -> only newly CLOSED candles are appended
        -> oldest candles are discarded from the rolling buffer

    IMPORTANT:
        - No calculate_signals()
        - No new ScriptRunner on every polling cycle
        - No replay of the complete history every minute
        - MTF remains disabled
    """
    import queue

    exchange = TrueTradePrivateExchange()
    public = TrueTradePublicData()

    logger.info("DTM BOT START — STAGE 2 TRUE LIVE PYNECORE")

    class LiveSymbolState:
        def __init__(self, symbol):
            self.symbol = symbol
            self.buffer = []
            self.seen_timestamps = set()
            self.feed_queue = queue.Queue()
            self.runner = None
            self.runner_thread = None
            self.started = False
            self.last_closed_ts = None
            self.last_signal = None
            self.last_entry = None

        def add_closed_candle(self, row):
            ts = int(row.Index.timestamp() * 1000)

            if self.last_closed_ts is not None and ts <= self.last_closed_ts:
                return False

            if ts in self.seen_timestamps:
                return False

            candle = OHLCV(
                timestamp=ts,
                open=float(row.open),
                high=float(row.high),
                low=float(row.low),
                close=float(row.close),
                volume=float(row.volume),
            )

            self.buffer.append(candle)

            if len(self.buffer) > LIVE_BUFFER_SIZE:
                self.buffer.pop(0)

            self.seen_timestamps.add(ts)

            # Keep the timestamp set bounded exactly like the rolling buffer.
            if len(self.seen_timestamps) > LIVE_BUFFER_SIZE:
                self.seen_timestamps = {
                    x.timestamp
                    for x in self.buffer
                }

            self.last_closed_ts = ts
            return True

        def iterator(self):
            """
            Persistent OHLCV iterator.

            First yields the warmup buffer.
            Afterwards blocks waiting for exactly one new CLOSED candle.
            """
            for candle in self.buffer:
                yield candle

            while True:
                candle = self.feed_queue.get()
                if candle is None:
                    return
                yield candle

        def start(self):
            if self.started:
                return

            if len(self.buffer) < 50:
                raise RuntimeError(
                    f"{self.symbol}: insufficient warmup buffer: "
                    f"{len(self.buffer)}"
                )

            _basecurrency = self.symbol.replace("USDT", "")

            _opening_hours = [
                SymInfoInterval(
                    day=0,
                    start=time(0, 0),
                    end=time(23, 59, 59),
                )
            ]

            _session_starts = [
                SymInfoSession(
                    day=0,
                    time=time(0, 0),
                )
            ]

            _session_ends = [
                SymInfoSession(
                    day=0,
                    time=time(23, 59, 59),
                )
            ]

            _mintick = float(TICK_SIZES.get(self.symbol, 0.01))
            _pricescale = max(1, int(round(1.0 / _mintick)))

            syminfo = SymInfo(
                prefix="",
                description=self.symbol,
                ticker=self.symbol,
                currency="USDT",
                basecurrency=_basecurrency,
                period="15",
                type="crypto",
                volumetype="base",
                mintick=_mintick,
                pricescale=_pricescale,
                minmove=1,
                pointvalue=1.0,
                mincontract=0.0,
                opening_hours=_opening_hours,
                session_starts=_session_starts,
                session_ends=_session_ends,
                timezone="UTC",
            )

            strategy_path = (
                Path(__file__).resolve().parent / "strategy.py"
            )

            # The SAME ScriptRunner instance lives for the whole process.
            # Its run_iter() consumes the warmup and then waits for
            # subsequent live candles from feed_queue.
            self.runner = ScriptRunner(
                strategy_path,
                self.iterator(),
                syminfo,
                last_bar_index=len(self.buffer) - 1,
            )

            self.started = True

            def _runner_worker():
                try:
                    logger.info(
                        f"{self.symbol}: "
                        f"PyneCore ScriptRunner LIVE START | "
                        f"warmup={len(self.buffer)}"
                    )

                    for result in self.runner.run_iter():
                        if not result or len(result) < 2:
                            continue

                        bar = result[0]
                        values = result[1]

                        sig = None
                        entry = None
                        signal_snapshot = dict(values) if isinstance(values, dict) else {}

                        if isinstance(values, dict):
                            for key, value in values.items():
                                key_l = str(key).lower()

                                if key_l in ("signal", "sig"):
                                    sig = value

                                elif key_l in (
                                    "entry",
                                    "entry_price",
                                ):
                                    entry = value

                        # Preserve the exact PyneCore result in one snapshot.
                        # Reporting does not recalculate strategy values.
                        if sig is not None:
                            signal_snapshot["signal"] = sig
                            self.last_signal = sig

                        if entry is not None:
                            signal_snapshot["entry"] = entry
                            self.last_entry = entry

                        logger.info(
                            f"{self.symbol}: "
                            f"PYNECORE LIVE BAR | "
                            f"ts={getattr(bar, 'timestamp', None)} | "
                            f"signal={sig} | "
                            f"entry={entry}"
                        )

                        # ADDITIVE ONLY:
                        # This sends the two new reporting messages.
                        # It does NOT call create_order(), does NOT alter
                        # strategy state, and does NOT alter existing messages.
                        if sig in ("LONG", "SHORT"):
                            send_dtm_signal_reports(
                                self.symbol,
                                TIMEFRAME,
                                signal_snapshot,
                                bar,
                            )

                except Exception as exc:
                    logger.exception(
                        f"{self.symbol}: "
                        f"PyneCore live runner stopped: {exc}"
                    )

            self.runner_thread = threading.Thread(
                target=_runner_worker,
                name=f"pynecore-live-{self.symbol}",
                daemon=True,
            )

            self.runner_thread.start()

    states = {
        symbol: LiveSymbolState(symbol)
        for symbol in SYMBOLS
    }

    # ------------------------------------------------------------
    # INITIAL WARMUP
    # ------------------------------------------------------------
    for symbol, state in states.items():
        try:
            df = public.fetch_ohlcv(
                symbol,
                TIMEFRAME,
                LIVE_BUFFER_SIZE,
            )

            if df.empty:
                logger.warning(
                    f"{symbol}: empty initial OHLCV"
                )
                continue

            # The current 1m candle is not closed until the next
            # minute begins. Never feed the open candle to Pine.
            now_ts = int(time.time())
            current_bucket = (
                now_ts // 60
            ) * 60

            closed_df = df[
                df.index.astype("int64") // 10**9
                < current_bucket
            ]

            if len(closed_df) > LIVE_BUFFER_SIZE:
                closed_df = closed_df.tail(LIVE_BUFFER_SIZE)

            for row in closed_df.itertuples():
                state.add_closed_candle(row)

            if len(state.buffer) < 50:
                logger.warning(
                    f"{symbol}: insufficient closed-candle warmup: "
                    f"{len(state.buffer)}"
                )
                continue

            state.start()

            logger.info(
                f"{symbol}: LIVE WARMUP COMPLETE | "
                f"closed_candles={len(state.buffer)} | "
                f"last_closed="
                f"{state.last_closed_ts}"
            )

        except Exception as exc:
            logger.exception(
                f"{symbol}: initial live setup failed: {exc}"
            )

    # ------------------------------------------------------------
    # LIVE POLLING
    # ------------------------------------------------------------
    while True:
        try:
            conn = exchange.test_connection()
            balance = (
                exchange.fetch_balance()
                if conn
                else 0
            )

            now_ts = int(time.time())
            current_bucket = (
                now_ts // 60
            ) * 60

            for symbol, state in states.items():
                if not state.started:
                    continue

                try:
                    # Fetch only a small live tail.
                    # This is NOT replayed through ScriptRunner.
                    df = public.fetch_ohlcv(
                        symbol,
                        TIMEFRAME,
                        min(10, LIVE_BUFFER_SIZE),
                    )

                    if df.empty:
                        continue

                    for row in df.itertuples():
                        row_ts = int(
                            row.Index.timestamp()
                        )

                        # Only CLOSED candles enter Pine.
                        if row_ts >= current_bucket:
                            continue

                        if state.add_closed_candle(row):
                            candle = state.buffer[-1]

                            # Feed ONLY the new candle to the
                            # already-running ScriptRunner.
                            state.feed_queue.put(candle)

                            logger.info(
                                f"{symbol}: "
                                f"NEW CLOSED CANDLE -> PYNECORE | "
                                f"ts={candle.timestamp} | "
                                f"buffer={len(state.buffer)}"
                            )

                            # Do not execute an order from the
                            # polling path. Signal execution remains
                            # attached to the PyneCore live stream.
                            if (
                                state.last_signal
                                and balance
                                and balance > 0
                            ):
                                logger.info(
                                    f"{symbol}: "
                                    f"PyneCore signal available: "
                                    f"{state.last_signal} | "
                                    f"entry={state.last_entry}"
                                )

                except Exception as exc:
                    logger.exception(
                        f"{symbol}: live update failed: {exc}"
                    )

            time.sleep(5)

        except Exception as exc:
            logger.exception(
                f"[LIVE LOOP] {exc}"
            )
            time.sleep(5)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=run_trading_loop, daemon=True).start()
    logger.info(f"Flask on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)
