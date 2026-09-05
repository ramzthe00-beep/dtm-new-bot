import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import signal
import time
import hmac
import hashlib
import logging
import requests
import pandas as pd
from strategy_wrapper import calculate_signals
from datetime import datetime, timezone, timedelta
import math
import random
import trade_ledger

# ===== TIMEZONE CONSTANTS =====
IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

def format_iran_time(dt=None):
    if dt is None:
        dt = datetime.now(UTC_TZ)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC_TZ)
    return dt.astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = os.getenv("BASE_URL", "https://apiv2.thetruetrade.io")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")
# ============================================================
# تنظیمات تایم‌فریم‌های چندگانه
# ============================================================
SYMBOLS = ["LTCUSDT", "DOGEUSDT", "ETHUSDT", "BNBUSDT", "PUMPUSDT"]
TIMEFRAMES = ["1" , "5"]
HISTORY_BARS = 500

CHECK_INTERVAL = {
    "1": 60,
    "5": 300,
}

LEVERAGE_MAP = {"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50, "BNBUSDT": 75, "PUMPUSDT": 75}
TARGET_RISK = 2.0
TICK_SIZES = {"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01, "BNBUSDT": 0.01, "PUMPUSDT": 0.000001}


def _precision_from_tick(tick):
    """
    تعداد رقم اعشار را مستقیماً از اندازه‌ی تیک (TICK_SIZES) محاسبه می‌کند،
    تا PRICE_PRECISION هرگز با TICK_SIZES ناهماهنگ نشود.
    علت باگ قبلی «Stop Loss: 0.00 / Take Profit: 0.00» برای ارزهای ۶ رقمی
    (مثل PUMPUSDT) دقیقاً همین بود: تیک آن 0.000001 (۶ رقم اعشار) بود اما
    PRICE_PRECISION آن به‌اشتباه روی 2 هارد-کد شده بود، پس هر قیمتی مثل
    0.0039 هنگام رند شدن به ۲ رقم اعشار می‌شد 0.00 و همان مقدار نامعتبر هم
    در پیام تلگرام نمایش داده می‌شد و هم داخل بدنه‌ی سفارش به صرافی ارسال می‌شد.
    """
    s = f"{tick:.10f}".rstrip("0")
    return len(s.split(".")[1]) if "." in s else 0


PRICE_PRECISION = {sym: _precision_from_tick(tick) for sym, tick in TICK_SIZES.items()}
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BOT")

logger.info("=" * 60)
logger.info("BOT STARTING...")
logger.info("=" * 60)

# ============================================================
# 🛡️ تنظیمات ریسک فری (Risk-Free)
# ============================================================
RISK_FREE_ENABLED = os.getenv("RISK_FREE_ENABLED", "1") == "1"
RISK_FREE_FEE_MODE = os.getenv("RISK_FREE_FEE_MODE", "open")
RISK_FREE_FEE_DEFAULT = float(os.getenv("RISK_FREE_FEE_DEFAULT", "0.30"))
RISK_FREE_PENDING = {}

# 🆕 آیا ریسک‌فری در همه‌ی تایم‌فریم‌هایی که ربات روی آن‌ها معامله می‌کند فعال شود،
# یا فقط روی یک تایم‌فریم مشخص؟
#   RISK_FREE_ALL_TIMEFRAMES=1  → روی همه‌ی TIMEFRAMES (پیش‌فرض، رفتار قبلی)
#   RISK_FREE_ALL_TIMEFRAMES=0  → فقط روی تایم‌فریم RISK_FREE_TIMEFRAME (مثلاً "5")
RISK_FREE_ALL_TIMEFRAMES = os.getenv("RISK_FREE_ALL_TIMEFRAMES", "1") == "1"
RISK_FREE_TIMEFRAME = os.getenv("RISK_FREE_TIMEFRAME", TIMEFRAMES[0] if TIMEFRAMES else "1")

# 🆕 حداقل «cost» (سرمایه/کولترال) قابل قبول برای ثبت سفارش.
# صرافی هر سفارشی با cost کمتر از این مقدار را با خطای
# "Collateral is below the minimum allowed" رد می‌کند. عدد دقیقِ صرافی در
# مستندات ذکر نشده — این فقط یک مقدار پیش‌فرض احتیاطی است؛ آن را طبق حداقل
# واقعی TheTrueTrade تنظیم کنید (متغیر محیطی MIN_ORDER_COST_USDT در Railway).
MIN_ORDER_COST_USDT = float(os.getenv("MIN_ORDER_COST_USDT", "5"))

# ============================================================
# Rate limiter برای درخواست‌های thetruetrade.io
# ============================================================
TRUETRADE_MIN_INTERVAL = float(os.getenv("TRUETRADE_MIN_INTERVAL", "2.5"))
_truetrade_lock = threading.Lock()
_truetrade_last_req = 0.0

def throttle_truetrade():
    global _truetrade_last_req
    with _truetrade_lock:
        now = time.monotonic()
        wait = TRUETRADE_MIN_INTERVAL - (now - _truetrade_last_req)
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _truetrade_last_req = now

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=20)
        if r.status_code == 200:
            return True
        else:
            logger.error(f"[TELEGRAM] Failed to send message: {r.status_code} {r.text[:300]}")
            return False
    except Exception as e:
        logger.error(f"[TELEGRAM] Failed to send message: {e}")
        return False

def send_telegram_long(text):
    text = str(text)
    if len(text) <= 4000:
        return send_telegram(text)
    
    parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
    ok = True
    for i, part in enumerate(parts):
        ok = send_telegram(part) and ok
        time.sleep(0.5)
    return ok

class PublicData:
    BINANCE_BASE_CANDIDATES = [
        "https://data-api.binance.vision",
        "https://api.binance.com",
    ]

    def __init__(self):
        self.base = BASE_URL
        self.session = requests.Session()
        self._binance_base_working = None

    def fetch_ohlcv_binance(self, symbol, timeframe="1"):
        interval_map = {"1": "1m", "5": "5m", "15": "15m"}
        interval = interval_map.get(str(timeframe), f"{timeframe}m")

        multiplier = int(timeframe)
        limit = min(HISTORY_BARS, 1000)
        now_ms = int(time.time() * 1000)
        start_ms = now_ms - limit * multiplier * 60 * 1000

        bases = (
            [self._binance_base_working] if self._binance_base_working
            else self.BINANCE_BASE_CANDIDATES
        )

        last_err = None
        for base in bases:
            try:
                url = (
                    f"{base}/api/v3/klines?symbol={symbol.upper()}"
                    f"&interval={interval}&startTime={start_ms}&endTime={now_ms}&limit={limit}"
                )
                r = self.session.get(url, timeout=15)
                r.raise_for_status()
                rows = r.json()
                if not rows:
                    logger.warning(f"Binance: no candles for {symbol} {timeframe}m")
                    return pd.DataFrame()

                t = [row[0] / 1000.0 for row in rows]
                o = [row[1] for row in rows]
                h = [row[2] for row in rows]
                l = [row[3] for row in rows]
                c = [row[4] for row in rows]
                v = [row[5] for row in rows]

                df = pd.DataFrame({
                    'open': pd.to_numeric(o, errors='coerce'),
                    'high': pd.to_numeric(h, errors='coerce'),
                    'low': pd.to_numeric(l, errors='coerce'),
                    'close': pd.to_numeric(c, errors='coerce'),
                    'volume': pd.to_numeric(v, errors='coerce'),
                }, index=pd.to_datetime(t, unit='s', utc=True))

                df = df.sort_index()
                df = df[~df.index.duplicated(keep='last')]
                df = df.dropna(subset=['open', 'high', 'low', 'close'])

                self._binance_base_working = base
                result = df.tail(HISTORY_BARS)
                logger.info(f"Fetched {len(result)} BINANCE-SPOT candles for {symbol} {timeframe}m via {base}")
                return result

            except Exception as e:
                last_err = e
                logger.warning(f"Binance base {base} failed for {symbol} {timeframe}m: {e}")
                self._binance_base_working = None
                continue

        logger.error(
            f"⚠️ Binance UNREACHABLE for {symbol} {timeframe}m ({last_err}) — "
            f"falling back to thetruetrade.io data for THIS cycle only."
        )
        return self.fetch_ohlcv(symbol, timeframe)

    def fetch_ohlcv(self, symbol, timeframe="1"):
        now = int(time.time())
        multiplier = int(timeframe)
        bars_needed = HISTORY_BARS * multiplier * 2
        from_ts = now - bars_needed * 60 - 60
        uri = f"/futures/udf/history?symbol={symbol.upper()}&resolution={timeframe}&from={from_ts}&to={now}&countback={HISTORY_BARS * multiplier}"

        max_attempts = 2
        for attempt in range(max_attempts):
            throttle_truetrade()
            try:
                r = self.session.get(f"{self.base}{uri}", timeout=20)

                if r.status_code == 429:
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"[thetruetrade 429] {symbol} {timeframe}m — "
                            f"still rate-limited after {max_attempts} attempts"
                        )
                        return pd.DataFrame()

                    wait = min(20, 2 ** attempt) + random.random() * 0.5
                    logger.warning(
                        f"[thetruetrade 429] {symbol} {timeframe}m — "
                        f"attempt {attempt + 1}/{max_attempts}, retry in {wait:.2f}s"
                    )
                    time.sleep(wait)
                    continue

                r.raise_for_status()
                data = r.json()

                if data.get('s') != 'ok':
                    logger.warning(f"Data not ok for {symbol} {timeframe}m: {data.get('s')}")
                    return pd.DataFrame()

                if not data.get('t') or len(data['t']) == 0:
                    logger.warning(f"No data for {symbol} {timeframe}m")
                    return pd.DataFrame()

                t = data['t']
                o = data['o']
                h = data['h']
                l = data['l']
                c = data['c']
                v = data.get('v', [None] * len(t))

                df = pd.DataFrame({
                    'open': pd.to_numeric(o, errors='coerce'),
                    'high': pd.to_numeric(h, errors='coerce'),
                    'low': pd.to_numeric(l, errors='coerce'),
                    'close': pd.to_numeric(c, errors='coerce'),
                    'volume': pd.to_numeric(v, errors='coerce'),
                }, index=pd.to_datetime(t, unit='s', utc=True))

                df = df.sort_index()
                df = df[~df.index.duplicated(keep='last')]
                df = df.dropna(subset=['open', 'high', 'low', 'close'])

                result = df.tail(HISTORY_BARS)
                logger.info(f"Fetched {len(result)} candles for {symbol} {timeframe}m")
                return result

            except Exception as e:
                logger.error(f"Data error for {symbol} {timeframe}m: {e}")
                return pd.DataFrame()

        return pd.DataFrame()


