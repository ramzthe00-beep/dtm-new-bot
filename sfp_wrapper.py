"""
sfp_wrapper.py
==============
Wrapper استراتژی SFP (همان نقشِ strategy_wrapper.py برای DTM)

- منطق تشخیص SFP کاملاً از sfp_strategy.py می‌آید (بدون هیچ تغییری؛ تطابق ۱۰۰٪ با Pine).
- کندل ناقص (در حال تشکیل) دقیقاً با همان قاعده‌ی DTM حذف می‌شود.
- قاعده‌ی ورود: وقتی کندل SFP «بسته» شد (HIT_H / HIT_L)، در کندل بعدی سیگنال داده می‌شود.
    ورود   : close کندل SFP (≈ open کندل بعدی؛ در اجرا مثل DTM روی قیمت لنگر درصدی اعمال می‌شود)
    استاپ  : بالای شدوی کندل SFP (شورت) / پایین شدوی کندل SFP (لانگ) + بافر (همان بافر DTM)
    تارگت  : فیبوناچی از «خط چین» (همان خط oppos که منطق SFP قبل از کندل SFP می‌کشد؛ پایین‌ترین low / بالاترین high
             بین سوئینگ و کندل SFP) تا «انتهای شدوی کندل SFP»؛ سطح 0 = انتهای شدو، سطح 1 = خط چین، تارگت = سطح 2.618
             شورت: target = H - 2.618 * (H - D)      لانگ: target = L + 2.618 * (D - L)
             (H/L = انتهای شدو، D = خط چین)
             اگر R:R < 2 شد، تارگت دورتر برده می‌شود تا R:R = 2 شود.
- خروجی calculate_sfp_signals هم‌شکل calculate_signals در DTM است (۷ مقدار).
"""
import logging
import math
import time as _time
from datetime import datetime, timezone, timedelta

from sfp_strategy import run_sfp

try:  # همان جدول tick که DTM استفاده می‌کند
    from strategy_wrapper import SYMBOL_TICK_INFO
except Exception:  # pragma: no cover  (مثلاً تست بدون PyneCore)
    SYMBOL_TICK_INFO = {}

logger = logging.getLogger("SFP_WRAPPER")

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

# ═══════════════════════════════════════════════════════════
# پارامترها
# ═══════════════════════════════════════════════════════════
SFP_LENGTH = 5            # طول پیوت (مثل پارامتر length در Pine)
SFP_FIB_EXT = 2.618       # سطح فیبوی تارگت
SFP_MIN_RR = 2.0          # حداقل ریسک به ریوارد
COMPLETION_SAFETY_BUFFER_SEC = 5   # دقیقاً مثل DTM


def _buffer_ticks(symbol):
    """بافر استاپ بر حسب tick — عین جدول DTM در strategy_wrapper.calculate_signals."""
    s = symbol.upper()
    if s in ("BNBUSDT", "ETHUSDT"):
        return 1
    if s in ("LTCUSDT", "DOGEUSDT"):
        return 1
    if s == "PUMPUSDT":
        return 1
    return 1


def _tick_info(symbol):
    symbol = symbol.upper()
    return SYMBOL_TICK_INFO.get(
        symbol, {"mintick": 0.01, "pricescale": 100, "basecurrency": symbol.replace("USDT", "")}
    )


def price_prec(mintick):
    s_ = f"{float(mintick):.10f}".rstrip("0")
    return len(s_.split(".")[1]) if "." in s_ else 0


# ═══════════════════════════════════════════════════════════
# حذف کندل ناقص (همان قاعده‌ی DTM)
# ═══════════════════════════════════════════════════════════
def closed_candles_only(df, timeframe, now_ts=None, safety_buffer_sec=COMPLETION_SAFETY_BUFFER_SEC):
    if df is None or len(df) < 2:
        return df
    try:
        tf_sec = int(timeframe) * 60
    except (TypeError, ValueError):
        return df
    now = _time.time() if now_ts is None else now_ts
    last_open = df.index[-1].timestamp()
    if (now - last_open) < tf_sec + safety_buffer_sec:
        return df.iloc[:-1]
    return df


