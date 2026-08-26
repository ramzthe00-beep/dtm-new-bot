"""
trade_ledger.py
================
ماژول کاملاً مستقل برای ثبت «همهٔ» سیگنال‌ها (چه واقعاً روی صرافی اجرا شده باشند
چه نه، چه موجودی کافی بوده باشد چه نه) و محاسبهٔ نتیجهٔ فرضیِ هر معامله بر اساس
برخورد قیمت بعدی با استاپ/تارگت، به‌علاوهٔ گزارش‌های دوره‌ای (صبح/ظهر/شب، پایان روز،
پایان ماه).

این فایل به هیچ‌کدام از strategy.py / strategy_wrapper.py / منطق سیگنال‌دهی دست
نمی‌زند؛ فقط از bot.py صدا زده می‌شود.
"""

import json
import math
import os
import threading
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("TRADE_LEDGER")

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

LEDGER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trade_ledger.jsonl")

# فرمول محاسبهٔ سود/ضرر دلاری فرضی — کاملاً مستقل از موجودی/اجرای واقعی صرافی
BASE_CAPITAL = 2.0

_lock = threading.Lock()


# ---------------------------------------------------------------------------
# ابزارهای کمکی امن (هرگز Exception بالا نمی‌اندازند)
# ---------------------------------------------------------------------------
def _safe_float(x):
    try:
        if x is None:
            return None
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def _now_iran():
    return datetime.now(UTC_TZ).astimezone(IRAN_TZ)


