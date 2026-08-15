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
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import pandas as pd
import numpy as np
from flask import Flask
from strategy import calculate_signals

# PyneCore imports
from pynecore import pine_range
from pynecore.lib import (
    bar_index, barmerge, close, color, high, input, location, low, math, na,
    open, plotshape, request, script, shape, size, strategy, syminfo, ta
)
from pynecore.types import Persistent, Series

# ===== Config =====
API_KEY = os.getenv("API_KEY", "pXJ3uOI3y7iPHxIgefQJ30PikXHqbQyVV9Ouj-_K")
API_SECRET = os.getenv("API_SECRET", "4cd23e00385ea761250034b420c86f40c4edb8e27c285c21572dbadf7e927b09")
BASE_URL = os.getenv("BASE_URL", "https://apiv2.thetruetrade.io")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")

SYMBOLS = ["LTCUSDT", "DOGEUSDT", "ETHUSDT"]
TIMEFRAME = "1m"
HISTORY_BARS = 500

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
        headers = {"X-API-Key": self.api_key, "X-Timestamp": ts, "X-Signature": sig, "Content-Type": "application/json"}
        r = self.session.request(method, f"{self.base_url}{uri}", headers=headers, json=data, timeout=15)
        self._last_response = r
        if not r.ok:
            self.connected = False
            r.raise_for_status()
        self.connected = True
        try:
            return r.json()
        except ValueError:
            return {"raw": r.text}

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
        od = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "tradeType": "MARKET",
            "leverage": params.get("leverage", 1),
            "cost": f"{capital:.{prec}f}",
            "walletType": "debit"
        }
        if "stopLoss" in params:
            od["stopLoss"] = f"{self._round_price(params['stopLoss'], symbol):.{prec}f}"
        if "takeProfit" in params:
            od["takeProfit"] = f"{self._round_price(params['takeProfit'], symbol):.{prec}f}"
        send_telegram_message(f"📤 ثبت سفارش — {symbol} {side} | اهرم: {od['leverage']}")
        try:
            result = self._request("POST", "/futures/positions", od)
            send_telegram_message(f"📥 سفارش ثبت شد — {symbol} {side}")
            return {"id": result.get("positionId") if isinstance(result, dict) else None}
        except Exception as e:
            body = self._last_response.text[:300] if self._last_response is not None else str(e)
            send_telegram_message(f"❌ خطای سفارش {symbol} {side}\n{body}")
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
    exchange = TrueTradePrivateExchange()
    public = TrueTradePublicData()
    logger.info("DTM BOT START")
    while True:
        try:
            conn = exchange.test_connection()
            balance = exchange.fetch_balance() if conn else 0
            for symbol in SYMBOLS:
                df = public.fetch_ohlcv(symbol, TIMEFRAME, HISTORY_BARS)
                if df.empty:
                    continue
                sig, entry = calculate_signals(df)
                if sig and balance and balance > 0:
                    allowed = LEVERAGE_MAP.get(symbol, 50)
                    capital = min(balance * 0.98, TARGET_RISK)
                    exchange.create_order(symbol, sig, capital, {"leverage": allowed})
                logger.info(f"{symbol}: signal={sig}, entry={entry}, candles={len(df)}")
            time.sleep(60)
        except Exception as e:
            logger.error(f"[LOOP] {e}")
            time.sleep(60)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    threading.Thread(target=run_trading_loop, daemon=True).start()
    logger.info(f"Flask on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True, use_reloader=False)
