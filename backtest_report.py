#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest_report.py
===================
بک‌تستِ «exact / event-driven» استراتژیِ DTM — دقیقاً بر پایهٔ همان کدی که در
لایو سیگنال می‌سازد (strategy_wrapper.calculate_signals → strategy.py از طریق
PyneCore ScriptRunner، و trade_ledger برای فرمول PnL) اجرا می‌شود.

طبق سند طراحی (بخش ۲ — «یک کد، دو مصرف‌کننده»): این فایل هیچ منطق تصمیم‌گیریِ
مستقلی ندارد. سیگنال، استاپ/تارگت، و فرمول PnL همگی import مستقیم از
strategy_wrapper.py / trade_ledger.py هستند؛ چیزی کپی/بازنویسی نشده. اگر فردا
در آن فایل‌ها چیزی عوض شود، این بک‌تست خودکار هماهنگ می‌شود.

⚠️ نمادها/تایم‌فریم‌ها/لوریج/تیک‌سایز اینجا (بخش ۱ زیر) به‌صورت مستقل از
bot.py تعیین می‌شوند — یعنی bot.py اصلاً import نمی‌شود و اجرای لایو روی
Railway هیچ تأثیری روی این بک‌تست ندارد. برای تغییرشان مستقیماً همان بخش را
ویرایش کن (یا از --symbols/--timeframes در خط فرمان استفاده کن).

📣 اعلانِ تلگرام: تمامِ پیام‌های وضعیتِ این بک‌تست (شروع، تخمینِ زمان، خلاصهٔ
قابلیت‌ها، پایانِ هر ترکیبِ نماد/تایم‌فریم، پایانِ هر نماد، گزارشِ نهایی) به یک
رباتِ تلگرامِ کاملاً جدا و مستقل از رباتِ لایو ارسال می‌شوند — از طریقِ
BACKTEST_TELEGRAM_BOT_TOKEN / BACKTEST_TELEGRAM_CHAT_ID (متغیرِ محیطی). این
هیچ ربطی به _send_telegram داخلِ strategy_wrapper.py ندارد و پیام‌های لحظه‌ایِ
خودِ calculate_signals همچنان (طبق قبل) در بک‌تست خاموش نگه داشته می‌شوند تا
اسپم نشود — جزئیات در بخش ۱-الف.

🔒 قفلِ تک‌اجرایی: کلِ این بک‌تست فقط یک‌بار در هر «استارتِ» فرآیند باید اجرا
شود. این با یک فایلِ قفل تضمین می‌شود — جزئیات و ⚠️ محدودیتِ مهمِ آن (در برابرِ
ری‌استارتِ واقعیِ سرویس/کانتینر محافظت نمی‌کند) در بخش ۱-ب.

نحوهٔ اجرا (نمونه):
    python backtest_report.py --from 2024-01-01 --to 2025-01-01
    python backtest_report.py --symbols BNBUSDT,ETHUSDT --timeframes 1,5
    python backtest_report.py --from 2024-06-01 --to 2024-09-01 --robust
    python backtest_report.py --engine fast   # ⚠️ فقط برای مقایسهٔ سریع؛ هرگز پیش‌فرض نیست

فایل‌های strategy.py / strategy_wrapper.py / trade_ledger.py باید در همان
پوشه (یا در PYTHONPATH) کنار این فایل باشند — دقیقاً همان منطقی که در Railway
دیپلوی شده (bot.py خودش لازم نیست، فقط این سه فایل).

متغیرهای محیطیِ لازم برای اعلانِ تلگرام (رباتِ جدید، جدا از رباتِ لایو):
    BACKTEST_TELEGRAM_BOT_TOKEN   ← توکنِ رباتِ جدید از BotFather
    BACKTEST_TELEGRAM_CHAT_ID     ← chat_id مقصد (کاربر/گروه/کانال)
اگر این دو ست نشوند، بک‌تست بدون کرش ادامه می‌یابد؛ فقط یک هشدار در لاگ
چاپ می‌شود و هیچ پیامی ارسال نمی‌شود.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import math
import os
import statistics
import sys
import time as _time_mod
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

UTC = timezone.utc
IRAN_TZ = timezone(timedelta(hours=3, minutes=30))

# ============================================================================
# بازهٔ زمانیِ پیش‌فرضِ بک‌تست — هر وقت خواستی همین دو رشته را عوض کن
# (فرمت: "YYYY-MM-DD"). اگر موقع اجرا --from/--to بدهی، همان‌ها اولویت دارند
# و این پیش‌فرض‌ها نادیده گرفته می‌شوند.
# ============================================================================
DEFAULT_DATE_FROM = "2024-09-08"
DEFAULT_DATE_TO = "2025-09-08"

