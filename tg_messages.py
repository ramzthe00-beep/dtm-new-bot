"""
tg_messages.py — سازنده‌ی همه‌ی پیام‌های تلگرام ربات (DTM / CT / SFP / سفارش / ریسک‌فری / هشدار / گزارش)
همه‌ی خروجی‌ها HTML هستند (parse_mode=HTML) و در tg_style.py ارسال امن دارند.
"""
from datetime import datetime, timedelta

from tg_style import (
    LINE, THIN, esc, b, i, code, pre, meter, spark, money, pct, session_label,
    fa_weekday, now_pair, IRAN_TZ, UTC_TZ,
)
from tg_rich import Card, signal_buttons

STRATEGIES = {
    "DTM": ("🧬", "DTM · واگرایی MACD/RSI"),
    "CT":  ("🎯", "CT · آنی / آتی"),
    "SFP": ("🪤", "SFP · شکار نقدینگی"),
}


# ═══════════════════════════════════════════════════════════
# ابزارهای مشترک
# ═══════════════════════════════════════════════════════════
def _rr_grade(rr):
    if rr is None:
        return "نامشخص"
    if rr >= 4:
        return "عالی 🚀"
    if rr >= 3:
        return "خوب ✅"
    if rr >= 2:
        return "متوسط ⚠️"
    return "ضعیف ❌"


def _fmt(x, pp):
    try:
        return f"{float(x):.{pp}f}"
    except Exception:
        return str(x)


def strategy_of(row):
    """تشخیص استراتژی یک رکورد ledger از order_reason."""
    reason = str(row.get("order_reason") or "")
    if reason.startswith("SFP"):
        return "SFP"
    if reason.startswith("CT"):
        return "CT"
    return "DTM"


def card_header(emoji, title, subtitle=None):
    s = f"{emoji} {b(title)}"
    if subtitle:
        s += f"\n{i(subtitle)}"
    return s


# ═══════════════════════════════════════════════════════════
# 📡 کارت سیگنال (DTM / CT / SFP)
# ═══════════════════════════════════════════════════════════
def _tg_time(dt_utc, ir):
    """زمان به‌صورت date_time (در Rich به وقت محلیِ بیننده؛ در HTML کلاسیک متن تهران)."""
    return f'<tg-time unix="{int(dt_utc.timestamp())}" format="wDT">{ir.strftime("%H:%M")} تهران</tg-time>'


def _fpct(p):
    return f"{p:+.2f}%".replace("-", "−")


def _favorable_pct(direction, entry, price):
    """درصد حرکت نسبت به ورود (مثبت = به نفع معامله)."""
    p = (price - entry) / entry * 100 if entry else 0.0
    return p if direction == "LONG" else -p


def _stage_defs(direction, entry, stop, target, rf_pct=None):
    """مراحل «واقعی» پیشرفت معامله بر اساس منطق استراتژی: ریسک‌فری (اگر دارد) یا 1R، و تارگت نهایی."""
    risk = abs(entry - stop)
    out = []
    if rf_pct is not None and entry:
        trig = entry * (1 + abs(rf_pct)) if direction == "LONG" else entry * (1 - abs(rf_pct))
        out.append(("RF", "🛡 RISK-FREE", trig))
    elif target and risk > 0 and abs(target - entry) > 1.05 * risk:
        out.append(("R1", "⚡ 1R", entry + risk if direction == "LONG" else entry - risk))
    if target:
        out.append(("TP", "🎯 TP", target))
    return out


