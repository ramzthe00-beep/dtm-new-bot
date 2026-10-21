"""
golden_paper_trader.py — Paper Trading ۳۰ روزه
اجرای هر ساعت، دریافت سیگنال‌های جدید، ثبت در CSV
"""
import os, sys, time, json, csv, logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd

BASE = Path.home() / "dtm-new-bot"
sys.path.insert(0, str(BASE))
os.chdir(BASE)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(BASE / "golden_logs" / "paper_trader.log"),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger("PAPER_TRADER")

UTC = timezone.utc
IRAN = timezone(timedelta(hours=3, minutes=30))

PAPER_TRADES_FILE = BASE / "golden_paper_trades.csv"
PAPER_STATE_FILE = BASE / "golden_paper_state.json"

from golden_portfolio import check_all_signals, GOLDEN_CONFIGS


def log_signal(sig):
    """ثبت سیگنال در CSV"""
    file_exists = PAPER_TRADES_FILE.exists()
    with open(PAPER_TRADES_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow([
                "config_id", "symbol", "ct_tf", "mode", "rr",
                "direction", "kind", "entry", "stop", "target",
                "time_utc", "time_iran", "outcome", "exit_price",
                "pnl_R", "net_R", "resolved_at"
            ])
        t_iran = sig["time_utc"].tz_convert(IRAN)
        w.writerow([
            sig["config_id"], sig["symbol"], sig["ct_tf"], sig["mode"], sig["rr"],
            sig["direction"], sig["kind"],
            f"{sig['entry']:.4f}", f"{sig['stop']:.4f}", f"{sig['target']:.4f}",
            sig["time_utc"].isoformat(),
            t_iran.strftime("%Y-%m-%d %H:%M"),
            "OPEN", "", "", "", "",
        ])
    logger.info(f"📝 NEW: {sig['config_id']} {sig['symbol']} {sig['direction']} "
                f"@ {sig['entry']:.4f} | SL={sig['stop']:.4f} | TP={sig['target']:.4f} | "
                f"{t_iran.strftime('%Y-%m-%d %H:%M')} تهران")


def update_open_trades():
    """بررسی معاملات باز — آیا به TP/SL رسیده‌اند؟"""
    if not PAPER_TRADES_FILE.exists():
        return
    df = pd.read_csv(PAPER_TRADES_FILE)
    open_trades = df[df["outcome"] == "OPEN"]
    if open_trades.empty:
        return

    from golden_portfolio import fetch_klines
    import math

    for idx, trade in open_trades.iterrows():
        symbol = trade["symbol"]
        entry_time = pd.Timestamp(trade["time_utc"])
        try:
            df_1m = fetch_klines(symbol, "1m", limit=500)
        except:
            continue

        # کندل‌های بعد از ورود
        after = df_1m[df_1m.index > entry_time]
        if after.empty:
            continue

        direction = trade["direction"]
        entry = float(trade["entry"])
        stop = float(trade["stop"])
        target = float(trade["target"])

        exit_price = None
        outcome = None
        for ts, row in after.iterrows():
            h = row['high']; l = row['low']
            if direction == "LONG":
                if l <= stop: exit_price = stop; outcome = "STOP"; break
                if h >= target: exit_price = target; outcome = "TARGET"; break
            else:
                if h >= stop: exit_price = stop; outcome = "STOP"; break
                if l <= target: exit_price = target; outcome = "TARGET"; break

        if exit_price is not None:
            D = abs(entry - stop)
            if direction == "LONG":
                pnl = (exit_price - entry) / D
            else:
                pnl = (entry - exit_price) / D

            df.at[idx, "outcome"] = outcome
            df.at[idx, "exit_price"] = f"{exit_price:.4f}"
            df.at[idx, "pnl_R"] = f"{pnl:.2f}"
            df.at[idx, "net_R"] = f"{pnl:.2f}"  # کارمزد نادیده (تقریبی)
            df.at[idx, "resolved_at"] = datetime.now(UTC).isoformat()
            logger.info(f"✅ {outcome}: {symbol} {direction} → {pnl:+.2f}R")

    df.to_csv(PAPER_TRADES_FILE, index=False)


def print_status():
    """چاپ وضعیت فعلی"""
    if not PAPER_TRADES_FILE.exists():
        logger.info("هیچ معامله‌ای ثبت نشده")
        return

    df = pd.read_csv(PAPER_TRADES_FILE)
    if df.empty:
        return

    closed = df[df["outcome"].isin(["TARGET", "STOP"])]
    open_cnt = len(df[df["outcome"] == "OPEN"])
    total_net = pd.to_numeric(closed["net_R"], errors='coerce').sum()

    logger.info(f"📊 STATUS: {len(df)} کل | {len(closed)} بسته | "
                f"{open_cnt} باز | Net={total_net:+.2f}R")


def main():
    logger.info("🚀 Paper Trader شروع شد")
    logger.info(f"📋 {len(GOLDEN_CONFIGS)} ترکیب فعال")
    for cfg in GOLDEN_CONFIGS:
        logger.info(f"   - {cfg['label']}")

    cycle = 0
    while True:
        cycle += 1
        logger.info(f"\n{'='*70}")
        logger.info(f"🔄 چرخه {cycle} — {datetime.now(IRAN).strftime('%Y-%m-%d %H:%M')} تهران")
        logger.info(f"{'='*70}")

        try:
            new_signals = check_all_signals()
            for sig in new_signals:
                log_signal(sig)

            if not new_signals:
                logger.info("😴 سیگنال جدیدی نیست")

            update_open_trades()
            print_status()

        except Exception as e:
            logger.exception(f"❌ خطا در چرخه: {e}")

        # هر ۵ دقیقه
        logger.info(f"⏳ انتظار ۵ دقیقه...")
        time.sleep(300)


if __name__ == "__main__":
    main()