logging.basicConfig(
    level=logging.WARNING,  # جزئیاتِ لایو (INFO) خیلی پرحجم است؛ فقط بالاتر از این را روی کنسول نشان بده.
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("BACKTEST")


# ============================================================================
# ۱) اتصال زنده به کدهای لایو — «یک کد، دو مصرف‌کننده» (سند، بخش ۲)
#    هیچ‌کدام از این‌ها اینجا کپی نمی‌شوند؛ مستقیماً از ماژول‌های واقعی
#    خوانده می‌شوند تا هر تغییری در آن‌ها خودکار در بک‌تست منعکس شود.
# ============================================================================

CONST_SOURCE = "دستی — مستقل از bot.py (تعیین‌شده در خود backtest_report.py)"

# ============================================================================
# نمادها/تایم‌فریم‌ها/لوریج/تیک‌سایز اینجا به‌صورت مستقل از bot.py (لایو)
# تعیین می‌شوند. هر تغییری در bot.py روی این مقادیر هیچ اثری ندارد.
# ============================================================================
SYMBOLS: list[str] = ["BNBUSDT", "ETHUSDT", "SOLUSDT"]          # ← نمادهای موردنظر خودت
TIMEFRAMES: list[str] = ["1"]                  # ← تایم‌فریم‌ها (دقیقه، رشته)
HISTORY_BARS: int = 500                                         # ← تعداد کندلِ هر پنجره

LEVERAGE_MAP: dict = {"BNBUSDT": 75, "ETHUSDT": 50, "SOLUSDT": 60}
TICK_SIZES: dict = {"BNBUSDT": 0.01, "ETHUSDT": 0.01, "SOLUSDT": 0.001}

MIN_ORDER_COST_USDT: float = 5.0
_BINANCE_BASES = ["https://data-api.binance.vision", "https://api.binance.com"]

LOGIC_SOURCE_OK = True
_logic_import_error: Optional[str] = None
_original_send_telegram = None  # مرجعِ تابعِ ارسالِ تلگرامِ خودِ strategy_wrapper (دیگر برای اعلاناتِ این فایل استفاده نمی‌شود؛ فقط برای رفرنس نگه داشته شده)
try:
    import strategy_wrapper as _sw  # noqa: E402
    import trade_ledger as _tl  # noqa: E402

    from trade_ledger import _hypothetical_pnl_usd as ledger_pnl_usd  # noqa: E402
    from trade_ledger import BASE_CAPITAL  # noqa: E402

    # مرجعِ اصلیِ تابعِ ارسالِ تلگرامِ لایو را نگه می‌داریم (صرفاً برای رفرنس/دیباگ)،
    # ولی اعلاناتِ این فایل دیگر از آن استفاده نمی‌کنند — به یک رباتِ کاملاً
    # جدا و مستقل می‌روند (بخشِ notify_telegram پایین‌تر).
    _original_send_telegram = getattr(_sw, "_send_telegram", None)

    # جلوگیری از اسپم تلگرام: strategy_wrapper به‌ازای هر سیگنال/خطا پیام
    # می‌فرستد. در بک‌تست ممکن است هزاران کندل پردازش شود — این باید خاموش شود
    # بدون این‌که هیچ منطقِ تصمیم‌گیری تغییر کند (فقط کانال ارسال، نه محاسبه).
    _sw._send_telegram = lambda *a, **k: True  # type: ignore

    # نمادهای جدیدی که در SYMBOL_TICK_INFO خودِ strategy_wrapper.py نیستند را
    # اینجا runtime تزریق می‌کنیم، وگرنه با mintick پیش‌فرض 0.01 محاسبه می‌شوند
    # (که برای نمادهایی با تیک متفاوت باعث محاسبهٔ اشتباهِ استاپ/تارگت می‌شود).
    for _sym, _tick in TICK_SIZES.items():
        if _sym not in _sw.SYMBOL_TICK_INFO:
            _sw.SYMBOL_TICK_INFO[_sym] = {
                "mintick": _tick,
                "pricescale": int(round(1 / _tick)),
                "basecurrency": _sym.replace("USDT", ""),
            }
except Exception as e:
    LOGIC_SOURCE_OK = False
    _logic_import_error = f"{type(e).__name__}: {e}"

if not LOGIC_SOURCE_OK:
    # طبق خواستهٔ ۱ کاربر («دقیقاً همان‌طور که در لایو محاسبه می‌شود»)، بدون
    # این import، ادامهٔ کار به‌معنیِ شبیه‌سازیِ مستقل (=دقیقاً همان چیزی که رد
    # شد) خواهد بود. پس با پیام روشن متوقف می‌شویم، نه سقوط بی‌صدا.
    sys.stderr.write(
        "\n❌ FATAL: نمی‌توان strategy_wrapper.py / trade_ledger.py را import کرد:\n"
        f"   {_logic_import_error}\n\n"
        "طبق اصل «یک کد، دو مصرف‌کننده» (سند طراحی، بخش ۲)، این بک‌تست هرگز منطق "
        "سیگنال/PnL را بازنویسی نمی‌کند. مطمئن شوید strategy.py و strategy_wrapper.py "
        "و trade_ledger.py (با همین نام‌ها) کنار این فایل هستند و pynecore نصب است "
        "(pip install pynecore).\n"
    )
    sys.exit(1)


# ============================================================================
# ۱-الف) اعلانِ تلگرام — رباتِ کاملاً جدا و مستقل از رباتِ لایو
#    این تابع دیگر به هیچ‌وجه به _send_telegram داخلِ strategy_wrapper وابسته
#    نیست (که در بالا هم‌زمان به no-op تبدیل شده تا اسپمِ لحظه‌ایِ سیگنال‌ها
#    خاموش شود). اینجا مستقیماً با requests به Bot API تلگرام زده می‌شود، با
#    توکن/چت‌آیدیِ یک رباتِ تازه که فقط برای وضعیتِ بک‌تست استفاده می‌شود.
# ============================================================================
BACKTEST_TELEGRAM_BOT_TOKEN = os.environ.get("BACKTEST_TELEGRAM_BOT_TOKEN", "8681448214:AAG4Ve-8GUTtQQS3wb5V9FDcuTeOoGbA4oM").strip()
BACKTEST_TELEGRAM_CHAT_ID = os.environ.get("BACKTEST_TELEGRAM_CHAT_ID", "7402770612").strip()
_TELEGRAM_API_BASE = "https://api.telegram.org"
_TELEGRAM_MSG_LIMIT = 4000  # مرزِ ایمن زیرِ سقفِ ۴۰۹۶ کاراکتریِ تلگرام برایِ sendMessage
_telegram_config_warned = False


def _telegram_configured() -> bool:
    """چک می‌کند که توکن/چت‌آیدیِ رباتِ جدید ست شده‌اند. اگر نه، فقط یک‌بار در
    کلِ اجرا هشدار می‌دهد (نه به‌ازای هر پیام) تا لاگ شلوغ نشود."""
    global _telegram_config_warned
    ok = bool(BACKTEST_TELEGRAM_BOT_TOKEN and BACKTEST_TELEGRAM_CHAT_ID)
    if not ok and not _telegram_config_warned:
        logger.warning(
            "⚠️ BACKTEST_TELEGRAM_BOT_TOKEN و/یا BACKTEST_TELEGRAM_CHAT_ID تنظیم نشده؛ "
            "هیچ پیامی به تلگرام ارسال نمی‌شود. این دو را به‌عنوانِ متغیرِ محیطی ست کنید "
            "(BotFather → توکن، @userinfobot یا افزودنِ ربات به گروه/کانال → chat_id)."
        )
        _telegram_config_warned = True
    return ok


def notify_telegram(message: str) -> bool:
    """
    ارسالِ پیامِ متنیِ وضعیتِ بک‌تست به رباتِ تلگرامِ جدید (شروع/تخمینِ زمان/
    خلاصهٔ قابلیت‌ها/پایانِ هر نماد-تایم‌فریم/گزارشِ نهایی). کاملاً مستقل از
    رباتِ لایو است. هرگز نباید کلِ اجرای بک‌تست را متوقف کند — اگر ارسال شکست
    بخورد، فقط در لاگ ثبت می‌شود، نه یک Exception که کلِ اسکریپت را بترکاند.
    پیام‌های طولانی‌تر از سقفِ تلگرام به‌صورتِ خودکار تکه‌تکه ارسال می‌شوند.
    """
    if not _telegram_configured():
        return False
    ok_all = True
    chunks = [message[i:i + _TELEGRAM_MSG_LIMIT] for i in range(0, len(message), _TELEGRAM_MSG_LIMIT)] or [message]
    for chunk in chunks:
        try:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{BACKTEST_TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": BACKTEST_TELEGRAM_CHAT_ID, "text": chunk},
                timeout=15,
            )
            if resp.status_code != 200:
                logger.warning(f"ارسالِ پیامِ تلگرام شکست خورد ({resp.status_code}): {resp.text[:300]}")
                ok_all = False
        except Exception as e:
            logger.warning(f"ارسالِ پیامِ تلگرام شکست خورد: {e}")
            ok_all = False
    return ok_all


def notify_telegram_document(file_path, caption: str = "") -> bool:
    """
    ارسالِ یک فایل (txt/xlsx/...) به همان رباتِ تلگرامِ جدید — برای گزارشِ
    نهاییِ ۷ روزِ اخیرِ تایم‌فریمِ ۱ دقیقه. هرگز اجرای بک‌تست را متوقف نمی‌کند.
    """
    if not _telegram_configured():
        return False
    try:
        with open(file_path, "rb") as f:
            resp = requests.post(
                f"{_TELEGRAM_API_BASE}/bot{BACKTEST_TELEGRAM_BOT_TOKEN}/sendDocument",
                data={"chat_id": BACKTEST_TELEGRAM_CHAT_ID, "caption": caption[:1024]},
                files={"document": (Path(file_path).name, f)},
                timeout=60,
            )
        if resp.status_code != 200:
            logger.warning(f"ارسالِ فایل به تلگرام شکست خورد ({resp.status_code}): {resp.text[:300]}")
            return False
        return True
    except Exception as e:
        logger.warning(f"ارسالِ فایل به تلگرام شکست خورد: {e}")
        return False


# ============================================================================
# ۱-ب) قفلِ تک‌اجراییِ فرآیند
#    کلِ این بک‌تست باید فقط یک‌بار در هر «استارت» اجرا شود، نه دوباره. این
#    فایل به‌عنوانِ نشانگرِ «این فرآیند/کانتینر قبلاً یک‌بار بک‌تستِ کامل را
#    شروع کرده» عمل می‌کند.
#
#    ⚠️ محدودیتِ صادقانه (حتماً به آن توجه کن): این قفل صرفاً یک فایل روی
#    دیسکِ همین کانتینر است. اگر سرویس (مثلاً روی Railway) واقعاً ری‌استارت
#    شود، یک فرآیند/کانتینرِ *جدید* بالا می‌آید، فایلِ قفل هم به‌طورِ طبیعی از
#    بین می‌رود (مگر این‌که روی یک volume دائمی mount شده باشد) — یعنی با هر
#    ری‌استارتِ واقعیِ سرویس، بک‌تست دوباره از اول اجرا خواهد شد. این قفل فقط
#    جلوی «فراخوانیِ تصادفیِ دوبارهٔ main() در طولِ عمرِ همان یک فرآیند»
#    (مثلاً به‌خاطرِ باگ یا retry logic) را می‌گیرد، نه جلوی خودِ ری‌استارتِ
#    سرویس/کانتینر را.
# ============================================================================
RUN_LOCK_FILE = BASE_DIR / ".backtest_run.lock"


# ============================================================================
# ۲) نگاشتِ صریحِ تایم‌فریم → interval بایننس (رفع باگ #۳ در سند)
# ============================================================================
BINANCE_INTERVAL_MAP = {
    "1": "1m", "3": "3m", "5": "5m", "15": "15m", "30": "30m",
    "60": "1h", "120": "2h", "240": "4h", "360": "6h", "480": "8h",
    "720": "12h", "1440": "1d", "4320": "3d", "10080": "1w",
}


def to_binance_interval(timeframe: str) -> str:
    tf = str(timeframe)
    if tf in BINANCE_INTERVAL_MAP:
        return BINANCE_INTERVAL_MAP[tf]
    # هیچ حدسِ بی‌صدا: اگر تایم‌فریم ناشناخته بود، صریحاً log و بهترین حدسِ
    # معقول (n دقیقه) را برگردان — ولی در گزارش به‌عنوان "نگاشتِ حدسی" علامت زده می‌شود.
    logger.warning(f"⚠️ تایم‌فریم {tf} در BINANCE_INTERVAL_MAP نیست؛ حدسِ '{tf}m' استفاده می‌شود.")
    return f"{tf}m"


UNMAPPED_TIMEFRAME_GUESSES: set[str] = set()


def to_binance_interval_tracked(timeframe: str) -> str:
    tf = str(timeframe)
    if tf not in BINANCE_INTERVAL_MAP:
        UNMAPPED_TIMEFRAME_GUESSES.add(tf)
    return to_binance_interval(tf)


# ============================================================================
# ۳) بازهٔ «سیگنال‌های اخیر» متناسب با تایم‌فریم (سند، بخش ۷)
#    ⚠️ این جدول فقط برای دو نقطه (1m, 5m) صریحاً از کاربر گرفته شده؛ بقیه
#    برون‌یابی است و باید در گزارش صریحاً به‌عنوان "نیازمند تأیید" علامت بخورد.
# ============================================================================
RECENT_SIGNALS_CALENDAR_DAYS_CONFIRMED = {"1": 7, "5": 22}
RECENT_SIGNALS_CALENDAR_DAYS_PROPOSED = {
    "1": 7, "5": 22, "15": 45, "30": 75, "60": 120, "240": 240,
}


def recent_window_days(timeframe: str) -> tuple[int, bool]:
    """برمی‌گرداند (تعداد روز, آیا این عدد تاییدشده توسط کاربر است یا برون‌یابی‌شده)."""
    tf = str(timeframe)
    if tf in RECENT_SIGNALS_CALENDAR_DAYS_CONFIRMED:
        return RECENT_SIGNALS_CALENDAR_DAYS_CONFIRMED[tf], True
    if tf in RECENT_SIGNALS_CALENDAR_DAYS_PROPOSED:
        return RECENT_SIGNALS_CALENDAR_DAYS_PROPOSED[tf], False
    # برون‌یابیِ خطیِ لگاریتمی بین دو نقطهٔ تاییدشده (1m→7d , 5m→22d) روی مقیاسِ
    # log(minutes) تا برای هر تایم‌فریمِ جدید/ناشناخته هم عددی معقول (نه خطا) بدهد.
    try:
        tf_min = int(tf)
        x1, y1 = 1.0, 7.0
        x5, y5 = 5.0, 22.0
        slope = (math.log(y5) - math.log(y1)) / (math.log(x5) - math.log(x1))
        days = math.exp(math.log(y1) + slope * (math.log(tf_min) - math.log(x1)))
        return max(1, round(days)), False
    except Exception:
        return 30, False


def utc_ms(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return int(dt.astimezone(UTC).timestamp() * 1000)


def ms_to_dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000.0, tz=UTC)


# ============================================================================
# ۴) دریافت دادهٔ کامل تاریخی از بایننس (chunked)، مقاوم در برابر خطای شبکه
# ============================================================================
KLINES_LIMIT = 1000  # حداکثر مجاز بایننس هر درخواست


def fetch_klines_chunk(base: str, symbol: str, interval: str, start_ms: int, end_ms: int,
                        limit: int = KLINES_LIMIT, timeout: float = 20.0) -> list:
    url = (
        f"{base}/api/v3/klines?symbol={symbol.upper()}&interval={interval}"
        f"&startTime={start_ms}&endTime={end_ms}&limit={limit}"
    )
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_full_history(symbol: str, timeframe: str, start_dt: datetime, end_dt: datetime,
                        max_retries: int = 4) -> pd.DataFrame:
    """
    کل تاریخچهٔ OHLCV بین start_dt/end_dt را در chunkهای ۱۰۰۰تایی از بایننس
    می‌گیرد. مقاوم است: خطای شبکه/چانکِ خالی هرگز کل اجرا را متوقف نمی‌کند —
    فقط آن بازه را در گزارشِ «شکاف‌های داده» ثبت می‌کند (بند ۳ سند: مقاومت در
    برابر هر باگ، بدون توقف کامل یا سکوت).
    """
    interval = to_binance_interval_tracked(timeframe)
    tf_minutes = int(timeframe)
    step_ms = tf_minutes * 60 * 1000

    start_ms = utc_ms(start_dt)
    end_ms = utc_ms(end_dt)

    all_rows = []
    gaps: list[tuple[int, int, str]] = []
    cursor = start_ms
    bases = list(_BINANCE_BASES)

    while cursor < end_ms:
        chunk_end = min(cursor + KLINES_LIMIT * step_ms, end_ms)
        rows = None
        last_err = None
        for base in bases:
            for attempt in range(max_retries):
                try:
                    rows = fetch_klines_chunk(base, symbol, interval, cursor, chunk_end)
                    break
                except Exception as e:
                    last_err = e
                    _time_mod.sleep(min(2 ** attempt, 8) * 0.5)
            if rows is not None:
                break
        if rows is None:
            gaps.append((cursor, chunk_end, f"network_error: {last_err}"))
            logger.error(f"[{symbol} {timeframe}m] شکافِ داده {ms_to_dt(cursor)}→{ms_to_dt(chunk_end)}: {last_err}")
            cursor = chunk_end
            continue
        if not rows:
            # چانکِ خالی طبیعی است (مثلاً نماد هنوز روی بایننس لیست نشده بود)
            gaps.append((cursor, chunk_end, "no_data_returned"))
            cursor = chunk_end
            continue

        all_rows.extend(rows)
        last_open = rows[-1][0]
        cursor = last_open + step_ms
        if len(rows) < 2:
            cursor = chunk_end  # جلوگیری از حلقهٔ بی‌نهایت روی چانکِ تک‌سطری

    if not all_rows:
        logger.warning(f"[{symbol} {timeframe}m] هیچ کندلی دریافت نشد.")
        df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        df.attrs["gaps"] = gaps
        df.attrs["source"] = "binance"
        return df

    t = [row[0] / 1000.0 for row in all_rows]
    df = pd.DataFrame(
        {
            "open": pd.to_numeric([r[1] for r in all_rows], errors="coerce"),
            "high": pd.to_numeric([r[2] for r in all_rows], errors="coerce"),
            "low": pd.to_numeric([r[3] for r in all_rows], errors="coerce"),
            "close": pd.to_numeric([r[4] for r in all_rows], errors="coerce"),
            "volume": pd.to_numeric([r[5] for r in all_rows], errors="coerce"),
        },
        index=pd.to_datetime(t, unit="s", utc=True),
    )
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    n_before = len(df)
    df = df.dropna(subset=["open", "high", "low", "close"])
    if len(df) < n_before:
        logger.warning(f"[{symbol} {timeframe}m] {n_before - len(df)} کندلِ ناقص (NaN) حذف شد.")

    df.attrs["gaps"] = gaps
    df.attrs["source"] = "binance"
    return df


# کش سراسریِ دادهٔ ۱-دقیقه‌ای برای حل ابهامِ استاپ/تارگتِ هم‌کندل (سند، بخش ۴)
_ONE_MIN_CACHE: dict[str, pd.DataFrame] = {}


def get_1m_slice(symbol: str, start_ms: int, end_ms: int) -> Optional[pd.DataFrame]:
    """
    دادهٔ ۱-دقیقه‌ایِ واقعی برای بازهٔ [start_ms, end_ms] را برمی‌گرداند (برای
    تشخیص این‌که در یک کندلِ تایم‌فریمِ بالاتر، استاپ یا تارگت واقعاً کدام‌یک
    زودتر لمس شده). کل روزِ حاویِ این بازه کش می‌شود تا معاملات هم‌پوشان
    دوباره از بایننس گرفته نشوند.
    """
    day_key = f"{symbol}:{ms_to_dt(start_ms).strftime('%Y-%m-%d')}"
    day_start = int(datetime(ms_to_dt(start_ms).year, ms_to_dt(start_ms).month, ms_to_dt(start_ms).day, tzinfo=UTC).timestamp() * 1000)
    day_end = day_start + 24 * 3600 * 1000

    if day_key not in _ONE_MIN_CACHE:
        try:
            df_day = fetch_full_history(symbol, "1", ms_to_dt(day_start), ms_to_dt(day_end))
        except Exception as e:
            logger.warning(f"[{symbol}] دریافت دادهٔ ۱m برای {day_key} شکست خورد: {e}")
            df_day = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        _ONE_MIN_CACHE[day_key] = df_day
        # جلوگیری از رشدِ نامحدود حافظه در بک‌تست‌های خیلی طولانی
        if len(_ONE_MIN_CACHE) > 400:
            oldest = sorted(_ONE_MIN_CACHE.keys())[0]
            _ONE_MIN_CACHE.pop(oldest, None)

    df_day = _ONE_MIN_CACHE[day_key]
    if df_day.empty:
        return None
    idx_ms = (df_day.index.values.astype("datetime64[ns]").view("int64") // 10 ** 6)
    mask = (idx_ms >= start_ms) & (idx_ms < end_ms)
    sub = df_day.loc[mask]
    return sub if not sub.empty else None


# ============================================================================
# ۵) ضبطِ کاملِ لاگِ الگوریتمی هر سیگنال — بدون بازنویسیِ منطق (سند، بند ۹)
#    strategy_wrapper خودش لاگ‌های بسیار مفصلی می‌فرستد (DIVCHECK, SIGNAL_TRACE,
#    SL/TP, RISK-FREE, ...). به‌جای استخراجِ دستیِ last_values (که یعنی دوباره
#    دست‌کاریِ داخلِ calculate_signals)، یک هندلرِ موقتِ لاگ را به لاگرِ
#    STRATEGY_WRAPPER وصل می‌کنیم و همان خروجیِ واقعی را ذخیره می‌کنیم.
# ============================================================================
class _ListLogHandler(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.records: list[str] = []

    def emit(self, record):
        try:
            self.records.append(self.format(record))
        except Exception:
            pass


@contextlib.contextmanager
def capture_algo_log():
    handler = _ListLogHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s"))
    target_logger = logging.getLogger("STRATEGY_WRAPPER")
    prev_level = target_logger.level
    target_logger.addHandler(handler)
    target_logger.setLevel(logging.DEBUG)
    try:
        yield handler
    finally:
        target_logger.removeHandler(handler)
        target_logger.setLevel(prev_level)


# ============================================================================
# ۶) موتورِ سیگنالِ exact / event-driven (سند، بخش ۳) — تنها موتورِ معتبر
# ============================================================================
@dataclass
class SignalEvent:
    symbol: str
    timeframe: str
    signal: str                 # "LONG" | "SHORT"
    entry: float
    stop: float
    target: Optional[float]
    signal_bar_ts_ms: int
    risk_free_pct: Optional[float]
    algo_log: str = ""          # لاگِ کاملِ محاسباتیِ همان لحظه (بند ۹ سند)
    window_len: int = 0


def _build_ohlcv_window(df_full: pd.DataFrame, end_idx: int, history_bars: int) -> pd.DataFrame:
    """دقیقاً همان چیزی که bot.py هر چرخه از بایننس می‌گیرد: آخرین history_bars
    کندلِ منتهی به کندلِ end_idx (شامل خودش)."""
    start_idx = max(0, end_idx - history_bars + 1)
    return df_full.iloc[start_idx:end_idx + 1]


def _run_calculate_signals_capture(df_window: pd.DataFrame, symbol: str, timeframe: str):
    """صدا زدنِ مستقیمِ calculate_signals لایو + ضبطِ کاملِ لاگِ همان اجرا."""
    with capture_algo_log() as handler:
        try:
            result = _sw.calculate_signals(df_window, symbol=symbol, timeframe=timeframe)
        except Exception:
            # طبق بند ۳ سند: هیچ باگی نباید کل اجرا را متوقف کند.
            tb = traceback.format_exc()
            handler.records.append(f"EXCEPTION در calculate_signals:\n{tb}")
            result = (None, None, None, None, None, None)
        algo_log = "\n".join(handler.records)
    return result, algo_log


def _process_single_bar(df_full: pd.DataFrame, i: int, symbol: str, timeframe: str,
                         history_bars: int, keep_log: bool = True):
    window = _build_ohlcv_window(df_full, i, history_bars)
    if len(window) < 50:
        return None  # همان آستانهٔ calculate_signals؛ صرفاً صرفه‌جویی در محاسبه
    (signal, entry, stop, target, signal_bar_ts_ms, risk_free_pct), algo_log = \
        _run_calculate_signals_capture(window, symbol, timeframe)
    if signal not in ("LONG", "SHORT") or entry is None or stop is None:
        return None
    return SignalEvent(
        symbol=symbol, timeframe=str(timeframe), signal=signal,
        entry=float(entry), stop=float(stop),
        target=float(target) if target is not None else None,
        signal_bar_ts_ms=int(signal_bar_ts_ms) if signal_bar_ts_ms is not None else int(window.index[-1].timestamp() * 1000),
        risk_free_pct=float(risk_free_pct) if risk_free_pct is not None else None,
        algo_log=algo_log if keep_log else "",
        window_len=len(window),
    )


def _worker_process_range(pickled_args):
    """تابعِ سطحِ ماژول برای ProcessPoolExecutor (باید pickle‌پذیر باشد).
    هر پردازه بازهٔ [lo, hi) از ایندکسِ کندل‌ها را پردازش می‌کند."""
    (df_full, lo, hi, symbol, timeframe, history_bars, keep_log) = pickled_args
    out = []
    for i in range(lo, hi):
        ev = _process_single_bar(df_full, i, symbol, timeframe, history_bars, keep_log)
        if ev is not None:
            out.append(ev)
    return out


def generate_signals_exact(df_full: pd.DataFrame, symbol: str, timeframe: str,
                            history_bars: int = HISTORY_BARS,
                            workers: int = 1, keep_log: bool = True,
                            progress_label: str = "") -> list[SignalEvent]:
    """
    موتورِ اصلیِ بک‌تست: برای هر کندلِ بسته‌شده، دقیقاً همان محاسبه‌ای که
    bot.py در آن لحظه انجام می‌داد را دوباره اجرا می‌کند (نه شبیه‌سازیِ
    مستقل). چون هر پنجره کاملاً مستقل است، «embarrassingly parallel» است.
    """
    n = len(df_full)
    if n < 50:
        return []

    if workers and workers > 1:
        try:
            chunks = []
            chunk_size = max(1, math.ceil(n / workers))
            for lo in range(0, n, chunk_size):
                hi = min(n, lo + chunk_size)
                chunks.append((df_full, lo, hi, symbol, timeframe, history_bars, keep_log))
            events: list[SignalEvent] = []
            with ProcessPoolExecutor(max_workers=workers) as ex:
                futures = [ex.submit(_worker_process_range, c) for c in chunks]
                for fut in as_completed(futures):
                    events.extend(fut.result())
            events.sort(key=lambda e: e.signal_bar_ts_ms)
            return events
        except Exception as e:
            # سقوط امنِ اجباری به تک‌پردازه‌ای (سند، بخش ۳) — کندتر ولی امن
            logger.warning(f"[{symbol} {timeframe}m] موازی‌سازی شکست خورد ({e})؛ سقوط به تک‌پردازه‌ای.")

    events = []
    for i in range(n):
        ev = _process_single_bar(df_full, i, symbol, timeframe, history_bars, keep_log)
        if ev is not None:
            events.append(ev)
    return events


# ============================================================================
# ۷) چکِ Determinism (سند، بخش ۳) — دوباره‌محاسبهٔ زیرمجموعه‌ای کوچک و
#    مطمئن‌شدن از این‌که عدد یکسان می‌گیریم (کشفِ باگِ حالتِ مشترک/کش اشتباه)
# ============================================================================
def determinism_check(df_full: pd.DataFrame, symbol: str, timeframe: str,
                       history_bars: int, sample_size: int = 20) -> dict:
    n = len(df_full)
    if n < 60:
        return {"checked": 0, "mismatches": 0, "ok": True, "note": "دادهٔ کافی برای چک نبود."}
    import random
    random.seed(1234)  # نتیجهٔ چک باید خودش هم determinism داشته باشد
    idxs = random.sample(range(50, n), min(sample_size, n - 50))
    mismatches = []
    for i in idxs:
        first, _log1 = _run_calculate_signals_capture(_build_ohlcv_window(df_full, i, history_bars), symbol, timeframe)
        second, _log2 = _run_calculate_signals_capture(_build_ohlcv_window(df_full, i, history_bars), symbol, timeframe)
        # مقایسهٔ ۴ مقدارِ اولِ خروجی (signal, entry, stop, target)
        if first[:4] != second[:4]:
            mismatches.append({"bar_index": i, "run1": first[:4], "run2": second[:4]})
    return {
        "checked": len(idxs),
        "mismatches": len(mismatches),
        "ok": len(mismatches) == 0,
        "details": mismatches[:10],
    }


# ============================================================================
# ۸) ابزارِ خودتشخیصیِ لوک‌اِهد (سند، بخش ۳؛ الهام از freqtrade lookahead-analysis)
#    اختیاری (--lookahead-check) چون سنگین است: هر سیگنالِ یافته‌شده را با یک
#    پنجرهٔ کوتاه‌ترشده (بریدنِ آخرین کندل) دوباره محاسبه می‌کند.
# ============================================================================
def lookahead_check(df_full: pd.DataFrame, events: list[SignalEvent], symbol: str,
                     timeframe: str, history_bars: int, max_checks: int = 200,
                     rel_tol: float = 0.02) -> dict:
    """
    ⚠️ محدودیتِ صادقانه: چون calculate_signals فقط وضعیتِ آخرینِ کندلِ هر پنجره
    را برمی‌گرداند (نه سری‌ای از تمامِ کندل‌های میانی)، تست کلاسیکِ
    freqtrade lookahead-analysis (که به وضعیتِ *هر* کندل در یک اجرایِ طولانی
    نیاز دارد) از پشتِ این API قابل‌اجرا نیست، بدون این‌که به داخلِ
    calculate_signals دست زده شود — که طبق سند (بخش ۲) ممنوع است.

    به‌جای آن، این تابع فقط یک چکِ ضعیف‌تر ولی صادقانه انجام می‌دهد:
    «حساسیت به طولِ تاریخچه» — همان کندلِ سیگنال را با یک تاریخچهٔ کمی
    کوتاه‌تر (ولی هنوز به همان کندل ختم می‌شود) دوباره محاسبه می‌کند. تغییرِ
    جزئیِ اعداد به‌خاطرِ warm-upِ متفاوتِ اندیکاتورها طبیعی است و باگ نیست؛
    آنچه واقعاً مشکوک است فقط **تغییرِ جهتِ سیگنال** (LONG↔SHORT↔هیچ) است.
    بنابراین «مشکوک» در خروجیِ این تابع به‌معنیِ «اثباتِ لوک‌اِهد» نیست، فقط
    نشانه‌ای برای بررسیِ بیشتر است.
    """
    ts_to_idx = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_full.index)}
    suspicious = []
    checked = 0
    shorter_hist = max(60, int(history_bars * 0.8))
    for ev in events[:max_checks]:
        i = ts_to_idx.get(ev.signal_bar_ts_ms)
        if i is None:
            continue
        alt_window = _build_ohlcv_window(df_full, i, shorter_hist)
        if len(alt_window) < 50:
            continue
        (sig_alt, entry_alt, stop_alt, target_alt, _, _), _ = _run_calculate_signals_capture(alt_window, symbol, timeframe)
        checked += 1
        direction_flipped = sig_alt != ev.signal  # این تنها معیارِ واقعاً معنادار است
        if direction_flipped:
            suspicious.append({
                "bar_ts_ms": ev.signal_bar_ts_ms,
                "original_signal": ev.signal,
                "signal_with_shorter_history": sig_alt,
                "note": f"جهتِ سیگنال با تاریخچهٔ {shorter_hist} کندلی به‌جای {history_bars} کندلی عوض شد.",
            })
    return {
        "checked": checked, "suspicious": len(suspicious), "details": suspicious[:10],
        "caveat": "این چک فقط تغییرِ جهتِ سیگنال را می‌سنجد، نه لوک‌اِهدِ واقعی را اثبات می‌کند (به محدودیتِ بالا نگاه کنید).",
    }


# ============================================================================
# ۹) حلِ قطعیِ ابهامِ «استاپ/تارگت در یک کندل» (سند، بخش ۴)
# ============================================================================
@dataclass
class TradeResult:
    event: SignalEvent
    exit_price: Optional[float] = None
    exit_time_ms: Optional[int] = None
    status: str = "OPEN"           # OPEN | WIN | LOSS
    exit_reason: Optional[str] = None   # TARGET | STOP_LOSS | RISK_FREE_STOP | NO_RESOLUTION
    resolution_method: str = "no_ambiguity"  # intrabar_verified | conservative_assumption | no_ambiguity
    risk_free_armed: bool = False
    risk_free_armed_ms: Optional[int] = None
    pnl_usd: Optional[float] = None
    pnl_r: Optional[float] = None
    mae_pct: Optional[float] = None   # Maximum Adverse Excursion (٪ از ریسکِ اولیه)
    mfe_pct: Optional[float] = None   # Maximum Favorable Excursion (٪ از ریسکِ اولیه)
    bars_held: int = 0


def _resolve_ambiguous_candle(symbol: str, candle_ts_ms: int, tf_minutes: int,
                               direction: str, stop: float, target: Optional[float]) -> tuple[Optional[str], str]:
    """
    وقتی در یک کندلِ تایم‌فریمِ اصلی هم استاپ هم تارگت لمس شده‌اند: دادهٔ
    ۱-دقیقه‌ایِ همان بازه را می‌گیرد و می‌بیند واقعاً کدام سطح زودتر لمس شده.
    برمی‌گرداند: ("STOP"|"TARGET"|None, resolution_method)
    """
    if tf_minutes <= 1:
        return None, "conservative_assumption"  # خودِ تایم‌فریم همین حالا ۱ دقیقه است

    start_ms = candle_ts_ms
    end_ms = candle_ts_ms + tf_minutes * 60 * 1000
    sub = get_1m_slice(symbol, start_ms, end_ms)
    if sub is None or sub.empty:
        return None, "conservative_assumption"  # دادهٔ ریزتر موجود نبود

    for _, row in sub.iterrows():
        hi, lo = float(row["high"]), float(row["low"])
        stop_hit = (lo <= stop) if direction == "LONG" else (hi >= stop)
        target_hit = (target is not None) and ((hi >= target) if direction == "LONG" else (lo <= target))
        if stop_hit and target_hit:
            # هر دو در همین کندلِ ۱ دقیقه‌ای هم لمس شدند (نادر) — استاپ محافظه‌کارانه
            return "STOP", "intrabar_verified"
        if stop_hit:
            return "STOP", "intrabar_verified"
        if target_hit:
            return "TARGET", "intrabar_verified"
    return None, "intrabar_verified"  # عجیب: نه استاپ نه تارگت در ریزکندل‌ها لمس نشد


def resolve_trade(ev: SignalEvent, df_full: pd.DataFrame, ts_to_idx: dict,
                   max_bars_forward: int = 100000) -> TradeResult:
    """
    دنبال‌کردنِ قیمت پس از سیگنال تا برخورد با استاپ/تارگت/ریسک‌فری — دقیقاً
    با همان فرمولِ trade_ledger (قانونِ محافظه‌کارانه به‌عنوان fallback، ولی
    وقتی داده‌ی ریزتر موجود است از آن برای حلِ قطعیِ ابهام استفاده می‌شود).
    """
    res = TradeResult(event=ev)
    i0 = ts_to_idx.get(ev.signal_bar_ts_ms)
    if i0 is None:
        res.exit_reason = "NO_RESOLUTION"
        return res

    tf_minutes = int(ev.timeframe)
    direction = ev.signal
    entry = ev.entry
    initial_stop = ev.stop
    stop = ev.stop
    target = ev.target
    risk_free_armed = False
    risk_free_pct = ev.risk_free_pct

    mae = 0.0  # بدترین حرکتِ برخلافِ جهت (به٪ ریسک)
    mfe = 0.0  # بهترین حرکتِ همجهت (به٪ ریسک)
    initial_risk = abs(entry - initial_stop)
    if initial_risk <= 0:
        res.exit_reason = "NO_RESOLUTION"
        return res

    n = len(df_full)
    end = min(n, i0 + 1 + max_bars_forward)
    bars_held = 0

    for i in range(i0 + 1, end):
        bars_held += 1
        row = df_full.iloc[i]
        hi, lo = float(row["high"]), float(row["low"])
        candle_ts_ms = int(df_full.index[i].timestamp() * 1000)

        # --- MAE/MFE (نسبت به ریسکِ اولیه، مثبت = به سودِ معامله) ---
        if direction == "LONG":
            adverse = (entry - lo) / initial_risk
            favorable = (hi - entry) / initial_risk
        else:
            adverse = (hi - entry) / initial_risk
            favorable = (entry - lo) / initial_risk
        mae = max(mae, adverse)
        mfe = max(mfe, favorable)

        # --- شبیه‌سازیِ ریسک‌فری، دقیقاً همان منطقِ trade_ledger.update_open_trades ---
        if not risk_free_armed and risk_free_pct is not None:
            if direction == "LONG":
                rf_trigger = entry * (1 + risk_free_pct)
                rf_crossed = hi >= rf_trigger
            else:
                rf_trigger = entry * (1 - abs(risk_free_pct))
                rf_crossed = lo <= rf_trigger
            if rf_crossed:
                initial_stop_for_pnl = initial_stop  # ریسکِ اولیه برای PnL دست‌نخورده می‌ماند
                stop = entry  # سربه‌سرِ بدونِ کارمزد — دقیقاً مطابق trade_ledger
                risk_free_armed = True
                res.risk_free_armed = True
                res.risk_free_armed_ms = candle_ts_ms

        hit_stop = (lo <= stop) if direction == "LONG" else (hi >= stop)
        hit_target = (target is not None) and ((hi >= target) if direction == "LONG" else (lo <= target))

        if hit_stop and hit_target:
            outcome, method = _resolve_ambiguous_candle(
                ev.symbol, candle_ts_ms, tf_minutes, direction, stop, target
            )
            res.resolution_method = method
            if outcome == "TARGET":
                hit_stop, hit_target = False, True
            else:
                hit_stop, hit_target = True, False  # پیش‌فرض/تاییدشده: استاپ

        if hit_stop:
            res.status = "WIN" if risk_free_armed else "LOSS"
            res.exit_reason = "RISK_FREE_STOP" if risk_free_armed else "STOP_LOSS"
            res.exit_price = stop
            res.exit_time_ms = candle_ts_ms
            break
        if hit_target:
            res.status = "WIN"
            res.exit_reason = "TARGET"
            res.exit_price = target
            res.exit_time_ms = candle_ts_ms
            break

    res.bars_held = bars_held
    res.mae_pct = round(mae * 100, 3)
    res.mfe_pct = round(mfe * 100, 3)

    if res.status != "OPEN":
        pnl_usd, pnl_r = ledger_pnl_usd(
            direction, entry, initial_stop, res.exit_price,
            LEVERAGE_MAP.get(ev.symbol)
        )
        res.pnl_usd = pnl_usd
        res.pnl_r = pnl_r
    else:
        res.exit_reason = res.exit_reason or "STILL_OPEN_AT_END_OF_DATA"

    return res


# ============================================================================
# ۱۰) متریک‌های سطح پرتفوی (سند، بخش ۵)
# ============================================================================
def _closed(trades: list[TradeResult]) -> list[TradeResult]:
    return [t for t in trades if t.status in ("WIN", "LOSS") and t.pnl_usd is not None]


def compute_equity_curve(trades: list[TradeResult]) -> pd.Series:
    closed = sorted(_closed(trades), key=lambda t: t.exit_time_ms or 0)
    if not closed:
        return pd.Series(dtype=float)
    times = [ms_to_dt(t.exit_time_ms) for t in closed]
    pnl = [t.pnl_usd for t in closed]
    equity = BASE_CAPITAL + pd.Series(pnl, index=pd.DatetimeIndex(times)).cumsum()
    return equity


def max_drawdown(equity: pd.Series) -> dict:
    if equity.empty:
        return {"max_dd_pct": 0.0, "max_dd_usd": 0.0, "peak_time": None, "valley_time": None}
    running_max = equity.cummax()
    dd_usd = equity - running_max
    dd_pct = dd_usd / running_max.replace(0, np.nan) * 100
    valley_idx = dd_usd.idxmin() if not dd_usd.empty else None
    peak_idx = running_max.loc[:valley_idx].idxmax() if valley_idx is not None else None
    return {
        "max_dd_pct": float(dd_pct.min()) if not dd_pct.empty else 0.0,
        "max_dd_usd": float(dd_usd.min()) if not dd_usd.empty else 0.0,
        "peak_time": peak_idx,
        "valley_time": valley_idx,
    }


def sharpe_sortino_calmar(trades: list[TradeResult], equity: pd.Series) -> dict:
    closed = _closed(trades)
    if len(closed) < 2:
        return {"sharpe": None, "sortino": None, "calmar": None}
    pnl = np.array([t.pnl_usd for t in closed], dtype=float)
    mean, std = pnl.mean(), pnl.std(ddof=1)
    sharpe = (mean / std) * math.sqrt(len(pnl)) if std > 0 else None

    downside = pnl[pnl < 0]
    dstd = downside.std(ddof=1) if len(downside) > 1 else None
    sortino = (mean / dstd) * math.sqrt(len(pnl)) if dstd else None

    dd = max_drawdown(equity)
    total_return_pct = ((equity.iloc[-1] - BASE_CAPITAL) / BASE_CAPITAL * 100) if not equity.empty else 0.0
    calmar = (total_return_pct / abs(dd["max_dd_pct"])) if dd["max_dd_pct"] not in (0, None) else None

    return {"sharpe": sharpe, "sortino": sortino, "calmar": calmar}


def sqn(trades: list[TradeResult]) -> Optional[float]:
    closed = _closed(trades)
    r_values = [t.pnl_r for t in closed if t.pnl_r is not None]
    if len(r_values) < 2:
        return None
    arr = np.array(r_values, dtype=float)
    if arr.std(ddof=1) == 0:
        return None
    return float((arr.mean() / arr.std(ddof=1)) * math.sqrt(len(arr)))


def expectancy(trades: list[TradeResult]) -> dict:
    closed = _closed(trades)
    if not closed:
        return {"expectancy_usd": None, "expectancy_r": None, "win_rate": None, "avg_win": None, "avg_loss": None}
    wins = [t for t in closed if t.status == "WIN"]
    losses = [t for t in closed if t.status == "LOSS"]
    win_rate = len(wins) / len(closed) * 100
    avg_win = statistics.mean([t.pnl_usd for t in wins]) if wins else 0.0
    avg_loss = statistics.mean([t.pnl_usd for t in losses]) if losses else 0.0
    exp_usd = (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)
    r_vals = [t.pnl_r for t in closed if t.pnl_r is not None]
    exp_r = statistics.mean(r_vals) if r_vals else None
    return {
        "expectancy_usd": exp_usd, "expectancy_r": exp_r, "win_rate": win_rate,
        "avg_win": avg_win, "avg_loss": avg_loss,
    }


def cagr(equity: pd.Series) -> Optional[float]:
    if equity.empty or len(equity) < 2:
        return None
    days = (equity.index[-1] - equity.index[0]).total_seconds() / 86400.0
    if days <= 0:
        return None
    total_return = equity.iloc[-1] / BASE_CAPITAL
    if total_return <= 0:
        return None  # سرمایه منفی شده — CAGR بی‌معنی؛ به‌جایش MaxDD/PF را نگاه کنید
    years = days / 365.25
    return (total_return ** (1 / years) - 1) * 100 if years > 0 else None


def exposure_time(trades: list[TradeResult], total_start_ms: int, total_end_ms: int) -> float:
    closed = _closed(trades)
    if not closed or total_end_ms <= total_start_ms:
        return 0.0
    covered = 0
    for t in sorted(closed, key=lambda t: t.event.signal_bar_ts_ms):
        covered += max(0, (t.exit_time_ms or t.event.signal_bar_ts_ms) - t.event.signal_bar_ts_ms)
    return min(100.0, covered / (total_end_ms - total_start_ms) * 100)


def benchmark_buy_hold(df_full: pd.DataFrame) -> Optional[float]:
    if df_full.empty or len(df_full) < 2:
        return None
    first, last = float(df_full["close"].iloc[0]), float(df_full["close"].iloc[-1])
    if first <= 0:
        return None
    return (last - first) / first * 100


def profit_factor(trades: list[TradeResult]) -> Optional[float]:
    closed = _closed(trades)
    gross_win = sum(t.pnl_usd for t in closed if t.pnl_usd and t.pnl_usd > 0)
    gross_loss = abs(sum(t.pnl_usd for t in closed if t.pnl_usd and t.pnl_usd < 0))
    if gross_loss == 0:
        return None if gross_win == 0 else float("inf")
    return gross_win / gross_loss


def validity_label(metrics: dict) -> tuple[str, list[str]]:
    """برچسبِ خودکار GOOD/SUSPICIOUS/UNRELIABLE (سند، بخش ۵)."""
    reasons = []
    sharpe = metrics.get("sharpe")
    pf = metrics.get("profit_factor")
    win_rate = metrics.get("win_rate")
    n_closed = metrics.get("n_closed", 0)

    label = "GOOD"
    if n_closed < 30:
        label = "UNRELIABLE"
        reasons.append(f"تعداد معاملات بسته‌شده خیلی کم است ({n_closed} < 30) — هر متریکی غیرقابل‌اتکاست.")
    if sharpe is not None and sharpe > 10:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Sharpe غیرعادی بالاست ({sharpe:.2f} > 10) — احتمال باگ یا نمونهٔ خیلی کوچک.")
    if pf is not None and pf != float("inf") and pf > 100:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Profit Factor غیرعادی بالاست ({pf:.1f} > 100) — احتمال لوک‌اِهد بایاس.")
    if pf == float("inf"):
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append("Profit Factor = ∞ (هیچ معاملهٔ بازنده‌ای ثبت نشده) — بسیار مشکوک.")
    if win_rate is not None and win_rate > 95:
        label = "SUSPICIOUS" if label == "GOOD" else label
        reasons.append(f"Win Rate غیرعادی بالاست ({win_rate:.1f}% > 95%) — احتمال survivorship bias.")
    if not reasons:
        reasons.append("هیچ الگوی مشکوکِ شناخته‌شده‌ای یافت نشد.")
    return label, reasons


def compute_portfolio_metrics(trades: list[TradeResult], df_full: pd.DataFrame,
                               total_start_ms: int, total_end_ms: int) -> dict:
    closed = _closed(trades)
    equity = compute_equity_curve(trades)
    dd = max_drawdown(equity)
    ssc = sharpe_sortino_calmar(trades, equity)
    exp = expectancy(trades)
    pf = profit_factor(trades)

    win_durations = [t.bars_held for t in closed if t.status == "WIN"]
    loss_durations = [t.bars_held for t in closed if t.status == "LOSS"]

    metrics = {
        "n_signals_total": len(trades),
        "n_closed": len(closed),
        "n_open_at_end": len([t for t in trades if t.status == "OPEN"]),
        "n_wins": len([t for t in closed if t.status == "WIN"]),
        "n_losses": len([t for t in closed if t.status == "LOSS"]),
        "n_target_wins": len([t for t in closed if t.exit_reason == "TARGET"]),
        "n_risk_free_wins": len([t for t in closed if t.exit_reason == "RISK_FREE_STOP"]),
        "win_rate": exp["win_rate"],
        "total_pnl_usd": sum(t.pnl_usd for t in closed if t.pnl_usd is not None),
        "expectancy_usd": exp["expectancy_usd"],
        "expectancy_r": exp["expectancy_r"],
        "avg_win_usd": exp["avg_win"],
        "avg_loss_usd": exp["avg_loss"],
        "profit_factor": pf,
        "sharpe": ssc["sharpe"],
        "sortino": ssc["sortino"],
        "calmar": ssc["calmar"],
        "sqn": sqn(trades),
        "cagr_pct": cagr(equity),
        "max_dd_pct": dd["max_dd_pct"],
        "max_dd_usd": dd["max_dd_usd"],
        "max_dd_peak_time": dd["peak_time"],
        "max_dd_valley_time": dd["valley_time"],
        "exposure_pct": exposure_time(trades, total_start_ms, total_end_ms),
        "benchmark_buy_hold_pct": benchmark_buy_hold(df_full),
        "avg_win_duration_bars": statistics.mean(win_durations) if win_durations else None,
        "avg_loss_duration_bars": statistics.mean(loss_durations) if loss_durations else None,
        "avg_mae_pct": statistics.mean([t.mae_pct for t in closed if t.mae_pct is not None]) if closed else None,
        "avg_mfe_pct": statistics.mean([t.mfe_pct for t in closed if t.mfe_pct is not None]) if closed else None,
        "intrabar_verified_count": len([t for t in trades if t.resolution_method == "intrabar_verified"]),
        "conservative_assumption_count": len([t for t in trades if t.resolution_method == "conservative_assumption"]),
        "no_ambiguity_count": len([t for t in trades if t.resolution_method == "no_ambiguity"]),
    }
    metrics["edge_ratio"] = (
        metrics["avg_mfe_pct"] / metrics["avg_mae_pct"]
        if metrics["avg_mae_pct"] not in (None, 0) and metrics["avg_mfe_pct"] is not None
        else None
    )
    label, reasons = validity_label(metrics)
    metrics["validity_label"] = label
    metrics["validity_reasons"] = reasons
    metrics["equity_curve"] = equity
    return metrics


# ============================================================================
# ۱۱) اعتبارسنجی در برابر Overfitting (سند، بخش ۶) — اجباری
# ============================================================================
MIN_SAMPLE_SIZE_DEFAULT = 30


def _signal_type_of(ev: SignalEvent, algo_log: str = "") -> str:
    """نوعِ سیگنال (CD-/CD+/HD+/HD-) از روی لاگِ ضبط‌شده استخراج می‌شود —
    این مقدار توسط strategy_wrapper در خطِ [SIGNAL_TRACE] چاپ می‌شود؛ اینجا
    فقط parse می‌کنیم، دوباره محاسبه نمی‌کنیم."""
    log = algo_log or ev.algo_log
    for line in log.splitlines():
        if "[SIGNAL_TRACE]" in line and "signal=" in line:
            try:
                part = line.split("signal=", 1)[1]
                return part.split("|", 1)[0].strip()
            except Exception:
                continue
    return "UNKNOWN"


def three_dim_breakdown(all_trades: list[TradeResult], min_samples: int = MIN_SAMPLE_SIZE_DEFAULT) -> list[dict]:
    """
    تحلیل سه‌بعدیِ خودکار: ارز × تایم‌فریم × نوعِ سیگنال (سند، بخش ۶ و ۹).
    معیارِ اصلیِ فیلتر = سود/Expectancy، نه صرفاً winrate (طبق درسِ گرفته‌شده
    از گزارشِ واقعیِ کاربر — بخش ۹ سند).
    """
    buckets: dict[tuple, list[TradeResult]] = {}
    for t in _closed(all_trades):
        stype = _signal_type_of(t.event)
        key = (t.event.symbol, t.event.timeframe, stype)
        buckets.setdefault(key, []).append(t)

    rows = []
    for (symbol, tf, stype), trs in buckets.items():
        n = len(trs)
        wins = [t for t in trs if t.status == "WIN"]
        win_rate = len(wins) / n * 100 if n else 0.0
        total_pnl = sum(t.pnl_usd for t in trs if t.pnl_usd is not None)
        exp_r_vals = [t.pnl_r for t in trs if t.pnl_r is not None]
        exp_r = statistics.mean(exp_r_vals) if exp_r_vals else None
        gross_win = sum(t.pnl_usd for t in trs if t.pnl_usd and t.pnl_usd > 0)
        gross_loss = abs(sum(t.pnl_usd for t in trs if t.pnl_usd and t.pnl_usd < 0))
        pf = (gross_win / gross_loss) if gross_loss > 0 else (float("inf") if gross_win > 0 else None)
        rows.append({
            "symbol": symbol, "timeframe": tf, "signal_type": stype,
            "n": n, "win_rate": win_rate, "total_pnl_usd": total_pnl,
            "expectancy_r": exp_r, "profit_factor": pf,
            "reliable_sample": n >= min_samples,
            "recommendation": (
                "نگه‌داشتن" if (n >= min_samples and total_pnl > 0) else
                "حذف/بررسیِ بیشتر" if (n >= min_samples and total_pnl <= 0) else
                "نمونهٔ کم — محافظه‌کارانه نگه‌داشته شود (بدون تصمیمِ قطعی)"
            ),
        })
    rows.sort(key=lambda r: (r["total_pnl_usd"] if r["total_pnl_usd"] is not None else 0))
    return rows


def half_split_validation(all_trades: list[TradeResult], breakdown: list[dict]) -> list[dict]:
    """اعتبارسنجیِ نیم‌اول/نیم‌دومِ هر سلولِ فیلترشده — آیا جهتِ سودآوری در
    هر دو نیمهٔ بازه یکسان است یا فقط در یک نیمه بوده (نشانهٔ overfitting)."""
    by_key: dict[tuple, list[TradeResult]] = {}
    for t in _closed(all_trades):
        stype = _signal_type_of(t.event)
        key = (t.event.symbol, t.event.timeframe, stype)
        by_key.setdefault(key, []).append(t)

    out = []
    for row in breakdown:
        key = (row["symbol"], row["timeframe"], row["signal_type"])
        trs = sorted(by_key.get(key, []), key=lambda t: t.event.signal_bar_ts_ms)
        if len(trs) < min(10, MIN_SAMPLE_SIZE_DEFAULT):
            out.append({**row, "half1_pnl": None, "half2_pnl": None, "consistent": None})
            continue
        mid = len(trs) // 2
        h1, h2 = trs[:mid], trs[mid:]
        pnl1 = sum(t.pnl_usd for t in h1 if t.pnl_usd is not None)
        pnl2 = sum(t.pnl_usd for t in h2 if t.pnl_usd is not None)
        consistent = (pnl1 > 0) == (pnl2 > 0)
        out.append({**row, "half1_pnl": pnl1, "half2_pnl": pnl2, "consistent": consistent})
    return out


def monte_carlo_permutation_test(trades: list[TradeResult], n_permutations: int = 1000, seed: int = 42) -> dict:
    """
    تستِ مونت‌کارلوی permutation (اختیاری، --robust؛ سند بخش ۶): ترتیبِ
    برد/باختِ معاملات را می‌شفلد و می‌بیند PnLِ واقعی چند درصدِ توزیعِ تصادفی
    را رد می‌کند (p-value تقریبی). این *ترتیب* را می‌شفلد نه بازارِ زیرین —
    نسخه‌ای سبک‌تر از نسخهٔ کاملِ مبتنی‌بر بازآفرینیِ مسیرِ قیمت.
    """
    closed = _closed(trades)
    pnls = np.array([t.pnl_usd for t in closed], dtype=float)
    if len(pnls) < 10:
        return {"p_value": None, "note": "نمونهٔ خیلی کم برای Monte Carlo."}
    rng = np.random.default_rng(seed)
    real_total = pnls.sum()
    count_ge = 0
    for _ in range(n_permutations):
        shuffled = rng.permutation(pnls)
        # جهتِ تصادفی به هر معامله می‌دهیم (سناریوی null: مهارتی در انتخابِ جهت نبوده)
        signs = rng.choice([-1, 1], size=len(shuffled))
        sim_total = (np.abs(shuffled) * signs).sum()
        if sim_total >= real_total:
            count_ge += 1
    p_value = count_ge / n_permutations
    return {"p_value": p_value, "n_permutations": n_permutations, "real_total_pnl": real_total}


def walk_forward_validation(df_full: pd.DataFrame, symbol: str, timeframe: str,
                             history_bars: int, workers: int, n_folds: int = 3) -> dict:
    """Walk-forward سادهٔ اختیاری (--robust): بازه به n_folds قسمت تقسیم می‌شود؛
    هر فولد به‌طورِ مستقل سیگنال‌دهی/PnL می‌شود تا ثباتِ نتیجه در طولِ زمان
    دیده شود (نه صرفاً یک بازهٔ کلی)."""
    n = len(df_full)
    if n < 200:
        return {"folds": [], "note": "داده برای walk-forward کافی نیست."}
    fold_size = n // n_folds
    folds_out = []
    ts_to_idx_full = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_full.index)}
    for f in range(n_folds):
        lo = f * fold_size
        hi = n if f == n_folds - 1 else (f + 1) * fold_size
        df_fold = df_full.iloc[lo:hi]
        if len(df_fold) < 60:
            continue
        events = generate_signals_exact(df_fold, symbol, timeframe, history_bars, workers=workers, keep_log=False)
        ts_to_idx_fold = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_fold.index)}
        trades = [resolve_trade(ev, df_fold, ts_to_idx_fold) for ev in events]
        closed = _closed(trades)
        total_pnl = sum(t.pnl_usd for t in closed if t.pnl_usd is not None)
        folds_out.append({
            "fold": f + 1,
            "start": str(df_fold.index[0]), "end": str(df_fold.index[-1]),
            "n_signals": len(events), "n_closed": len(closed), "total_pnl_usd": total_pnl,
        })
    profitable_folds = sum(1 for r in folds_out if r["total_pnl_usd"] > 0)
    return {"folds": folds_out, "profitable_folds": profitable_folds, "total_folds": len(folds_out)}


