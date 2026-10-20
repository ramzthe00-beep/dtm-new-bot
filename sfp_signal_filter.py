"""
sfp_signal_filter.py
====================
فیلتر SFP برای DTM (هم‌خانواده‌ی ct_signal_filter.py)

قاعده:
  سیگنال DTM (CD-/CD+/HD-/HD+) فقط وقتی صادر می‌شود که یک SFP «هم‌جهت» در بازه‌ی
  [۳ کندل قبل از پیوت … ۳ کندل بعد از پیوت] رخ داده باشد.
    - پیوت = کندل قله/دره‌ی واگرایی (همان کندلی که برچسب CD-/HD- روی آن می‌نشیند).
    - پیوت DTM با rightBars=3 تأیید می‌شود؛ پس کندل سیگنال = پیوت + ۳ و
      «۳ کندل بعد از پیوت» دقیقاً تا همان کندل سیگنال است.
    - هم‌جهت: DTM نزولی (SHORT) ↔ SFP نزولی (HIT_H)، DTM صعودی (LONG) ↔ SFP صعودی (HIT_L).
    - SFP از همان کندل‌های هم‌تایم‌فریمِ DTM و با همان sfp_strategy.run_sfp (طول پیوت ۵) محاسبه می‌شود.
    - SFP روی کندل خودِ پیوت هم قبول است (فاصله ۰).
  اگر SFP پیدا نشد → reject (مثل رفتار CT).
"""
import logging

from sfp_wrapper import run_sfp_signals, closed_candles_only

logger = logging.getLogger("SFP_FILTER")

DTM_RIGHT_BARS = 3        # rightBars استراتژی DTM (strategy.py)
SFP_BARS_BEFORE = 3       # کندل قبل از پیوت
SFP_BARS_AFTER = 3        # کندل بعد از پیوت


def check_sfp_filter(df, symbol, dtm_direction, dtm_timeframe, signal_bar_ts_ms,
                     right_bars=DTM_RIGHT_BARS, bars_before=SFP_BARS_BEFORE,
                     bars_after=SFP_BARS_AFTER):
    """
    خروجی: dict با کلیدهای
      allowed, reason, sfp_signal, offset (منفی=قبل از پیوت، ۰=روی پیوت، مثبت=بعد از پیوت),
      pivot_time_ms
    """
    result = {"allowed": False, "reason": "unknown", "sfp_signal": None,
              "offset": None, "pivot_time_ms": None}
    try:
        closed = closed_candles_only(df, dtm_timeframe)
        if closed is None or len(closed) < 50:
            result["reason"] = "not_enough_candles"
            return result

        ts = [int(i.timestamp() * 1000) for i in closed.index]
        if signal_bar_ts_ms not in ts:
            result["reason"] = "signal_bar_not_found"
            return result

        sig_idx = ts.index(signal_bar_ts_ms)
        pivot_idx = sig_idx - right_bars
        if pivot_idx < 0:
            result["reason"] = "pivot_out_of_range"
            return result
        result["pivot_time_ms"] = ts[pivot_idx]

        lo = max(0, pivot_idx - bars_before)
        hi = min(len(ts) - 1, pivot_idx + bars_after)
        window = {ts[i]: i - pivot_idx for i in range(lo, hi + 1)}

        sfps = run_sfp_signals(df, symbol, dtm_timeframe)
        same_dir = [s for s in sfps if s["direction"] == dtm_direction]
        match = [s for s in same_dir if s["time_ms"] in window]

        if not match:
            result["reason"] = "no_sfp_near_pivot" if not sfps else "no_same_direction_sfp_near_pivot"
            return result

        best = min(match, key=lambda s: (abs(window[s["time_ms"]]), window[s["time_ms"]]))
        result.update(allowed=True, reason="confirmed", sfp_signal=best,
                      offset=window[best["time_ms"]])
        return result
    except Exception as e:
        logger.exception(f"[SFP-FILTER] {symbol} {dtm_timeframe}m: error: {e}")
        result["reason"] = "filter_error"
        return result


def _offset_text(off):
    if off is None:
        return "?"
    if off == 0:
        return "روی کندل پیوت"
    return f"{abs(off)} کندل {'بعد از' if off > 0 else 'قبل از'} پیوت"


def format_sfp_filter_log(symbol, dtm_direction, dtm_timeframe, result):
    status = "✅ ALLOW" if result.get("allowed") else "❌ REJECT"
    line = (f"[SFP-FILTER] {symbol} DTM@{dtm_timeframe}m {dtm_direction} → {status} "
            f"({result.get('reason')})")
    s = result.get("sfp_signal")
    if s:
        line += f" | SFP: {s['kind']} @ {s['time_iran'].strftime('%m-%d %H:%M')} ({_offset_text(result.get('offset'))})"
    return line


def format_sfp_filter_telegram_line(result):
    """خط تأیید فیلتر برای ضمیمه‌ی پیام سیگنال DTM (HTML)."""
    s = result.get("sfp_signal")
    if not (result.get("allowed") and s):
        return ""
    import tg_messages as tgm
    detail = f"{s['kind']} · {s['time_iran'].strftime('%H:%M')} تهران · {_offset_text(result.get('offset'))}"
    return tgm.filter_confirm_line("SFP", detail) + "\n"
