# -*- coding: utf-8 -*-
"""
backtest_report.py  (نسخه v5 — موتور پیوسته + فیلتر پنجره‌ی لایو)
=================================================================
بک‌تست مستقل استراتژی DTM روی داده‌های واقعی Binance Spot + گزارش کامل و تفکیکی
به تلگرام.

معماری این نسخه (و چرا):
------------------------
• موتور سیگنال = «پاس پیوسته» (یک ScriptRunner روی کل تاریخچه) — همان موتوری که
  گزارش‌های درست و منطقی می‌داد — به‌علاوه‌ی «فیلتر پنجره‌ی لایو»:
  سیگنالی که پیوت‌های استاپ/تارگتش قدیمی‌تر از پنجره‌ی ~۵۰۰کندلی لایو باشد،
  حذف می‌شود؛ چون bot.py در لایو فقط آخرین ۵۰۰ کندل را می‌بیند و سیگنالی با
  پیوت قدیمی‌تر هرگز تولید نمی‌شد. (این مهم‌ترین اختلاف پاس پیوسته با لایو بود.)
• موتور exact (پنجره‌ی سرد برای هر کندل) هم حفظ شده ولی دیگر پیش‌فرض نیست و
  باگ ایندکس پیوت‌هایش (فضای محلی پنجره در برابر فضای کلی آرایه) رفع شد.
• 🛡️ excepthook: هر خطای پیش‌بینی‌نشده هم به تلگرام می‌رسد (دیگر صفرِ بی‌صدا وجود ندارد).
• 🎯 نمونه‌گیری کنترلی (--verify-sample): هر N-مین کندلِ غیرکاندید با پنجره‌ی سرد
  چک می‌شود تا نرخ سیگنال‌های جاافتاده‌ی پاس پیوسته تخمین و در گزارش بیاید.

• هیچ دست‌زدنی به bot.py / trade_ledger.jsonl ندارد و سفارشی روی صرافی ثبت نمی‌کند.
• سیگنال‌ها: عیناً strategy.py از طریق PyneCore ScriptRunner.
• استاپ/تارگت: عیناً همان _compute_stop_target در strategy_wrapper (تیک از wrapper).
• PnL و شبیه‌سازی ریسک‌فری: عیناً همان فرمول trade_ledger (سرمایه پایه ۲$، استاپ
  برنده در همان کندل اگر هم استاپ هم تارگت لمس شدند).

اجرا:
    python backtest_report.py                        → گزارش کامل ۶۰ روزه (موتور پیش‌فرض)
    python backtest_report.py --mode both            → گزارش کامل + تفکیک هر ارز/تایم‌فریم
    python backtest_report.py --days 365             → بازه ۱ ساله
    python backtest_report.py --tfs 1 5 15 30 60 240 → تایم‌فریم‌های دلخواه
    python backtest_report.py --window-clamp 0       → خاموش‌کردن فیلتر پنجره (رفتار v1 خام)
    python backtest_report.py --verify-sample 100    → نمونه‌گیری کنترلی (هر ۱۰۰ کندل)
    python backtest_report.py --engine exact         → پنجره سرد برای هر کندل (خیلی کند)
    python backtest_report.py --account-sim 50       → شبیه‌سازی با موجودی واقعی
    python backtest_report.py --signal-dump 5000     → ارسال فایل کامل سیگنال‌های اخیر به تلگرام
    python backtest_report.py --force                → نادیده‌گرفتن قفل روزانه
    python backtest_report.py --resend               → ارسال مجدد از نتایج ذخیره‌شده
    python backtest_report.py --no-send              → فقط چاپ/ذخیره، بدون تلگرام
"""

import os
import sys
import json
import math
import time
import argparse
import logging
import traceback
import multiprocessing as mp
from pathlib import Path
from datetime import datetime, timedelta, timezone
from concurrent.futures import ProcessPoolExecutor, as_completed

import requests
import pandas as pd

# ============================================================
# مسیرها و ثابت‌ها
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
STRATEGY_PATH = BASE_DIR / "strategy.py"
RESULTS_PATH = BASE_DIR / "backtest_results.json"
MARKER_PATH = BASE_DIR / "backtest_report_state.json"
TICK_CACHE_PATH = BASE_DIR / "backtest_tick_cache.json"

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7402770612")

# ------------------------------------------------------------------
# مقادیر پیش‌فرض محلی — دقیقاً کپیِ فعلیِ bot.py. اگر پایین‌تر وارد کردن
# مستقیم از bot.py موفق شود، همه‌ی این‌ها با مقادیر واقعیِ زنده جایگزین
# می‌شوند تا هرگز دو منبعِ ناهماهنگ نداشته باشیم.
# ------------------------------------------------------------------
SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SUIUSDT", "DASHUSDT",
    "BTWUSDT", "ARBUSDT", "ZECUSDT", "HYPEUSDT", "BCHUSDT",
    "AAVEUSDT", "ENAUSDT", "1000PEPEUSDT", "CAKEUSDT", "ASTERUSDT",
    "UNIUSDT", "LINKUSDT", "1000SHIBUSDT", "SOLUSDT", "XLMUSDT",
    "TUTUSDT", "DOGEUSDT", "XRPUSDT", "PUMPUSDT", "WLDUSDT",
    "ETCUSDT", "LTCUSDT", "APTUSDT", "HBARUSDT", "VERSOUSDT",
    "INJUSDT", "AVAXUSDT", "NOTUSDT", "NEARUSDT", "TRUMPUSDT",
    "QNTUSDT", "PAXGUSDT", "ONDOUSDT", "KSMUSDT", "ADAUSDT",
    "SANDUSDT", "FILUSDT", "BMTUSDT", "OPUSDT", "KAITOUSDT",
    "FETUSDT", "ICPUSDT", "TRXUSDT", "BANDUSDT", "ATOMUSDT",
    "ALGOUSDT", "GRAMUSDT", "DOTUSDT", "APEUSDT"
]

TIMEFRAMES = ["1", "5", "15", "30", "60", "240"]

LEVERAGE_MAP = {
    "BTCUSDT": 150, "ETHUSDT": 50, "BNBUSDT": 75, "SUIUSDT": 75,
    "DASHUSDT": 50, "BTWUSDT": 10, "ARBUSDT": 75, "ZECUSDT": 50,
    "HYPEUSDT": 75, "BCHUSDT": 75, "AAVEUSDT": 75, "ENAUSDT": 75,
    "1000PEPEUSDT": 75, "CAKEUSDT": 50, "ASTERUSDT": 50,
    "UNIUSDT": 75, "LINKUSDT": 75, "1000SHIBUSDT": 75,
    "SOLUSDT": 100, "XLMUSDT": 75, "TUTUSDT": 10,
    "DOGEUSDT": 75, "XRPUSDT": 75, "PUMPUSDT": 75,
    "WLDUSDT": 75, "ETCUSDT": 75, "LTCUSDT": 75,
    "APTUSDT": 75, "HBARUSDT": 75, "VERSOUSDT": 75,
    "INJUSDT": 75, "AVAXUSDT": 75, "NOTUSDT": 75,
    "NEARUSDT": 75, "TRUMPUSDT": 75, "QNTUSDT": 75,
    "PAXGUSDT": 75, "ONDOUSDT": 75, "KSMUSDT": 50,
    "ADAUSDT": 75, "SANDUSDT": 75, "FILUSDT": 75,
    "BMTUSDT": 20, "OPUSDT": 75, "KAITOUSDT": 75,
    "FETUSDT": 75, "ICPUSDT": 75, "TRXUSDT": 75,
    "BANDUSDT": 50, "ATOMUSDT": 75, "ALGOUSDT": 75,
    "GRAMUSDT": 75, "DOTUSDT": 50, "APEUSDT": 75,
}

TICK_SIZES = {
    "BTCUSDT": 0.1, "ETHUSDT": 0.01, "BNBUSDT": 0.01,
    "SUIUSDT": 0.0001, "DASHUSDT": 0.01, "BTWUSDT": 0.00001,
    "ARBUSDT": 0.0001, "ZECUSDT": 0.01, "HYPEUSDT": 0.001,
    "BCHUSDT": 0.01, "AAVEUSDT": 0.01, "ENAUSDT": 0.00001,
    "1000PEPEUSDT": 0.0000001, "CAKEUSDT": 0.0001, "ASTERUSDT": 0.0001,
    "UNIUSDT": 0.001, "LINKUSDT": 0.001, "1000SHIBUSDT": 0.000001,
    "SOLUSDT": 0.01, "XLMUSDT": 0.00001, "TUTUSDT": 0.00001,
    "DOGEUSDT": 0.00001, "XRPUSDT": 0.0001, "PUMPUSDT": 0.000001,
    "WLDUSDT": 0.0001, "ETCUSDT": 0.001, "LTCUSDT": 0.01,
    "APTUSDT": 0.0001, "HBARUSDT": 0.00001, "VERSOUSDT": 0.00001,
    "INJUSDT": 0.001, "AVAXUSDT": 0.001, "NOTUSDT": 0.000001,
    "NEARUSDT": 0.001, "TRUMPUSDT": 0.001, "QNTUSDT": 0.01,
    "PAXGUSDT": 0.01, "ONDOUSDT": 0.0001, "KSMUSDT": 0.01,
    "ADAUSDT": 0.0001, "SANDUSDT": 0.00001, "FILUSDT": 0.001,
    "BMTUSDT": 0.00001, "OPUSDT": 0.0001, "KAITOUSDT": 0.0001,
    "FETUSDT": 0.0001, "ICPUSDT": 0.01, "TRXUSDT": 0.00001,
    "BANDUSDT": 0.001, "ATOMUSDT": 0.001, "ALGOUSDT": 0.0001,
    "GRAMUSDT": 0.001, "DOTUSDT": 0.001, "APEUSDT": 0.0001,
}

HISTORY_BARS = 500          # عیناً bot.py — طول پنجره‌ی غلتانِ لایو
MIN_ORDER_COST_USDT = 5.0   # عیناً bot.py (پیش‌فرض؛ ممکن است در Railway override شده باشد)
LIVE_BASE_CAPITAL = 1.5     # عیناً مقدار محلیِ BASE_CAPITAL داخل loop() در bot.py
LIVE_BALANCE_USE_RATIO = 0.70

BASE_CAPITAL = 2.0          # سرمایه‌ی پایه‌ی فرمول PnL فرضی — عیناً trade_ledger.BASE_CAPITAL
DAYS_DEFAULT = 365          # 🔴 تغییر از ۶۰ به ۳۶۵ (۱ سال)
BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]
KLINE_LIMIT = 1000
REQUEST_SLEEP = 0.15
MAX_FETCH_ITER = 20000       # سقف ایمنی برای حلقه‌ی صفحه‌بندی (جلوگیری از حلقه‌ی بی‌نهایت)

