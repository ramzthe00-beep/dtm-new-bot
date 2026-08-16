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
            data
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
        # اگر side قبلاً LONG یا SHORT است، همان را استفاده کن
        side_upper = side.upper()
        if side_upper in ("BUY", "LONG"):
            api_side = "LONG"
        elif side_upper in ("SELL", "SHORT"):
            api_side = "SHORT"
        else:
            api_side = side_upper  # اگر قبلاً LONG یا SHORT است
        
        # ساختار صحیح بر اساس کتابچه
        od = {
            "symbol": symbol.upper(),
            "side": api_side,  # LONG یا SHORT
            "tradeType": "MARKET",  # MARKET یا LIMIT
            "leverage": params.get("leverage", 1),
            "cost": f"{capital:.{prec}f}",  # cost به معنی collateral در quote asset
            "walletType": "debit"
        }
        
        # افزودن حد ضرر و حد سود اگر موجود باشند
        if "stopLoss" in params:
            od["stopLoss"] = f"{self._round_price(params['stopLoss'], symbol):.{prec}f}"
        if "takeProfit" in params:
            od["takeProfit"] = f"{self._round_price(params['takeProfit'], symbol):.{prec}f}"
            
        send_telegram_message(f"📤 ثبت سفارش — {symbol} {api_side} | اهرم: {od['leverage']}")
        
        try:
            # امضای صحیح: timestamp + METHOD + URI (بدون body)
            result = self._request("POST", "/futures/positions", od)
            
            # پاسخ موفقیت‌آمیز شامل positionId است
            position_id = result.get("positionId") if isinstance(result, dict) else None
            
            send_telegram_message(f"📥 سفارش ثبت شد — {symbol} {api_side} | Position ID: {position_id}")
            return {"id": position_id}
            
        except Exception as e:
            # نمایش خطای دقیق از پاسخ API
            if self._last_response is not None:
                try:
                    error_data = self._last_response.json()
                    if "errors" in error_data:
                        error_messages = []
                        for error in error_data["errors"]:
                            field = error.get("field", "unknown")
                            message = error.get("message", "unknown error")
                            error_messages.append(f"{field}: {message}")
                        error_text = "\n".join(error_messages)
                    else:
                        error_text = f"HTTP {self._last_response.status_code}: {self._last_response.text[:300]}"
                except ValueError:
                    error_text = f"HTTP {self._last_response.status_code}: {self._last_response.text[:300]}"
            else:
                error_text = str(e)
                
            send_telegram_message(f"❌ خطای سفارش {symbol} {api_side}\n{error_text}")
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

                        if sig is not None:
                            self.last_signal = sig

                        if entry is not None:
                            self.last_entry = entry

                        logger.info(
                            f"{self.symbol}: "
                            f"PYNECORE LIVE BAR | "
                            f"ts={getattr(bar, 'timestamp', None)} | "
                            f"signal={sig} | "
                            f"entry={entry}"
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