# ═══════════════════════════════════════════════════════════
# استاپ / تارگت
# ═══════════════════════════════════════════════════════════
def compute_sfp_stop_target(direction, entry, dashed, wick, mintick, buffer_ticks):
    """
    direction: 'SHORT' (SFP نزولی، swing = قله) یا 'LONG' (SFP صعودی، swing = دره)
    entry    : close کندل SFP
    dashed   : قیمت خط چین (oppos)
    wick     : انتهای شدوی کندل SFP (high برای SHORT، low برای LONG)
    خروجی    : dict یا None
    """
    buf = buffer_ticks * mintick
    if direction == "SHORT":
        stop = wick + buf
        risk = stop - entry
        if risk <= 0:
            return None
        raw_target = wick - SFP_FIB_EXT * (wick - dashed)
        rr_raw = (entry - raw_target) / risk
        if rr_raw >= SFP_MIN_RR:
            target, rr, adjusted = raw_target, rr_raw, False
        else:
            target, rr, adjusted = entry - SFP_MIN_RR * risk, SFP_MIN_RR, True
    else:
        stop = wick - buf
        risk = entry - stop
        if risk <= 0:
            return None
        raw_target = wick + SFP_FIB_EXT * (dashed - wick)
        rr_raw = (raw_target - entry) / risk
        if rr_raw >= SFP_MIN_RR:
            target, rr, adjusted = raw_target, rr_raw, False
        else:
            target, rr, adjusted = entry + SFP_MIN_RR * risk, SFP_MIN_RR, True

    if target <= 0 or stop <= 0:
        return None
    return {"stop": stop, "target": target, "rr": rr, "rr_raw": rr_raw,
            "raw_target": raw_target, "target_adjusted": adjusted}


# ═══════════════════════════════════════════════════════════
# همه‌ی سیگنال‌های SFP روی یک DataFrame
# ═══════════════════════════════════════════════════════════
def run_sfp_signals(df, symbol, timeframe, length=SFP_LENGTH):
    """
    sfp_strategy.run_sfp را روی کندل‌های «بسته‌شده» اجرا می‌کند و برای هر HIT یک سیگنال می‌سازد.
    time_ms = زمان باز شدن کندل SFP (همان قراردادِ signal_bar_ts_ms در DTM).
    """
    if df is None or df.empty:
        return []
    df = closed_candles_only(df, timeframe)
    if df is None or len(df) < 50:
        return []

    symbol = symbol.upper()
    mintick = float(_tick_info(symbol)["mintick"])
    bt = _buffer_ticks(symbol)

    o = [float(x) for x in df["open"]]
    h = [float(x) for x in df["high"]]
    l = [float(x) for x in df["low"]]
    c = [float(x) for x in df["close"]]
    ms = [int(i.timestamp() * 1000) for i in df.index]

    signals = []
    for e in run_sfp(o, h, l, c, length=length):
        if e["kind"] not in ("HIT_H", "HIT_L"):
            continue
        n = e["bar"]
        bearish = e["kind"] == "HIT_H"
        direction = "SHORT" if bearish else "LONG"
        swing = float(e["sw"])
        dashed = float(e["oppos"])   # خط چین
        wick = h[n] if bearish else l[n]
        entry = c[n]

        calc = compute_sfp_stop_target(direction, entry, dashed, wick, mintick, bt)
        if calc is None:
            logger.warning(f"[SFP] {symbol} bar={n} {direction}: invalid stop/target — skipped")
            continue

        t_utc = datetime.fromtimestamp(ms[n] / 1000, tz=UTC_TZ)
        signals.append({
            "time_ms": ms[n], "time_utc": t_utc, "time_iran": t_utc.astimezone(IRAN_TZ),
            "kind": "SFP-S" if bearish else "SFP-L",
            "direction": direction,
            "entry": entry, "stop": calc["stop"], "target": calc["target"],
            "rr": calc["rr"], "rr_raw": calc["rr_raw"], "raw_target": calc["raw_target"],
            "target_adjusted": calc["target_adjusted"],
            "swing": swing, "dashed": dashed, "wick": wick, "swing_bar": e["bx"],
            "bar_index": n, "bars_total": len(df),
        })
    return signals


