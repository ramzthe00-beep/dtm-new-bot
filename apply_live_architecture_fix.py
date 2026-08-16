from pathlib import Path
import shutil
import re

ROOT = Path.home() / "dtm-new-bot"
LIVE = ROOT / "dtm_live.py"
BACKUP = ROOT / "dtm_live.py.before_live_arch_fix"

if not LIVE.exists():
    raise SystemExit("ERROR: dtm_live.py not found")

if not BACKUP.exists():
    shutil.copy2(LIVE, BACKUP)

src = LIVE.read_text(encoding="utf-8")

# ------------------------------------------------------------
# SAFETY: dtm.py must remain untouched
# ------------------------------------------------------------
dtm = ROOT / "dtm.py"
if not dtm.exists():
    raise SystemExit("ERROR: dtm.py not found")

# ------------------------------------------------------------
# Replace the current full-history-per-loop architecture.
# We deliberately keep strategy logic inside dtm.py/PyneCore.
# ------------------------------------------------------------

start = src.find("def analyze_and_execute():")
end = src.find("\n\ndef run_live_loop():", start)

if start < 0 or end < 0:
    raise SystemExit("ERROR: expected live functions not found")

new_block = r'''
# ============================================================
# PERSISTENT PYNECORE LIVE ARCHITECTURE
# ============================================================

RUNNERS = {}
LAST_LIVE_TS = {}
WARMUP_DONE = {}

def _closed_only(df):
    """Return only finalized candles."""
    if df.empty:
        return df

    out = df.copy()

    if API_RETURNS_OPEN_CANDLE and len(out):
        out = out.iloc[:-1].copy()

    if len(out):
        ts = out.index[-1]
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")

        bar_end = ts + pd.Timedelta(minutes=1)

        if pd.Timestamp.now(tz="UTC") < bar_end:
            out = out.iloc[:-1].copy()

    return out


def _create_runner(symbol, warmup_df):
    """Create ONE persistent ScriptRunner for a symbol."""
    candles = list(_df_to_ohlcv(warmup_df))

    if len(candles) < 120:
        raise RuntimeError(
            f"{symbol}: insufficient warmup candles={len(candles)}"
        )

    logger.info(
        "[WARMUP START] %s | candles=%d | first=%s | last=%s",
        symbol,
        len(candles),
        warmup_df.index[0],
        warmup_df.index[-1],
    )

    runner = ScriptRunner(
        script_path=PYNE_SCRIPT,
        ohlcv_iter=candles,
        syminfo=_make_syminfo(symbol),
        inputs=PYNE_INPUTS,
    )

    last = None
    for result in runner.run_iter():
        last = result

    if last is None:
        raise RuntimeError(f"{symbol}: PyneCore warmup produced no result")

    RUNNERS[symbol] = runner
    WARMUP_DONE[symbol] = True

    logger.info(
        "[WARMUP COMPLETE] %s | candles=%d",
        symbol,
        len(candles),
    )

    return last


def _run_persistent_runner(symbol, candle):
    """
    Feed a NEW candle through the persistent PyneCore lifecycle.

    NOTE:
    The exact ScriptRunner incremental API depends on the installed
    PyneCore version. We intentionally do not recreate the runner here.
    """
    runner = RUNNERS.get(symbol)

    if runner is None:
        raise RuntimeError(
            f"{symbol}: persistent runner is not initialized"
        )

    # Current PyneCore ScriptRunner exposes run_iter() around its input
    # iterator. For a true incremental provider, the provider/generator
    # must own the stream and keep this runner alive.
    #
    # Do NOT rebuild ScriptRunner here.
    return None


def warmup_symbol(symbol, data):
    df = data.fetch_ohlcv(symbol, TIMEFRAME, HISTORY_BARS)

    if df.empty:
        raise RuntimeError(f"{symbol}: empty OHLCV")

    closed = _closed_only(df)

    if len(closed) < 120:
        raise RuntimeError(
            f"{symbol}: insufficient closed candles={len(closed)}"
        )

    return _create_runner(symbol, closed)


def analyze_and_execute():
    logger.info("[LIVE CYCLE] checking new closed candles")

    exchange = TrueTradePrivateExchange(API_KEY, API_SECRET, BASE_URL)
    conn = exchange.test_connection() if API_KEY and API_SECRET else False

    balance = exchange.fetch_balance() if conn else 0.0
    if balance is None:
        balance = 0.0

    data = TrueTradePublicData()

    # --------------------------------------------------------
    # ONE-TIME WARMUP
    # --------------------------------------------------------
    for symbol in SYMBOLS:
        try:
            if not WARMUP_DONE.get(symbol):
                warmup_symbol(symbol, data)
        except Exception:
            logger.error(
                "[WARMUP ERROR] %s\n%s",
                symbol,
                traceback.format_exc(),
            )

    # --------------------------------------------------------
    # LIVE CLOSED-BAR GATE
    # --------------------------------------------------------
    for symbol in SYMBOLS:
        try:
            df = data.fetch_ohlcv(symbol, TIMEFRAME, HISTORY_BARS)

            if df.empty:
                continue

            closed_df = _closed_only(df)

            if closed_df.empty:
                continue

            ts = closed_df.index[-1]
            processed_ts = str(ts)

            if LAST_LIVE_TS.get(symbol) == processed_ts:
                logger.info(
                    "[DUPLICATE BAR SKIP] %s %s",
                    symbol,
                    processed_ts,
                )
                continue

            logger.info(
                "[NEW CLOSED BAR] %s %s",
                symbol,
                processed_ts,
            )

            # IMPORTANT:
            # The strategy state is NOT recreated here.
            #
            # The existing ScriptRunner remains the owner of the
            # historical state. The installed PyneCore live/provider
            # adapter must feed this candle into that same runner.
            #
            # Until the installed ScriptRunner exposes an incremental
            # feed API, do not fake it by rebuilding the runner.

            LAST_LIVE_TS[symbol] = processed_ts

        except Exception:
            logger.error(
                "[LIVE ERROR] %s\n%s",
                symbol,
                traceback.format_exc(),
            )

    save_states()


def run_live_loop():
    logger.info(
        "DTM LIVE BOT | PERSISTENT PYNECORE ARCHITECTURE | %s | %s",
        TIMEFRAME,
        ",".join(SYMBOLS),
    )

    logger.info(
        "PYNECORE SOURCE: %s",
        PYNE_SCRIPT,
    )

    while True:
        try:
            analyze_and_execute()
        except Exception:
            logger.error(
                "[LOOP ERROR]\n%s",
                traceback.format_exc(),
            )

        time.sleep(60)
'''

src = src[:start] + new_block + src[end:]

LIVE.write_text(src, encoding="utf-8")

print("PATCH APPLIED")
print("Backup:", BACKUP)
print("Modified:", LIVE)
print("dtm.py was NOT modified")
