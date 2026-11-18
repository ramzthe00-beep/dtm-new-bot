"""
exchange_diagnosis.py — تشخیص علت خطای صرافی (TheTrueTrade) و ساخت پیام‌های خطای تلگرام.

هر پیام خطا سه بخش دارد:
  📨 پاسخ کامل صرافی   (status + بدنه‌ی کامل؛ برای خطای اتصال: نوع و متن استثنا)
  🔍 علت رد            (بر اساس کد/وضعیت/متن پیام صرافی یا نوع خطای اتصال)
  🛠 راهکار عملی       (قدم‌های مشخص، با نام متغیرها/تنظیمات همین ربات)

منبع علت‌ها: «Error reference» مستندات API صرافی + وضعیت HTTP + متن پیام + نوع خطای اتصال.
اگر علت دقیقاً از کد صرافی نیامده باشد، برچسب «محتمل» می‌خورد تا گمراه‌کننده نباشد.
"""
import json
import re
from datetime import datetime, timezone

from tg_style import esc
from tg_rich import Card

MAX_BODY_CHARS = 2500
_KEEP_HEADERS = ("retry-after", "x-ratelimit", "ratelimit")


# ─────────────────────────── ثبت خطا ───────────────────────────
def capture_error(method, uri, exc, response=None):
    """خطای یک درخواست را به‌صورت دیکشنری ذخیره می‌کند. هرگز استثنا نمی‌اندازد."""
    try:
        d = {
            "method": str(method).upper(), "uri": str(uri),
            "exc_type": type(exc).__name__ if exc is not None else None,
            "exc_text": repr(exc) if exc is not None else "",
            "status": None, "body": None, "headers": {},
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        }
        if response is not None:
            d["status"] = getattr(response, "status_code", None)
            d["body"] = getattr(response, "text", None)
            try:
                for k, v in response.headers.items():
                    if str(k).lower().startswith(_KEEP_HEADERS):
                        d["headers"][k] = v
            except Exception:
                pass
        return d
    except Exception:
        return {"method": str(method), "uri": str(uri), "exc_type": None, "exc_text": "",
                "status": None, "body": None, "headers": {}, "ts": ""}


def synthetic_response(method, uri, status, obj):
    """برای وقتی که صرافی خطا نداده ولی پاسخ آن (مثلاً GET پوزیشن) باید نشان داده شود."""
    try:
        body = json.dumps(obj, ensure_ascii=False, indent=2, default=str)
    except Exception:
        body = str(obj)
    return {"method": str(method).upper(), "uri": str(uri), "exc_type": None, "exc_text": "",
            "status": status, "body": body, "headers": {},
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}


# ─────────────────────────── پاسخ کامل ───────────────────────────
def response_text(err):
    """متن کامل پاسخ صرافی (یا توضیح اینکه پاسخی نیامده) برای نمایش در بلوک pre."""
    if not err:
        return "(اطلاعاتی از پاسخ صرافی ثبت نشده است)"
    lines = [f"{err.get('method', '')} {err.get('uri', '')}"]
    if err.get("ts"):
        lines.append(f"زمان: {err['ts']}")
    if err.get("status") is not None:
        lines.append(f"HTTP {err['status']}")
        body = err.get("body")
        if body is None or str(body).strip() == "":
            lines.append("(بدنه‌ی پاسخ خالی است)")
        else:
            txt = str(body)
            try:
                txt = json.dumps(json.loads(txt), ensure_ascii=False, indent=2)
            except Exception:
                pass
            if len(txt) > MAX_BODY_CHARS:
                txt = txt[:MAX_BODY_CHARS] + f"\n… (بریده شد؛ {len(txt) - MAX_BODY_CHARS} کاراکتر دیگر در لاگ سرور هست)"
            lines.append(txt)
        for k, v in (err.get("headers") or {}).items():
            lines.append(f"{k}: {v}")
    else:
        lines.append("پاسخ HTTP دریافت نشد (خطا در سطح اتصال، قبل از رسیدن پاسخ از صرافی)")
        lines.append(f"{err.get('exc_type') or ''}: {err.get('exc_text') or ''}".strip(": "))
    return "\n".join(lines)