# ============================================================================
# ۱۲) گزارشِ «سیگنال‌های اخیر» متناسب با تایم‌فریم + لاگِ کاملِ الگوریتمی
#     (سند، بخش ۷ و ۱۰-۷)
# ============================================================================
def build_recent_signals_section(events: list[SignalEvent], trades: dict[int, TradeResult],
                                  timeframe: str, now_ms: int) -> str:
    days, confirmed = recent_window_days(timeframe)
    cutoff_ms = now_ms - days * 86400 * 1000
    recent = [e for e in events if e.signal_bar_ts_ms >= cutoff_ms]
    recent.sort(key=lambda e: e.signal_bar_ts_ms, reverse=True)

    lines = []
    conf_note = "✅ تاییدشده توسط کاربر" if confirmed else "⚠️ برون‌یابی‌شده — نیازمند تایید نهایی (سند، بخش ۷/۱۱)"
    lines.append(f"### سیگنال‌های اخیر — تایم‌فریم {timeframe} دقیقه (بازهٔ {days} روز منتهی به پایانِ بازهٔ بک‌تست, {conf_note})")
    lines.append(f"تعداد سیگنال در این بازه: {len(recent)}")
    lines.append("")

    for ev in recent:
        key = ev.signal_bar_ts_ms
        tr = trades.get(key)
        ts_str = ms_to_dt(ev.signal_bar_ts_ms).astimezone(IRAN_TZ).strftime("%Y-%m-%d %H:%M:%S")
        lines.append(f"--- {ev.symbol} | {ev.signal} | {ts_str} (تهران) ---")
        lines.append(f"  ورود={ev.entry} | استاپ={ev.stop} | تارگت={ev.target} | ریسک‌فری٪={ev.risk_free_pct}")
        if tr:
            lines.append(
                f"  نتیجه: {tr.status} ({tr.exit_reason}) | خروج={tr.exit_price} | "
                f"PnL=${tr.pnl_usd} ({tr.pnl_r}R) | روشِ حلِ ابهام={tr.resolution_method} | "
                f"MAE={tr.mae_pct}% MFE={tr.mfe_pct}%"
            )
        else:
            lines.append("  نتیجه: (هنوز محاسبه نشده)")
        lines.append("  لاگِ کاملِ الگوریتمی:")
        for logline in (ev.algo_log or "").splitlines():
            lines.append(f"    {logline}")
        lines.append("")
    return "\n".join(lines)


