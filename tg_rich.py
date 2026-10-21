"""
tg_rich.py — لایه‌ی مدرن پیام‌های تلگرام (Bot API 10.x)
=========================================================
هر پیام یک «Card» است (ساختار بلوکی)، و سه نمای خروجی دارد:
  1) rich()  → Rich Message (sendRichMessage، Bot API ≥ 10.1): جدول، RTL واقعی، بخش جمع‌شونده، زمان محلی کاربر
  2) html()  → HTML کلاسیک (sendMessage) — fallback خودکار
  3) plain() → متن ساده — آخرین fallback

ارسال (deliver): Rich → HTML → متن ساده. اگر Rich خطا بدهد همان پیام با HTML کلاسیک می‌رود
و بعد از ۳ خطای پشت‌سرهم Rich برای ادامه‌ی اجرا خاموش می‌شود.
دکمه‌ها: copy_text (کپی ورود/استاپ/تارگت) + لینک چارت، با رنگ‌بندی style (primary/success/danger).

قرارداد متن‌ها: هر «fragment» یک تکه‌ی HTML کلاسیک است (escape شده) با تگ‌های b / i / u / s / code / mark / tg-time.
"""
import html as _html
import json
import logging
import os
import re
import time

import requests

import tg_emoji
from tg_style import LINE, plain_fallback, split_message

logger = logging.getLogger("TELEGRAM")

# ───────────────────────── تنظیمات ─────────────────────────
def rich_enabled():
    # پیش‌فرض خاموش: HTML کلاسیک دقیقاً همان چیدمانِ خطیِ کانال‌های سیگنال را می‌دهد. روشن‌کردن: TG_RICH=1
    return os.getenv("TG_RICH", "0") == "1"


_rich_dead = False
_rich_fail_streak = 0
_RICH_MAX_FAILS = 3

# ═══════════════════════════════════════════════════════════
# پارسر fragment → RichText
# ═══════════════════════════════════════════════════════════
_TOKEN_RE = re.compile(r"(<[^>]+>)")
_ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')
_SIMPLE = {"b": "bold", "strong": "bold", "i": "italic", "em": "italic", "u": "underline",
           "s": "strikethrough", "code": "code", "mark": "marked"}


def parse_inline(fragment):
    """fragment (HTML کلاسیک) → RichText (str | list | dict)."""
    s = str(fragment)
    root = []
    stack = [("root", None, root)]
    for tok in _TOKEN_RE.split(s):
        if not tok:
            continue
        if tok.startswith("<") and tok.endswith(">"):
            body = tok[1:-1].strip()
            if body.startswith("/"):
                name = body[1:].strip().lower()
                if len(stack) > 1 and stack[-1][0] == name:
                    nm, attrs, children = stack.pop()
                    node = _make_node(nm, attrs, children)
                    stack[-1][2].append(node)
                continue
            parts = body.split(None, 1)
            name = parts[0].lower()
            attrs = dict(_ATTR_RE.findall(parts[1])) if len(parts) > 1 else {}
            if name in _SIMPLE or name == "tg-time":
                stack.append((name, attrs, []))
            elif name == "br":
                stack[-1][2].append("\n")
            # تگ‌های ناشناخته نادیده گرفته می‌شوند
        else:
            txt = tg_emoji.split_text_rich(_html.unescape(tok))
            if isinstance(txt, list):
                stack[-1][2].extend(txt)
            else:
                stack[-1][2].append(txt)
    while len(stack) > 1:                       # تگ‌های بسته‌نشده
        nm, attrs, children = stack.pop()
        stack[-1][2].append(_make_node(nm, attrs, children))
    return _collapse(root)


def _collapse(children):
    out = []
    for c in children:
        if isinstance(c, str) and out and isinstance(out[-1], str):
            out[-1] += c
        else:
            out.append(c)
    if not out:
        return ""
    return out[0] if len(out) == 1 else out


def _make_node(name, attrs, children):
    inner = _collapse(children)
    if name == "tg-time":
        try:
            return {"type": "date_time", "text": inner or "", "unix_time": int(attrs.get("unix", "0")),
                    "date_time_format": attrs.get("format", "wDT")}
        except ValueError:
            return inner
    return {"type": _SIMPLE[name], "text": inner}


_TIME_RE = re.compile(r"<tg-time[^>]*>(.*?)</tg-time>", re.DOTALL)