def signal_card(strategy, direction, symbol, tf_label, entry, stop, target, pp,
                trade_id=None, type_label=None, rr=None, score=None,
                extra_lines=None, sizing=None, min_rr=2.0, now_utc=None, rf_pct=None):
    """کارت سیگنال جدید — سبک کانال‌های سیگنال: عنوان، ورود، TRADE PROGRESS، استاپ، خلاصه."""
    long_ = direction == "LONG"
    dot = "🟢" if long_ else "🔴"
    s_emoji, s_name = STRATEGIES.get(strategy, ("📡", strategy))
    n_utc, n_ir = now_pair(now_utc)

    stop_d = abs(stop - entry)
    tgt_d = abs(target - entry) if target else 0.0
    if rr is None:
        rr = (tgt_d / stop_d) if stop_d > 0 else None

    sub = f"{s_emoji} {strategy} · {tf_label}" + (f" · {trade_id}" if trade_id else "")
    c = Card([("title", "🏹", f"{symbol} | NEW SIGNAL {dot}", sub)])
    c.add(("p", f"{'📈 LONG · خرید' if long_ else '📉 SHORT · فروش'}   📍 ENTRY: {b(_fmt(entry, pp))}"))

    rows = []
    for key, label, price in _stage_defs(direction, entry, stop, target, rf_pct):
        rows.append((label, _fmt(price, pp), _fpct(_favorable_pct(direction, entry, price)), "⌛"))
    rows.append(("🛑 SL", _fmt(stop, pp), _fpct(_favorable_pct(direction, entry, stop)), ""))
    c.add(("h", "📊 TRADE PROGRESS 👇"), ("progress", rows))

    line = []
    if rr:
        line.append(f"⚖️ R:R {b(f'1:{rr:.2f}')}")
    line.append(session_label(n_utc))
    c.add(("p", "  ·  ".join(line)))

    tl = []
    if type_label:
        tl.append(f"🔬 {b(type_label)}")
    if score is not None:
        tl.append(f"⭐ {b(f'{score}/5')}")
    if tl:
        c.add(("p", "  ·  ".join(tl)))
    for ln in (extra_lines or []):
        c.add(("p", ln))

    if sizing:
        profit = sizing.get("actual_profit_dollar")
        tail = f" → سود {b('$' + format(profit, '.2f'))}" if profit else ""
        c.add(("p", f"💼 مارجین {b(format(sizing['capital'], '.2f'))} · اهرم {b(str(sizing['leverage']) + 'x')}"
                    f" · ریسک {b('$' + format(sizing['actual_stop_dollar'], '.2f'))}{tail}"))

    c.add(("footer", f"📌 درصدها بر پایه‌ی قیمت ورود و بدون اهرم/کارمزد · 🕐 {_tg_time(n_utc, n_ir)}"))
    c.buttons = signal_buttons(symbol, entry, stop, target, pp)
    return c


def _dur_text(ms):
    m = max(0, int(ms / 60000))
    return f"{m}m" if m < 60 else f"{m // 60}h{m % 60:02d}m"


_EVENT_TITLES = {"TARGET": "TARGET UPDATE", "STOP_LOSS": "STOP LOSS UPDATE",
                 "RISK_FREE": "RISK-FREE UPDATE", "RISK_FREE_STOP": "BREAKEVEN EXIT"}
_EVENT_DOTS = {"TARGET": "🟢", "STOP_LOSS": "🔴", "RISK_FREE": "🛡️", "RISK_FREE_STOP": "⚪"}


