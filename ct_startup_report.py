"""
ct_startup_report.py
====================
گزارش استارت‌آپ CT برای نمایش در تلگرام
- دریافت دیتا از thetruetrade.io (داخل bot.py)
- محاسبه ۵ سیگنال آخر CT برای هر نماد × تایم‌فریم
- فرمت پیشرفته با تاریخ/ساعت دقیق ایران
"""
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger("CT_STARTUP")

IRAN_TZ = timezone(timedelta(hours=3, minutes=30))
UTC_TZ = timezone.utc

# ═══════════════════════════════════════════════════════════════
# نمادها و تایم‌فریم‌های CT
# ═══════════════════════════════════════════════════════════════
CT_SYMBOLS = ["ETHUSDT", "BTCUSDT", "SOLUSDT", "BNBUSDT"]
CT_TIMEFRAMES = ["60", "240"]  # 1h, 4h
CT_SIGNALS_TO_SHOW = 5


def _time_ago_fa(delta_seconds: float) -> str:
    """زمان نسبی به فارسی"""
    if delta_seconds < 60:
        return "الان"
    elif delta_seconds < 3600:
        return f"{int(delta_seconds/60)}د"
    elif delta_seconds < 86400:
        return f"{int(delta_seconds/3600)}س"
    else:
        return f"{int(delta_seconds/86400)}ر"


def _tf_label(tf: str) -> str:
    """برچسب تایم‌فریم"""
    tf_min = int(tf)
    return f"{tf_min}m" if tf_min < 60 else f"{tf_min//60}h"


def format_one_block(symbol: str, tf_label: str, signals: list, now_iran: datetime) -> str:
    """فرمت یه بلوک (نماد @ تایم‌فریم) — بدون باکس، تراز RTL-friendly"""
    lines = []
    
    # هدر بلوک
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"🪙 {symbol}  @  {tf_label}   ({len(signals)} سیگنال)")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if not signals:
        lines.append("⚠️ بدون سیگنال در بازه اخیر")
        lines.append("")
        return "\n".join(lines)
    
    # ۵ سیگنال آخر (جدیدترین اول)
    sorted_signals = sorted(signals, key=lambda x: x['time_ms'] or 0, reverse=True)
    last5 = sorted_signals[:CT_SIGNALS_TO_SHOW]
    
    for i, s in enumerate(last5, 1):
        emoji = "🟢" if s['direction'] == 'LONG' else "🔴"
        direction_fa = "لانگ" if s['direction'] == 'LONG' else "شورت"
        
        t_iran = s['time_iran']
        if t_iran:
            t_str = t_iran.strftime('%Y-%m-%d %H:%M')
            ago = _time_ago_fa((now_iran - t_iran).total_seconds())
        else:
            t_str = "?"
            ago = "?"
        
        # R:R
        rr = 0.0
        if s['entry'] and s['stop']:
            risk = abs(s['entry'] - s['stop'])
            if risk > 0:
                rr = abs(s['target'] - s['entry']) / risk
        
        lines.append(f"{emoji} #{i}  {s['kind']}  ({direction_fa})")
        lines.append(f"   🕐 {t_str}  ({ago} پیش)")
        lines.append(f"   📍 ورود: {s['entry']:.4f}")
        lines.append(f"   🛑 SL:  {s['stop']:.4f}")
        lines.append(f"   🎯 TP:  {s['target']:.4f}")
        lines.append(f"   ⚖️ R:R = 1 : {rr:.2f}")
        lines.append("")
    
    # خلاصه بلوک
    long_count = sum(1 for s in signals if s['direction'] == 'LONG')
    short_count = sum(1 for s in signals if s['direction'] == 'SHORT')
    lines.append(f"📊 خلاصه: {len(signals)} سیگنال  |  🟢 {long_count} لانگ  |  🔴 {short_count} شورت")
    lines.append("")
    
    return "\n".join(lines)


def build_ct_startup_report(public_data, symbols=None, timeframes=None) -> str:
    """
    ساخت گزارش کامل استارت‌آپ CT.
    
    Args:
        public_data: PublicData instance از bot.py
        symbols: لیست نمادها (پیش‌فرض: CT_SYMBOLS)
        timeframes: لیست تایم‌فریم‌ها (پیش‌فرض: CT_TIMEFRAMES)
    
    Returns:
        str — گزارش کامل برای ارسال به تلگرام
    """
    from ct_wrapper import run_ct_strategy
    
    if symbols is None:
        symbols = CT_SYMBOLS
    if timeframes is None:
        timeframes = CT_TIMEFRAMES
    
    all_results = {}
    now_iran = datetime.now(UTC_TZ).astimezone(IRAN_TZ)
    
    for symbol in symbols:
        for tf in timeframes:
            tf_label = _tf_label(tf)
            try:
                df = public_data.fetch_ohlcv(symbol, tf)
                if df is None or df.empty:
                    logger.warning(f"[CT-STARTUP] {symbol} {tf_label}: empty data")
                    all_results[f"{symbol}|{tf_label}"] = []
                    continue
                
                signals = run_ct_strategy(df, symbol, tf)
                signals = [s for s in signals if s is not None]
                all_results[f"{symbol}|{tf_label}"] = signals
                
                logger.info(f"[CT-STARTUP] {symbol} {tf_label}: {len(signals)} signals")
            except Exception as e:
                logger.error(f"[CT-STARTUP] {symbol} {tf_label}: {e}")
                all_results[f"{symbol}|{tf_label}"] = []
    
    # ساخت گزارش
    lines = []
    
    # هدر
    lines.append("╔══════════════════════════════════════╗")
    lines.append("║   🎯  گزارش CT (Ichimoku)            ║")
    lines.append("╚══════════════════════════════════════╝")
    lines.append("")
    lines.append(f"🕐 {now_iran.strftime('%Y-%m-%d %H:%M:%S')} (تهران)")
    lines.append("")
    
    # بلوک‌ها
    for symbol in symbols:
        for tf in timeframes:
            tf_label = _tf_label(tf)
            key = f"{symbol}|{tf_label}"
            signals = all_results.get(key, [])
            lines.append(format_one_block(symbol, tf_label, signals, now_iran))
    
    # Footer
    total = sum(len(v) for v in all_results.values())
    lines.append("════════════════════════════════════")
    lines.append(f"📊 مجموع: {total} سیگنال در {len(all_results)} ترکیب")
    lines.append("════════════════════════════════════")
    
    return "\n".join(lines)