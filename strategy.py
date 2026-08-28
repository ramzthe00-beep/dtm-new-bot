"""
@pyne edge

This code was compiled by PyneComp v6.0.54 — the Pine Script to Python compiler.
Run with open-source PyneCore: https://pynecore.org
Compile Pine Scripts online at PyneSys: https://pynesys.io
"""
from pynecore import pine_range
from pynecore.lib import (
    bar_index, barmerge, close, color, high, input, location, low, math, na,
    open, plotshape, request, script, shape, size, strategy, syminfo, ta
)
from pynecore.types import Persistent, Series

grp_pivot: str = "Pivot"
grp_ind: str = "Indicators"
grp_trend: str = "Trend"
grp_score: str = "Min Confirmations"
grp_fib: str = "Fibonacci"
grp_candle: str = "Price Action"
# ============================================================
# آستانه‌های فیلتر ترکیبی (بر اساس تحلیل ۳۲ سیگنال)
# ============================================================
RSI_MIN_GAP = 1.3          # با حاشیه امن ۱۵٪ (۱.۵۸۹ × ۰.۸۵)
PRICE_MIN_GAP_PCT = 0.025  # با حاشیه امن ۱۵٪ (۰.۰۲۹۴ × ۰.۸۵)
MACD_MIN_GAP = 0.00001     # تقریباً بی‌اثر، برای امنیت
HIST_MIN_FIRST = 0.00001   # تقریباً بی‌اثر
HIST_MIN_SECOND = 0.000001 # کاملاً بی‌اثر

