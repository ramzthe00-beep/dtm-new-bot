"""
tg_messages.py — سازنده‌ی همه‌ی پیام‌های تلگرام ربات (DTM / CT / SFP / سفارش / ریسک‌فری / هشدار / گزارش)
همه‌ی خروجی‌ها HTML هستند (parse_mode=HTML) و در tg_style.py ارسال امن دارند.
"""
from datetime import datetime, timedelta

from tg_style import (
    LINE, THIN, esc, b, i, code, pre, meter, spark, money, pct, session_label,
    fa_weekday, now_pair, IRAN_TZ, UTC_TZ,
)

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
def signal_card(strategy, direction, symbol, tf_label, entry, stop, target, pp,
                trade_id=None, type_label=None, rr=None, score=None,
                extra_lines=None, sizing=None, min_rr=2.0, now_utc=None):
    long_ = direction == "LONG"
    dir_emoji = "🟢" if long_ else "🔴"
    dir_fa = "خرید" if long_ else "فروش"
    arrow = "📈" if long_ else "📉"
    s_emoji, s_name = STRATEGIES.get(strategy, ("📡", strategy))
    n_utc, n_ir = now_pair(now_utc)

    stop_d = abs(stop - entry)
    tgt_d = abs(target - entry) if target else 0.0
    stop_pct = stop_d / entry * 100 if entry else 0.0
    tgt_pct = tgt_d / entry * 100 if entry else 0.0
    if rr is None:
        rr = (tgt_d / stop_d) if stop_d > 0 else None

    sgn = 1 if long_ else -1
    r1 = entry + sgn * stop_d
    r2 = entry + sgn * 2 * stop_d
    be_wr = (1 / (1 + rr) * 100) if rr else None

    L = []
    L.append(f"{dir_emoji}{arrow} {b('سیگنال ' + dir_fa)} · {b(direction)}")
    L.append(f"{s_emoji} {b(s_name)}")
    L.append(LINE)
    head = f"🪙 {b(symbol)}   ⏱ {b(tf_label)}"
    if trade_id:
        head += f"   🆔 {code(trade_id)}"
    L.append(head)
    L.append(f"🕐 {n_ir.strftime('%H:%M:%S')} تهران · {fa_weekday(n_ir)}  |  {n_utc.strftime('%H:%M')} UTC")
    L.append(f"🌐 سشن: {session_label(n_utc)}")
    L.append(LINE)
    L.append(f"📍 ورود: {code(_fmt(entry, pp))}")
    L.append(f"🛑 استاپ: {code(_fmt(stop, pp))}  {i(f'(−{stop_pct:.2f}٪ · فاصله {_fmt(stop_d, pp)})')}")
    if target:
        L.append(f"🎯 تارگت: {code(_fmt(target, pp))}  {i(f'(+{tgt_pct:.2f}٪ · فاصله {_fmt(tgt_d, pp)})')}")
    if rr:
        L.append(f"⚖️ ریسک به ریوارد: {b(f'1 : {rr:.2f}')}  {meter(min(rr, 5), 5)}  {_rr_grade(rr)}")
        L.append(f"🪜 پله‌ها: 1R {code(_fmt(r1, pp))} · 2R {code(_fmt(r2, pp))}")
        L.append(f"🧮 وین‌ریت سربه‌سر لازم: {b(f'{be_wr:.1f}٪')}")
    if type_label or score is not None or extra_lines:
        L.append(LINE)
    if type_label:
        L.append(f"🔬 نوع: {b(type_label)}")
    if score is not None:
        L.append(f"🏆 امتیاز: {b(f'{score}/5')}  {'⭐' * int(score)}{'☆' * (5 - int(score))}")
    for ln in (extra_lines or []):
        L.append(ln)

    if sizing:
        notional = sizing["capital"] * sizing["leverage"]
        mode_fa = {"FULL": "سرمایه کامل", "REDUCED_98": "سرمایه کاهشی (موجودی کم)"}.get(sizing["mode"], sizing["mode"])
        L.append(LINE)
        L.append(f"💼 {b('مدیریت سرمایه')}")
        bal_s = format(sizing["balance"], ".4f")
        cap_s = format(sizing["capital"], ".4f")
        L.append(f"💰 موجودی: {code(bal_s)} USDT")
        lev_s = str(sizing["leverage"]) + "x"
        L.append(f"🧰 حالت: {b(mode_fa)} · اهرم {b(lev_s)}")
        L.append(f"💵 مارجین ارسالی: {code(cap_s)} USDT")
        L.append(f"🏗 حجم پوزیشن: {code(f'{notional:,.2f}')} USDT")
        L.append(f"📉 ریسک دلاری: {code('$' + format(sizing['actual_stop_dollar'], '.4f'))}")
        if sizing.get("actual_profit_dollar"):
            L.append(f"📈 سود دلاری: {code('$' + format(sizing['actual_profit_dollar'], '.4f'))}")

    L.append(LINE)
    ok = bool(rr and rr >= min_rr)
    L.append(f"🔒 وضعیت: {'✅ معتبر' if ok else '⚠️ ریسک بالا'}  ·  {s_emoji} {strategy}")
    return "\n".join(L)


