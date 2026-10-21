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


def signal_card(strategy, direction, symbol, tf_label, entry, stop, target, pp,
                trade_id=None, type_label=None, rr=None, score=None,
                extra_lines=None, sizing=None, min_rr=2.0, now_utc=None):
    """کارت سیگنال — فشرده: عنوان، سه قیمت، یک خط خلاصه، (نوع)، (سرمایه)، دکمه‌ها."""
    long_ = direction == "LONG"
    dir_emoji = "🟢" if long_ else "🔴"
    dir_fa = "خرید" if long_ else "فروش"
    s_emoji, _s_name = STRATEGIES.get(strategy, ("📡", strategy))
    n_utc, n_ir = now_pair(now_utc)

    stop_d = abs(stop - entry)
    tgt_d = abs(target - entry) if target else 0.0
    stop_pct = stop_d / entry * 100 if entry else 0.0
    tgt_pct = tgt_d / entry * 100 if entry else 0.0
    if rr is None:
        rr = (tgt_d / stop_d) if stop_d > 0 else None

    sub = f"{s_emoji} {strategy}" + (f" · {trade_id}" if trade_id else "")
    c = Card([("title", dir_emoji, f"{dir_fa} {symbol} · {tf_label}", sub)])

    prices = [("📍 ورود", _fmt(entry, pp)), ("🛑 استاپ", _fmt(stop, pp))]
    if target:
        prices.append(("🎯 تارگت", _fmt(target, pp)))
    c.add(("kpi", prices))

    parts = [f"−{stop_pct:.2f}٪"]
    if target:
        parts.append(f"+{tgt_pct:.2f}٪")
    line = i(" / ".join(parts))
    if rr:
        line += "  ·  ⚖️ " + b(f"1:{rr:.2f}")
    line += f"  ·  {session_label(n_utc)}"
    c.add(("p", line))

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

    c.add(("footer", f"🕐 {_tg_time(n_utc, n_ir)}"))
    c.buttons = signal_buttons(symbol, entry, stop, target, pp)
    return c


def filter_confirm_line(kind_label, detail):
    """خط تأیید فیلتر (مثلاً تأیید SFP برای DTM) — fragment."""
    return f"🛰 {b('فیلتر ' + kind_label)} ✅ {esc(detail)}"


# ═══════════════════════════════════════════════════════════
# 🧾 سفارش (صرافی)
# ═══════════════════════════════════════════════════════════
def order_request_card(symbol, side, leverage, cost, stop_loss, take_profit, body_json):
    icon = "🟢" if str(side).upper() in ("BUY", "LONG") else "🔴"
    return Card([
        ("title", "📤", f"ارسال سفارش {symbol}", f"{icon} {side} · {leverage}x · مارجین {cost}"),
        ("p", f"🛑 {code(stop_loss)}  ·  🎯 {code(take_profit)}"),
        ("details", "جزئیات درخواست", [("pre", str(body_json)[:900])], False),
    ])


def order_success_card(symbol, side, position_id, response_text):
    icon = "🟢" if str(side).upper() in ("BUY", "LONG") else "🔴"
    return Card([
        ("title", "✅", f"سفارش ثبت شد · {symbol}", f"{icon} {side} · Position {position_id}"),
        ("details", "پاسخ صرافی", [("pre", str(response_text)[:900])], False),
    ])


def order_failed_card(symbol, side, leverage, cost, stop_loss, take_profit,
                      body_json, exchange_error, local_exception):
    return Card([
        ("title", "❌", f"سفارش ناموفق · {symbol}", f"{side} · {leverage}x · مارجین {cost}"),
        ("pre", str(exchange_error)[:900]),
        ("p", f"🧯 {code(str(local_exception)[:200])}"),
        ("details", "بدنه‌ی درخواست", [("pre", str(body_json)[:600])], False),
    ])


