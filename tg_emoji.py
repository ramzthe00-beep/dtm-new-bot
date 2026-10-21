"""
tg_emoji.py — ایموجی‌های سفارشی تلگرام (Premium custom emoji) برای پیام‌های ربات
================================================================================
Bot API 9.4: ربات می‌تواند در پیام‌های مستقیم (چت خصوصی/گروه/سوپرگروه) از ایموجی سفارشی استفاده کند،
به شرط اینکه «صاحب ربات» اشتراک Telegram Premium داشته باشد. (در کانال‌ها فقط با username خریداری‌شده از Fragment.)
بیننده‌ها نیازی به Premium ندارند.

تنظیم (متغیر محیطی، هر دو اختیاری):
  TG_EMOJI_PACKS = "PackName1,PackName2"     نام پک ایموجی (از لینک t.me/addemoji/PackName)
  TG_EMOJI_MAP   = '{"🎯":"5368324170671202286"}'   نگاشت دستی ایموجی → custom_emoji_id
  TG_CUSTOM_EMOJI = "0"                       خاموش‌کردن کامل (پیش‌فرض: روشن اگر پک/نگاشت تنظیم شده باشد)

هر ایموجی ساده‌ای که در پک وجود داشته باشد خودکار با نسخه‌ی سفارشی جایگزین می‌شود؛ بقیه عادی می‌مانند.
اگر تلگرام ایموجی سفارشی را نپذیرفت (مثلاً صاحب ربات Premium ندارد)، همان لحظه خاموش می‌شود و پیام ساده ارسال می‌شود.

اسکن پک:  python tg_emoji.py <BOT_TOKEN> <PackName>
"""
import html as _html
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

import requests

logger = logging.getLogger("TG_EMOJI")

_CACHE_FILE = Path.home() / "tg_emoji_cache.json"
_CACHE_TTL = 24 * 3600
_FE0F = "\ufe0f"

_map = {}            # emoji (بدون FE0F) → custom_emoji_id
_loaded = False
_disabled = False
_regex = None


def _norm(e):
    return e.replace(_FE0F, "")


def enabled():
    return (not _disabled) and os.getenv("TG_CUSTOM_EMOJI", "1") == "1" and bool(_map)


def disable(reason=""):
    global _disabled
    if not _disabled:
        logger.warning(f"[TG_EMOJI] custom emoji disabled for this run {reason}")
    _disabled = True


def _build_regex():
    global _regex
    keys = sorted(_map.keys(), key=len, reverse=True)
    _regex = re.compile("(" + "|".join(re.escape(k) for k in keys) + ")" + _FE0F + "?") if keys else None


def fetch_pack(token, name):
    """getStickerSet → {emoji: custom_emoji_id} (اولین استیکر برای هر ایموجی)."""
    r = requests.post(f"https://api.telegram.org/bot{token}/getStickerSet", json={"name": name}, timeout=20)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(data.get("description", "getStickerSet failed"))
    out = {}
    for st in data["result"].get("stickers", []):
        cid, em = st.get("custom_emoji_id"), st.get("emoji")
        if cid and em:
            out.setdefault(_norm(em), cid)
    return out


def load(token):
    """یک‌بار در شروع (یا اولین ارسال) صدا زده می‌شود. هیچ‌وقت exception نمی‌دهد."""
    global _loaded, _map
    if _loaded:
        return
    _loaded = True
    try:
        mapping = {}
        raw = os.getenv("TG_EMOJI_MAP", "").strip()
        if raw:
            for k, v in json.loads(raw).items():
                mapping[_norm(k)] = str(v)

        packs = [p.strip() for p in os.getenv("TG_EMOJI_PACKS", "").split(",") if p.strip()]
        cache = {}
        if _CACHE_FILE.exists():
            try:
                cache = json.loads(_CACHE_FILE.read_text())
            except Exception:
                cache = {}
        changed = False
        for p in packs:
            ent = cache.get(p)
            if not ent or time.time() - ent.get("ts", 0) > _CACHE_TTL:
                try:
                    ent = {"ts": time.time(), "map": fetch_pack(token, p)}
                    cache[p] = ent
                    changed = True
                    logger.info(f"[TG_EMOJI] pack '{p}' loaded: {len(ent['map'])} emoji")
                except Exception as e:
                    logger.warning(f"[TG_EMOJI] pack '{p}' failed: {e}")
                    ent = cache.get(p)
            if ent:
                for k, v in ent["map"].items():
                    mapping.setdefault(k, v)
        if changed:
            try:
                _CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False))
            except Exception:
                pass
        _map = mapping
        _build_regex()
        if _map:
            logger.info(f"[TG_EMOJI] active — {len(_map)} custom emoji mapped")
    except Exception as e:
        logger.warning(f"[TG_EMOJI] load failed: {e}")


def lookup(emoji):
    return _map.get(_norm(emoji))


_TAG_SPLIT = re.compile(r"(<[^>]+>)")


def apply_classic(html_text):
    """ایموجی‌های ساده‌ی نگاشت‌شده → <tg-emoji> (خارج از code/pre)."""
    if not enabled() or _regex is None:
        return html_text
    out, depth = [], 0
    for tok in _TAG_SPLIT.split(html_text):
        if tok.startswith("<") and tok.endswith(">"):
            low = tok.lower()
            if low.startswith(("<pre", "<code")):
                depth += 1
            elif low.startswith(("</pre", "</code")):
                depth = max(0, depth - 1)
            out.append(tok)
        elif depth or not tok:
            out.append(tok)
        else:
            out.append(_regex.sub(lambda m: f'<tg-emoji emoji-id="{_map[_norm(m.group(1))]}">{m.group(1)}</tg-emoji>', tok))
    return "".join(out)


def split_text_rich(text):
    """رشته → لیست (رشته | dict custom_emoji) برای Rich."""
    if not enabled() or _regex is None or not text:
        return text
    parts, pos = [], 0
    for m in _regex.finditer(text):
        if m.start() > pos:
            parts.append(text[pos:m.start()])
        parts.append({"type": "custom_emoji", "custom_emoji_id": _map[_norm(m.group(1))], "alternative_text": m.group(1)})
        pos = m.end()
    if not parts:
        return text
    if pos < len(text):
        parts.append(text[pos:])
    return parts


def apply_buttons(markup):
    """ایموجی ابتدای متن دکمه → icon_custom_emoji_id (اگر نگاشت داشته باشد)."""
    if not enabled() or not markup:
        return markup
    new = []
    for row in markup:
        nr = []
        for btn in row:
            b = dict(btn)
            txt = b.get("text", "")
            if txt:
                first = txt.split(" ", 1)[0]
                cid = lookup(first)
                if cid:
                    b["icon_custom_emoji_id"] = cid
                    b["text"] = txt[len(first):].strip() or txt
            nr.append(b)
        new.append(nr)
    return new


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python tg_emoji.py <BOT_TOKEN> <PackName>")
        sys.exit(1)
    m = fetch_pack(sys.argv[1], sys.argv[2])
    print(f"{len(m)} emoji in pack:")
    for k, v in m.items():
        print(k, v)