# ============================================================================
# ۱۳) رندرِ نهاییِ گزارش (چک‌لیستِ محتوایی — سند، بخش ۱۰)
# ============================================================================
def _fmt(x, nd=2, suffix=""):
    if x is None:
        return "N/A"
    if x == float("inf"):
        return "∞"
    try:
        return f"{x:.{nd}f}{suffix}"
    except Exception:
        return str(x)


def render_report(args, run_meta: dict, per_symbol_tf: dict, portfolio_metrics: dict,
                   breakdown: list[dict], half_split: list[dict],
                   recent_sections: list[str], robust_extra: dict) -> str:
    out = []
    out.append("=" * 78)
    out.append("گزارشِ بک‌تستِ استراتژیِ DTM — موتورِ exact/event-driven")
    out.append("=" * 78)
    out.append(f"بازه: {args.date_from} → {args.date_to}")
    out.append(f"نمادها: {', '.join(run_meta['symbols'])}")
    out.append(f"تایم‌فریم‌ها: {', '.join(run_meta['timeframes'])}")
    out.append(f"منبعِ ثابت‌ها (SYMBOLS/TIMEFRAMES/LEVERAGE_MAP/TICK_SIZES/HISTORY_BARS): {CONST_SOURCE}")
    out.append(f"موتورِ سیگنال: {'⚠️ FAST (تقریبی)' if args.engine == 'fast' else 'EXACT/event-driven (تنها موتورِ معتبر)'}")
    if UNMAPPED_TIMEFRAME_GUESSES:
        out.append(f"⚠️ تایم‌فریم‌های بدون نگاشتِ صریح در BINANCE_INTERVAL_MAP (حدس زده شد): {sorted(UNMAPPED_TIMEFRAME_GUESSES)}")
    label = portfolio_metrics.get("validity_label", "N/A")
    out.append(f"برچسبِ اعتبارِ کلی: {label}")
    for r in portfolio_metrics.get("validity_reasons", []):
        out.append(f"  - {r}")
    out.append("")

    out.append("── ۱) آمارِ کلیِ سبد ──────────────────────────────────────")
    m = portfolio_metrics
    out.append(f"تعداد کل سیگنال: {m['n_signals_total']}  |  بسته‌شده: {m['n_closed']}  |  هنوز باز: {m['n_open_at_end']}")
    out.append(f"برد: {m['n_wins']} (تارگت={m['n_target_wins']}, ریسک‌فری={m['n_risk_free_wins']})  |  باخت: {m['n_losses']}  |  Win Rate: {_fmt(m['win_rate'], 2, '%')}")
    out.append(f"مجموع PnL: ${_fmt(m['total_pnl_usd'], 4)}  (بر اساس سرمایهٔ پایهٔ ${BASE_CAPITAL:.0f}, مستقل از موجودی واقعیِ صرافی)")
    out.append(f"Expectancy: ${_fmt(m['expectancy_usd'], 4)}  |  Expectancy (R): {_fmt(m['expectancy_r'], 3)}R  |  Profit Factor: {_fmt(m['profit_factor'], 3)}")
    out.append(f"میانگین برد: ${_fmt(m['avg_win_usd'], 4)}  |  میانگین باخت: ${_fmt(m['avg_loss_usd'], 4)}")
    out.append(f"Sharpe: {_fmt(m['sharpe'], 3)}  |  Sortino: {_fmt(m['sortino'], 3)}  |  Calmar: {_fmt(m['calmar'], 3)}  |  SQN: {_fmt(m['sqn'], 3)}")
    out.append(f"CAGR: {_fmt(m['cagr_pct'], 2, '%')}  |  Max Drawdown: {_fmt(m['max_dd_pct'], 2, '%')} (${_fmt(m['max_dd_usd'], 4)})")
    out.append(f"  اوجِ افت: {m['max_dd_peak_time']}  →  کفِ افت: {m['max_dd_valley_time']}")
    out.append(f"Exposure Time: {_fmt(m['exposure_pct'], 2, '%')}  |  Benchmark Buy&Hold (اولین نماد): {_fmt(m['benchmark_buy_hold_pct'], 2, '%')}")
    out.append(f"میانگین طولِ معاملهٔ برنده: {_fmt(m['avg_win_duration_bars'], 1)} کندل  |  بازنده: {_fmt(m['avg_loss_duration_bars'], 1)} کندل")
    out.append(f"میانگین MAE: {_fmt(m['avg_mae_pct'], 2, '%')}  |  میانگین MFE: {_fmt(m['avg_mfe_pct'], 2, '%')}  |  Edge Ratio (MFE/MAE): {_fmt(m['edge_ratio'], 3)}")
    out.append(
        f"روشِ حلِ ابهامِ استاپ/تارگتِ هم‌کندل: intrabar_verified={m['intrabar_verified_count']} | "
        f"conservative_assumption={m['conservative_assumption_count']} | no_ambiguity={m['no_ambiguity_count']}"
    )
    out.append("")

    out.append("── ۲) تفکیک بر اساس نماد/تایم‌فریم ─────────────────────────")
    for (symbol, tf), sub_m in per_symbol_tf.items():
        out.append(
            f"{symbol} {tf}m: سیگنال={sub_m['n_signals_total']} | بسته={sub_m['n_closed']} | "
            f"WinRate={_fmt(sub_m['win_rate'],1,'%')} | PnL=${_fmt(sub_m['total_pnl_usd'],4)} | "
            f"PF={_fmt(sub_m['profit_factor'],2)} | Expectancy(R)={_fmt(sub_m['expectancy_r'],3)}"
        )
    out.append("")

    out.append("── ۳) تحلیل سه‌بعدیِ خودکار (ارز × تایم‌فریم × نوعِ سیگنال) ──")
    out.append("معیارِ فیلتر = سود/Expectancy، نه صرفاً Win Rate (سند، بخش ۹/۱۱).")
    out.append(f"{'symbol':<10}{'tf':<6}{'type':<8}{'n':<6}{'winRate':<10}{'PnL($)':<12}{'Exp(R)':<10}{'PF':<8}{'reliable':<10}{'recommendation'}")
    for row in breakdown:
        out.append(
            f"{row['symbol']:<10}{row['timeframe']:<6}{row['signal_type']:<8}{row['n']:<6}"
            f"{_fmt(row['win_rate'],1):<10}{_fmt(row['total_pnl_usd'],2):<12}"
            f"{_fmt(row['expectancy_r'],3):<10}{_fmt(row['profit_factor'],2):<8}"
            f"{'بله' if row['reliable_sample'] else 'خیر':<10}{row['recommendation']}"
        )
    out.append("")

    out.append("── ۴) اعتبارسنجیِ نیم‌اول/نیم‌دوم (هر سلولِ فیلترشده) ──────")
    for row in half_split:
        cons = "سازگار ✅" if row["consistent"] else ("ناسازگار ⚠️ (نشانهٔ overfitting)" if row["consistent"] is False else "نمونه کم")
        out.append(
            f"{row['symbol']} {row['timeframe']}m {row['signal_type']}: "
            f"نیمهٔ اول=${_fmt(row['half1_pnl'],2)} | نیمهٔ دوم=${_fmt(row['half2_pnl'],2)} | {cons}"
        )
    out.append("")

    if robust_extra:
        out.append("── ۵) اعتبارسنجیِ سنگین (--robust) ─────────────────────")
        if "monte_carlo" in robust_extra:
            mc = robust_extra["monte_carlo"]
            out.append(f"Monte Carlo Permutation Test: p-value ≈ {_fmt(mc.get('p_value'), 4)} (کمتر = نتیجه بعیدتر بود که تصادفی باشد)")
        if "walk_forward" in robust_extra:
            for (symbol, tf), wf in robust_extra["walk_forward"].items():
                out.append(f"Walk-Forward {symbol} {tf}m: {wf['profitable_folds']}/{wf['total_folds']} فولد سودآور بودند.")
                for f in wf["folds"]:
                    out.append(f"   فولد {f['fold']}: {f['start']}→{f['end']} | سیگنال={f['n_signals']} | PnL=${_fmt(f['total_pnl_usd'],2)}")
        out.append("")

    if run_meta.get("determinism"):
        out.append("── ۶) چکِ Determinism ───────────────────────────────────")
        for (symbol, tf), d in run_meta["determinism"].items():
            status = "✅ سازگار" if d["ok"] else f"❌ {d['mismatches']} ناسازگاری یافت شد!"
            out.append(f"{symbol} {tf}m: {d['checked']} نمونه بررسی شد — {status}")
        out.append("")

    if run_meta.get("lookahead"):
        out.append("── ۷) چکِ خودتشخیصیِ لوک‌اِهد ─────────────────────────────")
        for (symbol, tf), la in run_meta["lookahead"].items():
            out.append(f"{symbol} {tf}m: {la['checked']} سیگنال بررسی شد — {la['suspicious']} مورد مشکوک.")
        out.append("")

    out.append("── ۸) شکاف‌های داده (network/no-data) ────────────────────")
    any_gap = False
    for (symbol, tf), gaps in run_meta.get("gaps", {}).items():
        if gaps:
            any_gap = True
            out.append(f"{symbol} {tf}m: {len(gaps)} شکاف —")
            for g in gaps[:10]:
                out.append(f"    {ms_to_dt(g[0])} → {ms_to_dt(g[1])} ({g[2]})")
    if not any_gap:
        out.append("هیچ شکافِ داده‌ای گزارش نشد.")
    out.append("")

    out.append("── ۹) سیگنال‌های اخیر (متناسب با تایم‌فریم) + لاگِ کاملِ الگوریتمی ──")
    for sec in recent_sections:
        out.append(sec)
        out.append("")

    out.append("── ۱۰) روش‌شناسی و محدودیت‌ها ────────────────────────────")
    out.append(
        "- سیگنال، استاپ/تارگت، و PnL مستقیماً از strategy_wrapper.calculate_signals و "
        "trade_ledger._hypothetical_pnl_usd (import شده، نه بازنویسی) محاسبه شده‌اند."
    )
    out.append(
        f"- هر کندلِ بسته‌شده با یک اجرایِ کاملاً تازهٔ ScriptRunner روی آخرین "
        f"{HISTORY_BARS} کندل پردازش شده — دقیقاً همان چیزی که bot.py هر چرخه انجام می‌دهد."
    )
    out.append(
        "- ابهامِ «استاپ و تارگت در یک کندل»: در صورت وجودِ دادهٔ ۱-دقیقه‌ایِ واقعی حل شده "
        "(intrabar_verified)؛ در غیر این صورت با قاعدهٔ محافظه‌کارانهٔ «استاپ برنده» "
        "(conservative_assumption) — تعدادِ هرکدام در بخش (۱) آمده."
    )
    out.append(
        "- ریسک‌فری با همان منطقِ trade_ledger.update_open_trades شبیه‌سازی شده (سربه‌سرِ بدونِ کارمزد، "
        "چون کارمزدِ واقعیِ صرافی فقط از یک پوزیشنِ زندهٔ صرافی قابل خواندن است، نه از دادهٔ تاریخی)."
    )
    out.append(
        f"- جدولِ بازهٔ «سیگنال‌های اخیر» برای تایم‌فریم‌های ≥۱۵ دقیقه برون‌یابی‌شده و باید تایید شود "
        "(سند، بخش ۷/۱۱)؛ فقط ۱m→۷روز و ۵m→۲۲روز مستقیماً از کاربر گرفته شده‌اند."
    )
    out.append(
        "- اعلان‌های تلگرام (شروعِ اجرا، تخمینِ زمانِ پایان، خلاصهٔ قابلیت‌های همین اجرا، پایانِ هر "
        "ترکیبِ نماد/تایم‌فریم، پایانِ هر نماد، و گزارشِ نهایی) به یک رباتِ تلگرامِ کاملاً جدا و مستقل "
        "از رباتِ لایو ارسال می‌شوند (BACKTEST_TELEGRAM_BOT_TOKEN/BACKTEST_TELEGRAM_CHAT_ID) — این "
        "کاملاً مستقل از پیام‌های لحظه‌ایِ خودِ calculate_signals است (که در بک‌تست عمداً خاموش شده‌اند "
        "تا اسپم نشود)."
    )
    out.append(
        f"- کلِ این بک‌تست فقط یک‌بار در هر اجرا/استارتِ فرآیند اجرا می‌شود (قفلِ فایلی: "
        f"{RUN_LOCK_FILE.name}). ⚠️ این قفل فقط در طولِ عمرِ همان فرآیند/کانتینر معتبر است؛ با "
        "ری‌استارتِ واقعیِ سرویس (کانتینرِ جدید، مثلاً روی Railway) از بین می‌رود و بک‌تست دوباره از "
        "اول اجرا خواهد شد، مگر این‌که مسیرِ قفل روی یک volume دائمی mount شده باشد."
    )
    if not args.robust:
        out.append("- Monte Carlo Permutation Test و Walk-Forward اجرا نشدند (پیش‌فرض خاموش؛ با --robust فعال می‌شوند).")
    if args.engine == "fast":
        out.append("⚠️ این اجرا با --engine fast بوده — نتیجه صرفاً تقریبی است و نباید برای تصمیم‌گیریِ نهایی استفاده شود.")
    if not LOGIC_SOURCE_OK:
        out.append(f"⚠️ import از strategy_wrapper.py/trade_ledger.py شکست خورد: {_logic_import_error}")

    out.append("=" * 78)
    return "\n".join(out)