class PrivateExchange:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base = BASE_URL
        self.session = requests.Session()
        self._last_response = None
        self.last_positions_payload = None  # برای ریسک فری
        self.connected = False
        self._cached_balance = None
        
    def _sign(self, method, uri, ts):
        payload = f"{ts}{method.upper()}{uri}"
        return hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    
    def _request(self, method, uri, data=None):
        self._last_response = None
        url = f"{self.base}{uri}"

        logger.info(
            "[EXCHANGE REQUEST] %s %s | DATA=%s",
            method.upper(),
            url,
            json.dumps(data, ensure_ascii=False) if data else None
        )

        max_attempts = 3
        for attempt in range(max_attempts):
            ts = str(int(time.time() * 1000))
            sig = self._sign(method, uri, ts)

            headers = {
                "X-API-Key": self.api_key,
                "X-Timestamp": ts,
                "X-Signature": sig,
                "Content-Type": "application/json"
            }

            throttle_truetrade()

            try:
                r = self.session.request(
                    method,
                    url,
                    headers=headers,
                    json=data,
                    timeout=15
                )

                self._last_response = r

                logger.info(
                    "[EXCHANGE RESPONSE] %s %s | HTTP=%s | BODY=%s",
                    method.upper(),
                    uri,
                    r.status_code,
                    r.text
                )

                logger.info(
                    "[EXCHANGE RAW RESPONSE COMPLETE] "
                    "method=%s | uri=%s | status=%s | body=%s",
                    method.upper(),
                    uri,
                    r.status_code,
                    r.text,
                )

                if r.status_code == 429:
                    if attempt == max_attempts - 1:
                        logger.error(
                            "[EXCHANGE 429 RATE LIMIT] %s %s | HTTP=%s | "
                            "giving up after %s attempts | BODY=%s",
                            method.upper(), uri, r.status_code, max_attempts, r.text
                        )
                        r.raise_for_status()

                    wait = min(20, 2 ** attempt) + random.random() * 0.5
                    logger.warning(
                        "[EXCHANGE 429 RATE LIMIT] %s %s | HTTP=%s | "
                        "attempt %s/%s, retry in %.2fs",
                        method.upper(), uri, r.status_code,
                        attempt + 1, max_attempts, wait
                    )
                    time.sleep(wait)
                    continue

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
                self.connected = False
                raise

        raise RuntimeError(f"Exhausted {max_attempts} attempts for {method} {uri}")

    def test_connection(self):
        try:
            self.last_positions_payload = self._request("GET", "/futures/positions")
            return True
        except Exception:
            return False
    
    def fetch_balance(self):
        try:
            data = self._request("GET", "/futures/assets")
            assets = data.get('assets', [])
            for a in assets:
                if a.get('symbol') == 'USDT':
                    balance = float(a.get('availableBalance', 0))
                    self._cached_balance = balance
                    logger.info(f"[BALANCE] Fetched: {balance:.4f} USDT")
                    return balance
            self._cached_balance = 0.0
            return 0.0
        except Exception as e:
            if self._cached_balance is not None:
                logger.warning(
                    f"[BALANCE] Failed to fetch fresh balance: {e} — "
                    f"using cached balance: {self._cached_balance:.4f} USDT"
                )
                return self._cached_balance
            else:
                logger.error(f"[BALANCE] Failed to fetch balance and no cache available: {e}")
                return 0.0
    
    def _round_price(self, price, symbol):
        tick = TICK_SIZES.get(symbol.upper(), 0.01)
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        return round(round(float(price)/tick)*tick, prec)
    
    def create_order(self, symbol, side, capital, leverage, take_profit=None, stop_loss=None):
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        
        side_upper = str(side).upper().strip()
        if side_upper in ("BUY", "LONG"):
            api_side = "LONG"
        elif side_upper in ("SELL", "SHORT"):
            api_side = "SHORT"
        else:
            api_side = side_upper
        
        od = {
            "symbol": symbol.upper(),
            "side": api_side,
            "tradeType": "MARKET",
            "leverage": int(leverage),
            "cost": f"{capital:.{prec}f}",
            "walletType": "debit"
        }
        
        if take_profit is not None and not math.isnan(take_profit) and take_profit > 0:
            rounded_tp = self._round_price(take_profit, symbol)
            if rounded_tp > 0:
                od["takeProfit"] = f"{rounded_tp:.{prec}f}"
                logger.info(f"[TP] Take Profit set at {rounded_tp:.{prec}f}")
            else:
                logger.warning(
                    f"[TP] {symbol}: raw take_profit={take_profit} rounded to 0 "
                    f"at precision={prec} (tick={TICK_SIZES.get(symbol.upper())}) — "
                    f"omitting field instead of sending an invalid 0.00 to the exchange"
                )

        if stop_loss is not None and not math.isnan(stop_loss) and stop_loss > 0:
            rounded_sl = self._round_price(stop_loss, symbol)
            if rounded_sl > 0:
                od["stopLoss"] = f"{rounded_sl:.{prec}f}"
                logger.info(f"[SL] Stop Loss set at {rounded_sl:.{prec}f}")
            else:
                logger.warning(
                    f"[SL] {symbol}: raw stop_loss={stop_loss} rounded to 0 "
                    f"at precision={prec} (tick={TICK_SIZES.get(symbol.upper())}) — "
                    f"omitting field instead of sending an invalid 0.00 to the exchange"
                )
        
        logger.info(
            "[ORDER REQUEST] %s %s\n%s",
            symbol.upper(),
            api_side,
            json.dumps(od, ensure_ascii=False, indent=2)
        )
        
        request_msg = (
            f"📤 ORDER REQUEST\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Symbol: {symbol.upper()}\n"
            f"Side: {api_side}\n"
            f"Leverage: {int(leverage)}\n"
            f"Cost: {capital:.{prec}f}\n"
            f"Stop Loss: {od.get('stopLoss', 'N/A')}\n"
            f"Take Profit: {od.get('takeProfit', 'N/A')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Body:\n{json.dumps(od, ensure_ascii=False, indent=2)}"
        )
        if not send_telegram_long(request_msg):
            logger.error("[TELEGRAM] Failed to send ORDER REQUEST")
        
        try:
            result = self._request("POST", "/futures/positions", od)
            position_id = result.get("positionId") if isinstance(result, dict) else None
            
            logger.info(
                "[ORDER SUCCESS] %s %s\n%s",
                symbol.upper(),
                api_side,
                json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, (dict, list)) else str(result)
            )
            
            success_msg = (
                f"✅ ORDER SUCCESS\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"Symbol: {symbol.upper()}\n"
                f"Side: {api_side}\n"
                f"Position ID: {position_id}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"Response:\n{json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, (dict, list)) else str(result)}"
            )
            if not send_telegram_long(success_msg):
                logger.error("[TELEGRAM] Failed to send ORDER SUCCESS")
            
            return result
            
        except Exception as e:
            response = self._last_response
            
            if response is not None:
                http_status = response.status_code
                raw_response = response.text
                
                try:
                    parsed_json = response.json()
                    parsed_text = json.dumps(parsed_json, ensure_ascii=False, indent=2)
                except Exception:
                    parsed_text = "(Response is not valid JSON)"
                
                complete_error = (
                    f"HTTP STATUS: {http_status}\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"RAW RESPONSE:\n{raw_response}\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"PARSED JSON:\n{parsed_text}"
                )
            else:
                complete_error = "NO HTTP RESPONSE RECEIVED"
            
            local_exception = repr(e)
            
            logger.error(
                "[ORDER FAILED] %s %s\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Symbol: %s\n"
                "Side: %s\n"
                "Leverage: %s\n"
                "Cost: %s\n"
                "Stop Loss: %s\n"
                "Take Profit: %s\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Request Body:\n%s\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🔴 COMPLETE EXCHANGE ERROR:\n%s\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "LOCAL EXCEPTION: %s",
                symbol.upper(),
                api_side,
                symbol.upper(),
                api_side,
                int(leverage),
                f"{capital:.{prec}f}",
                od.get('stopLoss', 'N/A'),
                od.get('takeProfit', 'N/A'),
                json.dumps(od, ensure_ascii=False, indent=2),
                complete_error,
                local_exception
            )
            
            failed_msg = (
                f"❌ ORDER FAILED\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"Symbol: {symbol.upper()}\n"
                f"Side: {api_side}\n"
                f"Leverage: {int(leverage)}\n"
                f"Cost: {capital:.{prec}f}\n"
                f"Stop Loss: {od.get('stopLoss', 'N/A')}\n"
                f"Take Profit: {od.get('takeProfit', 'N/A')}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"Request Body:\n{json.dumps(od, ensure_ascii=False, indent=2)}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"🔴 COMPLETE EXCHANGE ERROR:\n{complete_error}\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"LOCAL EXCEPTION: {local_exception}"
            )
            if not send_telegram_long(failed_msg):
                logger.error("[TELEGRAM] Failed to send ORDER FAILED")
            
            return None

    # ============================================================
    # 🛡️ متد تغییر استاپ (ریسک فری) طبق مستندات TheTrueTrade
    # ============================================================
    def update_position_sl(self, pos, stop_loss):
        """
        تغییر استاپ‌لاس پوزیشن باز (ریسک فری).
        PATCH /futures/positions/{id}/tpsl
        طبق مستندات TheTrueTrade
        """
        symbol = str(pos.get("symbol", "")).upper()
        prec = PRICE_PRECISION.get(symbol, 2)
        sl_str = f"{self._round_price(stop_loss, symbol):.{prec}f}"

        body = {"stopLoss": sl_str}
        
        tp = pos.get("takeProfit")
        if tp:
            try:
                body["takeProfit"] = f"{self._round_price(float(tp), symbol):.{prec}f}"
            except Exception:
                pass

        body["stopLossStrategy"] = "LATEST_PRICE"
        body["stopLossOrderType"] = "STOP_MARKET"

        uri = f"/futures/positions/{pos.get('id')}/tpsl"
        logger.info(f"[RISK-FREE] update SL request: PATCH {uri} {body}")
        
        try:
            return self._request("PATCH", uri, body)
        except Exception as e:
            logger.error(f"[RISK-FREE] update SL failed: {e}")
            raise