@script.strategy("DTM Divergence Light", overlay=True, initial_capital=500, default_qty_type=strategy.fixed, default_qty_value=1, commission_type=strategy.commission.percent, commission_value=0.1, pyramiding=3, process_orders_on_close=True, max_labels_count=50, max_lines_count=50)
def main(
    pivotMode=input.string("سریع (5/3)", "روش Pivot", options=("استاندارد (5/5)", "سریع (5/3)"), group=grp_pivot),
    rsiLen=input.int(14, "RSI", group=grp_ind),
    macdFast=input.int(12, "MACD Fast", group=grp_ind),
    macdSlow=input.int(26, "MACD Slow", group=grp_ind),
    macdSig=input.int(9, "MACD Signal", group=grp_ind),
    trendLookback=input.int(20, "Trend Lookback", group=grp_trend),
    trendSlopeMinPct=input.float(0.05, "Min Slope %", step=0.01, group=grp_trend),
    minConfirmations=input.string("۳ تعییدیه (حداقل مجاز)", "حداقل شرط", options=("۳ تعییدیه (حداقل مجاز)", "۳ تعییدیه + فیبوناچی (۴ امتیاز) [Custom]", "۳ تعییدیه + پرایس‌اکشن (۴ امتیاز) [Custom]", "۵ امتیاز کامل (ایده‌آل)"), group=grp_score),
    enableHidden=input.bool(True, "Enable Hidden Divergence"),
    fibUse618=input.bool(True, "Use 0.618", group=grp_fib),
    fibUse786=input.bool(True, "Use 0.786", group=grp_fib),
    fibTolerancePct=input.float(0.5, "Fib Tolerance %", step=0.1, group=grp_fib),
    fibTrendSearchBars=input.int(100, "Fib Search Bars", group=grp_fib),
    shadowToBodyRatio=input.float(2.0, "Shadow/Body Ratio", group=grp_candle),
    maxOppositeShadowPct=input.float(20.0, "Max Opposite Shadow %", group=grp_candle),
    minCandleATRRatio=input.float(0.3, "Min Candle ATR Ratio", group=grp_candle),
    bigCandleAvgLen=input.int(14, "Big Candle Avg Len", group=grp_candle),
    bigCandleMultiplier=input.float(1.5, "Big Candle Mult", group=grp_candle),
):
    leftBars: int = 5
    rightBars = 3

    # PyneCore 6.8.7 — native RSI API
    rsiVal: Series = ta.rsi(source=close, length=rsiLen)
    macdLine: Series
    histLine: Series
    macdLine, signalLine, histLine = ta.macd(source=close, fastlen=macdFast, slowlen=macdSlow, siglen=macdSig)
    atr14 = ta.atr(length=14)

    pivotHighPrice = ta.pivothigh(high, leftBars, rightBars)
    pivotLowPrice = ta.pivotlow(low, leftBars, rightBars)

    rsiAtPivotHigh = ta.valuewhen(not na(pivotHighPrice), rsiVal[rightBars], 0)
    rsiAtPivotLow = ta.valuewhen(not na(pivotLowPrice), rsiVal[rightBars], 0)
    macdLineAtPivotHigh = ta.valuewhen(not na(pivotHighPrice), macdLine[rightBars], 0)
    macdLineAtPivotLow = ta.valuewhen(not na(pivotLowPrice), macdLine[rightBars], 0)
    histAtPivotHigh = ta.valuewhen(not na(pivotHighPrice), histLine[rightBars], 0)
    histAtPivotLow = ta.valuewhen(not na(pivotLowPrice), histLine[rightBars], 0)

    ph_price_2: Persistent[float] = na(float)
    ph_price_1: Persistent[float] = na(float)
    ph_bar_2: Persistent[int] = na(int)
    ph_bar_1: Persistent[int] = na(int)
    ph_rsi_2: Persistent[float] = na(float)
    ph_rsi_1: Persistent[float] = na(float)
    ph_macdline_2: Persistent[float] = na(float)
    ph_macdline_1: Persistent[float] = na(float)
    ph_hist_2: Persistent[float] = na(float)
    ph_hist_1: Persistent[float] = na(float)


    pl_price_2: Persistent[float] = na(float)
    pl_price_1: Persistent[float] = na(float)
    pl_bar_2: Persistent[int] = na(int)
    pl_bar_1: Persistent[int] = na(int)
    pl_rsi_2: Persistent[float] = na(float)
    pl_rsi_1: Persistent[float] = na(float)
    pl_macdline_2: Persistent[float] = na(float)
    pl_macdline_1: Persistent[float] = na(float)
    pl_hist_2: Persistent[float] = na(float)
    pl_hist_1: Persistent[float] = na(float)

    newPivotHigh = not na(pivotHighPrice)
    newPivotLow = not na(pivotLowPrice)

    if newPivotHigh:
        ph_price_1 = ph_price_2
        ph_bar_1 = ph_bar_2
        ph_rsi_1 = ph_rsi_2
        ph_macdline_1 = ph_macdline_2
        ph_hist_1 = ph_hist_2
        ph_price_2 = pivotHighPrice
        ph_bar_2 = bar_index - rightBars
        ph_rsi_2 = rsiAtPivotHigh
        ph_macdline_2 = macdLineAtPivotHigh
        ph_hist_2 = histAtPivotHigh
        leftNeighborMaxHigh = ta.highest(high[rightBars + 1], leftBars)
        rightNeighborMaxHigh = ta.highest(high, rightBars) if rightBars > 0 else na(float)
        prominenceHigh = pivotHighPrice - math.max(leftNeighborMaxHigh, rightNeighborMaxHigh)
    else:
        prominenceHigh = na(float)

    if newPivotLow:
        pl_price_1 = pl_price_2
        pl_bar_1 = pl_bar_2
        pl_rsi_1 = pl_rsi_2
        pl_macdline_1 = pl_macdline_2
        pl_hist_1 = pl_hist_2
        pl_price_2 = pivotLowPrice
        pl_bar_2 = bar_index - rightBars
        pl_rsi_2 = rsiAtPivotLow
        pl_macdline_2 = macdLineAtPivotLow
        pl_hist_2 = histAtPivotLow
        leftNeighborMinLow = ta.lowest(low[rightBars + 1], leftBars)
        rightNeighborMinLow = ta.lowest(low, rightBars) if rightBars > 0 else na(float)
        prominenceLow = math.min(leftNeighborMinLow, rightNeighborMinLow) - pivotLowPrice
    else:
        prominenceLow = na(float)

    def checkColorChange(barStart, barEnd, needRedPhase):
        found: bool = False
        if not na(barStart) and (not na(barEnd)) and (barEnd > barStart):
            startOffset = bar_index - (barEnd - 1)
            endOffset = bar_index - (barStart + 1)
            if startOffset >= 0 and endOffset <= 5000 and (endOffset >= startOffset):
                for j in pine_range(startOffset, endOffset):
                    h = histLine[j]
                    if needRedPhase and h < 0:
                        found = True
                        break
                    if not needRedPhase and h > 0:
                        found = True
                        break
        return found

    macdColorChangedForHighs = checkColorChange(ph_bar_1, ph_bar_2, True) if newPivotHigh and (not na(ph_bar_1)) else False
    macdColorChangedForLows = checkColorChange(pl_bar_1, pl_bar_2, False) if newPivotLow and (not na(pl_bar_1)) else False


    def isTrendingUp(refBar):
        result: bool = False
        if not na(refBar):
            offset = bar_index - refBar
            if offset >= 0 and offset + trendLookback < 5000:
                slope = ta.linreg(close[offset], trendLookback, 0) - ta.linreg(close[offset + trendLookback], trendLookback, 0)
                avgPrice = ta.sma(close[offset], trendLookback)
                slopePct = slope / avgPrice * 100 if avgPrice != 0 else 0.0
                result = slopePct > trendSlopeMinPct
        return result

    def isTrendingDown(refBar):
        result: bool = False
        if not na(refBar):
            offset = bar_index - refBar
            if offset >= 0 and offset + trendLookback < 5000:
                slope = ta.linreg(close[offset], trendLookback, 0) - ta.linreg(close[offset + trendLookback], trendLookback, 0)
                avgPrice = ta.sma(close[offset], trendLookback)
                slopePct = slope / avgPrice * 100 if avgPrice != 0 else 0.0
                result = slopePct < -trendSlopeMinPct
        return result

    trendOkForBearish = isTrendingUp(ph_bar_1) if newPivotHigh and (not na(ph_bar_1)) else False
    trendOkForBullish = isTrendingDown(pl_bar_1) if newPivotLow and (not na(pl_bar_1)) else False

    def findTrendStartLow(refBar):
        result: float = na(float)
        if not na(refBar):
            offset = bar_index - refBar
            if offset >= 0 and offset + fibTrendSearchBars < 5000:
                result = ta.lowest(low[offset], fibTrendSearchBars)
        return result

    def findTrendStartHigh(refBar):
        result: float = na(float)
        if not na(refBar):
            offset = bar_index - refBar
            if offset >= 0 and offset + fibTrendSearchBars < 5000:
                result = ta.highest(high[offset], fibTrendSearchBars)
        return result

    def checkFibLevel(fibStart, fibEnd, targetPrice, isBullish):
        ok: bool = False
        if not na(fibStart) and not na(fibEnd) and fibEnd != fibStart:
            range_ = math.abs(fibEnd - fibStart)
            tol = range_ * (fibTolerancePct / 100.0)
        
            # موج صعودی: کف به سقف → اصلاح به سمت پایین
            # موج نزولی: سقف به کف → اصلاح به سمت بالا
            if isBullish:  # Bullish: از کف به سقف
                level618 = fibEnd - range_ * 0.618
                level786 = fibEnd - range_ * 0.786
            else:          # Bearish: از سقف به کف
                level618 = fibEnd + range_ * 0.618
                level786 = fibEnd + range_ * 0.786
        
            if fibUse618 and math.abs(targetPrice - level618) <= tol:
                ok = True
            if fibUse786 and math.abs(targetPrice - level786) <= tol:
                ok = True
        return ok


    # Bearish Divergence - Fibonacci
    fibScoreBearish: bool = False
    if newPivotHigh and (not na(ph_bar_1)):
        trendStart = findTrendStartLow(ph_bar_1)   # کف روند
        fibScoreBearish = checkFibLevel(trendStart, ph_price_1, ph_price_2, False)  # isBullish = False

    # Bullish Divergence - Fibonacci
    fibScoreBullish: bool = False
    if newPivotLow and (not na(pl_bar_1)):
        trendStart = findTrendStartHigh(pl_bar_1)  # سقف روند
        fibScoreBullish = checkFibLevel(trendStart, pl_price_1, pl_price_2, True)   # isBullish = True

    
    # ============================================================
    # محاسبه اندیکاتورهای کندلی
    # ============================================================
    candleRange = high - low
    candleBody = math.abs(close - open)
    upperShadow = high - math.max(close, open)
    lowerShadow = math.min(close, open) - low
    avgBody = ta.sma(math.abs(close - open), bigCandleAvgLen)
    sizeOk = candleRange >= minCandleATRRatio * atr14

    # ============================================================
    # الگوهای صعودی (Bullish)
    # ============================================================
    bullishHammer = (
        candleRange > 0
        and lowerShadow >= shadowToBodyRatio * candleBody
        and (upperShadow / candleRange * 100 <= maxOppositeShadowPct)
        and sizeOk
    )

    bullishLargeBody = (
        close > open
        and candleBody >= bigCandleMultiplier * avgBody
        and sizeOk
    )

    priceActionBullish = bullishHammer or bullishLargeBody

    # ============================================================
    # الگوهای نزولی (Bearish)
    # ============================================================
    bearishShootingStar = (
        candleRange > 0
        and upperShadow >= shadowToBodyRatio * candleBody
        and (lowerShadow / candleRange * 100 <= maxOppositeShadowPct)
        and sizeOk
    )

    bearishLowerWickRejection = (
        candleRange > 0
        and lowerShadow >= shadowToBodyRatio * candleBody
        and (upperShadow / candleRange * 100 <= maxOppositeShadowPct)
        and sizeOk
    )

    bearishLargeBody = (
        close < open
        and candleBody >= bigCandleMultiplier * avgBody
        and sizeOk
    )

    priceActionBearish = (
        bearishShootingStar
        or bearishLowerWickRejection
        or bearishLargeBody
    )

    # ============================================================
    # ذخیره در کندل تأیید Pivot
    # ============================================================
    priceActionBullishAtPivot = priceActionBullish
    priceActionBearishAtPivot = priceActionBearish

    priceHigherHigh = newPivotHigh and (not na(ph_price_1)) and (ph_price_2 > ph_price_1) and (((ph_price_2 - ph_price_1) / ph_price_1) * 100 > PRICE_MIN_GAP_PCT)
    rsiLowerHighOnPeaks = newPivotHigh and (not na(ph_rsi_1)) and ((ph_rsi_1 - ph_rsi_2) > RSI_MIN_GAP)
    macdLineLowerHighOnPeaks = newPivotHigh and (not na(ph_macdline_1)) and (ph_macdline_2 < ph_macdline_1)
    histLowerHighOnPeaks = newPivotHigh and (not na(ph_hist_1)) and (ph_hist_2 < ph_hist_1)
    bothPeaksGreen = newPivotHigh and (not na(ph_hist_1)) and (ph_hist_1 > 0) and (ph_hist_2 > 0)

    classicBearishCond1_RSI = priceHigherHigh and rsiLowerHighOnPeaks
    classicBearishCond2_MACDl = priceHigherHigh and macdLineLowerHighOnPeaks
    classicBearishCond3_MACDh = priceHigherHigh and histLowerHighOnPeaks and bothPeaksGreen and macdColorChangedForHighs
    classicBearishBase3 = priceHigherHigh and trendOkForBearish and classicBearishCond3_MACDh and classicBearishCond1_RSI and classicBearishCond2_MACDl

    
    priceLowerLow = newPivotLow and (not na(pl_price_1)) and (pl_price_2 < pl_price_1) and (((pl_price_1 - pl_price_2) / pl_price_1) * 100 > PRICE_MIN_GAP_PCT)
    rsiHigherLowOnTroughs = newPivotLow and (not na(pl_rsi_1)) and ((pl_rsi_2 - pl_rsi_1) > RSI_MIN_GAP)
    macdLineHigherLowOnTroughs = newPivotLow and (not na(pl_macdline_1)) and (pl_macdline_2 > pl_macdline_1)
    histHigherLowOnTroughs = newPivotLow and (not na(pl_hist_1)) and (pl_hist_2 > pl_hist_1)
    bothTroughsRed = newPivotLow and (not na(pl_hist_1)) and (pl_hist_1 < 0) and (pl_hist_2 < 0)

    classicBullishCond1_RSI = priceLowerLow and rsiHigherLowOnTroughs
    classicBullishCond2_MACDl = priceLowerLow and macdLineHigherLowOnTroughs
    classicBullishCond3_MACDh = priceLowerLow and histHigherLowOnTroughs and bothTroughsRed and macdColorChangedForLows
    classicBullishBase3 = priceLowerLow and trendOkForBullish and classicBullishCond3_MACDh and classicBullishCond1_RSI and classicBullishCond2_MACDl

    
    priceHigherLow = newPivotLow and (not na(pl_price_1)) and (pl_price_2 > pl_price_1) and (((pl_price_2 - pl_price_1) / pl_price_1) * 100 > PRICE_MIN_GAP_PCT)
    rsiLowerLowOnTroughs = newPivotLow and (not na(pl_rsi_1)) and ((pl_rsi_1 - pl_rsi_2) > RSI_MIN_GAP)
    macdLineLowerLowOnTroughs = newPivotLow and (not na(pl_macdline_1)) and (pl_macdline_2 < pl_macdline_1)
    histLowerLowOnTroughs = newPivotLow and (not na(pl_hist_1)) and (pl_hist_2 < pl_hist_1)

    hiddenBullishCond1_RSI = priceHigherLow and rsiLowerLowOnTroughs
    hiddenBullishCond2_MACDl = priceHigherLow and macdLineLowerLowOnTroughs
    hiddenBullishCond3_MACDh = priceHigherLow and histLowerLowOnTroughs and bothTroughsRed and macdColorChangedForLows
    hiddenBullishBase3 = enableHidden and priceHigherLow and hiddenBullishCond3_MACDh and hiddenBullishCond1_RSI and hiddenBullishCond2_MACDl

    
    priceLowerHigh = newPivotHigh and (not na(ph_price_1)) and (ph_price_2 < ph_price_1) and (((ph_price_1 - ph_price_2) / ph_price_1) * 100 > PRICE_MIN_GAP_PCT)
    rsiHigherHighOnPeaks = newPivotHigh and (not na(ph_rsi_1)) and ((ph_rsi_2 - ph_rsi_1) > RSI_MIN_GAP)
    macdLineHigherHighOnPeaks = newPivotHigh and (not na(ph_macdline_1)) and (ph_macdline_2 > ph_macdline_1)
    histHigherHighOnPeaks = newPivotHigh and (not na(ph_hist_1)) and (ph_hist_2 > ph_hist_1)

    hiddenBearishCond1_RSI = priceLowerHigh and rsiHigherHighOnPeaks
    hiddenBearishCond2_MACDl = priceLowerHigh and macdLineHigherHighOnPeaks
    hiddenBearishCond3_MACDh = priceLowerHigh and histHigherHighOnPeaks and bothPeaksGreen and macdColorChangedForHighs
    hiddenBearishBase3 = enableHidden and priceLowerHigh and hiddenBearishCond3_MACDh and hiddenBearishCond1_RSI and hiddenBearishCond2_MACDl

    def passesMinRequirement(base3, fibOk, paOk):
        result: bool = False
        if base3:
            if minConfirmations == '۳ تعییدیه (حداقل مجاز)':
                result = True
            elif minConfirmations == '۳ تعییدیه + فیبوناچی (۴ امتیاز) [Custom]':
                result = fibOk
            elif minConfirmations == '۳ تعییدیه + پرایس\u200cاکشن (۴ امتیاز) [Custom]':
                result = paOk
            elif minConfirmations == '۵ امتیاز کامل (ایده\u200cآل)':
                result = fibOk and paOk
        return result

    finalClassicBearish = passesMinRequirement(classicBearishBase3, fibScoreBearish, priceActionBearishAtPivot)
    finalClassicBullish = passesMinRequirement(classicBullishBase3, fibScoreBullish, priceActionBullishAtPivot)
    finalHiddenBullish = passesMinRequirement(hiddenBullishBase3, fibScoreBullish, priceActionBullishAtPivot)
    finalHiddenBearish = passesMinRequirement(hiddenBearishBase3, fibScoreBearish, priceActionBearishAtPivot)


    plotshape(finalClassicBearish, title='CD-', style=shape.triangledown, location=location.abovebar, color=color.red, size=size.small, text='CD-', offset=-rightBars)
    plotshape(finalClassicBullish, title='CD+', style=shape.triangleup, location=location.belowbar, color=color.green, size=size.small, text='CD+', offset=-rightBars)
    plotshape(finalHiddenBullish, title='HD+', style=shape.triangleup, location=location.belowbar, color=color.blue, size=size.small, text='HD+', offset=-rightBars)
    plotshape(finalHiddenBearish, title='HD-', style=shape.triangledown, location=location.abovebar, color=color.orange, size=size.small, text='HD-', offset=-rightBars)
    # ============================================================
    # DTM SIGNAL SNAPSHOT
    # Existing strategy calculations above are untouched.
    # This dictionary only exposes values ALREADY calculated here.
    # ============================================================
    return {
        "signal": ("LONG" if (finalClassicBullish or finalHiddenBullish) else "SHORT" if (finalClassicBearish or finalHiddenBearish) else None),
        "entry": close,

        "CD+": finalClassicBullish,
        "CD-": finalClassicBearish,
        "HD+": finalHiddenBullish,
        "HD-": finalHiddenBearish,

        # Indicators
        "rsi": rsiVal,
        "rsi_len": rsiLen,
        "macd_fast": macdFast,
        "macd_slow": macdSlow,
        "macd_signal_len": macdSig,
        "macd_line": macdLine,
        "macd_signal_line": signalLine,
        "macd_histogram": histLine,
        "atr": atr14,
        "atr_len": 14,

        # Trend
        "trend_lookback": trendLookback,
        "trend_slope_min_pct": trendSlopeMinPct,
        "trend_bearish_ok": trendOkForBearish,
        "trend_bullish_ok": trendOkForBullish,

        # Pivots
        "left_bars": leftBars,
        "right_bars": rightBars,
        "pivot_high": pivotHighPrice,
        "pivot_low": pivotLowPrice,
        "pivot_high_price": ph_price_2,
        "pivot_low_price": pl_price_2,
        "pivot_high_index": ph_bar_2,
        "pivot_low_index": pl_bar_2,
        "previous_pivot_high_price": ph_price_1,
        "previous_pivot_low_price": pl_price_1,
        "previous_pivot_high_index": ph_bar_1,
        "previous_pivot_low_index": pl_bar_1,

        # Divergence components
        "classic_bullish_base": classicBullishBase3,
        "classic_bearish_base": classicBearishBase3,
        "hidden_bullish_base": hiddenBullishBase3,
        "hidden_bearish_base": hiddenBearishBase3,

        "classic_bullish_rsi": classicBullishCond1_RSI,
        "classic_bullish_macd": classicBullishCond2_MACDl,
        "classic_bullish_hist": classicBullishCond3_MACDh,
        "classic_bearish_rsi": classicBearishCond1_RSI,
        "classic_bearish_macd": classicBearishCond2_MACDl,
        "classic_bearish_hist": classicBearishCond3_MACDh,

        "hidden_bullish_rsi": hiddenBullishCond1_RSI,
        "hidden_bullish_macd": hiddenBullishCond2_MACDl,
        "hidden_bullish_hist": hiddenBullishCond3_MACDh,
        "hidden_bearish_rsi": hiddenBearishCond1_RSI,
        "hidden_bearish_macd": hiddenBearishCond2_MACDl,
        "hidden_bearish_hist": hiddenBearishCond3_MACDh,

        "rsi_lower_high": rsiLowerHighOnPeaks,
        "rsi_higher_low": rsiHigherLowOnTroughs,
        "rsi_lower_low": rsiLowerLowOnTroughs,
        "rsi_higher_high": rsiHigherHighOnPeaks,

        "macd_lower_high": macdLineLowerHighOnPeaks,
        "macd_higher_low": macdLineHigherLowOnTroughs,
        "macd_lower_low": macdLineLowerLowOnTroughs,
        "macd_higher_high": macdLineHigherHighOnPeaks,

        # Fibonacci
        "fib_use_618": fibUse618,
        "fib_use_786": fibUse786,
        "fib_tolerance_pct": fibTolerancePct,
        "fib_search_bars": fibTrendSearchBars,
        "fib_bearish": fibScoreBearish,
        "fib_bullish": fibScoreBullish,

        # Price action
        "candle_range": candleRange,
        "candle_body": candleBody,
        "upper_shadow": upperShadow,
        "lower_shadow": lowerShadow,
        "avg_body": avgBody,
        "size_ok": sizeOk,
        "bullish_wick": bullishHammer,              # ← تغییر
        "bearish_wick": bearishShootingStar,       # ← تغییر
        "bearish_hanging_man": bearishLowerWickRejection,  # ← تغییر
        "big_green_candle": bullishLargeBody,      # ← تغییر
        "big_red_candle": bearishLargeBody,        # ← تغییر
        "price_action_bullish": priceActionBullish,
        "price_action_bearish": priceActionBearish,

        # Volume is not calculated by this strategy.
        "volume_analysis": False,

        # MTF is explicitly disabled by the current configuration.

        # Confirmation / decision trace
        "min_confirmations": minConfirmations,
        "minimum_requirement_bullish": passesMinRequirement(
            classicBullishBase3 or hiddenBullishBase3,
            fibScoreBullish,
            priceActionBullishAtPivot,
        ),
        "minimum_requirement_bearish": passesMinRequirement(
            classicBearishBase3 or hiddenBearishBase3,
            fibScoreBearish,
            priceActionBearishAtPivot,
        ),
        "final_classic_bullish": finalClassicBullish,
        "final_classic_bearish": finalClassicBearish,
        "final_hidden_bullish": finalHiddenBullish,
        "final_hidden_bearish": finalHiddenBearish,
        # ====== کلیدهای جدید برای دیباگ (اضافه شده) ======
        "ph_rsi_1": ph_rsi_1,
        "ph_rsi_2": ph_rsi_2,
        "ph_macdline_1": ph_macdline_1,
        "ph_macdline_2": ph_macdline_2,
        "ph_hist_1": ph_hist_1,
        "ph_hist_2": ph_hist_2,
        "pl_rsi_1": pl_rsi_1,
        "pl_rsi_2": pl_rsi_2,
        "pl_macdline_1": pl_macdline_1,
        "pl_macdline_2": pl_macdline_2,
        "pl_hist_1": pl_hist_1,
        "pl_hist_2": pl_hist_2,
        "both_peaks_green": bothPeaksGreen,
        "both_troughs_red": bothTroughsRed,
        "macd_color_changed_highs": macdColorChangedForHighs,
        "macd_color_changed_lows": macdColorChangedForLows,

        "prominence_high": prominenceHigh,
        "prominence_low": prominenceLow,
    }


# ============================================================
# WRAPPER — compatibility layer for bot.py
# Does NOT modify PyneCore strategy logic.
# ============================================================



if __name__ == "__main__":
    from pynecore.standalone import run
    run(__file__)