# ============================================================================
# ۱۳-الف) پیامِ خلاصهٔ قابلیت‌ها/کارهایی که در همین اجرا انجام می‌شود
#    (داینامیک — بر اساسِ آرگومان‌های واقعیِ همین اجرا، نه یک متنِ ثابت)
# ============================================================================
def build_capabilities_message(args, symbols: list[str], timeframes: list[str]) -> str:
    lines = ["🧩 کارهایی که در این اجرا انجام می‌شود:"]
    lines.append(f"• موتورِ سیگنال: {'⚠️ fast (تقریبی)' if args.engine == 'fast' else 'exact/event-driven (بازسازیِ دقیقِ لایو)'}")
    lines.append(f"• نمادها: {', '.join(symbols)}")
    lines.append(f"• تایم‌فریم‌ها: {', '.join(timeframes)} دقیقه")
    lines.append(f"• بازهٔ زمانی: {args.date_from} → {args.date_to}")
    lines.append(f"• تعدادِ پردازه‌های موازی: {args.workers}")
    lines.append("• حلِ ابهامِ استاپ/تارگتِ هم‌کندل با دادهٔ ۱ دقیقه‌ای: همیشه فعال")
    lines.append("• شبیه‌سازیِ ریسک‌فری با فرمولِ trade_ledger: همیشه فعال")
    lines.append(f"• چکِ Determinism: {'فعال' if args.determinism_check else 'غیرفعال'}")
    lines.append(f"• چکِ خودتشخیصیِ لوک‌اِهد: {'فعال' if args.lookahead_check else 'غیرفعال'}")
    lines.append(f"• اعتبارسنجیِ سنگین (Monte Carlo + Walk-Forward، --robust): {'فعال' if args.robust else 'غیرفعال'}")
    lines.append(f"• حداقلِ نمونهٔ آماریِ اجباری برای هر سلولِ فیلترشده: {args.min_samples}")
    lines.append(f"• ضبطِ لاگِ کاملِ الگوریتمیِ هر سیگنال: {'فعال' if args.keep_log else 'غیرفعال'}")
    lines.append("• پس از پایان: آمارِ کلیِ سبد + تفکیکِ نماد/تایم‌فریم + تحلیلِ سه‌بعدی + اعتبارسنجیِ نیم‌اول/نیم‌دوم")
    lines.append("• در پایان: گزارشِ ۷ روزِ اخیرِ تایم‌فریمِ ۱ دقیقه (txt + xlsx) به همین چت ارسال می‌شود.")
    return "\n".join(lines)