def to_classic(fragment):
    """fragment → HTML امن برای sendMessage (tg-time → متن، mark → b)."""
    s = _TIME_RE.sub(r"\1", str(fragment))
    return s.replace("<mark>", "<b>").replace("</mark>", "</b>")


def to_plain(fragment):
    return plain_fallback(_TIME_RE.sub(r"\1", str(fragment)))


# ═══════════════════════════════════════════════════════════
# Card
# ═══════════════════════════════════════════════════════════
def _cell(text, header=False, align="right"):
    return {"text": parse_inline(text), "is_header": True, "align": align, "valign": "middle"} if header \
        else {"text": parse_inline(text), "align": align, "valign": "middle"}


class Card:
    def __init__(self, blocks=None, buttons=None, rich_ok=True):
        self.blocks = list(blocks or [])
        self.buttons = buttons          # inline_keyboard: list[list[dict]]
        self.rich_ok = rich_ok

    # ── ساخت ──
    @classmethod
    def from_html(cls, text):
        return cls([("raw", str(text))], rich_ok=False)

    def add(self, *blocks):
        self.blocks.extend(blocks)
        return self

    def add_note(self, fragment):
        """یک خط اضافه (fragment) به انتهای کارت — قبل از فوتر."""
        if not str(fragment).strip():
            return self
        idx = len(self.blocks)
        if self.blocks and self.blocks[-1][0] == "footer":
            idx -= 1
        self.blocks.insert(idx, ("p", str(fragment).strip()))
        return self

    def __add__(self, other):
        if isinstance(other, Card):
            return Card(self.blocks + [("hr",)] + other.blocks, self.buttons, self.rich_ok and other.rich_ok)
        return Card(self.blocks + [("raw", "\n" + str(other))], self.buttons, False)

    def __len__(self):
        return len(self.html())

    def __str__(self):
        return self.html()

    # ── نمای کلاسیک ──
    def _html_lines(self, blocks):
        out = []
        for b in blocks:
            k = b[0]
            if k == "raw":
                out.append(b[1])
            elif k == "title":
                _, emoji, text, sub = b
                out.append(f"<b>{emoji} {to_classic(text)}</b>")
                if sub:
                    out.append(to_classic(sub))
            elif k == "lines":
                out.extend(to_classic(x) for x in b[1])
            elif k == "h":
                out.append(f"<b>{to_classic(b[1])}</b>")
            elif k == "kv":
                for icon, label, value in b[1]:
                    out.append(f"{icon} {to_classic(label)}: {to_classic(value)}")
            elif k == "p":
                out.append(to_classic(b[1]))
            elif k == "hr":
                pass                      # در نمای کلاسیک جداکننده نداریم؛ فاصله‌ی خط خالی کافی است
            elif k == "pre":
                out.append(f"<pre>{_html.escape(str(b[1]), quote=False)}</pre>")
            elif k == "details":
                _, summary, inner, _open = b
                out.append(f"<b>{to_classic(summary)}</b>")
                out.append("<blockquote expandable>" + "\n".join(self._html_lines(inner)) + "</blockquote>")
            elif k == "list":
                out.extend(f"• {to_classic(x)}" for x in b[1])
            elif k == "table":
                _, header, rows, _aligns, caption = b
                if caption:
                    out.append(f"<b>{to_classic(caption)}</b>")
                for r in rows:
                    out.append(" · ".join(to_classic(c) for c in r if str(c).strip()))
            elif k == "progress":
                for label, price, pct_txt, status in b[1]:
                    out.append(f"{label}: {to_classic(price)} → {to_classic(pct_txt)} {status}")
            elif k == "kpi":
                out.append("  ·  ".join(f"{to_classic(l)}: <b>{to_classic(v)}</b>" for l, v in b[1]))
            elif k == "quote":
                out.append(f"<blockquote>{to_classic(b[1])}</blockquote>")
            elif k == "footer":
                out.append(f"<i>{to_classic(b[1])}</i>")
        return out

    def html(self):
        chunks, prev_flow = [], False
        for blk in self.blocks:
            ls = self._html_lines([blk])
            if not ls:
                continue
            flow = blk[0] in ("p", "lines")          # خطوط پشت‌سرهم یک «پاراگراف» می‌شوند (بدون خط خالی اضافه)
            if flow and prev_flow and chunks:
                chunks[-1] += "\n" + "\n".join(ls)
            else:
                chunks.append("\n".join(ls))
            prev_flow = flow
        return "\n\n".join(chunks)

    def plain(self):
        return plain_fallback(self.html())

    # ── نمای Rich ──
    def _rich_blocks(self, blocks):
        out = []
        for b in blocks:
            k = b[0]
            if k == "title":
                _, emoji, text, sub = b
                out.append({"type": "heading", "text": parse_inline(f"{emoji} {text}"), "size": 2})
                if sub:
                    out.append({"type": "paragraph", "text": {"type": "italic", "text": parse_inline(sub)}})
            elif k == "h":
                out.append({"type": "heading", "text": parse_inline(b[1]), "size": 3})
            elif k == "kv":
                cells = [[_cell(f"{icon} {label}", align="right"), _cell(value, align="left")]
                         for icon, label, value in b[1]]
                out.append({"type": "table", "cells": cells, "is_compact": True, "is_striped": True})
            elif k == "lines":
                out.extend({"type": "paragraph", "text": parse_inline(x)} for x in b[1])
            elif k == "p":
                for part in str(b[1]).split("\n"):
                    if part.strip():
                        out.append({"type": "paragraph", "text": parse_inline(part)})
            elif k == "hr":
                out.append({"type": "divider"})
            elif k == "pre":
                out.append({"type": "pre", "text": str(b[1])})
            elif k == "details":
                _, summary, inner, is_open = b
                d = {"type": "details", "summary": parse_inline(summary), "blocks": self._rich_blocks(inner)}
                if is_open:
                    d["is_open"] = True
                out.append(d)
            elif k == "list":
                out.append({"type": "list", "items": [
                    {"blocks": [{"type": "paragraph", "text": parse_inline(x)}]} for x in b[1]]})
            elif k == "table":
                _, header, rows, aligns, caption = b
                cells = []
                if header:
                    cells.append([_cell(h, header=True, align=(aligns[i] if aligns else "right"))
                                  for i, h in enumerate(header)])
                for r in rows:
                    cells.append([_cell(c, align=(aligns[i] if aligns else "right")) for i, c in enumerate(r)])
                t = {"type": "table", "cells": cells, "is_bordered": True, "is_striped": True, "is_compact": True}
                if caption:
                    t["caption"] = parse_inline(caption)
                out.append(t)
            elif k == "progress":
                cells = [[_cell(label, align="right"), _cell(price, align="center"),
                          _cell(pct_txt, align="center"), _cell(status, align="center")]
                         for label, price, pct_txt, status in b[1]]
                out.append({"type": "table", "cells": cells, "is_compact": True})
            elif k == "kpi":
                items = b[1]
                cells = [[_cell(l, header=True, align="center") for l, _v in items],
                         [_cell(f"<b>{v}</b>", align="center") for _l, v in items]]
                out.append({"type": "table", "cells": cells, "is_bordered": True, "is_compact": True})
            elif k == "quote":
                out.append({"type": "blockquote", "blocks": [{"type": "paragraph", "text": parse_inline(b[1])}]})
            elif k == "footer":
                out.append({"type": "footer", "text": parse_inline(b[1])})
        return out

    def rich(self):
        return {"blocks": self._rich_blocks(self.blocks), "is_rtl": True, "skip_entity_detection": True}