def trade_update_card(event, row):
    """پیام به‌روزرسانی معامله (تارگت / استاپ / ریسک‌فری / خروج سربه‌سر) از روی رکورد ledger."""
    direction = row["direction"]
    entry = row["entry"]
    stop0 = row.get("initial_stop", row.get("stop"))
    target = row.get("target")
    symbol = row["symbol"]
    pp = 2 if entry >= 100 else (4 if entry >= 1 else 5)
    tf_label = f"{row['timeframe']}m"
    strategy = strategy_of(row)
    s_emoji, _ = STRATEGIES.get(strategy, ("📡", strategy))
    dot = _EVENT_DOTS[event]
    closed = event in ("TARGET", "STOP_LOSS", "RISK_FREE_STOP")
    risk = abs(entry - stop0) or 1e-12
    mfe = row.get("mfe_r", 0.0) or 0.0

    kind = row.get("kind") or ""
    reason = str(row.get("order_reason") or "")
    if not kind and reason.startswith("CT-"):
        kind = reason[3:].split("|")[0]
    sub = f"{s_emoji} {strategy}" + (f" · {kind}" if kind else "") + f" · {tf_label} · {'LONG' if direction == 'LONG' else 'SHORT'}"
    c = Card([("title", "🏹", f"{symbol} | {_EVENT_TITLES[event]} {dot}", sub)])

    heads = {
        "TARGET": "🔥 تارگت با موفقیت تاچ شد! 🎯✅",
        "STOP_LOSS": "🛑 استاپ فعال شد؛ معامله با ضرر بسته شد",
        "RISK_FREE": "🛡️ ریسک‌فری فعال شد؛ استاپ به نقطه‌ی ورود منتقل شد",
        "RISK_FREE_STOP": "⚖️ معامله در نقطه‌ی سربه‌سر بسته شد",
    }
    c.add(("p", heads[event]))

    rows = []
    for key, label, price in _stage_defs(direction, entry, stop0, target, row.get("rf_pct")):
        r_stage = abs(price - entry) / risk
        reached = (event == "TARGET") or (key == "RF" and (row.get("risk_free") or event in ("RISK_FREE", "RISK_FREE_STOP"))) \
            or (mfe >= r_stage - 1e-6)
        status = "✅" if reached else ("❌" if closed else "⌛")
        rows.append((label, _fmt(price, pp), _fpct(_favorable_pct(direction, entry, price)), status))
    if event == "RISK_FREE":
        rows.append(("🛑 SL → ENTRY", _fmt(entry, pp), _fpct(0.0), "✅"))
    else:
        rows.append(("🛑 SL", _fmt(stop0, pp), _fpct(_favorable_pct(direction, entry, stop0)),
                     "❌" if event == "STOP_LOSS" else ""))
    c.add(("h", "📊 TRADE PROGRESS 👇"), ("progress", rows))

    if closed:
        pnl, r_ = row.get("pnl_usd"), row.get("pnl_r")
        dur = _dur_text((row.get("exit_time_ms") or 0) - row["entry_time_ms"])
        res = []
        if pnl is not None:
            res.append(f"💵 {b(money(pnl))}" + (f" ({r_:+.1f}R)" if r_ is not None else ""))
        res.append(f"⏱ {dur}")
        c.add(("p", "  ·  ".join(res)))
        mfe_d = min(mfe, r_) if (event == "TARGET" and r_) else mfe
        mae_d = min(row.get("mae_r", 0.0) or 0.0, 1.0)
        c.add(("p", f"📈 MFE {b(f'{mfe_d:+.1f}R')}  ·  📉 MAE {b('−' + format(mae_d, '.1f') + 'R')}"))
        tail = {"TARGET": "💥 معامله با سود بسته شد؛ آماده‌ی فرصت بعدی 📈🔥",
                "STOP_LOSS": "🎯 ضرر کنترل‌شده بخشی از بازی است؛ سیگنال بعدی در راه است",
                "RISK_FREE_STOP": "💸 ریسک‌فری عمل کرد؛ ضرری ثبت نشد 🛡️"}[event]
        c.add(("p", tail))
    else:
        c.add(("p", "✨ از این لحظه معامله بدون ریسک است؛ تارگت در راه است 📈"))

    if strategy == "SFP" and row.get("dashed") is not None:
        c.add(("p", f"🪤 خط چین {code(_fmt(row['dashed'], pp))} · شدو {code(_fmt(row['wick'], pp))}"
                    + (f" · فیبو 2.618 {code(_fmt(row['raw_target'], pp))}" if row.get("raw_target") else "")))
    c.add(("footer", "📌 درصدها بر پایه‌ی قیمت ورود و بدون اهرم/کارمزد"))
    return c


def filter_confirm_line(kind_label, detail):
    """خط تأیید فیلتر (مثلاً تأیید SFP برای DTM) — fragment."""
    return f"🛰 {b('فیلتر ' + kind_label)} ✅ {esc(detail)}"


