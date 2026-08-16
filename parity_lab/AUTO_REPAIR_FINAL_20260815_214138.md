# DTM — AUTOMATIC PARITY REPAIR FINAL REPORT

Generated: 2026-08-15T21:42:58.938346

## RESULT

- Initial mismatch score: **8**
- Final mismatch score: **8**
- Changes applied: **0**
- Rollbacks: **0**

## ROOT CAUSES DETECTED

### [HIGH] PIVOT SOURCE/CONFIRMATION INDEX

- Evidence: strategy.py contains i+right pivot storage

### [HIGH] POSSIBLE SHIFT

- Evidence: strategy.py contains pandas shift()

### [CRITICAL] PINE/PYTHON OHLC MAPPING

- Evidence: 6 Pine pivot prices are not same-bar OHLC values

## FILES MODIFIED

No high-confidence source-code modification was performed.

## ROLLBACKS

- None

## FINAL DIAGNOSTIC

```text
31 offset=+12 time=2026-08-13 01:51:00+00:00 HIGH=44.83 diff=0.0

HD- | P1 Pine=44.96 bar=4596 time=2026-08-13 04:36:00+00:00
   P1 NEAREST: bar=4598 offset=+2 time=2026-08-13 04:38:00+00:00 HIGH=44.94 diff=0.020000000000003126
HD- | P2 Pine=44.95 bar=4606 time=2026-08-13 04:46:00+00:00
   P2 NEAREST: bar=4598 offset=-8 time=2026-08-13 04:38:00+00:00 HIGH=44.94 diff=0.010000000000005116

HD- | P1 Pine=44.73 bar=5025 time=2026-08-13 11:45:00+00:00
   P1 NEAREST: bar=5003 offset=-22 time=2026-08-13 11:23:00+00:00 LOW=44.73 diff=0.0
HD- | P2 Pine=44.71 bar=5037 time=2026-08-13 11:57:00+00:00
   P2 NEAREST: bar=5012 offset=-25 time=2026-08-13 11:32:00+00:00 LOW=44.71 diff=0.0

CD+ | P1 Pine=44.72 bar=5159 time=2026-08-13 13:59:00+00:00
   P1 NEAREST: bar=5161 offset=+2 time=2026-08-13 14:01:00+00:00 CLOSE=44.72 diff=0.0
CD+ | P2 Pine=44.66 bar=5168 time=2026-08-13 14:08:00+00:00
   P2 NEAREST: bar=5169 offset=+1 time=2026-08-13 14:09:00+00:00 LOW=44.65 diff=0.00999999999999801

------------------------------------------------------------------------------------------------------------------------
OFFSET SUMMARY
------------------------------------------------------------------------------------------------------------------------
P1 EXACT PRICE FOUND: 12 / 15
P2 EXACT PRICE FOUND: 11 / 15
P1 OFFSETS: [-7, -8, -10, -25, -11, -30, -22, 2, -9, -26, -4, 25]
P2 OFFSETS: [-9, 2, -20, -30, -14, 12, -25, -18, -9, -10, 24]

========================================================================================================================
DOGEUSDT
========================================================================================================================
SIGNALS: 17

------------------------------------------------------------------------------------------------------------------------
FIRST 10 PIVOT PRICE LOCATIONS
------------------------------------------------------------------------------------------------------------------------

HD+ | P1 Pine=0.07059 bar=2109 time=2026-08-11 11:09:00+00:00
   P1 NEAREST: bar=2123 offset=+14 time=2026-08-11 11:23:00+00:00 LOW=0.07059 diff=0.0
HD+ | P2 Pine=0.07061 bar=2122 time=2026-08-11 11:22:00+00:00
   P2 NEAREST: bar=2121 offset=-1 time=2026-08-11 11:21:00+00:00 HIGH=0.07061 diff=0.0

HD+ | P1 Pine=0.0726 bar=2770 time=2026-08-11 22:10:00+00:00
   P1 NEAREST: bar=2798 offset=+28 time=2026-08-11 22:38:00+00:00 CLOSE=0.072599 diff=1.000000000001e-06
HD+ | P2 Pine=0.07277 bar=2779 time=2026-08-11 22:19:00+00:00
   P2 NEAREST: bar=2780 offset=+1 time=2026-08-11 22:20:00+00:00 LOW=0.072775 diff=5.0000000000050004e-06

HD+ | P1 Pine=0.07218 bar=2936 time=2026-08-12 00:56:00+00:00
   P1 NEAREST: bar=2920 offset=-16 time=2026-08-12 00:40:00+00:00 LOW=0.072181 diff=1.000000000001e-06
HD+ | P2 Pine=0.07224 bar=2957 time=2026-08-12 01:17:00+00:00
   P2 NEAREST: bar=2976 offset=+19 time=2026-08-12 01:36:00+00:00 CLOSE=0.07224 diff=0.0

CD- | P1 Pine=0.07242 bar=3086 time=2026-08-12 03:26:00+00:00
   P1 NEAREST: bar=3097 offset=+11 time=2026-08-12 03:37:00+00:00 HIGH=0.072426 diff=6.0000000000060005e-06
CD- | P2 Pine=0.07248 bar=3097 time=2026-08-12 03:37:00+00:00
   P2 NEAREST: bar=3097 offset=+0 time=2026-08-12 03:37:00+00:00 HIGH=0.072426 diff=5.3999999999998494e-05

CD+ | P1 Pine=0.07182 bar=3625 time=2026-08-12 12:25:00+00:00
   P1 NEAREST: bar=3623 offset=-2 time=2026-08-12 12:23:00+00:00 LOW=0.071812 diff=7.999999999994123e-06
CD+ | P2 Pine=0.0717 bar=3630 time=2026-08-12 12:30:00+00:00
   P2 NEAREST: bar=3640 offset=+10 time=2026-08-12 12:40:00+00:00 LOW=0.071701 diff=1.000000000001e-06

CD- | P1 Pine=0.07098 bar=3858 time=2026-08-12 16:18:00+00:00
   P1 NEAREST: bar=3874 offset=+16 time=2026-08-12 16:34:00+00:00 HIGH=0.070945 diff=3.500000000000725e-05
CD- | P2 Pine=0.07099 bar=3874 time=2026-08-12 16:34:00+00:00
   P2 NEAREST: bar=3874 offset=+0 time=2026-08-12 16:34:00+00:00 HIGH=0.070945 diff=4.500000000000337e-05

HD+ | P1 Pine=0.07031 bar=4643 time=2026-08-13 05:23:00+00:00
   P1 NEAREST: bar=4627 offset=-16 time=2026-08-13 05:07:00+00:00 HIGH=0.07031 diff=0.0
HD+ | P2 Pine=0.07032 bar=4650 time=2026-08-13 05:30:00+00:00
   P2 NEAREST: bar=4638 offset=-12 time=2026-08-13 05:18:00+00:00 LOW=0.070319 diff=9.999999999871223e-07

HD- | P1 Pine=0.07051 bar=4860 time=2026-08-13 09:00:00+00:00
   P1 NEAREST: bar=4832 offset=-28 time=2026-08-13 08:32:00+00:00 HIGH=0.070511 diff=1.000000000001e-06
HD- | P2 Pine=0.07044 bar=4880 time=2026-08-13 09:20:00+00:00
   P2 NEAREST: bar=4905 offset=+25 time=2026-08-13 09:45:00+00:00 HIGH=0.07044 diff=0.0

HD- | P1 Pine=0.07021 bar=4943 time=2026-08-13 10:23:00+00:00
   P1 NEAREST: bar=4926 offset=-17 time=2026-08-13 10:06:00+00:00 LOW=0.070217 diff=7.000000000007001e-06
HD- | P2 Pine=0.07015 bar=4964 time=2026-08-13 10:44:00+00:00
   P2 NEAREST: bar=4934 offset=-30 time=2026-08-13 10:14:00+00:00 LOW=0.07015 diff=0.0

HD+ | P1 Pine=0.06985 bar=5377 time=2026-08-13 17:37:00+00:00
   P1 NEAREST: bar=5369 offset=-8 time=2026-08-13 17:29:00+00:00 CLOSE=0.06985 diff=0.0
HD+ | P2 Pine=0.06987 bar=5401 time=2026-08-13 18:01:00+00:00
   P2 NEAREST: bar=5371 offset=-30 time=2026-08-13 17:31:00+00:00 HIGH=0.06987 diff=0.0

------------------------------------------------------------------------------------------------------------------------
OFFSET SUMMARY
------------------------------------------------------------------------------------------------------------------------
P1 EXACT PRICE FOUND: 7 / 17
P2 EXACT PRICE FOUND: 10 / 17
P1 OFFSETS: [14, -16, -8, 21, -11, -30, -30]
P2 OFFSETS: [-1, 19, 25, -30, -30, -1, 19, -19, 6, -5]

========================================================================================================================
ETHUSDT
========================================================================================================================
SIGNALS: 32

------------------------------------------------------------------------------------------------------------------------
FIRST 10 PIVOT PRICE LOCATIONS
------------------------------------------------------------------------------------------------------------------------

CD+ | P1 Pine=1898.04 bar=873 time=2026-08-10 14:33:00+00:00
   P1 NEAREST: bar=852 offset=-21 time=2026-08-10 14:12:00+00:00 LOW=1898.02 diff=0.01999999999998181
CD+ | P2 Pine=1897.38 bar=879 time=2026-08-10 14:39:00+00:00
   P2 NEAREST: bar=889 offset=+10 time=2026-08-10 14:49:00+00:00 HIGH=1897.36 diff=0.020000000000209184

HD- | P1 Pine=1874.79 bar=1087 time=2026-08-10 18:07:00+00:00
   P1 NEAREST: bar=1070 offset=-17 time=2026-08-10 17:50:00+00:00 HIGH=1874.85 diff=0.05999999999994543
HD- | P2 Pine=1874.54 bar=1106 time=2026-08-10 18:26:00+00:00
   P2 NEAREST: bar=1080 offset=-26 time=2026-08-10 18:00:00+00:00 HIGH=1874.02 diff=0.5199999999999818

CD- | P1 Pine=1877.85 bar=1513 time=2026-08-11 01:13:00+00:00
   P1 NEAREST: bar=1524 offset=+11 time=2026-08-11 01:24:00+00:00 HIGH=1878.04 diff=0.19000000000005457
CD- | P2 Pine=1878.57 bar=1524 time=2026-08-11 01:24:00+00:00
   P2 NEAREST: bar=1524 offset=+0 time=2026-08-11 01:24:00+00:00 HIGH=1878.04 diff=0.5299999999999727

HD+ | P1 Pine=1873.9 bar=1520 time=2026-08-11 01:20:00+00:00
   P1 NEAREST: bar=1507 offset=-13 time=2026-08-11 01:07:00+00:00 LOW=1873.93 diff=0.029999999999972715
HD+ | P2 Pine=1874.25 bar=1542 time=2026-08-11 01:42:00+00:00
   P2 NEAREST: bar=1515 offset=-27 time=2026-08-11 01:15:00+00:00 LOW=1874.28 diff=0.029999999999972715

HD+ | P1 Pine=1877.7 bar=1567 time=2026-08-11 02:07:00+00:00
   P1 NEAREST: bar=1572 offset=+5 time=2026-08-11 02:12:00+00:00 CLOSE=1877.7 diff=0.0
HD+ | P2 Pine=1878.03 bar=1575 time=2026-08-11 02:15:00+00:00
   P2 NEAREST: bar=1561 offset=-14 time=2026-08-11 02:01:00+00:00 HIGH=1878.02 diff=0.009999999999990905

CD- | P1 Pine=1880.44 bar=1633 time=2026-08-11 03:13:00+00:00
   P1 NEAREST: bar=1643 offset=+10 time=2026-08-11 03:23:00+00:00 HIGH=1880.48 diff=0.03999999999996362
CD- | P2 Pine=1881.22 bar=1639 time=2026-08-11 03:19:00+00:00
   P2 NEAREST: bar=1660 offset=+21 time=2026-08-11 03:40:00+00:00 HIGH=1880.84 diff=0.38000000000010914

HD+ | P1 Pine=1879.61 bar=1636 time=2026-08-11 03:16:00+00:00
   P1 NEAREST: bar=1642 offset=+6 time=2026-08-11 03:22:00+00:00 HIGH=1879.6 diff=0.009999999999990905
HD+ | P2 Pine=1879.74 bar=1642 time=2026-08-11 03:22:00+00:00
   P2 NEAREST: bar=1669 offset=+27 time=2026-08-11 03:49:00+00:00 HIGH=1879.72 diff=0.01999999999998181

HD+ | P1 Pine=1879.74 bar=1642 time=2026-08-11 03:22:00+00:00
   P1 NEAREST: bar=1669 offset=+27 time=2026-08-11 03:49:00+00:00 HIGH=1879.72 diff=0.01999999999998181
HD+ | P2 Pine=1880.22 bar=1651 time=2026-08-11 03:31:00+00:00
   P2 NEAREST: bar=1678 offset=+27 time=2026-08-11 03:58:00+00:00 HIGH=1880.22 diff=0.0

CD- | P1 Pine=1881.29 bar=1647 time=2026-08-11 03:27:00+00:00
   P1 NEAREST: bar=1660 offset=+13 time=2026-08-11 03:40:00+00:00 HIGH=1880.84 diff=0.4500000000000455
CD- | P2 Pine=1881.78 bar=1660 time=2026-08-11 03:40:00+00:00
   P2 NEAREST: bar=1682 offset=+22 time=2026-08-11 04:02:00+00:00 HIGH=1881.17 diff=0.6099999999999

HD+ | P1 Pine=1891.0 bar=2117 time=2026-08-11 11:17:00+00:00
   P1 NEAREST: bar=2109 offset=-8 time=2026-08-11 11:09:00+00:00 LOW=1891.0 diff=0.0
HD+ | P2 Pine=1891.46 bar=2124 time=2026-08-11 11:24:00+00:00
   P2 NEAREST: bar=2122 offset=-2 time=2026-08-11 11:22:00+00:00 CLOSE=1891.45 diff=0.009999999999990905

------------------------------------------------------------------------------------------------------------------------
OFFSET SUMMARY
------------------------------------------------------------------------------------------------------------------------
P1 EXACT PRICE FOUND: 6 / 32
P2 EXACT PRICE FOUND: 4 / 32
P1 OFFSETS: [5, -8, -2, -8, -4, -19]
P2 OFFSETS: [27, -2, -12, 5]

========================================================================================================================
LOCATOR FINISHED
========================================================================================================================

====================================================================================================
PINE <-> BINANCE SPOT RAW OHLC DIAGNOSTIC
====================================================================================================

====================================================================================================
BNBUSDT
====================================================================================================
Traceback (most recent call last):
  File "/data/data/com.termux/files/home/dtm-new-bot/parity_lab/fast_spot_check.py", line 35, in <module>
    raw = pd.read_csv(
        RAW[symbol],
        usecols=["time", "open", "high", "low", "close"]
    )
  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pandas/io/parsers/readers.py", line 873, in read_csv
    return _read(filepath_or_buffer, kwds)
  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pandas/io/parsers/readers.py", line 300, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pandas/io/parsers/readers.py", line 1645, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pandas/io/parsers/readers.py", line 1904, in _make_engine
    self.handles = get_handle(
                   ~~~~~~~~~~^
        f,
        ^^
    ...<6 lines>...
        storage_options=self.options.get("storage_options", None),
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/data/data/com.termux/files/usr/lib/python3.14/site-packages/pandas/io/common.py", line 930, in get_handle
    handle = open(
        handle,
    ...<3 lines>...
        newline="",
    )
FileNotFoundError: [Errno 2] No such file or directory: 'parity_lab/raw_data/BNBUSDT_1m_binance_spot.csv'

```

## BACKUP

/data/data/com.termux/files/home/dtm-new-bot/parity_lab/AUTO_REPAIR_BACKUP_20260815_214138

## IMPORTANT

The engine intentionally refuses blind pivot/timestamp rewrites when the available evidence does not mathematically prove the correct replacement.