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
from strategy_wrapper import calculate_signals, SYMBOL_TICK_INFO
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