# ═══════════════════════════════════════════════════════════
# 🧾 سفارش (صرافی) — سبک کانال سیگنال
# ═══════════════════════════════════════════════════════════
def order_request_card(symbol, side, leverage, cost, stop_loss, take_profit, body_json):
    icon = "🟢" if str(side).upper() in ("BUY", "LONG") else "🔴"
    return Card([
        ("title", "🏹", f"{symbol} | ORDER SENT 📤", f"{icon} {side} · {leverage}x"),
        ("lines", [f"💵 MARGIN: {code(cost)} USDT", f"🛑 SL: {code(stop_loss)}", f"🎯 TP: {code(take_profit)}"]),
        ("details", "🧾 REQUEST BODY", [("pre", str(body_json)[:900])], False),
    ])


def order_success_card(symbol, side, position_id, response_text):
    icon = "🟢" if str(side).upper() in ("BUY", "LONG") else "🔴"
    return Card([
        ("title", "🏹", f"{symbol} | ORDER PLACED ✅", f"{icon} {side} · Position {position_id}"),
        ("p", "🔥 سفارش با موفقیت روی صرافی ثبت شد! 🎯"),
        ("details", "🧾 EXCHANGE RESPONSE", [("pre", str(response_text)[:900])], False),
    ])


def order_failed_card(symbol, side, leverage, cost, stop_loss, take_profit,
                      body_json, exchange_error, local_exception):
    return Card([
        ("title", "🏹", f"{symbol} | ORDER FAILED ❌", f"{side} · {leverage}x · مارجین {cost}"),
        ("p", "🚨 ثبت سفارش انجام نشد؛ خطای صرافی 👇"),
        ("pre", str(exchange_error)[:900]),
        ("p", f"🧯 {code(str(local_exception)[:200])}"),
        ("details", "📦 REQUEST BODY", [("pre", str(body_json)[:600])], False),
    ])


def risk_free_card(symbol, side, position_id, trigger, mark, entry, size, fee_total, old_sl, new_sl, prec):
    icon = "🟢" if side == "LONG" else "🔴"
    return Card([
        ("title", "🏹", f"{symbol} | RISK-FREE UPDATE 🛡️", f"{icon} {side} · Position {position_id}"),
        ("p", "🛡️ ریسک‌فری فعال شد؛ استاپ به نقطه‌ی ورود منتقل شد! ✅"),
        ("h", "📊 TRADE PROGRESS 👇"),
        ("progress", [("📍 ENTRY", f"{entry:.{prec}f}", "", ""),
                      ("🛡 TRIGGER", f"{trigger:.{prec}f}", f"mark {mark:.{prec}f}", "✅"),
                      ("🛑 SL (قبلی)", str(old_sl), "", ""),
                      ("🛡 SL (جدید)", f"{new_sl:.{prec}f}", "", "✅")]),
        ("p", f"✨ از این لحظه معامله بدون ریسک است؛ کارمزد {code(f'{fee_total:.4f}')} USDT برگشت داده می‌شود"),
    ])


# ═══════════════════════════════════════════════════════════
# ⚠️ هشدارها و خطاها
# ═══════════════════════════════════════════════════════════
_LEVELS = {"warn": ("WARNING", "⚠️"), "error": ("ERROR", "🚨"), "info": ("INFO", "ℹ️"),
           "ok": ("OK", "✅"), "stop": ("SYSTEM STOP", "⛔")}


def alert_card(level, title, lines=None, footer=None):
    name, emo = _LEVELS.get(level, ("INFO", "ℹ️"))
    c = Card([("title", "🏹", f"{name} | {title} {emo}", None)])
    if lines:
        c.add(("lines", list(lines)))
    if footer:
        c.add(("footer", footer))
    return c


def not_executed_card(strategy, direction, symbol, tf_label, reason_title, lines):
    s_emoji, _ = STRATEGIES.get(strategy, ("📡", strategy))
    dot = "🟢" if direction == "LONG" else "🔴"
    return alert_card(
        "warn", f"{symbol} · سیگنال {strategy} اجرا نشد",
        [f"{s_emoji}{dot} {direction} · {tf_label}", f"📝 دلیل: {b(reason_title)}"] + list(lines),
    )