# ─────────────────────────── پایگاه دانش علت‌ها ───────────────────────────
_AUTH_STEPS = [
    "مقدار API_KEY و API_SECRET در متغیرهای محیطی هاست را با کلید ساخته‌شده در TheTrueTrade (API Management) یکی کن؛ فاصله یا کاراکتر اضافه نباشد.",
    "ساعت سرور هاست باید با UTC هماهنگ باشد؛ اختلاف بیش از ۳۰ ثانیه با ساعت صرافی رد می‌شود.",
    "اگر برای کلید IP allowlist فعال است، IP خروجی هاست (در Railway ممکن است عوض شود) را اضافه کن یا allowlist را موقتاً بردار.",
    "مطمئن شو کلید فعال و منقضی‌نشده است.",
]
_SCOPE_STEPS = [
    "در TheTrueTrade > API Management برای همین کلید scope با نام api-keys.trade-futures را فعال کن (همه‌ی مسیرهای /futures به آن نیاز دارند) یا کلید جدید با این scope بساز.",
    "بعد از تغییر کلید، API_KEY و API_SECRET را در هاست به‌روز کن و ربات را ری‌استارت کن.",
]
_CODE_INFO = {
    "E_SECURITY_UNAUTHENTICATED": (
        "احراز هویت درخواست ردشد. صرافی این کد را برای امضای نامعتبر، timestamp خارج از پنجره‌ی ۳۰ ثانیه، کلید اشتباه و IP غیرمجاز یکسان برمی‌گرداند.",
        _AUTH_STEPS),
    "E_HTTP_UNAUTHORIZED_EXCEPTION": ("دسترسی بدون احراز هویت معتبر ردشد.", _AUTH_STEPS),
    "E_DATA_API_KEY_NOT_FOUND": (
        "صرافی کلید API ارسال‌شده را پیدا نکرد (کلید اشتباه، حذف‌شده یا از حساب دیگر است).",
        ["در API Management وجود کلید را بررسی کن؛ اگر حذف شده کلید جدید بساز و API_KEY/API_SECRET را در هاست به‌روز کن."]),
    "E_SECURITY_PERMISSION_DENIED": ("کلید API دسترسی (scope) لازم برای این درخواست را ندارد.", _SCOPE_STEPS),
    "E_DATA_PERMISSIONS_NOT_FOUND": ("کلید API دسترسی (scope) لازم برای این درخواست را ندارد.", _SCOPE_STEPS),
    "E_BUSINESS_RULE_API_KEY_NOT_ACTIVE": (
        "کلید API فعال نیست (غیرفعال، منقضی یا لغوشده).",
        ["در API Management وضعیت و تاریخ انقضای کلید را ببین؛ فعالش کن یا کلید جدید بساز و در هاست به‌روز کن."]),
    "E_SYSTEM_INTERNAL_SERVER_ERROR": (
        "خطای داخلی در سرور صرافی (سمت صرافی است، نه ربات).",
        ["۱ تا ۲ دقیقه صبر کن و دوباره امتحان کن؛ اگر ادامه داشت به پشتیبانی TheTrueTrade اطلاع بده.",
         "قبل از تلاش دستی، پوزیشن‌های باز را در صرافی چک کن تا سفارش تکراری باز نشود."]),
    "E_BUSINESS_RULE_INSUFFICIENT_FUNDS": (
        "موجودی قابل‌استفاده برای این عملیات کافی نیست.",
        ["availableBalance حساب futures (walletType: debit) را در صرافی ببین؛ مارجینِ پوزیشن‌های باز از آن کم می‌شود.",
         "موجودی را افزایش بده یا سرمایه‌ی هر معامله را کمتر کن."]),
}

_STATUS_INFO = {
    400: ("درخواست نامعتبر: صرافی یکی از پارامترها را قبول نکرد (فیلد و پیام صرافی در پاسخ بالا آمده).",
          ["فیلد و پیام صرافی را بخوان و مقدار همان پارامتر را در کد/تنظیمات اصلاح کن."]),
    401: ("احراز هویت ناموفق بود (کلید/امضا/زمان/IP).", _AUTH_STEPS),
    403: ("دسترسی ردشد: scope کلید، IP مجاز یا وضعیت کلید مشکل دارد.", _SCOPE_STEPS + _AUTH_STEPS[2:]),
    404: ("منبع مورد نظر پیدا نشد (پوزیشن/سفارش/مسیر وجود ندارد؛ معمولاً پوزیشن قبلاً بسته شده است).",
          ["پوزیشن‌های باز را در صرافی ببین؛ اگر پوزیشن بسته شده این خطا طبیعی است و اقدامی لازم نیست."]),
    409: ("تداخل وضعیت: صرافی عملیات را با وضعیت فعلی سازگار ندید.", ["وضعیت پوزیشن/سفارش را در صرافی ببین و بعد دوباره امتحان کن."]),
    422: ("قانون کسب‌وکار صرافی اجازه‌ی این عملیات را نداد (مثلاً موجودی، حداقل/حداکثر مقدار یا وضعیت پوزیشن).",
          ["پیام صرافی در پاسخ بالا قاعده‌ی دقیق را می‌گوید؛ مقدار مربوط را مطابق آن اصلاح کن."]),
    429: ("محدودیت نرخ درخواست (Rate Limit): تعداد درخواست‌ها از سقف صرافی بیشتر شد.",
          ["TRUETRADE_MIN_INTERVAL (فاصله‌ی بین درخواست‌ها، الان پیش‌فرض ۱.۵ ثانیه) را بیشتر کن.",
           "تعداد نمادها/درخواست‌های هم‌زمان را کم کن؛ اگر Retry-After در پاسخ بالا هست همان‌قدر صبر کن."]),
}