def filter_confirm_line(kind_label, detail):
    """خط تأیید فیلتر (مثلاً تأیید SFP برای DTM)."""
    return f"🛰 {b('فیلتر ' + kind_label)}: ✅ {esc(detail)}"


# ═══════════════════════════════════════════════════════════
# 🧾 سفارش (صرافی)
# ═══════════════════════════════════════════════════════════
def order_request_card(symbol, side, leverage, cost, stop_loss, take_profit, body_json):
    try:
        notional = float(cost) * float(leverage)
        notional_s = f"{notional:,.2f}"
    except Exception:
        notional_s = "—"
    icon = "🟢" if str(side).upper() in ("BUY", "LONG") else "🔴"
    return "\n".join([
        f"📤 {b('درخواست سفارش به صرافی')}",
        LINE,
        f"{icon} {b(symbol)} · {b(side)}",
        f"🔧 اهرم: {b(str(leverage) + 'x')}",
        f"💵 مارجین: {code(cost)} USDT",
        f"🏗 حجم پوزیشن: {code(notional_s)} USDT",
        f"🛑 SL: {code(stop_loss)}   🎯 TP: {code(take_profit)}",
        LINE,
        pre(body_json, 900),
    ])


def order_success_card(symbol, side, position_id, response_text):
    icon = "🟢" if str(side).upper() in ("BUY", "LONG") else "🔴"
    return "\n".join([
        f"✅ {b('سفارش با موفقیت ثبت شد')}",
        LINE,
        f"{icon} {b(symbol)} · {b(side)}",
        f"🆔 Position ID: {code(position_id)}",
        LINE,
        f"🧾 {i('پاسخ صرافی')}",
        pre(response_text, 900),
    ])


def order_failed_card(symbol, side, leverage, cost, stop_loss, take_profit,
                      body_json, exchange_error, local_exception):
    return "\n".join([
        f"❌ {b('ثبت سفارش ناموفق بود')}",
        LINE,
        f"🪙 {b(symbol)} · {b(side)} · {b(str(leverage) + 'x')}",
        f"💵 مارجین: {code(cost)}   🛑 SL: {code(stop_loss)}   🎯 TP: {code(take_profit)}",
        LINE,
        f"🔴 {b('خطای صرافی')}",
        pre(exchange_error, 1100),
        f"🧯 {b('استثنای محلی')}: {code(str(local_exception)[:300])}",
        LINE,
        f"📦 {i('بدنه‌ی درخواست')}",
        pre(body_json, 600),
    ])


def risk_free_card(symbol, side, position_id, trigger, mark, entry, size, fee_total, old_sl, new_sl, prec):
    icon = "🟢" if side == "LONG" else "🔴"
    return "\n".join([
        f"🛡️ {b('ریسک‌فری فعال شد')}",
        LINE,
        f"{icon} {b(symbol)} · {b(side)}   🆔 {code(position_id)}",
        LINE,
        f"⚡ نقطه‌ی فعال‌سازی: {code(f'{trigger:.{prec}f}')}",
        f"💹 قیمت مارک: {code(f'{mark:.{prec}f}')}",
        f"📍 ورود واقعی: {code(f'{entry:.{prec}f}')} · حجم {code(size)}",
        f"💸 کارمزد مبنا: {code(f'{fee_total:.4f}')} USDT",
        LINE,
        f"🛑 استاپ قبلی: {code(old_sl)}",
        f"🛡️ استاپ جدید: {code(f'{new_sl:.{prec}f}')}",
        f"{i('اگر استاپ جدید خورده شود، کارمزد برگشت داده می‌شود ✅')}",
    ])


