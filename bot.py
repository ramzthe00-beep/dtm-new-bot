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
LEVERAGE_MAP = {"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50}
HISTORY_BARS = 500

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BOT")

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
            t = data['t']; o = data['o']; h = data['h']; l = data['l']; c = data['c']
            return pd.DataFrame({'open': o, 'high': h, 'low': l, 'close': c}, index=pd.to_datetime(t, unit='s', utc=True)).tail(HISTORY_BARS)
        except Exception as e:
            logger.error(f"Data error: {e}")
            return pd.DataFrame()

def loop():
    public = PublicData()
    while True:
        try:
            for symbol in SYMBOLS:
                df = public.fetch_ohlcv(symbol)
                if df.empty:
                    continue
                sig, entry = calculate_signals(df)
                logger.info(f"{symbol}: signal={sig}, entry={entry}, candles={len(df)}")
            time.sleep(60)
        except Exception as e:
            logger.error(f"Loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    loop()