def fatal_error_card(where, exc_type, message, traceback_text):
    tb = str(traceback_text)
    if len(tb) > 1300:
        tb = "…\n" + tb[-1300:]
    return Card([
        ("title", "🏹", f"SYSTEM | CRITICAL ERROR 🚨", f"{where} · {exc_type}"),
        ("p", f"💬 {code(str(message)[:300])}"),
        ("details", "🔎 TRACEBACK", [("pre", tb[-1400:])], False),
    ])


def warning_candles_card(symbol, count):
    return alert_card("warn", f"{symbol} · کندل ناکافی", [f"🕯 تعداد کندل: {b(count)} (حداقل ۵۰ لازم است)"])


# ═══════════════════════════════════════════════════════════
# 🚀 استارتاپ
# ═══════════════════════════════════════════════════════════
def startup_ping_card():
    return Card([("title", "🏹", "SYSTEM | SELF-TEST STARTED 🧪", "تلگرام · صرافی · داده‌ی بازار · استراتژی‌ها")])


def _on(flag):
    return "🟢 ON" if flag else "⚫ OFF"


def startup_report_card(d):
    g = d.get
    ok = lambda v: "✅" if v else "❌"
    bal = g("balance")
    mt, mo = g("market_total", 0), g("market_ok", 0)
    all_ok = all([g("telegram_ok"), g("exchange_ok"), g("position_api_ok"), g("create_order_ok")]) and mo == mt
    c = Card([("title", "🏹", f"ENGINE | SYSTEM ONLINE {'🟢' if all_ok else '🟡'}", "DTM · CT · SFP")])
    c.add(("p", "🚀 موتور معاملاتی راه‌اندازی شد؛ همه‌ی بخش‌ها زیر بررسی شدند 👇" if all_ok
           else "🚀 موتور راه‌اندازی شد، ولی بعضی بخش‌ها نیاز به توجه دارند 👇"))

    c.add(("h", "🩺 SYSTEM HEALTH 👇"),
          ("lines", [f"📱 Telegram: {ok(g('telegram_ok'))}", f"🏦 Exchange: {ok(g('exchange_ok'))}",
                     f"📂 Positions API: {ok(g('position_api_ok'))}", f"🧾 Order API: {ok(g('create_order_ok'))}",
                     f"💰 Balance: {b(format(bal, '.2f') + ' USDT') if bal else '❌ نامشخص'}",
                     f"📊 Market Data: {b(f'{mo}/{mt}')}  {meter(mo, mt or 1)}"]))

    strat_state = ("✅ سالم" if g("strategy_ok") else ("⚠️ آماده، بدون سیگنال فعلی" if g("strategy_import_ok") else "❌ غیرفعال"))
    ct = _on(g("enable_ct_standalone"))
    if g("ct_combos"):
        ct += f" ({g('ct_combos')})" + ("" if g("ct_filter_ok", True) else " ❌ فیلتر لود نشد")
    c.add(("h", "🧠 STRATEGIES 👇"),
          ("lines", [f"🧬 DTM: {strat_state} — واگرایی CD± / HD± + امتیاز ۵ستاره",
                     f"🪤 SFP: {_on(g('enable_sfp'))} — ورود کندل بعد · استاپ پشت شدو · TP فیبو ۲.۶۱۸ (حداقل R=2)",
                     f"🎯 CT: {ct}"]))

    lev = g("leverage_map") or {}
    lev_txt = " · ".join(f"{k.replace('USDT', '')} {v}x" for k, v in lev.items())
    c.add(("h", "🛰 FILTERS & RISK 👇"),
          ("lines", [f"🪤 DTM ← SFP Filter (±۳ کندل پیوت): {_on(g('enable_dtm_sfp_filter'))}",
                     f"🎯 DTM ← CT Filter: {_on(g('enable_dtm_ct_filter'))}",
                     f"🔧 Leverage: {lev_txt}" if lev_txt else "🔧 Leverage: پیش‌فرض",
                     f"💼 Base Capital: {b(g('base_capital'))} · Min Order: {b(g('min_order_cost'))} USDT",
                     "🧮 Sizing: BASE / INCREASED / REDUCED",
                     "🛡 Smart Risk-Free (fee-aware) · ⚓ Live-price anchor"]))

    syms = " ".join(s.replace("USDT", "") for s in (g("symbols") or []))
    tfs = " · ".join(str(x) + "m" for x in (g("timeframes") or []))
    stfs = " · ".join(str(x) + "m" for x in (g("sfp_timeframes") or []))
    c.add(("h", "📡 COVERAGE 👇"),
          ("lines", [f"🪙 Symbols: {syms}", f"⏱ DTM/CT: {tfs}   🪤 SFP: {stfs}"]))
    c.add(("h", "🗓 REPORTS & ALERTS 👇"),
          ("lines", ["☀️ ۱۲:۰۰ گزارش نیمروز", "🌙 ۰۰:۰۰ گزارش کامل روز", "🗓 گزارش ماهانه (روز اول ۰۹:۰۰)",
                     "🏹 اعلان لحظه‌ای: NEW SIGNAL · TARGET · STOP LOSS · RISK-FREE",
                     "🧷 دکمه‌های کپی ورود/استاپ/تارگت + چارت روی هر سیگنال"]))
    for w in (g("warnings") or []):
        c.add(("quote", f"⚠️ {esc(w)}"))
    c.add(("p", "💥 آماده‌ی شکار فرصت‌ها! 📈🔥"))
    c.add(("footer", f"🕐 {g('time_str', '')} تهران"))
    return c