# ================= RAILWAY HTTP HEALTH SERVER =================

STOP_EVENT = threading.Event()

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/health"):
            body = b'{"status":"ok","service":"DTM Trading Bot"}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = b'{"status":"not_found"}'
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_HEAD(self):
        if self.path in ("/", "/health"):
            body = b'{"status":"ok","service":"DTM Trading Bot"}'
            self.send_response(200)
        else:
            body = b'{"status":"not_found"}'
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

    def log_message(self, fmt, *args):
        logger.info("[HEALTH] " + (fmt % args))


def run_health_server(port):
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.timeout = 1

    logger.info("HTTP health server listening on 0.0.0.0:%d", port)

    try:
        while not STOP_EVENT.is_set():
            server.handle_request()
    finally:
        server.server_close()
        logger.info("HTTP health server stopped")


def _handle_shutdown(signum, frame):
    logger.info("Shutdown signal received: %s", signum)
    STOP_EVENT.set()


# ================================================================
# STARTUP DIAGNOSTIC
# ================================================================

def startup_diagnostic(exchange, public):
    logger.info("=" * 60)
    logger.info("STARTUP DIAGNOSTIC BEGINNING...")
    logger.info("=" * 60)

    failures = []
    warnings = []
    balance = None
    strategy_ok = False
    test_signal = None
    test_entry = None
    test_symbol = SYMBOLS[0] if SYMBOLS else "LTCUSDT"

    def add(title, ok, details=""):
        status = "✅ ACTIVE" if ok else "❌ FAILED"
        text = f"{title}: {status}"
        if details:
            text += f"\n{details}"
        return text

    def full_exchange_error(prefix="FULL EXCHANGE ERROR"):
        response = getattr(exchange, "_last_response", None)

        if response is None:
            return (
                f"{prefix}\n"
                "NO HTTP RESPONSE RECEIVED"
            )

        text = (
            f"{prefix}\n"
            f"HTTP STATUS: {response.status_code}\n"
            f"HTTP URL: {response.url}\n"
            f"RAW RESPONSE:\n{response.text}"
        )

        try:
            parsed = response.json()
            text += (
                "\nPARSED JSON:\n"
                + json.dumps(
                    parsed,
                    ensure_ascii=False,
                    indent=2
                )
            )
        except Exception:
            pass

        return text

    try:
        send_telegram("🧪 DTM startup diagnostic started")
        telegram_ok = True
    except Exception:
        telegram_ok = False

    try:
        exchange._last_response = None
        exchange_ok = exchange.test_connection()
    except Exception:
        exchange_ok = False

    try:
        exchange._last_response = None
        balance = exchange.fetch_balance()
        if balance is None or balance < 0:
            balance = None
    except Exception:
        balance = None

    market_ok = 0
    total_checks = len(SYMBOLS) * len(TIMEFRAMES)
    market_status_list = []

    for symbol in SYMBOLS:
        for tf in TIMEFRAMES:
            try:
                df = public.fetch_ohlcv(symbol, tf)
                if df is not None and not df.empty:
                    market_ok += 1
                    market_status_list.append(f"{symbol}({tf})")
            except Exception:
                pass

    market_all_ok = (market_ok == total_checks)

    calculate_signals_fn = None
    strategy_import_ok = False

    try:
        from strategy_wrapper import calculate_signals as _calculate_signals
        calculate_signals_fn = _calculate_signals
        strategy_import_ok = callable(calculate_signals_fn)
    except Exception:
        strategy_import_ok = False

    if callable(calculate_signals_fn):
        for symbol in SYMBOLS:
            try:
                df = public.fetch_ohlcv(symbol)
                if df is not None and not df.empty:
                    test_signal, test_entry, stop_price, target_price, _, _ = calculate_signals_fn(df, symbol)
                    strategy_ok = True
                    test_symbol = symbol
                    break
            except Exception:
                continue

    try:
        exchange._last_response = None
        positions = exchange._request("GET", "/futures/positions")
        position_api_ok = True
    except Exception:
        position_api_ok = False

    try:
        create_order = getattr(exchange, "create_order", None)
        create_order_ok = callable(create_order)
    except Exception:
        create_order_ok = False

    from datetime import datetime, timezone, timedelta
    
    IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
    UTC_TZ = timezone.utc
    
    def _now_iran():
        return datetime.now(UTC_TZ).astimezone(IRAN_TZ)
    
    now_iran = _now_iran()
    time_str = now_iran.strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "🚀 راه‌اندازی ربات DTM",
        "─────────────────────────────────────────",
        f"🔒 حالت: فقط‌خوانی | سفارش: ❌ ارسال نمی‌شود",
        f"💰 موجودی: {balance:.4f} USDT" if balance else "💰 موجودی: ❌ نامشخص",
        f"📱 تلگرام: {'✅' if telegram_ok else '❌'} | صرافی: {'✅' if exchange_ok else '❌'}",
        "─────────────────────────────────────────",
    ]
    
    if market_status_list:
        report_lines.append(f"📊 بازارهای فعال: {market_ok}/{total_checks}")
        line1 = "   " + " ".join(market_status_list[:4]) if len(market_status_list) >= 4 else "   " + " ".join(market_status_list)
        line2 = "   " + " ".join(market_status_list[4:]) if len(market_status_list) > 4 else ""
        report_lines.append(line1)
        if line2:
            report_lines.append(line2)
    else:
        report_lines.append(f"📊 بازارهای فعال: ۰/{total_checks} ❌")
    
    report_lines.append("─────────────────────────────────────────")
    
    if strategy_import_ok:
        report_lines.append(f"📈 استراتژی: {'✅ فعال' if strategy_ok else '⚠️ قابل‌اجرا اما بدون سیگنال'}")
    else:
        report_lines.append("📈 استراتژی: ❌ غیرفعال")
    
    if strategy_ok:
        report_lines.append(f"🧪 تست {test_symbol}: سیگنال={test_signal} | ورود={test_entry}")
    else:
        report_lines.append("🧪 تست استراتژی: ❌ انجام نشد")
    
    report_lines.append("─────────────────────────────────────────")
    
    leverage_str = " ".join([f"{k}={v}" for k, v in LEVERAGE_MAP.items()])
    report_lines.append(f"⚙️ تنظیمات: ریسک={TARGET_RISK}٪")
    report_lines.append(f"🔧 اهرم: {leverage_str}")
    report_lines.append(f"💼 سرمایه پایه: {trade_ledger.BASE_CAPITAL} USDT")
    
    report_lines.append("─────────────────────────────────────────")
    report_lines.append(f"✅ راه‌اندازی کامل شد | زمان: {time_str}")
    
    final_report = "\n".join(report_lines)
    
    logger.info(
        "[STARTUP DIAGNOSTIC]\n%s",
        final_report
    )

    try:
        send_telegram_long(final_report)
        logger.info(
            "[STARTUP DIAGNOSTIC] TELEGRAM SENT"
        )
    except Exception as e:
        logger.exception(
            "[STARTUP DIAGNOSTIC] "
            "TELEGRAM SEND FAILED: %s",
            e,
        )

    return final_report