def risk_free_card(symbol, side, position_id, trigger, mark, entry, size, fee_total, old_sl, new_sl, prec):
    icon = "🟢" if side == "LONG" else "🔴"
    return Card([
        ("title", "🛡️", f"ریسک‌فری فعال شد · {symbol}", f"{icon} {side} · Position {position_id}"),
        ("kpi", [("ورود", f"{entry:.{prec}f}"), ("استاپ قبلی", str(old_sl)), ("استاپ جدید", f"{new_sl:.{prec}f}")]),
        ("footer", f"قیمت مارک {mark:.{prec}f} · کارمزد برگشتی {fee_total:.4f} USDT"),
    ])


# ═══════════════════════════════════════════════════════════
# ⚠️ هشدارها و خطاها
# ═══════════════════════════════════════════════════════════
_LEVELS = {"warn": "⚠️", "error": "🚨", "info": "ℹ️", "ok": "✅", "stop": "⛔"}


def alert_card(level, title, lines=None, footer=None):
    c = Card([("title", _LEVELS.get(level, "ℹ️"), title, None)])
    for ln in (lines or []):
        c.add(("p", ln))
    if footer:
        c.add(("footer", footer))
    return c


def not_executed_card(strategy, direction, symbol, tf_label, reason_title, lines):
    s_emoji, _ = STRATEGIES.get(strategy, ("📡", strategy))
    dir_emoji = "🟢" if direction == "LONG" else "🔴"
    return alert_card(
        "warn", f"{strategy} اجرا نشد · {reason_title}",
        [f"{s_emoji}{dir_emoji} {b(symbol)} · {direction} · {tf_label}"] + list(lines),
    )


def fatal_error_card(where, exc_type, message, traceback_text):
    tb = str(traceback_text)
    if len(tb) > 1300:
        tb = "…\n" + tb[-1300:]
    return Card([
        ("title", "🚨", f"خطای بحرانی · {where}", f"{exc_type}: {str(message)[:200]}"),
        ("details", "Traceback", [("pre", tb[-1400:])], False),
    ])


def warning_candles_card(symbol, count):
    return alert_card("warn", f"کندل ناکافی · {symbol}", [f"تعداد کندل: {b(count)} (حداقل ۵۰)"])


# ═══════════════════════════════════════════════════════════
# 🚀 استارتاپ
# ═══════════════════════════════════════════════════════════
def startup_ping_card():
    return Card([("title", "🧪", "خودآزمایی راه‌اندازی…", None)])


def _on(flag):
    return "فعال 🟢" if flag else "غیرفعال ⚫"


def startup_report_card(d):
    g = d.get
    ok = lambda v: "✅" if v else "❌"
    bal = g("balance")
    mt, mo = g("market_total", 0), g("market_ok", 0)
    c = Card([("title", "🚀", "موتور معاملاتی آنلاین شد", "DTM · CT · SFP")])
    c.add(("kpi", [("تلگرام", ok(g("telegram_ok"))), ("صرافی", ok(g("exchange_ok"))),
                   ("API پوزیشن", ok(g("position_api_ok"))), ("ثبت سفارش", ok(g("create_order_ok")))]))
    c.add(("p", f"💰 {b(format(bal, '.2f') + ' USDT') if bal else '❌ نامشخص'}  ·  📊 داده‌ی بازار {b(f'{mo}/{mt}')}"))

    strat_state = ("سالم" if g("strategy_ok") else ("بدون سیگنال فعلی" if g("strategy_import_ok") else "❌ غیرفعال"))
    ct = _on(g("enable_ct_standalone"))
    if g("ct_combos"):
        ct += f" ({g('ct_combos')})" + ("" if g("ct_filter_ok", True) else " ❌ فیلتر لود نشد")
    c.add(("h", "🧠 استراتژی‌ها"),
          ("list", [f"🧬 {b('DTM')} — واگرایی CD± / HD± با امتیاز ۵ستاره · {strat_state}",
                    f"🪤 {b('SFP')} — {_on(g('enable_sfp'))} · ورود کندل بعد، استاپ پشت شدو، تارگت فیبو ۲.۶۱۸ (حداقل R=2)",
                    f"🎯 {b('CT')} — {ct}"]))

    lev = g("leverage_map") or {}
    lev_txt = " · ".join(f"{k.replace('USDT', '')}={v}x" for k, v in lev.items())
    c.add(("h", "🛡 فیلتر و ریسک"),
          ("list", [f"فیلتر SFP روی DTM {_on(g('enable_dtm_sfp_filter'))} · فیلتر CT {_on(g('enable_dtm_ct_filter'))}",
                    f"اهرم: {lev_txt}" if lev_txt else "اهرم: پیش‌فرض",
                    f"سرمایه‌ی پایه {g('base_capital')} · حداقل سفارش {g('min_order_cost')} USDT · مدل BASE/INCREASED/REDUCED",
                    "ریسک‌فری هوشمند مبتنی بر کارمزد · لنگر قیمت لحظه‌ای"]))

    syms = " ".join(s.replace("USDT", "") for s in (g("symbols") or []))
    tfs = " · ".join(str(x) + "m" for x in (g("timeframes") or []))
    stfs = " · ".join(str(x) + "m" for x in (g("sfp_timeframes") or []))
    c.add(("h", "📡 پوشش و گزارش"),
          ("list", [f"{syms} — DTM/CT: {tfs} · SFP: {stfs}",
                    "☀️ ۱۲:۰۰ گزارش نیمروز · 🌙 ۰۰:۰۰ گزارش کامل روز · 🗓 ماهانه",
                    "دکمه‌های کپی ورود/استاپ/تارگت و لینک چارت روی هر سیگنال"]))
    for w in (g("warnings") or []):
        c.add(("quote", f"⚠️ {esc(w)}"))
    c.add(("footer", f"{g('time_str', '')} تهران"))
    return c