# ═══════════════════════════════════════════════════════════
# ⚠️ هشدارها و خطاها
# ═══════════════════════════════════════════════════════════
_LEVELS = {"warn": "⚠️", "error": "🚨", "info": "ℹ️", "ok": "✅", "stop": "⛔"}


def alert_card(level, title, lines=None, footer=None):
    L = [f"{_LEVELS.get(level, 'ℹ️')} {b(title)}", LINE]
    for ln in (lines or []):
        L.append(ln)
    if footer:
        L.append(LINE)
        L.append(i(footer))
    return "\n".join(L)


def not_executed_card(strategy, direction, symbol, tf_label, reason_title, lines):
    s_emoji, _ = STRATEGIES.get(strategy, ("📡", strategy))
    dir_emoji = "🟢" if direction == "LONG" else "🔴"
    return alert_card(
        "warn", f"سیگنال {strategy} اجرا نشد",
        [f"{s_emoji} {dir_emoji} {b(symbol)} · {b(direction)} · ⏱ {b(tf_label)}",
         f"📝 دلیل: {b(reason_title)}"] + list(lines),
    )


def fatal_error_card(where, exc_type, message, traceback_text):
    tb = str(traceback_text)
    if len(tb) > 1300:
        tb = "…\n" + tb[-1300:]
    return "\n".join([
        f"🚨 {b('خطای بحرانی')} · {code(where)}",
        LINE,
        f"🧩 نوع: {code(exc_type)}",
        f"💬 پیام: {code(str(message)[:400])}",
        LINE,
        f"🔎 {i('Traceback (انتها)')}",
        pre(tb, 1400),
        f"{i('بررسی: خطاهای PyneCore، strategy.py، پارامترها، اطلاعات نماد')}",
    ])


def warning_candles_card(symbol, count):
    return alert_card("warn", "کندل ناکافی",
                      [f"🪙 {b(symbol)}", f"🕯 تعداد کندل: {b(count)} (حداقل ۵۰ لازم است)"])


# ═══════════════════════════════════════════════════════════
# 🚀 استارتاپ
# ═══════════════════════════════════════════════════════════
def startup_ping_card():
    return "\n".join([f"🧪 {b('خودآزمایی راه‌اندازی شروع شد')}", i("در حال بررسی تلگرام، صرافی، داده‌ی بازار، استراتژی‌ها…")])


def _on(flag):
    return "🟢 فعال" if flag else "⚫ غیرفعال"