# ============================================================================
# ۱۴) CLI / orchestration
# ============================================================================
def parse_args():
    p = argparse.ArgumentParser(description="بک‌تستِ exact/event-driven استراتژیِ DTM.")
    p.add_argument("--from", dest="date_from", default=DEFAULT_DATE_FROM, help="تاریخ شروع، مثل 2024-01-01")
    p.add_argument("--to", dest="date_to", default=DEFAULT_DATE_TO, help="تاریخ پایان، مثل 2025-01-01")
    p.add_argument("--symbols", default=",".join(SYMBOLS), help="لیست نمادها با کاما جدا شده")
    p.add_argument("--timeframes", default=",".join(TIMEFRAMES), help="لیست تایم‌فریم‌ها با کاما جدا شده")
    p.add_argument("--engine", choices=["exact", "fast"], default="exact",
                    help="⚠️ 'fast' فقط برای مقایسهٔ سریع؛ هرگز پیش‌فرض/معتبر نیست.")
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1),
                    help="تعداد پردازه برای موازی‌سازیِ موتورِ exact")
    p.add_argument("--min-samples", type=int, default=MIN_SAMPLE_SIZE_DEFAULT,
                    help="حداقل نمونهٔ آماریِ اجباری برای هر سلولِ فیلترشونده")
    p.add_argument("--robust", action="store_true",
                    help="فعال‌سازیِ Monte Carlo Permutation Test و Walk-Forward (سنگین)")
    p.add_argument("--determinism-check", action="store_true", default=True,
                    help="چکِ determinism روی یک نمونهٔ کوچک (پیش‌فرض روشن)")
    p.add_argument("--no-determinism-check", dest="determinism_check", action="store_false")
    p.add_argument("--lookahead-check", action="store_true",
                    help="اجرایِ ابزارِ خودتشخیصیِ لوک‌اِهد (سنگین)")
    p.add_argument("--no-log", dest="keep_log", action="store_false", default=True,
                    help="خاموش‌کردنِ ضبطِ لاگِ کاملِ الگوریتمی برای هر سیگنال (خروجی سبک‌تر)")
    p.add_argument("--output", default=None, help="مسیر فایلِ گزارشِ متنیِ خروجی")
    p.add_argument("--json-output", default=None, help="مسیرِ دلخواه برای dumpِ کاملِ JSON هر معامله")
    return p.parse_args()