def engine_online_card(dtm_tfs, sfp_tfs, enable_sfp):
    lines = ["🧬 DTM: " + " · ".join(str(x) + "m" for x in dtm_tfs)]
    if enable_sfp:
        lines.append("🪤 SFP: " + " · ".join(str(x) + "m" for x in sfp_tfs))
    return Card([("title", "🏹", "SCANNER | MARKET SCAN STARTED 🟢", None), ("lines", lines),
                 ("p", "📡 از این لحظه سیگنال‌ها لحظه‌ای ارسال می‌شوند! 🔥")])


# ═══════════════════════════════════════════════════════════
# 📊 آمار و گزارش‌های دوره‌ای
# ═══════════════════════════════════════════════════════════
def compute_stats(rows):
    closed = [r for r in rows if r.get("status") in ("WIN", "LOSS")]
    wins = [r for r in closed if r["status"] == "WIN"]
    losses = [r for r in closed if r["status"] == "LOSS"]
    opens = [r for r in rows if r.get("status") == "OPEN"]
    pnls = [r["pnl_usd"] for r in closed if r.get("pnl_usd") is not None]
    gp = sum(p for p in pnls if p > 0)
    gl = sum(p for p in pnls if p < 0)
    rs = [r["pnl_r"] for r in closed if r.get("pnl_r") is not None]

    seq = sorted(closed, key=lambda r: (r.get("exit_time_ms") or r["entry_time_ms"]))
    cum, curve, peak, mdd = 0.0, [], 0.0, 0.0
    best_w = cur_w = best_l = cur_l = 0
    for r in seq:
        p = r.get("pnl_usd") or 0.0
        cum += p
        curve.append(cum)
        peak = max(peak, cum)
        mdd = max(mdd, peak - cum)
        if r["status"] == "WIN":
            cur_w += 1; cur_l = 0
        else:
            cur_l += 1; cur_w = 0
        best_w, best_l = max(best_w, cur_w), max(best_l, cur_l)

    return {
        "total": len(rows), "wins": wins, "losses": losses, "opens": opens, "closed": closed,
        "win_rate": (len(wins) / len(closed) * 100) if closed else 0.0,
        "pnl": sum(pnls), "gross_profit": gp, "gross_loss": gl,
        "profit_factor": (gp / abs(gl)) if gl < 0 else (float("inf") if gp > 0 else 0.0),
        "avg_win": (gp / len([p for p in pnls if p > 0])) if any(p > 0 for p in pnls) else 0.0,
        "avg_loss": (gl / len([p for p in pnls if p < 0])) if any(p < 0 for p in pnls) else 0.0,
        "expectancy_r": (sum(rs) / len(rs)) if rs else 0.0,
        "avg_r": (sum(rs) / len(rs)) if rs else 0.0,
        "mdd": mdd, "curve": curve, "best_win_streak": best_w, "best_loss_streak": best_l,
        "rf_count": len([r for r in wins if r.get("exit_reason") == "RISK_FREE_STOP"]),
        "tp_count": len([r for r in wins if r.get("exit_reason") == "TARGET"]),
        "best": max((r for r in closed if r.get("pnl_usd") is not None), key=lambda r: r["pnl_usd"], default=None),
        "worst": min((r for r in closed if r.get("pnl_usd") is not None), key=lambda r: r["pnl_usd"], default=None),
    }