def startup_report_card(d):
    """
    d: dict با کلیدهای زیر (همه اختیاری با مقدار پیش‌فرض)
      balance, telegram_ok, exchange_ok, position_api_ok, create_order_ok,
      market_ok, market_total, market_list, strategy_import_ok, strategy_ok, test_symbol, test_signal, test_entry,
      symbols, timeframes, sfp_timeframes, leverage_map, base_capital, min_order_cost, target_risk,
      enable_sfp, enable_dtm_sfp_filter, enable_dtm_ct_filter, enable_ct_standalone, ct_combos, ct_filter_ok,
      balance_use_ratio, risk_free_mode, warnings(list), time_str
    """
    g = d.get
    ok = lambda v: "✅" if v else "❌"
    bal = g("balance")
    L = []
    L.append(f"🚀 {b('موتور معاملاتی آنلاین شد')}")
    L.append(i("DTM · CT · SFP — اجرای خودکار با مدیریت ریسک هوشمند"))
    L.append(LINE)
    L.append(f"🩺 {b('سلامت سیستم')}")
    L.append(f"📱 تلگرام {ok(g('telegram_ok'))}   🏦 صرافی {ok(g('exchange_ok'))}   📂 API پوزیشن {ok(g('position_api_ok'))}   🧾 ثبت سفارش {ok(g('create_order_ok'))}")
    bal_txt = (code(format(bal, ".4f")) + " USDT") if bal else "❌ نامشخص"
    L.append(f"💰 موجودی: {bal_txt}")
    mt, mo = g("market_total", 0), g("market_ok", 0)
    L.append(f"📊 داده‌ی بازار: {b(f'{mo}/{mt}')}  {meter(mo, mt or 1)}")
    if g("market_list"):
        L.append("   " + " · ".join(code(x) for x in g("market_list")))
    L.append(LINE)
    L.append(f"🧠 {b('موتورهای استراتژی')}")
    strat_state = ("✅ سالم" if g("strategy_ok") else ("⚠️ قابل‌اجرا، بدون سیگنال فعلی" if g("strategy_import_ok") else "❌ غیرفعال"))
    L.append(f"🧬 {b('DTM')} — {strat_state}")
    L.append(f"   ↳ واگرایی کلاسیک/مخفی (CD± / HD±) + امتیازدهی ۵‌ستاره + فیلترهای ساختاری")
    if g("test_symbol"):
        L.append(f"   ↳ تست {code(g('test_symbol'))}: سیگنال {code(g('test_signal'))}")
    L.append(f"🪤 {b('SFP')} — ترید مستقل: {_on(g('enable_sfp'))}")
    L.append(f"   ↳ ورود کندل بعد از SFP · استاپ پشت شدو · تارگت فیبو ۲.۶۱۸ با حداقل R:R=۲")
    L.append(f"🎯 {b('CT')} — مستقل: {_on(g('enable_ct_standalone'))}")
    if g("ct_combos"):
        L.append(f"   ↳ {g('ct_combos')} " + ("✅" if g("ct_filter_ok", True) else "❌ فیلتر لود نشد"))
    L.append(LINE)
    L.append(f"🛰 {b('فیلترهای سیگنال DTM')}")
    L.append(f"🪤 فیلتر SFP (±۳ کندل از پیوت): {_on(g('enable_dtm_sfp_filter'))}")
    L.append(f"🎯 فیلتر CT: {_on(g('enable_dtm_ct_filter'))}")
    L.append(LINE)
    L.append(f"🛡 {b('مدیریت ریسک و سرمایه')}")
    lev = g("leverage_map") or {}
    if lev:
        L.append("🔧 اهرم: " + " · ".join(f"{code(k.replace('USDT', ''))}={v}x" for k, v in lev.items()))
    L.append(f"💼 سرمایه‌ی پایه: {code(g('base_capital'))} USDT · حداقل سفارش: {code(g('min_order_cost'))} USDT")
    L.append(f"🧮 مدل اندازه‌گیری: BASE / INCREASED / REDUCED (ضریب {g('balance_use_ratio', 0.7)})")
    L.append(f"⚓ لنگر قیمت لحظه‌ای: thetruetrade → Binance → قیمت خام")
    L.append(f"🛡️ ریسک‌فری هوشمند (مبتنی بر کارمزد) روی DTM")
    L.append(LINE)
    L.append(f"📡 {b('پوشش بازار')}")
    L.append(f"🪙 نمادها: {' '.join(code(s.replace('USDT', '')) for s in (g('symbols') or []))}")
    L.append(f"⏱ DTM/CT: {b(' · '.join(str(x) + 'm' for x in (g('timeframes') or [])))}   🪤 SFP: {b(' · '.join(str(x) + 'm' for x in (g('sfp_timeframes') or [])))}")
    L.append(LINE)
    L.append(f"📝 {b('دفترچه و گزارش‌ها')}")
    L.append("📒 دفترچه‌ی سیگنال با PnL فرضی (R، ضریب سود، امید ریاضی، MDD)")
    L.append("🗓 گزارش‌ها: ☀️ ۱۲:۰۰ ظهر · 🌙 ۰۰:۰۰ (کل روز) · 🗓 ماهانه (روز اول ۰۹:۰۰)")
    L.append("🔔 هشدار فوری: قطع صرافی، رد سفارش، موجودی کم، خطای بحرانی")
    for w in (g("warnings") or []):
        L.append(LINE)
        L.append(f"⚠️ {esc(w)}")
    L.append(LINE)
    L.append(f"✅ {b('راه‌اندازی کامل شد')} · 🕐 {code(g('time_str', ''))} تهران")
    return "\n".join(L)