_KEYWORDS = [
    (("leverage",),
     "نشانه‌ی پیام: اهرم خارج از بازه‌ی مجاز همین بازار است.",
     ["LEVERAGE_MAP برای این نماد را در بازه‌ی مجاز بازار بگذار (بازه‌ی دقیق در پیام صرافی آمده؛ در مثال مستندات ۱ تا ۱۰۰ است)."]),
    (("stoploss", "stop loss", "stop_loss", "takeprofit", "take profit", "take_profit"),
     "نشانه‌ی پیام: قیمت استاپ/تارگت نسبت به قیمت ورود/لحظه‌ای معتبر نیست (سمت اشتباه یا بیش از حد نزدیک).",
     ["قیمت از لحظه‌ی سیگنال تا ارسال سفارش حرکت کرده؛ فاصله‌ی استاپ/تارگت تا قیمت لحظه‌ای را در لاگ (لنگر اجرا) ببین.",
      "اگر استاپ خیلی تنگ است، سیگنال را رد کن یا فاصله‌ی حداقلی بگذار."]),
    (("minimum", "at least", "too small", "min order", "min cost", "min size"),
     "نشانه‌ی پیام: مقدار سفارش از حداقل مجاز بازار کمتر است.",
     ["سرمایه‌ی سفارش (cost) را بالاتر ببر؛ MIN_ORDER_COST_USDT را فقط وقتی پایین بیاور که صرافی واقعاً سفارش کوچک‌تر را می‌پذیرد."]),
    (("insufficient", "not enough", "balance", "funds"),
     "نشانه‌ی پیام: موجودی/مارجین کافی نیست.",
     ["موجودی قابل‌استفاده‌ی futures را افزایش بده یا مقدار سفارش را کم کن."]),
    (("precision", "decimal places", "tick size", "step size"),
     "نشانه‌ی پیام: تعداد اعشار یا گام قیمت/مقدار درست نیست.",
     ["TICK_SIZES و PRICE_PRECISION این نماد را با مشخصات بازار در صرافی تطبیق بده."]),
    (("symbol not found", "invalid symbol", "unknown symbol", "market not found", "market closed", "market is closed",
      "not tradable", "trading suspended"),
     "نشانه‌ی پیام: نماد/بازار نامعتبر یا فعلاً در دسترس نیست.",
     ["نام نماد در SYMBOLS را با نام بازار در صرافی مقایسه کن و وضعیت بازار را چک کن."]),
]

_EXC_INFO = [
    (("connectionreset", "connection reset", "connection aborted", "protocolerror", "remotedisconnected", "broken pipe"),
     "سرور/گیت‌وی صرافی اتصال را وسط درخواست قطع کرد (Connection reset by peer). مشکل کلید، امضا یا پارامتر نیست؛ معمولاً اتصال keep-alive قدیمی یا قطعی لحظه‌ای مسیر است.",
     ["معمولاً گذراست؛ ربات در چرخه‌ی بعدی دوباره امتحان می‌کند.",
      "اگر چند بار در ساعت تکرار شد: وضعیت سرویس thetruetrade و شبکه‌ی هاست را چک کن یا ریجن هاست را عوض کن.",
      "راهکار کد: برای درخواست‌های GET چند بار تلاش مجدد با اتصال تازه (برای POST سفارش هرگز، چون ممکن است سفارش تکراری شود)."]),
    (("timeout", "timed out"),
     "صرافی در مهلت مقرر (۱۵ ثانیه) جواب نداد: کندی/ازدحام صرافی یا شبکه‌ی هاست.",
     ["چند ثانیه صبر کن؛ ربات دوباره امتحان می‌کند.", "اگر تکرار شد وضعیت thetruetrade و تأخیر شبکه‌ی هاست را بررسی کن."]),
    (("ssl", "certificate"),
     "خطای TLS/SSL در برقراری ارتباط امن با صرافی.",
     ["ساعت سرور و گواهی‌های سیستم هاست را بررسی کن؛ BASE_URL باید https://apiv2.thetruetrade.io باشد."]),
    (("nameresolution", "name or service not known", "temporary failure in name resolution", "gaierror", "getaddrinfo"),
     "DNS آدرس صرافی را resolve نکرد (مشکل شبکه/DNS هاست).",
     ["BASE_URL را بررسی کن و دسترسی DNS هاست را چک کن؛ معمولاً با ری‌استارت/تغییر ریجن هاست حل می‌شود."]),
    (("connectionrefused", "connection refused", "max retries exceeded", "newconnectionerror"),
     "اتصال به سرور صرافی برقرار نشد (رد یا در دسترس نیست).",
     ["BASE_URL و دسترسی شبکه‌ی هاست به apiv2.thetruetrade.io را بررسی کن؛ اگر صرافی در دست نگهداری است صبر کن."]),
]