# ============================================================
# 🛡️ پایش ریسک فری
# ============================================================
def _is_open_position(p):
    try:
        return p.get("isActive") is True or str(p.get("status", "")).upper() == "OPEN"
    except Exception:
        return False


def risk_free_monitor(exchange):
    """
    🛡️ پایش ریسک فری — در هر سیکل ۳۰ ثانیه‌ای، درست بعد از test_connection صدا زده می‌شود.
    """
    if not RISK_FREE_ENABLED or not RISK_FREE_PENDING:
        return

    payload = getattr(exchange, "last_positions_payload", None)
    if not isinstance(payload, dict):
        return

    meta = payload.get("meta") or {}
    total_pages = meta.get("totalPages", 1)
    current_page = meta.get("currentPage", 1)
    open_positions = [p for p in (payload.get("items") or []) if _is_open_position(p)]

    needed_ids = {
        str(r.get("position_id")) for r in RISK_FREE_PENDING.values()
        if r.get("state") == "pending" and r.get("position_id") is not None
    }
    found_ids = {str(p.get("id")) for p in open_positions}
    page = current_page
    while needed_ids and not needed_ids.issubset(found_ids) and page < total_pages:
        page += 1
        try:
            more = exchange._request("GET", f"/futures/positions?page={page}")
        except Exception:
            break
        for p in (more.get("items") or []):
            if _is_open_position(p):
                open_positions.append(p)
                found_ids.add(str(p.get("id")))

    for key in list(RISK_FREE_PENDING.keys()):
        rec = RISK_FREE_PENDING[key]
        if rec.get("state") != "pending":
            continue

        symbol = str(rec.get("symbol", "")).upper()
        side = str(rec.get("side", "")).upper()
        prec = PRICE_PRECISION.get(symbol, 2)

        pos = None
        pid = rec.get("position_id")
        if pid is not None:
            for p in open_positions:
                if str(p.get("id")) == str(pid):
                    pos = p
                    break
        if pos is None:
            cands = [
                p for p in open_positions
                if str(p.get("symbol", "")).upper() == symbol
                and str(p.get("side", "")).upper() == side
            ]
            if len(cands) == 1:
                pos = cands[0]

        if pos is None:
            rec["missing_cycles"] = rec.get("missing_cycles", 0) + 1
            if rec["missing_cycles"] > 10:
                logger.info(f"[RISK-FREE] {symbol} {side}: no open position found — record dropped")
                RISK_FREE_PENDING.pop(key, None)
            continue

        try:
            entry_actual = float(pos.get("entryPrice") or rec.get("entry_est"))
            size = abs(float(pos.get("size") or 0))
            mark = float(pos.get("markPrice") or 0)
        except Exception:
            logger.warning(f"[RISK-FREE] {symbol} {side}: bad position numbers")
            continue

        rf_pct = rec.get("rf_pct")
        if rf_pct is None or size <= 0 or entry_actual <= 0:
            continue

        trigger = entry_actual * (1 + rf_pct) if side == "LONG" else entry_actual * (1 - abs(rf_pct))
        crossed = (mark >= trigger) if side == "LONG" else (mark <= trigger)
        if not crossed:
            continue

        try:
            open_fee = float(pos.get("openFees") or 0)
        except Exception:
            open_fee = 0.0
        if open_fee <= 0:
            open_fee = RISK_FREE_FEE_DEFAULT

        if RISK_FREE_FEE_MODE == "round_trip":
            try:
                close_fee = float(pos.get("closeFees") or open_fee)
            except Exception:
                close_fee = open_fee
            if close_fee <= 0:
                close_fee = open_fee
            fee_total = open_fee + close_fee
        else:
            fee_total = open_fee

        old_sl = pos.get("stopLoss")
        tick = TICK_SIZES.get(symbol, 0.01)
        if side == "LONG":
            new_sl = exchange._round_price(entry_actual + fee_total / size, symbol)
            if new_sl <= entry_actual:
                new_sl = exchange._round_price(entry_actual + tick, symbol)
            valid = (entry_actual < new_sl < mark)
        else:
            new_sl = exchange._round_price(entry_actual - fee_total / size, symbol)
            if new_sl >= entry_actual:
                new_sl = exchange._round_price(entry_actual - tick, symbol)
            valid = (mark < new_sl < entry_actual)

        if not valid:
            logger.warning(
                f"[RISK-FREE] {symbol} {side}: invalid SL {new_sl} "
                f"(entry={entry_actual}, mark={mark}) — retry next cycle"
            )
            continue

        try:
            exchange.update_position_sl(pos, new_sl)
        except Exception as e:
            logger.error(f"[RISK-FREE] {symbol} {side}: exchange update failed: {e}")
            continue

        # ========== هماهنگ‌سازی دفترچه ==========
        try:
            trade_ledger.update_open_trade_stop(
                symbol,
                rec.get("timeframe"),
                side,
                rec.get("signal_bar_ts_ms"),
                new_sl,
            )
        except Exception as ledger_err:
            logger.error(f"[RISK-FREE] {symbol} {side}: ledger sync failed: {ledger_err}")

        rec["state"] = "done"

        msg = (
            f"🛡️ ریسک فری فعال شد\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"Symbol: {symbol} | {side}\n"
            f"Position ID: {pos.get('id')}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎯 Trigger: {trigger:.{prec}f}\n"
            f"💹 Mark: {mark:.{prec}f}\n"
            f"💰 Entry: {entry_actual:.{prec}f} | Size: {size}\n"
            f"💸 کارمزد مبنا: {fee_total:.4f} USDT\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🛑 استاپ قبلی: {old_sl}\n"
            f"🛡️ استاپ جدید (ریسک فری): {new_sl:.{prec}f}\n"
            f"اگر استاپ جدید خورده شود ≈ کارمزد بازپس‌گرفته شده ✅"
        )
        send_telegram_long(msg)
        logger.info(f"[RISK-FREE] {symbol} {side} | SL {old_sl} -> {new_sl:.{prec}f} | DONE")