def _group_line(label, items):
    w = sum(1 for r in items if r["status"] == "WIN")
    l = sum(1 for r in items if r["status"] == "LOSS")
    p = sum(r.get("pnl_usd") or 0 for r in items if r["status"] in ("WIN", "LOSS"))
    wr = (w / (w + l) * 100) if (w + l) else 0
    ic = "🟢" if p > 0 else ("🔴" if p < 0 else "⚪")
    return f"{ic} {label}: {b(f'{w}W/{l}L')} · {wr:.0f}% · {code(money(p))}"


def _ms_to_iran(ms):
    try:
        return datetime.fromtimestamp(ms / 1000, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception:
        return None


def _trade_line(r):
    t = _ms_to_iran(r["entry_time_ms"])
    ic = "🛡️" if r.get("exit_reason") == "RISK_FREE_STOP" else ("✅" if r["status"] == "WIN" else "❌")
    rr_ = r.get("pnl_r")
    tail = money(r.get("pnl_usd")) + (f" ({rr_:+.1f}R)" if rr_ is not None else "")
    return (f"{ic} {t.strftime('%m-%d %H:%M') if t else '?'} {STRATEGIES[strategy_of(r)][0]}"
            f"{'🟢' if r['direction'] == 'LONG' else '🔴'} {r['symbol'].replace('USDT', '')} · {code(tail)}")


def build_report_card(rows, title, subtitle=None, icon="📊", base_capital=1.5, max_trade_lines=20, carry_rows=None):
    st = compute_stats(rows)
    c = Card([("title", "🏹", f"{title} {icon}", subtitle)])

    if st["total"] == 0 and not carry_rows:
        c.add(("p", "😴 در این بازه سیگنالی ثبت نشده است."))
        return c

    if st["total"]:
        nclosed = len(st["closed"])
        pf = "∞" if st["profit_factor"] == float("inf") else f"{st['profit_factor']:.2f}"
        pnl_dot = "💚" if st["pnl"] > 0 else ("💔" if st["pnl"] < 0 else "🤍")
        c.add(("p", "📈 عملکرد معاملات این بازه 👇" if nclosed else "⏳ هنوز معامله‌ی بسته‌ای وجود ندارد"))
        c.add(("h", "📊 PERFORMANCE 👇"),
              ("lines", [f"🎯 Signals: {b(st['total'])} · ✅ Wins: {b(len(st['wins']))} · ❌ Losses: {b(len(st['losses']))} · ⏳ Open: {b(len(st['opens']))}",
                         f"🏆 Win Rate: {b(pct(st['win_rate']))}  {meter(st['win_rate'], 100)}",
                         f"{pnl_dot} Net PnL: {b(money(st['pnl']))}",
                         f"⚖️ Profit Factor: {b(pf)} · 🧮 Expectancy: {b(format(st['expectancy_r'], '+.2f') + 'R')}",
                         f"📉 Max Drawdown: {b('-' + format(st['mdd'], '.2f') + '$')}",
                         f"🔥 Win Streak: {b(st['best_win_streak'])} · 🧊 Loss Streak: {b(st['best_loss_streak'])}"
                         + (f" · 🛡 Risk-Free: {b(st['rf_count'])}" if st["rf_count"] else "")]))
        if len(st["curve"]) >= 2:
            c.add(("h", "📈 EQUITY CURVE 👇"), ("p", f"{spark(st['curve'])}  {code(money(st['curve'][-1]))}"))

        by_strat, by_sym = {}, {}
        for r in rows:
            if r["status"] == "OPEN":
                continue
            by_strat.setdefault(strategy_of(r), []).append(r)
            by_sym.setdefault(r["symbol"], []).append(r)
        if by_strat:
            c.add(("h", "🧩 BY STRATEGY 👇"),
                  ("lines", [_group_line(f"{STRATEGIES[k][0]} {k}", by_strat[k]) for k in ("DTM", "CT", "SFP") if k in by_strat]))
        if len(by_sym) >= 2:
            ordered = sorted(by_sym.items(), key=lambda kv: -sum(r.get("pnl_usd") or 0 for r in kv[1]))
            c.add(("h", "🪙 BY SYMBOL 👇"), ("lines", [_group_line(k.replace("USDT", ""), v) for k, v in ordered[:5]]))

        if st["opens"]:
            items = []
            for r in st["opens"][:6]:
                t = _ms_to_iran(r["entry_time_ms"])
                items.append(f"{'🟢' if r['direction'] == 'LONG' else '🔴'} {t.strftime('%H:%M') if t else '?'} · "
                             f"{STRATEGIES[strategy_of(r)][0]} {r['symbol']}")
            if len(st["opens"]) > 6:
                items.append(i(f"… و {len(st['opens']) - 6} مورد دیگر"))
            c.add(("details", f"⏳ OPEN TRADES ({len(st['opens'])})", [("lines", items)], False))

        if st["closed"]:
            items = sorted(st["closed"], key=lambda r: r["entry_time_ms"])
            shown = items[-max_trade_lines:]
            inner = []
            if len(items) > len(shown):
                inner.append(("p", i(f"… {len(items) - len(shown)} معامله‌ی قدیمی‌تر نمایش داده نشد")))
            inner.append(("lines", [_trade_line(r) for r in shown]))
            c.add(("details", f"📋 TRADE LOG ({len(items)})", inner, len(items) <= 6))

    if carry_rows:
        cs = compute_stats(carry_rows)
        lines = [_trade_line(r) for r in sorted(carry_rows, key=lambda r: r.get("exit_time_ms") or 0)]
        c.add(("details", f"↩️ CARRY-OVER ({len(carry_rows)} · {money(cs['pnl'])})", [("lines", lines)], True))

    if st["total"] and st["closed"]:
        c.add(("p", ("💥 بازه‌ی سودده! سرمایه‌ی فرضی رشد کرد 📈🔥" if st["pnl"] > 0
                     else "🛡 بازه‌ی منفی؛ مدیریت ریسک حفظ شد و فرصت‌های بعدی در راه است 🎯")))
    c.add(("footer", f"📌 PnL فرضی بر پایه‌ی سرمایه‌ی پایه {base_capital:.1f}$ و بدون کارمزد/لغزش"))
    return c


def noon_report_card(rows, now_iran, base_capital, carry_rows=None):
    sub = f"{fa_weekday(now_iran)} {now_iran.strftime('%Y-%m-%d')} · ۰۰:۰۰ تا ۱۲:۰۰ تهران"
    return build_report_card(rows, "DAILY REPORT | NOON UPDATE", sub, "☀️", base_capital, carry_rows=carry_rows)


def midnight_report_card(rows, day_iran, base_capital):
    sub = f"{fa_weekday(day_iran)} {day_iran.strftime('%Y-%m-%d')} · کل روز"
    return build_report_card(rows, "DAILY REPORT | FULL DAY", sub, "🌙", base_capital, max_trade_lines=25)


def period_report_card(rows, title, base_capital, icon="🗓"):
    return build_report_card(rows, title.replace("گزارش ماه", "MONTHLY REPORT |"), None, icon, base_capital, max_trade_lines=15)