# ═══════════════════════════════════════════════════════════
# ارسال: Rich → HTML → متن ساده
# ═══════════════════════════════════════════════════════════
def _api(token, method, payload, timeout=30):
    """یک درخواست؛ 429 را با retry_after مدیریت می‌کند. خروجی: (ok, status, text)."""
    url = f"https://api.telegram.org/bot{token}/{method}"
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, timeout=timeout)
        except Exception as e:
            logger.error(f"[TELEGRAM] {method} exception: {e}")
            if attempt == 2:
                return False, 0, str(e)
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 429:
            try:
                wait = min(int(r.json().get("parameters", {}).get("retry_after", 10)) + 2, 30)
            except Exception:
                wait = 10
            if attempt == 2:
                return False, 429, r.text[:300]
            logger.warning(f"[TELEGRAM] rate limit, retry in {wait}s")
            time.sleep(wait)
            continue
        return r.status_code == 200, r.status_code, r.text
    return False, 0, ""


def _send_classic(token, chat_id, html_text, markup):
    base = {"chat_id": chat_id, "link_preview_options": {"is_disabled": True}}

    def attempt(text, mk, parse=True):
        body = dict(base, text=text)
        if parse:
            body["parse_mode"] = "HTML"
        if mk:
            body["reply_markup"] = {"inline_keyboard": mk}
        return _api(token, "sendMessage", body), body

    # ۱) با ایموجی سفارشی (اگر تنظیم و فعال باشد)
    if tg_emoji.enabled():
        (ok, st, tx), _b = attempt(tg_emoji.apply_classic(html_text), tg_emoji.apply_buttons(markup))
        if ok:
            return True
        low = tx.lower()
        if st == 400 and ("emoji" in low or "entit" in low or "premium" in low or "icon" in low):
            tg_emoji.disable(f"({tx[:120]})")      # مثلاً صاحب ربات Premium ندارد → ارسال ساده
        elif st != 400:
            logger.error(f"[TELEGRAM] sendMessage failed: {st} {tx[:200]}")
            return False

    # ۲) ایموجی معمولی
    (ok, st, tx), body = attempt(html_text, markup)
    if ok:
        return True
    if st == 400 and markup and ("button" in tx.lower() or "markup" in tx.lower() or "copy" in tx.lower()):
        logger.warning("[TELEGRAM] buttons rejected — resending without buttons")
        (ok, st, tx), body = attempt(html_text, None)
        if ok:
            return True
    if st == 400 and "parse" in tx.lower():
        logger.warning("[TELEGRAM] HTML parse failed — resending as plain text")
        (ok, st, tx), _b = attempt(plain_fallback(html_text), None, parse=False)
        if ok:
            return True
    logger.error(f"[TELEGRAM] sendMessage failed: {st} {tx[:300]}")
    return False


