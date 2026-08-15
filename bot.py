import os
import time
import hmac
import hashlib
import logging
import requests
import pandas as pd
from strategy import calculate_signals

API_KEY = os.getenv("API_KEY", "pXJ3uOI3y7iPHxIgefQJ30PikXHqbQyVV9Ouj-_K")
API_SECRET = os.getenv("API_SECRET", "4cd23e00385ea761250034b420c86f40c4edb8e27c285c21572dbadf7e927b09")
BASE_URL = os.getenv("BASE_URL", "https://apiv2.thetruetrade.io")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")
SYMBOLS = ["LTCUSDT", "DOGEUSDT", "ETHUSDT"]
HISTORY_BARS = 500
LEVERAGE_MAP = {"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50}
TARGET_RISK = 2.0
TICK_SIZES = {"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01}
PRICE_PRECISION = {"LTCUSDT": 2, "DOGEUSDT": 5, "ETHUSDT": 2}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BOT")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=15)
    except Exception as e:
        logger.error(f"Telegram error: {e}")

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
            o = data['o']; h = data['h']; l = data['l']; c = data['c']
            return pd.DataFrame({'open': o, 'high': h, 'low': l, 'close': c},
                                index=pd.to_datetime(t, unit='s', utc=True)).tail(HISTORY_BARS)
        except Exception as e:
            logger.error(f"Data error: {e}")
            return pd.DataFrame()

class PrivateExchange:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.base = BASE_URL
        self.session = requests.Session()
    def _sign(self, method, uri, ts):
        payload = f"{ts}{method.upper()}{uri}"
        return hmac.new(self.api_secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    def _request(self, method, uri, data=None):
        ts = str(int(time.time()*1000))
        sig = self._sign(method, uri, ts)
        headers = {"X-API-Key": self.api_key, "X-Timestamp": ts, "X-Signature": sig, "Content-Type": "application/json"}
        r = self.session.request(method, f"{self.base}{uri}", headers=headers, json=data, timeout=15)
        if not r.ok:
            r.raise_for_status()
        return r.json()
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
    def create_order(self, symbol, side, capital, leverage):
        prec = PRICE_PRECISION.get(symbol.upper(), 2)
        od = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "tradeType": "MARKET",
            "leverage": leverage,
            "cost": f"{capital:.{prec}f}",
            "walletType": "debit"
        }
        send_telegram(f"📤 ثبت سفارش {symbol} {side} اهرم {leverage} | هزینه {capital:.{prec}f}")
        try:
            result = self._request("POST", "/futures/positions", od)
            send_telegram(f"📥 سفارش ثبت شد {symbol} {side}")
            return result
        except Exception as e:
            send_telegram(f"❌ خطای سفارش {symbol} {side}\n{e}")
            return None

def loop():
    public = PublicData()
    exchange = PrivateExchange()
    send_telegram("ربات شروع شد")
    logger.info("Worker bot started")
    while True:
        try:
            if not exchange.test_connection():
                send_telegram("اتصال صرافی قطع است")
                time.sleep(60)
                continue
            balance = exchange.fetch_balance()
            for symbol in SYMBOLS:
                df = public.fetch_ohlcv(symbol)
                if df.empty:
                    continue
                sig, entry = calculate_signals(df)
                logger.info(f"{symbol}: signal={sig}, entry={entry}, candles={len(df)}")
                if sig and balance > 0:
                    leverage = LEVERAGE_MAP.get(symbol, 50)
                    capital = min(balance * 0.98, TARGET_RISK)
                    exchange.create_order(symbol, sig, capital, leverage)
                    balance = exchange.fetch_balance()
            time.sleep(60)
        except Exception as e:
            logger.error(f"Loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    loop()
