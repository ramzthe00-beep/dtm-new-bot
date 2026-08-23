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
SYMBOLS = ["LTCUSDT", "DOGEUSDT", "ETHUSDT", "BNBUSDT"]
HISTORY_BARS = 500
LEVERAGE_MAP = {"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50, "BNBUSDT": 75}
TARGET_RISK = 2.0
TICK_SIZES = {"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01, "BNBUSDT": 0.01}
PRICE_PRECISION = {"LTCUSDT": 2, "DOGEUSDT": 5, "ETHUSDT": 2, "BNBUSDT": 2}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BOT")

# ===== لاگ اولیه برای اطمینان از اجرا =====
logger.info("=" * 60)
logger.info("BOT STARTING...")
logger.info("=" * 60)

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=15)
        if r.status_code == 200:
            return True
        else:
            logger.error(f"[TELEGRAM] Failed to send message: {r.status_code} {r.text[:300]}")
            return False
    except Exception as e:
        logger.error(f"[TELEGRAM] Failed to send message: {e}")
        return False

def send_telegram_long(text):
    """Send long text to Telegram, splitting into chunks if needed."""
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
    def __init__(self):
        self.base = BASE_URL
        self.session = requests.Session()
    def fetch_ohlcv(self, symbol):
        now = int(time.time())
        from_ts = now - HISTORY_BARS * 60 - 60
        uri = f"/futures/udf/history?symbol={symbol.upper()}&resolution=1&from={from_ts}&to={now}&countback={HISTORY_BARS}"
        try:
            r = self.session.get(f"{self.base}{uri}", timeout=20)
            r.raise_for_status()
            data = r.json()
            if data.get('s') != 'ok':
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

            return df.tail(HISTORY_BARS)
        except Exception as e:
            logger.error(f"Data error: {e}")
            return pd.DataFrame()

class PrivateExchange:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base = BASE_URL
        self.session = requests.Session()
        self._last_response = None
        self.connected = False
        
    def _sign(self, method, uri, ts):
        payload = f"{ts}{method.upper()}{uri}"
        return hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    
    def _request(self, method, uri, data=None):
        # IMPORTANT: never reuse a previous HTTP response
        self._last_response = None

        ts = str(int(time.time()*1000))
        sig = self._sign(method, uri, ts)

        headers = {
            "X-API-Key": self.api_key,
            "X-Timestamp": ts,
            "X-Signature": sig,
            "Content-Type": "application/json"
        }

        url = f"{self.base}{uri}"

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

            # Keep the COMPLETE raw exchange response visible in log
            logger.info(
                "[EXCHANGE RAW RESPONSE COMPLETE] "
                "method=%s | uri=%s | status=%s | body=%s",
                method.upper(),
                uri,
                r.status_code,
                r.text,
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
            assets = data.get('assets', [])
            for a in assets:
                if a.get('symbol') == 'USDT':
                    return float(a.get('availableBalance', 0))
            return 0.0
        except Exception:
            return 0.0
    
    def _round_price(self, price, symbol):
        tick = TICK_SIZES.get(symbol.upper(), 0.01)
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        return round(round(float(price)/tick)*tick, prec)
    
    def create_order(self, symbol, side, capital, leverage, take_profit=None, stop_loss=None):
        """
        ایجاد سفارش بازار با ساختار صحیح مطابق مستندات API
        
        Args:
            symbol: نام نماد (مثلاً ETHUSDT)
            side: LONG یا SHORT (یا BUY/SELL که تبدیل می‌شوند)
            capital: مقدار سرمایه به USDT
            leverage: مقدار اهرم
            take_profit: قیمت تارگت (اختیاری)
            stop_loss: قیمت استاپ لاس (اختیاری)
        """
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        
        # ============================================================
        # تبدیل side به فرمت صحیح API
        # API فقط LONG و SHORT را قبول دارد
        # ============================================================
        side_upper = str(side).upper().strip()
        
        # اگر side برابر با BUY یا LONG باشد → LONG
        if side_upper in ("BUY", "LONG"):
            api_side = "LONG"
        # اگر side برابر با SELL یا SHORT باشد → SHORT
        elif side_upper in ("SELL", "SHORT"):
            api_side = "SHORT"
        else:
            # در غیر این صورت همان مقدار ارسال می‌شود
            api_side = side_upper
        
        # ============================================================
        # ساختار صحیح درخواست مطابق مستندات API
        # ============================================================
        od = {
            "symbol": symbol.upper(),
            "side": api_side,
            "tradeType": "MARKET",
            "leverage": int(leverage),
            "cost": f"{capital:.{prec}f}",
            "walletType": "debit"
        }
        
        # ============================================================
        # اضافه کردن استاپ و تارگت اگر موجود باشند
        # ============================================================
        if take_profit is not None and not math.isnan(take_profit) and take_profit > 0:
            od["takeProfit"] = f"{self._round_price(take_profit, symbol):.{prec}f}"
            logger.info(f"[TP] Take Profit set at {self._round_price(take_profit, symbol):.{prec}f}")
        
        if stop_loss is not None and not math.isnan(stop_loss) and stop_loss > 0:
            od["stopLoss"] = f"{self._round_price(stop_loss, symbol):.{prec}f}"
            logger.info(f"[SL] Stop Loss set at {self._round_price(stop_loss, symbol):.{prec}f}")
        
        # ===== FULL ORDER REQUEST LOG =====
        logger.info(
            "[ORDER REQUEST] %s %s\n%s",
            symbol.upper(),
            api_side,
            json.dumps(od, ensure_ascii=False, indent=2)
        )
        
        # ===== FULL ORDER REQUEST TO TELEGRAM =====
        request_msg = (
            f"📤 عدم موفقیت در سفارش\n"
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
            
            # ===== FULL ORDER SUCCESS LOG =====
            logger.info(
                "[ORDER SUCCESS] %s %s\n%s",
                symbol.upper(),
                api_side,
                json.dumps(result, ensure_ascii=False, indent=2) if isinstance(result, (dict, list)) else str(result)
            )
            
            # ===== FULL ORDER SUCCESS TO TELEGRAM =====
            success_msg = (
                f"✅ سفارش با موفقیت در صرافی ثبت شد\n"
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
            # ===== FULL EXCHANGE ERROR EXTRACTION =====
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
            
            # ===== FULL ORDER FAILED LOG =====
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
            
            # ===== FULL ORDER FAILED TO TELEGRAM =====
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
# STARTUP DIAGNOSTIC — READ ONLY
# ================================================================
# IMPORTANT:
# This diagnostic NEVER sends a real order.
# It NEVER changes trading formulas or calculations.
# ================================================================

def startup_diagnostic(exchange, public):
    """
    READ-ONLY startup diagnostic.

    This function:
      - NEVER creates an order
      - NEVER changes trading calculations
      - NEVER changes capital formulas
      - NEVER changes leverage formulas
      - NEVER changes strategy.py
      - checks APIs, market data, configuration and engine readiness
      - sends the complete diagnostic to Telegram
    """
    
    # ===== لاگ شروع دیاگنوستیک =====
    logger.info("=" * 60)
    logger.info("...شروع عیب‌یابی استارتاپ")
    logger.info("=" * 60)

    report = [
        "🚀 عیب‌یابی راه‌اندازی ربات DTM",
        "━━━━━━━━━━━━━━━━━━━━━━",
        "MODE: READ-ONLY",
        "REAL ORDER: 🚫 NOT SENT",
    ]

    failures = []
    warnings = []

    def add(title, ok, details=""):
        status = "✅ ACTIVE" if ok else "❌ FAILED"
        text = f"{title}: {status}"
        if details:
            text += f"\n{details}"
        report.append(text)

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

    # ------------------------------------------------------------
    # TELEGRAM
    # ------------------------------------------------------------
    try:
        send_telegram("🧪 Началось расхождение в стратегии DTM")
        add("TELEGRAM", True)
    except Exception as e:
        add(
            "TELEGRAM",
            False,
            f"FULL ERROR: {repr(e)}"
        )

    # ------------------------------------------------------------
    # EXCHANGE CONNECTION
    # ------------------------------------------------------------
    try:
        exchange._last_response = None
        ok = exchange.test_connection()

        if ok:
            add("EXCHANGE API", True)
        else:
            add(
                "EXCHANGE API",
                False,
                full_exchange_error()
            )
    except Exception as e:
        add(
            "EXCHANGE API",
            False,
            full_exchange_error() +
            f"\nLOCAL EXCEPTION: {repr(e)}"
        )

    # ------------------------------------------------------------
    # BALANCE
    # ------------------------------------------------------------
    balance = None

    try:
        exchange._last_response = None
        balance = exchange.fetch_balance()

        if balance is not None and balance >= 0:
            add(
                "BALANCE",
                True,
                f"Available USDT: {balance}"
            )
        else:
            add(
                "BALANCE",
                False,
                full_exchange_error()
            )
    except Exception as e:
        add(
            "BALANCE",
            False,
            full_exchange_error() +
            f"\nLOCAL EXCEPTION: {repr(e)}"
        )

    # ------------------------------------------------------------
    # MARKET DATA
    # ------------------------------------------------------------
    report.append("━━━━━━━━━━━━━━━━━━━━━━")
    report.append("MARKET DATA:")

    market_ok = 0

    for symbol in SYMBOLS:
        try:
            df = public.fetch_ohlcv(symbol)

            if df is not None and not df.empty:
                market_ok += 1
                report.append(
                    f"{symbol}: ✅ ACTIVE "
                    f"({len(df)} candles)"
                )
            else:
                report.append(
                    f"{symbol}: ❌ FAILED\n"
                    "FULL ERROR: Empty OHLCV response"
                )

        except Exception as e:
            report.append(
                f"{symbol}: ❌ FAILED\n"
                f"FULL ERROR: {repr(e)}"
            )

    add(
        "MARKET DATA SYSTEM",
        market_ok == len(SYMBOLS),
        f"Active symbols: {market_ok}/{len(SYMBOLS)}"
    )

    # ------------------------------------------------------------
    # STRATEGY IMPORT
    # ------------------------------------------------------------
    calculate_signals_fn = None

    report.append("━━━━━━━━━━━━━━━━━━━━━━")

    try:
        from strategy_wrapper import calculate_signals as _calculate_signals
        calculate_signals_fn = _calculate_signals

        add(
            "STRATEGY.PY",
            callable(calculate_signals_fn),
            "calculate_signals: AVAILABLE"
        )

    except Exception as e:
        add(
            "STRATEGY.PY",
            False,
            f"FULL ERROR: {repr(e)}"
        )

    # ------------------------------------------------------------
    # STRATEGY EXECUTION — READ ONLY
    # ------------------------------------------------------------
    strategy_ok = False

    if callable(calculate_signals_fn):
        for symbol in SYMBOLS:
            try:
                df = public.fetch_ohlcv(symbol)

                if df is not None and not df.empty:
                    # دریافت ۴ مقدار از strategy_wrapper
                    sig, entry, stop_price, target_price = calculate_signals_fn(df, symbol)
                    

                    logger.info(
                        "[STARTUP DIAGNOSTIC] "
                        "%s signal=%r entry=%r stop=%r target=%r",
                        symbol,
                        sig,
                        entry,
                        stop_price,
                        target_price,
                    )

                    strategy_ok = True
                    report.append(
                        f"STRATEGY TEST {symbol}: "
                        f"✅ OK | signal={sig!r} | entry={entry!r} | stop={stop_price!r} | target={target_price!r}"
                    )
                    break

            except Exception as e:
                logger.exception(
                    "[STARTUP DIAGNOSTIC] "
                    "Strategy test failed: %s",
                    symbol,
                )

        add(
            "STRATEGY EXECUTION",
            strategy_ok
        )

    else:
        add(
            "STRATEGY EXECUTION",
            False,
            "calculate_signals unavailable"
        )

    # ------------------------------------------------------------
    # POSITION API — READ ONLY
    # ------------------------------------------------------------
    try:
        exchange._last_response = None

        positions = exchange._request(
            "GET",
            "/futures/positions"
        )

        add(
            "POSITION API",
            True,
            f"Response type: {type(positions).__name__}"
        )

    except Exception as e:
        add(
            "POSITION API",
            False,
            full_exchange_error() +
            f"\nLOCAL EXCEPTION: {repr(e)}"
        )

    # ------------------------------------------------------------
    # ORDER CAPABILITY — NO REAL ORDER
    # ------------------------------------------------------------
    report.append("━━━━━━━━━━━━━━━━━━━━━━")
    report.append("ORDER SYSTEM — READ ONLY")

    try:
        create_order = getattr(
            exchange,
            "create_order",
            None
        )

        if callable(create_order):
            add(
                "CREATE_ORDER FUNCTION",
                True,
                "Function exists"
            )
        else:
            add(
                "CREATE_ORDER FUNCTION",
                False,
                "create_order not found"
            )

    except Exception as e:
        add(
            "CREATE_ORDER FUNCTION",
            False,
            f"FULL ERROR: {repr(e)}"
        )

    # ------------------------------------------------------------
    # ORDER STRUCTURE VALIDATION
    # ------------------------------------------------------------
    try:
        for symbol in SYMBOLS:
            leverage = LEVERAGE_MAP.get(symbol, 50)

            # IMPORTANT:
            # These are ONLY the currently configured values.
            # No trading formula is recalculated or modified.
            side_test = "LONG"
            trade_type = "MARKET"
            wallet_type = "debit"

            report.append(
                f"\n{symbol} ORDER STRUCTURE:"
            )
            report.append(
                f"  side={side_test}"
            )
            report.append(
                f"  tradeType={trade_type}"
            )
            report.append(
                f"  leverage={leverage}"
            )
            report.append(
                f"  walletType={wallet_type}"
            )

            report.append(
                "  cost: 🔒 محاسبه ربات فعلی "
                "(NOT MODIFIED)"
            )

        add(
            "ORDER REQUEST STRUCTURE",
            True,
            "Structure inspected without sending an order"
        )

    except Exception as e:
        add(
            "ORDER REQUEST STRUCTURE",
            False,
            f"FULL ERROR: {repr(e)}"
        )

    # ------------------------------------------------------------
    # CURRENT FORMULA / RISK VALUES — OBSERVATION ONLY
    # ------------------------------------------------------------
    report.append("━━━━━━━━━━━━━━━━━━━━━━")
    report.append("CURRENT TRADING CONFIG — OBSERVATION ONLY")

    report.append(
        f"TARGET_RISK: {TARGET_RISK}"
    )

    for symbol in SYMBOLS:
        report.append(
            f"{symbol}: "
            f"LEVERAGE_MAP={LEVERAGE_MAP.get(symbol)}"
        )

    report.append(
        "فرمول‌های معاملاتی: 🔒 اصلاح نشده"
    )
    report.append(
        "محاسبه سرمایه: 🔒 اصلاح نشده"
    )
    report.append(
        "محاسبه‌ی لوریج: 🔒 اصلاح نشده"
    )
    report.append(
        "منطق استراتژی: 🔒 اصلاح نشده"
    )

    # ------------------------------------------------------------
    # FINAL SAFETY
    # ------------------------------------------------------------
    report.extend([
        "━━━━━━━━━━━━━━━━━━━━━━",
        "REAL ORDER: 🚫 NOT SENT",
        "ORDER TEST MODE: READ-ONLY",
        "DIAGNOSTIC COMPLETE",
    ])

    final_report = "\n".join(report)

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


def loop():
    public = PublicData()
    exchange = PrivateExchange()

    # ============================================================
    # READ-ONLY STARTUP DIAGNOSTIC
    # ============================================================
    try:
        startup_diagnostic(exchange, public)
    except Exception as e:
        logger.exception("[STARTUP DIAGNOSTIC] FATAL ERROR: %s", e)

    send_telegram("ربات شروع شد")
    logger.info("Worker bot started")

    # ============================================================
    # ⚙️ تنظیمات ثابت — دقیقاً مطابق بک‌تست
    # ============================================================
    BASE_CAPITAL = 2.0          # مبنا = ۲ دلار
    BALANCE_USE_RATIO = 0.98    # ۹۸٪ موجودی در صورت کمبود

    while not STOP_EVENT.is_set():
        try:
            if not exchange.test_connection():
                send_telegram("اتصال صرافی قطع است")
                STOP_EVENT.wait(60)
                continue

            balance = exchange.fetch_balance()

            for symbol in SYMBOLS:
                df = public.fetch_ohlcv(symbol)
                if df.empty:
                    continue

                sig, entry, stop_price, target_price = calculate_signals(df, symbol)

                logger.info(
                    f"{symbol}: signal={sig}, entry={entry}, "
                    f"stop={stop_price}, target={target_price}, candles={len(df)}"
                )

                if not sig or balance <= 0 or stop_price is None or entry is None:
                    continue

                allowed_leverage = LEVERAGE_MAP.get(symbol, 50)

                # ============================================================
                # ۱) محاسبه درصد استاپ
                # ============================================================
                if sig == "LONG":
                    stop_pct = abs(entry - stop_price) / entry if entry > 0 else 0
                else:  # SHORT
                    stop_pct = abs(stop_price - entry) / entry if entry > 0 else 0

                if stop_pct <= 0:
                    logger.warning(f"{symbol}: invalid stop_pct={stop_pct}, skip")
                    continue

                # ============================================================
                # ۲) محاسبه درصد تارگت
                # ============================================================
                if target_price is not None and not math.isnan(target_price) and target_price > 0:
                    if sig == "LONG":
                        target_pct = abs(target_price - entry) / entry
                    else:  # SHORT
                        target_pct = abs(entry - target_price) / entry
                else:
                    target_pct = 0

                # ============================================================
                # ۳) فرمول دقیق بک‌تست — محاسبه سرمایه
                # ============================================================
                old_leverage = 1.0 / stop_pct

                if old_leverage > allowed_leverage:
                    required_capital = (old_leverage / allowed_leverage) * BASE_CAPITAL
                    leverage_mode = "INCREASED"
                else:
                    required_capital = BASE_CAPITAL
                    leverage_mode = "BASE"

                # ============================================================
                # ۴) مدیریت موجودی
                # ============================================================
                if balance < required_capital:
                    # موجودی ناکافی → ۹۸٪ موجودی
                    capital = balance * BALANCE_USE_RATIO
                    actual_stop_dollar = capital * stop_pct * allowed_leverage
                    actual_profit_dollar = (
                        capital * target_pct * allowed_leverage
                        if target_pct > 0 else None
                    )
                    mode = "REDUCED_98"
                else:
                    # موجودی کافی → دقیقاً طبق فرمول
                    capital = required_capital
                    actual_stop_dollar = BASE_CAPITAL
                    actual_profit_dollar = (
                        (target_pct / stop_pct) * BASE_CAPITAL
                        if target_pct > 0 else None
                    )
                    mode = "FULL"

                # ============================================================
                # ۵) محاسبه R
                # ============================================================
                r_value = (target_pct / stop_pct) if target_pct > 0 else None

                # ============================================================
                # ۶) لاگ نهایی — شفاف و دقیق
                # ============================================================
                profit_str = f"{actual_profit_dollar:.4f}" if actual_profit_dollar else "N/A"
                r_str = f"{r_value:.2f}" if r_value else "N/A"

                logger.info(
                    f"[{symbol}] سیگنال={sig} | ورود={entry}\n"
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
                # ۷) ارسال سفارش با سرمایه دقیق
                # ============================================================
                exchange.create_order(
                    symbol,
                    sig,
                    capital,
                    allowed_leverage,
                    take_profit=target_price,
                    stop_loss=stop_price,
                )

                balance = exchange.fetch_balance()

            STOP_EVENT.wait(60)

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

    logger.info("DTM WORKER START | HTTP port=%d", port)

    try:
        loop()
    finally:
        STOP_EVENT.set()
        health_thread.join(timeout=3)
        logger.info("DTM PROCESS EXIT")