# mintick fallback عمومی — فقط وقتی نماد نه در دیکشنری دستی است و نه از
# Binance قابل کشف. دیگر به‌صورت خاموش استفاده نمی‌شود؛ همیشه لاگ/هشدار می‌دهد.
GENERIC_FALLBACK_TICK = 0.0001

# ورودی‌های استراتژی — عیناً همان مقادیر strategy_wrapper
STRATEGY_INPUTS = {
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

# ============================================================
# 🆕 تنظیمات Pivot Mode بر اساس تایم‌فریم
# ============================================================
PIVOT_MODE_BY_TIMEFRAME = {
    "1": "سریع (5/3)",      # ۱ دقیقه → سریع
    "5": "سریع (5/3)",      # ۵ دقیقه → سریع
    "15": "استاندارد (5/5)", # ۱۵ دقیقه → استاندارد
    "30": "استاندارد (5/5)", # ۳۰ دقیقه → استاندارد
    "60": "استاندارد (5/5)", # ۱ ساعت → استاندارد
    "240": "استاندارد (5/5)",# ۴ ساعت → استاندارد
}

# ============================================================
# 🆕 تابع دریافت ورودی‌های استراتژی بر اساس تایم‌فریم
# ============================================================
def get_strategy_inputs(timeframe):
    """برگرداندن ورودی‌های استراتژی با pivotMode مخصوص تایم‌فریم"""
    base = dict(STRATEGY_INPUTS)
    base["pivotMode"] = PIVOT_MODE_BY_TIMEFRAME.get(str(timeframe), "سریع (5/3)")
    return base


SCORE_KEYS = {
    "CD-": "score_classic_bearish",
    "CD+": "score_classic_bullish",
    "HD+": "score_hidden_bullish",
    "HD-": "score_hidden_bearish",
}
WD_FA = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
W = "━━━━━━━━━━━━━━━━━━━━"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BACKTEST")

# ============================================================
# تلاش برای وارد کردن ثابت‌های واقعیِ لایو مستقیماً از bot.py
# ============================================================
try:
    logging.disable(logging.CRITICAL)
    import bot as _bot_module
    # فقط SYMBOLS و TIMEFRAMES و LEVERAGE_MAP را از bot.py بگیر
    # اما SYMBOLS/TIMEFRAMES ما قبلاً تنظیم شده، فقط در صورت لزوم
    _bot_symbols = getattr(_bot_module, "SYMBOLS", None)
    if _bot_symbols:
        # فقط ارزهایی که در bot.py هستند را نگه دار، اما ارزهای جدید را هم اضافه کن
        existing = set(SYMBOLS)
        new_from_bot = [s for s in _bot_symbols if s not in existing]
        if new_from_bot:
            SYMBOLS.extend(new_from_bot)
            logger.info(f"[BOT] ارزهای جدید از bot.py اضافه شد: {new_from_bot}")
    
    _bot_tfs = getattr(_bot_module, "TIMEFRAMES", None)
    if _bot_tfs:
        existing_tfs = set(TIMEFRAMES)
        new_tfs = [t for t in _bot_tfs if t not in existing_tfs]
        if new_tfs:
            TIMEFRAMES.extend(new_tfs)
            TIMEFRAMES = sorted(TIMEFRAMES, key=lambda x: int(x))
            logger.info(f"[BOT] تایم‌فریم‌های جدید از bot.py اضافه شد: {new_tfs}")
    
    _bot_leverage = getattr(_bot_module, "LEVERAGE_MAP", None)
    if _bot_leverage:
        for k, v in _bot_leverage.items():
            if k not in LEVERAGE_MAP:
                LEVERAGE_MAP[k] = v
    
    _bot_tick = getattr(_bot_module, "TICK_SIZES", None)
    if _bot_tick:
        for k, v in _bot_tick.items():
            if k not in TICK_SIZES:
                TICK_SIZES[k] = v
    
    HISTORY_BARS = int(getattr(_bot_module, "HISTORY_BARS", HISTORY_BARS))
    MIN_ORDER_COST_USDT = float(getattr(_bot_module, "MIN_ORDER_COST_USDT", MIN_ORDER_COST_USDT))
    CONST_SOURCE = "bot.py (زنده)"
except Exception as e:
    CONST_SOURCE = f"مقادیر محلی (import bot.py ناموفق: {e})"
finally:
    logging.disable(logging.NOTSET)

# SYMBOL_TICK_INFO برای strategy_wrapper (mintick/pricescale/basecurrency)
def _tick_to_pricescale(tick):
    try:
        return max(1, round(1.0 / float(tick)))
    except Exception:
        return 100


SYMBOL_TICK_INFO = {
    sym: {"mintick": tick, "pricescale": _tick_to_pricescale(tick), "basecurrency": sym.replace("USDT", "")}
    for sym, tick in TICK_SIZES.items()
}


# ============================================================
# ابزارهای ایمن
# ============================================================
def _f(x):
    try:
        if x is None:
            return None
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except (TypeError, ValueError):
        return None


def _ms_to_iran(ms):
    try:
        return datetime.fromtimestamp(int(ms) / 1000.0, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception:
        return None


def now_iran_str():
    return datetime.now(UTC_TZ).astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")


def today_str():
    return datetime.now(UTC_TZ).astimezone(IRAN_TZ).strftime("%Y-%m-%d")


def _parse_kv_overrides(items):
    out = {}
    for it in items or []:
        if "=" not in it:
            continue
        k, v = it.split("=", 1)
        k = k.strip().upper()
        try:
            out[k] = float(v.strip())
        except ValueError:
            logger.warning(f"[ARGS] مقدار نامعتبر نادیده گرفته شد: {it}")
    return out


# ============================================================
# تلگرام
# ============================================================
def tg_send(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": str(text)}, timeout=30)
        return r.ok
    except Exception as e:
        logger.error(f"[TG] send error: {e}")
        return False


def tg_send_long(text):
    text = str(text)
    chunks = [text[i:i + 3900] for i in range(0, len(text), 3900)] or [text]
    ok = True
    for part in chunks:
        sent = False
        for attempt in range(3):
            if tg_send(part):
                sent = True
                break
            time.sleep(1 + attempt)
        if not sent:
            ok = False
        time.sleep(0.4)
    return ok


def tg_send_document(path, caption=""):
    """ارسال فایل به تلگرام (sendDocument) — هرگز Exception بالا نمی‌اندازد."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(path, "rb") as f:
            r = requests.post(
                url,
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": str(caption)[:1000]},
                files={"document": f},
                timeout=120,
            )
        return r.ok
    except Exception as e:
        logger.error(f"[TG] document error: {e}")
        return False


def _global_error_handler(exc_type, exc_value, exc_tb):
    """🛡️ تضمین: هر خطای پیش‌بینی‌نشده هم به تلگرام برسد."""
    try:
        tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        tg_send(f"❌ خطای پیش‌بینی‌نشده بک‌تست: {exc_type.__name__}: {exc_value}\n{tb_text}"[:3500])
    except Exception:
        pass


sys.excepthook = _global_error_handler


# ============================================================
# موتور استراتژی
# ============================================================
try:
    import strategy_wrapper as _sw
    try:
        _sw._send_telegram = lambda text: True
    except Exception:
        pass
    _compute_stop_target = _sw._compute_stop_target
    SYMBOL_TICK_INFO_FROM_WRAPPER = getattr(_sw, "SYMBOL_TICK_INFO", None)
    if SYMBOL_TICK_INFO_FROM_WRAPPER:
        merged = dict(SYMBOL_TICK_INFO)
        merged.update(SYMBOL_TICK_INFO_FROM_WRAPPER)
        SYMBOL_TICK_INFO = merged
    ENGINE_NAME = "strategy_wrapper (import شد)"
except Exception as e:
    logger.warning(f"[ENGINE] strategy_wrapper import نشد → fallback محلی: {e}")
    ENGINE_NAME = "fallback محلی"
    _sw = None

try:
    from pynecore.core.ohlcv import OHLCV
    from pynecore.core.syminfo import SymInfo, SymInfoInterval, SymInfoSession
    from pynecore.core.script_runner import ScriptRunner
except Exception as e:
    logger.error(f"[FATAL] pynecore در دسترس نیست: {e}")
    tg_send(f"❌ backtest_report: pynecore نصب نیست یا خراب است:\n{e}")
    sys.exit(1)


def _local_compute_stop_target(candles, signal, last_values, mintick, buffer_ticks=2):
    def _v(x):
        return x is not None and not (isinstance(x, float) and math.isnan(x))
    entry = last_values.get("entry")
    if not _v(entry):
        return None, None, None, None
    buffer_abs = buffer_ticks * mintick
    if signal == "LONG":
        low1 = last_values.get("previous_pivot_low_price")
        low2 = last_values.get("pivot_low_price")
        bar1 = last_values.get("previous_pivot_low_index")
        bar2 = last_values.get("pivot_low_index")
        if not (_v(low1) and _v(low2) and _v(bar1) and _v(bar2)):
            return None, None, None, None
        stop = min(low1, low2) - buffer_abs
        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None, None
        mid_peak = max(c.high for c in candles[lo:hi + 1])
        risk = entry - stop
        if risk <= 0:
            return None, None, None, None
        rr = (mid_peak - entry) / risk
        target = mid_peak if rr >= 2 else entry + 2 * risk
        return stop, target, max(rr, 2.0), mid_peak
    elif signal == "SHORT":
        high1 = last_values.get("previous_pivot_high_price")
        high2 = last_values.get("pivot_high_price")
        bar1 = last_values.get("previous_pivot_high_index")
        bar2 = last_values.get("pivot_high_index")
        if not (_v(high1) and _v(high2) and _v(bar1) and _v(bar2)):
            return None, None, None, None
        stop = max(high1, high2) + buffer_abs
        lo, hi = sorted((int(bar1), int(bar2)))
        lo, hi = max(lo, 0), min(hi, len(candles) - 1)
        if hi < lo:
            return None, None, None, None
        mid_trough = min(c.low for c in candles[lo:hi + 1])
        risk = stop - entry
        if risk <= 0:
            return None, None, None, None
        rr = (entry - mid_trough) / risk
        target = mid_trough if rr >= 2 else entry - 2 * risk
        return stop, target, max(rr, 2.0), mid_trough
    return None, None, None, None


if _sw is None:
    _compute_stop_target = _local_compute_stop_target

try:
    from trade_ledger import _hypothetical_pnl_usd as pnl_fn
    from trade_ledger import BASE_CAPITAL as _BC
    BASE_CAPITAL = float(_BC)
except Exception as e:
    logger.warning(f"[LEDGER] trade_ledger import نشد → فرمول محلی: {e}")

    def pnl_fn(direction, entry, initial_stop, exit_price, leverage):
        try:
            if not entry or not initial_stop or entry <= 0:
                return None, None
            stop_pct = abs(entry - initial_stop) / entry
            if stop_pct <= 0:
                return None, None
            move_pct = (exit_price - entry) / entry if direction == "LONG" else (entry - exit_price) / entry
            r_multiple = move_pct / stop_pct
            lev = leverage if (leverage and leverage > 0) else 50
            old_leverage = 1.0 / stop_pct
            capital = (old_leverage / lev) * BASE_CAPITAL if old_leverage > lev else BASE_CAPITAL
            return round(capital * lev * move_pct, 4), round(r_multiple, 4)
        except Exception:
            return None, None


def _build_syminfo(symbol, timeframe):
    tick = SYMBOL_TICK_INFO.get(
        symbol, {"mintick": GENERIC_FALLBACK_TICK, "pricescale": _tick_to_pricescale(GENERIC_FALLBACK_TICK),
                 "basecurrency": symbol.replace("USDT", "")}
    )
    return SymInfo(
        prefix="", description=f"{symbol} {timeframe}m", ticker=symbol,
        currency="USDT", basecurrency=tick["basecurrency"], period=str(timeframe),
        type="crypto", volumetype="base", mintick=tick["mintick"], pricescale=tick["pricescale"],
        minmove=1, pointvalue=1.0, mincontract=0.0,
        opening_hours=[SymInfoInterval(day=0, start=datetime.min.time(), end=datetime.max.time())],
        session_starts=[SymInfoSession(day=0, time=datetime.min.time())],
        session_ends=[SymInfoSession(day=0, time=datetime.max.time())],
        timezone="UTC",
    )


def buffer_ticks_for(symbol):
    if symbol in ("BNBUSDT", "ETHUSDT"):
        return 9
    if symbol in ("LTCUSDT", "DOGEUSDT"):
        return 3
    if symbol == "PUMPUSDT":
        return 1
    return 5


def compute_rf_pct(signal, entry, stop, structural_level):
    entry, stop = _f(entry), _f(stop)
    structural_level = _f(structural_level)
    if structural_level is None or stop is None or entry is None or entry <= 0:
        return None
    risk_pct = abs(entry - stop) / entry
    if signal == "LONG":
        return max((structural_level - entry) / entry, risk_pct)
    return -max((entry - structural_level) / entry, risk_pct)


def signal_type_of(lv):
    try:
        if lv.get("final_classic_bearish"):
            return "CD-"
        if lv.get("final_classic_bullish"):
            return "CD+"
        if lv.get("final_hidden_bullish"):
            return "HD+"
        if lv.get("final_hidden_bearish"):
            return "HD-"
    except Exception:
        pass
    return None


def _score_of(lv, st):
    if not st:
        return 0
    v = _f(lv.get(SCORE_KEYS.get(st, "")))
    if v is None:
        return 0
    return int(max(0, min(5, round(v))))


# ============================================================
# نگاشت دقیقه → interval رسمی بایننس
# ============================================================
_BINANCE_MINUTE_INTERVALS = {
    1: "1m", 3: "3m", 5: "5m", 15: "15m", 30: "30m",
    60: "1h", 120: "2h", 240: "4h", 360: "6h", 480: "8h", 720: "12h",
    1440: "1d", 4320: "3d", 10080: "1w",
}


def binance_interval_str(interval_min):
    m = int(interval_min)
    if m in _BINANCE_MINUTE_INTERVALS:
        return _BINANCE_MINUTE_INTERVALS[m]
    raise ValueError(
        f"تایم‌فریم {m} دقیقه توسط Binance پشتیبانی نمی‌شود. "
        f"مقادیر مجاز: {sorted(_BINANCE_MINUTE_INTERVALS.keys())}"
    )


# ============================================================
# کشف خودکار tick size از Binance
# ============================================================
_tick_cache_mem = None


def _load_tick_cache():
    global _tick_cache_mem
    if _tick_cache_mem is not None:
        return _tick_cache_mem
    try:
        _tick_cache_mem = json.loads(TICK_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        _tick_cache_mem = {}
    return _tick_cache_mem


def _save_tick_cache():
    try:
        TICK_CACHE_PATH.write_text(json.dumps(_tick_cache_mem or {}, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.warning(f"[TICK-CACHE] ذخیره ناموفق: {e}")


def discover_tick_size(symbol):
    cache = _load_tick_cache()
    if symbol in cache:
        return cache[symbol]
    for base in BINANCE_BASES:
        try:
            r = requests.get(f"{base}/api/v3/exchangeInfo", params={"symbol": symbol.upper()}, timeout=15)
            r.raise_for_status()
            data = r.json()
            symbols = data.get("symbols") or []
            if not symbols:
                continue
            filters = symbols[0].get("filters", [])
            for f_ in filters:
                if f_.get("filterType") == "PRICE_FILTER":
                    tick = float(f_.get("tickSize"))
                    if tick > 0:
                        cache[symbol] = tick
                        _save_tick_cache()
                        logger.info(f"[TICK-DISCOVER] {symbol}: tick واقعی از Binance = {tick}")
                        return tick
        except Exception as e:
            logger.warning(f"[TICK-DISCOVER] {symbol} @ {base} ناموفق: {e}")
            continue
    logger.error(
        f"⚠️ [TICK-DISCOVER] {symbol}: کشف خودکار tick ناموفق بود — از مقدار "
        f"پیش‌فرضِ عمومی {GENERIC_FALLBACK_TICK} استفاده می‌شود."
    )
    return None


def ensure_symbol_info(symbol, manual_tick_overrides, manual_leverage_overrides):
    symbol = symbol.upper()
    if symbol in manual_tick_overrides:
        tick = manual_tick_overrides[symbol]
        source = "override دستی (--tick)"
    elif symbol in TICK_SIZES:
        tick = TICK_SIZES[symbol]
        source = "دیکشنری شناخته‌شده"
    else:
        discovered = discover_tick_size(symbol)
        tick = discovered if discovered is not None else GENERIC_FALLBACK_TICK
        source = "کشف خودکار از Binance" if discovered is not None else "⚠️ پیش‌فرض عمومی"
    TICK_SIZES[symbol] = tick
    SYMBOL_TICK_INFO[symbol] = {
        "mintick": tick, "pricescale": _tick_to_pricescale(tick),
        "basecurrency": symbol.replace("USDT", ""),
    }
    if symbol in manual_leverage_overrides:
        LEVERAGE_MAP[symbol] = manual_leverage_overrides[symbol]
        lev_source = "override دستی (--leverage)"
    elif symbol in LEVERAGE_MAP:
        lev_source = "دیکشنری شناخته‌شده"
    else:
        LEVERAGE_MAP[symbol] = 50
        lev_source = "⚠️ پیش‌فرض عمومی 50x"
    logger.info(
        f"[SYMBOL-INFO] {symbol}: tick={tick} ({source}) | "
        f"leverage={LEVERAGE_MAP[symbol]}x ({lev_source})"
    )
    return tick, LEVERAGE_MAP[symbol], source, lev_source


# ============================================================
# دریافت دیتا از Binance Spot
# ============================================================
def fetch_klines(symbol, interval_min, start_ms, end_ms):
    interval = binance_interval_str(interval_min)
    tf_ms = int(interval_min) * 60_000
    all_rows = {}
    cursor = start_ms
    session = requests.Session()
    iters = 0
    while cursor <= end_ms:
        iters += 1
        if iters > MAX_FETCH_ITER:
            raise RuntimeError(f"صفحه‌بندی Binance بیش از {MAX_FETCH_ITER} تکرار طول کشید")
        chunk, last_err = None, None
        for attempt in range(4):
            base = BINANCE_BASES[attempt % len(BINANCE_BASES)]
            try:
                url = (f"{base}/api/v3/klines?symbol={symbol.upper()}&interval={interval}"
                       f"&startTime={cursor}&endTime={end_ms}&limit={KLINE_LIMIT}")
                r = session.get(url, timeout=20)
                if r.status_code in (418, 429):
                    time.sleep(2 ** attempt + 1)
                    continue
                r.raise_for_status()
                data = r.json()
                if not isinstance(data, list):
                    raise ValueError(f"bad payload: {str(data)[:100]}")
                chunk = data
                break
            except Exception as e:
                last_err = e
                time.sleep(0.8 * (attempt + 1))
        if chunk is None:
            raise RuntimeError(f"Binance unreachable {symbol} {interval} @ {cursor}: {last_err}")
        if not chunk:
            break
        added = 0
        for row in chunk:
            try:
                ot = int(row[0])
            except Exception:
                continue
            if ot not in all_rows:
                all_rows[ot] = row
                added += 1
        new_cursor = int(chunk[-1][0]) + tf_ms
        if new_cursor <= cursor:
            new_cursor = cursor + tf_ms
        cursor = new_cursor
        if added == 0 and len(chunk) < KLINE_LIMIT:
            break
        time.sleep(REQUEST_SLEEP)
    if not all_rows:
        return pd.DataFrame()
    rows = sorted(all_rows.values(), key=lambda x: int(x[0]))
    t = [r[0] / 1000.0 for r in rows]
    df = pd.DataFrame({
        "open": pd.to_numeric([r[1] for r in rows], errors="coerce"),
        "high": pd.to_numeric([r[2] for r in rows], errors="coerce"),
        "low": pd.to_numeric([r[3] for r in rows], errors="coerce"),
        "close": pd.to_numeric([r[4] for r in rows], errors="coerce"),
        "volume": pd.to_numeric([r[5] for r in rows], errors="coerce"),
    }, index=pd.to_datetime(t, unit="s", utc=True))
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    df = df.dropna(subset=["open", "high", "low", "close"])
    now_ms = int(time.time() * 1000)
    if rows and int(rows[-1][0]) + tf_ms > now_ms and len(df) > 0:
        df = df.iloc[:-1]
    return df


def df_to_candles(df):
    candles = []
    for idx, row in df.iterrows():
        candles.append(OHLCV(
            timestamp=int(idx.timestamp() * 1000),
            open=float(row["open"]), high=float(row["high"]),
            low=float(row["low"]), close=float(row["close"]),
            volume=float(row.get("volume", 0) or 0), is_closed=True,
        ))
    return candles


def _candles_to_tuples(candles):
    return [(c.timestamp, c.open, c.high, c.low, c.close, c.volume) for c in candles]


def _tuples_to_candles(tuples):
    return [OHLCV(timestamp=t[0], open=t[1], high=t[2], low=t[3], close=t[4], volume=t[5], is_closed=True)
            for t in tuples]


def _extract_hit_from_last_values(lv, i):
    sig = lv.get("signal")
    if sig not in ("LONG", "SHORT"):
        return None
    entry = _f(lv.get("entry"))
    if entry is None or entry <= 0:
        return None
    return (i, lv, sig, entry)


# ============================================================
# موتور «fast» — یک پاس پیوسته روی کل تاریخچه
# ============================================================
def run_strategy_pass_fast(candles, symbol, timeframe):
    syminfo = _build_syminfo(symbol, timeframe)
    inputs = get_strategy_inputs(timeframe)  # 🆕 استفاده از pivotMode مخصوص تایم‌فریم
    runner = ScriptRunner(
        STRATEGY_PATH, iter(candles), syminfo,
        last_bar_index=len(candles) - 1, inputs=inputs,
    )
    hits = []
    stats = {"bars": 0, "dicts": 0, "raw": 0, "errors": 0}
    logging.disable(logging.INFO)
    try:
        for i, result in enumerate(runner.run_iter()):
            stats["bars"] += 1
            try:
                if result is None or len(result) < 2:
                    continue
                raw = result[1]
                if not (isinstance(raw, dict) and len(raw) > 0):
                    continue
                lv = dict(raw)
                stats["dicts"] += 1
                hit = _extract_hit_from_last_values(lv, i)
                if hit is not None:
                    stats["raw"] += 1
                    hits.append(hit)
            except Exception:
                stats["errors"] += 1
                continue
    finally:
        logging.disable(logging.NOTSET)
    return hits, stats


# ============================================================
# موتور «exact» — بازسازیِ رفتار دقیقِ لایو
# ============================================================
def _run_one_window(candle_tuples, symbol, timeframe, i, history_bars):
    lo = max(0, i - history_bars + 1)
    window = _tuples_to_candles(candle_tuples[lo:i + 1])
    if len(window) < 50:
        return None
    syminfo = _build_syminfo(symbol, timeframe)
    inputs = get_strategy_inputs(timeframe)  # 🆕 استفاده از pivotMode مخصوص تایم‌فریم
    runner = ScriptRunner(
        STRATEGY_PATH, iter(window), syminfo,
        last_bar_index=len(window) - 1, inputs=inputs,
    )
    last_values = None
    for result in runner.run_iter():
        if result is None or len(result) < 2:
            continue
        raw = result[1]
        if isinstance(raw, dict) and len(raw) > 0:
            last_values = dict(raw)
    if last_values is None:
        return None
    return _extract_hit_from_last_values(last_values, i)


def _exact_worker(args):
    (candle_tuples, symbol, timeframe, idx_start, idx_end, history_bars) = args
    out = []
    errors = 0
    logging.disable(logging.CRITICAL)
    try:
        for i in range(idx_start, idx_end):
            try:
                hit = _run_one_window(candle_tuples, symbol, timeframe, i, history_bars)
                if hit is not None:
                    out.append(hit)
            except Exception:
                errors += 1
                continue
    finally:
        logging.disable(logging.NOTSET)
    return out, errors, (idx_end - idx_start)


def run_strategy_pass_exact(candles, symbol, timeframe, idx_from, idx_to,
                             history_bars=HISTORY_BARS, workers=1, progress_cb=None):
    n_total = idx_to - idx_from
    if n_total <= 0:
        return [], {"bars": 0, "dicts": 0, "raw": 0, "errors": 0}
    candle_tuples = _candles_to_tuples(candles)
    hits = []
    errors = 0
    done = 0
    if workers and workers > 1:
        try:
            chunk_size = max(1, math.ceil(n_total / workers))
            tasks = []
            for start in range(idx_from, idx_to, chunk_size):
                end = min(idx_to, start + chunk_size)
                tasks.append((candle_tuples, symbol, timeframe, start, end, history_bars))
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futures = {ex.submit(_exact_worker, t): t for t in tasks}
                for fut in as_completed(futures):
                    out, errs, cnt = fut.result()
                    hits.extend(out)
                    errors += errs
                    done += cnt
                    if progress_cb:
                        progress_cb(done, n_total)
            hits.sort(key=lambda h: h[0])
        except Exception as e:
            logger.warning(f"[EXACT] موازی‌سازی ناموفق ({e}) → اجرای تک‌پردازه‌ای")
            hits, errors, done = [], 0, 0
            for i in range(idx_from, idx_to):
                try:
                    hit = _run_one_window(candle_tuples, symbol, timeframe, i, history_bars)
                    if hit is not None:
                        hits.append(hit)
                except Exception:
                    errors += 1
                done += 1
                if progress_cb and done % 200 == 0:
                    progress_cb(done, n_total)
    else:
        for i in range(idx_from, idx_to):
            try:
                hit = _run_one_window(candle_tuples, symbol, timeframe, i, history_bars)
                if hit is not None:
                    hits.append(hit)
            except Exception:
                errors += 1
            done += 1
            if progress_cb and done % 200 == 0:
                progress_cb(done, n_total)
    stats = {"bars": n_total, "dicts": None, "raw": len(hits), "errors": errors}
    return hits, stats


# ============================================================
# تابع ساخت فایل دامپ سیگنال‌ها
# ============================================================
def build_signal_dump_file(trades, symbol, timeframe, last_n=5000):
    """
    آخرین N سیگنال/معامله را به‌صورت فایل کامل csv-like می‌نویسد.
    فرمت: ENTRY_TIME,ENTRY_TIME_IR,EXIT_TIME,EXIT_TIME_IR,DIRECTION,ENTRY,STOP,TARGET,SIGNAL_TYPE,SCORE,EXIT_REASON,PNL_R,PNL_USD,STATUS
    """
    try:
        if not trades or last_n <= 0:
            return None, 0
        
        sorted_trades = sorted(trades, key=lambda t: t.get("entry_time_ms", 0))
        subset = sorted_trades[-int(last_n):]
        
        p = BASE_DIR / f"backtest_signals_{symbol}_{timeframe}m.txt"
        lines = [
            f"# SYMBOL={symbol} TF={timeframe}m SIGNALS={len(subset)}",
            "# همه‌ی سیگنال‌ها کامل است — هیچ برشی انجام نشده",
            "# ENTRY_TIME(UTC),ENTRY_TIME(IRAN),EXIT_TIME(UTC),EXIT_TIME(IRAN),DIRECTION,ENTRY,STOP,TARGET,SIGNAL_TYPE,SCORE,EXIT_REASON,PNL_R,PNL_USD,STATUS",
        ]
        
        for t in subset:
            entry_dt = _ms_to_iran(t.get("entry_time_ms"))
            entry_str = entry_dt.strftime("%Y-%m-%d %H:%M") if entry_dt else "?"
            
            exit_dt = _ms_to_iran(t.get("exit_time_ms"))
            exit_str = exit_dt.strftime("%Y-%m-%d %H:%M") if exit_dt else "?"
            
            entry_price = t.get('entry', 0)
            stop_price = t.get('stop', 0)
            target_price = t.get('target', 0)
            
            # برای ارزهای با قیمت کوچک دقت بیشتر
            if symbol == "PUMPUSDT" or symbol == "1000PEPEUSDT" or symbol == "NOTUSDT":
                entry_str_p = f"{entry_price:.8f}"
                stop_str_p = f"{stop_price:.8f}"
                target_str_p = f"{target_price:.8f}"
            else:
                entry_str_p = f"{entry_price:.4f}"
                stop_str_p = f"{stop_price:.4f}"
                target_str_p = f"{target_price:.4f}"
            
            pnl_r = t.get('pnl_r', 0)
            pnl_usd = t.get('pnl_usd', 0)
            
            lines.append(
                f"{t.get('entry_time_ms', 0)},{entry_str},"
                f"{t.get('exit_time_ms', 0) or ''},{exit_str},"
                f"{t.get('direction', '')},"
                f"{entry_str_p},{stop_str_p},{target_str_p},"
                f"{t.get('signal_type', '?')},"
                f"{t.get('score', 0)},"
                f"{t.get('exit_reason', '')},"
                f"{pnl_r:.2f},{pnl_usd:.2f},"
                f"{t.get('status', '')}"
            )
        
        p.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"[SIGNAL-DUMP] {symbol} {timeframe}m: {len(subset)} سیگنال کامل → {p.name}")
        return str(p), len(subset)
    except Exception as e:
        logger.warning(f"[SIGNAL-DUMP] {symbol} {timeframe}m ناموفق: {e}")
        return None, 0


# ============================================================
# شبیه‌سازی هر معامله
# ============================================================
def simulate_trade(tr, candles, n, risk_free_fee_usd=0.0):
    try:
        entry, initial_stop = tr["entry"], tr["stop"]
        target, direction = tr["target"], tr["direction"]
        rf = tr.get("rf_pct")
        stop, risk_free = initial_stop, False
        fee_pct = (risk_free_fee_usd / (BASE_CAPITAL * (tr.get("leverage") or 50))) if risk_free_fee_usd else 0.0
        for j in range(tr["entry_idx"] + 1, n):
            c = candles[j]
            high, low = float(c.high), float(c.low)
            ts = int(c.timestamp)
            if not risk_free and rf is not None:
                if direction == "LONG":
                    crossed = high >= entry * (1 + abs(rf))
                else:
                    crossed = low <= entry * (1 - abs(rf))
                if crossed:
                    risk_free = True
                    stop = entry * (1 + fee_pct) if direction == "LONG" else entry * (1 - fee_pct)
            if direction == "LONG":
                hit_stop = low <= stop
                hit_target = (target is not None) and high >= target
            else:
                hit_stop = high >= stop
                hit_target = (target is not None) and low <= target
            if hit_stop:
                tr["status"] = "WIN" if risk_free else "LOSS"
                tr["exit_reason"] = "RISK_FREE_STOP" if risk_free else "STOP_LOSS"
                tr["exit_price"], tr["exit_time_ms"] = stop, ts
                break
            if hit_target:
                tr["status"], tr["exit_reason"] = "WIN", "TARGET"
                tr["exit_price"], tr["exit_time_ms"] = target, ts
                break
        tr["risk_free"] = risk_free
        if tr["status"] != "OPEN":
            pnl, r = pnl_fn(direction, entry, initial_stop, tr["exit_price"], tr["leverage"])
            tr["pnl_usd"], tr["pnl_r"] = pnl, r
    except Exception as e:
        logger.warning(f"[SIM] {tr.get('symbol')} error: {e}")
        tr["status"] = "OPEN"


# ============================================================
# بک‌تست یک ترکیب ارز/تایم‌فریم
# ============================================================
def backtest_combo(symbol, timeframe, start_ms, end_ms, engine="fast",
                    history_bars=HISTORY_BARS, workers=1, risk_free_fee_usd=0.0,
                    progress_cb=None, window_clamp=HISTORY_BARS, verify_sample_n=0,
                    signal_dump_n=5000):
    tf_minutes = int(timeframe)
    warmup_ms = history_bars * tf_minutes * 60_000 + 3 * 86_400_000
    fetch_start = start_ms - warmup_ms
    df = fetch_klines(symbol, tf_minutes, fetch_start, end_ms)
    if df is None or df.empty:
        raise RuntimeError("دیتای خالی از Binance")
    if len(df) < history_bars + 50:
        raise RuntimeError(f"کندل کافی برای پنجره‌ی {history_bars}-تایی نیست: {len(df)}")

    candles = df_to_candles(df)
    n = len(candles)
    mintick = SYMBOL_TICK_INFO.get(symbol, {"mintick": GENERIC_FALLBACK_TICK})["mintick"]

    timestamps = [int(c.timestamp) for c in candles]
    idx_from = next((k for k, ts in enumerate(timestamps) if ts >= start_ms), n)
    idx_to = n

    if engine == "fast":
        raw_hits, diag = run_strategy_pass_fast(candles, symbol, timeframe)
    else:
        raw_hits, diag = run_strategy_pass_exact(
            candles, symbol, timeframe, idx_from, idx_to,
            history_bars=history_bars, workers=workers, progress_cb=progress_cb,
        )
        fixed = []
        for (i, lv, sig, entry) in raw_hits:
            lo = max(0, i - history_bars + 1)
            lv2 = dict(lv)
            for _k in ("pivot_high_index", "pivot_low_index",
                       "previous_pivot_high_index", "previous_pivot_low_index"):
                _v = _f(lv.get(_k))
                if _v is not None:
                    lv2[_k] = _v + lo
            fixed.append((i, lv2, sig, entry))
        raw_hits = fixed

    seen, trades = set(), []
    drop = {"out_of_range": 0, "bad_sltp": 0, "dup": 0, "outside_window": 0}
    raw_stats = {
        "total": len(raw_hits),
        "by_signal": {"LONG": 0, "SHORT": 0},
        "by_score": {},
        "by_type": {"CD+": 0, "CD-": 0, "HD+": 0, "HD-": 0},
    }

    for (i, lv, sig, entry) in raw_hits:
        try:
            ts = int(candles[i].timestamp)
            if ts < start_ms or ts > end_ms:
                drop["out_of_range"] += 1
                continue
            key = (symbol, str(timeframe), ts, sig)
            if key in seen:
                drop["dup"] += 1
                continue
            seen.add(key)

            if window_clamp and window_clamp > 0:
                wlo = max(0, i - int(window_clamp) + 1)
                if sig == "LONG":
                    p2i = _f(lv.get("pivot_low_index"))
                    p1i = _f(lv.get("previous_pivot_low_index"))
                else:
                    p2i = _f(lv.get("pivot_high_index"))
                    p1i = _f(lv.get("previous_pivot_high_index"))
                if p1i is None or p2i is None or p1i < wlo or p2i < wlo:
                    drop["outside_window"] += 1
                    continue

            stop, target, rr, struct = None, None, None, None
            try:
                stop, target, rr, struct = _compute_stop_target(
                    candles, sig, lv, mintick, buffer_ticks=buffer_ticks_for(symbol)
                )
            except Exception as e:
                logger.warning(f"[SL/TP] {symbol} {timeframe}m bar {i}: {e}")
            if stop is None or target is None or abs(entry - stop) <= 0:
                drop["bad_sltp"] += 1
                continue

            st = signal_type_of(lv)
            sc = _score_of(lv, st)

            raw_stats["by_signal"][sig] = raw_stats["by_signal"].get(sig, 0) + 1
            raw_stats["by_score"][sc] = raw_stats["by_score"].get(sc, 0) + 1
            if st:
                raw_stats["by_type"][st] = raw_stats["by_type"].get(st, 0) + 1

            tr = {
                "symbol": symbol, "timeframe": str(timeframe), "direction": sig,
                "entry": float(entry), "stop": float(stop), "target": float(target),
                "entry_time_ms": ts, "entry_idx": int(i),
                "leverage": LEVERAGE_MAP.get(symbol, 50),
                "signal_type": st or "?", "score": sc,
                "rf_pct": compute_rf_pct(sig, entry, stop, struct),
                "rr_planned": _f(rr),
                "status": "OPEN", "exit_reason": None, "exit_price": None,
                "exit_time_ms": None, "pnl_usd": None, "pnl_r": None, "risk_free": False,
                "filter_rsi": lv.get("classic_bearish_rsi") or lv.get("classic_bullish_rsi") or False,
                "filter_macd": lv.get("classic_bearish_macd") or lv.get("classic_bullish_macd") or False,
                "filter_hist": lv.get("classic_bearish_hist") or lv.get("classic_bullish_hist") or False,
                "filter_fib": lv.get("fib_bearish") or lv.get("fib_bullish") or False,
                "filter_pa": lv.get("price_action_bearish") or lv.get("price_action_bullish") or False,
                "trend_bullish_ok": lv.get("trend_bullish_ok", False),
                "trend_bearish_ok": lv.get("trend_bearish_ok", False),
            }
            simulate_trade(tr, candles, n, risk_free_fee_usd=risk_free_fee_usd)
            trades.append(tr)
        except Exception as e:
            logger.warning(f"[BT] {symbol} {timeframe}m bar {i}: {e}")
            continue

    # فایل کامل آخرین N سیگنال
    if signal_dump_n and signal_dump_n > 0:
        dump_path, dump_count = build_signal_dump_file(trades, symbol, timeframe, signal_dump_n)
        diag["signal_dump_path"] = dump_path
        diag["signal_dump_count"] = dump_count

    # نمونه‌گیری کنترلی
    if verify_sample_n and verify_sample_n > 0 and engine == "fast":
        cand_bars = {h[0] for h in raw_hits}
        tuples_all = _candles_to_tuples(candles)
        checked = found = 0
        for j in range(idx_from, n, max(1, int(verify_sample_n))):
            if j in cand_bars:
                continue
            try:
                hit = _run_one_window(tuples_all, symbol, timeframe, j, history_bars)
            except Exception:
                continue
            checked += 1
            if hit is not None:
                ts_j = int(candles[j].timestamp)
                if start_ms <= ts_j <= end_ms:
                    found += 1
        diag["control_checked"] = checked
        diag["control_found"] = found
        if found:
            logger.warning(f"[CONTROL] {symbol} {timeframe}m: {found} سیگنال جاافتاده در نمونه‌ی کنترلی")

    diag.update(drop)
    diag["trades"] = len(trades)
    diag["engine"] = engine
    return trades, n, raw_stats, diag


# ============================================================
# شبیه‌سازی با موجودی واقعی
# ============================================================
def simulate_with_account_balance(trades, start_balance,
                                   base_capital=LIVE_BASE_CAPITAL,
                                   balance_use_ratio=LIVE_BALANCE_USE_RATIO,
                                   min_order_cost=MIN_ORDER_COST_USDT):
    closed = sorted(
        [t for t in trades if t.get("status") in ("WIN", "LOSS") and t.get("pnl_r") is not None],
        key=lambda t: t.get("exit_time_ms") or t["entry_time_ms"],
    )
    balance = float(start_balance)
    executed, skipped_low_capital = 0, 0
    for t in closed:
        stop_pct = abs(t["entry"] - t["stop"]) / t["entry"] if t["entry"] else 0
        if stop_pct <= 0:
            continue
        allowed_leverage = t.get("leverage") or 50
        old_leverage = 1.0 / stop_pct
        if old_leverage > allowed_leverage:
            required_capital = (old_leverage / allowed_leverage) * base_capital
        else:
            required_capital = base_capital
        if balance < required_capital:
            capital = balance * balance_use_ratio
        else:
            capital = required_capital
        if capital < min_order_cost:
            skipped_low_capital += 1
            continue
        r_multiple = t["pnl_r"]
        pnl_usd = capital * allowed_leverage * stop_pct * r_multiple
        balance += pnl_usd
        executed += 1
        if balance <= 0:
            balance = 0.0
            break
    return {
        "start_balance": start_balance,
        "end_balance": round(balance, 2),
        "executed_trades": executed,
        "skipped_low_capital": skipped_low_capital,
        "total_closed": len(closed),
    }


# ============================================================
# آمار و گزارش (کامل - بدون تغییر)
# ============================================================
def stats_of(trades):
    s = {"total": len(trades)}
    wins = [t for t in trades if t.get("status") == "WIN"]
    losses = [t for t in trades if t.get("status") == "LOSS"]
    opens = [t for t in trades if t.get("status") == "OPEN"]
    closed = wins + losses
    s.update(wins=len(wins), losses=len(losses), opens=len(opens), closed=len(closed))
    s["rf_wins"] = sum(1 for t in wins if t.get("exit_reason") == "RISK_FREE_STOP")
    s["tp_wins"] = sum(1 for t in wins if t.get("exit_reason") == "TARGET")
    s["winrate"] = (len(wins) / len(closed) * 100) if closed else 0.0
    pnls = [t["pnl_usd"] for t in closed if t.get("pnl_usd") is not None]
    s["pnl_total"] = sum(pnls)
    gw = sum(p for p in pnls if p > 0)
    gl = sum(p for p in pnls if p < 0)
    s["pf"] = (gw / abs(gl)) if gl < 0 else (float("inf") if gw > 0 else 0.0)
    s["avg_win"] = gw / len(wins) if wins else 0.0
    s["avg_loss"] = gl / len(losses) if losses else 0.0
    rs = [t["pnl_r"] for t in closed if t.get("pnl_r") is not None]
    s["avg_r"] = sum(rs) / len(rs) if rs else 0.0
    rrs = [t["rr_planned"] for t in trades if t.get("rr_planned")]
    s["avg_rr"] = sum(rrs) / len(rrs) if rrs else 0.0
    seq = sorted([t for t in closed if t.get("pnl_usd") is not None],
                 key=lambda t: t.get("exit_time_ms") or t["entry_time_ms"])
    streak = best_streak = 0
    cum = peak = 0.0
    dd = 0.0
    for t in seq:
        if t["status"] == "LOSS":
            streak += 1
            best_streak = max(best_streak, streak)
        else:
            streak = 0
        cum += t["pnl_usd"]
        peak = max(peak, cum)
        dd = min(dd, cum - peak)
    s["max_consec_loss"] = best_streak
    s["max_dd"] = dd
    durs = [(t["exit_time_ms"] - t["entry_time_ms"]) / 60000.0
            for t in closed if t.get("exit_time_ms")]
    s["avg_hold_min"] = sum(durs) / len(durs) if durs else 0.0
    return s


def fmt_money(x):
    return f"{x:+.2f}$" if x is not None else "—"


def fmt_pf(pf):
    return "∞" if pf == float("inf") else f"{pf:.2f}"


def group_dict(items, keyfn):
    d = {}
    for it in items:
        d.setdefault(keyfn(it), []).append(it)
    return d


def fmt_trade_line(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    ts = dt.strftime("%m-%d %H:%M") if dt else "?"
    emoji = {"WIN": "✅", "LOSS": "❌", "OPEN": "⏳"}.get(t.get("status"), "•")
    if t.get("exit_reason") == "RISK_FREE_STOP":
        emoji = "🛡️"
    r = t.get("pnl_r")
    r_str = f"{r:+.2f}R" if r is not None else "—"
    return f"  {emoji} {ts} | {t['timeframe']}m | {t.get('signal_type','?')} S{t.get('score',0)} | {r_str} {fmt_money(t.get('pnl_usd'))}"


def _section(lines, title, trades, keyfn):
    g = group_dict(trades, keyfn)
    if not g:
        return
    lines.append(W)
    lines.append(title)
    for k in sorted(g.keys(), key=str):
        stg = stats_of(g[k])
        lines.append(f"  • {k}: {stg['total']} سیگنال | ✅{stg['wins']} ❌{stg['losses']} ⏳{stg['opens']} "
                     f"| نرخ {stg['winrate']:.0f}٪ | {fmt_money(stg['pnl_total'])}")


def hour_bucket(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    return f"{(dt.hour // 4) * 4:02d}-{(dt.hour // 4) * 4 + 3:02d}" if dt else "?"


def weekday_fa(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    return WD_FA[dt.weekday()] if dt else "?"


def season_of(t):
    dt = _ms_to_iran(t["entry_time_ms"])
    if not dt:
        return "?"
    m = dt.month
    if m in (3, 4, 5):
        return "بهار"
    if m in (6, 7, 8):
        return "تابستان"
    if m in (9, 10, 11):
        return "پاییز"
    return "زمستان"


def build_seasonal_analysis(trades):
    seasons = {}
    for t in trades:
        s = season_of(t)
        seasons.setdefault(s, []).append(t)
    lines = ["🌍 تحلیل فصلی:"]
    for season, items in seasons.items():
        st = stats_of(items)
        if st["closed"] >= 5:
            lines.append(f"  • {season}: {st['closed']} معامله | نرخ {st['winrate']:.0f}٪ | {fmt_money(st['pnl_total'])}")
    if len(lines) == 1:
        lines.append("  • داده‌های کافی برای تحلیل فصلی وجود ندارد.")
    return lines


def build_filter_analysis(trades):
    filters = {
        "RSI": "filter_rsi", "MACD": "filter_macd", "Histogram": "filter_hist",
        "Fibonacci": "filter_fib", "Price Action": "filter_pa",
    }
    lines = ["🔬 تحلیل فیلترها:"]
    closed = [t for t in trades if t.get("status") in ("WIN", "LOSS")]
    for fname, fkey in filters.items():
        with_filter = [t for t in closed if t.get(fkey, False)]
        without_filter = [t for t in closed if not t.get(fkey, False)]
        if len(with_filter) >= 10:
            st_w = stats_of(with_filter)
            st_wo = stats_of(without_filter) if without_filter else None
            diff = st_w["winrate"] - (st_wo["winrate"] if st_wo else 0)
            emoji = "✅" if diff > 0 else "❌" if diff < 0 else "➖"
            lines.append(f"  • {fname}: {st_w['winrate']:.0f}٪ ({len(with_filter)} معامله) | "
                        f"{emoji} تفاوت: {diff:+.1f}٪ | {fmt_money(st_w['pnl_total'])}")
    if len(lines) == 1:
        lines.append("  • داده‌های کافی برای تحلیل فیلترها وجود ندارد.")
    return lines


def build_market_analysis(trades):
    closed = [t for t in trades if t.get("status") in ("WIN", "LOSS")]
    trending_up = [t for t in closed if t.get("trend_bullish_ok", False)]
    trending_down = [t for t in closed if t.get("trend_bearish_ok", False)]
    neutral = [t for t in closed if not t.get("trend_bullish_ok", False) and not t.get("trend_bearish_ok", False)]
    lines = ["📈 تحلیل بازار:"]
    for name, items in [("📈 روند صعودی", trending_up), ("📉 روند نزولی", trending_down), ("➖ خنثی", neutral)]:
        if len(items) >= 5:
            st = stats_of(items)
            lines.append(f"  {name}: {st['closed']} معامله | نرخ {st['winrate']:.0f}٪ | {fmt_money(st['pnl_total'])}")
    if len(lines) == 1:
        lines.append("  • داده‌های کافی برای تحلیل بازار وجود ندارد.")
    return lines


def build_advanced_insights(trades):
    lines = ["🎯 پیشنهادات بهینه‌سازی:"]
    closed = [t for t in trades if t.get("status") in ("WIN", "LOSS")]
    if len(closed) < 20:
        lines.append("  • داده‌های کافی برای پیشنهاد دقیق وجود ندارد.")
        return lines
    combos = group_dict(trades, lambda t: f"{t['symbol']} {t['timeframe']}m")
    valid_combos = [(k, stats_of(v)) for k, v in combos.items() if stats_of(v)["closed"] >= 10]
    if valid_combos:
        best = max(valid_combos, key=lambda kv: kv[1]["winrate"])
        worst = min(valid_combos, key=lambda kv: kv[1]["winrate"])
        lines.append(f"  • ✅ بهترین ترکیب: {best[0]} (نرخ {best[1]['winrate']:.0f}٪، {fmt_money(best[1]['pnl_total'])})")
        lines.append(f"  • ❌ ضعیف‌ترین ترکیب: {worst[0]} (نرخ {worst[1]['winrate']:.0f}٪، {fmt_money(worst[1]['pnl_total'])})")
    types = group_dict(trades, lambda t: t.get("signal_type", "?"))
    valid_types = [(k, stats_of(v)) for k, v in types.items() if stats_of(v)["closed"] >= 10]
    if valid_types:
        best_type = max(valid_types, key=lambda kv: kv[1]["winrate"])
        lines.append(f"  • ✅ بهترین نوع سیگنال: {best_type[0]} (نرخ {best_type[1]['winrate']:.0f}٪)")
    hours = group_dict(trades, lambda t: f"{_ms_to_iran(t['entry_time_ms']).hour:02d}:00" if _ms_to_iran(t['entry_time_ms']) else "?")
    valid_hours = [(k, stats_of(v)) for k, v in hours.items() if stats_of(v)["closed"] >= 8]
    if len(valid_hours) >= 3:
        best_hour = max(valid_hours, key=lambda kv: kv[1]["winrate"])
        worst_hour = min(valid_hours, key=lambda kv: kv[1]["winrate"])
        lines.append(f"  • 🕐 بهترین ساعت: {best_hour[0]} (نرخ {best_hour[1]['winrate']:.0f}٪)")
        lines.append(f"  • 🕐 ضعیف‌ترین ساعت: {worst_hour[0]} (نرخ {worst_hour[1]['winrate']:.0f}٪)")
    for score_threshold in [4, 5]:
        filtered = [t for t in closed if (t.get("score") or 0) >= score_threshold]
        if len(filtered) >= 10:
            st = stats_of(filtered)
            base = stats_of(closed)
            improvement = st["winrate"] - base["winrate"]
            tag = f"({improvement:+.1f}٪ بهتر از پایه)" if improvement > 2 else f"({improvement:+.1f}٪ تغییر)"
            lines.append(f"  • ⭐ فیلتر امتیاز ≥ {score_threshold}: نرخ {st['winrate']:.0f}٪ {tag} | {fmt_money(st['pnl_total'])}")
    rf_trades = [t for t in closed if t.get("risk_free", False)]
    non_rf_trades = [t for t in closed if not t.get("risk_free", False)]
    if len(rf_trades) >= 10 and len(non_rf_trades) >= 10:
        rf_st = stats_of(rf_trades)
        non_rf_st = stats_of(non_rf_trades)
        rf_impact = rf_st["winrate"] - non_rf_st["winrate"]
        lines.append(f"  • 🛡️ ریسک‌فری: {rf_st['winrate']:.0f}٪ vs بدون ریسک‌فری {non_rf_st['winrate']:.0f}٪ "
                    f"({rf_impact:+.1f}٪ تفاوت) | {fmt_money(rf_st['pnl_total'])}")
    rr_groups = group_dict(trades, lambda t: f"1:{round(t.get('rr_planned', 0), 1)}")
    valid_rr = [(k, stats_of(v)) for k, v in rr_groups.items() if stats_of(v)["closed"] >= 10 and k != "1:nan"]
    if valid_rr:
        best_rr = max(valid_rr, key=lambda kv: kv[1]["pnl_total"])
        lines.append(f"  • 📊 بهترین R:R: {best_rr[0]} (نرخ {best_rr[1]['winrate']:.0f}٪، {fmt_money(best_rr[1]['pnl_total'])})")
    total_pnl = stats_of(closed)["pnl_total"]
    if total_pnl > 0:
        lines.append(f"  • ✅ استراتژی در مجموع سودآور است: {fmt_money(total_pnl)}")
    else:
        lines.append(f"  • ❌ استراتژی در مجموع زیان‌ده است: {fmt_money(total_pnl)}")
        lines.append("  • 💡 پیشنهاد: حذف ضعیف‌ترین ترکیب‌ها یا تنظیم پارامترهای ورودی")
    return lines


def build_methodology_note(meta):
    engine = meta.get("engine_mode", "fast")
    clamp = meta.get("window_clamp", 0) or 0
    lines = [W, "🧭 روش‌شناسی این گزارش (برای تفسیر درست نتایج):"]
    if engine == "exact":
        lines.append(
            f"  • موتور سیگنال: «exact» — هر کندل با پنجره‌ی سردِ "
            f"{meta.get('history_bars', HISTORY_BARS)}کندلی (عیناً لایو؛ ایندکس‌های پیوت به فضای کلی تبدیل شده‌اند)."
        )
    elif clamp > 0:
        lines.append(
            f"  • موتور سیگنال: «پیوسته + فیلتر پنجره‌ی لایو» — یک پاس کامل روی تاریخچه، و حذف سیگنال‌هایی که "
            f"پیوت‌های استاپ/تارگتشان قدیمی‌تر از {clamp} کندل‌اند؛ چون لایو فقط ~۵۰۰ کندل آخر را می‌بیند و "
            f"سیگنال با پیوت قدیمی‌تر در لایو هرگز تولید نمی‌شد."
        )
    else:
        lines.append(
            "  • ⚠️ موتور «پیوسته» بدون فیلتر پنجره — ممکن است سیگنال‌هایی با پیوت خیلی قدیمی بشمارد که لایو نمی‌دید. "
            "فعال‌سازی: --window-clamp 500"
        )
    lines.append(
        f"  • PnL بر مبنای «سرمایه‌ی پایه‌ی ثابت {BASE_CAPITAL:.0f}$» به‌ازای هر معامله (دقیقاً مثل trade_ledger)، "
        f"نه موجودی واقعی حساب — یعنی «کیفیت خالص استراتژی» را می‌سنجد."
    )
    lines.append(
        "  • ریسک‌فری با تقریب «سربه‌سر» شبیه‌سازی شده (بدون کارمزد واقعی صرافی)، مگر با --risk-free-fee-usd."
    )
    lines.append("  • بدون احتساب اسلیپیج و کارمزد واقعی صرافی روی ورود/خروج.")
    if meta.get("control_checked_total"):
        lines.append(
            f"  • 🎯 نمونه‌گیری کنترلی: {meta['control_checked_total']} کندلِ غیرکاندید با پنجره‌ی سرد چک شد؛ "
            f"{meta['control_found_total']} سیگنالِ جاافتاده تخمین زده شد."
        )
    if meta.get("account_sim"):
        acc = meta["account_sim"]
        lines.append(
            f"  • 💼 شبیه‌سازی تکمیلی با موجودی واقعی: شروع از {acc['start_balance']:.2f}$ → "
            f"پایان {acc['end_balance']:.2f}$ ({acc['executed_trades']} اجرا شد، "
            f"{acc['skipped_low_capital']} ردشده به‌دلیل سرمایه‌ی کم)."
        )
    return lines


def build_overall_report(trades, meta):
    st = stats_of(trades)
    L = ["📊 گزارش کامل بک‌تست استراتژی DTM", W]
    L.append(f"🗓 بازه: {meta['start_date']} تا {meta['end_date']} ({meta['days']} روز — تهران)")
    L.append(f"📡 دیتا: Binance Spot | تایم‌فریم: {', '.join(tf + 'm' for tf in meta['tfs'])}")
    L.append(f"💱 نمادها: {', '.join(meta['symbols'])}")
    L.append(f"🕐 تولید گزارش: {meta['generated_at']} (تهران)")
    L.append(f"⚙️ موتور سیگنال: {meta['engine']} | حالت: {meta.get('engine_mode', 'exact')}")
    L.append(f"🔧 منبع تنظیمات نماد/اهرم: {meta.get('const_source', CONST_SOURCE)}")
    L.append(W)
    L.append(f"📈 کل سیگنال‌ها: {st['total']}")
    L.append(f"✅ برنده: {st['wins']}  (🎯 تارگت: {st['tp_wins']} | 🛡️ ریسک‌فری: {st['rf_wins']})")
    L.append(f"❌ بازنده: {st['losses']}")
    L.append(f"⏳ هنوز باز: {st['opens']}")
    L.append(f"🏆 نرخ برد: {st['winrate']:.1f}٪ (از {st['closed']} معامله بسته‌شده)")
    L.append(f"💰 سود/زیان فرضی کل: {fmt_money(st['pnl_total'])} (سرمایه پایه {BASE_CAPITAL:.0f}$)")
    L.append(f"⚖️ پروفیت فکتور: {fmt_pf(st['pf'])}")
    L.append(f"📊 میانگین R: {st['avg_r']:.2f} | میانگین برد: {fmt_money(st['avg_win'])} | میانگین باخت: {fmt_money(st['avg_loss'])}")
    L.append(f"🎯 میانگین R:R برنامه‌ریزی‌شده: 1:{st['avg_rr']:.2f}")
    L.append(f"⏱ میانگین طول معامله: {st['avg_hold_min']:.0f} دقیقه")
    L.append(f"🔥 حداکثر باخت متوالی: {st['max_consec_loss']}")
    L.append(f"📉 حداکثر افت سرمایه: {fmt_money(st['max_dd'])}")

    _section(L, "💼 به تفکیک ارز:", trades, lambda t: t["symbol"])
    _section(L, "🕐 به تفکیک تایم‌فریم:", trades, lambda t: f"{t['timeframe']}m")
    _section(L, "🔀 به تفکیک نوع سیگنال:", trades, lambda t: t.get("signal_type", "?"))
    _section(L, "⭐ به تفکیک امتیاز:", trades, lambda t: f"امتیاز {t.get('score', 0)}")

    L.append(W); L.extend(build_seasonal_analysis(trades))
    L.append(W); L.extend(build_filter_analysis(trades))
    L.append(W); L.extend(build_market_analysis(trades))
    L.append(W); L.extend(build_advanced_insights(trades))
    L.extend(build_methodology_note(meta))

    cs = sorted([t for t in trades if t.get("pnl_usd") is not None], key=lambda t: t["pnl_usd"])
    if cs:
        L.append(W)
        L.append("🏅 ۵ معامله برتر:")
        for t in cs[-5:][::-1]:
            L.append(fmt_trade_line(t))
        L.append("💥 ۵ معامله ضعیف:")
        for t in cs[:5]:
            L.append(fmt_trade_line(t))

    if meta.get("combos"):
        L.append(W)
        L.append("🧮 خلاصه اجرا:")
        for c in meta["combos"]:
            raw_info = c.get("raw_hits", {})
            raw_total = raw_info.get("total", 0)
            raw_by_signal = raw_info.get("by_signal", {})
            line = (f"  • {c['symbol']} {c['tf']}m | کندل: {c['bars']:,} | سیگنال خام: {raw_total}"
                    f" | خارج‌ازپنجره: {c.get('outside_window', 0)}")
            if raw_by_signal:
                line += f" (LONG: {raw_by_signal.get('LONG', 0)} | SHORT: {raw_by_signal.get('SHORT', 0)})"
            line += f" | معاملات: {c['signals']}"
            if c.get("elapsed_sec") is not None:
                line += f" | {c['elapsed_sec']:.0f}s"
            if c.get("signal_dump_count", 0):
                line += f" | 📄 سیگنال‌ها: {c['signal_dump_count']}"
            L.append(line)

    if meta.get("errors"):
        L.append(W)
        L.append("⚠️ خطاهای بک‌تست:")
        for e in meta["errors"][:10]:
            L.append(f"  • {e[:150]}...")

    L.append(W)
    L.append("⚠️ نتایج فرضی است (بدون اسلیپیج/کارمزد واقعی) — صرفاً برای ارزیابی استراتژی.")
    return "\n".join(L)


def build_combo_report(sym, tf, trades):
    st = stats_of(trades)
    L = [f"📋 گزارش تفکیکی {sym} — {tf} دقیقه", W]
    if st["total"] == 0:
        L.append("در این بازه هیچ سیگنالی ثبت نشد.")
        return "\n".join(L)
    L.append(f"📈 سیگنال‌ها: {st['total']} | ✅{st['wins']} (🎯{st['tp_wins']} 🛡️{st['rf_wins']}) | ❌{st['losses']} | ⏳{st['opens']}")
    L.append(f"🏆 نرخ برد: {st['winrate']:.1f}٪ | 💰 {fmt_money(st['pnl_total'])} | PF: {fmt_pf(st['pf'])}")
    L.append(f"📊 میانگین R: {st['avg_r']:.2f} | 🔥 باخت متوالی: {st['max_consec_loss']} | 📉 افت: {fmt_money(st['max_dd'])}")
    L.append(W)
    items = sorted(trades, key=lambda t: t["entry_time_ms"])
    if len(items) <= 25:
        L.append("🧾 همه معاملات:")
        for t in items:
            L.append(fmt_trade_line(t))
    else:
        cs = sorted([t for t in items if t.get("pnl_usd") is not None], key=lambda t: t["pnl_usd"])
        L.append("🏅 ۵ معامله برتر:")
        for t in cs[-5:][::-1]:
            L.append(fmt_trade_line(t))
        L.append("💥 ۵ معامله ضعیف:")
        for t in cs[:5]:
            L.append(fmt_trade_line(t))
        L.append(f"  … و {len(items) - 10} معامله دیگر")
    return "\n".join(L)


# ============================================================
# ذخیره/بارگذاری نتایج و قفل روزانه
# ============================================================
def save_results(trades, meta):
    try:
        with open(RESULTS_PATH, "w", encoding="utf-8") as f:
            json.dump({"meta": meta, "trades": trades}, f, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"[SAVE] {e}")
        return False


def load_results():
    try:
        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("trades", []), data.get("meta", {})
    except Exception as e:
        logger.error(f"[LOAD] {e}")
        return [], {}


def marker_already_sent(mode):
    try:
        data = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
        return data.get(mode) == today_str()
    except Exception:
        return False


def marker_set(mode):
    try:
        data = {}
        if MARKER_PATH.exists():
            data = json.loads(MARKER_PATH.read_text(encoding="utf-8"))
        data[mode] = today_str()
        MARKER_PATH.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.error(f"[MARKER] {e}")


def save_report_backup(text):
    try:
        p = BASE_DIR / f"backtest_report_{datetime.now(UTC_TZ).strftime('%Y%m%d_%H%M')}.txt"
        p.write_text(text, encoding="utf-8")
        logger.info(f"[BACKUP] گزارش در {p.name} ذخیره شد")
    except Exception as e:
        logger.error(f"[BACKUP] {e}")


# ============================================================
# ارسال گزارش‌ها
# ============================================================
def send_reports(trades, meta, mode, do_send):
    texts = []
    if mode in ("full", "both"):
        texts.append(("📊 گزارش کامل", build_overall_report(trades, meta)))
    if mode in ("breakdown", "both"):
        groups = group_dict(trades, lambda t: (t["symbol"], t["timeframe"]))
        order = {(s, tf) for s in meta.get("symbols", SYMBOLS) for tf in meta.get("tfs", TIMEFRAMES)}
        keys = sorted(set(groups.keys()) | order, key=lambda k: (k[0], int(k[1])))
        for (sym, tf) in keys:
            texts.append((f"📋 {sym} {tf}m", build_combo_report(sym, tf, groups.get((sym, tf), []))))

    full_text = "\n\n".join(f"{h}\n{b}" for h, b in texts)
    save_report_backup(full_text)

    if not do_send:
        print(full_text)
        return True

    ok = True
    for header, body in texts:
        ok = tg_send_long(f"{header}\n\n{body}") and ok
        time.sleep(1)
    if not ok:
        logger.error("[SEND] ارسال تلگرام ناقص بود — با --resend دوباره بفرست")
    return ok


# ============================================================
# main
# ============================================================
def parse_args():
    p = argparse.ArgumentParser(description="بک‌تست و گزارش استراتژی DTM")
    p.add_argument("--days", type=int, default=DAYS_DEFAULT,
                   help="تعداد روزهای بک‌تست (پیش‌فرض ۳۶۵ = ۱ سال)")
    p.add_argument("--symbols", nargs="*", default=SYMBOLS,
                   help="نمادها — می‌تواند شامل نمادهایی باشد که فعلاً در bot.py لایو نیستند")
    p.add_argument("--tfs", nargs="*", default=TIMEFRAMES,
                   help="تایم‌فریم‌ها به‌دقیقه — هر مقدار پشتیبانی‌شده توسط Binance (1,3,5,15,30,60,120,240,...)")
    p.add_argument("--mode", choices=["full", "breakdown", "both"], default="full")
    p.add_argument("--engine", choices=["exact", "fast"], default="fast",
                   help="fast = پاس پیوسته + فیلتر پنجره‌ی لایو (پیش‌فرض) | exact = پنجره سرد هر کندل (خیلی کند)")
    p.add_argument("--window-clamp", type=int, default=HISTORY_BARS,
                   help="حداکثر عمر مجاز پیوت‌ها به کندل (پیش‌فرض ۵۰۰ مثل پنجره لایو | 0 = خاموش)")
    p.add_argument("--verify-sample", type=int, default=0,
                   help="نمونه‌گیری کنترلی: هر N-مین کندلِ غیرکاندید با پنجره سرد چک می‌شود (0 = خاموش)")
    p.add_argument("--signal-dump", type=int, default=5000,
                   help="آخرین N سیگنالِ هر ترکیب به‌صورت فایل کامل به تلگرام ارسال شود (0 = خاموش)")
    p.add_argument("--history-bars", type=int, default=HISTORY_BARS,
                   help=f"طول پنجره‌ی غلتان برای موتور exact (پیش‌فرض = HISTORY_BARS لایو = {HISTORY_BARS})")
    p.add_argument("--workers", type=int, default=max(1, min(4, (os.cpu_count() or 2) - 1)),
                   help="تعداد پردازه‌های موازی برای موتور exact")
    p.add_argument("--leverage", nargs="*", default=[],
                   help="بازنویسی اهرم برای نماد: SYMBOL=VALUE (مثلاً SOLUSDT=50)")
    p.add_argument("--tick", nargs="*", default=[],
                   help="بازنویسی tick size قیمت برای نماد: SYMBOL=VALUE (مثلاً SOLUSDT=0.001)")
    p.add_argument("--risk-free-fee-usd", type=float, default=0.0,
                   help="کارمزد تقریبی (دلار) برای نزدیک‌ترکردن ریسک‌فری به رفتار واقعی صرافی؛ پیش‌فرض ۰")
    p.add_argument("--account-sim", type=float, default=None,
                   help="اگر ست شود، یک شبیه‌سازی تکمیلی با موجودی شروع داده‌شده و فرمول واقعی position-sizing لایو اجرا می‌شود")
    p.add_argument("--force", action="store_true", help="نادیده‌گرفتن قفل روزانه")
    p.add_argument("--resend", action="store_true", help="ارسال مجدد از نتایج ذخیره‌شده")
    p.add_argument("--no-send", action="store_true", help="فقط چاپ/ذخیره، بدون تلگرام")
    return p.parse_args()


def main():
    args = parse_args()
    symbols = [s.upper() for s in args.symbols]
    tfs = [str(t) for t in args.tfs]
    leverage_overrides = _parse_kv_overrides(args.leverage)
    tick_overrides = _parse_kv_overrides(args.tick)
    history_bars = int(args.history_bars)

    try:
        if args.resend:
            trades, meta = load_results()
            if not trades:
                logger.error("نتایج ذخیره‌شده‌ای پیدا نشد")
                return 1
            logger.info(f"Resend از فایل ذخیره‌شده ({len(trades)} معامله)...")
            send_reports(trades, meta, args.mode, do_send=not args.no_send)
            return 0

        if (not args.force) and (not args.no_send) and marker_already_sent(args.mode):
            logger.info(f"گزارش '{args.mode}' امروز ({today_str()}) قبلاً ارسال شده. برای اجرای مجدد: --force")
            return 0

        # اطمینان از حضور صحیح اطلاعات هر نماد
        for sym in symbols:
            ensure_symbol_info(sym, tick_overrides, leverage_overrides)

        # اعتبارسنجی زودهنگام تایم‌فریم‌ها
        for tf in tfs:
            try:
                binance_interval_str(tf)
            except ValueError as e:
                logger.error(str(e))
                tg_send(f"❌ {e}")
                return 1

        now_ir = datetime.now(UTC_TZ).astimezone(IRAN_TZ)
        today_mid = now_ir.replace(hour=0, minute=0, second=0, microsecond=0)
        start_ir = today_mid - timedelta(days=max(1, args.days) - 1)
        start_ms = int(start_ir.timestamp() * 1000)
        end_ms = int(time.time() * 1000)
        meta = {
            "days": args.days, "symbols": symbols, "tfs": tfs,
            "start_date": start_ir.strftime("%Y-%m-%d"), "end_date": now_ir.strftime("%Y-%m-%d"),
            "generated_at": now_iran_str(), "engine": ENGINE_NAME, "engine_mode": args.engine,
            "window_clamp": args.window_clamp,
            "history_bars": history_bars, "const_source": CONST_SOURCE,
            "combos": [], "errors": [],
        }

        est_bars = sum(int(args.days) * 1440 // int(tf) for tf in tfs) * len(symbols)
        intro = (f"🚀 شروع بک‌تست استراتژی DTM\n"
                 f"🗓 {meta['start_date']} تا {meta['end_date']} ({meta['days']} روز — تهران)\n"
                 f"📡 {len(symbols)} ارز × {len(tfs)} تایم‌فریم\n"
                 f"📈 تخمین کندل‌ها: ~{est_bars:,}\n"
                 f"⚙️ موتور: {args.engine}"
                 + (f" (پنجره {history_bars} کندلی)" if args.engine == "exact"
                    else (f" (پیوسته + فیلتر پنجره {args.window_clamp} کندلی)" if args.window_clamp else " (پیوسته)"))
                 + "\n⏳ ممکن است زمان‌بر باشد...")
        logger.info(intro.replace("\n", " | "))
        if not args.no_send:
            tg_send(intro)

        all_trades = []
        total = len(tfs) * len(symbols)
        done = 0
        for tf in tfs:
            for sym in symbols:
                done += 1
                t0 = time.time()
                try:
                    def _progress(d, n_total, _sym=sym, _tf=tf, _done=done, _total=total, _t0=t0):
                        if n_total <= 0 or d == 0:
                            return
                        pct = d / n_total * 100
                        elapsed = time.time() - _t0
                        eta = elapsed / d * (n_total - d)
                        logger.info(
                            f"[{_done}/{_total}] {_sym} {_tf}m — {pct:.1f}٪ "
                            f"({d:,}/{n_total:,}) | ETA ~{eta/60:.1f} دقیقه"
                        )

                    trades, n_bars, raw_stats, diag = backtest_combo(
                        sym, tf, start_ms, end_ms, engine=args.engine,
                        history_bars=history_bars, workers=args.workers,
                        risk_free_fee_usd=args.risk_free_fee_usd,
                        progress_cb=_progress if args.engine == "exact" else None,
                        window_clamp=args.window_clamp,
                        verify_sample_n=args.verify_sample,
                        signal_dump_n=args.signal_dump,
                    )
                    elapsed = time.time() - t0
                    all_trades.extend(trades)
                    meta["control_checked_total"] = meta.get("control_checked_total", 0) + diag.get("control_checked", 0)
                    meta["control_found_total"] = meta.get("control_found_total", 0) + diag.get("control_found", 0)
                    meta["combos"].append({
                        "symbol": sym, "tf": tf, "bars": n_bars,
                        "raw_hits": raw_stats, "signals": len(trades),
                        "out_of_range": diag.get("out_of_range", 0),
                        "outside_window": diag.get("outside_window", 0),
                        "bad_sltp": diag.get("bad_sltp", 0),
                        "control_checked": diag.get("control_checked", 0),
                        "control_found": diag.get("control_found", 0),
                        "elapsed_sec": elapsed,
                        "signal_dump_path": diag.get("signal_dump_path"),
                        "signal_dump_count": diag.get("signal_dump_count", 0),
                    })
                    msg = (f"⏳ [{done}/{total}] {sym} {tf}m ✓ | "
                           f"کندل: {n_bars:,} | خام: {raw_stats.get('total', 0)} | "
                           f"خارج‌ازپنجره: {diag.get('outside_window', 0)} | "
                           f"معاملات: {len(trades)} | {elapsed:.0f}s"
                           + (f" | کنترلی: {diag.get('control_found', 0)}/{diag.get('control_checked', 0)}"
                              if diag.get("control_checked") else ""))
                except Exception as e:
                    meta["errors"].append(f"{sym} {tf}m: {e}")
                    logger.error(f"[COMBO] {sym} {tf}m failed: {e}\n{traceback.format_exc()}")
                    msg = f"⚠️ [{done}/{total}] {sym} {tf}m ✗ | {e}"
                logger.info(msg)
                if not args.no_send:
                    tg_send(msg)

        # ارسال فایل کامل سیگنال‌های اخیر هر ترکیب
        if args.signal_dump and not args.no_send:
            for c in meta["combos"]:
                p = c.get("signal_dump_path")
                if p and Path(p).exists():
                    tg_send_document(
                        p,
                        caption=f"📊 {c['symbol']} {c['tf']}m — {c.get('signal_dump_count', 0)} سیگنال اخیر (کامل، بدون برش)",
                    )
                    time.sleep(1)

        if args.account_sim is not None:
            meta["account_sim"] = simulate_with_account_balance(all_trades, args.account_sim)

        save_results(all_trades, meta)
        sent_ok = send_reports(all_trades, meta, args.mode, do_send=not args.no_send)
        if sent_ok and not args.no_send:
            marker_set(args.mode)
            tg_send(f"✅ بک‌تست تمام شد — {len(all_trades)} سیگنال پردازش شد.")
        return 0

    except KeyboardInterrupt:
        tg_send("⏹ بک‌تست توسط کاربر متوقف شد.")
        return 130
    except Exception as e:
        err = f"❌ خطای کلی بک‌تست: {type(e).__name__}: {e}\n{traceback.format_exc()[:1500]}"
        logger.error(err)
        tg_send(err)
        return 1


if __name__ == "__main__":
    try:
        if mp.get_start_method(allow_none=True) is None:
            mp.set_start_method("fork" if sys.platform != "win32" else "spawn")
    except Exception:
        pass
    sys.exit(main())