_BASIS = {"code": "کد خطای صرافی (طبق مستندات)",
          "status": "کد وضعیت HTTP — تشخیص محتمل",
          "message": "متن پیام صرافی — تشخیص محتمل",
          "exception": "نوع خطای اتصال — تشخیص محتمل",
          "unknown": ""}


def _error_items(body):
    out = []
    try:
        data = json.loads(body or "")
        errs = data.get("errors") if isinstance(data, dict) else None
        if isinstance(errs, list):
            for e in errs:
                if isinstance(e, dict):
                    out.append((str(e.get("field") or ""), str(e.get("message") or "")))
    except Exception:
        pass
    return out


def diagnose(err, context="generic"):
    """خروجی: dict(reason, steps, basis, note)"""
    err = err or {}
    status = err.get("status")
    body = str(err.get("body") or "")
    low = body.lower()
    reason, steps, basis = None, [], "unknown"

    if status is None:                                   # خطای سطح اتصال
        ex = f"{err.get('exc_type') or ''} {err.get('exc_text') or ''}".lower()
        for keys, r, s in _EXC_INFO:
            if any(k in ex for k in keys):
                reason, steps, basis = r, list(s), "exception"
                break
        if reason is None:
            reason = "ارتباط با صرافی برقرار نشد و پاسخی نیامد؛ نوع خطا در بخش پاسخ بالا آمده است."
            steps = ["لاگ سرور (EXCHANGE REQUEST EXCEPTION) را ببین؛ اگر تکرار شد شبکه‌ی هاست و وضعیت صرافی را بررسی کن."]
    else:
        codes = re.findall(r"E_[A-Z0-9_]+", body)
        for c in codes:
            if c in _CODE_INFO:
                reason, steps = _CODE_INFO[c][0], list(_CODE_INFO[c][1])
                basis = "code"
                break
        if reason is None and status in _STATUS_INFO:
            reason, steps = _STATUS_INFO[status][0], list(_STATUS_INFO[status][1])
            basis = "status"
        if reason is None and status >= 500:
            reason = f"خطای سمت صرافی/گیت‌وی (HTTP {status})."
            steps = ["۱ تا ۲ دقیقه صبر کن و دوباره امتحان کن؛ اگر ادامه داشت به پشتیبانی TheTrueTrade اطلاع بده.",
                     "قبل از هر اقدام دستی، پوزیشن‌های باز را در صرافی چک کن."]
            basis = "status"
        if reason is None:
            reason = f"صرافی با HTTP {status} درخواست را رد کرد؛ علت دقیق در متن پاسخ بالا آمده."
            steps = ["متن پاسخ صرافی را بخوان و پارامتر مربوط را اصلاح کن."]
        # فیلد/پیام‌های ساختاریافته + نشانه‌های متنی (فقط برای خطاهای کلاینت)
        if status < 500:
            items = [(f, m) for f, m in _error_items(body) if f]
            if items:
                reason += " فیلد: " + " | ".join(f"{f}: {m}" for f, m in items[:4])
            if basis != "code":
                for keys, r, s in _KEYWORDS:
                    if any(k in low for k in keys):
                        reason += " " + r
                        steps += [x for x in s if x not in steps]
                        basis = "message"
                        break

    note = None
    if context == "connection":
        note = ("تا برقراری اتصال سفارش‌گذاری و پایش ریسک‌فری متوقف است؛ ربات ۶۰ ثانیه بعد دوباره تلاش می‌کند "
                "و چک کندل همان دقیقه ممکن است از دست برود.")
    elif context == "order":
        if status is not None and 400 <= status < 500:
            note = "سفارش توسط صرافی رد شد؛ پوزیشنی باز نشده و مارجینی درگیر نشده است."
        else:
            note = ("نتیجه‌ی سفارش نامعلوم است: ممکن است درخواست به صرافی رسیده و پوزیشن باز شده باشد. "
                    "قبل از هر اقدام، پوزیشن‌های باز را در صرافی بررسی کن.")
    elif context == "risk_free_patch":
        note = ("پوزیشن با استاپ قبلی باقی مانده است؛ اگر قیمت برگردد ممکن است با ضرر کامل بسته شود. "
                "در صورت نیاز استاپ را دستی به نقطه‌ی ورود ببر.")
    elif context == "rf_mismatch":
        reason = ("صرافی درخواست تغییر استاپ را پذیرفت (HTTP 2xx) ولی در خواندن مجدد، استاپ ثبت‌شده روی پوزیشن "
                  "با مقدار درخواستی برابر نیست (پاسخ GET بالا).")
        steps = ["فیلد stopLoss در پاسخ بالا را با مقدار درخواستی مقایسه کن.",
                 "بدنه‌ی PATCH را در لاگ (خط «[RISK-FREE] update SL request») و پاسخ صرافی به آن را بررسی کن.",
                 "تا روشن شدن علت، استاپ پوزیشن را دستی به نقطه‌ی ورود ببر."]
        basis = "unknown"
        note = "پوزیشن با استاپ قبلی باقی مانده است."
    elif context == "tp_changed":
        reason = ("بعد از تغییر استاپ، تارگت (takeProfit) پوزیشن روی صرافی با مقدار قبلی برابر نیست (پاسخ GET بالا).")
        steps = ["تارگت فعلی پوزیشن را در صرافی ببین و در صورت نیاز دستی اصلاح کن.",
                 "اگر تکرار شد، پاسخ PATCH را برای بررسی رفتار صرافی نگه دار."]
        basis = "unknown"
    return {"reason": reason, "steps": steps, "basis": basis, "note": note}