def engine_online_card(dtm_tfs, sfp_tfs, enable_sfp):
    txt = "🧬 DTM " + " · ".join(str(x) + "m" for x in dtm_tfs)
    if enable_sfp:
        txt += "   🪤 SFP " + " · ".join(str(x) + "m" for x in sfp_tfs)
    return Card([("title", "🟢", "اسکن بازار آغاز شد", txt)])


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


def _group_row(label, items):
    w = sum(1 for r in items if r["status"] == "WIN")
    l = sum(1 for r in items if r["status"] == "LOSS")
    p = sum(r.get("pnl_usd") or 0 for r in items if r["status"] in ("WIN", "LOSS"))
    return [label, f"{w}W/{l}L", code(money(p))]


def _ms_to_iran(ms):
    try:
        return datetime.fromtimestamp(ms / 1000, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception:
        return None


def _trade_row(r):
    t = _ms_to_iran(r["entry_time_ms"])
    ic = "🛡️" if r.get("exit_reason") == "RISK_FREE_STOP" else ("✅" if r["status"] == "WIN" else "❌")
    rr_ = r.get("pnl_r")
    tail = money(r.get("pnl_usd")) + (f" ({rr_:+.1f}R)" if rr_ is not None else "")
    return [t.strftime("%m-%d %H:%M") if t else "?",
            STRATEGIES[strategy_of(r)][0] + ("🟢" if r["direction"] == "LONG" else "🔴") + " " + r["symbol"].replace("USDT", ""),
            f"{ic} {code(tail)}"]


def build_report_card(rows, title, subtitle=None, icon="📊", base_capital=1.5, max_trade_lines=20, carry_rows=None):
    st = compute_stats(rows)
    c = Card([("title", icon, title, subtitle)])

    if st["total"] == 0 and not carry_rows:
        c.add(("p", "😴 در این بازه سیگنالی ثبت نشده است."))
        return c

    if st["total"]:
        nclosed = len(st["closed"])
        pf = "∞" if st["profit_factor"] == float("inf") else f"{st['profit_factor']:.2f}"
        c.add(("kpi", [("سیگنال", str(st["total"])), ("✅ برد", str(len(st["wins"]))),
                       ("❌ باخت", str(len(st["losses"]))), ("⏳ باز", str(len(st["opens"])))]),
              ("kpi", [("نرخ برد", pct(st["win_rate"])), ("سود/زیان", money(st["pnl"])),
                       ("PF", pf), ("امید ریاضی", f"{st['expectancy_r']:+.2f}R")]))
        extra = [f"📉 MDD {b('-' + format(st['mdd'], '.2f') + '$')}",
                 f"🔥 برد پیاپی {b(st['best_win_streak'])}", f"🧊 باخت پیاپی {b(st['best_loss_streak'])}"]
        if st["rf_count"]:
            extra.append(f"🛡️ ریسک‌فری {b(st['rf_count'])}")
        c.add(("p", "  ·  ".join(extra)))
        if len(st["curve"]) >= 2:
            c.add(("p", f"{spark(st['curve'])}  {code(money(st['curve'][-1]))}"))

        by_strat, by_sym = {}, {}
        for r in rows:
            if r["status"] == "OPEN":
                continue
            by_strat.setdefault(strategy_of(r), []).append(r)
            by_sym.setdefault(r["symbol"], []).append(r)
        al = ["right", "center", "left"]
        if len(by_strat) >= 1:
            c.add(("table", ["استراتژی", "برد/باخت", "سود/زیان"],
                   [_group_row(f"{STRATEGIES[k][0]} {k}", by_strat[k]) for k in ("DTM", "CT", "SFP") if k in by_strat],
                   al, None))
        if len(by_sym) >= 2:
            ordered = sorted(by_sym.items(), key=lambda kv: -sum(r.get("pnl_usd") or 0 for r in kv[1]))
            c.add(("table", ["نماد", "برد/باخت", "سود/زیان"],
                   [_group_row(k.replace("USDT", ""), v) for k, v in ordered[:5]], al, None))

        if st["opens"]:
            items = []
            for r in st["opens"][:5]:
                t = _ms_to_iran(r["entry_time_ms"])
                items.append(f"{'🟢' if r['direction'] == 'LONG' else '🔴'} {t.strftime('%H:%M') if t else '?'} · "
                             f"{STRATEGIES[strategy_of(r)][0]} {r['symbol']}")
            if len(st["opens"]) > 5:
                items.append(i(f"… و {len(st['opens']) - 5} مورد دیگر"))
            c.add(("details", f"⏳ معاملات باز ({len(st['opens'])})", [("list", items)], False))

        if st["closed"]:
            items = sorted(st["closed"], key=lambda r: r["entry_time_ms"])
            shown = items[-max_trade_lines:]
            inner = []
            if len(items) > len(shown):
                inner.append(("p", i(f"… {len(items) - len(shown)} معامله‌ی قدیمی‌تر نمایش داده نشد")))
            inner.append(("table", ["زمان", "معامله", "نتیجه"], [_trade_row(r) for r in shown],
                          ["right", "center", "left"], None))
            c.add(("details", f"📋 جزئیات معاملات ({len(items)})", inner, len(items) <= 6))

    if carry_rows:
        cs = compute_stats(carry_rows)
        crow = [_trade_row(r) for r in sorted(carry_rows, key=lambda r: r.get("exit_time_ms") or 0)]
        c.add(("details", f"↩️ بسته‌شده از معاملات دیروز ({len(carry_rows)} · {money(cs['pnl'])})",
               [("table", ["ورود", "معامله", "نتیجه"], crow, ["right", "center", "left"], None)], True))

    c.add(("footer", f"PnL فرضی بر پایه‌ی سرمایه‌ی پایه {base_capital:.1f}$"))
    return c


def noon_report_card(rows, now_iran, base_capital, carry_rows=None):
    sub = f"{fa_weekday(now_iran)} {now_iran.strftime('%Y-%m-%d')} · ۰۰:۰۰ تا ۱۲:۰۰ تهران"
    return build_report_card(rows, "گزارش نیمروز", sub, "☀️", base_capital, carry_rows=carry_rows)


def midnight_report_card(rows, day_iran, base_capital):
    sub = f"{fa_weekday(day_iran)} {day_iran.strftime('%Y-%m-%d')} · کل روز"
    return build_report_card(rows, "گزارش کامل روز", sub, "🌙", base_capital, max_trade_lines=25)


def period_report_card(rows, title, base_capital, icon="🗓"):
    return build_report_card(rows, title, None, icon, base_capital, max_trade_lines=15)
