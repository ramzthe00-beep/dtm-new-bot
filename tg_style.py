"""
tg_style.py — کیت ظاهری پیام‌های تلگرام (HTML parse mode)
===========================================================
- همه‌ی پیام‌های پروژه با parse_mode=HTML ارسال می‌شوند (bold / code / pre / italic).
- اگر تلگرام HTML را نپذیرفت (خطای 400)، همان پیام به‌صورت متن ساده ارسال می‌شود تا هیچ پیامی گم نشود.
"""
import html
import re
from datetime import datetime, timezone, timedelta

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

LINE = "━━━━━━━━━━━━━━━━━━━━"
THIN = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"

_FA_WEEKDAYS = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]


# ───────────────────────── escape / tags ─────────────────────────
def esc(x):
    return html.escape(str(x), quote=False)


def b(x):
    return f"<b>{esc(x)}</b>"


def i(x):
    return f"<i>{esc(x)}</i>"


def code(x):
    return f"<code>{esc(x)}</code>"


def pre(x, limit=1400):
    t = str(x)
    if len(t) > limit:
        t = t[:limit] + "\n… (ادامه برش خورد)"
    return f"<pre>{esc(t)}</pre>"


_TAG_RE = re.compile(r"</?(b|i|u|s|code|pre|a|tg-spoiler|tg-emoji|tg-time|blockquote|mark)(\s[^>]*)?>", re.IGNORECASE)


def plain_fallback(text):
    """HTML → متن ساده (برای وقتی که تلگرام parse را رد کرد)."""
    return html.unescape(_TAG_RE.sub("", str(text)))


def split_message(text, limit=3800):
    """تقسیم پیام بلند روی مرز خط (نه وسط تگ)."""
    text = str(text)
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for line in text.split("\n"):
        while len(line) > limit:           # خط خیلی بلند
            if cur:
                parts.append(cur); cur = ""
            parts.append(line[:limit]); line = line[limit:]
        if len(cur) + len(line) + 1 > limit:
            parts.append(cur); cur = line
        else:
            cur = f"{cur}\n{line}" if cur else line
    if cur:
        parts.append(cur)
    return parts


# ───────────────────────── visual helpers ─────────────────────────
def meter(value, maximum, width=10, fill="▰", empty="▱"):
    try:
        ratio = 0.0 if maximum <= 0 else max(0.0, min(1.0, float(value) / float(maximum)))
    except Exception:
        ratio = 0.0
    n = int(round(ratio * width))
    return fill * n + empty * (width - n)


_SPARK = "▁▂▃▄▅▆▇█"


def spark(values, max_points=24):
    vals = [float(v) for v in values]
    if not vals:
        return ""
    if len(vals) > max_points:               # نمونه‌برداری یکنواخت
        step = len(vals) / max_points
        vals = [vals[int(k * step)] for k in range(max_points)]
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-12:
        return _SPARK[3] * len(vals)
    return "".join(_SPARK[int((v - lo) / (hi - lo) * (len(_SPARK) - 1))] for v in vals)


def money(x, digits=2):
    if x is None:
        return "—"
    return f"{x:+.{digits}f}$"


def pct(x, digits=1):
    return f"{x:.{digits}f}%"


def price_prec_from_tick(mintick):
    s_ = f"{float(mintick):.10f}".rstrip("0")
    return len(s_.split(".")[1]) if "." in s_ else 0


def session_label(dt_utc=None):
    """سشن‌های فعال بازار (تقریبی بر اساس ساعت UTC)."""
    dt_utc = dt_utc or datetime.now(UTC_TZ)
    h = dt_utc.hour
    names = []
    if 0 <= h < 9:
        names.append("🌏 آسیا")
    if 7 <= h < 16:
        names.append("🇬🇧 لندن")
    if 12 <= h < 21:
        names.append("🗽 نیویورک")
    return " + ".join(names) if names else "🌙 خارج از سشن اصلی"


def fa_weekday(dt):
    return _FA_WEEKDAYS[dt.weekday()]


def now_pair(now_utc=None):
    n = now_utc or datetime.now(UTC_TZ)
    return n, n.astimezone(IRAN_TZ)