def loop():
    public = PublicData()
    exchange = PrivateExchange()

    try:
        startup_diagnostic(exchange, public)
    except Exception as e:
        logger.exception("[STARTUP DIAGNOSTIC] FATAL ERROR: %s", e)

    send_telegram("🤖 ربات شروع شد - تایم‌فریم‌های ۱، ۵ و ۱۵ دقیقه")
    logger.info("Worker bot started with timeframes: %s", TIMEFRAMES)

    BASE_CAPITAL = 1.5
    BALANCE_USE_RATIO = 0.70
    
    last_processed_boundary = {tf: 0 for tf in TIMEFRAMES}

    while not STOP_EVENT.is_set():
        try:
            if not exchange.test_connection():
                send_telegram("⚠️ اتصال صرافی قطع است")
                STOP_EVENT.wait(60)
                continue

            # ============================================================
            # 🛡️ پایش ریسک فری
            # ============================================================
            try:
                risk_free_monitor(exchange)
            except Exception as e:
                logger.exception(f"[RISK-FREE] monitor error: {e}")

            balance = exchange.fetch_balance()
            current_time = time.time()
            
            for timeframe in TIMEFRAMES:
                tf_minutes = int(timeframe)
                tf_seconds = tf_minutes * 60
                BOUNDARY_SETTLE_BUFFER_SEC = 5

                current_boundary = int(current_time // tf_seconds) * tf_seconds

                if current_time < current_boundary + BOUNDARY_SETTLE_BUFFER_SEC:
                    continue

                if current_boundary <= last_processed_boundary.get(timeframe, 0):
                    continue

                last_processed_boundary[timeframe] = current_boundary
                logger.info(f"🔄 Checking {timeframe}m timeframes... (boundary={current_boundary})")
                
                for symbol in SYMBOLS:
                    try:
                        df_signal = public.fetch_ohlcv_binance(symbol, timeframe)
                        if df_signal.empty:
                            logger.warning(f"Empty BINANCE data for {symbol} {timeframe}m")
                            continue

                        df_exec = public.fetch_ohlcv(symbol, timeframe)
                        if df_exec.empty:
                            logger.warning(f"Empty thetruetrade.io data for {symbol} {timeframe}m")
                            df_exec = df_signal

                        df = df_signal

                        trade_ledger.update_open_trades(symbol, timeframe, df_exec)

                        # ============================================================
                        # اجرای استراتژی — ۶ مقدار
                        # ============================================================
                        sig, entry, stop_price, target_price, signal_bar_ts_ms, risk_free_pct = calculate_signals(df, symbol, timeframe)

                        logger.info(
                            f"[{timeframe}m] {symbol}: signal={sig}, entry={entry}, "
                            f"stop={stop_price}, target={target_price}, candles={len(df)}, "
                            f"signal_bar_ts_ms={signal_bar_ts_ms}"
                        )

                        if sig and entry is not None:
                            trade_ledger.record_signal(
                                symbol=symbol,
                                timeframe=timeframe,
                                direction=sig,
                                entry=entry,
                                stop=stop_price,
                                target=target_price,
                                entry_time_ms=signal_bar_ts_ms,
                                leverage=LEVERAGE_MAP.get(symbol, 50),
                                order_placed=None,
                                risk_free_pct=risk_free_pct,  # 🆕 برای شبیه‌سازی مستقل ریسک‌فری در گزارش‌ها
                            )

                        if not sig or balance <= 0 or stop_price is None or entry is None:
                            continue

                        allowed_leverage = LEVERAGE_MAP.get(symbol, 50)

                        if sig == "LONG":
                            stop_pct = abs(entry - stop_price) / entry if entry > 0 else 0
                        else:
                            stop_pct = abs(stop_price - entry) / entry if entry > 0 else 0

                        if stop_pct <= 0:
                            logger.warning(f"{symbol}: invalid stop_pct={stop_pct}, skip")
                            continue

                        if target_price is not None and not math.isnan(target_price) and target_price > 0:
                            if sig == "LONG":
                                target_pct = abs(target_price - entry) / entry
                            else:
                                target_pct = abs(entry - target_price) / entry
                        else:
                            target_pct = 0

                        old_leverage = 1.0 / stop_pct

                        if old_leverage > allowed_leverage:
                            required_capital = (old_leverage / allowed_leverage) * BASE_CAPITAL
                            leverage_mode = "INCREASED"
                        else:
                            required_capital = BASE_CAPITAL
                            leverage_mode = "BASE"

                        if balance < required_capital:
                            capital = balance * BALANCE_USE_RATIO
                            actual_stop_dollar = capital * stop_pct * allowed_leverage
                            actual_profit_dollar = (
                                capital * target_pct * allowed_leverage
                                if target_pct > 0 else None
                            )
                            mode = "REDUCED_98"
                        else:
                            capital = required_capital
                            actual_stop_dollar = BASE_CAPITAL
                            actual_profit_dollar = (
                                (target_pct / stop_pct) * BASE_CAPITAL
                                if target_pct > 0 else None
                            )
                            mode = "FULL"

                        r_value = (target_pct / stop_pct) if target_pct > 0 else None

                        profit_str = f"{actual_profit_dollar:.4f}" if actual_profit_dollar else "N/A"
                        r_str = f"{r_value:.2f}" if r_value else "N/A"

                        logger.info(
                            f"[{timeframe}m][{symbol}] سیگنال={sig} | ورود={entry}\n"
                            f"  درصد استاپ={stop_pct:.6f} | درصد تارگت={target_pct:.6f}\n"
                            f"  اهرم قدیمی={old_leverage:.2f} | اهرم مجاز={allowed_leverage}\n"
                            f"  سرمایه موردنیاز={required_capital:.4f} | حالت اهرم={leverage_mode}\n"
                            f"  موجودی={balance:.4f} | حالت سرمایه={mode}\n"
                            f"  سرمایه ارسالی={capital:.4f}\n"
                            f"  استاپ دلاری=${actual_stop_dollar:.4f}\n"
                            f"  سود دلاری=${profit_str}\n"
                            f"  R={r_str}"
                        )

                        # ============================================================
                        # 🆕 بررسی حداقل سرمایه قابل قبول صرافی قبل از ارسال سفارش
                        # (علت اصلی اینکه ریسک‌فری «اصلاً اجرا نمی‌شد»: تمام سفارش‌ها
                        # به‌خاطر موجودی/سرمایه‌ی خیلی کم با خطای صرافی
                        # "Collateral is below the minimum allowed" رد می‌شدند، پس هیچ
                        # پوزیشنی باز نمی‌شد و ریسک‌فری چیزی برای مانیتور کردن نداشت)
                        # ============================================================
                        if capital < MIN_ORDER_COST_USDT:
                            logger.warning(
                                f"[SKIP-LOW-BALANCE] {symbol} {sig}: cost محاسبه‌شده "
                                f"{capital:.4f} USDT کمتر از حداقل مجاز ({MIN_ORDER_COST_USDT} "
                                f"USDT) است — سفارش ارسال نشد (صرافی حتماً رد می‌کرد)."
                            )
                            send_telegram(
                                f"⚠️ سیگنال {sig} برای {symbol} ({timeframe}m) اجرا نشد\n"
                                f"سرمایه محاسبه‌شده: {capital:.4f} USDT\n"
                                f"حداقل مجاز فعلی (تنظیم‌شده): {MIN_ORDER_COST_USDT} USDT\n"
                                f"موجودی فعلی حساب: {balance:.4f} USDT\n"
                                f"❗️ تا افزایش موجودی، این سیگنال‌ها معامله نمی‌شوند."
                            )
                            continue

                        exec_stop_price = stop_price
                        exec_target_price = target_price
                        exec_anchor_price = None
                        try:
                            df_anchor = public.fetch_ohlcv(symbol, "1")
                            if not df_anchor.empty:
                                exec_anchor_price = float(df_anchor['close'].iloc[-1])
                                if sig == "LONG":
                                    exec_stop_price = exec_anchor_price * (1 - stop_pct)
                                    exec_target_price = (
                                        exec_anchor_price * (1 + target_pct)
                                        if target_pct > 0 else None
                                    )
                                else:
                                    exec_stop_price = exec_anchor_price * (1 + stop_pct)
                                    exec_target_price = (
                                        exec_anchor_price * (1 - target_pct)
                                        if target_pct > 0 else None
                                    )
                                logger.info(
                                    f"[{timeframe}m][{symbol}] لنگر اجرا (thetruetrade.io)={exec_anchor_price} | "
                                    f"stop(binance)={stop_price} → stop(exec)={exec_stop_price} | "
                                    f"target(binance)={target_price} → target(exec)={exec_target_price}"
                                )
                            else:
                                logger.warning(
                                    f"{symbol}: exec-anchor price unavailable — "
                                    f"using BINANCE anchor from df_signal"
                                )
                                binance_anchor_price = float(df_signal['close'].iloc[-1])
                                if sig == "LONG":
                                    exec_stop_price = binance_anchor_price * (1 - stop_pct)
                                    exec_target_price = (
                                        binance_anchor_price * (1 + target_pct)
                                        if target_pct > 0 else None
                                    )
                                else:
                                    exec_stop_price = binance_anchor_price * (1 + stop_pct)
                                    exec_target_price = (
                                        binance_anchor_price * (1 - target_pct)
                                        if target_pct > 0 else None
                                    )
                                logger.info(
                                    f"[{timeframe}m][{symbol}] FALLBACK BINANCE anchor={binance_anchor_price} | "
                                    f"stop(exec)={exec_stop_price} | target(exec)={exec_target_price}"
                                )
                        except Exception as anchor_err:
                            logger.warning(
                                f"{symbol}: exec-anchor fetch failed ({anchor_err}) — "
                                f"using BINANCE anchor from df_signal"
                            )
                            try:
                                binance_anchor_price = float(df_signal['close'].iloc[-1])
                                if sig == "LONG":
                                    exec_stop_price = binance_anchor_price * (1 - stop_pct)
                                    exec_target_price = (
                                        binance_anchor_price * (1 + target_pct)
                                        if target_pct > 0 else None
                                    )
                                else:
                                    exec_stop_price = binance_anchor_price * (1 + stop_pct)
                                    exec_target_price = (
                                        binance_anchor_price * (1 - target_pct)
                                        if target_pct > 0 else None
                                    )
                                logger.info(
                                    f"[{timeframe}m][{symbol}] EXCEPTION FALLBACK BINANCE anchor={binance_anchor_price} | "
                                    f"stop(exec)={exec_stop_price} | target(exec)={exec_target_price}"
                                )
                            except Exception as e2:
                                logger.warning(
                                    f"{symbol}: even binance anchor failed ({e2}) — "
                                    f"using raw stop/target"
                                )
                                exec_stop_price = stop_price
                                exec_target_price = target_price

                        # ============================================================
                        # ارسال سفارش
                        # ============================================================
                        order_result = exchange.create_order(
                            symbol,
                            sig,
                            capital,
                            allowed_leverage,
                            take_profit=exec_target_price,
                            stop_loss=exec_stop_price,
                        )

                        # ============================================================
                        # 🛡️ ثبت پندینگ ریسک فری
                        # 🆕 فقط اگر RISK_FREE_ALL_TIMEFRAMES=1 باشد (همه‌ی تایم‌فریم‌ها)
                        # یا timeframe فعلی همان RISK_FREE_TIMEFRAME انتخابی باشد.
                        # ============================================================
                        risk_free_tf_allowed = (
                            RISK_FREE_ALL_TIMEFRAMES or str(timeframe) == str(RISK_FREE_TIMEFRAME)
                        )
                        if order_result is not None and risk_free_pct is not None and risk_free_tf_allowed:
                            position_id = None
                            if isinstance(order_result, dict):
                                position_id = (
                                    order_result.get("positionId")
                                    or order_result.get("id")
                                    or (order_result.get("position") or {}).get("id")
                                )
                            entry_est_val = exec_anchor_price if exec_anchor_price else entry
                            RISK_FREE_PENDING[f"{symbol}|{sig}|{time.time()}"] = {
                                "symbol": symbol,
                                "side": sig,
                                "timeframe": timeframe,
                                "position_id": position_id,
                                "entry_est": float(entry_est_val),
                                "rf_pct": float(risk_free_pct),
                                "signal_bar_ts_ms": signal_bar_ts_ms,
                                "opened_at": time.time(),
                                "state": "pending",
                                "missing_cycles": 0,
                            }
                            logger.info(
                                f"[RISK-FREE] {symbol} {sig} pending | "
                                f"position_id={position_id} | rf_pct={risk_free_pct:.6f}"
                            )
                        elif order_result is not None and risk_free_pct is not None:
                            logger.info(
                                f"[RISK-FREE] {symbol} {sig} on tf={timeframe} — skipped "
                                f"(RISK_FREE_ALL_TIMEFRAMES=0, target tf={RISK_FREE_TIMEFRAME})"
                            )

                        balance = exchange.fetch_balance()
                        
                    except Exception as e:
                        logger.exception(f"Error processing {symbol} {timeframe}m: {e}")
                        continue

            STOP_EVENT.wait(30)

        except Exception as e:
            logger.exception("Loop error")
            STOP_EVENT.wait(60)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    signal.signal(signal.SIGTERM, _handle_shutdown)
    signal.signal(signal.SIGINT, _handle_shutdown)

    health_thread = threading.Thread(
        target=run_health_server,
        args=(port,),
        name="health-server",
        daemon=True,
    )
    health_thread.start()

    report_thread = threading.Thread(
        target=trade_ledger.scheduler_loop,
        args=(send_telegram_long, STOP_EVENT),
        name="report-scheduler",
        daemon=True,
    )
    report_thread.start()

    # ============================================================
    # 🚀 اجرای خودکار بک‌تست ۶۰ روزه در هر استارت — غیرمسدودکننده
    # ============================================================
    def _run_backtest_once():
        try:
            import subprocess
            import sys as _sys
            from pathlib import Path as _Path
            bt = _Path(__file__).resolve().parent / "backtest_report.py"
            if bt.exists():
                subprocess.Popen(
                    [_sys.executable, str(bt), "--mode", "both", "--force"],
                    cwd=str(bt.parent),
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                logger.info("[BACKTEST] launched in background")
            else:
                logger.warning("[BACKTEST] backtest_report.py not found")
        except Exception as e:
            logger.error(f"[BACKTEST] launch failed: {e}")

    _run_backtest_once()


    logger.info("DTM WORKER START | HTTP port=%d", port)

    try:
        loop()
    finally:
        STOP_EVENT.set()
        health_thread.join(timeout=3)
        report_thread.join(timeout=3)
        
        logger.info("DTM PROCESS EXIT")