def _fast_engine_placeholder(*a, **kw):
    """حالتِ fast صرفاً برای مقایسهٔ سریع — نگاشتِ صریح به همان موتورِ exact
    ولی با یک ScriptRunner پیوسته روی کلِ تاریخچه (سریع‌تر، ولی دقیقاً همان
    باگِ رده‌شدهٔ #۱ در سند: با رفتارِ لایو یکی نیست). عمداً هرگز پیش‌فرض
    نیست و همیشه با برچسبِ ⚠️ در گزارش علامت می‌خورد."""
    raise NotImplementedError(
        "حالت --engine fast در این نسخه پیاده‌سازی نشده (عمداً، چون سند صراحتاً می‌گوید "
        "هرگز نباید پیش‌فرض یا جایگزینِ موتورِ exact باشد). برای مقایسهٔ سریع، بازهٔ زمانیِ "
        "کوچک‌تری با --engine exact اجرا کنید."
    )


def estimate_total_runtime(symbols: list[str], timeframes: list[str],
                            start_dt: datetime, end_dt: datetime, workers: int) -> tuple[float, int]:
    """
    تخمینِ زمانِ کلِ اجرا: به‌جای یک عددِ ثابتِ حدسی، ابتدا تعدادِ کندلِ
    موردِ انتظار در کلِ بازه/نمادها/تایم‌فریم‌ها را از روی خودِ بازهٔ زمانی
    محاسبه می‌کند (بدون نیاز به دانلود)، سپس یک کالیبراسیونِ واقعیِ کوچک
    (پردازشِ چند ده کندلِ اولِ اولین ترکیبِ نماد/تایم‌فریم، تک‌پردازه‌ای) انجام
    می‌دهد تا سرعتِ واقعیِ همین سیستم را اندازه بگیرد و آن را تعمیم دهد.

    ⚠️ این فقط یک تخمین است، نه تضمین — صرفاً برای اطلاع‌رسانیِ اولیه در
    پیامِ تلگرام و لاگ، نه برای برنامه‌ریزیِ دقیق.
    برمی‌گرداند: (ثانیهٔ تخمینی, تعدادِ کندلِ تخمینی)
    """
    total_bars_est = 0
    minutes_span = (end_dt - start_dt).total_seconds() / 60.0
    for tf in timeframes:
        try:
            tf_min = int(tf)
        except Exception:
            tf_min = 1
        total_bars_est += int(minutes_span / max(tf_min, 1)) * len(symbols)

    if not symbols or not timeframes or total_bars_est <= 0:
        return 0.0, 0

    calib_symbol, calib_tf = symbols[0], timeframes[0]
    calib_bars_target = 40
    sec_per_bar_single_core = 0.05  # حدسِ محافظه‌کارانهٔ fallback اگر کالیبراسیون شکست بخورد

    try:
        calib_tf_min = int(calib_tf)
        calib_fetch_start = start_dt - timedelta(minutes=calib_tf_min * (HISTORY_BARS + calib_bars_target) * 1.2 + 60)
        calib_fetch_end = start_dt + timedelta(minutes=calib_tf_min * calib_bars_target)
        df_calib = fetch_full_history(calib_symbol, calib_tf, calib_fetch_start, calib_fetch_end)
        if df_calib.empty or len(df_calib) < 60:
            raise ValueError("دادهٔ کالیبراسیون ناکافی بود.")
        n_calib = min(calib_bars_target, len(df_calib) - 50)
        n_calib = max(n_calib, 5)
        t0 = _time_mod.time()
        # کالیبراسیون عمداً تک‌پردازه‌ای (workers=1) تا سرعتِ خالصِ محاسبه‌ی
        # هر کندل روی یک هسته اندازه‌گیری شود؛ سپس با فرضِ speedupِ نزدیک‌به‌
        # خطیِ workerها (با ضریبِ کاراییِ محافظه‌کارانهٔ ۰.۸) تعمیم داده می‌شود.
        _ = generate_signals_exact(df_calib.iloc[-(n_calib + 50):], calib_symbol, calib_tf,
                                    HISTORY_BARS, workers=1, keep_log=False)
        elapsed = _time_mod.time() - t0
        sec_per_bar_single_core = elapsed / max(n_calib, 1)
    except Exception as e:
        logger.warning(f"کالیبراسیونِ تخمینِ زمان شکست خورد ({e})؛ از یک تخمینِ خیلی تقریبی استفاده می‌شود.")

    effective_workers = max(1, workers)
    est_seconds = (total_bars_est * sec_per_bar_single_core) / (effective_workers * 0.8)
    # به‌علاوهٔ سربارِ تقریبیِ دانلودِ دادهٔ تاریخی برای هر ترکیبِ نماد/تایم‌فریم
    est_seconds += len(symbols) * len(timeframes) * 15.0
    return max(0.0, est_seconds), total_bars_est