def deliver(token, chat_id, msg):
    """msg: Card یا رشته‌ی HTML کلاسیک. True اگر ارسال شد."""
    global _rich_dead, _rich_fail_streak
    tg_emoji.load(token)
    card = msg if isinstance(msg, Card) else Card.from_html(msg)
    markup = card.buttons

    # ۱) Rich Message
    if card.rich_ok and rich_enabled() and not _rich_dead:
        body = {"chat_id": chat_id, "rich_message": card.rich()}
        if markup:
            body["reply_markup"] = {"inline_keyboard": tg_emoji.apply_buttons(markup)}
        ok, st, tx = _api(token, "sendRichMessage", body)
        if not ok and st == 400 and "emoji" in tx.lower() and tg_emoji.enabled():
            tg_emoji.disable(f"({tx[:120]})")
            body["rich_message"] = card.rich()
            if markup:
                body["reply_markup"] = {"inline_keyboard": markup}
            ok, st, tx = _api(token, "sendRichMessage", body)
        if ok:
            _rich_fail_streak = 0
            return True
        if st == 400 and markup and ("button" in tx.lower() or "markup" in tx.lower() or "copy" in tx.lower()):
            body.pop("reply_markup", None)           # فقط دکمه‌ها مشکل داشتند
            ok, st, tx = _api(token, "sendRichMessage", body)
            if ok:
                _rich_fail_streak = 0
                return True
        if st in (400, 404):
            _rich_fail_streak += 1
            logger.warning(f"[TELEGRAM] rich message rejected ({st}): {tx[:200]} — falling back to HTML")
            if st == 404 or _rich_fail_streak >= _RICH_MAX_FAILS:
                _rich_dead = True
                logger.error("[TELEGRAM] Rich Messages disabled for this run (repeated failures)")

    # ۲) HTML کلاسیک (با تقسیم امن)
    parts = split_message(card.html(), 3800)
    ok_all = True
    for i, part in enumerate(parts):
        ok_all = _send_classic(token, chat_id, part, markup if i == len(parts) - 1 else None) and ok_all
        if len(parts) > 1:
            time.sleep(0.8)
    return ok_all


# ═══════════════════════════════════════════════════════════
# دکمه‌های سیگنال
# ═══════════════════════════════════════════════════════════
def signal_buttons(symbol, entry, stop, target, pp):
    def fmt(x):
        return f"{float(x):.{pp}f}"
    row1 = [
        {"text": "📍 ورود", "copy_text": {"text": fmt(entry)}, "style": "primary"},
        {"text": "🛑 استاپ", "copy_text": {"text": fmt(stop)}, "style": "danger"},
    ]
    if target:
        row1.append({"text": "🎯 تارگت", "copy_text": {"text": fmt(target)}, "style": "success"})
    row2 = [{"text": "📈 چارت TradingView",
             "url": f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol.upper()}"}]
    return [row1, row2]