# ─────────────────────────── ساخت بلوک‌های کارت ───────────────────────────
def append_diagnosis(card, err=None, context="generic", reason=None, steps=None, response_note=None):
    """
    سه بخش (پاسخ کامل صرافی، علت، راهکار) را به انتهای کارت اضافه می‌کند.
    reason/steps اگر داده شوند جای تشخیص خودکار را می‌گیرند (برای رد شدن‌های سمت ربات).
    هرگز استثنا نمی‌اندازد.
    """
    try:
        d = diagnose(err, context) if (err is not None or reason is None) else {"reason": reason, "steps": steps or [],
                                                                                 "basis": "unknown", "note": None}
        if reason is not None:
            d["reason"], d["basis"] = reason, "unknown"
        if steps is not None:
            d["steps"] = steps
        card.add(("h", "📨 پاسخ کامل صرافی"))
        if err is not None:
            card.add(("pre", response_text(err)))
        else:
            card.add(("p", esc(response_note or "درخواستی به صرافی ارسال نشد؛ رد در سمت ربات انجام شد.")))
        card.add(("h", "🔍 علت رد"))
        card.add(("p", esc(d["reason"])))
        basis_txt = _BASIS.get(d["basis"], "")
        if basis_txt:
            card.add(("p", f"<i>🏷 منبع تشخیص: {esc(basis_txt)}</i>"))
        if d.get("note"):
            card.add(("p", "ℹ️ " + esc(d["note"])))
        card.add(("h", "🛠 راهکار عملی"))
        card.add(("list", [esc(s) for s in d["steps"]] or [esc("جزئیات بیشتر در لاگ سرور است.")]))
    except Exception as e:  # پیام خطا نباید خودش خطا بدهد
        card.add(("p", esc(f"(ساخت بخش تشخیص خطا ناموفق بود: {e})")))
    return card


def order_failed_card_full(symbol, side, leverage, cost, body_json, err):
    """کارت ثبت سفارش ناموفق با پاسخ کامل صرافی + علت + راهکار (جایگزین tgm.order_failed_card که پاسخ را ۹۰۰ کاراکتر می‌برید)."""
    card = Card([
        ("title", "🏹", f"{symbol} | ORDER FAILED ❌", f"{side} · {leverage}x · مارجین {cost}"),
        ("p", "🚨 ثبت سفارش انجام نشد."),
    ])
    append_diagnosis(card, err, "order")
    card.add(("details", "📦 REQUEST BODY", [("pre", str(body_json)[:900])], False))
    return card