def main():
    args = parse_args()

    # ------------------------------------------------------------------
    # قفلِ تک‌اجرایی (بخش ۱-ب): کلِ بک‌تست باید فقط یک‌بار در طولِ عمرِ همین
    # فرآیند/کانتینر اجرا شود. اگر قفل از قبل وجود دارد، فقط یک پیامِ کوتاه
    # می‌دهیم و خارج می‌شویم — بدون هیچ محاسبهٔ سنگینی.
    # ------------------------------------------------------------------
    if RUN_LOCK_FILE.exists():
        try:
            prev_ts = RUN_LOCK_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            prev_ts = "نامشخص"
        skip_msg = (
            "⏭️ بک‌تست اجرا نشد: طبقِ قفلِ اجرا، این فرآیند/کانتینر قبلاً یک‌بار بک‌تست را "
            f"شروع کرده (زمانِ شروعِ اجرایِ قبلی: {prev_ts}).\n"
            f"برای اجرای دوباره در همین کانتینر، فایلِ قفل ({RUN_LOCK_FILE}) را دستی حذف کنید."
        )
        logger.warning(skip_msg)
        notify_telegram(skip_msg)
        print(skip_msg)
        return
    RUN_LOCK_FILE.write_text(datetime.now(UTC).isoformat(), encoding="utf-8")

    start_dt = datetime.strptime(args.date_from, "%Y-%m-%d").replace(tzinfo=UTC)
    end_dt = datetime.strptime(args.date_to, "%Y-%m-%d").replace(tzinfo=UTC)
    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    timeframes = [t.strip() for t in args.timeframes.split(",") if t.strip()]

    run_meta = {
        "symbols": symbols, "timeframes": timeframes,
        "gaps": {}, "determinism": {}, "lookahead": {},
    }

    all_trades: list[TradeResult] = []
    per_symbol_tf: dict = {}
    recent_sections: list[str] = []
    recent_1m_sections: list[str] = []
    recent_1m_trades: list = []
    robust_extra: dict = {}
    global_start_ms = utc_ms(start_dt)
    global_end_ms = utc_ms(end_dt)
    # لنگرِ «سیگنال‌های اخیر» = انتهایِ بازهٔ بک‌تست، نه لحظهٔ واقعیِ اجرا؛
    # وگرنه برای بازه‌های تاریخیِ گذشته همیشه صفر سیگنال «اخیر» پیدا می‌شد.
    recent_anchor_ms = global_end_ms
    first_df_for_benchmark: Optional[pd.DataFrame] = None

    if args.engine == "fast":
        logger.warning("⚠️ در حالِ اجرا با --engine fast — نتیجه تقریبی است.")

    # ------------------------------------------------------------------
    # اعلاناتِ شروعِ اجرا — سه پیامِ جداگانه به رباتِ جدید (بخش ۱-الف)
    # ------------------------------------------------------------------
    run_start_mono = _time_mod.time()
    try:
        est_seconds, est_bars = estimate_total_runtime(symbols, timeframes, start_dt, end_dt, args.workers)
    except Exception as e:
        logger.warning(f"تخمینِ زمانِ اجرا شکست خورد: {e}")
        est_seconds, est_bars = 0.0, 0

    # پیامِ ۱: شروعِ بک‌تست
    start_msg = (
        "🚀 بک‌تستِ DTM شروع شد.\n"
        f"بازه: {args.date_from} → {args.date_to}\n"
        f"نمادها: {', '.join(symbols)}\n"
        f"تایم‌فریم‌ها: {', '.join(timeframes)}\n"
        f"موتور: {'⚠️ fast (تقریبی)' if args.engine == 'fast' else 'exact/event-driven'}"
    )
    logger.warning(start_msg)
    notify_telegram(start_msg)

    # پیامِ ۲: زمانِ تخمینیِ آماده‌شدنِ گزارش
    if est_seconds > 0:
        eta_dt = datetime.now(UTC) + timedelta(seconds=est_seconds)
        eta_msg = (
            f"⏱️ تخمینِ زمانِ پایان: {eta_dt.astimezone(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')} (تهران)\n"
            f"تخمینِ تعدادِ کندلِ قابلِ پردازش: ~{est_bars:,}\n"
            "⚠️ این فقط یک تخمینِ تقریبی بر اساسِ سرعتِ اندازه‌گیری‌شده روی یک نمونهٔ کوچک است."
        )
    else:
        eta_msg = "⏱️ زمانِ تخمینیِ پایان: قابلِ محاسبه نبود (به لاگ نگاه کنید)."
    logger.warning(eta_msg)
    notify_telegram(eta_msg)

    # پیامِ ۳: خلاصهٔ داینامیکِ قابلیت‌ها/کارهای همین اجرا
    capabilities_msg = build_capabilities_message(args, symbols, timeframes)
    logger.warning(capabilities_msg)
    notify_telegram(capabilities_msg)

    for symbol in symbols:
        symbol_start_mono = _time_mod.time()
        symbol_trades: list[TradeResult] = []
        symbol_n_events = 0

        for tf in timeframes:
            logger.warning(f"[{symbol} {tf}m] دریافتِ دادهٔ تاریخی از بایننس...")
            # کمی حاشیه به عقب برای این‌که اولین کندلِ واقعیِ بازه هم history_bars کاملِ خودش را داشته باشد
            fetch_start = start_dt - timedelta(minutes=int(tf) * HISTORY_BARS * 1.2 + 60)
            df_full = fetch_full_history(symbol, tf, fetch_start, end_dt)
            run_meta["gaps"][(symbol, tf)] = df_full.attrs.get("gaps", [])
            if df_full.empty:
                logger.error(f"[{symbol} {tf}m] هیچ داده‌ای دریافت نشد — این ترکیب رد می‌شود.")
                continue
            if first_df_for_benchmark is None:
                # برشِ دقیقِ بازهٔ درخواستی برای بنچمارکِ Buy&Hold
                mask = (df_full.index >= start_dt) & (df_full.index <= end_dt)
                first_df_for_benchmark = df_full.loc[mask]

            logger.warning(f"[{symbol} {tf}m] {len(df_full)} کندل دریافت شد؛ اجرایِ موتورِ سیگنال...")

            if args.engine == "fast":
                _fast_engine_placeholder()

            events = generate_signals_exact(
                df_full, symbol, tf, HISTORY_BARS,
                workers=args.workers, keep_log=args.keep_log,
            )
            # فقط سیگنال‌های داخلِ بازهٔ درخواستی (نه حاشیهٔ warm-up) را نگه دار
            events = [e for e in events if global_start_ms <= e.signal_bar_ts_ms <= global_end_ms]
            logger.warning(f"[{symbol} {tf}m] {len(events)} سیگنال یافت شد؛ در حالِ حلِ نتیجهٔ هر معامله...")

            ts_to_idx = {int(ts.timestamp() * 1000): i for i, ts in enumerate(df_full.index)}
            trades = [resolve_trade(ev, df_full, ts_to_idx) for ev in events]
            all_trades.extend(trades)
            symbol_trades.extend(trades)
            symbol_n_events += len(events)

            sub_metrics = compute_portfolio_metrics(trades, df_full, global_start_ms, global_end_ms)
            per_symbol_tf[(symbol, tf)] = sub_metrics

            trades_by_bar = {t.event.signal_bar_ts_ms: t for t in trades}
            recent_sections.append(build_recent_signals_section(events, trades_by_bar, tf, recent_anchor_ms))

            # ----------------------------------------------------------------
            # پیامِ پایانِ این ترکیبِ خاصِ (نماد، تایم‌فریم)
            # ----------------------------------------------------------------
            tf_closed = _closed(trades)
            tf_pnl = sum(t.pnl_usd for t in tf_closed if t.pnl_usd is not None)
            tf_win_rate = (len([t for t in tf_closed if t.status == "WIN"]) / len(tf_closed) * 100) if tf_closed else None
            tf_done_msg = (
                f"☑️ {symbol} | تایم‌فریم {tf} دقیقه تمام شد.\n"
                f"سیگنال: {len(events)}  |  معاملهٔ بسته‌شده: {len(tf_closed)}  |  "
                f"Win Rate: {_fmt(tf_win_rate, 1, '%')}  |  PnL: ${_fmt(tf_pnl, 2)}"
            )
            logger.warning(tf_done_msg)
            notify_telegram(tf_done_msg)

            # جمع‌آوریِ دادهٔ تایم‌فریمِ ۱ دقیقه برای گزارشِ نهاییِ ۷روزه (txt+xlsx)
            if str(tf) == "1":
                recent_1m_sections.append(build_recent_signals_section(events, trades_by_bar, tf, recent_anchor_ms))
                _days1m, _ = recent_window_days("1")
                _cutoff1m_ms = recent_anchor_ms - _days1m * 86400 * 1000
                for ev in events:
                    if ev.signal_bar_ts_ms >= _cutoff1m_ms:
                        recent_1m_trades.append(trades_by_bar.get(ev.signal_bar_ts_ms))

            if args.determinism_check:
                run_meta["determinism"][(symbol, tf)] = determinism_check(df_full, symbol, tf, HISTORY_BARS)

            if args.lookahead_check:
                run_meta["lookahead"][(symbol, tf)] = lookahead_check(df_full, events, symbol, tf, HISTORY_BARS)

            if args.robust:
                robust_extra.setdefault("walk_forward", {})[(symbol, tf)] = walk_forward_validation(
                    df_full, symbol, tf, HISTORY_BARS, args.workers
                )

        # ----------------------------------------------------------------
        # پیامِ پایانِ بررسیِ کاملِ این نماد (روی همهٔ تایم‌فریم‌هایش)
        # ----------------------------------------------------------------
        symbol_elapsed_min = (_time_mod.time() - symbol_start_mono) / 60.0
        symbol_closed = _closed(symbol_trades)
        symbol_pnl = sum(t.pnl_usd for t in symbol_closed if t.pnl_usd is not None)
        symbol_wins = len([t for t in symbol_closed if t.status == "WIN"])
        symbol_win_rate = (symbol_wins / len(symbol_closed) * 100) if symbol_closed else None
        symbol_done_msg = (
            f"✅ بررسیِ {symbol} روی تایم‌فریم‌های [{', '.join(timeframes)}] تمام شد "
            f"({symbol_elapsed_min:.1f} دقیقه طول کشید).\n"
            f"سیگنال: {symbol_n_events}  |  معاملهٔ بسته‌شده: {len(symbol_closed)}  |  "
            f"Win Rate: {_fmt(symbol_win_rate, 1, '%')}  |  PnL: ${_fmt(symbol_pnl, 2)}"
        )
        logger.warning(symbol_done_msg)
        notify_telegram(symbol_done_msg)

    if args.robust:
        robust_extra["monte_carlo"] = monte_carlo_permutation_test(all_trades)

    portfolio_metrics = compute_portfolio_metrics(
        all_trades,
        first_df_for_benchmark if first_df_for_benchmark is not None else pd.DataFrame(),
        global_start_ms, global_end_ms,
    )
    breakdown = three_dim_breakdown(all_trades, min_samples=args.min_samples)
    half_split = half_split_validation(all_trades, breakdown)

    report_text = render_report(
        args, run_meta, per_symbol_tf, portfolio_metrics, breakdown, half_split,
        recent_sections, robust_extra,
    )

    out_path = args.output or f"backtest_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(report_text)
    print(f"\n[گزارش در فایل ذخیره شد: {out_path}]")

    if args.json_output:
        def _trade_to_dict(t: TradeResult) -> dict:
            d = asdict(t)
            d["event"]["algo_log"] = t.event.algo_log if args.keep_log else ""
            return d
        with open(args.json_output, "w", encoding="utf-8") as f:
            json.dump([_trade_to_dict(t) for t in all_trades], f, ensure_ascii=False, indent=2, default=str)
        print(f"[dumpِ کاملِ JSON معاملات: {args.json_output}]")

    # ------------------------------------------------------------------
    # گزارشِ ۷ روزِ اخیرِ تایم‌فریمِ ۱ دقیقه — txt + xlsx، به رباتِ جدید
    # ------------------------------------------------------------------
    if recent_1m_sections:
        days_1m, confirmed_1m = recent_window_days("1")
        header = (
            f"گزارشِ سیگنال‌های {days_1m} روزِ اخیر — تایم‌فریمِ ۱ دقیقه "
            f"({'✅ بازهٔ تاییدشده' if confirmed_1m else '⚠️ بازهٔ برون‌یابی‌شده'})\n"
            f"تولیدشده در: {datetime.now(UTC).astimezone(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')} (تهران)\n"
            + "=" * 78 + "\n"
        )
        recent_1m_text = header + "\n".join(recent_1m_sections)
        recent_1m_txt_path = f"recent_7d_1m_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.txt"
        with open(recent_1m_txt_path, "w", encoding="utf-8") as f:
            f.write(recent_1m_text)

        recent_1m_xlsx_path = None
        try:
            rows = []
            for t in recent_1m_trades:
                if t is None:
                    continue
                rows.append({
                    "symbol": t.event.symbol,
                    "signal": t.event.signal,
                    "signal_time_utc": ms_to_dt(t.event.signal_bar_ts_ms),
                    "entry": t.event.entry,
                    "stop": t.event.stop,
                    "target": t.event.target,
                    "status": t.status,
                    "exit_reason": t.exit_reason,
                    "exit_price": t.exit_price,
                    "exit_time_utc": ms_to_dt(t.exit_time_ms) if t.exit_time_ms else None,
                    "pnl_usd": t.pnl_usd,
                    "pnl_r": t.pnl_r,
                    "resolution_method": t.resolution_method,
                    "mae_pct": t.mae_pct,
                    "mfe_pct": t.mfe_pct,
                    "bars_held": t.bars_held,
                })
            if rows:
                df_recent_1m = pd.DataFrame(rows)
                recent_1m_xlsx_path = f"recent_7d_1m_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.xlsx"
                df_recent_1m.to_excel(recent_1m_xlsx_path, index=False)
        except Exception as e:
            logger.warning(f"ساختِ فایلِ اکسلِ گزارشِ ۷روزهٔ ۱دقیقه‌ای شکست خورد: {e}")
            recent_1m_xlsx_path = None

        notify_telegram_document(
            recent_1m_txt_path,
            caption=f"📄 گزارشِ سیگنال‌های {days_1m} روزِ اخیر — تایم‌فریمِ ۱ دقیقه (txt)",
        )
        if recent_1m_xlsx_path:
            notify_telegram_document(
                recent_1m_xlsx_path,
                caption=f"📊 نسخهٔ اکسلِ همان گزارش ({days_1m} روزِ اخیر، ۱ دقیقه)",
            )
    else:
        logger.warning("⚠️ برای گزارشِ ۷روزهٔ تایم‌فریمِ ۱ دقیقه سیگنالی یافت نشد (یا '1' جزوِ --timeframes نبود).")
        notify_telegram("⚠️ گزارشِ ۷روزهٔ تایم‌فریمِ ۱ دقیقه ساخته نشد: سیگنال/دادهٔ منطبقی پیدا نشد.")

    # ------------------------------------------------------------------
    # پیامِ پایانِ کاملِ بک‌تست
    # ------------------------------------------------------------------
    total_elapsed_min = (_time_mod.time() - run_start_mono) / 60.0
    final_msg = (
        "🏁 بک‌تست به‌طورِ کامل تمام شد.\n"
        f"مدتِ کلِ اجرا: {total_elapsed_min:.1f} دقیقه\n"
        f"کل سیگنال: {portfolio_metrics['n_signals_total']}  |  بسته‌شده: {portfolio_metrics['n_closed']}\n"
        f"Win Rate: {_fmt(portfolio_metrics['win_rate'], 1, '%')}  |  "
        f"PnL کل: ${_fmt(portfolio_metrics['total_pnl_usd'], 2)}\n"
        f"برچسبِ اعتبار: {portfolio_metrics.get('validity_label')}\n"
        f"فایلِ گزارش: {out_path}"
    )
    logger.warning(final_msg)
    notify_telegram(final_msg)


if __name__ == "__main__":
    main()