def engine_online_card(dtm_tfs, sfp_tfs, enable_sfp):
    L = [f"🟢 {b('اسکن بازار آغاز شد')}",
         f"🧬 DTM: {b(' · '.join(str(x) + 'm' for x in dtm_tfs))}"]
    if enable_sfp:
        L.append(f"🪤 SFP: {b(' · '.join(str(x) + 'm' for x in sfp_tfs))}")
    L.append(i("از این لحظه سیگنال‌ها لحظه‌ای ارسال می‌شوند 📡"))
    return "\n".join(L)


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
    return f"{ic} {label}: {b(f'{w}W/{l}L')} · {wr:.0f}٪ · {code(money(p))}"


def _ms_to_iran(ms):
    try:
        return datetime.fromtimestamp(ms / 1000, tz=UTC_TZ).astimezone(IRAN_TZ)
    except Exception:
        return None


def build_report_card(rows, title, subtitle=None, icon="📊", base_capital=1.5, max_trade_lines=20):
    st = compute_stats(rows)
    L = [f"{icon} {b(title)}"]
    if subtitle:
        L.append(i(subtitle))
    L.append(LINE)

    if st["total"] == 0:
        L.append("😴 در این بازه سیگنالی ثبت نشده است.")
        return "\n".join(L)

    nclosed = len(st["closed"])
    L.append(f"📈 {b('خلاصه عملکرد')}")
    L.append(f"🎯 سیگنال‌ها: {b(st['total'])}  ·  ✅ برد {b(len(st['wins']))}  ·  ❌ باخت {b(len(st['losses']))}  ·  ⏳ باز {b(len(st['opens']))}")
    L.append(f"🏆 نرخ برد: {b(pct(st['win_rate']))}  {meter(st['win_rate'], 100)}  {i(f'از {nclosed} معامله‌ی بسته')}")
    pnl_icon = "💚" if st["pnl"] > 0 else ("💔" if st["pnl"] < 0 else "🤍")
    L.append(f"{pnl_icon} سود/زیان فرضی: {b(money(st['pnl']))}")
    pf = "∞" if st["profit_factor"] == float("inf") else f"{st['profit_factor']:.2f}"
    exp_s = format(st["expectancy_r"], "+.2f") + "R"
    L.append(f"⚖️ ضریب سود (PF): {b(pf)}  ·  🧮 امید ریاضی: {b(exp_s)}")
    L.append(f"📗 میانگین برد: {code(money(st['avg_win']))}  ·  📕 میانگین باخت: {code(money(st['avg_loss']))}")
    mdd_s = "-" + format(st["mdd"], ".2f") + "$"
    L.append(f"🔻 حداکثر افت سرمایه (MDD): {code(mdd_s)}")
    L.append(f"🔥 برد پیاپی: {b(st['best_win_streak'])}  ·  🧊 باخت پیاپی: {b(st['best_loss_streak'])}")
    L.append(f"🏁 خروج با تارگت: {b(st['tp_count'])}  ·  🛡️ خروج ریسک‌فری: {b(st['rf_count'])}")

    if len(st["curve"]) >= 2:
        L.append(LINE)
        L.append(f"📉 {b('منحنی سرمایه')}")
        L.append(f"{spark(st['curve'])}  {code(money(st['curve'][-1]))}")

    # تفکیک
    by_strat, by_sym, by_dir, by_sess = {}, {}, {}, {}
    for r in rows:
        if r["status"] == "OPEN":
            continue
        by_strat.setdefault(strategy_of(r), []).append(r)
        by_sym.setdefault(r["symbol"], []).append(r)
        by_dir.setdefault(r["direction"], []).append(r)
        t = _ms_to_iran(r["entry_time_ms"])
        if t:
            h_utc = t.astimezone(UTC_TZ).hour
            by_sess.setdefault(session_label(t.astimezone(UTC_TZ).replace(hour=h_utc)), []).append(r)

    if by_strat:
        L.append(LINE)
        L.append(f"🧩 {b('تفکیک استراتژی')}")
        for k in ("DTM", "CT", "SFP"):
            if k in by_strat:
                L.append(_group_line(f"{STRATEGIES[k][0]} {k}", by_strat[k]))
    if by_sym:
        L.append(LINE)
        L.append(f"🪙 {b('تفکیک نماد')}")
        ordered = sorted(by_sym.items(), key=lambda kv: -sum(r.get("pnl_usd") or 0 for r in kv[1]))
        for k, items in ordered[:8]:
            L.append(_group_line(k.replace("USDT", ""), items))
    if by_dir:
        L.append(LINE)
        L.append(f"↕️ {b('جهت معامله')}")
        if "LONG" in by_dir:
            L.append(_group_line("لانگ 📈", by_dir["LONG"]))
        if "SHORT" in by_dir:
            L.append(_group_line("شورت 📉", by_dir["SHORT"]))
    if by_sess:
        L.append(LINE)
        L.append(f"🌐 {b('عملکرد به تفکیک سشن')}")
        for k, items in by_sess.items():
            L.append(_group_line(k, items))

    if st["best"] and st["worst"] and nclosed >= 2:
        L.append(LINE)
        bt, wt = st["best"], st["worst"]
        L.append(f"🥇 بهترین: {b(bt['symbol'])} {bt['direction']} {code(money(bt['pnl_usd']))}")
        L.append(f"🥶 بدترین: {b(wt['symbol'])} {wt['direction']} {code(money(wt['pnl_usd']))}")

    if st["opens"]:
        L.append(LINE)
        L.append(f"⏳ {b('معاملات باز')}")
        for r in st["opens"][:6]:
            t = _ms_to_iran(r["entry_time_ms"])
            ts = t.strftime("%H:%M") if t else "?"
            ic = "🟢" if r["direction"] == "LONG" else "🔴"
            L.append(f"{ic} {ts} · {STRATEGIES[strategy_of(r)][0]} {r['symbol']} {r['direction']}")
        if len(st["opens"]) > 6:
            L.append(i(f"… و {len(st['opens']) - 6} مورد دیگر"))

    if st["closed"]:
        L.append(LINE)
        L.append(f"📋 {b('جزئیات معاملات')}")
        items = sorted(st["closed"], key=lambda r: r["entry_time_ms"])
        shown = items[-max_trade_lines:]
        if len(items) > len(shown):
            L.append(i(f"… {len(items) - len(shown)} معامله‌ی قدیمی‌تر نمایش داده نشد"))
        for r in shown:
            t = _ms_to_iran(r["entry_time_ms"])
            ts = t.strftime("%m-%d %H:%M") if t else "?"
            ic = "🛡️" if r.get("exit_reason") == "RISK_FREE_STOP" else ("✅" if r["status"] == "WIN" else "❌")
            pnl = r.get("pnl_usd")
            rr_ = r.get("pnl_r")
            d_ic = "🟢" if r["direction"] == "LONG" else "🔴"
            tail = f"{money(pnl)}" + (f" ({rr_:+.1f}R)" if rr_ is not None else "")
            L.append(f"{ic} {ts} {STRATEGIES[strategy_of(r)][0]}{d_ic} {r['symbol'].replace('USDT','')} {code(tail)}")

    L.append(LINE)
    L.append(i(f"ℹ️ PnL فرضی بر پایه‌ی سرمایه‌ی پایه {base_capital:.1f}$ و بدون توجه به اجرای واقعی صرافی"))
    return "\n".join(L)


def noon_report_card(rows, now_iran, base_capital):
    sub = f"{fa_weekday(now_iran)} · {now_iran.strftime('%Y-%m-%d')} · از ۰۰:۰۰ تا ۱۲:۰۰ تهران"
    return build_report_card(rows, "گزارش نیمروز", sub, "☀️", base_capital)


def midnight_report_card(rows, day_iran, base_capital):
    sub = f"{fa_weekday(day_iran)} · {day_iran.strftime('%Y-%m-%d')} · کل روز (۰۰:۰۰ تا ۲۴:۰۰ تهران)"
    return build_report_card(rows, "گزارش کامل روز", sub, "🌙", base_capital, max_trade_lines=25)


def period_report_card(rows, title, base_capital, icon="🗓"):
    return build_report_card(rows, title, None, icon, base_capital, max_trade_lines=15)