# ═══════════════════════════════════════════════════════════
# پیام تلگرام (قالب DTM + جزئیات SFP + بخش سایزینگ)
# ═══════════════════════════════════════════════════════════
def build_sfp_message(sig, symbol, timeframe, trade_id, mintick, sizing=None):
    emoji = "🟢" if sig["direction"] == "LONG" else "🔴"
    direction_fa = "خرید" if sig["direction"] == "LONG" else "فروش"
    entry, stop, target, rr = sig["entry"], sig["stop"], sig["target"], sig["rr"]
    pp = price_prec(mintick)

    stop_distance = abs(stop - entry)
    target_distance = abs(target - entry)
    stop_pct = stop_distance / entry * 100 if entry else 0
    target_pct = target_distance / entry * 100 if entry else 0

    if rr >= 4:
        rr_status = "عالی 🚀"
    elif rr >= 3:
        rr_status = "خوب ✅"
    elif rr >= 2:
        rr_status = "متوسط ⚠️"
    else:
        rr_status = "ضعیف ❌"

    type_fa = ("SFP-L (شکست‌ساختگی کف - صعودی)" if sig["direction"] == "LONG"
               else "SFP-S (شکست‌ساختگی سقف - نزولی)")
    now_utc = datetime.now(UTC_TZ)
    now_ir = now_utc.astimezone(IRAN_TZ)
    sig_ir = sig["time_iran"].strftime("%H:%M")

    tgt_note = (f"تعدیل‌شده به R=2 (فیبو 2.618 = {sig['raw_target']:.{pp}f}، R={sig['rr_raw']:.2f})"
                if sig["target_adjusted"] else f"فیبو 2.618 (R={sig['rr_raw']:.2f})")

    msg = f"""
{emoji} سیگنال SFP {direction_fa} ({sig['direction']}) - {symbol} - {timeframe} دقیقه
─────────────────────────────────────────
🆔 شماره: {trade_id}
🕐 زمان: {now_utc.strftime('%H:%M:%S')} UTC ({now_ir.strftime('%H:%M:%S')} تهران)
🕯 کندل SFP: {sig_ir} تهران (بسته شد، ورود در کندل بعد)
─────────────────────────────────────────
📊 ورود: {entry:.{pp}f}
🛑 حد ضرر: {stop:.{pp}f} ({stop_distance:.{pp}f}- | {stop_pct:.2f}%)
🎯 هدف: {target:.{pp}f} ({target_distance:.{pp}f}+ | {target_pct:.2f}%)
⭐ نسبت ریسک: 1 : {rr:.2f} ({rr_status})
📌 نوع: {type_fa}
📐 خط چین: {sig['dashed']:.{pp}f} | انتهای شدو: {sig['wick']:.{pp}f}
🧮 تارگت: {tgt_note}
"""
    if sizing:
        profit_str = f"{sizing['actual_profit_dollar']:.4f}" if sizing.get("actual_profit_dollar") else "N/A"
        msg += f"""─────────────────────────────────────────
💰 موجودی: {sizing['balance']:.4f} USDT
📊 حالت اهرم: {sizing['mode']} | اهرم: {sizing['leverage']}x
💵 سرمایه ارسالی: {sizing['capital']:.4f} USDT
📉 استاپ دلاری: ${sizing['actual_stop_dollar']:.4f}
📈 سود دلاری: ${profit_str}
"""
    msg += f"""─────────────────────────────────────────
🔒 وضعیت: {'✅ معتبر' if rr >= SFP_MIN_RR else '⚠️ ریسک بالا'}
"""
    return msg


# ═══════════════════════════════════════════════════════════
# هم‌شکل calculate_signals در DTM (۷ مقدار) — فقط آخرین کندل بسته‌شده
# ═══════════════════════════════════════════════════════════
def calculate_sfp_signals(df, symbol="LTCUSDT", timeframe="1", silent=True):
    """
    خروجی: (signal, entry, stop, target, signal_bar_ts_ms, risk_free_pct, msg)
    signal فقط وقتی LONG/SHORT است که «آخرین کندل بسته‌شده» یک SFP باشد.
    risk_free_pct همیشه None است (ریسک‌فری برای SFP تعریف نشده).
    """
    try:
        closed = closed_candles_only(df, timeframe)
        if closed is None or len(closed) < 50:
            return None, None, None, None, None, None, None
        last_ms = int(closed.index[-1].timestamp() * 1000)
        sigs = [s for s in run_sfp_signals(df, symbol, timeframe) if s["time_ms"] == last_ms]
        if not sigs:
            return None, None, None, None, last_ms, None, None
        if len(sigs) > 1:
            logger.warning(f"[SFP] {symbol} {timeframe}m: both SFP directions on the same bar — skipped")
            return None, None, None, None, last_ms, None, None
        s = sigs[0]
        msg = build_sfp_message(s, symbol.upper(), timeframe, "#SFP", _tick_info(symbol)["mintick"])
        if not silent:
            logger.info(msg)
        return s["direction"], s["entry"], s["stop"], s["target"], s["time_ms"], None, msg
    except Exception as e:
        logger.exception(f"[SFP] calculate_sfp_signals failed: {e}")
        return None, None, None, None, None, None, None