def _ms_to_iran(ms):
    try:
        return datetime.fromtimestamp(ms / 1000.0, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# خواندن / نوشتن ایمن فایل (JSON Lines، append-only برای رکوردهای جدید،
# rewrite کامل برای آپدیت وضعیت معاملات باز)
# ---------------------------------------------------------------------------
def _read_all():
    if not os.path.exists(LEDGER_PATH):
        return []
    rows = []
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue  # یک خط خراب هرگز کل فایل را خراب نکند
    except Exception as e:
        logger.error(f"[LEDGER] read error: {e}")
    return rows


def _write_all(rows):
    tmp_path = LEDGER_PATH + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        os.replace(tmp_path, LEDGER_PATH)  # atomic-ish روی همان فایل‌سیستم
    except Exception as e:
        logger.error(f"[LEDGER] write error: {e}")


# ---------------------------------------------------------------------------
# ثبت سیگنال جدید (صرف‌نظر از موفقیت سفارش واقعی/موجودی کافی)
# ---------------------------------------------------------------------------
def record_signal(symbol, timeframe, direction, entry, stop, target,
                   entry_time_ms, leverage=None, order_placed=None,
                   order_reason=""):
    entry = _safe_float(entry)
    stop = _safe_float(stop)
    target = _safe_float(target)

    if entry is None or stop is None or direction not in ("LONG", "SHORT"):
        logger.warning(
            f"[LEDGER] رد سیگنال ناقص برای ثبت: symbol={symbol} entry={entry} stop={stop} dir={direction}"
        )
        return None

    try:
        entry_time_ms = int(entry_time_ms)
    except Exception:
        entry_time_ms = int(datetime.now(UTC_TZ).timestamp() * 1000)

    row = {
        "id": f"{symbol}_{timeframe}_{entry_time_ms}",
        "symbol": symbol,
        "timeframe": timeframe,
        "direction": direction,
        "entry": entry,
        "stop": stop,
        "target": target,  # می‌تواند None باشد
        "entry_time_ms": entry_time_ms,
        "last_checked_ms": entry_time_ms,
        "status": "OPEN",           # OPEN | WIN | LOSS
        "exit_price": None,
        "exit_time_ms": None,
        "leverage": leverage,
        "order_placed": order_placed,   # وضعیت واقعیِ اجرا روی صرافی (اطلاعاتی، در محاسبهٔ سود اثر ندارد)
        "order_reason": order_reason,
        "pnl_usd": None,
        "pnl_r": None,
    }

    with _lock:
        rows = _read_all()
        # جلوگیری از ثبت تکراری همان سیگنال (همان نماد/تایم‌فریم/زمان ورود)
        if any(r["id"] == row["id"] for r in rows):
            return row["id"]
        rows.append(row)
        _write_all(rows)

    logger.info(f"[LEDGER] سیگنال جدید ثبت شد: {row['id']} {direction} entry={entry} stop={stop} target={target}")
    return row["id"]


# ---------------------------------------------------------------------------
# محاسبهٔ سود/ضرر دلاریِ فرضی طبق فرمول (مستقل از موجودی واقعی)
# ---------------------------------------------------------------------------
def _hypothetical_pnl_usd(direction, entry, stop, exit_price, leverage):
    try:
        if not entry or not stop or entry <= 0:
            return None, None
        stop_pct = abs(entry - stop) / entry
        if stop_pct <= 0:
            return None, None

        if direction == "LONG":
            move_pct = (exit_price - entry) / entry
        else:
            move_pct = (entry - exit_price) / entry

        r_multiple = move_pct / stop_pct  # چند برابر ریسک اولیه

        lev = leverage if (leverage and leverage > 0) else 50
        old_leverage = 1.0 / stop_pct
        if old_leverage > lev:
            capital = (old_leverage / lev) * BASE_CAPITAL
        else:
            capital = BASE_CAPITAL

        pnl_usd = capital * lev * move_pct
        return round(pnl_usd, 4), round(r_multiple, 4)
    except Exception as e:
        logger.error(f"[LEDGER] pnl calc error: {e}")
        return None, None


# ---------------------------------------------------------------------------
# بررسی معاملات باز نسبت به کندل‌های تازه (تشخیص برخورد استاپ/تارگت)
# قانون محافظه‌کارانه: اگر در یک کندل هم استاپ هم تارگت لمس شد، استاپ برنده است.
# ---------------------------------------------------------------------------
def update_open_trades(symbol, timeframe, df):
    """
    df: دیتافریم OHLCV (همان چیزی که هر چرخهٔ bot.py برای این symbol/timeframe می‌گیرد).
    ایندکس df باید timestamp (UTC، pandas datetime) باشد و ستون‌های
    open/high/low/close داشته باشد.
    """
    if df is None or df.empty:
        return

    with _lock:
        rows = _read_all()
        changed = False

        for r in rows:
            if r["symbol"] != symbol or r["timeframe"] != timeframe:
                continue
            if r["status"] != "OPEN":
                continue

            try:
                last_checked = r.get("last_checked_ms", r["entry_time_ms"])
                # فقط کندل‌های *بعد از* آخرین بررسی را نگاه کن
                sub = df[df.index.view("int64") // 10**6 > last_checked]
                if sub.empty:
                    continue

                for ts, row_candle in sub.iterrows():
                    high = _safe_float(row_candle.get("high"))
                    low = _safe_float(row_candle.get("low"))
                    if high is None or low is None:
                        continue

                    candle_ms = int(ts.timestamp() * 1000) if hasattr(ts, "timestamp") else int(ts.value // 10**6)

                    hit_stop = False
                    hit_target = False

                    if r["direction"] == "LONG":
                        if low <= r["stop"]:
                            hit_stop = True
                        if r["target"] is not None and high >= r["target"]:
                            hit_target = True
                    else:  # SHORT
                        if high >= r["stop"]:
                            hit_stop = True
                        if r["target"] is not None and low <= r["target"]:
                            hit_target = True

                    if hit_stop:
                        r["status"] = "LOSS"
                        r["exit_price"] = r["stop"]
                        r["exit_time_ms"] = candle_ms
                    elif hit_target:
                        r["status"] = "WIN"
                        r["exit_price"] = r["target"]
                        r["exit_time_ms"] = candle_ms

                    r["last_checked_ms"] = candle_ms

                    if r["status"] != "OPEN":
                        pnl_usd, pnl_r = _hypothetical_pnl_usd(
                            r["direction"], r["entry"], r["stop"], r["exit_price"], r.get("leverage")
                        )
                        r["pnl_usd"] = pnl_usd
                        r["pnl_r"] = pnl_r
                        changed = True
                        break  # این معامله بسته شد؛ کندل‌های بعدی برایش بی‌معنا هستند

                if r["last_checked_ms"] != last_checked:
                    changed = True

            except Exception as e:
                logger.error(f"[LEDGER] update_open_trades error for {r.get('id')}: {e}")
                continue

        if changed:
            _write_all(rows)


# ---------------------------------------------------------------------------
# ساخت گزارش برای یک بازهٔ زمانی مشخص
# ---------------------------------------------------------------------------
def _in_range(row, start_ms, end_ms):
    return start_ms <= row["entry_time_ms"] < end_ms


def _build_report(rows, title):
    total = len(rows)
    wins = [r for r in rows if r["status"] == "WIN"]
    losses = [r for r in rows if r["status"] == "LOSS"]
    opens = [r for r in rows if r["status"] == "OPEN"]

    closed = wins + losses
    win_rate = (len(wins) / len(closed) * 100) if closed else 0.0

    total_pnl = sum(r["pnl_usd"] for r in closed if r.get("pnl_usd") is not None)

    lines = [
        f"📊 {title}",
        "━━━━━━━━━━━━━━━━━━━━",
        f"تعداد کل سیگنال‌ها: {total}",
        f"برنده (TP): {len(wins)}",
        f"بازنده (SL): {len(losses)}",
        f"هنوز باز: {len(opens)}",
        f"نرخ برد: {win_rate:.1f}٪ (از {len(closed)} معاملهٔ بسته‌شده)",
        f"سود/زیان فرضی کل: {total_pnl:+.2f}$ "
        f"(بر اساس سرمایهٔ پایهٔ {BASE_CAPITAL:.0f}$، بدون توجه به موجودی/اجرای واقعی صرافی)",
    ]

    if closed:
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("جزئیات معاملات بسته‌شده:")
        for r in sorted(closed, key=lambda x: x["entry_time_ms"]):
            t = _ms_to_iran(r["entry_time_ms"])
            t_str = t.strftime("%Y-%m-%d %H:%M") if t else "?"
            emoji = "✅" if r["status"] == "WIN" else "❌"
            pnl = r.get("pnl_usd")
            pnl_str = f"{pnl:+.2f}$" if pnl is not None else "—"
            lines.append(
                f"  {emoji} {t_str} | {r['symbol']} {r['direction']} [{r['timeframe']}] | {pnl_str}"
            )

    return "\n".join(lines)


def report_for_day(date_iran=None):
    """گزارش یک روز مشخص (پیش‌فرض: امروز) به وقت ایران."""
    if date_iran is None:
        date_iran = _now_iran()
    start_local = date_iran.replace(hour=0, minute=0, second=0, microsecond=0)
    end_local = start_local + timedelta(days=1)
    start_ms = int(start_local.astimezone(UTC_TZ).timestamp() * 1000)
    end_ms = int(end_local.astimezone(UTC_TZ).timestamp() * 1000)

    with _lock:
        rows = _read_all()
    day_rows = [r for r in rows if _in_range(r, start_ms, end_ms)]
    title = f"گزارش روز {start_local.strftime('%Y-%m-%d')}"
    return _build_report(day_rows, title)


def report_for_month(year, month):
    """گزارش یک ماه میلادی مشخص (بر اساس تقویم UTC/ساده، برای سادگی و صحت محاسبات)."""
    start_local = datetime(year, month, 1, tzinfo=IRAN_TZ)
    if month == 12:
        end_local = datetime(year + 1, 1, 1, tzinfo=IRAN_TZ)
    else:
        end_local = datetime(year, month + 1, 1, tzinfo=IRAN_TZ)
    start_ms = int(start_local.astimezone(UTC_TZ).timestamp() * 1000)
    end_ms = int(end_local.astimezone(UTC_TZ).timestamp() * 1000)

    with _lock:
        rows = _read_all()
    month_rows = [r for r in rows if _in_range(r, start_ms, end_ms)]
    title = f"گزارش ماه {year}-{month:02d}"
    return _build_report(month_rows, title)


def report_current_and_previous_month():
    """در شروع هر ماه جدید: گزارش ماه تازه‌تمام‌شده + ماه قبل از آن، هر دو با هم."""
    now = _now_iran()
    first_of_this_month = now.replace(day=1)
    last_month_end = first_of_this_month - timedelta(days=1)
    y1, m1 = last_month_end.year, last_month_end.month  # ماه تازه‌تمام‌شده

    prev_end = last_month_end.replace(day=1) - timedelta(days=1)
    y2, m2 = prev_end.year, prev_end.month  # ماه قبل از آن

    r1 = report_for_month(y1, m1)
    r2 = report_for_month(y2, m2)
    return r1 + "\n\n" + ("═" * 22) + "\n\n" + r2


# ---------------------------------------------------------------------------
# زمان‌بند گزارش‌ها — یک Thread جدا که هر ۶۰ ثانیه چک می‌کند و در ساعات
# مشخص (صبح/ظهر/شب، پایان روز، ابتدای ماه) دقیقاً یک‌بار گزارش می‌فرستد.
# ---------------------------------------------------------------------------
_last_sent = {}  # key -> "YYYY-MM-DD HH:MM" آخرین باری که آن گزارش ارسال شد


def _should_send(key, now_str):
    return _last_sent.get(key) != now_str


def scheduler_loop(send_telegram_fn, stop_event,
                    daily_times=("08:00", "13:00", "21:00"),
                    end_of_day_time="23:55"):
    """
    این تابع باید در یک Thread جدا و به‌صورت daemon اجرا شود، مثلاً:
        threading.Thread(target=trade_ledger.scheduler_loop,
                          args=(send_telegram_long, STOP_EVENT), daemon=True).start()
    """
    logger.info("[LEDGER] scheduler_loop started")
    
    # 🔧 محافظت: اگر stop_event یک عدد یا چیز اشتباه است، تبدیلش کن
    if not hasattr(stop_event, 'is_set'):
        import threading
        stop_event = threading.Event()
        logger.warning("[LEDGER] stop_event was not an Event, created new one")
    
    while not stop_event.is_set():
        try:
            now = _now_iran()
            hhmm = now.strftime("%H:%M")
            date_str = now.strftime("%Y-%m-%d")

            # گزارش‌های صبح/ظهر/شب (خلاصهٔ از ابتدای همان روز تا الان)
            if hhmm in daily_times:
                key = f"daily_{hhmm}"
                tag = f"{date_str}_{hhmm}"
                if _should_send(key, tag):
                    try:
                        report = report_for_day(now)
                        send_telegram_fn(report)
                        _last_sent[key] = tag
                    except Exception as e:
                        logger.error(f"[LEDGER] daily report error: {e}")

            # گزارش پایان روز
            if hhmm == end_of_day_time:
                key = "end_of_day"
                tag = date_str
                if _should_send(key, tag):
                    try:
                        report = report_for_day(now)
                        send_telegram_fn("🌙 گزارش پایان روز\n\n" + report)
                        _last_sent[key] = tag
                    except Exception as e:
                        logger.error(f"[LEDGER] end-of-day report error: {e}")

            # گزارش ابتدای ماه (ماه تازه‌تمام‌شده + ماه قبل از آن)
            if now.day == 1 and hhmm == "09:00":
                key = "monthly"
                tag = now.strftime("%Y-%m")
                if _should_send(key, tag):
                    try:
                        report = report_current_and_previous_month()
                        send_telegram_fn("🗓️ گزارش ماهانه\n\n" + report)
                        _last_sent[key] = tag
                    except Exception as e:
                        logger.error(f"[LEDGER] monthly report error: {e}")

        except Exception as e:
            logger.error(f"[LEDGER] scheduler_loop unexpected error: {e}")

        stop_event.wait(30)  # ✅ این متد در threading.Event وجود دارد


if __name__ == "__main__":
    print("trade_ledger.py loaded successfully")
