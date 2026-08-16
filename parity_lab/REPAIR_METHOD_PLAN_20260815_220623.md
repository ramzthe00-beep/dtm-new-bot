# DTM — COMPLETE PINE ↔ PYTHON REPAIR METHOD PLAN

Generated: 2026-08-15T22:06:24.186158

## دستور اصلی

بر اساس COMPLETE_DTM_PARITY_ANALYSIS.txt، هدف این سند تعیین روش اصلاح ریشه‌ای اختلاف Pine و Python است؛ نه اصلاح ظاهری خروجی.

### قوانین غیرقابل‌مذاکره

1. Pine Script مرجع نهایی رفتار است.
2. هیچ تابع یا پارامتری بدون بررسی semantics آن تغییر نکند.
3. timestamp، bar identity، source bar و confirmation bar کاملاً جدا باشند.
4. هیچ `shift()` یا `+right`/`-right` بدون اثبات دقیق وارد یا حذف نشود.
5. state persistence باید دقیقاً با state Pine تطبیق داده شود.
6. RMA/EMA/RSI/MACD/ATR باید bar-by-bar مقایسه شوند.
7. Pivot باید قبل از divergence، Fibonacci، scoring و signal به 100% parity برسد.
8. هر اصلاح باید قبل/بعد با تست parity مقایسه شود.
9. اگر اصلاح نتیجه را بدتر کرد، rollback شود.
10. هیچ API، Telegram، order execution یا risk-management بدون ارتباط اثبات‌شده با خطای parity تغییر نکند.

## ANALYSIS EVIDENCE

فایل تحلیل اصلی:
`/data/data/com.termux/files/home/dtm-new-bot/parity_lab/COMPLETE_DTM_PARITY_ANALYSIS.txt`

### مهم‌ترین شواهد موجود

- **PRIMARY ROOT CAUSE: PIVOT / INDEXING / STATE**
- Pivot identity is upstream of divergence, Fibonacci, scoring and final signals. If pivot source/confirmation indexing is wrong, every downstream signal can move or disappear.
- ### 1. [HIGH] PIVOT INDEX
- **Problem:** Pivot value is stored on confirmation bar
- **Likely cause:** This can be correct only if every downstream consumer treats the value as a confirmed pivot while preserving source-bar identity. Mixing source and confirmation indices causes systematic shift.
- **Required correction:** Keep source index and confirmation index explicitly separate. Never apply another right-bar shift later.
- ### 2. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 3. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 4. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 5. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 6. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 7. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 8. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 9. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 10. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 11. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 12. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 13. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 14. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 15. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 16. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 17. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 18. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 19. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 20. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 21. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 22. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 23. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 24. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 25. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 26. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 27. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 28. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 29. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 30. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 31. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 32. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 33. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 34. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 35. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 36. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 37. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 38. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 39. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 40. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 41. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 42. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 43. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 44. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 45. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 46. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 47. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 48. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 49. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 50. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 51. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 52. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 53. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 54. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 55. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 56. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 57. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 58. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 59. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 60. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 61. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 62. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 63. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 64. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 65. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 66. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 67. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 68. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 69. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 70. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 71. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 72. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 73. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 74. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 75. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 76. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 77. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 78. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 79. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 80. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 81. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 82. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 83. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 84. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 85. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 86. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 87. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 88. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 89. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 90. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 91. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 92. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 93. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 94. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 95. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 96. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 97. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 98. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 99. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 100. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 101. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 102. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 103. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 104. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 105. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 106. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 107. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 108. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 109. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 110. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 111. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 112. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 113. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 114. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 115. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 116. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 117. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 118. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 119. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 120. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 121. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 122. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 123. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 124. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 125. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 126. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 127. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 128. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 129. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 130. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 131. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 132. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 133. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 134. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 135. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 136. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 137. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 138. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 139. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 140. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 141. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 142. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 143. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 144. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 145. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 146. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 147. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 148. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 149. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 150. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 151. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 152. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 153. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 154. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 155. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 156. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 157. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 158. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 159. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 160. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 161. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 162. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 163. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 164. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 165. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 166. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 167. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 168. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 169. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 170. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- ### 171. [CRITICAL] PIVOT PARITY
- **Problem:** Pivot mismatch detected in parity result
- **Likely cause:** Python pivot source/confirmation/state does not match Pine for at least one bar.
- **Required correction:** Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%.
- 1. Verify exact timestamp/bar identity.
- 2. Verify Pine pivot source bar versus confirmation bar.
- 3. Verify pivot state persistence and eliminate any second shift.
- 4. Re-run pivot parity until it is 100%.
- 5. Compare RMA/EMA/RSI/MACD per bar.
- 6. Compare divergence inputs.
- 7. Compare Fibonacci and candle filters.
- ===== PIVOT PRICE MISMATCH FORENSIC =====
- 78-FIRST 10 PIVOT PRICE LOCATIONS
- 82-   P1 NEAREST: bar=885 offset=+8 time=2026-08-10 14:45:00+00:00 HIGH=45.54 diff=0.00999999999999801
- 84-   P2 NEAREST: bar=885 offset=+2 time=2026-08-10 14:45:00+00:00 HIGH=45.54 diff=0.020000000000003126
- 87-   P1 NEAREST: bar=1560 offset=-7 time=2026-08-11 02:00:00+00:00 HIGH=45.27 diff=0.0
- 89-   P2 NEAREST: bar=1565 offset=-9 time=2026-08-11 02:05:00+00:00 HIGH=45.28 diff=0.0
- 145-FIRST 10 PIVOT PRICE LOCATIONS
- 151-   P2 NEAREST: bar=2121 offset=-1 time=2026-08-11 11:21:00+00:00 HIGH=0.07061 diff=0.0
- 196-   P2 NEAREST: bar=5371 offset=-30 time=2026-08-13 17:31:00+00:00 HIGH=0.06987 diff=0.0
- 212-FIRST 10 PIVOT PRICE LOCATIONS
- 218-   P2 NEAREST: bar=889 offset=+10 time=2026-08-10 14:49:00+00:00 HIGH=1897.36 diff=0.020000000000209184
- 221-   P1 NEAREST: bar=1070 offset=-17 time=2026-08-10 17:50:00+00:00 HIGH=1874.85 diff=0.05999999999994543
- 223-   P2 NEAREST: bar=1080 offset=-26 time=2026-08-10 18:00:00+00:00 HIGH=1874.02 diff=0.5199999999999818
- 226-   P1 NEAREST: bar=1524 offset=+11 time=2026-08-11 01:24:00+00:00 HIGH=1878.04 diff=0.19000000000005457
- PIVOT SAME-BAR FORENSIC
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- HEADER: ['time', 'open', 'high', 'low', 'close', 'volume']
- This test determines whether Pine pivot price exists in OHLC of the SAME Pine pivot bar.
- HIGH       : 45.52
- HIGH DIFF  : 0.02999999999999403
- RESULT     : PINE PRICE IS NOT SAME-BAR HIGH/LOW
- HIGH       : 45.53
- HIGH DIFF  : 0.030000000000001137
- RESULT     : PINE PRICE IS NOT SAME-BAR HIGH/LOW
- HIGH       : 0.070601
- HIGH DIFF  : -1.0999999999997123e-05
- RESULT     : PINE PRICE IS NOT SAME-BAR HIGH/LOW
- HIGH       : 0.070649
- HIGH DIFF  : -3.899999999999737e-05
- RESULT     : PINE PRICE IS NOT SAME-BAR HIGH/LOW
- HIGH       : 1897.93
- HIGH DIFF  : 0.10999999999989996
- RESULT     : PINE PRICE IS NOT SAME-BAR HIGH/LOW
- HIGH       : 1898
- HIGH DIFF  : -0.6199999999998909
- RESULT     : PINE PRICE IS NOT SAME-BAR HIGH/LOW
- REPORT: parity_lab/PIVOT_SAME_BAR_FORENSIC.txt
- - `parity_lab/pine_timestamp_ohlc_check.py` (7384 bytes)
- - `parity_lab/pine_pivot_price_locator.py` (5090 bytes)
- 2. PIVOT / STATE / SHIFT STATIC ANALYSIS
- ### SEARCH: `pivot`
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:105:    ph = pivot_high(high)
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:106:    pl = pivot_low(low)
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:34:    LAB / "pine_pivot_price_locator.py",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:124:        "PIVOT MISMATCH": 30,
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:249:samebar_file = LAB / "PIVOT_SAME_BAR_FORENSIC.txt"
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:250:locator_file = LAB / "PIVOT_PRICE_FORENSIC.txt"
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:281:        "Pine pivot price does not map to same-timestamp OHLC."
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:289:        "strategy.py stores pivot value using confirmation-bar indexing."
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:302:if "pivot_state" in combined:
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:304:        "Pivot state persistence is present."
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:379:# PIVOT SEMANTICS REPAIR
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:383:say("[5] PIVOT SOURCE/CONFIRMATION FORENSICS")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:394:# Find pivot functions.
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:395:pivot_functions = re.findall(
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:396:    r"def\s+pivot_(?:high|low)\s*\([^)]*\):.*?(?=\ndef\s+|\Z)",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:401:for fn in pivot_functions:
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:404:    say("[PIVOT FUNCTION FOUND]")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:413:# SEARCH ALL PYTHON FOR SECONDARY PIVOT SHIFTS
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:417:say("[6] SEARCHING FOR SECONDARY PIVOT SHIFTS")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:439:            "pivot" in low
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:449:                f"[PIVOT TRACE] "
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:467:say(f"NON-SAME-BAR PIVOTS = {len(not_same)}")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:474:say("[8] PIVOT PRICE OFFSET ANALYSIS")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:556:        "pivot_state",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:585:        "pivot",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:701:report.append("## PIVOT FORENSICS")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:704:    "The engine does NOT assume that Pine pivot price must equal "
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:705:    "the High/Low of the candle carrying the logged pivot timestamp."
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:105:    ph = pivot_high(high)
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:106:    pl = pivot_low(low)
- ./parity_lab/AUTO_REPAIR_ALL.py:29:    LAB / "pine_pivot_price_locator.py",
- ./parity_lab/AUTO_REPAIR_ALL.py:211:        "name": "PIVOT SOURCE/CONFIRMATION INDEX",
- ./parity_lab/AUTO_REPAIR_ALL.py:213:        "evidence": "strategy.py contains i+right pivot storage",
- ./parity_lab/AUTO_REPAIR_ALL.py:223:if "pivot_state" in combined:
- ./parity_lab/AUTO_REPAIR_ALL.py:225:        "name": "PIVOT STATE",
- ./parity_lab/AUTO_REPAIR_ALL.py:227:        "evidence": "pivot_state detected",
- ./parity_lab/AUTO_REPAIR_ALL.py:244:samebar = LAB / "PIVOT_SAME_BAR_FORENSIC.txt"
- ./parity_lab/AUTO_REPAIR_ALL.py:263:            "evidence": f"{n} Pine pivot prices are not same-bar OHLC values",
- ./parity_lab/AUTO_REPAIR_ALL.py:328:# Preserve pivot source/confirmation identity.
- ./parity_lab/AUTO_REPAIR_ALL.py:343:        # Pine pivot confirmation semantics require the
- ./parity_lab/AUTO_REPAIR_ALL.py:345:        say("[CHECKED] pivot storage i+right")
- ./parity_lab/AUTO_REPAIR_ALL.py:354:say("[KEPT] No blind timestamp rewrite because Pine pivot price was proven not to equal same-bar OHLC")
- ./parity_lab/AUTO_REPAIR_ALL.py:485:    "The engine intentionally refuses blind pivot/timestamp rewrites "
- ./parity_lab/auto_parity_auditor.py:76:# Pivot settings
- ./parity_lab/auto_parity_auditor.py:88:        "HIGH", "PIVOT",
- ./parity_lab/auto_parity_auditor.py:91:        "Pivot window is not identical to Pine configuration",
- ./parity_lab/auto_parity_auditor.py:97:        "HIGH", "PIVOT",
- ./parity_lab/auto_parity_auditor.py:100:        "Pivot confirmation window differs",
- ./parity_lab/auto_parity_auditor.py:107:        "HIGH", "PIVOT INDEX",
- ./parity_lab/auto_parity_auditor.py:108:        "Pivot value is stored on confirmation bar",
- ./parity_lab/auto_parity_auditor.py:110:        "This can be correct only if every downstream consumer treats the value as a confirmed pivot while preserving source-bar identity. Mixing source and confirmation indices causes systematic shift.",
- ./parity_lab/auto_parity_auditor.py:121:    (r'pivot_state', "pivot state"),
- ./parity_lab/auto_parity_auditor.py:257:            "Indicator and pivot parity cannot be guaranteed without identical OHLC.",
- ./parity_lab/auto_parity_auditor.py:262:# 6. PIVOT PARITY RESULTS
- ./parity_lab/auto_parity_auditor.py:266:print("[6/9] PIVOT PARITY RESULTS")
- ./parity_lab/auto_parity_auditor.py:268:pivot_results = sorted((LAB / "results").glob("*pivot*parity*.csv"))
- ./parity_lab/auto_parity_auditor.py:270:if not pivot_results:
- ./parity_lab/auto_parity_auditor.py:272:        "CRITICAL", "PIVOT PARITY",
- ./parity_lab/auto_parity_auditor.py:273:        "No pivot parity result was found",
- ./parity_lab/auto_parity_auditor.py:274:        "No *pivot*parity*.csv",
- ./parity_lab/auto_parity_auditor.py:275:        "The current evidence cannot prove Pine and Python pivot identity.",
- ./parity_lab/auto_parity_auditor.py:276:        "Run the pivot parity generator before modifying trading logic."
- ./parity_lab/auto_parity_auditor.py:279:    for f in pivot_results:
- ./parity_lab/auto_parity_auditor.py:305:                            "CRITICAL", "PIVOT PARITY",
- ./parity_lab/auto_parity_auditor.py:306:                            "Pivot mismatch detected in parity result",
- ./parity_lab/auto_parity_auditor.py:308:                            "Python pivot source/confirmation/state does not match Pine for at least one bar.",
- ./parity_lab/auto_parity_auditor.py:309:                            "Fix pivot source-bar versus confirmation-bar indexing first. Do not modify signal scoring until pivot parity reaches 100%."
- ./parity_lab/auto_parity_auditor.py:340:    "PIVOT": 0,
- ./parity_lab/auto_parity_auditor.py:345:    "PIVOT INDEX": 0,
- ./parity_lab/auto_parity_auditor.py:346:    "PIVOT PARITY": 0,
- ./parity_lab/auto_parity_auditor.py:358:if categories["PIVOT PARITY"] or categories["PIVOT INDEX"] or categories["PIVOT"]:
- ./parity_lab/auto_parity_auditor.py:359:    root = "PIVOT / INDEXING / STATE"
- ./parity_lab/auto_parity_auditor.py:361:        "Pivot identity is upstream of divergence, Fibonacci, scoring and final signals. "
- ./parity_lab/auto_parity_auditor.py:362:        "If pivot source/confirmation indexing is wrong, every downstream signal can move or disappear."
- ./parity_lab/auto_parity_auditor.py:418:        "2. Verify Pine pivot source bar versus confirmation bar.",
- ./parity_lab/auto_parity_auditor.py:419:        "3. Verify pivot state persistence and eliminate any second shift.",
- ./parity_lab/auto_parity_auditor.py:420:        "4. Re-run pivot parity until it is 100%.",
- ./parity_lab/deep_analyzer.py:58:# 2. Exact pivot/state/shift search
- ./parity_lab/deep_analyzer.py:61:report.append(section("2. PIVOT / STATE / SHIFT STATIC ANALYSIS"))
- ./parity_lab/deep_analyzer.py:64:    "pivot",
- ./parity_lab/deep_analyzer.py:66:    "pivot_state",
- ./parity_lab/deep_analyzer.py:71:    "pivothigh",
- ./parity_lab/deep_analyzer.py:72:    "pivotlow",
- ./parity_lab/deep_analyzer.py:216:# 7. Pivot implementation mathematical inspection
- ./parity_lab/deep_analyzer.py:219:report.append(section("7. PIVOT MATHEMATICAL INSPECTION"))
- ./parity_lab/deep_analyzer.py:229:        "pivot_high_storage": r"out\.iloc\[i\+right\]\s*=",
- ./parity_lab/deep_analyzer.py:230:        "pivot_low_storage": r"out\.iloc\[i\+right\]\s*=",
- ./parity_lab/deep_analyzer.py:234:        "state_usage": r"pivot_state|_pine_load_previous_state",
- ./parity_lab/deep_analyzer.py:246:1. Pivot source bar
- ./parity_lab/deep_analyzer.py:247:2. Pivot confirmation bar
- ./parity_lab/deep_analyzer.py:250:5. Previous-pivot location
- ./parity_lab/deep_analyzer.py:270:    "parity_lab/pine_pivot_price_locator.py",
- ./parity_lab/deep_analyzer.py:314:P0 — PIVOT INDEXING / CONFIRMATION SEMANTICS
- ./parity_lab/deep_analyzer.py:355:→ PIVOT SOURCE/CONFIRMATION
- ./parity_lab/deep_analyzer.py:356:→ PIVOT STATE
- ./parity_lab/pine_pivot_price_locator.py:22:    r"Pivot اول:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
- ./parity_lab/pine_pivot_price_locator.py:25:    r"Pivot دوم:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
- ./parity_lab/pine_pivot_price_locator.py:61:print("PINE PIVOT PRICE LOCATOR")
- ./parity_lab/pine_pivot_price_locator.py:136:    print("FIRST 10 PIVOT PRICE LOCATIONS")
- ./parity_lab/pine_timestamp_ohlc_check.py:21:    r"Pivot اول:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
- ./parity_lab/pine_timestamp_ohlc_check.py:24:    r"Pivot دوم:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)"
- ./parity_lab/pine_timestamp_ohlc_check.py:28:print("PINE TIMESTAMP → RAW OHLC EXACT PIVOT TEST")
- ./parity_lab/fast_spot_check.py:22:P1 = re.compile(r"Pivot اول:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)")
- ./parity_lab/fast_spot_check.py:23:P2 = re.compile(r"Pivot دوم:\s*قیمت\s*([0-9.]+)\s*@\s*کندل\s*(\d+)")
- ./strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./strategy.py:105:    ph = pivot_high(high)
- ./strategy.py:106:    pl = pivot_low(low)
- ### SEARCH: `_pine_load_previous_state`
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:307:if "_pine_load_previous_state" in combined:
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:557:        "_pine_load_previous_state",
- ./parity_lab/AUTO_REPAIR_ALL.py:230:if "_pine_load_previous_state" in combined:
- ./parity_lab/AUTO_REPAIR_ALL.py:234:        "evidence": "_pine_load_previous_state detected",
- ./parity_lab/auto_parity_auditor.py:120:    (r'_pine_load_previous_state', "previous Pine state loader"),
- ./parity_lab/deep_analyzer.py:65:    "_pine_load_previous_state",
- ./parity_lab/deep_analyzer.py:234:        "state_usage": r"pivot_state|_pine_load_previous_state",
- ### SEARCH: `pivot_state`
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:302:if "pivot_state" in combined:
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:556:        "pivot_state",
- ./parity_lab/AUTO_REPAIR_ALL.py:223:if "pivot_state" in combined:
- ./parity_lab/AUTO_REPAIR_ALL.py:227:        "evidence": "pivot_state detected",
- ./parity_lab/auto_parity_auditor.py:121:    (r'pivot_state', "pivot state"),
- ./parity_lab/deep_analyzer.py:66:    "pivot_state",
- ./parity_lab/deep_analyzer.py:234:        "state_usage": r"pivot_state|_pine_load_previous_state",
- ### SEARCH: `bar_index`
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/dtm_bot.py:27:    bar_index, barmerge, close, color, high, input, location, low, math, na,
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/dtm_bot.py:27:    bar_index, barmerge, close, color, high, input, location, low, math, na,
- ./parity_lab/auto_parity_auditor.py:122:    (r'bar_index', "bar_index"),
- ./parity_lab/deep_analyzer.py:67:    "bar_index",
- ./parity_lab/deep_analyzer.py:233:        "bar_index_usage": r"bar_index",
- ./dtm_bot.py:27:    bar_index, barmerge, close, color, high, input, location, low, math, na,
- ### SEARCH: `shift`
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:74:    prev_close = close.shift(1)
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:292:if ".shift(" in source_text().get(
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:297:        "strategy.py contains explicit pandas shift operation."
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:333:    # Remove only an EXPLICIT second RIGHT_BARS shift.
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:341:        "Remove explicit double RIGHT_BARS shift.",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:347:        "Remove explicit 2*RIGHT_BARS shift.",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:369:        say("[CANDIDATE] Explicit double-shift correction")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:410:    # Instead check whether caller later shifts it again.
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:413:# SEARCH ALL PYTHON FOR SECONDARY PIVOT SHIFTS
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:417:say("[6] SEARCHING FOR SECONDARY PIVOT SHIFTS")
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:441:                "shift(" in low
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:509:            "[FINDING] Offsets are not a constant shift. "
- ./parity_lab/AUTO_REPAIR_ALL.py:216:if ".shift(" in strategy_text:
- ./parity_lab/AUTO_REPAIR_ALL.py:218:        "name": "POSSIBLE SHIFT",
- ./parity_lab/AUTO_REPAIR_ALL.py:220:        "evidence": "strategy.py contains pandas shift()",
- ./parity_lab/AUTO_REPAIR_ALL.py:275:# Fix accidental SECOND right-bar shift only.
- ./parity_lab/AUTO_REPAIR_ALL.py:285:    # Detect explicit double shift patterns.
- ./parity_lab/AUTO_REPAIR_ALL.py:324:            say("[FIXED] Explicit double RIGHT_BARS shift")
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:74:    prev_close = close.shift(1)
- ./parity_lab/auto_parity_auditor.py:104:# Detect storage shift
- ./parity_lab/auto_parity_auditor.py:110:        "This can be correct only if every downstream consumer treats the value as a confirmed pivot while preserving source-bar identity. Mixing source and confirmation indices causes systematic shift.",
- ./parity_lab/auto_parity_auditor.py:111:        "Keep source index and confirmation index explicitly separate. Never apply another right-bar shift later."
- ./parity_lab/auto_parity_auditor.py:114:# Detect pandas shift
- ./parity_lab/auto_parity_auditor.py:115:if re.search(r'\.shift\s*\(', strategy_text):
- ./parity_lab/auto_parity_auditor.py:116:    print("  [INFO] pandas shift() detected")
- ./parity_lab/auto_parity_auditor.py:419:        "3. Verify pivot state persistence and eliminate any second shift.",
- ./strategy.py:74:    prev_close = close.shift(1)
- ./parity_lab/deep_analyzer.py:58:# 2. Exact pivot/state/shift search
- ./parity_lab/deep_analyzer.py:61:report.append(section("2. PIVOT / STATE / SHIFT STATIC ANALYSIS"))
- ./parity_lab/deep_analyzer.py:68:    "shift",
- ./parity_lab/deep_analyzer.py:232:        "shift_usage": r"\.shift\s*\(",
- ./parity_lab/deep_analyzer.py:315:P0 — STATE RESTORATION / DOUBLE SHIFT
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:333:    # Remove only an EXPLICIT second RIGHT_BARS shift.
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:341:        "Remove explicit double RIGHT_BARS shift.",
- ./parity_lab/FORENSIC_AUTO_REPAIR.py:347:        "Remove explicit 2*RIGHT_BARS shift.",
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/AUTO_REPAIR_ALL.py:324:            say("[FIXED] Explicit double RIGHT_BARS shift")
- ./strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/FORENSIC_BACKUP_20260815_214452/strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./parity_lab/AUTO_REPAIR_BACKUP_20260815_214138/strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ./strategy.py:78:def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- ./strategy.py:87:def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- ### SEARCH: `pivothigh`
- ./parity_lab/deep_analyzer.py:71:    "pivothigh",
- ### SEARCH: `pivotlow`
- ./parity_lab/deep_analyzer.py:72:    "pivotlow",
- 0010: RSI_LEN = 14
- 0011: MACD_FAST = 12
- 0012: MACD_SLOW = 26
- 0013: MACD_SIG = 9
- 0015: def rma(s, length):
- 0016:     out = pd.Series(np.nan, index=s.index)
- 0034: def ema(s, length):
- 0035:     out = pd.Series(np.nan, index=s.index)
- 0053: def rsi(close, length=RSI_LEN):
- 0057:     ag = rma(gain, length)
- 0058:     al = rma(loss, length)
- 0065: def macd(close, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIG):
- 0066:     ef = ema(close, fast)
- 0067:     es = ema(close, slow)
- 0069:     sig = ema(line, signal)
- 0073: def atr(high, low, close, length=14):
- 0074:     prev_close = close.shift(1)
- 0075:     tr = pd.concat([high - low, (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
- 0076:     return rma(tr, length)
- 0078: def pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS):
- 0079:     out = pd.Series(np.nan, index=high.index, dtype=float)
- 0080:     n = len(high)
- 0082:         x = high.iloc[i]
- 0083:         if high.iloc[i-left:i].max() < x and high.iloc[i+1:i+right+1].max() < x:
- 0087: def pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS):
- 0088:     out = pd.Series(np.nan, index=low.index, dtype=float)
- 0098:     high = df['high']
- 0101:     rsi_val = rsi(close)
- 0102:     macd_line, signal_line, hist_line = macd(close)
- 0103:     atr_val = atr(high, low, close)
- 0105:     ph = pivot_high(high)
- 0106:     pl = pivot_low(low)
- 0120:         prev_ph_idx = ph_prev.index[-1]
- 0124:         price_higher_high = curr_ph_price > prev_ph_price
- 0125:         rsi_lower = rsi_val.iloc[last_confirmed] < rsi_val.loc[prev_ph_idx]
- 0126:         macd_lower = macd_line.iloc[last_confirmed] < macd_line.loc[prev_ph_idx]
- 0131:         start = df.index.get_loc(prev_ph_idx) + 1
- 0132:         end = df.index.get_loc(ph.index[last_confirmed])
- 0138:         if price_higher_high and rsi_lower and macd_lower and hist_lower and both_green and color_changed:
- 0142:         prev_pl_idx = pl_prev.index[-1]
- 0147:         rsi_higher = rsi_val.iloc[last_confirmed] > rsi_val.loc[prev_pl_idx]
- 0148:         macd_higher = macd_line.iloc[last_confirmed] > macd_line.loc[prev_pl_idx]
- 0149:         hist_higher = hist_line.iloc[last_confirmed] > hist_line.loc[prev_pl_idx]
- 0153:         start = df.index.get_loc(prev_pl_idx) + 1
- 0154:         end = df.index.get_loc(pl.index[last_confirmed])
- 0160:         if price_lower_low and rsi_higher and macd_higher and hist_higher and both_red and color_changed:
- 5. TIMESTAMP / INDEX / BAR ALIGNMENT ANALYSIS
- 6. NUMERIC PRECISION / OHLC ANALYSIS
- 7. PIVOT MATHEMATICAL INSPECTION
- - `pivot_high_storage` → **FOUND**
- - `pivot_low_storage` → **FOUND**
- - `shift_usage` → **FOUND**
- - `bar_index_usage` → **NOT FOUND**
- - `state_usage` → **NOT FOUND**
- 1. Pivot source bar
- 2. Pivot confirmation bar
- 5. Previous-pivot location
- 6. State-restored location
- series semantics exactly.
- ## `parity_lab/pine_pivot_price_locator.py`
- PINE PIVOT PRICE LOCATOR
- FIRST 10 PIVOT PRICE LOCATIONS
- P1 NEAREST: bar=841 offset=+16 time=2026-08-10 14:01:00+00:00 HIGH=601.73 diff=0.01999999999998181
- P2 NEAREST: bar=822 offset=-19 time=2026-08-10 13:42:00+00:00 HIGH=601.55 diff=0.0
- P1 NEAREST: bar=1130 offset=-24 time=2026-08-10 18:50:00+00:00 HIGH=600.33 diff=0.029999999999972715
- P1 NEAREST: bar=2404 offset=-6 time=2026-08-11 16:04:00+00:00 HIGH=609.8 diff=0.009999999999990905
- P1 NEAREST: bar=3437 offset=-2 time=2026-08-12 09:17:00+00:00 HIGH=612.06 diff=0.020000000000095497
- P1 NEAREST: bar=3768 offset=+2 time=2026-08-12 14:48:00+00:00 HIGH=611.16 diff=0.04000000000007731
- P2 NEAREST: bar=3783 offset=-4 time=2026-08-12 15:03:00+00:00 HIGH=610.64 diff=0.0
- FIRST 10 PIVOT PRICE LOCATIONS
- P1 NEAREST: bar=885 offset=+8 time=2026-08-10 14:45:00+00:00 HIGH=45.54 diff=0.00999999999999801
- P2 NEAREST: bar=885 offset=+2 time=2026-08-10 14:45:00+00:00 HIGH=45.54 diff=0.020000000000003126
- P1 NEAREST: bar=1560 offset=-7 time=2026-08-11 02:00:00+00:00 HIGH=45.27 diff=0.0
- P2 NEAREST: bar=1565 offset=-9 time=2026-08-11 02:05:00+00:00 HIGH=45.28 diff=0.0
- P1 NEAREST: bar=2275 offset=-10 time=2026-08-11 13:55:00+00:00 HIGH=45.16 diff=0.0
- P2 NEAREST: bar=2934 offset=-30 time=2026-08-12 00:54:00+00:00 HIGH=45.52 diff=0.0
- P1 NEAREST: bar=3437 offset=-11 time=2026-08-12 09:17:00+00:00 HIGH=45.36 diff=0.0
- P2 NEAREST: bar=3444 offset=-14 time=2026-08-12 09:24:00+00:00 HIGH=45.37 diff=0.0
- P1 NEAREST: bar=4366 offset=-30 time=2026-08-13 00:46:00+00:00 HIGH=44.85 diff=0.0
- P2 NEAREST: bar=4431 offset=+12 time=2026-08-13 01:51:00+00:00 HIGH=44.83 diff=0.0
- P1 NEAREST: bar=4598 offset=+2 time=2026-08-13 04:38:00+00:00 HIGH=44.94 diff=0.020000000000003126
- P2 NEAREST: bar=4598 offset=-8 time=2026-08-13 04:38:00+00:00 HIGH=44.94 diff=0.010000000000005116
- FIRST 10 PIVOT PRICE LOCATIONS
- P2 NEAREST: bar=2121 offset=-1 time=2026-08-11 11:21:00+00:00 HIGH=0.07061 diff=0.0
- P1 NEAREST: bar=3097 offset=+11 time=2026-08-12 03:37:00+00:00 HIGH=0.072426 diff=6.0000000000060005e-06
- P2 NEAREST: bar=3097 offset=+0 time=2026-08-12 03:37:00+00:00 HIGH=0.072426 diff=5.3999999999998494e-05
- P1 NEAREST: bar=3874 offset=+16 time=2026-08-12 16:34:00+00:00 HIGH=0.070945 diff=3.500000000000725e-05
- P2 NEAREST: bar=3874 offset=+0 time=2026-08-12 16:34:00+00:00 HIGH=0.070945 diff=4.500000000000337e-05
- P1 NEAREST: bar=4627 offset=-16 time=2026-08-13 05:07:00+00:00 HIGH=0.07031 diff=0.0
- P1 NEAREST: bar=4832 offset=-28 time=2026-08-13 08:32:00+00:00 HIGH=0.070511 diff=1.000000000001e-06
- P2 NEAREST: bar=4905 offset=+25 time=2026-08-13 09:45:00+00:00 HIGH=0.07044 diff=0.0
- P2 NEAREST: bar=5371 offset=-30 time=2026-08-13 17:31:00+00:00 HIGH=0.06987 diff=0.0
- FIRST 10 PIVOT PRICE LOCATIONS
- P2 NEAREST: bar=889 offset=+10 time=2026-08-10 14:49:00+00:00 HIGH=1897.36 diff=0.020000000000209184
- P1 NEAREST: bar=1070 offset=-17 time=2026-08-10 17:50:00+00:00 HIGH=1874.85 diff=0.05999999999994543
- P2 NEAREST: bar=1080 offset=-26 time=2026-08-10 18:00:00+00:00 HIGH=1874.02 diff=0.5199999999999818
- P1 NEAREST: bar=1524 offset=+11 time=2026-08-11 01:24:00+00:00 HIGH=1878.04 diff=0.19000000000005457
- P2 NEAREST: bar=1524 offset=+0 time=2026-08-11 01:24:00+00:00 HIGH=1878.04 diff=0.5299999999999727
- P2 NEAREST: bar=1561 offset=-14 time=2026-08-11 02:01:00+00:00 HIGH=1878.02 diff=0.009999999999990905
- P1 NEAREST: bar=1643 offset=+10 time=2026-08-11 03:23:00+00:00 HIGH=1880.48 diff=0.03999999999996362
- P2 NEAREST: bar=1660 offset=+21 time=2026-08-11 03:40:00+00:00 HIGH=1880.84 diff=0.38000000000010914
- P1 NEAREST: bar=1642 offset=+6 time=2026-08-11 03:22:00+00:00 HIGH=1879.6 diff=0.009999999999990905
- P2 NEAREST: bar=1669 offset=+27 time=2026-08-11 03:49:00+00:00 HIGH=1879.72 diff=0.01999999999998181
- P1 NEAREST: bar=1669 offset=+27 time=2026-08-11 03:49:00+00:00 HIGH=1879.72 diff=0.01999999999998181
- P2 NEAREST: bar=1678 offset=+27 time=2026-08-11 03:58:00+00:00 HIGH=1880.22 diff=0.0
- P1 NEAREST: bar=1660 offset=+13 time=2026-08-11 03:40:00+00:00 HIGH=1880.84 diff=0.4500000000000455
- P2 NEAREST: bar=1682 offset=+22 time=2026-08-11 04:02:00+00:00 HIGH=1881.17 diff=0.6099999999999
- ## `parity_lab/pine_timestamp_ohlc_check.py`
- PINE TIMESTAMP → RAW OHLC EXACT PIVOT TEST
- RAW P1: HIGH = 602.16 DIFF= 0.4499999999999318
- P1 OHLC: O=602.04 H=602.16 L=601.77 C=601.8
- RAW P2: HIGH = 601.73 DIFF= 0.18000000000006366
- P2 OHLC: O=601.07 H=601.73 L=601.07 C=601.57
- P1 OHLC: O=600.23 H=600.46 L=600.22 C=600.41
- P2 OHLC: O=600.34 H=600.36 L=600.24 C=600.36
- P1 OHLC: O=600.84 H=600.86 L=600.56 C=600.86
- P2 OHLC: O=601.06 H=601.16 L=600.94 C=601.16
- RAW P1: HIGH = 601.27 DIFF= 0.37000000000000455
- P1 OHLC: O=601.25 H=601.27 L=601.16 C=601.16
- RAW P2: HIGH = 601.4 DIFF= 0.39999999999997726
- P2 OHLC: O=601.37 H=601.4 L=601.21 C=601.21
- P1 OHLC: O=599.44 H=599.56 L=599.34 C=599.48
- P2 OHLC: O=599.53 H=599.76 L=599.5 C=599.66
- FIRST P1 MISMATCHES
- FIRST P2 MISMATCHES
- RAW P1: HIGH = 45.52 DIFF= -0.02999999999999403
- P1 OHLC: O=45.51 H=45.52 L=45.49 C=45.5
- RAW P2: HIGH = 45.53 DIFF= -0.030000000000001137
- P2 OHLC: O=45.52 H=45.53 L=45.5 C=45.51
- P1 OHLC: O=45.26 H=45.27 L=45.24 C=45.24
- P2 OHLC: O=45.26 H=45.28 L=45.25 C=45.25
- P1 OHLC: O=45.02 H=45.03 L=45.0 C=45.02
- P2 OHLC: O=45.04 H=45.04 L=44.99 C=45.02
- RAW P1: HIGH = 45.14 DIFF= -0.01999999999999602
- P1 OHLC: O=45.12 H=45.14 L=45.1 C=45.1
- RAW P2: HIGH = 45.1 DIFF= -0.01999999999999602
- P2 OHLC: O=45.1 H=45.1 L=45.07 C=45.07
- P1 OHLC: O=45.49 H=45.49 L=45.48 C=45.48
- P2 OHLC: O=45.5 H=45.52 L=45.5 C=45.52
- FIRST P1 MISMATCHES
- FIRST P2 MISMATCHES
- P1 OHLC: O=0.0706 H=0.070601 L=0.07056 C=0.070564
- P2 OHLC: O=0.070602 H=0.070649 L=0.070575 C=0.070595
- P1 OHLC: O=0.072583 H=0.07279 L=0.072583 C=0.072788
- P2 OHLC: O=0.072798 H=0.072839 L=0.072754 C=0.072796
- P1 OHLC: O=0.072174 H=0.072208 L=0.072164 C=0.07219
- P2 OHLC: O=0.07229 H=0.072301 L=0.072215 C=0.072299
- RAW P1: HIGH = 0.072382 DIFF= -3.799999999999637e-05
- P1 OHLC: O=0.072365 H=0.072382 L=0.072342 C=0.072342
- RAW P2: HIGH = 0.072426 DIFF= -5.3999999999998494e-05
- P2 OHLC: O=0.072375 H=0.072426 L=0.072344 C=0.072344
- P1 OHLC: O=0.071869 H=0.071869 L=0.071798 C=0.071798
- P2 OHLC: O=0.072055 H=0.072121 L=0.07173 C=0.071872
- FIRST P1 MISMATCHES
- FIRST P2 MISMATCHES
- P1 OHLC: O=1897.53 H=1897.93 L=1896.99 C=1897.33
- P2 OHLC: O=1897.87 H=1898.0 L=1896.65 C=1898.0
- RAW P1: HIGH = 1873.53 DIFF= -1.259999999999991
- P1 OHLC: O=1873.02 H=1873.53 L=1872.81 C=1873.02
- RAW P2: HIGH = 1873.98 DIFF= -0.5599999999999454
- P2 OHLC: O=1873.73 H=1873.98 L=1872.72 C=1873.0
- RAW P1: HIGH = 1877.0 DIFF= -0.849999999999909
- P1 OHLC: O=1876.59 H=1877.0 L=1876.02 C=1876.98
- RAW P2: HIGH = 1878.04 DIFF= -0.5299999999999727
- P2 OHLC: O=1876.53 H=1878.04 L=1876.53 C=1877.5
- P1 OHLC: O=1873.27 H=1875.01 L=1873.02 C=1875.01
- P2 OHLC: O=1874.37 H=1874.47 L=1873.49 C=1874.22
- P1 OHLC: O=1878.0 H=1878.0 L=1877.01 C=1877.53
- P2 OHLC: O=1877.0 H=1878.02 L=1877.0 C=1877.67
- FIRST P1 MISMATCHES
- FIRST P2 MISMATCHES
- PINE <-> BINANCE SPOT RAW OHLC DIAGNOSTIC
- usecols=["time", "open", "high", "low", "close"]
- 9. CURRENT WORKTREE STATE
- P0 — PIVOT INDEXING / CONFIRMATION SEMANTICS
- P0 — STATE RESTORATION / DOUBLE SHIFT
- P1 — RSI/RMA/EMA initialization
- P1 — MACD semantics
- P1 — divergence comparison
- P2 — candle confirmation
- For every claimed root cause provide:
- → INDEX/BAR ALIGNMENT
- → PIVOT SOURCE/CONFIRMATION
- → PIVOT STATE
- → DIVERGENCE
- The first mathematically proven divergence is the root-cause candidate.

## روش اصلاح

اصلاح باید از upstream به downstream انجام شود. ترتیب صحیح:

### 1. DATA / BAR IDENTITY
- بررسی منبع دقیق OHLC.
- بررسی timezone.
- بررسی timestamp هر candle.
- بررسی duplicate/missing candle.
- تعیین دقیق mapping بین Pine bar و Python row.
- جلوگیری از استفاده از timestamp به‌عنوان جایگزین bar identity.

### 2. PIVOT
- تعیین source bar.
- تعیین confirmation bar.
- تعیین زمان قابل‌مشاهده شدن pivot.
- ذخیره source_index و confirmation_index به‌صورت جداگانه.
- حذف هرگونه second shift.
- تطبیق قیمت pivot با رفتار واقعی Pine، نه فرض same-bar OHLC.
- مقایسه pivotها به‌صورت bar-by-bar.

### 3. STATE
- بررسی load state.
- بررسی save state.
- بررسی restore state.
- بررسی historical pivot arrays.
- بررسی اینکه pivot پس از restore دوباره shift نشود.
- مقایسه state قبل و بعد از هر bar.

### 4. INDICATORS
- RMA: seed، na handling، recursive update.
- EMA: seed و اولین مقدار معتبر.
- RSI: دقیقاً مطابق Pine.
- MACD: fast EMA، slow EMA، signal EMA، histogram.
- ATR: true range و RMA.
- هر indicator باید bar-by-bar مقایسه شود.

### 5. DIVERGENCE
- استفاده از همان pivotهای اصلاح‌شده.
- تطبیق p1/p2.
- تطبیق price values.
- تطبیق RSI values.
- تطبیق MACD values.
- تطبیق فاصله بین pivotها.
- تطبیق نوع divergence.

### 6. FIBONACCI
- تطبیق swing source.
- تطبیق anchorها.
- تطبیق 0.618.
- تطبیق 0.786.
- تطبیق tolerance.
- تطبیق search window.

### 7. CANDLE / PRICE ACTION
- تطبیق open/high/low/close.
- body.
- upper/lower shadow.
- ATR candle ratio.
- big candle threshold.
- pin/shadow conditions.

### 8. SCORE / SIGNAL
- تطبیق تک‌تک score components.
- تطبیق ترتیب محاسبات.
- تطبیق boolean conditions.
- تطبیق finalScore.
- تطبیق signal generation.

## INVENTORY OF FUNCTIONS AND PARAMETERS

### FILE: `bot.py`

#### Classes
- `PublicData`
- `PrivateExchange`
- `HealthHandler`

#### Functions
- `send_telegram(text)`
- `__init__(self)`
- `fetch_ohlcv(self, symbol)`
- `__init__(self)`
- `_sign(self, method, uri, ts)`
- `_request(self, method, uri, data=None)`
- `test_connection(self)`
- `fetch_balance(self)`
- `_round_price(self, price, symbol)`
- `create_order(self, symbol, side, capital, leverage)`
- `do_GET(self)`
- `log_message(self, fmt, *args)`
- `run_health_server(port)`
- `_handle_shutdown(signum, frame)`
- `loop()`

#### Parameters / Constants
- `API_KEY` = `os.getenv("API_KEY", "pXJ3uOI3y7iPHxIgefQJ30PikXHqbQyVV9Ouj-_K")`
- `API_SECRET` = `os.getenv("API_SECRET", "4cd23e00385ea761250034b420c86f40c4edb8e27c285c21572dbadf7e927b09")`
- `BASE_URL` = `os.getenv("BASE_URL", "https://apiv2.thetruetrade.io")`
- `TELEGRAM_BOT_TOKEN` = `os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")`
- `TELEGRAM_CHAT_ID` = `os.getenv("TELEGRAM_CHAT_ID", "7402770612")`
- `SYMBOLS` = `["LTCUSDT", "DOGEUSDT", "ETHUSDT", "BNBUSDT"]`
- `HISTORY_BARS` = `500`
- `LEVERAGE_MAP` = `{"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50, "BNBUSDT": 50}`
- `TARGET_RISK` = `2.0`
- `TICK_SIZES` = `{"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01, "BNBUSDT": 0.01}`
- `PRICE_PRECISION` = `{"LTCUSDT": 2, "DOGEUSDT": 5, "ETHUSDT": 2, "BNBUSDT": 2}`
- `STOP_EVENT` = `threading.Event()`

### FILE: `dtm_bot.py`

#### Classes
- `TrueTradePublicData`
- `TrueTradePrivateExchange`

#### Functions
- `_ignore_sigterm(signum, frame)`
- `send_telegram_message(text)`
- `format_iran_time()`
- `__init__(self)`
- `fetch_ohlcv(self, symbol, timeframe="1m", limit=HISTORY_BARS)`
- `__init__(self)`
- `_sign(self, method, uri, ts)`
- `_request(self, method, uri, data=None)`
- `test_connection(self)`
- `fetch_balance(self)`
- `fetch_open_positions(self)`
- `_round_price(self, price, symbol)`
- `create_order(self, symbol, side, capital, params=None)`
- `health()`
- `health_check()`
- `run_trading_loop()`

#### Parameters / Constants
- `API_KEY` = `os.getenv("API_KEY", "pXJ3uOI3y7iPHxIgefQJ30PikXHqbQyVV9Ouj-_K")`
- `API_SECRET` = `os.getenv("API_SECRET", "4cd23e00385ea761250034b420c86f40c4edb8e27c285c21572dbadf7e927b09")`
- `BASE_URL` = `os.getenv("BASE_URL", "https://apiv2.thetruetrade.io")`
- `TELEGRAM_BOT_TOKEN` = `os.getenv("TELEGRAM_BOT_TOKEN", "8514469828:AAFC76EiVA7I4TFiX08jJ5N6-eKtOLMKitE")`
- `TELEGRAM_CHAT_ID` = `os.getenv("TELEGRAM_CHAT_ID", "7402770612")`
- `SYMBOLS` = `["LTCUSDT", "DOGEUSDT", "ETHUSDT"]`
- `TIMEFRAME` = `"1m"`
- `HISTORY_BARS` = `500`
- `RSI_LEN` = `14`
- `MACD_FAST` = `12`
- `MACD_SLOW` = `26`
- `MACD_SIG` = `9`
- `TREND_LOOKBACK` = `20`
- `TREND_SLOPE_MIN_PCT` = `0.05`
- `MIN_CONFIRMATIONS` = `"۳ تعییدیه (حداقل مجاز)"`
- `ENABLE_HIDDEN` = `True`
- `FIB_USE_618` = `True`
- `FIB_USE_786` = `True`
- `FIB_TOLERANCE_PCT` = `0.5`
- `FIB_TREND_SEARCH_BARS` = `100`
- `SHADOW_TO_BODY_RATIO` = `2.0`
- `MAX_OPPOSITE_SHADOW_PCT` = `20.0`
- `MIN_CANDLE_ATR_RATIO` = `0.3`
- `BIG_CANDLE_AVG_LEN` = `14`
- `BIG_CANDLE_MULTIPLIER` = `1.5`
- `ENABLE_MTF` = `False`
- `MTF_TIMEFRAME` = `"240"`
- `LEFT_BARS` = `5`
- `RIGHT_BARS` = `3`
- `TICK_SIZES` = `{"LTCUSDT": 0.01, "DOGEUSDT": 0.00001, "ETHUSDT": 0.01}`
- `PRICE_PRECISION` = `{"LTCUSDT": 2, "DOGEUSDT": 5, "ETHUSDT": 2}`
- `LEVERAGE_MAP` = `{"LTCUSDT": 75, "DOGEUSDT": 75, "ETHUSDT": 50}`

### FILE: `health_server.py`

#### Classes
- `HealthHandler`

#### Functions
- `do_GET(self)`
- `log_message(self, fmt, *args)`

#### Parameters / Constants
- `HOST` = `"0.0.0.0"`
- `PORT` = `int(os.environ.get("PORT", "8080"))`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_argcomplete.py`

#### Classes
- `FastFilesCompleter`

#### Functions
- `__init__(self, directories: bool = True)`
- `__call__(self, prefix: str, **kwargs: Any)`
- `try_argcomplete(parser: argparse.ArgumentParser)`
- `try_argcomplete(parser: argparse.ArgumentParser)`

#### Parameters / Constants
- `SPEEDUP` = `======`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_code/code.py`

#### Classes
- `Code`
- `Frame`
- `TracebackEntry`
- `Traceback`
- `ExceptionInfo`
- `ExceptionInfoFormatter`
- `TerminalRepr`
- `ExceptionRepr`
- `ExceptionChainRepr`
- `ReprExceptionInfo`
- `ReprTraceback`
- `ReprTracebackNative`
- `ReprEntryNative`
- `ReprEntry`
- `ReprFileLocation`
- `ReprLocals`
- `ReprFuncArgs`

#### Functions
- `__init__(self, obj: CodeType)`
- `from_function(cls, obj: object)`
- `__eq__(self, other)`
- `firstlineno(self)`
- `name(self)`
- `path(self)`
- `fullsource(self)`
- `source(self)`
- `getargs(self, var: bool = False)`
- `__init__(self, frame: FrameType)`
- `lineno(self)`
- `f_globals(self)`
- `f_locals(self)`
- `code(self)`
- `statement(self)`
- `eval(self, code, **vars)`
- `repr(self, object: object)`
- `getargs(self, var: bool = False)`
- `__init__(
        self,
        rawentry: TracebackType,
        repr_style: Literal["short", "long"] | None = None,
    )`
- `with_repr_style(
        self, repr_style: Literal["short", "long"] | None
    )`
- `lineno(self)`
- `get_python_framesummary(self)`
- `end_lineno_relative(self)`
- `colno(self)`
- `end_colno(self)`
- `end_lineno_relative(self)`
- `colno(self)`
- `end_colno(self)`
- `frame(self)`
- `relline(self)`
- `__repr__(self)`
- `statement(self)`
- `path(self)`
- `locals(self)`
- `getfirstlinesource(self)`
- `getsource(
        self, astcache: dict[str | Path, ast.AST] | None = None
    )`
- `ishidden(self, excinfo: ExceptionInfo[BaseException] | None)`
- `__str__(self)`
- `name(self)`
- `__init__(
        self,
        tb: TracebackType | Iterable[TracebackEntry],
    )`
- `f(cur: TracebackType)`
- `cut(
        self,
        path: os.PathLike[str] | str | None = None,
        lineno: int | None = None,
        firstlineno: int | None = None,
        excludepath: os.PathLike[str] | None = None,
    )`
- `__getitem__(self, key: SupportsIndex)`
- `__getitem__(self, key: slice)`
- `__getitem__(self, key: SupportsIndex | slice)`
- `filter(
        self,
        excinfo_or_fn: ExceptionInfo[BaseException] | Callable[[TracebackEntry], bool],
        /,
    )`
- `recursionindex(self)`
- `stringify_exception(
    exc: BaseException, include_subexception_msg: bool = True
)`
- `__init__(
        self,
        excinfo: tuple[type[E], E, TracebackType] | None,
        striptext: str = "",
        traceback: Traceback | None = None,
        *,
        _ispytest: bool = False,
    )`
- `from_exception(
        cls,
        # Ignoring error: "Cannot use a covariant type variable as a parameter".
        # This is OK to ignore because this class is (conceptually)`
- `from_exc_info(
        cls,
        exc_info: tuple[type[E], E, TracebackType],
        exprinfo: str | None = None,
    )`
- `from_current(cls, exprinfo: str | None = None)`
- `for_later(cls)`
- `fill_unfilled(self, exc_info: tuple[type[E], E, TracebackType])`
- `type(self)`
- `value(self)`
- `tb(self)`
- `typename(self)`
- `traceback(self)`
- `traceback(self, value: Traceback)`
- `__repr__(self)`
- `exconly(self, tryshort: bool = False)`
- `_get_single_subexc(
            eg: BaseExceptionGroup[BaseException],
        )`
- `errisinstance(self, exc: EXCEPTION_OR_MORE)`
- `_getreprcrash(self)`
- `getrepr(
        self,
        showlocals: bool = False,
        style: TracebackStyle = "long",
        abspath: bool = False,
        tbfilter: bool | Callable[[ExceptionInfo[BaseException]], Traceback] = True,
        funcargs: bool = False,
        truncate_locals: bool = True,
        truncate_args: bool = True,
        chain: bool = True,
    )`
- `match(self, regexp: str | re.Pattern[str])`
- `_group_contains(
        self,
        exc_group: BaseExceptionGroup[BaseException],
        expected_exception: EXCEPTION_OR_MORE,
        match: str | re.Pattern[str] | None,
        target_depth: int | None = None,
        current_depth: int = 1,
    )`
- `group_contains(
        self,
        expected_exception: EXCEPTION_OR_MORE,
        *,
        match: str | re.Pattern[str] | None = None,
        depth: int | None = None,
    )`
- `_getindent(self, source: Source)`
- `_getentrysource(self, entry: TracebackEntry)`
- `repr_args(self, entry: TracebackEntry)`
- `get_source(
        self,
        source: Source | None,
        line_index: int = -1,
        excinfo: ExceptionInfo[BaseException] | None = None,
        short: bool = False,
        end_line_index: int | None = None,
        colno: int | None = None,
        end_colno: int | None = None,
    )`
- `get_highlight_arrows_for_line(
        self,
        line: str,
        raw_line: str,
        lineno: int | None,
        end_lineno: int | None,
        colno: int | None,
        end_colno: int | None,
    )`
- `get_exconly(
        self,
        excinfo: ExceptionInfo[BaseException],
        indent: int = 4,
        markall: bool = False,
    )`
- `repr_locals(self, locals: Mapping[str, object])`
- `repr_traceback_entry(
        self,
        entry: TracebackEntry | None,
        excinfo: ExceptionInfo[BaseException] | None = None,
    )`
- `_makepath(self, path: Path | str)`
- `repr_traceback(self, excinfo: ExceptionInfo[BaseException])`
- `_truncate_recursive_traceback(
        self, traceback: Traceback
    )`
- `repr_excinfo(self, excinfo: ExceptionInfo[BaseException])`
- `__str__(self)`
- `__repr__(self)`
- `toterminal(self, tw: TerminalWriter)`
- `addsection(self, name: str, content: str, sep: str = "-")`
- `toterminal(self, tw: TerminalWriter)`
- `__init__(
        self,
        chain: Sequence[tuple[ReprTraceback, ReprFileLocation | None, str | None]],
    )`
- `toterminal(self, tw: TerminalWriter)`
- `toterminal(self, tw: TerminalWriter)`
- `toterminal(self, tw: TerminalWriter)`
- `__init__(self, tblines: Sequence[str], *, extraline: str | None = None)`
- `toterminal(self, tw: TerminalWriter)`
- `_write_entry_lines(self, tw: TerminalWriter)`
- `toterminal(self, tw: TerminalWriter)`
- `__str__(self)`
- `__post_init__(self)`
- `toterminal(self, tw: TerminalWriter)`
- `toterminal(self, tw: TerminalWriter, indent: str = "")`
- `toterminal(self, tw: TerminalWriter)`
- `getfslineno(obj: object)`
- `_byte_offset_to_character_offset(str, offset)`
- `filter_traceback(entry: TracebackEntry)`
- `filter_excinfo_traceback(
    tbfilter: TracebackFilter, excinfo: ExceptionInfo[BaseException]
)`

#### Parameters / Constants
- `EXCEPTION_OR_MORE` = `type[BaseException] | tuple[type[BaseException], ...]`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_code/source.py`

#### Classes
- `Source`

#### Functions
- `__init__(self, obj: object = None)`
- `__eq__(self, other: object)`
- `__getitem__(self, key: int)`
- `__getitem__(self, key: slice)`
- `__getitem__(self, key: int | slice)`
- `__iter__(self)`
- `__len__(self)`
- `strip(self)`
- `indent(self, indent: str = " " * 4)`
- `getstatement(self, lineno: int)`
- `getstatementrange(self, lineno: int)`
- `deindent(self)`
- `__str__(self)`
- `findsource(obj)`
- `getrawcode(obj: object, trycall: bool = True)`
- `deindent(lines: Iterable[str])`
- `get_statement_startend2(lineno: int, node: ast.AST)`
- `getstatementrange_ast(
    lineno: int,
    source: Source,
    assertion: bool = False,
    astnode: ast.AST | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_io/pprint.py`

#### Classes
- `_safe_key`
- `PrettyPrinter`

#### Functions
- `__init__(self, obj)`
- `__lt__(self, other)`
- `_safe_tuple(t)`
- `__init__(
        self,
        indent: int = 4,
        width: int = 80,
        depth: int | None = None,
    )`
- `pformat(self, object: Any)`
- `_format(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_dataclass(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_dict(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_ordered_dict(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_list(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_tuple(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_set(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_str(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_bytes(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_bytearray(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_mappingproxy(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_simplenamespace(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_format_dict_items(
        self,
        items: list[tuple[Any, Any]],
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_format_namespace_items(
        self,
        items: list[tuple[Any, Any]],
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_format_items(
        self,
        items: list[Any],
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_repr(self, object: Any, context: set[int], level: int)`
- `_pprint_default_dict(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_counter(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_chain_map(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_deque(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_user_dict(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_user_list(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_pprint_user_string(
        self,
        object: Any,
        stream: IO[str],
        indent: int,
        allowance: int,
        context: set[int],
        level: int,
    )`
- `_safe_repr(
        self, object: Any, context: set[int], maxlevels: int | None, level: int
    )`
- `_recursion(object: Any)`
- `_wrap_bytes_repr(object: Any, width: int, allowance: int)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_io/saferepr.py`

#### Classes
- `SafeRepr`

#### Functions
- `_try_repr_or_str(obj: object)`
- `_format_repr_exception(exc: BaseException, obj: object)`
- `_ellipsize(s: str, maxsize: int)`
- `__init__(self, maxsize: int | None, use_ascii: bool = False)`
- `repr(self, x: object)`
- `repr_instance(self, x: object, level: int)`
- `repr_dict(self, x: dict[object, object], level: int)`
- `safeformat(obj: object)`
- `saferepr(
    obj: object, maxsize: int | None = DEFAULT_REPR_MAX_SIZE, use_ascii: bool = False
)`
- `saferepr_unlimited(obj: object, use_ascii: bool = True)`

#### Parameters / Constants
- `DEFAULT_REPR_MAX_SIZE` = `240`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_io/terminalwriter.py`

#### Classes
- `TerminalWriter`

#### Functions
- `get_terminal_width()`
- `should_do_markup(file: TextIO)`
- `__init__(self, file: TextIO | None = None)`
- `fullwidth(self)`
- `fullwidth(self, value: int)`
- `width_of_current_line(self)`
- `markup(self, text: str, **markup: bool)`
- `sep(
        self,
        sepchar: str,
        title: str | None = None,
        fullwidth: int | None = None,
        **markup: bool,
    )`
- `write(self, msg: str, *, flush: bool = False, **markup: bool)`
- `write_raw(self, msg: str, *, flush: bool = False)`
- `line(self, s: str = "", **markup: bool)`
- `flush(self)`
- `_write_source(self, lines: Sequence[str], indents: Sequence[str] = ()`
- `_get_pygments_lexer(self, lexer: Literal["python", "diff"])`
- `_get_pygments_formatter(self)`
- `_highlight(
        self, source: str, lexer: Literal["diff", "python"] = "python"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_io/wcwidth.py`

#### Functions
- `wcwidth(c: str)`
- `wcswidth(s: str)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_py/error.py`

#### Classes
- `Error`
- `ErrorMaker`

#### Functions
- `__repr__(self)`
- `__str__(self)`
- `__getattr__(self, name: str)`
- `_geterrnoclass(self, eno: int)`
- `checked_call(
        self, func: Callable[P, R], *args: P.args, **kwargs: P.kwargs
    )`
- `__getattr__(attr: str)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/_py/path.py`

#### Classes
- `Checkers`
- `NeverRaised`
- `Visitor`
- `FNMatcher`
- `Stat`
- `LocalPath`
- `ImportMismatchError`

#### Functions
- `__init__(self, path)`
- `dotfile(self)`
- `ext(self, arg)`
- `basename(self, arg)`
- `basestarts(self, arg)`
- `relto(self, arg)`
- `fnmatch(self, arg)`
- `endswith(self, arg)`
- `_evaluate(self, kw)`
- `_stat(self)`
- `dir(self)`
- `file(self)`
- `exists(self)`
- `link(self)`
- `__init__(self, fil, rec, ignore, bf, sort)`
- `gen(self, path)`
- `__init__(self, pattern)`
- `__call__(self, path)`
- `map_as_list(func, iter)`
- `size(self)`
- `mtime(self)`
- `__getattr__(self, name: str)`
- `__init__(self, path, osstatresult)`
- `owner(self)`
- `group(self)`
- `isdir(self)`
- `isfile(self)`
- `islink(self)`
- `getuserid(user)`
- `getgroupid(group)`
- `__init__(self, path=None, expanduser=False)`
- `chown(self, user, group, rec=0)`
- `readlink(self)`
- `mklinkto(self, oldname)`
- `mksymlinkto(self, value, absolute=1)`
- `__div__(self, other)`
- `basename(self)`
- `dirname(self)`
- `purebasename(self)`
- `ext(self)`
- `read_binary(self)`
- `read_text(self, encoding)`
- `read(self, mode="r")`
- `readlines(self, cr=1)`
- `load(self)`
- `move(self, target)`
- `fnmatch(self, pattern)`
- `relto(self, relpath)`
- `ensure_dir(self, *args)`
- `bestrelpath(self, dest)`
- `exists(self)`
- `isdir(self)`
- `isfile(self)`
- `parts(self, reverse=False)`
- `common(self, other)`
- `__add__(self, other)`
- `visit(self, fil=None, rec=None, ignore=NeverRaised, bf=False, sort=False)`
- `_sortlist(self, res, sort)`
- `__fspath__(self)`
- `__hash__(self)`
- `__eq__(self, other)`
- `__ne__(self, other)`
- `__lt__(self, other)`
- `__gt__(self, other)`
- `samefile(self, other)`
- `remove(self, rec=1, ignore_errors=False)`
- `computehash(self, hashtype="md5", chunksize=524288)`
- `new(self, **kw)`
- `_getbyspec(self, spec: str)`
- `dirpath(self, *args, **kwargs)`
- `join(self, *args: os.PathLike[str], abs: bool = False)`
- `open(self, mode="r", ensure=False, encoding=None)`
- `_fastjoin(self, name)`
- `islink(self)`
- `check(self, **kw)`
- `listdir(self, fil=None, sort=None)`
- `size(self)`
- `mtime(self)`
- `copy(self, target, mode=False, stat=False)`
- `rec(p)`
- `rename(self, target)`
- `dump(self, obj, bin=1)`
- `mkdir(self, *args)`
- `write_binary(self, data, ensure=False)`
- `write_text(self, data, encoding, ensure=False)`
- `write(self, data, mode="w", ensure=False)`
- `_ensuredirs(self)`
- `ensure(self, *args, **kwargs)`
- `stat(self, raising: Literal[True] = ...)`
- `stat(self, raising: Literal[False])`
- `stat(self, raising: bool = True)`
- `lstat(self)`
- `setmtime(self, mtime=None)`
- `chdir(self)`
- `as_cwd(self)`
- `realpath(self)`
- `atime(self)`
- `__repr__(self)`
- `__str__(self)`
- `chmod(self, mode, rec=0)`
- `pypkgpath(self)`
- `_ensuresyspath(self, ensuremode, path)`
- `pyimport(self, modname=None, ensuresyspath=True)`
- `sysexec(self, *argv: os.PathLike[str], **popen_opts: Any)`
- `sysfind(cls, name, checker=None, paths=None)`
- `_gethomedir(cls)`
- `get_temproot(cls)`
- `mkdtemp(cls, rootdir=None)`
- `make_numbered_dir(
        cls, prefix="session-", rootdir=None, keep=3, lock_timeout=172800
    )`
- `parse_num(path)`
- `create_lockfile(path)`
- `atexit_remove_lockfile(lockfile)`
- `try_remove_lockfile()`
- `get_mtime(path)`
- `is_garbage(path)`
- `copymode(src, dest)`
- `copystat(src, dest)`
- `copychunked(src, dest)`
- `isimportable(name)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/__init__.py`

#### Classes
- `RewriteHook`
- `DummyRewriteHook`
- `AssertionState`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `register_assert_rewrite(*names: str)`
- `mark_rewrite(self, *names: str)`
- `mark_rewrite(self, *names: str)`
- `__init__(self, config: Config, mode)`
- `install_importhook(config: Config)`
- `undo()`
- `pytest_collection(session: Session)`
- `pytest_runtest_protocol(item: Item)`
- `callbinrepr(op, left: object, right: object)`
- `call_assertion_pass_hook(lineno: int, orig: str, expl: str)`
- `pytest_sessionfinish(session: Session)`
- `pytest_assertrepr_compare(
    config: Config, op: str, left: Any, right: Any
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_any.py`

#### Functions
- `_compare_eq_any(
    left: object,
    right: object,
    highlighter: _HighlightFunc,
    verbose: int,
    assertion_text_diff_style: _AssertionTextDiffStyle,
)`
- `_compare_eq_cls(
    left: object,
    right: object,
    highlighter: _HighlightFunc,
    verbose: int,
    assertion_text_diff_style: _AssertionTextDiffStyle,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_mapping.py`

#### Functions
- `_compare_eq_mapping(
    left: Mapping[object, object],
    right: Mapping[object, object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_sequence.py`

#### Functions
- `_compare_eq_iterable(
    left: Iterable[object],
    right: Iterable[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`
- `_compare_eq_sequence(
    left: Sequence[object],
    right: Sequence[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/_compare_set.py`

#### Functions
- `_set_one_sided_diff(
    posn: str,
    set1: AbstractSet[object],
    set2: AbstractSet[object],
    highlighter: _HighlightFunc,
)`
- `_compare_eq_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`
- `_compare_gte_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`
- `_compare_lte_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`
- `_compare_gt_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`
- `_compare_lt_set(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`
- `_both_sets_are_equal(
    left: AbstractSet[object],
    right: AbstractSet[object],
    highlighter: _HighlightFunc,
    verbose: int = 0,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/_guards.py`

#### Functions
- `issequence(x: object)`
- `istext(x: object)`
- `ismapping(x: object)`
- `isset(x: object)`
- `isnamedtuple(obj: object)`
- `isattrs(obj: object)`
- `isiterable(obj: object)`
- `has_default_eq(obj: object)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/_typing.py`

#### Classes
- `_HighlightFunc`

#### Functions
- `__call__(self, source: str, lexer: Literal["diff", "python"] = "python")`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/compare_text.py`

#### Functions
- `_compare_eq_text(
    left: str,
    right: str,
    highlighter: _HighlightFunc,
    verbose: int,
    assertion_text_diff_style: _AssertionTextDiffStyle,
)`
- `_diff_text_block(left: str, right: str)`
- `_format_text_block_lines(text: str)`
- `_diff_text(
    left: str, right: str, highlighter: _HighlightFunc, verbose: int = 0
)`
- `_notin_text(term: str, text: str, verbose: int = 0)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/highlight.py`

#### Functions
- `dummy_highlighter(source: str, lexer: Literal["diff", "python"] = "python")`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/rewrite.py`

#### Classes
- `Sentinel`
- `AssertionRewritingHook`
- `AssertionRewriter`

#### Functions
- `__init__(self, config: Config)`
- `set_session(self, session: Session | None)`
- `find_spec(
        self,
        name: str,
        path: Sequence[str | bytes] | None = None,
        target: types.ModuleType | None = None,
    )`
- `create_module(
        self, spec: importlib.machinery.ModuleSpec
    )`
- `exec_module(self, module: types.ModuleType)`
- `_early_rewrite_bailout(self, name: str, state: AssertionState)`
- `_should_rewrite(self, name: str, fn: str, state: AssertionState)`
- `_is_marked_for_rewrite(self, name: str, state: AssertionState)`
- `mark_rewrite(self, *names: str)`
- `_warn_already_imported(self, name: str)`
- `get_data(self, pathname: str | bytes)`
- `get_resource_reader(self, name: str)`
- `_write_pyc_fp(
    fp: IO[bytes], source_stat: os.stat_result, co: types.CodeType
)`
- `_write_pyc(
    state: AssertionState,
    co: types.CodeType,
    source_stat: os.stat_result,
    pyc: Path,
)`
- `_rewrite_test(fn: Path, config: Config)`
- `_read_pyc(
    source: Path, pyc: Path, trace: Callable[[str], None] = lambda x: None
)`
- `rewrite_asserts(
    mod: ast.Module,
    source: bytes,
    module_path: str | None = None,
    config: Config | None = None,
)`
- `_saferepr(obj: object)`
- `_get_maxsize_for_saferepr(config: Config | None)`
- `_format_assertmsg(obj: object)`
- `_should_repr_global_name(obj: object)`
- `_format_boolop(explanations: Iterable[str], is_or: bool)`
- `_call_reprcompare(
    ops: Sequence[str],
    results: Sequence[bool],
    expls: Sequence[str],
    each_obj: Sequence[object],
)`
- `_call_assertion_pass(lineno: int, orig: str, expl: str)`
- `_check_if_assertion_pass_impl()`
- `traverse_node(node: ast.AST)`
- `_get_assertion_exprs(src: bytes)`
- `_write_and_reset()`
- `__init__(
        self, module_path: str | None, config: Config | None, source: bytes
    )`
- `run(self, mod: ast.Module)`
- `is_rewrite_disabled(docstring: str)`
- `variable(self)`
- `assign(self, expr: ast.expr)`
- `display(self, expr: ast.expr)`
- `helper(self, name: str, *args: ast.expr)`
- `builtin(self, name: str)`
- `explanation_param(self, expr: ast.expr)`
- `push_format_context(self)`
- `pop_format_context(self, expl_expr: ast.expr)`
- `generic_visit(self, node: ast.AST)`
- `visit_Assert(self, assert_: ast.Assert)`
- `visit_NamedExpr(self, name: ast.NamedExpr)`
- `visit_Name(self, name: ast.Name)`
- `visit_BoolOp(self, boolop: ast.BoolOp)`
- `visit_UnaryOp(self, unary: ast.UnaryOp)`
- `visit_BinOp(self, binop: ast.BinOp)`
- `visit_Call(self, call: ast.Call)`
- `visit_Starred(self, starred: ast.Starred)`
- `visit_Attribute(self, attr: ast.Attribute)`
- `visit_Compare(self, comp: ast.Compare)`
- `try_makedirs(cache_dir: Path)`
- `get_cache_dir(file_path: Path)`

#### Parameters / Constants
- `PYTEST_TAG` = `f"{sys.implementation.cache_tag}-pytest-{version}"`
- `PYC_EXT` = `".py" + ((__debug__ and "c") or "o")`
- `PYC_TAIL` = `"." + PYTEST_TAG + PYC_EXT`
- `UNARY_MAP` = `{ast.Not: "not %s", ast.Invert: "~%s", ast.USub: "-%s", ast.UAdd: "+%s"}`
- `BINOP_MAP` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/truncate.py`

#### Functions
- `truncate_if_required(explanation: list[str], item: Item)`
- `_get_truncation_parameters(item: Item)`
- `_truncate_explanation(
    input_lines: list[str],
    max_lines: int,
    max_chars: int,
)`
- `_truncate_by_char_count(input_lines: list[str], max_chars: int)`

#### Parameters / Constants
- `DEFAULT_MAX_LINES` = `8`
- `DEFAULT_MAX_CHARS` = `DEFAULT_MAX_LINES * 80`
- `USAGE_MSG` = `"use '-vv' to show"`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/assertion/util.py`

#### Functions
- `get_assertion_text_diff_style(config: Config)`
- `validate_assertion_text_diff_style(config: Config)`
- `format_explanation(explanation: str)`
- `_split_explanation(explanation: str)`
- `_format_lines(lines: Sequence[str])`
- `assertrepr_compare(
    op: str,
    left: object,
    right: object,
    *,
    verbose: int,
    highlighter: _HighlightFunc,
    assertion_text_diff_style: _AssertionTextDiffStyle,
)`

#### Parameters / Constants
- `ASSERTION_TEXT_DIFF_STYLE_INI` = `"assertion_text_diff_style"`
- `ASSERTION_TEXT_DIFF_STYLE_CHOICES` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/cacheprovider.py`

#### Classes
- `Cache`
- `LFPluginCollWrapper`
- `LFPluginCollSkipfiles`
- `LFPlugin`
- `NFPlugin`

#### Functions
- `_make_cachedir(target: Path)`
- `__init__(
        self, cachedir: Path, config: Config, *, _ispytest: bool = False
    )`
- `for_config(cls, config: Config, *, _ispytest: bool = False)`
- `clear_cache(cls, cachedir: Path, _ispytest: bool = False)`
- `cache_dir_from_config(config: Config, *, _ispytest: bool = False)`
- `warn(self, fmt: str, *, _ispytest: bool = False, **args: object)`
- `_mkdir(self, path: Path)`
- `mkdir(self, name: str)`
- `_getvaluepath(self, key: str)`
- `get(self, key: str, default)`
- `set(self, key: str, value: object)`
- `_ensure_cache_dir_and_supporting_files(self)`
- `__init__(self, lfplugin: LFPlugin)`
- `pytest_make_collect_report(
        self, collector: nodes.Collector
    )`
- `sort_key(node: nodes.Item | nodes.Collector)`
- `__init__(self, lfplugin: LFPlugin)`
- `pytest_make_collect_report(
        self, collector: nodes.Collector
    )`
- `__init__(self, config: Config)`
- `get_last_failed_paths(self)`
- `pytest_report_collectionfinish(self)`
- `pytest_runtest_logreport(self, report: TestReport)`
- `pytest_collectreport(self, report: CollectReport)`
- `pytest_collection_modifyitems(
        self, config: Config, items: list[nodes.Item]
    )`
- `pytest_sessionfinish(self, session: Session)`
- `__init__(self, config: Config)`
- `pytest_collection_modifyitems(self, items: list[nodes.Item])`
- `_get_increasing_order(self, items: Iterable[nodes.Item])`
- `pytest_sessionfinish(self)`
- `pytest_addoption(parser: Parser)`
- `pytest_cmdline_main(config: Config)`
- `pytest_configure(config: Config)`
- `cache(request: FixtureRequest)`
- `pytest_report_header(config: Config)`
- `cacheshow(config: Config, session: Session)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/capture.py`

#### Classes
- `EncodedFile`
- `CaptureIO`
- `TeeCaptureIO`
- `DontReadFromInput`
- `CaptureBase`
- `NoCapture`
- `SysCaptureBase`
- `SysCaptureBinary`
- `SysCapture`
- `FDCaptureBase`
- `FDCaptureBinary`
- `FDCapture`
- `CaptureResult`
- `CaptureResult`
- `MultiCapture`
- `CaptureManager`
- `CaptureFixture`

#### Functions
- `pytest_addoption(parser: Parser)`
- `_colorama_workaround()`
- `_readline_workaround()`
- `_windowsconsoleio_workaround(stream: TextIO)`
- `_reopen_stdio(f, mode)`
- `pytest_load_initial_conftests(early_config: Config)`
- `name(self)`
- `mode(self)`
- `__init__(self)`
- `getvalue(self)`
- `__init__(self, other: TextIO)`
- `write(self, s: str)`
- `encoding(self)`
- `read(self, size: int = -1)`
- `__next__(self)`
- `readlines(self, hint: int | None = -1)`
- `__iter__(self)`
- `fileno(self)`
- `flush(self)`
- `isatty(self)`
- `close(self)`
- `readable(self)`
- `seek(self, offset: int, whence: int = 0)`
- `seekable(self)`
- `tell(self)`
- `truncate(self, size: int | None = None)`
- `write(self, data: str)`
- `writelines(self, lines: Iterable[str])`
- `writable(self)`
- `__enter__(self)`
- `__exit__(
        self,
        type: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    )`
- `buffer(self)`
- `__init__(self, fd: int)`
- `start(self)`
- `done(self)`
- `suspend(self)`
- `resume(self)`
- `writeorg(self, data: AnyStr)`
- `snap(self)`
- `__init__(self, fd: int)`
- `start(self)`
- `done(self)`
- `suspend(self)`
- `resume(self)`
- `snap(self)`
- `writeorg(self, data: str)`
- `__init__(
        self, fd: int, tmpfile: TextIO | None = None, *, tee: bool = False
    )`
- `repr(self, class_name: str)`
- `__repr__(self)`
- `_assert_state(self, op: str, states: tuple[str, ...])`
- `start(self)`
- `done(self)`
- `suspend(self)`
- `resume(self)`
- `snap(self)`
- `writeorg(self, data: bytes)`
- `snap(self)`
- `writeorg(self, data: str)`
- `__init__(self, targetfd: int)`
- `__repr__(self)`
- `_assert_state(self, op: str, states: tuple[str, ...])`
- `start(self)`
- `done(self)`
- `suspend(self)`
- `resume(self)`
- `snap(self)`
- `writeorg(self, data: bytes)`
- `snap(self)`
- `writeorg(self, data: str)`
- `__init__(
        self,
        in_: CaptureBase[AnyStr] | None,
        out: CaptureBase[AnyStr] | None,
        err: CaptureBase[AnyStr] | None,
    )`
- `__repr__(self)`
- `start_capturing(self)`
- `pop_outerr_to_orig(self)`
- `suspend_capturing(self, in_: bool = False)`
- `resume_capturing(self)`
- `stop_capturing(self)`
- `is_started(self)`
- `readouterr(self)`
- `_get_multicapture(method: _CaptureMethod)`
- `__init__(self, method: _CaptureMethod)`
- `__repr__(self)`
- `is_capturing(self)`
- `is_globally_capturing(self)`
- `start_global_capturing(self)`
- `stop_global_capturing(self)`
- `resume_global_capture(self)`
- `suspend_global_capture(self, in_: bool = False)`
- `suspend(self, in_: bool = False)`
- `resume(self)`
- `read_global_capture(self)`
- `set_fixture(self, capture_fixture: CaptureFixture[Any])`
- `unset_fixture(self)`
- `activate_fixture(self)`
- `deactivate_fixture(self)`
- `suspend_fixture(self)`
- `resume_fixture(self)`
- `global_and_fixture_disabled(self)`
- `item_capture(self, when: str, item: Item)`
- `pytest_make_collect_report(
        self, collector: Collector
    )`
- `pytest_runtest_setup(self, item: Item)`
- `pytest_runtest_call(self, item: Item)`
- `pytest_runtest_teardown(self, item: Item)`
- `pytest_keyboard_interrupt(self)`
- `pytest_internalerror(self)`
- `__init__(
        self,
        captureclass: type[CaptureBase[AnyStr]],
        request: SubRequest,
        *,
        config: dict[str, Any] | None = None,
        _ispytest: bool = False,
    )`
- `_start(self)`
- `close(self)`
- `readouterr(self)`
- `_suspend(self)`
- `_resume(self)`
- `_is_started(self)`
- `disabled(self)`
- `capsys(request: SubRequest)`
- `test_output(capsys)`
- `capteesys(request: SubRequest)`
- `test_output(capteesys)`
- `capsysbinary(request: SubRequest)`
- `test_output(capsysbinary)`
- `capfd(request: SubRequest)`
- `test_system_echo(capfd)`
- `capfdbinary(request: SubRequest)`
- `test_system_echo(capfdbinary)`

#### Parameters / Constants
- `EMPTY_BUFFER` = `""`
- `EMPTY_BUFFER` = `b""`
- `EMPTY_BUFFER` = `""`
- `EMPTY_BUFFER` = `b""`
- `EMPTY_BUFFER` = `""`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/compat.py`

#### Classes
- `NotSetType`
- `CallableBool`

#### Functions
- `legacy_path(path: str | os.PathLike[str])`
- `iscoroutinefunction(func: object)`
- `is_async_function(func: object)`
- `signature(obj: Callable[..., Any])`
- `getlocation(function, curdir: str | os.PathLike[str] | None = None)`
- `num_mock_patch_args(function)`
- `getfuncargnames(
    function: Callable[..., object],
    *,
    name: str = "",
    cls: type | None = None,
)`
- `get_default_arg_names(function: Callable[..., Any])`
- `ascii_escaped(val: bytes | str)`
- `get_real_func(obj)`
- `getimfunc(func)`
- `safe_getattr(object: Any, name: str, default: Any)`
- `safe_isclass(obj: object)`
- `get_user_id()`
- `assert_never(value: NoReturn)`
- `__init__(self, value: bool)`
- `__bool__(self)`
- `__call__(self)`
- `running_on_ci()`
- `deprecated(msg, /, *, category=None, stacklevel=1)`
- `decorator(func)`

#### Parameters / Constants
- `LEGACY_PATH` = `py.path. local`
- `ERROR` = `-1`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/config/__init__.py`

#### Classes
- `ExitCode`
- `ConftestImportFailure`
- `cmdline`
- `PytestPluginManager`
- `_DeprecatedInicfgProxy`
- `Config`
- `InvocationParams`
- `ArgsSource`

#### Functions
- `__init__(
        self,
        path: pathlib.Path,
        *,
        cause: Exception,
    )`
- `__str__(self)`
- `filter_traceback_for_conftest_import_failure(
    entry: _pytest._code.TracebackEntry,
)`
- `print_conftest_import_error(e: ConftestImportFailure, file: TextIO)`
- `print_usage_error(e: UsageError, file: TextIO)`
- `_get_prog_name(argv: Sequence[str])`
- `main(
    args: list[str] | os.PathLike[str] | None = None,
    plugins: Sequence[str | _PluggyPlugin] | None = None,
)`
- `_main(
    *,
    args: list[str] | os.PathLike[str] | None = None,
    plugins: Sequence[str | _PluggyPlugin] | None = None,
    prog: str,
)`
- `_console_main()`
- `console_main()`
- `filename_arg(path: str, optname: str)`
- `directory_arg(path: str, optname: str)`
- `get_config(
    args: Iterable[str] | None = None,
    plugins: Sequence[str | _PluggyPlugin] | None = None,
    *,
    prog: str | None = None,
)`
- `get_plugin_manager()`
- `_prepareconfig(
    args: list[str] | os.PathLike[str],
    plugins: Sequence[str | _PluggyPlugin] | None = None,
    *,
    prog: str | None = None,
)`
- `_get_directory(path: pathlib.Path)`
- `_get_legacy_hook_marks(
    method: Any,
    hook_type: str,
    opt_names: tuple[str, ...],
)`
- `__init__(self)`
- `parse_hookimpl_opts(
        self, plugin: _PluggyPlugin, name: str
    )`
- `parse_hookspec_opts(self, module_or_class, name: str)`
- `register(self, plugin: _PluggyPlugin, name: str | None = None)`
- `getplugin(self, name: str)`
- `hasplugin(self, name: str)`
- `pytest_configure(self, config: Config)`
- `_set_initial_conftests(
        self,
        args: Sequence[str | pathlib.Path],
        pyargs: bool,
        noconftest: bool,
        rootpath: pathlib.Path,
        confcutdir: pathlib.Path | None,
        invocation_dir: pathlib.Path,
        importmode: ImportMode | str,
        *,
        consider_namespace_packages: bool,
    )`
- `_is_in_confcutdir(self, path: pathlib.Path)`
- `_loadconftestmodules(
        self,
        path: pathlib.Path,
        importmode: str | ImportMode,
        rootpath: pathlib.Path,
        *,
        consider_namespace_packages: bool,
    )`
- `_getconftestmodules(self, path: pathlib.Path)`
- `_rget_with_confmod(
        self,
        name: str,
        path: pathlib.Path,
    )`
- `_importconftest(
        self,
        conftestpath: pathlib.Path,
        importmode: str | ImportMode,
        rootpath: pathlib.Path,
        *,
        consider_namespace_packages: bool,
    )`
- `_check_non_top_pytest_plugins(
        self,
        mod: types.ModuleType,
        conftestpath: pathlib.Path,
    )`
- `consider_preparse(
        self, args: Sequence[str], *, exclude_only: bool = False
    )`
- `consider_pluginarg(self, arg: str)`
- `consider_conftest(
        self, conftestmodule: types.ModuleType, registration_name: str
    )`
- `consider_env(self)`
- `consider_module(self, mod: types.ModuleType)`
- `_import_plugin_specs(
        self, spec: None | types.ModuleType | str | Sequence[str]
    )`
- `import_plugin(self, modname: str, consider_entry_points: bool = False)`
- `_get_plugin_specs_as_list(
    specs: None | types.ModuleType | str | Sequence[str],
)`
- `_iter_rewritable_modules(package_files: Iterable[str])`
- `__init__(self, config: Config)`
- `__getitem__(self, key: str)`
- `__setitem__(self, key: str, value: Any)`
- `__delitem__(self, key: str)`
- `__iter__(self)`
- `__len__(self)`
- `__init__(
            self,
            *,
            args: Iterable[str],
            plugins: Sequence[str | _PluggyPlugin] | None,
            dir: pathlib.Path,
        )`
- `__init__(
        self,
        pluginmanager: PytestPluginManager,
        *,
        invocation_params: InvocationParams | None = None,
        prog: str | None = None,
    )`
- `inicfg(self)`
- `inicfg(self)`
- `rootpath(self)`
- `inipath(self)`
- `add_cleanup(self, func: Callable[[], None])`
- `_do_configure(self)`
- `_ensure_unconfigure(self)`
- `get_terminal_writer(self)`
- `pytest_cmdline_parse(
        self, pluginmanager: PytestPluginManager, args: list[str]
    )`
- `notify_exception(
        self,
        excinfo: ExceptionInfo[BaseException],
        option: argparse.Namespace | None = None,
    )`
- `cwd_relative_nodeid(self, nodeid: str)`
- `fromdictargs(cls, option_dict: Mapping[str, Any], args: list[str])`
- `_processopt(self, opt: Argument)`
- `pytest_load_initial_conftests(self, early_config: Config)`
- `_consider_importhook(self)`
- `_mark_plugins_for_rewrite(
        self, hook: AssertionRewritingHook, disable_autoload: bool
    )`
- `_configure_python_path(self)`
- `_unconfigure_python_path(self)`
- `_validate_args(self, args: list[str], via: str)`
- `_decide_args(
        self,
        *,
        args: list[str],
        pyargs: bool,
        testpaths: list[str],
        invocation_dir: pathlib.Path,
        rootpath: pathlib.Path,
        warn: bool,
    )`
- `pytest_collection(self)`
- `_checkversion(self)`
- `_validate_config_options(self)`
- `_validate_plugins(self)`
- `_warn_or_fail_if_strict(self, message: str)`
- `_get_unknown_ini_keys(self)`
- `parse(self, args: list[str], addopts: bool = True)`
- `issue_config_time_warning(self, warning: Warning, stacklevel: int)`
- `addinivalue_line(self, name: str, line: str)`
- `getini(self, name: str)`
- `_getini_unknown_type(self, name: str, type: str, value: object)`
- `_getini(self, name: str)`
- `_getini_ini(
        self,
        name: str,
        canonical_name: str,
        type: str,
        value: str | list[str],
        default: Any,
    )`
- `_getini_toml(
        self,
        name: str,
        canonical_name: str,
        type: str,
        value: object,
        default: Any,
    )`
- `_getconftest_pathlist(
        self, name: str, path: pathlib.Path
    )`
- `getoption(self, name: str, default: Any = NOTSET, skip: bool = False)`
- `getvalue(self, name: str, path=None)`
- `getvalueorskip(self, name: str, path=None)`
- `get_verbosity(self, verbosity_type: str | None = None)`
- `_verbosity_ini_name(verbosity_type: str)`
- `_add_verbosity_ini(parser: Parser, verbosity_type: str, help: str)`
- `_warn_about_missing_assertion(self, mode: str)`
- `_warn_about_skipped_plugins(self)`
- `_assertion_supported()`
- `create_terminal_writer(
    config: Config, file: TextIO | None = None
)`
- `_strtobool(val: str)`
- `parse_warning_filter(
    arg: str, *, escape: bool
)`
- `_resolve_warning_category(category: str)`
- `apply_warning_filters(
    config_filters: Iterable[str], cmdline_filters: Iterable[str]
)`

#### Parameters / Constants
- `TESTS_FAILED` = `1`
- `INTERRUPTED` = `2`
- `INTERNAL_ERROR` = `3`
- `USAGE_ERROR` = `4`
- `NO_TESTS_COLLECTED` = `5`
- `MAX_WARNINGS_ERROR` = `6`
- `ARGS` = `enum.auto()`
- `INVOCATION_DIR` = `enum.auto()`
- `INCOVATION_DIR` = `INVOCATION_DIR  # backwards compatibility alias`
- `TESTPATHS` = `enum.auto()`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/config/argparsing.py`

#### Classes
- `Parser`
- `Argument`
- `OptionGroup`
- `PytestArgumentParser`
- `DropShorterLongHelpFormatter`
- `OverrideIniAction`

#### Functions
- `__init__(
        self,
        usage: str | None = None,
        processopt: Callable[[Argument], None] | None = None,
        *,
        prog: str | None = None,
        _ispytest: bool = False,
    )`
- `prog(self)`
- `prog(self, value: str)`
- `processoption(self, option: Argument)`
- `getgroup(
        self, name: str, description: str = "", after: str | None = None
    )`
- `addoption(self, *opts: str, **attrs: Any)`
- `parse(
        self,
        args: Sequence[str | os.PathLike[str]],
        namespace: argparse.Namespace | None = None,
    )`
- `parse_known_args(
        self,
        args: Sequence[str | os.PathLike[str]],
        namespace: argparse.Namespace | None = None,
    )`
- `parse_known_and_unknown_args(
        self,
        args: Sequence[str | os.PathLike[str]],
        namespace: argparse.Namespace | None = None,
    )`
- `addini(
        self,
        name: str,
        help: str,
        type: Literal[
            "string", "paths", "pathlist", "args", "linelist", "bool", "int", "float"
        ]
        | None = None,
        default: Any = NOTSET,
        *,
        aliases: Sequence[str] = ()`
- `get_ini_default_for_type(
    type: Literal[
        "string", "paths", "pathlist", "args", "linelist", "bool", "int", "float"
    ],
)`
- `__init__(self, action: argparse.Action)`
- `attrs(self)`
- `names(self)`
- `dest(self)`
- `default(self)`
- `type(self)`
- `__repr__(self)`
- `__init__(
        self,
        arggroup: argparse._ArgumentGroup,
        name: str,
        parser: Parser | None,
        _ispytest: bool = False,
    )`
- `addoption(self, *opts: str, **attrs: Any)`
- `_addoption(self, *opts: str, **attrs: Any)`
- `_addoption_inner(
        self, opts: tuple[str, ...], attrs: dict[str, Any], allow_reserved: bool
    )`
- `__init__(
        self,
        usage: str | None,
        extra_info: dict[str, str],
        *,
        prog: str | None = None,
    )`
- `error(self, message: str)`
- `__init__(self, *args: Any, **kwargs: Any)`
- `_format_action_invocation(self, action: argparse.Action)`
- `_split_lines(self, text: str, width: int)`
- `__init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        nargs: int | str | None = None,
        *args,
        ini_option: str,
        ini_value: str,
        **kwargs,
    )`
- `__call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        *args,
        **kwargs,
    )`

#### Parameters / Constants
- `FILE_OR_DIR` = `"file_or_dir"`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/config/exceptions.py`

#### Classes
- `UsageError`
- `PrintHelp`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/config/findpaths.py`

#### Classes
- `ConfigValue`

#### Functions
- `_parse_ini_config(path: Path)`
- `load_config_dict_from_file(
    filepath: Path,
)`
- `make_scalar(v: object)`
- `locate_config(
    invocation_dir: Path,
    args: Iterable[Path],
)`
- `get_common_ancestor(
    invocation_dir: Path,
    paths: Iterable[Path],
)`
- `get_dirs_from_args(args: Iterable[str])`
- `is_option(x: str)`
- `get_file_part_from_node_id(x: str)`
- `get_dir_from_path(path: Path)`
- `parse_override_ini(override_ini: Sequence[str] | None)`
- `determine_setup(
    *,
    inifile: str | None,
    override_ini: Sequence[str] | None,
    args: Sequence[str],
    rootdir_cmd_arg: str | None,
    invocation_dir: Path,
)`
- `is_fs_root(p: Path)`

#### Parameters / Constants
- `CFG_PYTEST_SECTION` = `"[pytest] section in {filename} files is no longer supported, change to [tool:pytest] instead."`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/debugging.py`

#### Classes
- `pytestPDB`
- `PytestPdbWrapper`
- `PdbInvoke`
- `PdbTrace`

#### Functions
- `_validate_usepdb_cls(value: str)`
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `fin()`
- `_is_capturing(cls, capman: CaptureManager | None)`
- `_import_pdb_cls(cls, capman: CaptureManager | None)`
- `_get_pdb_wrapper_class(cls, pdb_cls, capman: CaptureManager | None)`
- `do_debug(self, arg)`
- `do_continue(self, arg)`
- `do_quit(self, arg)`
- `setup(self, f, tb)`
- `get_stack(self, f, t)`
- `_init_pdb(cls, method, *args, **kwargs)`
- `set_trace(cls, *args, **kwargs)`
- `pytest_exception_interact(
        self, node: Node, call: CallInfo[Any], report: BaseReport
    )`
- `pytest_internalerror(self, excinfo: ExceptionInfo[BaseException])`
- `pytest_pyfunc_call(self, pyfuncitem)`
- `wrap_pytest_function_for_tracing(pyfuncitem)`
- `wrapper(*args, **kwargs)`
- `maybe_wrap_pytest_function_for_tracing(pyfuncitem)`
- `_enter_pdb(
    node: Node, excinfo: ExceptionInfo[BaseException], rep: BaseReport
)`
- `_postmortem_exc_or_tb(
    excinfo: ExceptionInfo[BaseException],
)`
- `post_mortem(tb_or_exc: types.TracebackType | BaseException)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/deprecated.py`

#### Functions
- `check_ispytest(ispytest: bool)`

#### Parameters / Constants
- `DEPRECATED_EXTERNAL_PLUGINS` = `{`
- `YIELD_FIXTURE` = `PytestDeprecationWarning(`
- `CLASS_FIXTURE_INSTANCE_METHOD` = `PytestRemovedIn10Warning(`
- `PRIVATE` = `PytestDeprecationWarning("A private pytest class or function was used.")`
- `HOOK_LEGACY_MARKING` = `UnformattedWarning(`
- `MONKEYPATCH_LEGACY_NAMESPACE_PACKAGES` = `PytestRemovedIn10Warning(`
- `PARAMETRIZE_NON_COLLECTION_ITERABLE` = `UnformattedWarning(`
- `CONSOLE_MAIN` = `PytestRemovedIn10Warning(`
- `CONFIG_INICFG` = `PytestRemovedIn10Warning(`
- `FIXTURE_GETFIXTUREVALUE_DURING_TEARDOWN` = `UnformattedWarning(`
- `PASTEBIN` = `PytestRemovedIn10Warning(`
- `FIXTURE_BASEID_DEPRECATED` = `PytestRemovedIn10Warning(`
- `FIXTURE_NODEID_DEPRECATED` = `PytestRemovedIn10Warning(`
- `FIXTUREDEF_HAS_LOCATION_DEPRECATED` = `PytestRemovedIn10Warning(`
- `PARSEFACTORIES_NODEID_DEPRECATED` = `PytestRemovedIn10Warning(`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/doctest.py`

#### Classes
- `ReprFailDoctest`
- `MultipleDoctestFailures`
- `PytestDoctestRunner`
- `DoctestItem`
- `DoctestTextfile`
- `DoctestModule`
- `MockAwareDocTestFinder`
- `LiteralsOutputChecker`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_unconfigure()`
- `pytest_collect_file(
    file_path: Path,
    parent: Collector,
)`
- `_is_setup_py(path: Path)`
- `_is_doctest(config: Config, path: Path, parent: Collector)`
- `_is_main_py(path: Path)`
- `__init__(
        self, reprlocation_lines: Sequence[tuple[ReprFileLocation, Sequence[str]]]
    )`
- `toterminal(self, tw: TerminalWriter)`
- `__init__(self, failures: Sequence[doctest.DocTestFailure])`
- `_init_runner_class()`
- `__init__(
            self,
            checker: doctest.OutputChecker | None = None,
            verbose: bool | None = None,
            optionflags: int = 0,
            continue_on_failure: bool = True,
        )`
- `report_failure(
            self,
            out,
            test: doctest.DocTest,
            example: doctest.Example,
            got: str,
        )`
- `report_unexpected_exception(
            self,
            out,
            test: doctest.DocTest,
            example: doctest.Example,
            exc_info: tuple[type[BaseException], BaseException, types.TracebackType],
        )`
- `_get_runner(
    checker: doctest.OutputChecker | None = None,
    verbose: bool | None = None,
    optionflags: int = 0,
    continue_on_failure: bool = True,
)`
- `__init__(
        self,
        name: str,
        parent: DoctestTextfile | DoctestModule,
        runner: doctest.DocTestRunner,
        dtest: doctest.DocTest,
    )`
- `from_parent(  # type: ignore[override]
        cls,
        parent: DoctestTextfile | DoctestModule,
        *,
        name: str,
        runner: doctest.DocTestRunner,
        dtest: doctest.DocTest,
    )`
- `_initrequest(self)`
- `setup(self)`
- `runtest(self)`
- `_disable_output_capturing_for_darwin(self)`
- `repr_failure(  # type: ignore[override]
        self,
        excinfo: ExceptionInfo[BaseException],
    )`
- `reportinfo(self)`
- `_get_flag_lookup()`
- `get_optionflags(config: Config)`
- `_get_continue_on_failure(config: Config)`
- `collect(self)`
- `_check_all_skipped(test: doctest.DocTest)`
- `_is_mocked(obj: object)`
- `_patch_unwrap_mock_aware()`
- `_mock_aware_unwrap(
        func: Callable[..., Any], *, stop: Callable[[Any], Any] | None = None
    )`
- `collect(self)`
- `_find_lineno(self, obj, source_lines)`
- `_from_module(self, module, object)`
- `_init_checker_class()`
- `check_output(self, want: str, got: str, optionflags: int)`
- `remove_prefixes(regex: re.Pattern[str], txt: str)`
- `_remove_unwanted_precision(self, want: str, got: str)`
- `_get_checker()`
- `_get_allow_unicode_flag()`
- `_get_allow_bytes_flag()`
- `_get_number_flag()`
- `_get_report_choice(key: str)`
- `doctest_namespace()`
- `add_np(doctest_namespace)`

#### Parameters / Constants
- `DOCTEST_REPORT_CHOICE_NONE` = `"none"`
- `DOCTEST_REPORT_CHOICE_CDIFF` = `"cdiff"`
- `DOCTEST_REPORT_CHOICE_NDIFF` = `"ndiff"`
- `DOCTEST_REPORT_CHOICE_UDIFF` = `"udiff"`
- `DOCTEST_REPORT_CHOICE_ONLY_FIRST_FAILURE` = `"only_first_failure"`
- `DOCTEST_REPORT_CHOICES` = `(`
- `RUNNER_CLASS` = `None`
- `RUNNER_CLASS` = `None`
- `RUNNER_CLASS` = `_init_runner_class()`
- `DONT_ACCEPT_TRUE_FOR_1` = `doctest.DONT_ACCEPT_TRUE_FOR_1,`
- `DONT_ACCEPT_BLANKLINE` = `doctest.DONT_ACCEPT_BLANKLINE,`
- `NORMALIZE_WHITESPACE` = `doctest.NORMALIZE_WHITESPACE,`
- `ELLIPSIS` = `doctest.ELLIPSIS,`
- `IGNORE_EXCEPTION_DETAIL` = `doctest.IGNORE_EXCEPTION_DETAIL,`
- `COMPARISON_FLAGS` = `doctest.COMPARISON_FLAGS,`
- `ALLOW_UNICODE` = `_get_allow_unicode_flag(),`
- `ALLOW_BYTES` = `_get_allow_bytes_flag(),`
- `NUMBER` = `_get_number_flag(),`
- `CHECKER_CLASS` = `_init_checker_class()`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/faulthandler.py`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `pytest_unconfigure(config: Config)`
- `get_stderr_fileno()`
- `get_timeout_config_value(config: Config)`
- `get_exit_on_timeout_config_value(config: Config)`
- `pytest_runtest_protocol(item: Item)`
- `pytest_enter_pdb()`
- `pytest_exception_interact()`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/fixtures.py`

#### Classes
- `ParamArgKey`
- `FuncFixtureInfo`
- `FixtureRequest`
- `TopRequest`
- `SubRequest`
- `FixtureLookupError`
- `FixtureLookupErrorRepr`
- `FixtureDef`
- `RequestFixtureDef`
- `FixtureFunctionMarker`
- `FixtureFunctionDefinition`
- `FixtureManager`

#### Functions
- `pytest_sessionstart(session: Session)`
- `get_scope_package(
    node: nodes.Item,
    fixturedef: FixtureDef[object],
)`
- `is_visibility_more_specific(
    candidate: FixtureDef[Any], other: FixtureDef[Any]
)`
- `get_scope_node(node: nodes.Node, scope: Scope)`
- `getfixturemarker(obj: object)`
- `get_param_argkeys(item: nodes.Item, scope: Scope)`
- `reorder_items(items: Sequence[nodes.Item])`
- `reorder_items_atscope(
    items: OrderedSet[nodes.Item],
    argkeys_by_item: Mapping[Scope, Mapping[nodes.Item, OrderedSet[ParamArgKey]]],
    items_by_argkey: Mapping[
        Scope, Mapping[ParamArgKey, OrderedDict[nodes.Item, None]]
    ],
    scope: Scope,
)`
- `traverse_fixture_closure(
    initialnames: Iterable[str],
    *,
    getfixturedefs: Callable[[str], Sequence[FixtureDef[Any]] | None],
)`
- `process_argname(argname: str)`
- `prune_dependency_tree(self)`
- `__init__(
        self,
        pyfuncitem: Function,
        fixturename: str | None,
        arg2fixturedefs: Mapping[str, Sequence[FixtureDef[Any]]],
        fixture_defs: dict[str, FixtureDef[Any]],
        *,
        _ispytest: bool = False,
    )`
- `_fixturemanager(self)`
- `_scope(self)`
- `scope(self)`
- `_check_scope(
        self,
        requested_fixturedef: FixtureDef[object],
        requested_scope: Scope,
    )`
- `fixturenames(self)`
- `node(self)`
- `config(self)`
- `function(self)`
- `cls(self)`
- `instance(self)`
- `module(self)`
- `path(self)`
- `keywords(self)`
- `session(self)`
- `addfinalizer(self, finalizer: Callable[[], object])`
- `applymarker(self, marker: str | MarkDecorator)`
- `raiseerror(self, msg: str | None)`
- `_raise_teardown_lookup_error(self, argname: str)`
- `getfixturevalue(self, argname: str)`
- `_iter_chain(self)`
- `_get_active_fixturedef(self, argname: str)`
- `_check_fixturedef_without_param(self, fixturedef: FixtureDef[object])`
- `_get_fixturestack(self)`
- `__init__(self, pyfuncitem: Function, *, _ispytest: bool = False)`
- `_scope(self)`
- `_check_scope(
        self,
        requested_fixturedef: FixtureDef[object],
        requested_scope: Scope,
    )`
- `node(self)`
- `__repr__(self)`
- `_fillfixtures(self)`
- `addfinalizer(self, finalizer: Callable[[], object])`
- `__init__(
        self,
        request: FixtureRequest,
        scope: Scope,
        param: Any,
        param_index: int,
        fixturedef: FixtureDef[object],
        *,
        _ispytest: bool = False,
    )`
- `__repr__(self)`
- `_scope(self)`
- `node(self)`
- `_check_scope(
        self,
        requested_fixturedef: FixtureDef[object],
        requested_scope: Scope,
    )`
- `_format_fixturedef_line(self, fixturedef: FixtureDef[object])`
- `addfinalizer(self, finalizer: Callable[[], object])`
- `__init__(
        self, argname: str | None, request: FixtureRequest, msg: str | None = None
    )`
- `formatrepr(self)`
- `__init__(
        self,
        filename: str | os.PathLike[str],
        firstlineno: int,
        tblines: Sequence[str],
        errorstring: str,
        argname: str | None,
    )`
- `toterminal(self, tw: TerminalWriter)`
- `call_fixture_func(
    fixturefunc: _FixtureFunc[FixtureValue], request: FixtureRequest, kwargs
)`
- `_teardown_yield_fixture(fixturefunc, it)`
- `_eval_scope_callable(
    scope_callable: Callable[[str, Config], ScopeName],
    fixture_name: str,
    config: Config,
)`
- `__init__(
        self,
        config: Config,
        baseid: str | None | NotSetType,
        argname: str,
        func: _FixtureFunc[FixtureValue],
        scope: Scope | ScopeName | Callable[[str, Config], ScopeName] | None,
        params: Sequence[object] | None,
        ids: tuple[object | None, ...] | Callable[[Any], object | None] | None = None,
        *,
        node: nodes.Node | NotSetType = NOTSET,
        # only used in a deprecationwarning msg, can be removed in pytest9
        _autouse: bool = False,
        _ispytest: bool = False,
    )`
- `scope(self)`
- `has_location(self)`
- `addfinalizer(self, finalizer: Callable[[], object])`
- `finish(self, request: SubRequest)`
- `execute(self, request: SubRequest)`
- `cache_key(self, request: SubRequest)`
- `__repr__(self)`
- `__init__(self, request: FixtureRequest)`
- `addfinalizer(self, finalizer: Callable[[], object])`
- `resolve_fixture_function(
    fixturedef: FixtureDef[FixtureValue], request: FixtureRequest
)`
- `pytest_fixture_setup(
    fixturedef: FixtureDef[FixtureValue], request: SubRequest
)`
- `__post_init__(self, _ispytest: bool)`
- `__call__(self, function: FixtureFunction)`
- `__init__(
        self,
        *,
        function: Callable[..., Any],
        fixture_function_marker: FixtureFunctionMarker,
        instance: object | None = None,
        _ispytest: bool = False,
    )`
- `__repr__(self)`
- `__get__(self, instance, owner=None)`
- `__call__(self, *args: Any, **kwds: Any)`
- `_get_wrapped_function(self)`
- `fixture(
    fixture_function: Callable[..., object],
    *,
    scope: ScopeName | Callable[[str, Config], ScopeName] = ...,
    params: Iterable[object] | None = ...,
    autouse: bool = ...,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = ...,
    name: str | None = ...,
)`
- `fixture(
    fixture_function: None = ...,
    *,
    scope: ScopeName | Callable[[str, Config], ScopeName] = ...,
    params: Iterable[object] | None = ...,
    autouse: bool = ...,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = ...,
    name: str | None = None,
)`
- `fixture(
    fixture_function: FixtureFunction | None = None,
    *,
    scope: ScopeName | Callable[[str, Config], ScopeName] = "function",
    params: Iterable[object] | None = None,
    autouse: bool = False,
    ids: Sequence[object | None] | Callable[[Any], object | None] | None = None,
    name: str | None = None,
)`
- `yield_fixture(
    fixture_function=None,
    *args,
    scope="function",
    params=None,
    autouse=False,
    ids=None,
    name=None,
)`
- `pytestconfig(request: FixtureRequest)`
- `test_foo(pytestconfig)`
- `pytest_addoption(parser: Parser)`
- `pytest_cmdline_main(config: Config)`
- `_resolve_args_directness(
    argnames: Sequence[str],
    indirect: bool | Sequence[str],
    nodeid: str,
)`
- `_get_direct_parametrize_args(node: nodes.Node)`
- `deduplicate_names(*seqs: Iterable[str])`
- `__init__(self, session: Session)`
- `getfixtureinfo(
        self,
        node: nodes.Item,
        func: Callable[..., object] | None,
        cls: type | None,
    )`
- `pytest_plugin_registered(self, plugin: _PluggyPlugin, plugin_name: str)`
- `pytest_make_collect_report(
        self, collector: nodes.Collector
    )`
- `_flush_pending_conftests_to_session(self, session: Session)`
- `pytest_collection_finish(self)`
- `_getautousenames(self, node: nodes.Node)`
- `_getusefixturesnames(self, node: nodes.Item)`
- `getfixtureclosure(
        self,
        parentnode: nodes.Node,
        initialnames: tuple[str, ...],
        ignore_args: AbstractSet[str],
    )`
- `getfixturedefs(argname: str)`
- `sort_by_scope(arg_name: str)`
- `pytest_generate_tests(self, metafunc: Metafunc)`
- `get_parametrize_mark_argnames(mark: Mark)`
- `pytest_collection_modifyitems(self, items: list[nodes.Item])`
- `_register_fixture(
        self,
        *,
        name: str,
        func: _FixtureFunc[object],
        nodeid: str | None | NotSetType = NOTSET,
        scope: Scope | ScopeName | Callable[[str, Config], ScopeName] = "function",
        params: Sequence[object] | None = None,
        ids: tuple[object | None, ...] | Callable[[Any], object | None] | None = None,
        autouse: bool = False,
        node: nodes.Node | NotSetType = NOTSET,
    )`
- `parsefactories(
        self,
        node_or_obj: nodes.Node,
    )`
- `parsefactories(
        self,
        node_or_obj: object,
        nodeid: str | None,
    )`
- `parsefactories(
        self,
        node_or_obj: NotSetType = ...,
        nodeid: NotSetType = ...,
        *,
        holder: object,
        node: nodes.Node,
    )`
- `parsefactories(
        self,
        node_or_obj: nodes.Node | object | NotSetType = NOTSET,
        nodeid: str | None | NotSetType = NOTSET,
        *,
        holder: object | NotSetType = NOTSET,
        node: nodes.Node | NotSetType = NOTSET,
    )`
- `getfixturedefs(
        self, argname: str, node: nodes.Node
    )`
- `_matchfactories(
        self, fixturedefs: Iterable[FixtureDef[Any]], node: nodes.Node
    )`
- `show_fixtures_per_test(config: Config)`
- `_pretty_fixture_path(invocation_dir: Path, func)`
- `_get_fixtures_per_test(test: nodes.Item)`
- `_show_fixtures_per_test(config: Config, session: Session)`
- `get_best_relpath(func)`
- `write_fixture(fixture_def: FixtureDef[object])`
- `write_item(item: nodes.Item)`
- `showfixtures(config: Config)`
- `_showfixtures_main(config: Config, session: Session)`
- `write_docstring(tw: TerminalWriter, doc: str, indent: str = "    ")`
- `register_fixture(
    *,
    name: str,
    func: _FixtureFunc[object],
    node: nodes.Node,
    scope: ScopeName | Callable[[str, Config], ScopeName] = "function",
    params: Sequence[object] | None = None,
    ids: tuple[object | None, ...] | Callable[[Any], object | None] | None = None,
    autouse: bool = False,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/freeze_support.py`

#### Functions
- `freeze_includes()`
- `_iter_all_modules(
    package: str | types.ModuleType,
    prefix: str = "",
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/helpconfig.py`

#### Classes
- `HelpAction`

#### Functions
- `__init__(
        self, option_strings: Sequence[str], dest: str, *, help: str | None = None
    )`
- `__call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    )`
- `pytest_addoption(parser: Parser)`
- `pytest_cmdline_parse()`
- `unset_tracing()`
- `show_version_verbose(config: Config)`
- `pytest_cmdline_main(config: Config)`
- `showhelp(config: Config)`
- `getpluginversioninfo(config: Config)`
- `pytest_report_header(config: Config)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/hookspec.py`

#### Functions
- `pytest_addhooks(pluginmanager: PytestPluginManager)`
- `pytest_plugin_registered(
    plugin: _PluggyPlugin,
    plugin_name: str,
    manager: PytestPluginManager,
)`
- `pytest_addoption(parser: Parser, pluginmanager: PytestPluginManager)`
- `pytest_configure(config: Config)`
- `pytest_cmdline_parse(
    pluginmanager: PytestPluginManager, args: list[str]
)`
- `pytest_load_initial_conftests(
    early_config: Config, parser: Parser, args: list[str]
)`
- `pytest_cmdline_main(config: Config)`
- `pytest_collection(session: Session)`
- `pytest_collection_modifyitems(
    session: Session, config: Config, items: list[Item]
)`
- `pytest_collection_finish(session: Session)`
- `pytest_ignore_collect(collection_path: Path, config: Config)`
- `pytest_collect_directory(path: Path, parent: Collector)`
- `pytest_collect_file(file_path: Path, parent: Collector)`
- `pytest_collectstart(collector: Collector)`
- `pytest_itemcollected(item: Item)`
- `pytest_collectreport(report: CollectReport)`
- `pytest_deselected(items: Sequence[Item])`
- `pytest_make_collect_report(collector: Collector)`
- `pytest_pycollect_makemodule(module_path: Path, parent)`
- `pytest_pycollect_makeitem(
    collector: Module | Class, name: str, obj: object
)`
- `pytest_pyfunc_call(pyfuncitem: Function)`
- `pytest_generate_tests(metafunc: Metafunc)`
- `pytest_make_parametrize_id(config: Config, val: object, argname: str)`
- `pytest_runtestloop(session: Session)`
- `pytest_runtest_protocol(item: Item, nextitem: Item | None)`
- `pytest_runtest_logstart(nodeid: str, location: tuple[str, int | None, str])`
- `pytest_runtest_logfinish(
    nodeid: str, location: tuple[str, int | None, str]
)`
- `pytest_runtest_setup(item: Item)`
- `pytest_runtest_call(item: Item)`
- `pytest_runtest_teardown(item: Item, nextitem: Item | None)`
- `pytest_runtest_makereport(item: Item, call: CallInfo[None])`
- `pytest_runtest_logreport(report: TestReport)`
- `pytest_report_to_serializable(
    config: Config,
    report: CollectReport | TestReport,
)`
- `pytest_report_from_serializable(
    config: Config,
    data: dict[str, Any],
)`
- `pytest_fixture_setup(
    fixturedef: FixtureDef[Any], request: SubRequest
)`
- `pytest_fixture_post_finalizer(
    fixturedef: FixtureDef[Any], request: SubRequest
)`
- `pytest_sessionstart(session: Session)`
- `pytest_sessionfinish(
    session: Session,
    exitstatus: int | ExitCode,
)`
- `pytest_unconfigure(config: Config)`
- `pytest_assertrepr_compare(
    config: Config, op: str, left: object, right: object
)`
- `pytest_assertion_pass(item: Item, lineno: int, orig: str, expl: str)`
- `pytest_report_header(config: Config, start_path: Path)`
- `pytest_report_collectionfinish(  # type: ignore[empty-body]
    config: Config,
    start_path: Path,
    items: Sequence[Item],
)`
- `pytest_report_teststatus(  # type:ignore[empty-body]
    report: CollectReport | TestReport, config: Config
)`
- `pytest_terminal_summary(
    terminalreporter: TerminalReporter,
    exitstatus: ExitCode,
    config: Config,
)`
- `pytest_warning_recorded(
    warning_message: warnings.WarningMessage,
    when: Literal["config", "collect", "runtest"],
    nodeid: str,
    location: tuple[str, int, str] | None,
)`
- `pytest_markeval_namespace(  # type:ignore[empty-body]
    config: Config,
)`
- `pytest_internalerror(
    excrepr: ExceptionRepr,
    excinfo: ExceptionInfo[BaseException],
)`
- `pytest_keyboard_interrupt(
    excinfo: ExceptionInfo[KeyboardInterrupt | Exit],
)`
- `pytest_exception_interact(
    node: Item | Collector,
    call: CallInfo[Any],
    report: CollectReport | TestReport,
)`
- `pytest_enter_pdb(config: Config, pdb: pdb.Pdb)`
- `pytest_leave_pdb(config: Config, pdb: pdb.Pdb)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/junitxml.py`

#### Classes
- `_NodeReporter`
- `LogXML`

#### Functions
- `bin_xml_escape(arg: object)`
- `repl(matchobj: re.Match[str])`
- `merge_family(left, right)`
- `__init__(self, nodeid: str | TestReport, xml: LogXML)`
- `append(self, node: ET.Element)`
- `add_property(self, name: str, value: object)`
- `add_attribute(self, name: str, value: object)`
- `make_properties_node(self)`
- `record_testreport(self, testreport: TestReport)`
- `to_xml(self)`
- `_add_simple(self, tag: str, message: str, data: str | None = None)`
- `write_captured_output(self, report: TestReport)`
- `_prepare_content(self, content: str, header: str)`
- `_write_content(self, report: TestReport, content: str, jheader: str)`
- `append_pass(self, report: TestReport)`
- `append_failure(self, report: TestReport)`
- `append_collect_error(self, report: TestReport)`
- `append_collect_skipped(self, report: TestReport)`
- `append_error(self, report: TestReport)`
- `append_skipped(self, report: TestReport)`
- `finalize(self)`
- `_warn_incompatibility_with_xunit2(
    request: FixtureRequest, fixture_name: str
)`
- `record_property(request: FixtureRequest)`
- `test_function(record_property)`
- `append_property(name: str, value: object)`
- `record_xml_attribute(request: FixtureRequest)`
- `add_attr_noop(name: str, value: object)`
- `_check_record_param_type(param: str, v: str)`
- `record_testsuite_property(request: FixtureRequest)`
- `test_foo(record_testsuite_property)`
- `record_func(name: str, value: object)`
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `pytest_unconfigure(config: Config)`
- `mangle_test_address(address: str)`
- `__init__(
        self,
        logfile,
        prefix: str | None,
        suite_name: str = "pytest",
        logging: str = "no",
        report_duration: str = "total",
        family="xunit1",
        log_passing_tests: bool = True,
    )`
- `finalize(self, report: TestReport)`
- `node_reporter(self, report: TestReport | str)`
- `add_stats(self, key: str)`
- `_opentestcase(self, report: TestReport)`
- `pytest_runtest_logreport(self, report: TestReport)`
- `update_testcase_duration(self, report: TestReport)`
- `pytest_collectreport(self, report: TestReport)`
- `pytest_internalerror(self, excrepr: ExceptionRepr)`
- `pytest_sessionstart(self)`
- `pytest_sessionfinish(self)`
- `pytest_terminal_summary(
        self, terminalreporter: TerminalReporter, config: pytest.Config
    )`
- `add_global_property(self, name: str, value: object)`
- `_get_global_properties_node(self)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/legacypath.py`

#### Classes
- `Testdir`
- `LegacyTestdirPlugin`
- `TempdirFactory`
- `LegacyTmpdirPlugin`

#### Functions
- `__init__(self, pytester: Pytester, *, _ispytest: bool = False)`
- `tmpdir(self)`
- `test_tmproot(self)`
- `request(self)`
- `plugins(self)`
- `plugins(self, plugins)`
- `monkeypatch(self)`
- `make_hook_recorder(self, pluginmanager)`
- `chdir(self)`
- `finalize(self)`
- `makefile(self, ext, *args, **kwargs)`
- `makeconftest(self, source)`
- `makeini(self, source)`
- `getinicfg(self, source: str)`
- `makepyprojecttoml(self, source)`
- `makepyfile(self, *args, **kwargs)`
- `maketxtfile(self, *args, **kwargs)`
- `syspathinsert(self, path=None)`
- `mkdir(self, name)`
- `mkpydir(self, name)`
- `copy_example(self, name=None)`
- `getnode(self, config: Config, arg)`
- `getpathnode(self, path)`
- `genitems(self, colitems: list[Item | Collector])`
- `runitem(self, source)`
- `inline_runsource(self, source, *cmdlineargs)`
- `inline_genitems(self, *args)`
- `inline_run(self, *args, plugins=()`
- `runpytest_inprocess(self, *args, **kwargs)`
- `runpytest(self, *args, **kwargs)`
- `parseconfig(self, *args)`
- `parseconfigure(self, *args)`
- `getitem(self, source, funcname="test_func")`
- `getitems(self, source)`
- `getmodulecol(self, source, configargs=()`
- `collect_by_name(self, modcol: Collector, name: str)`
- `popen(
        self,
        cmdargs,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=CLOSE_STDIN,
        **kw,
    )`
- `run(self, *cmdargs, timeout=None, stdin=CLOSE_STDIN)`
- `runpython(self, script)`
- `runpython_c(self, command)`
- `runpytest_subprocess(self, *args, timeout=None)`
- `spawn_pytest(self, string: str, expect_timeout: float = 10.0)`
- `spawn(self, cmd: str, expect_timeout: float = 10.0)`
- `__repr__(self)`
- `__str__(self)`
- `testdir(pytester: Pytester)`
- `__init__(
        self, tmppath_factory: TempPathFactory, *, _ispytest: bool = False
    )`
- `mktemp(self, basename: str, numbered: bool = True)`
- `getbasetemp(self)`
- `tmpdir_factory(request: FixtureRequest)`
- `tmpdir(tmp_path: Path)`
- `Cache_makedir(self: Cache, name: str)`
- `FixtureRequest_fspath(self: FixtureRequest)`
- `TerminalReporter_startdir(self: TerminalReporter)`
- `Config_invocation_dir(self: Config)`
- `Config_rootdir(self: Config)`
- `Config_inifile(self: Config)`
- `Session_startdir(self: Session)`
- `Config__getini_unknown_type(self, name: str, type: str, value: str | list[str])`
- `Node_fspath(self: Node)`
- `Node_fspath_set(self: Node, value: LEGACY_PATH)`
- `pytest_load_initial_conftests(early_config: Config)`
- `pytest_configure(config: Config)`
- `pytest_plugin_registered(plugin: object, manager: PytestPluginManager)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/logging.py`

#### Classes
- `DatetimeFormatter`
- `ColoredLevelFormatter`
- `PercentStyleMultiline`
- `catching_logs`
- `LogCaptureHandler`
- `LogCaptureFixture`
- `LoggingPlugin`
- `_FileHandler`
- `_LiveLoggingStreamHandler`
- `_LiveLoggingNullHandler`

#### Functions
- `_remove_ansi_escape_sequences(text: str)`
- `formatTime(self, record: LogRecord, datefmt: str | None = None)`
- `__init__(self, terminalwriter: TerminalWriter, *args, **kwargs)`
- `add_color_level(self, level: int, *color_opts: str)`
- `format(self, record: logging.LogRecord)`
- `__init__(self, fmt: str, auto_indent: int | str | bool | None)`
- `_get_auto_indent(auto_indent_option: int | str | bool | None)`
- `format(self, record: logging.LogRecord)`
- `get_option_ini(config: Config, *names: str)`
- `pytest_addoption(parser: Parser)`
- `add_option_ini(option, dest, default=None, type=None, **kwargs)`
- `__init__(self, handler: _HandlerType, level: int | None = None)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `__init__(self)`
- `emit(self, record: logging.LogRecord)`
- `reset(self)`
- `clear(self)`
- `handleError(self, record: logging.LogRecord)`
- `__init__(self, item: nodes.Node, *, _ispytest: bool = False)`
- `_finalize(self)`
- `handler(self)`
- `get_records(
        self, when: Literal["setup", "call", "teardown"]
    )`
- `text(self)`
- `records(self)`
- `record_tuples(self)`
- `messages(self)`
- `clear(self)`
- `_force_enable_logging(
        self, level: int | str, logger_obj: logging.Logger
    )`
- `set_level(self, level: int | str, logger: str | None = None)`
- `at_level(self, level: int | str, logger: str | None = None)`
- `filtering(self, filter_: logging.Filter)`
- `caplog(request: FixtureRequest)`
- `get_log_level_for_setting(config: Config, *setting_names: str)`
- `pytest_configure(config: Config)`
- `__init__(self, config: Config)`
- `_disable_loggers(self, loggers_to_disable: list[str])`
- `_create_formatter(self, log_format, log_date_format, auto_indent)`
- `set_log_path(self, fname: str)`
- `_log_cli_enabled(self)`
- `pytest_sessionstart(self)`
- `pytest_collection(self)`
- `pytest_runtestloop(self, session: Session)`
- `pytest_runtest_logstart(self)`
- `pytest_runtest_logreport(self)`
- `_runtest_for(self, item: nodes.Item, when: str)`
- `pytest_runtest_setup(self, item: nodes.Item)`
- `pytest_runtest_call(self, item: nodes.Item)`
- `pytest_runtest_teardown(self, item: nodes.Item)`
- `pytest_runtest_logfinish(self)`
- `pytest_sessionfinish(self)`
- `pytest_unconfigure(self)`
- `handleError(self, record: logging.LogRecord)`
- `__init__(
        self,
        terminal_reporter: TerminalReporter,
        capture_manager: CaptureManager | None,
    )`
- `reset(self)`
- `set_when(self, when: str | None)`
- `emit(self, record: logging.LogRecord)`
- `handleError(self, record: logging.LogRecord)`
- `reset(self)`
- `set_when(self, when: str)`
- `handleError(self, record: logging.LogRecord)`

#### Parameters / Constants
- `DEFAULT_LOG_FORMAT` = `"%(levelname)-8s %(name)s:%(filename)s:%(lineno)d %(message)s"`
- `DEFAULT_LOG_DATE_FORMAT` = `"%H:%M:%S"`
- `LEVELNAME_FMT_REGEX` = `re.compile(r"%\(levelname\)([+-.]?\d*(?:\.\d+)?s)")`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/main.py`

#### Classes
- `FSHookProxy`
- `Interrupted`
- `Failed`
- `_bestrelpath_cache`
- `Dir`
- `Session`
- `CollectionArgument`

#### Functions
- `pytest_addoption(parser: Parser)`
- `validate_basetemp(path: str)`
- `is_ancestor(base: Path, query: Path)`
- `wrap_session(
    config: Config, doit: Callable[[Config, Session], int | ExitCode | None]
)`
- `pytest_cmdline_main(config: Config)`
- `_main(config: Config, session: Session)`
- `pytest_collection(session: Session)`
- `pytest_runtestloop(session: Session)`
- `_in_venv(path: Path)`
- `pytest_ignore_collect(collection_path: Path, config: Config)`
- `pytest_collect_directory(
    path: Path, parent: nodes.Collector
)`
- `pytest_collection_modifyitems(items: list[nodes.Item], config: Config)`
- `__init__(
        self,
        pm: PytestPluginManager,
        remove_mods: AbstractSet[object],
    )`
- `__getattr__(self, name: str)`
- `__missing__(self, path: Path)`
- `from_parent(  # type: ignore[override]
        cls,
        parent: nodes.Collector,
        *,
        path: Path,
    )`
- `collect(self)`
- `__init__(self, config: Config)`
- `from_config(cls, config: Config)`
- `__repr__(self)`
- `shouldstop(self)`
- `shouldstop(self, value: bool | str)`
- `shouldfail(self)`
- `shouldfail(self, value: bool | str)`
- `startpath(self)`
- `_node_location_to_relpath(self, node_path: Path)`
- `pytest_collectstart(self)`
- `pytest_runtest_logreport(self, report: TestReport | CollectReport)`
- `isinitpath(
        self,
        path: str | os.PathLike[str],
        *,
        with_parents: bool = False,
    )`
- `gethookproxy(self, fspath: os.PathLike[str])`
- `_collect_path(
        self,
        path: Path,
        path_cache: dict[Path, Sequence[nodes.Collector]],
    )`
- `perform_collect(
        self, args: Sequence[str] | None = ..., genitems: Literal[True] = ...
    )`
- `perform_collect(
        self, args: Sequence[str] | None = ..., genitems: bool = ...
    )`
- `perform_collect(
        self, args: Sequence[str] | None = None, genitems: bool = True
    )`
- `_collect_one_node(
        self,
        node: nodes.Collector,
        handle_dupes: bool = True,
    )`
- `collect(self)`
- `genitems(self, node: nodes.Item | nodes.Collector)`
- `search_pypath(
    module_name: str, *, consider_namespace_packages: bool = False
)`
- `resolve_collection_argument(
    invocation_path: Path,
    arg: str,
    arg_index: int,
    *,
    as_pypath: bool = False,
    consider_namespace_packages: bool = False,
)`
- `is_collection_argument_subsumed_by(
    arg: CollectionArgument, by: CollectionArgument
)`
- `normalize_collection_arguments(
    collection_args: Sequence[CollectionArgument],
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/mark/__init__.py`

#### Classes
- `KeywordMatcher`
- `MarkMatcher`

#### Functions
- `param(
    *values: object,
    marks: MarkDecorator | Collection[MarkDecorator | Mark] = ()`
- `test_eval(test_input, expected)`
- `pytest_addoption(parser: Parser)`
- `pytest_cmdline_main(config: Config)`
- `from_item(cls, item: Item)`
- `__call__(self, subname: str, /, **kwargs: str | int | bool | None)`
- `deselect_by_keyword(items: list[Item], config: Config)`
- `from_markers(cls, markers: Iterable[Mark])`
- `__call__(self, name: str, /, **kwargs: str | int | bool | None)`
- `deselect_by_mark(items: list[Item], config: Config)`
- `_parse_expression(expr: str, exc_message: str)`
- `pytest_collection_modifyitems(items: list[Item], config: Config)`
- `pytest_configure(config: Config)`
- `pytest_unconfigure(config: Config)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/mark/expression.py`

#### Classes
- `TokenType`
- `Token`
- `Scanner`
- `ExpressionMatcher`
- `MatcherNameAdapter`
- `MatcherAdapter`
- `Expression`

#### Functions
- `__init__(self, input: str)`
- `lex(self, input: str)`
- `accept(self, type: TokenType, *, reject: Literal[True])`
- `accept(
        self, type: TokenType, *, reject: Literal[False] = False
    )`
- `accept(self, type: TokenType, *, reject: bool = False)`
- `reject(self, expected: Sequence[TokenType])`
- `expression(s: Scanner)`
- `expr(s: Scanner)`
- `and_expr(s: Scanner)`
- `not_expr(s: Scanner)`
- `single_kwarg(s: Scanner)`
- `all_kwargs(s: Scanner)`
- `matcher(name: str, /, **kwargs: str | int | bool | None)`
- `__call__(self, name: str, /, **kwargs: str | int | bool | None)`
- `__bool__(self)`
- `__call__(self, **kwargs: str | int | bool | None)`
- `__init__(self, matcher: ExpressionMatcher)`
- `__getitem__(self, key: str)`
- `__iter__(self)`
- `__len__(self)`
- `__init__(self, input: str, code: types.CodeType)`
- `compile(cls, input: str)`
- `evaluate(self, matcher: ExpressionMatcher)`

#### Parameters / Constants
- `LPAREN` = `"left parenthesis"`
- `RPAREN` = `"right parenthesis"`
- `AND` = `"and"`
- `NOT` = `"not"`
- `IDENT` = `"identifier"`
- `EOF` = `"end of input"`
- `EQUAL` = `"="`
- `STRING` = `"string literal"`
- `COMMA` = `","`
- `IDENT_PREFIX` = `"$"`
- `BUILTIN_MATCHERS` = `{"True": True, "False": False, "None": None}`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/mark/structures.py`

#### Classes
- `_HiddenParam`
- `ParameterSet`
- `Mark`
- `MarkDecorator`
- `_SkipMarkDecorator`
- `_SkipifMarkDecorator`
- `_XfailMarkDecorator`
- `_ParametrizeMarkDecorator`
- `_UsefixturesMarkDecorator`
- `_FilterwarningsMarkDecorator`
- `MarkGenerator`
- `NodeKeywords`

#### Functions
- `istestfunc(func)`
- `get_empty_parameterset_mark(
    config: Config, argnames: Sequence[str], func
)`
- `param(
        cls,
        *values: object,
        marks: MarkDecorator | Collection[MarkDecorator | Mark] = ()`
- `extract_from(
        cls,
        parameterset: ParameterSet | Sequence[object] | object,
        force_tuple: bool = False,
    )`
- `_parse_parametrize_args(
        argnames: str | Sequence[str],
        argvalues: Iterable[ParameterSet | Sequence[object] | object],
        *args,
        **kwargs,
    )`
- `_parse_parametrize_parameters(
        argvalues: Iterable[ParameterSet | Sequence[object] | object],
        force_tuple: bool,
    )`
- `_for_parametrize(
        cls,
        argnames: str | Sequence[str],
        argvalues: Iterable[ParameterSet | Sequence[object] | object],
        func,
        config: Config,
        nodeid: str,
    )`
- `__init__(
        self,
        name: str,
        args: tuple[Any, ...],
        kwargs: Mapping[str, Any],
        param_ids_from: Mark | None = None,
        param_ids_generated: Sequence[str] | None = None,
        *,
        _ispytest: bool = False,
    )`
- `_has_param_ids(self)`
- `combined_with(self, other: Mark)`
- `test_function()`
- `__init__(self, mark: Mark, *, _ispytest: bool = False)`
- `name(self)`
- `args(self)`
- `kwargs(self)`
- `markname(self)`
- `with_args(self, *args: object, **kwargs: object)`
- `__call__(self, arg: Markable)`
- `__call__(self, *args: object, **kwargs: object)`
- `__call__(self, *args: object, **kwargs: object)`
- `get_unpacked_marks(
    obj: object | type,
    *,
    consider_mro: bool = True,
)`
- `normalize_mark_list(
    mark_list: Iterable[Mark | MarkDecorator],
)`
- `store_mark(obj, mark: Mark)`
- `__call__(self, arg: Markable)`
- `__call__(self, reason: str = ...)`
- `__call__(  # type: ignore[override]
            self,
            condition: str | bool = ...,
            *conditions: str | bool,
            reason: str = ...,
        )`
- `__call__(self, arg: Markable)`
- `__call__(
            self,
            condition: str | bool = True,
            *conditions: str | bool,
            reason: str = ...,
            run: bool = ...,
            raises: None
            | type[BaseException]
            | tuple[type[BaseException], ...]
            | AbstractRaises[BaseException] = ...,
            strict: bool = ...,
        )`
- `__call__(  # type: ignore[override]
            self,
            argnames: str | Sequence[str],
            argvalues: Iterable[ParameterSet | Sequence[object] | object],
            # TODO(pytest10)`
- `__call__(self, *fixtures: str)`
- `__call__(self, *filters: str)`
- `test_function()`
- `__init__(self, *, _ispytest: bool = False)`
- `__getattr__(self, name: str)`
- `__init__(self, node: Node)`
- `__getitem__(self, key: str)`
- `__setitem__(self, key: str, value: Any)`
- `__contains__(self, key: object)`
- `update(  # type: ignore[override]
        self,
        other: Mapping[str, Any] | Iterable[tuple[str, Any]] = ()`
- `__delitem__(self, key: str)`
- `__iter__(self)`
- `__len__(self)`
- `__repr__(self)`

#### Parameters / Constants
- `EMPTY_PARAMETERSET_OPTION` = `"empty_parameter_set_mark"`
- `HIDDEN_PARAM` = `_HiddenParam.token`
- `MARK_GEN` = `MarkGenerator(_ispytest=True)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/monkeypatch.py`

#### Classes
- `MonkeyPatch`

#### Functions
- `monkeypatch()`
- `resolve(name: str)`
- `annotated_getattr(obj: object, name: str, ann: str)`
- `derive_importpath(import_path: str, raising: bool)`
- `__init__(self)`
- `context(cls)`
- `test_partial(monkeypatch)`
- `setattr(
        self,
        target: str,
        name: object,
        value: NotSetType = ...,
        raising: bool = ...,
    )`
- `setattr(
        self,
        target: object,
        name: str,
        value: object,
        raising: bool = ...,
    )`
- `setattr(
        self,
        target: str | object,
        name: object | str,
        value: object = NOTSET,
        raising: bool = True,
    )`
- `delattr(
        self,
        target: object | str,
        name: str | NotSetType = NOTSET,
        raising: bool = True,
    )`
- `setitem(self, dic: Mapping[K, V], name: K, value: V)`
- `delitem(self, dic: Mapping[K, V], name: K, raising: bool = True)`
- `setenv(self, name: str, value: str, prepend: str | None = None)`
- `delenv(self, name: str, raising: bool = True)`
- `syspath_prepend(self, path)`
- `chdir(self, path: str | os.PathLike[str])`
- `undo(self)`

#### Parameters / Constants
- `RE_IMPORT_ERROR_NAME` = `re.compile(r"^No module named (.*)$")`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/nodes.py`

#### Classes
- `NodeMeta`
- `Node`
- `Collector`
- `CollectError`
- `FSCollector`
- `File`
- `Directory`
- `Item`

#### Functions
- `norm_sep(path: str | os.PathLike[str])`
- `__call__(cls, *k, **kw)`
- `_create(cls: type[_T], *k, **kw)`
- `__init__(
        self,
        name: str,
        parent: Node | None = None,
        config: Config | None = None,
        session: Session | None = None,
        fspath: None = None,
        path: Path | None = None,
        nodeid: str | None = None,
    )`
- `from_parent(cls, parent: Node, **kw)`
- `ihook(self)`
- `__repr__(self)`
- `warn(self, warning: Warning)`
- `nodeid(self)`
- `__hash__(self)`
- `setup(self)`
- `teardown(self)`
- `iter_parents(self)`
- `listchain(self)`
- `add_marker(self, marker: str | MarkDecorator, append: bool = True)`
- `iter_markers(self, name: str | None = None)`
- `iter_markers_with_node(
        self, name: str | None = None
    )`
- `get_closest_marker(self, name: str)`
- `get_closest_marker(self, name: str, default: Mark)`
- `get_closest_marker(self, name: str, default: Mark | None = None)`
- `listextrakeywords(self)`
- `listnames(self)`
- `addfinalizer(self, fin: Callable[[], object])`
- `getparent(self, cls: type[_NodeType])`
- `_traceback_filter(self, excinfo: ExceptionInfo[BaseException])`
- `_repr_failure_py(
        self,
        excinfo: ExceptionInfo[BaseException],
        style: TracebackStyle | None = None,
    )`
- `repr_failure(
        self,
        excinfo: ExceptionInfo[BaseException],
        style: TracebackStyle | None = None,
    )`
- `get_fslocation_from_item(node: Node)`
- `collect(self)`
- `repr_failure(  # type: ignore[override]
        self, excinfo: ExceptionInfo[BaseException]
    )`
- `_traceback_filter(self, excinfo: ExceptionInfo[BaseException])`
- `_check_initialpaths_for_relpath(
    initial_paths: frozenset[Path], path: Path
)`
- `__init__(
        self,
        fspath: None = None,
        path_or_parent: Path | Node | None = None,
        path: Path | None = None,
        name: str | None = None,
        parent: Node | None = None,
        config: Config | None = None,
        session: Session | None = None,
        nodeid: str | None = None,
    )`
- `from_parent(
        cls,
        parent,
        *,
        fspath: None = None,
        path: Path | None = None,
        **kw,
    )`
- `__init__(
        self,
        name,
        parent=None,
        config: Config | None = None,
        session: Session | None = None,
        nodeid: str | None = None,
        **kw,
    )`
- `_check_item_and_collector_diamond_inheritance(self)`
- `runtest(self)`
- `add_report_section(self, when: str, key: str, content: str)`
- `reportinfo(self)`
- `location(self)`

#### Parameters / Constants
- `SEP` = `"/"`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/outcomes.py`

#### Classes
- `OutcomeException`
- `Skipped`
- `Failed`
- `Exit`
- `XFailed`
- `_Exit`
- `_Skip`
- `_Fail`
- `_XFail`

#### Functions
- `__init__(self, msg: str | None = None, pytrace: bool = True)`
- `__repr__(self)`
- `__init__(
        self,
        msg: str | None = None,
        pytrace: bool = True,
        allow_module_level: bool = False,
        *,
        _use_item_location: bool = False,
    )`
- `__init__(
        self, msg: str = "unknown reason", returncode: int | None = None
    )`
- `__call__(self, reason: str = "", returncode: int | None = None)`
- `__call__(self, reason: str = "", allow_module_level: bool = False)`
- `__call__(self, reason: str = "", pytrace: bool = True)`
- `__call__(self, reason: str = "")`
- `importorskip(
    modname: str,
    minversion: str | None = None,
    reason: str | None = None,
    *,
    exc_type: type[ImportError] | None = None,
)`

#### Parameters / Constants
- `TEST_OUTCOME` = `(OutcomeException, Exception)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/pastebin.py`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `tee_write(s, **kwargs)`
- `pytest_unconfigure(config: Config)`
- `create_new_paste(contents: str | bytes)`
- `pytest_terminal_summary(terminalreporter: TerminalReporter)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/pathlib.py`

#### Classes
- `ImportMode`
- `ImportPathMismatchError`
- `CouldNotResolvePathError`

#### Functions
- `_ignore_error(exception: Exception)`
- `get_lock_path(path: _AnyPurePath)`
- `on_rm_rf_error(
    func: Callable[..., Any] | None,
    path: str,
    excinfo: BaseException
    | tuple[type[BaseException], BaseException, types.TracebackType | None],
    *,
    start_path: Path,
)`
- `chmod_rw(p: str)`
- `ensure_extended_length_path(path: Path)`
- `get_extended_length_path_str(path: str)`
- `rm_rf(path: Path)`
- `find_prefixed(root: Path, prefix: str)`
- `extract_suffixes(iter: Iterable[os.DirEntry[str]], prefix: str)`
- `find_suffixes(root: Path, prefix: str)`
- `parse_num(maybe_num: str)`
- `_force_symlink(root: Path, target: str | PurePath, link_to: str | Path)`
- `make_numbered_dir(root: Path, prefix: str, mode: int = 0o700)`
- `create_cleanup_lock(p: Path)`
- `register_cleanup_lock_removal(lock_path: Path, register: Any)`
- `cleanup_on_exit(lock_path: Path = lock_path, original_pid: int = pid)`
- `maybe_delete_a_numbered_dir(path: Path)`
- `ensure_deletable(path: Path, consider_lock_dead_if_created_before: float)`
- `try_cleanup(path: Path, consider_lock_dead_if_created_before: float)`
- `cleanup_candidates(root: Path, prefix: str, keep: int)`
- `cleanup_dead_symlinks(root: Path)`
- `cleanup_numbered_dir(
    root: Path, prefix: str, keep: int, consider_lock_dead_if_created_before: float
)`
- `make_numbered_dir_with_cleanup(
    *,
    root: Path,
    prefix: str,
    mode: int,
    keep: int,
    lock_timeout: float,
    register: Any,
)`
- `resolve_from_str(input: str, rootpath: Path)`
- `fnmatch_ex(pattern: str, path: str | os.PathLike[str])`
- `parts(s: str)`
- `symlink_or_skip(
    src: os.PathLike[str] | str,
    dst: os.PathLike[str] | str,
    **kwargs: Any,
)`
- `import_path(
    path: str | os.PathLike[str],
    *,
    mode: str | ImportMode = ImportMode.prepend,
    root: Path,
    consider_namespace_packages: bool,
)`
- `_import_module_using_spec(
    module_name: str, module_path: Path, *, insert_modules: bool
)`
- `spec_matches_module_path(module_spec: ModuleSpec | None, module_path: Path)`
- `_is_same(f1: str, f2: str)`
- `_is_same(f1: str, f2: str)`
- `module_name_from_path(path: Path, root: Path)`
- `insert_missing_modules(modules: dict[str, ModuleType], module_name: str)`
- `resolve_package_path(path: Path)`
- `resolve_pkg_root_and_module_name(
    path: Path, *, consider_namespace_packages: bool = False
)`
- `is_importable(module_name: str, module_path: Path)`
- `compute_module_name(root: Path, module_path: Path)`
- `scandir(
    path: str | os.PathLike[str],
    sort_key: Callable[[os.DirEntry[str]], object] = lambda entry: entry.name,
)`
- `visit(
    path: str | os.PathLike[str], recurse: Callable[[os.DirEntry[str]], bool]
)`
- `absolutepath(path: str | os.PathLike[str])`
- `commonpath(path1: Path, path2: Path)`
- `bestrelpath(directory: Path, dest: Path)`
- `safe_exists(p: Path)`
- `samefile_nofollow(p1: Path, p2: Path)`

#### Parameters / Constants
- `LOCK_TIMEOUT` = `60 * 60 * 24 * 3`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/pytester.py`

#### Classes
- `LsofFdLeakChecker`
- `PytestArg`
- `RecordedHookCall`
- `HookRecorder`
- `RunResult`
- `SysModulesSnapshot`
- `SysPathsSnapshot`
- `Pytester`
- `TimeoutExpired`
- `PytesterHelperPlugin`
- `reprec`
- `reprec`
- `reprec`
- `LineComp`
- `LineMatcher`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `get_open_files(self)`
- `isopen(line: str)`
- `matching_platform(self)`
- `pytest_runtest_protocol(self, item: Item)`
- `_pytest(request: FixtureRequest)`
- `__init__(self, request: FixtureRequest)`
- `gethookrecorder(self, hook)`
- `get_public_names(values: Iterable[str])`
- `__init__(self, name: str, kwargs)`
- `__repr__(self)`
- `__getattr__(self, key: str)`
- `__init__(
        self, pluginmanager: PytestPluginManager, *, _ispytest: bool = False
    )`
- `before(hook_name: str, hook_impls, kwargs)`
- `after(outcome, hook_name: str, hook_impls, kwargs)`
- `finish_recording(self)`
- `getcalls(self, names: str | Iterable[str])`
- `assert_contains(self, entries: Sequence[tuple[str, str]])`
- `popcall(self, name: str)`
- `getcall(self, name: str)`
- `getreports(
        self,
        names: Literal["pytest_collectreport"],
    )`
- `getreports(
        self,
        names: Literal["pytest_runtest_logreport"],
    )`
- `getreports(
        self,
        names: str | Iterable[str] = (
            "pytest_collectreport",
            "pytest_runtest_logreport",
        )`
- `getreports(
        self,
        names: str | Iterable[str] = (
            "pytest_collectreport",
            "pytest_runtest_logreport",
        )`
- `matchreport(
        self,
        inamepart: str = "",
        names: str | Iterable[str] = (
            "pytest_runtest_logreport",
            "pytest_collectreport",
        )`
- `getfailures(
        self,
        names: Literal["pytest_collectreport"],
    )`
- `getfailures(
        self,
        names: Literal["pytest_runtest_logreport"],
    )`
- `getfailures(
        self,
        names: str | Iterable[str] = (
            "pytest_collectreport",
            "pytest_runtest_logreport",
        )`
- `getfailures(
        self,
        names: str | Iterable[str] = (
            "pytest_collectreport",
            "pytest_runtest_logreport",
        )`
- `getfailedcollections(self)`
- `listoutcomes(
        self,
    )`
- `countoutcomes(self)`
- `assertoutcome(self, passed: int = 0, skipped: int = 0, failed: int = 0)`
- `clear(self)`
- `linecomp()`
- `LineMatcher_fixture(request: FixtureRequest)`
- `pytester(
    request: FixtureRequest, tmp_path_factory: TempPathFactory, monkeypatch: MonkeyPatch
)`
- `_sys_snapshot()`
- `_config_for_test()`
- `__init__(
        self,
        ret: int | ExitCode,
        outlines: list[str],
        errlines: list[str],
        duration: float,
    )`
- `__repr__(self)`
- `parseoutcomes(self)`
- `parse_summary_nouns(cls, lines)`
- `assert_outcomes(
        self,
        passed: int = 0,
        skipped: int = 0,
        failed: int = 0,
        errors: int = 0,
        xpassed: int = 0,
        xfailed: int = 0,
        warnings: int | None = None,
        deselected: int | None = None,
    )`
- `__init__(self, preserve: Callable[[str], bool] | None = None)`
- `restore(self)`
- `__init__(self)`
- `restore(self)`
- `__init__(
        self,
        request: FixtureRequest,
        tmp_path_factory: TempPathFactory,
        monkeypatch: MonkeyPatch,
        *,
        _ispytest: bool = False,
    )`
- `path(self)`
- `__repr__(self)`
- `_finalize(self)`
- `__take_sys_modules_snapshot(self)`
- `preserve_module(name)`
- `make_hook_recorder(self, pluginmanager: PytestPluginManager)`
- `chdir(self)`
- `_makefile(
        self,
        ext: str,
        lines: Sequence[Any | bytes],
        files: Mapping[str, _FileContent],
        encoding: str = "utf-8",
    )`
- `to_text(s: Any | bytes)`
- `makefile(self, ext: str, *args: str, **kwargs: str)`
- `makeconftest(self, source: str)`
- `makeini(self, source: str)`
- `maketoml(self, source: str)`
- `getinicfg(self, source: str)`
- `makepyprojecttoml(self, source: str)`
- `makepyfile(self, *args: _FileContent, **kwargs: _FileContent)`
- `test_something(pytester)`
- `maketxtfile(self, *args: _FileContent, **kwargs: _FileContent)`
- `test_something(pytester)`
- `syspathinsert(self, path: str | os.PathLike[str] | None = None)`
- `mkdir(self, name: str | os.PathLike[str])`
- `mkpydir(self, name: str | os.PathLike[str])`
- `copy_example(self, name: str | None = None)`
- `getnode(self, config: Config, arg: str | os.PathLike[str])`
- `getpathnode(self, path: str | os.PathLike[str])`
- `genitems(self, colitems: Sequence[Item | Collector])`
- `runitem(self, source: str)`
- `inline_runsource(self, source: str, *cmdlineargs)`
- `inline_genitems(self, *args)`
- `inline_run(
        self,
        *args: str | os.PathLike[str],
        plugins=()`
- `pytest_configure(config: Config)`
- `runpytest_inprocess(
        self, *args: str | os.PathLike[str], **kwargs: Any
    )`
- `runpytest(self, *args: str | os.PathLike[str], **kwargs: Any)`
- `_ensure_basetemp(
        self, args: Sequence[str | os.PathLike[str]]
    )`
- `parseconfig(self, *args: str | os.PathLike[str])`
- `parseconfigure(self, *args: str | os.PathLike[str])`
- `getitem(
        self, source: str | os.PathLike[str], funcname: str = "test_func"
    )`
- `getitems(self, source: str | os.PathLike[str])`
- `getmodulecol(
        self,
        source: str | os.PathLike[str],
        configargs=()`
- `collect_by_name(self, modcol: Collector, name: str)`
- `popen(
        self,
        cmdargs: Sequence[str | os.PathLike[str]],
        stdout: int | TextIO = subprocess.PIPE,
        stderr: int | TextIO = subprocess.PIPE,
        stdin: NotSetType | bytes | IO[Any] | int = CLOSE_STDIN,
        **kw,
    )`
- `run(
        self,
        *cmdargs: str | os.PathLike[str],
        timeout: float | None = None,
        stdin: NotSetType | bytes | IO[Any] | int = CLOSE_STDIN,
    )`
- `handle_timeout()`
- `_dump_lines(self, lines, fp)`
- `_getpytestargs(self)`
- `runpython(self, script: os.PathLike[str])`
- `runpython_c(self, command: str)`
- `runpytest_subprocess(
        self, *args: str | os.PathLike[str], timeout: float | None = None
    )`
- `spawn_pytest(self, string: str, expect_timeout: float = 10.0)`
- `spawn(self, cmd: str, expect_timeout: float = 10.0)`
- `__init__(self)`
- `assert_contains_lines(self, lines2: Sequence[str])`
- `__init__(self, lines: list[str])`
- `__str__(self)`
- `_getlines(self, lines2: str | Sequence[str] | Source)`
- `fnmatch_lines_random(self, lines2: Sequence[str])`
- `re_match_lines_random(self, lines2: Sequence[str])`
- `_match_lines_random(
        self, lines2: Sequence[str], match_func: Callable[[str, str], bool]
    )`
- `get_lines_after(self, fnline: str)`
- `_log(self, *args)`
- `_log_text(self)`
- `fnmatch_lines(
        self, lines2: Sequence[str], *, consecutive: bool = False
    )`
- `re_match_lines(
        self, lines2: Sequence[str], *, consecutive: bool = False
    )`
- `_match_lines(
        self,
        lines2: Sequence[str],
        match_func: Callable[[str, str], bool],
        match_nickname: str,
        *,
        consecutive: bool = False,
    )`
- `no_fnmatch_line(self, pat: str)`
- `no_re_match_line(self, pat: str)`
- `_no_match_line(
        self, pat: str, match_func: Callable[[str, str], bool], match_nickname: str
    )`
- `_fail(self, msg: str)`
- `str(self)`

#### Parameters / Constants
- `IGNORE_PAM` = `[  # filenames added when obtaining details about the current user`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/pytester_assertions.py`

#### Functions
- `assertoutcome(
    outcomes: tuple[
        Sequence[TestReport],
        Sequence[CollectReport | TestReport],
        Sequence[CollectReport | TestReport],
    ],
    passed: int = 0,
    skipped: int = 0,
    failed: int = 0,
)`
- `assert_outcomes(
    outcomes: dict[str, int],
    passed: int = 0,
    skipped: int = 0,
    failed: int = 0,
    errors: int = 0,
    xpassed: int = 0,
    xfailed: int = 0,
    warnings: int | None = None,
    deselected: int | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/python.py`

#### Classes
- `PyobjMixin`
- `_EmptyClass`
- `PyCollector`
- `Module`
- `Package`
- `Class`
- `IdMaker`
- `CallSpec2`
- `DirectParamFixtureDef`
- `Metafunc`
- `Function`
- `FunctionDefinition`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_generate_tests(metafunc: Metafunc)`
- `pytest_configure(config: Config)`
- `async_fail(nodeid: str)`
- `pytest_pyfunc_call(pyfuncitem: Function)`
- `pytest_collect_directory(
    path: Path, parent: nodes.Collector
)`
- `pytest_collect_file(file_path: Path, parent: nodes.Collector)`
- `path_matches_patterns(path: Path, patterns: Iterable[str])`
- `pytest_pycollect_makemodule(module_path: Path, parent)`
- `pytest_pycollect_makeitem(
    collector: Module | Class, name: str, obj: object
)`
- `module(self)`
- `cls(self)`
- `instance(self)`
- `obj(self)`
- `obj(self, value)`
- `_getobj(self)`
- `getmodpath(self, stopatmodule: bool = True, includemodule: bool = False)`
- `reportinfo(self)`
- `funcnamefilter(self, name: str)`
- `isnosetest(self, obj: object)`
- `classnamefilter(self, name: str)`
- `istestfunction(self, obj: object, name: str)`
- `istestclass(self, obj: object, name: str)`
- `_matches_prefix_or_glob_option(self, option_name: str, name: str)`
- `collect(self)`
- `_genfunctions(self, name: str, funcobj)`
- `importtestmodule(
    path: Path,
    config: Config,
)`
- `_getobj(self)`
- `collect(self)`
- `_register_setup_module_fixture(self)`
- `xunit_setup_module_fixture(request)`
- `_register_setup_function_fixture(self)`
- `xunit_setup_function_fixture(request)`
- `__init__(
        self,
        fspath: None,
        parent: nodes.Collector,
        # NOTE: following args are unused:
        config=None,
        session=None,
        nodeid=None,
        path: Path | None = None,
    )`
- `setup(self)`
- `collect(self)`
- `sort_key(entry: os.DirEntry[str])`
- `_call_with_optional_argument(func, arg)`
- `_get_first_non_fixture_func(obj: object, names: Iterable[str])`
- `from_parent(cls, parent, *, name, obj=None, **kw)`
- `newinstance(self)`
- `collect(self)`
- `_register_setup_class_fixture(self)`
- `xunit_setup_class_fixture(request)`
- `_register_setup_method_fixture(self)`
- `xunit_setup_method_fixture(request)`
- `hasinit(obj: object)`
- `hasnew(obj: object)`
- `make_unique_parameterset_ids(self)`
- `_strict_parametrization_ids_enabled(self)`
- `_resolve_ids(self)`
- `_idval(self, val: object, argname: str, idx: int)`
- `_idval_from_function(self, val: object, argname: str, idx: int)`
- `_idval_from_hook(self, val: object, argname: str)`
- `_idval_from_value(self, val: object)`
- `_idval_from_value_required(self, val: object, idx: int)`
- `_idval_from_argname(argname: str, idx: int)`
- `_complain_multiple_hidden_parameter_sets(self)`
- `_make_error_prefix(self)`
- `setmulti(
        self,
        *,
        argnames: Iterable[str],
        valset: Iterable[object],
        id: str | _HiddenParam,
        marks: Iterable[Mark | MarkDecorator],
        scope: Scope,
        param_index: int,
        nodeid: str,
    )`
- `getparam(self, name: str)`
- `id(self)`
- `get_direct_param_fixture_func(request: FixtureRequest)`
- `__init__(self, *, node: nodes.Node, argname: str, scope: Scope)`
- `__init__(
        self,
        definition: FunctionDefinition,
        fixtureinfo: fixtures.FuncFixtureInfo,
        config: Config,
        cls=None,
        module=None,
        *,
        _ispytest: bool = False,
    )`
- `parametrize(
        self,
        argnames: str | Sequence[str],
        argvalues: Iterable[ParameterSet | Sequence[object] | object],
        indirect: bool | Sequence[str] = False,
        ids: Iterable[object | None] | Callable[[Any], object | None] | None = None,
        scope: ScopeName | None = None,
        *,
        _param_mark: Mark | None = None,
    )`
- `_resolve_parameter_set_ids(
        self,
        argnames: Sequence[str],
        ids: Iterable[object | None] | Callable[[Any], object | None] | None,
        parametersets: Sequence[ParameterSet],
        nodeid: str,
    )`
- `_validate_ids(
        self,
        ids: Iterable[object | None],
        parametersets: Sequence[ParameterSet],
    )`
- `_validate_if_using_arg_names(
        self,
        argnames: Sequence[str],
        indirect: bool | Sequence[str],
    )`
- `_recompute_direct_params_indices(self)`
- `_find_parametrized_scope(
    argnames: Sequence[str],
    arg2fixturedefs: Mapping[str, Sequence[fixtures.FixtureDef[object]]],
    indirect: bool | Sequence[str],
)`
- `_ascii_escaped_by_config(val: str | bytes, config: Config | None)`
- `__init__(
        self,
        name: str,
        parent,
        config: Config | None = None,
        callspec: CallSpec2 | None = None,
        callobj=NOTSET,
        keywords: Mapping[str, Any] | None = None,
        session: Session | None = None,
        fixtureinfo: FuncFixtureInfo | None = None,
        originalname: str | None = None,
    )`
- `from_parent(cls, parent, **kw)`
- `_initrequest(self)`
- `function(self)`
- `instance(self)`
- `_getinstance(self)`
- `_getobj(self)`
- `_pyfuncitem(self)`
- `runtest(self)`
- `setup(self)`
- `_traceback_filter(self, excinfo: ExceptionInfo[BaseException])`
- `repr_failure(  # type: ignore[override]
        self,
        excinfo: ExceptionInfo[BaseException],
    )`
- `runtest(self)`

#### Parameters / Constants
- `IGNORED_ATTRIBUTES` = `frozenset.union(`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/python_api.py`

#### Classes
- `ApproxBase`
- `ApproxNumpy`
- `ApproxMapping`
- `ApproxSequenceLike`
- `ApproxScalar`
- `ApproxDecimal`
- `ApproxTimedelta`

#### Functions
- `_compare_approx(
    full_object: object,
    message_data: Sequence[tuple[str, str, str]],
    number_of_elements: int,
    different_ids: Sequence[object],
    max_abs_diff: float,
    max_rel_diff: float,
)`
- `__init__(self, expected, rel=None, abs=None, nan_ok: bool = False)`
- `__repr__(self)`
- `_repr_compare(self, other_side: Any)`
- `__eq__(self, actual)`
- `__bool__(self)`
- `__ne__(self, actual)`
- `_approx_scalar(self, x)`
- `_yield_comparisons(self, actual)`
- `_check_type(self)`
- `_recursive_sequence_map(f, x)`
- `__repr__(self)`
- `_repr_compare(self, other_side: ndarray | list[Any])`
- `get_value_from_nested_list(
            nested_list: list[Any], nd_index: tuple[Any, ...]
        )`
- `__eq__(self, actual)`
- `_yield_comparisons(self, actual)`
- `__repr__(self)`
- `_repr_compare(self, other_side: Mapping[object, float])`
- `__eq__(self, actual)`
- `_yield_comparisons(self, actual)`
- `_check_type(self)`
- `__repr__(self)`
- `_repr_compare(self, other_side: Sequence[float])`
- `__eq__(self, actual)`
- `_yield_comparisons(self, actual)`
- `_check_type(self)`
- `__repr__(self)`
- `__eq__(self, actual)`
- `is_bool(val: Any)`
- `tolerance(self)`
- `set_default(x, default)`
- `__repr__(self)`
- `__init__(self, expected, rel=None, abs=None, nan_ok: bool = False)`
- `__repr__(self)`
- `__eq__(self, actual)`
- `_yield_comparisons(self, actual)`
- `_repr_compare(self, other_side: Any)`
- `approx(
    expected: Any,
    rel: float | Decimal | timedelta | None = None,
    abs: float | Decimal | timedelta | None = None,
    nan_ok: bool = False,
)`
- `_is_sequence_like(expected: object)`
- `_as_numpy_array(obj: object)`

#### Parameters / Constants
- `DEFAULT_ABSOLUTE_TOLERANCE` = `Decimal("1e-12")`
- `DEFAULT_RELATIVE_TOLERANCE` = `Decimal("1e-6")`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/raises.py`

#### Classes
- `AbstractRaises`
- `RaisesExc`
- `RaisesGroup`
- `NotChecked`
- `ResultHolder`

#### Functions
- `raises(
    expected_exception: type[E] | tuple[type[E], ...],
    *,
    match: str | re.Pattern[str] | None = ...,
    check: Callable[[E], bool] = ...,
)`
- `raises(
    *,
    match: str | re.Pattern[str],
    # If exception_type is not provided, check()`
- `raises(*, check: Callable[[BaseException], bool])`
- `raises(
    expected_exception: type[E] | tuple[type[E], ...],
    func: Callable[P, object],
    *args: P.args,
    **kwargs: P.kwargs,
)`
- `raises(
    expected_exception: type[E] | tuple[type[E], ...] | None = None,
    func: Callable[P, object] | None = None,
    *args: Any,
    **kwargs: Any,
)`
- `_match_pattern(match: Pattern[str])`
- `repr_callable(fun: Callable[[BaseExcT_1], bool])`
- `backquote(s: str)`
- `_exception_type_name(
    e: type[BaseException] | tuple[type[BaseException], ...],
)`
- `_check_raw_type(
    expected_type: type[BaseException] | tuple[type[BaseException], ...] | None,
    exception: BaseException,
)`
- `is_fully_escaped(s: str)`
- `unescape(s: str)`
- `__init__(
        self,
        *,
        match: str | Pattern[str] | None,
        check: Callable[[BaseExcT_co], bool] | None,
    )`
- `_parse_exc(
        self, exc: type[BaseExcT_1] | types.GenericAlias, expected: str
    )`
- `fail_reason(self)`
- `_check_check(
        self: AbstractRaises[BaseExcT_1],
        exception: BaseExcT_1,
    )`
- `_check_match(self, e: BaseException)`
- `matches(
        self: AbstractRaises[BaseExcT_1], exception: BaseException
    )`
- `__init__(
        self,
        expected_exception: (
            type[BaseExcT_co_default] | tuple[type[BaseExcT_co_default], ...]
        )`
- `__init__(
        self: RaisesExc[BaseException],  # Give E a value.
        /,
        *,
        match: str | Pattern[str] | None,
        # If exception_type is not provided, check()`
- `__init__(self, /, *, check: Callable[[BaseException], bool])`
- `__init__(
        self,
        expected_exception: (
            type[BaseExcT_co_default] | tuple[type[BaseExcT_co_default], ...] | None
        )`
- `matches(
        self,
        exception: BaseException | None,
    )`
- `__repr__(self)`
- `_check_type(self, exception: BaseException)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    )`
- `__init__(
        self,
        expected_exception: type[BaseExcT_co] | RaisesExc[BaseExcT_co],
        /,
        *,
        allow_unwrapped: Literal[True],
        flatten_subgroups: bool = False,
    )`
- `__init__(
        self,
        expected_exception: type[BaseExcT_co] | RaisesExc[BaseExcT_co],
        /,
        *other_exceptions: type[BaseExcT_co] | RaisesExc[BaseExcT_co],
        flatten_subgroups: Literal[True],
        match: str | Pattern[str] | None = None,
        check: Callable[[BaseExceptionGroup[BaseExcT_co]], bool] | None = None,
    )`
- `__init__(
        self: RaisesGroup[ExcT_1],
        expected_exception: type[ExcT_1] | RaisesExc[ExcT_1],
        /,
        *other_exceptions: type[ExcT_1] | RaisesExc[ExcT_1],
        match: str | Pattern[str] | None = None,
        check: Callable[[ExceptionGroup[ExcT_1]], bool] | None = None,
    )`
- `__init__(
        self: RaisesGroup[ExceptionGroup[ExcT_2]],
        expected_exception: RaisesGroup[ExcT_2],
        /,
        *other_exceptions: RaisesGroup[ExcT_2],
        match: str | Pattern[str] | None = None,
        check: Callable[[ExceptionGroup[ExceptionGroup[ExcT_2]]], bool] | None = None,
    )`
- `__init__(
        self: RaisesGroup[ExcT_1 | ExceptionGroup[ExcT_2]],
        expected_exception: type[ExcT_1] | RaisesExc[ExcT_1] | RaisesGroup[ExcT_2],
        /,
        *other_exceptions: type[ExcT_1] | RaisesExc[ExcT_1] | RaisesGroup[ExcT_2],
        match: str | Pattern[str] | None = None,
        check: (
            Callable[[ExceptionGroup[ExcT_1 | ExceptionGroup[ExcT_2]]], bool] | None
        )`
- `__init__(
        self: RaisesGroup[BaseExcT_1],
        expected_exception: type[BaseExcT_1] | RaisesExc[BaseExcT_1],
        /,
        *other_exceptions: type[BaseExcT_1] | RaisesExc[BaseExcT_1],
        match: str | Pattern[str] | None = None,
        check: Callable[[BaseExceptionGroup[BaseExcT_1]], bool] | None = None,
    )`
- `__init__(
        self: RaisesGroup[BaseExceptionGroup[BaseExcT_2]],
        expected_exception: RaisesGroup[BaseExcT_2],
        /,
        *other_exceptions: RaisesGroup[BaseExcT_2],
        match: str | Pattern[str] | None = None,
        check: (
            Callable[[BaseExceptionGroup[BaseExceptionGroup[BaseExcT_2]]], bool] | None
        )`
- `__init__(
        self: RaisesGroup[BaseExcT_1 | BaseExceptionGroup[BaseExcT_2]],
        expected_exception: type[BaseExcT_1]
        | RaisesExc[BaseExcT_1]
        | RaisesGroup[BaseExcT_2],
        /,
        *other_exceptions: type[BaseExcT_1]
        | RaisesExc[BaseExcT_1]
        | RaisesGroup[BaseExcT_2],
        match: str | Pattern[str] | None = None,
        check: (
            Callable[
                [BaseExceptionGroup[BaseExcT_1 | BaseExceptionGroup[BaseExcT_2]]],
                bool,
            ]
            | None
        )`
- `__init__(
        self: RaisesGroup[ExcT_1 | BaseExcT_1 | BaseExceptionGroup[BaseExcT_2]],
        expected_exception: type[BaseExcT_1]
        | RaisesExc[BaseExcT_1]
        | RaisesGroup[BaseExcT_2],
        /,
        *other_exceptions: type[BaseExcT_1]
        | RaisesExc[BaseExcT_1]
        | RaisesGroup[BaseExcT_2],
        allow_unwrapped: bool = False,
        flatten_subgroups: bool = False,
        match: str | Pattern[str] | None = None,
        check: (
            Callable[[BaseExceptionGroup[BaseExcT_1]], bool]
            | Callable[[ExceptionGroup[ExcT_1]], bool]
            | None
        )`
- `_parse_excgroup(
        self,
        exc: (
            type[BaseExcT_co]
            | types.GenericAlias
            | RaisesExc[BaseExcT_1]
            | RaisesGroup[BaseExcT_2]
        )`
- `__enter__(
        self: RaisesGroup[ExcT_1],
    )`
- `__enter__(
        self: RaisesGroup[BaseExcT_1],
    )`
- `__enter__(self)`
- `__repr__(self)`
- `_unroll_exceptions(
        self,
        exceptions: Sequence[BaseException],
    )`
- `matches(
        self: RaisesGroup[ExcT_1],
        exception: BaseException | None,
    )`
- `matches(
        self: RaisesGroup[BaseExcT_1],
        exception: BaseException | None,
    )`
- `matches(
        self,
        exception: BaseException | None,
    )`
- `_check_expected(
        expected_type: (
            type[BaseException] | RaisesExc[BaseException] | RaisesGroup[BaseException]
        )`
- `_repr_expected(e: type[BaseException] | AbstractRaises[BaseException])`
- `_check_exceptions(
        self: RaisesGroup[ExcT_1],
        _exception: Exception,
        actual_exceptions: Sequence[Exception],
    )`
- `_check_exceptions(
        self: RaisesGroup[BaseExcT_1],
        _exception: BaseException,
        actual_exceptions: Sequence[BaseException],
    )`
- `_check_exceptions(
        self,
        _exception: BaseException,
        actual_exceptions: Sequence[BaseException],
    )`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    )`
- `expected_type(self)`
- `__init__(
        self,
        expected_exceptions: tuple[
            type[BaseException] | AbstractRaises[BaseException], ...
        ],
        actual_exceptions: Sequence[BaseException],
    )`
- `set_result(self, expected: int, actual: int, result: str | None)`
- `get_result(self, expected: int, actual: int)`
- `has_result(self, expected: int, actual: int)`
- `no_match_for_expected(self, expected: list[int])`
- `no_match_for_actual(self, actual: list[int])`
- `possible_match(results: ResultHolder, used: set[int] | None = None)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/recwarn.py`

#### Classes
- `WarningsRecorder`
- `WarningsChecker`

#### Functions
- `recwarn()`
- `deprecated_call(
    *, match: str | re.Pattern[str] | None = ...
)`
- `deprecated_call(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs)`
- `deprecated_call(
    func: Callable[..., Any] | None = None, *args: Any, **kwargs: Any
)`
- `warns(
    expected_warning: type[Warning] | tuple[type[Warning], ...] = ...,
    *,
    match: str | re.Pattern[str] | None = ...,
)`
- `warns(
    expected_warning: type[Warning] | tuple[type[Warning], ...],
    func: Callable[P, T],
    *args: P.args,
    **kwargs: P.kwargs,
)`
- `warns(
    expected_warning: type[Warning] | tuple[type[Warning], ...] = Warning,
    func: Callable[..., object] | None = None,
    *args: Any,
    **kwargs: Any,
)`
- `__init__(self, *, _ispytest: bool = False)`
- `list(self)`
- `__getitem__(self, i: int)`
- `__iter__(self)`
- `__len__(self)`
- `pop(self, cls: type[Warning] = Warning)`
- `clear(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `__init__(
        self,
        expected_warning: type[Warning] | tuple[type[Warning], ...] = Warning,
        match_expr: str | re.Pattern[str] | None = None,
        *,
        _ispytest: bool = False,
    )`
- `matches(self, warning: warnings.WarningMessage)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `found_str()`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/reports.py`

#### Classes
- `BaseReport`
- `TestReport`
- `CollectReport`
- `CollectErrorRepr`

#### Functions
- `getworkerinfoline(node)`
- `__init__(self, **kw: Any)`
- `__getattr__(self, key: str)`
- `toterminal(self, out: TerminalWriter)`
- `get_sections(self, prefix: str)`
- `longreprtext(self)`
- `caplog(self)`
- `capstdout(self)`
- `capstderr(self)`
- `passed(self)`
- `failed(self)`
- `skipped(self)`
- `fspath(self)`
- `count_towards_summary(self)`
- `head_line(self)`
- `_get_verbose_word_with_markup(
        self, config: Config, default_markup: Mapping[str, bool]
    )`
- `_to_json(self)`
- `_from_json(cls, reportdict: dict[str, object])`
- `_report_unserialization_failure(
    type_name: str, report_class: type[BaseReport], reportdict
)`
- `_format_failed_longrepr(
    item: Item, call: CallInfo[None], excinfo: ExceptionInfo[BaseException]
)`
- `_format_exception_group_all_skipped_longrepr(
    item: Item,
    excinfo: ExceptionInfo[BaseExceptionGroup[BaseException | BaseExceptionGroup]],
)`
- `__init__(
        self,
        nodeid: str,
        location: tuple[str, int | None, str],
        keywords: Mapping[str, Any],
        outcome: Literal["passed", "failed", "skipped"],
        longrepr: None
        | ExceptionInfo[BaseException]
        | tuple[str, int, str]
        | str
        | TerminalRepr,
        when: Literal["setup", "call", "teardown"],
        sections: Iterable[tuple[str, str]] = ()`
- `__repr__(self)`
- `from_item_and_call(cls, item: Item, call: CallInfo[None])`
- `__init__(
        self,
        nodeid: str,
        outcome: Literal["passed", "failed", "skipped"],
        longrepr: None
        | ExceptionInfo[BaseException]
        | tuple[str, int, str]
        | str
        | TerminalRepr,
        result: list[Item | Collector] | None,
        sections: Iterable[tuple[str, str]] = ()`
- `location(  # type:ignore[override]
        self,
    )`
- `__repr__(self)`
- `__init__(self, msg: str)`
- `toterminal(self, out: TerminalWriter)`
- `pytest_report_to_serializable(
    report: CollectReport | TestReport,
)`
- `pytest_report_from_serializable(
    data: dict[str, Any],
)`
- `_report_to_json(report: BaseReport)`
- `serialize_repr_entry(
        entry: ReprEntry | ReprEntryNative,
    )`
- `serialize_repr_traceback(reprtraceback: ReprTraceback)`
- `serialize_repr_crash(
        reprcrash: ReprFileLocation | None,
    )`
- `serialize_exception_longrepr(rep: BaseReport)`
- `_report_kwargs_from_json(reportdict: dict[str, Any])`
- `deserialize_repr_entry(entry_data)`
- `deserialize_repr_traceback(repr_traceback_dict)`
- `deserialize_repr_crash(repr_crash_dict: dict[str, Any] | None)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/runner.py`

#### Classes
- `CallInfo`
- `SetupState`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_terminal_summary(terminalreporter: TerminalReporter)`
- `pytest_sessionstart(session: Session)`
- `pytest_sessionfinish(session: Session)`
- `pytest_runtest_protocol(item: Item, nextitem: Item | None)`
- `runtestprotocol(
    item: Item, log: bool = True, nextitem: Item | None = None
)`
- `show_test_item(item: Item, *, add_space: bool)`
- `pytest_runtest_setup(item: Item)`
- `pytest_runtest_call(item: Item)`
- `pytest_runtest_teardown(item: Item, nextitem: Item | None)`
- `_update_current_test_var(
    item: Item, when: Literal["setup", "call", "teardown"] | None
)`
- `pytest_report_teststatus(report: BaseReport)`
- `call_and_report(
    item: Item, when: Literal["setup", "call", "teardown"], log: bool = True, **kwds
)`
- `get_reraise_exceptions(config: Config)`
- `check_interactive_exception(call: CallInfo[object], report: BaseReport)`
- `__init__(
        self,
        result: TResult | None,
        excinfo: ExceptionInfo[BaseException] | None,
        start: float,
        stop: float,
        duration: float,
        when: Literal["collect", "setup", "call", "teardown"],
        *,
        _ispytest: bool = False,
    )`
- `result(self)`
- `from_call(
        cls,
        func: Callable[[], TResult],
        when: Literal["collect", "setup", "call", "teardown"],
        reraise: type[BaseException] | tuple[type[BaseException], ...] | None = None,
    )`
- `__repr__(self)`
- `pytest_runtest_makereport(item: Item, call: CallInfo[None])`
- `pytest_make_collect_report(collector: Collector)`
- `collect()`
- `__init__(self)`
- `is_node_active(self, node: Node)`
- `setup(self, item: Item)`
- `addfinalizer(self, finalizer: Callable[[], object], node: Node)`
- `teardown_exact(self, nextitem: Item | None)`
- `collect_one_node(collector: Collector)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/scope.py`

#### Classes
- `Scope`

#### Functions
- `next_lower(self)`
- `next_higher(self)`
- `__lt__(self, other: Scope)`
- `from_user(
        cls, scope_name: ScopeName, descr: str, where: str | None = None
    )`

#### Parameters / Constants
- `HIGH_SCOPES` = `[x for x in Scope if x is not Scope.Function]`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/setuponly.py`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_fixture_setup(
    fixturedef: FixtureDef[object], request: SubRequest
)`
- `pytest_fixture_post_finalizer(
    fixturedef: FixtureDef[object], request: SubRequest
)`
- `_show_fixture_action(
    fixturedef: FixtureDef[object], config: Config, msg: str
)`
- `pytest_cmdline_main(config: Config)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/setupplan.py`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_fixture_setup(
    fixturedef: FixtureDef[object], request: SubRequest
)`
- `pytest_cmdline_main(config: Config)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/skipping.py`

#### Classes
- `Skip`
- `Xfail`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `nop(*args, **kwargs)`
- `evaluate_condition(item: Item, mark: Mark, condition: object)`
- `evaluate_skip_marks(item: Item)`
- `evaluate_xfail_marks(item: Item)`
- `pytest_runtest_setup(item: Item)`
- `pytest_runtest_call(item: Item)`
- `pytest_runtest_makereport(
    item: Item, call: CallInfo[None]
)`
- `pytest_report_teststatus(report: BaseReport)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/stash.py`

#### Classes
- `StashKey`
- `Stash`

#### Functions
- `__init__(self)`
- `__setitem__(self, key: StashKey[T], value: T)`
- `__getitem__(self, key: StashKey[T])`
- `get(self, key: StashKey[T], default: D)`
- `setdefault(self, key: StashKey[T], default: T)`
- `__delitem__(self, key: StashKey[T])`
- `__contains__(self, key: StashKey[T])`
- `__len__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/stepwise.py`

#### Classes
- `StepwiseCacheInfo`
- `StepwisePlugin`

#### Functions
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `pytest_sessionfinish(session: Session)`
- `last_cache_date(self)`
- `empty(cls)`
- `update_date_to_now(self)`
- `__init__(self, config: Config)`
- `_load_cached_info(self)`
- `pytest_sessionstart(self, session: Session)`
- `pytest_collection_modifyitems(
        self, config: Config, items: list[nodes.Item]
    )`
- `pytest_runtest_logreport(self, report: TestReport)`
- `pytest_report_collectionfinish(self)`
- `pytest_sessionfinish(self)`

#### Parameters / Constants
- `STEPWISE_CACHE_DIR` = `"cache/stepwise"`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/subtests.py`

#### Classes
- `SubtestContext`
- `SubtestReport`
- `Subtests`
- `_SubTestContextManager`
- `Captured`
- `CapturedLogs`

#### Functions
- `pytest_addoption(parser: Parser)`
- `__post_init__(self)`
- `_to_json(self)`
- `_from_json(cls, d: dict[str, Any])`
- `head_line(self)`
- `_sub_test_description(self)`
- `_to_json(self)`
- `_from_json(cls, reportdict: dict[str, Any])`
- `_new(
        cls,
        test_report: TestReport,
        context: SubtestContext,
        captured_output: Captured | None,
        captured_logs: CapturedLogs | None,
    )`
- `subtests(request: SubRequest)`
- `__init__(
        self,
        ihook: pluggy.HookRelay,
        suspend_capture_ctx: Callable[[], AbstractContextManager[None]],
        request: SubRequest,
        *,
        _ispytest: bool = False,
    )`
- `test(
        self,
        msg: str | None = None,
        **kwargs: Any,
    )`
- `test(subtests)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `capturing_output(request: SubRequest)`
- `capturing_logs(
    request: SubRequest,
)`
- `pytest_report_to_serializable(report: TestReport)`
- `pytest_report_from_serializable(data: dict[str, Any])`
- `pytest_configure(config: Config)`
- `pytest_report_teststatus(
    report: TestReport,
    config: Config,
)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/terminal.py`

#### Classes
- `MoreQuietAction`
- `TestShortLogReport`
- `WarningReport`
- `TerminalReporter`
- `TerminalProgressPlugin`

#### Functions
- `__init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        default: object = None,
        required: bool = False,
        help: str | None = None,
    )`
- `__call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[object] | None,
        option_string: str | None = None,
    )`
- `pytest_addoption(parser: Parser)`
- `pytest_configure(config: Config)`
- `mywriter(tags, args)`
- `getreportopt(config: Config)`
- `pytest_report_teststatus(report: BaseReport)`
- `get_location(self, config: Config)`
- `__init__(self, config: Config, file: TextIO | None = None)`
- `_determine_show_progress_info(
        self,
    )`
- `verbosity(self)`
- `showheader(self)`
- `no_header(self)`
- `no_summary(self)`
- `showfspath(self)`
- `showfspath(self, value: bool | None)`
- `showlongtestinfo(self)`
- `reported_progress(self)`
- `hasopt(self, char: str)`
- `write_fspath_result(self, nodeid: str, res: str, **markup: bool)`
- `write_ensure_prefix(self, prefix: str, extra: str = "", **kwargs)`
- `ensure_newline(self)`
- `wrap_write(
        self,
        content: str,
        *,
        flush: bool = False,
        margin: int = 8,
        line_sep: str = "\n",
        **markup: bool,
    )`
- `write(self, content: str, *, flush: bool = False, **markup: bool)`
- `write_raw(self, content: str, *, flush: bool = False)`
- `flush(self)`
- `write_line(self, line: str | bytes, **markup: bool)`
- `rewrite(self, line: str, **markup: bool)`
- `write_sep(
        self,
        sep: str,
        title: str | None = None,
        fullwidth: int | None = None,
        **markup: bool,
    )`
- `section(self, title: str, sep: str = "=", **kw: bool)`
- `line(self, msg: str, **kw: bool)`
- `_add_stats(self, category: str, items: Sequence[Any])`
- `pytest_internalerror(self, excrepr: ExceptionRepr)`
- `pytest_warning_recorded(
        self,
        warning_message: warnings.WarningMessage,
        nodeid: str,
    )`
- `pytest_plugin_registered(self, plugin: _PluggyPlugin)`
- `pytest_deselected(self, items: Sequence[Item])`
- `pytest_runtest_logstart(
        self, nodeid: str, location: tuple[str, int | None, str]
    )`
- `pytest_runtest_logreport(self, report: TestReport)`
- `_is_last_item(self)`
- `pytest_runtestloop(self)`
- `_get_progress_information_message(self)`
- `_write_progress_information_if_past_edge(self)`
- `_write_progress_information_filling_space(self)`
- `_width_of_current_line(self)`
- `pytest_collection(self)`
- `pytest_collectreport(self, report: CollectReport)`
- `report_collect(self, final: bool = False)`
- `pytest_sessionstart(self, session: Session)`
- `_write_report_lines_from_hooks(
        self, lines: Sequence[str | Sequence[str]]
    )`
- `pytest_report_header(self, config: Config)`
- `pytest_collection_finish(self, session: Session)`
- `_printcollecteditems(self, items: Sequence[Item])`
- `pytest_sessionfinish(
        self, session: Session, exitstatus: int | ExitCode
    )`
- `pytest_terminal_summary(self)`
- `pytest_keyboard_interrupt(self, excinfo: ExceptionInfo[BaseException])`
- `pytest_unconfigure(self)`
- `_report_keyboardinterrupt(self)`
- `_locationline(
        self, nodeid: str, fspath: str, lineno: int | None, domain: str
    )`
- `mkrel(nodeid: str)`
- `_getfailureheadline(self, rep)`
- `_getcrashline(self, rep)`
- `_get_max_warnings(self)`
- `getreports(self, name: str)`
- `summary_warnings(self)`
- `collapsed_location_report(reports: list[WarningReport])`
- `summary_passes(self)`
- `summary_xpasses(self)`
- `summary_passes_combined(
        self, which_reports: str, sep_title: str, needed_opt: str
    )`
- `_get_teardown_reports(self, nodeid: str)`
- `_handle_teardown_sections(self, nodeid: str)`
- `print_teardown_sections(self, rep: TestReport)`
- `summary_failures(self)`
- `summary_xfailures(self)`
- `summary_failures_combined(
        self,
        which_reports: str,
        sep_title: str,
        *,
        style: str,
        needed_opt: str | None = None,
    )`
- `summary_errors(self)`
- `_outrep_summary(self, rep: BaseReport)`
- `summary_stats(self)`
- `short_test_summary(self)`
- `show_simple(lines: list[str], *, stat: str)`
- `show_xfailed(lines: list[str])`
- `show_xpassed(lines: list[str])`
- `show_skipped_folded(lines: list[str])`
- `show_skipped_unfolded(lines: list[str])`
- `show_skipped(lines: list[str])`
- `_get_main_color(self)`
- `_determine_main_color(self, unknown_type_seen: bool)`
- `_set_main_color(self)`
- `build_summary_stats_line(self)`
- `_get_reports_to_display(self, key: str)`
- `_build_normal_summary_stats_line(
        self,
    )`
- `_build_collect_only_summary_stats_line(
        self,
    )`
- `_get_node_id_with_markup(tw: TerminalWriter, config: Config, rep: BaseReport)`
- `_format_trimmed(format: str, msg: str, available_width: int)`
- `_get_line_with_reprcrash_message(
    config: Config, rep: BaseReport, tw: TerminalWriter, word_markup: dict[str, bool]
)`
- `_folded_skips(
    startpath: Path,
    skipped: Sequence[CollectReport],
)`
- `pluralize(count: int, noun: str)`
- `_plugin_nameversions(plugininfo)`
- `format_session_duration(seconds: float)`
- `format_node_duration(seconds: float)`
- `_get_raw_skip_reason(report: TestReport)`
- `__init__(self, tr: TerminalReporter)`
- `_emit_progress(
        self,
        state: Literal["remove", "normal", "error", "indeterminate", "paused"],
        progress: int | None = None,
    )`
- `pytest_sessionstart(self, session: Session)`
- `pytest_collection_finish(self)`
- `pytest_runtest_logreport(self, report: TestReport)`
- `pytest_sessionfinish(self)`

#### Parameters / Constants
- `REPORT_COLLECTING_RESOLUTION` = `0.5`
- `KNOWN_TYPES` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/terminalprogress.py`

#### Functions
- `pytest_configure(config: Config)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/threadexception.py`

#### Classes
- `ThreadExceptionMeta`

#### Functions
- `collect_thread_exception(config: Config)`
- `cleanup(
    *, config: Config, prev_hook: Callable[[threading.ExceptHookArgs], object]
)`
- `thread_exception_hook(
    args: threading.ExceptHookArgs,
    /,
    *,
    append: Callable[[ThreadExceptionMeta | BaseException], object],
)`
- `pytest_configure(config: Config)`
- `pytest_runtest_setup(item: Item)`
- `pytest_runtest_call(item: Item)`
- `pytest_runtest_teardown(item: Item)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/timing.py`

#### Classes
- `Instant`
- `Duration`
- `MockTiming`

#### Functions
- `elapsed(self)`
- `as_utc(self)`
- `seconds(self)`
- `sleep(self, seconds: float)`
- `time(self)`
- `patch(self, monkeypatch: MonkeyPatch)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/tmpdir.py`

#### Classes
- `TempPathFactory`

#### Functions
- `__init__(
        self,
        given_basetemp: Path | None,
        retention_count: int,
        retention_policy: RetentionType,
        trace,
        basetemp: Path | None = None,
        *,
        _ispytest: bool = False,
    )`
- `from_config(
        cls,
        config: Config,
        *,
        _ispytest: bool = False,
    )`
- `_ensure_relative_to_basetemp(self, basename: str)`
- `mktemp(self, basename: str, numbered: bool = True)`
- `getbasetemp(self)`
- `get_user()`
- `pytest_configure(config: Config)`
- `pytest_addoption(parser: Parser)`
- `tmp_path_factory(request: FixtureRequest)`
- `_mk_tmp(request: FixtureRequest, factory: TempPathFactory)`
- `tmp_path(
    request: FixtureRequest, tmp_path_factory: TempPathFactory
)`
- `pytest_sessionfinish(session, exitstatus: int | ExitCode)`
- `pytest_runtest_makereport(
    item: Item, call
)`

#### Parameters / Constants
- `MAXVAL` = `30`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/tracemalloc.py`

#### Functions
- `tracemalloc_message(source: object)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/unittest.py`

#### Classes
- `UnitTestCase`
- `TestCaseFunction`
- `TwistedVersion`

#### Functions
- `pytest_pycollect_makeitem(
    collector: Module | Class, name: str, obj: object
)`
- `newinstance(self)`
- `collect(self)`
- `_register_unittest_setup_class_fixture(self, cls: type)`
- `process_teardown_exceptions()`
- `unittest_setup_class_fixture(
            request: FixtureRequest,
        )`
- `_register_unittest_skip_fixture(self, cls: type)`
- `unittest_skip_fixture(request: FixtureRequest)`
- `_register_unittest_setup_method_fixture(self, cls: type)`
- `unittest_setup_method_fixture(
            request: FixtureRequest,
        )`
- `_getinstance(self)`
- `_testcase(self)`
- `setup(self)`
- `teardown(self)`
- `startTest(self, testcase: unittest.TestCase)`
- `_addexcinfo(self, rawexcinfo: _SysExcInfoType)`
- `addError(
        self, testcase: unittest.TestCase, rawexcinfo: _SysExcInfoType
    )`
- `addFailure(
        self, testcase: unittest.TestCase, rawexcinfo: _SysExcInfoType
    )`
- `addSkip(
        self, testcase: unittest.TestCase, reason: str, *, handle_subtests: bool = True
    )`
- `add_skip()`
- `addExpectedFailure(
        self,
        testcase: unittest.TestCase,
        rawexcinfo: _SysExcInfoType,
        reason: str = "",
    )`
- `addUnexpectedSuccess(
        self,
        testcase: unittest.TestCase,
        reason: twisted.trial.unittest.Todo | None = None,
    )`
- `addSuccess(self, testcase: unittest.TestCase)`
- `stopTest(self, testcase: unittest.TestCase)`
- `addDuration(self, testcase: unittest.TestCase, elapsed: float)`
- `runtest(self)`
- `_traceback_filter(
        self, excinfo: _pytest._code.ExceptionInfo[BaseException]
    )`
- `addSubTest(
        self,
        test_case: Any,
        test: TestCase,
        exc_info: ExceptionInfo[BaseException]
        | tuple[type[BaseException], BaseException, TracebackType]
        | None,
    )`
- `_obtain_errors_and_skips(self)`
- `pytest_runtest_makereport(item: Item, call: CallInfo[None])`
- `_is_skipped(obj)`
- `pytest_configure()`
- `_get_twisted_version()`
- `pytest_runtest_protocol(item: Item)`
- `store_raw_exception_info(
            self, exc_value=None, exc_type=None, exc_tb=None, captureVars=None
        )`
- `_handle_twisted_exc_info(
    rawexcinfo: _SysExcInfoType | BaseException,
)`

#### Parameters / Constants
- `TWISTED_RAW_EXCINFO_ATTR` = `"_twisted_raw_excinfo"`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/unraisableexception.py`

#### Classes
- `UnraisableMeta`

#### Functions
- `gc_collect_harder(iterations: int)`
- `collect_unraisable(config: Config)`
- `cleanup(
    *, config: Config, prev_hook: Callable[[sys.UnraisableHookArgs], object]
)`
- `unraisable_hook(
    unraisable: sys.UnraisableHookArgs,
    /,
    *,
    append: Callable[[UnraisableMeta | BaseException], object],
)`
- `pytest_configure(config: Config)`
- `pytest_unconfigure(config: Config)`
- `pytest_runtest_setup(item: Item)`
- `pytest_runtest_call(item: Item)`
- `pytest_runtest_teardown(item: Item)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/warning_types.py`

#### Classes
- `PytestWarning`
- `PytestAssertRewriteWarning`
- `PytestCacheWarning`
- `PytestConfigWarning`
- `PytestCollectionWarning`
- `PytestDeprecationWarning`
- `PytestRemovedIn10Warning`
- `PytestExperimentalApiWarning`
- `PytestReturnNotNoneWarning`
- `PytestUnknownMarkWarning`
- `PytestUnraisableExceptionWarning`
- `PytestUnhandledThreadExceptionWarning`
- `UnformattedWarning`
- `PytestFDWarning`

#### Functions
- `simple(cls, apiname: str)`
- `format(self, **kwargs: Any)`
- `warn_explicit_for(method: FunctionType, message: PytestWarning)`

### FILE: `parity_env/lib/python3.14/site-packages/_pytest/warnings.py`

#### Functions
- `catch_warnings_for_item(
    config: Config,
    ihook,
    when: Literal["config", "collect", "runtest"],
    item: Item | None,
    *,
    record: bool = True,
)`
- `warning_record_to_str(warning_message: warnings.WarningMessage)`
- `pytest_runtest_protocol(item: Item)`
- `pytest_collection(session: Session)`
- `pytest_terminal_summary(
    terminalreporter: TerminalReporter,
)`
- `pytest_sessionfinish(session: Session)`
- `pytest_load_initial_conftests(
    early_config: Config,
)`
- `pytest_configure(config: Config)`

### FILE: `parity_env/lib/python3.14/site-packages/iniconfig/__init__.py`

#### Classes
- `SectionWrapper`
- `IniConfig`

#### Functions
- `__init__(self, config: "IniConfig", name: str)`
- `lineof(self, name: str)`
- `get(self, key: str)`
- `get(
        self,
        key: str,
        convert: Callable[[str], _T],
    )`
- `get(
        self,
        key: str,
        default: None,
        convert: Callable[[str], _T],
    )`
- `get(self, key: str, default: _D, convert: None = None)`
- `get(
        self,
        key: str,
        default: _D,
        convert: Callable[[str], _T],
    )`
- `get(  # type: ignore [misc]
        self,
        key: str,
        default: _D | None = None,
        convert: Callable[[str], _T] | None = None,
    )`
- `__getitem__(self, key: str)`
- `__iter__(self)`
- `lineof(key: str)`
- `items(self)`
- `__init__(
        self,
        path: str | os.PathLike[str],
        data: str | None = None,
        encoding: str = "utf-8",
        *,
        _sections: Mapping[str, Mapping[str, str]] | None = None,
        _sources: Mapping[tuple[str, str | None], int] | None = None,
    )`
- `parse(
        cls,
        path: str | os.PathLike[str],
        data: str | None = None,
        encoding: str = "utf-8",
        *,
        strip_inline_comments: bool = True,
        strip_section_whitespace: bool = False,
    )`
- `lineof(self, section: str, name: str | None = None)`
- `get(
        self,
        section: str,
        name: str,
    )`
- `get(
        self,
        section: str,
        name: str,
        convert: Callable[[str], _T],
    )`
- `get(
        self,
        section: str,
        name: str,
        default: None,
        convert: Callable[[str], _T],
    )`
- `get(
        self, section: str, name: str, default: _D, convert: None = None
    )`
- `get(
        self,
        section: str,
        name: str,
        default: _D,
        convert: Callable[[str], _T],
    )`
- `get(  # type: ignore
        self,
        section: str,
        name: str,
        default: _D | None = None,
        convert: Callable[[str], _T] | None = None,
    )`
- `__getitem__(self, name: str)`
- `__iter__(self)`
- `__contains__(self, arg: str)`

### FILE: `parity_env/lib/python3.14/site-packages/iniconfig/_parse.py`

#### Classes
- `ParsedLine`

#### Functions
- `parse_ini_data(
    path: str,
    data: str,
    *,
    strip_inline_comments: bool,
    strip_section_whitespace: bool = False,
)`
- `parse_lines(
    path: str,
    line_iter: list[str],
    *,
    strip_inline_comments: bool = False,
    strip_section_whitespace: bool = False,
)`
- `_parseline(
    path: str,
    line: str,
    lineno: int,
    strip_inline_comments: bool,
    strip_section_whitespace: bool,
)`
- `iscommentline(line: str)`

#### Parameters / Constants
- `COMMENTCHARS` = `"#;"`

### FILE: `parity_env/lib/python3.14/site-packages/iniconfig/_version.py`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`
- `VERSION_TUPLE` = `Tuple[Union[int, str], ...]`
- `COMMIT_ID` = `Union[str, None]`
- `VERSION_TUPLE` = `object`
- `COMMIT_ID` = `object`

### FILE: `parity_env/lib/python3.14/site-packages/iniconfig/exceptions.py`

#### Classes
- `ParseError`

#### Functions
- `__init__(self, path: str, lineno: int, msg: str)`
- `__str__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_elffile.py`

#### Classes
- `ELFInvalid`
- `EIClass`
- `EIData`
- `EMachine`
- `ELFFile`

#### Functions
- `__init__(self, f: IO[bytes])`
- `_read(self, fmt: str)`
- `interpreter(self)`

#### Parameters / Constants
- `C32` = `1`
- `C64` = `2`
- `I386` = `3`
- `S390` = `22`
- `X8664` = `62`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_manylinux.py`

#### Classes
- `_GLibCVersion`

#### Functions
- `_parse_elf(path: str)`
- `_is_linux_armhf(executable: str)`
- `_is_linux_i686(executable: str)`
- `_have_compatible_abi(executable: str, archs: Sequence[str])`
- `_glibc_version_string_confstr()`
- `_glibc_version_string_ctypes()`
- `_glibc_version_string()`
- `_parse_glibc_version(version_str: str)`
- `_get_glibc_version()`
- `_get_manylinux_module()`
- `_is_compatible(arch: str, version: _GLibCVersion)`
- `platform_tags(archs: Sequence[str])`

#### Parameters / Constants
- `EF_ARM_ABIMASK` = `0xFF000000`
- `EF_ARM_ABI_VER5` = `0x05000000`
- `EF_ARM_ABI_FLOAT_HARD` = `0x00000400`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_musllinux.py`

#### Classes
- `_MuslVersion`

#### Functions
- `_parse_musl_version(output: str)`
- `_get_musl_version(executable: str)`
- `platform_tags(archs: Sequence[str])`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_parser.py`

#### Classes
- `Node`
- `Variable`
- `Value`
- `Op`
- `ParsedRequirement`

#### Functions
- `__init__(self, value: str)`
- `__str__(self)`
- `__repr__(self)`
- `serialize(self)`
- `__getstate__(self)`
- `_restore_value(self, value: object)`
- `__setstate__(self, state: object)`
- `serialize(self)`
- `serialize(self)`
- `serialize(self)`
- `parse_requirement(source: str)`
- `_parse_requirement(tokenizer: Tokenizer)`
- `_parse_requirement_details(
    tokenizer: Tokenizer,
)`
- `_parse_requirement_marker(
    tokenizer: Tokenizer, *, span_start: int, expected: str
)`
- `_parse_extras(tokenizer: Tokenizer)`
- `_parse_extras_list(tokenizer: Tokenizer)`
- `_parse_specifier(tokenizer: Tokenizer)`
- `_parse_version_many(tokenizer: Tokenizer)`
- `parse_marker(source: str)`
- `_parse_full_marker(tokenizer: Tokenizer)`
- `_parse_marker(tokenizer: Tokenizer)`
- `_parse_marker_atom(tokenizer: Tokenizer)`
- `_parse_marker_item(tokenizer: Tokenizer)`
- `_parse_marker_var(tokenizer: Tokenizer)`
- `process_env_var(env_var: str)`
- `process_python_str(python_str: str)`
- `_parse_marker_op(tokenizer: Tokenizer)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_ranges.py`

#### Classes
- `BoundaryKind`
- `BoundaryVersion`
- `LowerBound`
- `UpperBound`

#### Functions
- `__init__(self, version: Version, kind: BoundaryKind)`
- `_is_family(self, other: Version)`
- `_order_key(self)`
- `__eq__(self, other: object)`
- `__lt__(self, other: BoundaryVersion | Version)`
- `__gt__(self, other: BoundaryVersion | Version)`
- `__hash__(self)`
- `__repr__(self)`
- `__init__(self, version: _VersionOrBoundary, inclusive: bool)`
- `__eq__(self, other: object)`
- `__lt__(self, other: LowerBound)`
- `__hash__(self)`
- `__repr__(self)`
- `__init__(self, version: _VersionOrBoundary, inclusive: bool)`
- `__eq__(self, other: object)`
- `__lt__(self, other: UpperBound)`
- `__hash__(self)`
- `__repr__(self)`
- `trim_release(release: tuple[int, ...])`
- `_next_prefix_dev0(version: Version)`
- `_base_dev0(version: Version)`
- `coerce_version(version: Version | str)`
- `_make_above_after_posts(version: Version)`
- `above(parsed: Version)`
- `_make_above_after_locals(version: Version)`
- `above(parsed: Version)`
- `_make_below_after_locals(version: Version)`
- `below(parsed: Version)`
- `least_version_above(boundary: BoundaryVersion)`
- `range_is_empty(lower: LowerBound, upper: UpperBound)`
- `intersect_ranges(
    left: Sequence[Interval],
    right: Sequence[Interval],
)`
- `filter_by_ranges(
    ranges: Sequence[Interval],
    iterable: Iterable[Any],
    key: Callable[[Any], Version | str] | None,
    prereleases: bool | None,
    region: Sequence[Interval] = ()`
- `_nearest_release_above_prerelease(version: Version)`
- `_lowest_release_at_or_above(value: Version | BoundaryVersion | None)`
- `ranges_are_prerelease_only(ranges: Sequence[Interval])`
- `wildcard_ranges(op: str, base: Version)`
- `standard_ranges(op: str, version: Version, has_local: bool)`
- `bounds_for_spec(op: str, version_str: str, version: Version)`
- `intersect_specifier_bounds(
    per_specifier_ranges: Iterable[Sequence[Interval]],
)`
- `matches_bounds_only(ranges: Sequence[Interval], version: Version)`
- `resolve_prereleases(
    configured: bool | None, autodetected: bool | None
)`

#### Parameters / Constants
- `AFTER_LOCALS` = `enum.auto()  # after V+local, before V.post0`
- `AFTER_POSTS` = `enum.auto()  # after V.postN, before next release`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_structures.py`

#### Classes
- `InfinityType`
- `NegativeInfinityType`

#### Functions
- `__repr__(self)`
- `__repr__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/_tokenizer.py`

#### Classes
- `Token`
- `ParserSyntaxError`
- `Tokenizer`

#### Functions
- `__init__(
        self,
        message: str,
        *,
        source: str,
        span: tuple[int, int],
    )`
- `__str__(self)`
- `__init__(
        self,
        source: str,
        *,
        rules: Mapping[str, re.Pattern[str]],
    )`
- `consume(self, name: str)`
- `check(self, name: str, *, peek: bool = False)`
- `expect(self, name: str, *, expected: str)`
- `read(self)`
- `raise_syntax_error(
        self,
        message: str,
        *,
        span_start: int | None = None,
        span_end: int | None = None,
    )`
- `enclosing_tokens(
        self, open_token: str, close_token: str, *, around: str
    )`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/dependency_groups.py`

#### Classes
- `DuplicateGroupNames`
- `CyclicDependencyGroup`
- `InvalidDependencyGroupObject`
- `DependencyGroupInclude`
- `DependencyGroupResolver`

#### Functions
- `__dir__()`
- `__init__(self, requested_group: str, group: str, include_group: str)`
- `__reduce__(self)`
- `__init__(self, include_group: str)`
- `__repr__(self)`
- `__init__(
        self,
        dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    )`
- `lookup(self, group: str)`
- `resolve(self, group: str)`
- `_resolve(
        self, group: str, requested_group: str, errors: _ErrorCollector
    )`
- `_parse_group(
        self, group: str, errors: _ErrorCollector
    )`
- `resolve_dependency_groups(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]], /, *groups: str
)`
- `_normalize_name(name: str)`
- `_normalize_group_names(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    errors: _ErrorCollector,
)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/direct_url.py`

#### Classes
- `_FromMappingProtocol`
- `DirectUrlValidationError`
- `_DirectUrlRequiredKeyError`
- `VcsInfo`
- `ArchiveInfo`
- `DirInfo`
- `DirectUrl`

#### Functions
- `__dir__()`
- `_from_dict(cls, d: Mapping[str, Any])`
- `_json_dict_factory(data: list[tuple[str, Any]])`
- `_get(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_required(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_object(
    d: Mapping[str, Any], target_type: type[_FromMappingProtocolT], key: str
)`
- `_strip_auth_from_netloc(netloc: str, safe_user_passwords: Collection[str])`
- `_strip_url(url: str, safe_user_passwords: Collection[str])`
- `_file_url_has_absolute_path(parsed_url: SplitResult)`
- `__init__(
        self,
        cause: str | Exception,
        *,
        context: str | None = None,
    )`
- `__str__(self)`
- `__init__(self, key: str)`
- `__init__(
        self,
        *,
        vcs: str,
        commit_id: str,
        requested_revision: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        hashes: Mapping[str, str] | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        editable: bool | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        url: str,
        archive_info: ArchiveInfo | None = None,
        vcs_info: VcsInfo | None = None,
        dir_info: DirInfo | None = None,
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `from_dict(cls, d: Mapping[str, Any], /)`
- `to_dict(
        self,
        *,
        generate_legacy_hash: bool = False,
        strip_user_password: bool = True,
        safe_user_passwords: Collection[str] = ("git",)`
- `validate(self)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/errors.py`

#### Classes
- `ExceptionGroup`
- `_ErrorCollector`

#### Functions
- `__dir__()`
- `__init__(self, message: str, exceptions: list[Exception])`
- `__repr__(self)`
- `finalize(self, msg: str)`
- `on_exit(self, msg: str)`
- `collect(self, *err_cls: type[Exception])`
- `error(
        self,
        error: Exception,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/licenses/__init__.py`

#### Classes
- `InvalidLicenseExpression`

#### Functions
- `__dir__()`
- `canonicalize_license_expression(
    raw_license_expression: str,
)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/licenses/_spdx.py`

#### Classes
- `SPDXLicense`
- `SPDXException`

#### Parameters / Constants
- `VERSION` = `'3.27.0'`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/markers.py`

#### Classes
- `InvalidMarker`
- `UndefinedComparison`
- `UndefinedEnvironmentName`
- `Environment`
- `Marker`

#### Functions
- `__dir__()`
- `_normalize_extras(
    result: MarkerList | MarkerAtom | str,
)`
- `_normalize_extra_values(results: MarkerList)`
- `_format_marker(
    marker: list[str] | MarkerAtom | str, first: bool | None = True
)`
- `_eval_op(lhs: str, op: Op, rhs: str | AbstractSet[str], *, key: str)`
- `_normalize(
    lhs: str, rhs: str | AbstractSet[str], key: str
)`
- `_lookup_environment(
    environment: dict[str, str | AbstractSet[str]], key: str
)`
- `_evaluate_markers(
    markers: MarkerList, environment: dict[str, str | AbstractSet[str]]
)`
- `_format_full_version(info: sys._version_info)`
- `_cached_default_environment()`
- `default_environment()`
- `__init__(self, marker: str)`
- `_from_markers(cls, markers: MarkerList)`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `__and__(self, other: Marker)`
- `__or__(self, other: Marker)`
- `evaluate(
        self,
        environment: Mapping[str, str | AbstractSet[str]] | None = None,
        context: EvaluateContext = "metadata",
    )`
- `_pep440_python_full_version(python_full_version: str)`
- `_repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
)`

#### Parameters / Constants
- `MARKERS_ALLOWING_SET` = `{"extras", "dependency_groups"}`
- `MARKERS_REQUIRING_VERSION` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/metadata.py`

#### Classes
- `InvalidMetadata`
- `RawMetadata`
- `RFC822Policy`
- `RFC822Message`
- `_Validator`
- `Metadata`

#### Functions
- `__dir__()`
- `__init__(self, field: str, message: str)`
- `__reduce__(self)`
- `_parse_keywords(data: str)`
- `_parse_project_urls(data: list[str])`
- `_get_payload(msg: email.message.Message, source: bytes | str)`
- `header_store_parse(self, name: str, value: str)`
- `__init__(self)`
- `as_bytes(
        self, unixfrom: bool = False, policy: email.policy.Policy | None = None
    )`
- `parse_email(data: bytes | str)`
- `__init__(
        self,
        *,
        added: _MetadataVersion = "1.0",
    )`
- `__set_name__(self, _owner: Metadata, name: str)`
- `__get__(self, instance: Metadata, _owner: type[Metadata])`
- `_invalid_metadata(
        self, msg: str, cause: Exception | None = None
    )`
- `_process_metadata_version(self, value: str)`
- `_process_name(self, value: str)`
- `_process_version(self, value: str)`
- `_process_summary(self, value: str)`
- `_process_description_content_type(self, value: str)`
- `_process_dynamic(self, value: list[str])`
- `_process_provides_extra(
        self,
        value: list[str],
    )`
- `_process_requires_python(self, value: str)`
- `_process_requires_dist(
        self,
        value: list[str],
    )`
- `_process_license_expression(self, value: str)`
- `_process_license_files(self, value: list[str])`
- `_process_import_names(self, value: list[str])`
- `from_raw(cls, data: RawMetadata, *, validate: bool = True)`
- `from_email(cls, data: bytes | str, *, validate: bool = True)`
- `as_rfc822(self)`
- `_write_metadata(self, message: RFC822Message)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/pylock.py`

#### Classes
- `_FromMappingProtocol`
- `PylockValidationError`
- `_PylockRequiredKeyError`
- `PylockUnsupportedVersionError`
- `PylockSelectError`
- `PackageVcs`
- `PackageDirectory`
- `PackageArchive`
- `PackageSdist`
- `PackageWheel`
- `Package`
- `Pylock`

#### Functions
- `__dir__()`
- `_from_dict(cls, d: Mapping[str, Any])`
- `is_valid_pylock_path(path: Path)`
- `_toml_key(key: str)`
- `_toml_value(key: str, value: Any)`
- `_toml_dict_factory(data: list[tuple[str, Any]])`
- `_get(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_required(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_sequence(
    d: Mapping[str, Any], expected_item_type: type[_T], key: str
)`
- `_get_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
)`
- `_get_required_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
)`
- `_get_sequence_as(
    d: Mapping[str, Any],
    expected_item_type: type[_T],
    target_item_type: Callable[[_T], _T2],
    key: str,
)`
- `_get_object(
    d: Mapping[str, Any], target_type: type[_FromMappingProtocolT], key: str
)`
- `_get_sequence_of_objects(
    d: Mapping[str, Any], target_item_type: type[_FromMappingProtocolT], key: str
)`
- `_get_required_sequence_of_objects(
    d: Mapping[str, Any], target_item_type: type[_FromMappingProtocolT], key: str
)`
- `_validate_normalized_name(name: str)`
- `_validate_path_url(path: str | None, url: str | None)`
- `_path_name(path: str | None)`
- `_url_name(url: str | None)`
- `_validate_hashes(hashes: Mapping[str, Any])`
- `__init__(
        self,
        cause: str | Exception,
        *,
        context: str | None = None,
    )`
- `__str__(self)`
- `__init__(self, key: str)`
- `__init__(
        self,
        *,
        type: str,
        url: str | None = None,
        path: str | None = None,
        requested_revision: str | None = None,
        commit_id: str,
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        path: str,
        editable: bool | None = None,
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        url: str | None = None,
        path: str | None = None,
        size: int | None = None,
        upload_time: datetime | None = None,
        hashes: Mapping[str, str],
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        name: str | None = None,
        upload_time: datetime | None = None,
        url: str | None = None,
        path: str | None = None,
        size: int | None = None,
        hashes: Mapping[str, str],
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `filename(self)`
- `__init__(
        self,
        *,
        name: str | None = None,
        upload_time: datetime | None = None,
        url: str | None = None,
        path: str | None = None,
        size: int | None = None,
        hashes: Mapping[str, str],
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `filename(self)`
- `__init__(
        self,
        *,
        name: NormalizedName,
        version: Version | None = None,
        marker: Marker | None = None,
        requires_python: SpecifierSet | None = None,
        dependencies: Sequence[Mapping[str, Any]] | None = None,
        vcs: PackageVcs | None = None,
        directory: PackageDirectory | None = None,
        archive: PackageArchive | None = None,
        index: str | None = None,
        sdist: PackageSdist | None = None,
        wheels: Sequence[PackageWheel] | None = None,
        attestation_identities: Sequence[Mapping[str, Any]] | None = None,
        tool: Mapping[str, Any] | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `is_direct(self)`
- `__init__(
        self,
        *,
        lock_version: Version,
        environments: Sequence[Marker] | None = None,
        requires_python: SpecifierSet | None = None,
        extras: Sequence[NormalizedName] | None = None,
        dependency_groups: Sequence[str] | None = None,
        default_groups: Sequence[str] | None = None,
        created_by: str,
        packages: Sequence[Package],
        tool: Mapping[str, Any] | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `from_dict(cls, d: Mapping[str, Any], /)`
- `to_dict(self)`
- `validate(self)`
- `select(
        self,
        *,
        environment: Environment | None = None,
        tags: Sequence[Tag] | None = None,
        extras: Collection[str] | None = None,
        dependency_groups: Collection[str] | None = None,
        prefer_sdist_predicate: Callable[[NormalizedName], bool] | None = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/ranges.py`

#### Classes
- `_SetOp`
- `VersionRange`

#### Functions
- `__dir__()`
- `_union_ranges(
    left: Sequence[Interval],
    right: Sequence[Interval],
)`
- `_complement_ranges(ranges: Sequence[Interval])`
- `_canonical_floor(bounds: tuple[Interval, ...])`
- `_predecessor_boundary(version: Version)`
- `_canonicalize(bounds: tuple[Interval, ...])`
- `_struct_admits(
    bounds: tuple[Interval, ...], admit_arbitrary: bool, literal: str
)`
- `_bound_version_str(value: BoundaryVersion | Version)`
- `_format_lower(bound: LowerBound)`
- `_format_upper(bound: UpperBound)`
- `_format_intervals(intervals: Sequence[Interval])`
- `_is_dev0_version(version: Version)`
- `_clean_lower(version: Version)`
- `_epoch_floor_lower(
    lower: LowerBound, upper: UpperBound
)`
- `_dev_family_anchor(family: Version)`
- `_encode_lower(lower: LowerBound, keep_dev0: bool)`
- `_encode_upper(upper: UpperBound, keep_dev0: bool)`
- `_detect_equal_wildcard(lower: LowerBound, upper: UpperBound)`
- `_encode_interval(
    lower: LowerBound, upper: UpperBound, keep_dev0: bool
)`
- `_detect_not_equal(
    left_upper: UpperBound, right_lower: LowerBound
)`
- `_decompose_dev0_gap(
    lower_trim: tuple[int, ...],
    upper_trim: tuple[int, ...],
    epoch: int,
    budget: int = _MAX_EXCLUSION_RUN,
)`
- `_encode_gap(left_upper: UpperBound, right_lower: LowerBound)`
- `_encode_gaps(bounds: Sequence[Interval])`
- `_tighten_no_prereleases(bounds: tuple[Interval, ...])`
- `__new__(cls, *args: object, **kwargs: object)`
- `_build(
        cls,
        bounds: tuple[Interval, ...],
        admit: frozenset[str] = frozenset()`
- `_has_literals(self)`
- `_arbitrary_active(self)`
- `_is_plain(self)`
- `_check_policy_compat(self, other: VersionRange)`
- `_merged_region(self, other: VersionRange)`
- `_with_policy(
        self, *, pre_region: tuple[Interval, ...], configured: bool | None
    )`
- `empty(cls, *, prereleases: bool | None = None)`
- `full(
        cls, *, admit_arbitrary: bool = True, prereleases: bool | None = None
    )`
- `singleton(
        cls, version: Version | str, *, prereleases: bool | None = None
    )`
- `intersection(self, other: VersionRange)`
- `union(self, other: VersionRange)`
- `complement(self)`
- `difference(self, other: VersionRange)`
- `_combine_literals(
        self,
        other: VersionRange,
        new_bounds: tuple[Interval, ...],
        *,
        op: _SetOp,
        admit_arbitrary: bool,
        pre_region: tuple[Interval, ...],
        prereleases_configured: bool | None,
    )`
- `_matches_literal(self, literal: str)`
- `__and__(self, other: object)`
- `__or__(self, other: object)`
- `__invert__(self)`
- `__sub__(self, other: object)`
- `is_subset(self, other: VersionRange)`
- `is_superset(self, other: VersionRange)`
- `is_disjoint(self, other: VersionRange)`
- `_same_releases(self, other: VersionRange)`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], Version | str] | None = None,
    )`
- `_filter_with_admission(
        self,
        iterable: Iterable[Any],
        key: Callable[[Any], Version | str] | None,
        prereleases: bool | None,
        arbitrary_active: bool,
        region: tuple[Interval, ...],
    )`
- `admit(item: Any)`
- `_from_specifier_set(cls, specifier_set: SpecifierSet)`
- `to_specifier_set(self)`
- `is_empty(self)`
- `contains(
        self,
        item: Version | str,
        prereleases: bool | None = None,
        installed: bool | None = None,
    )`
- `__contains__(self, item: Version | str)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `__repr__(self)`

#### Parameters / Constants
- `INTERSECTION` = `enum.auto()`
- `UNION` = `enum.auto()`
- `DIFFERENCE` = `enum.auto()`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/requirements.py`

#### Classes
- `InvalidRequirement`
- `Requirement`

#### Functions
- `__dir__()`
- `__init__(self, requirement_string: str)`
- `_iter_parts(self, name: str)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/specifiers.py`

#### Classes
- `InvalidSpecifier`
- `BaseSpecifier`
- `Specifier`
- `SpecifierSet`

#### Functions
- `__dir__()`
- `_validate_spec(spec: object, /)`
- `_validate_pre(pre: object, /)`
- `_fast_match(specifier: Specifier, parsed: Version)`
- `_str(self)`
- `__str__(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`
- `prereleases(self)`
- `prereleases(self, value: bool)`
- `contains(self, item: str, prereleases: bool | None = None)`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], UnparsedVersion] | None = None,
    )`
- `__init__(self, spec: str = "", prereleases: bool | None = None)`
- `_get_spec_version(self, version: str)`
- `_require_spec_version(self, version: str)`
- `_to_ranges(self)`
- `prereleases(self)`
- `prereleases(self, value: bool | None)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `operator(self)`
- `version(self)`
- `__repr__(self)`
- `__str__(self)`
- `_canonical_spec(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`
- `__contains__(self, item: str | Version)`
- `contains(self, item: UnparsedVersion, prereleases: bool | None = None)`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], UnparsedVersion] | None = None,
    )`
- `_apply_prereleases_filter(
    matches: Iterable[Any],
    key: Callable[[Any], UnparsedVersion] | None,
    prereleases: bool | None,
)`
- `__init__(
        self,
        specifiers: str | Iterable[Specifier] = "",
        prereleases: bool | None = None,
    )`
- `_canonical_specs(self)`
- `prereleases(self)`
- `prereleases(self, value: bool | None)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `__repr__(self)`
- `__str__(self)`
- `__hash__(self)`
- `__and__(self, other: SpecifierSet | str)`
- `__eq__(self, other: object)`
- `__len__(self)`
- `__iter__(self)`
- `_get_ranges(self)`
- `is_unsatisfiable(self)`
- `_check_arbitrary_unsatisfiable(self)`
- `to_range(self)`
- `_check_relation_operand(self, other: object)`
- `is_subset(self, other: SpecifierSet)`
- `is_superset(self, other: SpecifierSet)`
- `is_disjoint(self, other: SpecifierSet)`
- `__contains__(self, item: UnparsedVersion)`
- `contains(
        self,
        item: UnparsedVersion,
        prereleases: bool | None = None,
        installed: bool | None = None,
    )`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], UnparsedVersion] | None = None,
    )`
- `_pep440_filter_prereleases(
    iterable: Iterable[Any], key: Callable[[Any], UnparsedVersion] | None
)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/tags.py`

#### Classes
- `UnsortedTagsError`
- `InvalidTag`
- `TooManyTagsError`
- `Tag`

#### Functions
- `__dir__()`
- `_compute_32_bit_interpreter()`
- `__init__(self, interpreter: str, abi: str, platform: str)`
- `interpreter(self)`
- `abi(self)`
- `platform(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `__str__(self)`
- `__repr__(self)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `parse_tag(
    tag: str, *, validate_order: bool = False, limit: int | None = None
)`
- `_get_config_var(name: str, warn: bool = False)`
- `_normalize_string(string: str)`
- `_is_threaded_cpython(abis: list[str])`
- `_abi3_applies(python_version: PythonVersion, threading: bool)`
- `_abi3t_applies(python_version: PythonVersion, threading: bool)`
- `_cpython_abis(py_version: PythonVersion, warn: bool = False)`
- `cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
)`
- `_generic_abi()`
- `generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
)`
- `_py_interpreter_range(py_version: PythonVersion)`
- `pure_python_tags(
    python_version: PythonVersion | None = None,
)`
- `compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
)`
- `_mac_arch(arch: str, is_32bit: bool = _32_BIT_INTERPRETER)`
- `_mac_binary_formats(version: AppleVersion, cpu_arch: str)`
- `mac_platforms(
    version: AppleVersion | None = None, arch: str | None = None
)`
- `ios_platforms(
    version: AppleVersion | None = None, multiarch: str | None = None
)`
- `android_platforms(
    api_level: int | None = None, abi: str | None = None
)`
- `_linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER)`
- `_emscripten_platforms()`
- `_generic_platforms()`
- `platform_tags()`
- `interpreter_name()`
- `interpreter_version(*, warn: bool = False)`
- `_version_nodot(version: PythonVersion)`
- `sys_tags(*, warn: bool = False)`
- `create_compatible_tags_selector(
    tags: Iterable[Tag],
)`
- `selector(
        tagged_things: Iterable[tuple[_T, AbstractSet[Tag]]],
    )`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/utils.py`

#### Classes
- `InvalidName`
- `InvalidWheelFilename`
- `InvalidSdistFilename`

#### Functions
- `__dir__()`
- `canonicalize_name(name: str, *, validate: bool = False)`
- `is_normalized_name(name: str)`
- `canonicalize_version(
    version: Version | str, *, strip_trailing_zero: bool = True
)`
- `parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
)`
- `parse_sdist_filename(filename: str)`

### FILE: `parity_env/lib/python3.14/site-packages/packaging/version.py`

#### Classes
- `_VersionReplace`
- `InvalidVersion`
- `_BaseVersion`
- `_Version`
- `Version`
- `_TrimmedRelease`

#### Functions
- `_deprecated(message: str)`
- `decorator(func: Callable[[...], object])`
- `wrapper(*args: object, **kwargs: object)`
- `__dir__()`
- `normalize_pre(letter: str, /)`
- `parse(version: str)`
- `_key(self)`
- `__hash__(self)`
- `__lt__(self, other: _BaseVersion)`
- `__le__(self, other: _BaseVersion)`
- `__eq__(self, other: object)`
- `__ge__(self, other: _BaseVersion)`
- `__gt__(self, other: _BaseVersion)`
- `__ne__(self, other: object)`
- `_validate_epoch(value: object, /)`
- `_validate_release(value: object, /)`
- `_validate_pre(value: object, /)`
- `_validate_post(value: object, /)`
- `_validate_dev(value: object, /)`
- `_validate_local(value: object, /)`
- `__init__(self, version: str)`
- `from_parts(
        cls,
        *,
        epoch: int = 0,
        release: tuple[int, ...],
        pre: tuple[str, int] | None = None,
        post: int | None = None,
        dev: int | None = None,
        local: str | None = None,
    )`
- `__replace__(self, **kwargs: Unpack[_VersionReplace])`
- `_key(self)`
- `__hash__(self)`
- `__lt__(self, other: _BaseVersion)`
- `__le__(self, other: _BaseVersion)`
- `__eq__(self, other: object)`
- `__ge__(self, other: _BaseVersion)`
- `__gt__(self, other: _BaseVersion)`
- `__ne__(self, other: object)`
- `__getstate__(
        self,
    )`
- `__setstate__(self, state: object)`
- `_version(self)`
- `_version(self, value: _Version)`
- `__repr__(self)`
- `__str__(self)`
- `_str(self)`
- `epoch(self)`
- `release(self)`
- `pre(self)`
- `post(self)`
- `dev(self)`
- `local(self)`
- `public(self)`
- `base_version(self)`
- `is_prerelease(self)`
- `is_postrelease(self)`
- `is_devrelease(self)`
- `major(self)`
- `minor(self)`
- `micro(self)`
- `__init__(self, version: str | Version)`
- `release(self)`
- `_parse_letter_version(
    letter: str | None, number: str | bytes | SupportsInt | None
)`
- `_parse_local_version(local: str | None)`
- `_cmpkey(
    epoch: int,
    release: tuple[int, ...],
    pre: tuple[str, int] | None,
    post: tuple[str, int] | None,
    dev: tuple[str, int] | None,
    local: LocalType | None,
)`

#### Parameters / Constants
- `VERSION_PATTERN` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/__init__.py`

#### Functions
- `main(args: list[str] | None = None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/__pip-runner__.py`

#### Classes
- `PipImportRedirectingFinder`

#### Functions
- `version_str(version)`
- `find_spec(self, fullname, path=None, target=None)`

#### Parameters / Constants
- `PYTHON_REQUIRES` = `(3, 10)`
- `PIP_SOURCES_ROOT` = `dirname(dirname(__file__))`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/__init__.py`

#### Functions
- `main(args: list[str] | None = None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/build_env.py`

#### Classes
- `ExtraEnviron`
- `_Prefix`
- `BuildEnvironmentInstaller`
- `SubprocessBuildEnvironmentInstaller`
- `InprocessBuildEnvironmentInstaller`
- `BuildEnvironment`
- `NoOpBuildEnvironment`

#### Functions
- `_dedup(a: str, b: str)`
- `__init__(self, path: str)`
- `get_runnable_pip()`
- `_get_system_sitepackages()`
- `install(
        self,
        requirements: Iterable[str],
        prefix: _Prefix,
        *,
        kind: str,
        for_req: InstallRequirement | None,
    )`
- `__init__(
        self,
        finder: PackageFinder,
        build_constraints: list[str] | None = None,
        build_constraint_feature_enabled: bool = False,
    )`
- `_deprecation_constraint_check(self)`
- `install(
        self,
        requirements: Iterable[str],
        prefix: _Prefix,
        *,
        kind: str,
        for_req: InstallRequirement | None,
    )`
- `__init__(
        self,
        *,
        finder: PackageFinder,
        build_tracker: BuildTracker,
        wheel_cache: WheelCache,
        build_constraints: Sequence[InstallRequirement] = ()`
- `install(
        self,
        requirements: Iterable[str],
        prefix: _Prefix,
        *,
        kind: str,
        for_req: InstallRequirement | None,
    )`
- `_install_impl(self, requirements: Iterable[str], prefix: _Prefix)`
- `_make_resolver(self)`
- `__init__(self, installer: BuildEnvironmentInstaller)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `check_requirements(
        self, reqs: Iterable[str]
    )`
- `install_requirements(
        self,
        requirements: Iterable[str],
        prefix_as_string: str,
        *,
        kind: str,
        for_req: InstallRequirement | None = None,
    )`
- `__init__(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `cleanup(self)`
- `install_requirements(
        self,
        requirements: Iterable[str],
        prefix_as_string: str,
        *,
        kind: str,
        for_req: InstallRequirement | None = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cache.py`

#### Classes
- `Cache`
- `SimpleWheelCache`
- `EphemWheelCache`
- `CacheEntry`
- `WheelCache`

#### Functions
- `_hash_dict(d: dict[str, str])`
- `__init__(self, cache_dir: str)`
- `_get_cache_path_parts(self, link: Link)`
- `_get_candidates(self, link: Link, canonical_package_name: str)`
- `get_path_for_link(self, link: Link)`
- `get(
        self,
        link: Link,
        package_name: str | None,
        supported_tags: list[Tag],
    )`
- `__init__(self, cache_dir: str)`
- `get_path_for_link(self, link: Link)`
- `get(
        self,
        link: Link,
        package_name: str | None,
        supported_tags: list[Tag],
    )`
- `__init__(self)`
- `__init__(
        self,
        link: Link,
        persistent: bool,
    )`
- `__init__(self, cache_dir: str)`
- `get_path_for_link(self, link: Link)`
- `get_ephem_path_for_link(self, link: Link)`
- `get(
        self,
        link: Link,
        package_name: str | None,
        supported_tags: list[Tag],
    )`
- `get_cache_entry(
        self,
        link: Link,
        package_name: str | None,
        supported_tags: list[Tag],
    )`
- `record_download_origin(cache_dir: str, download_info: DirectUrl)`

#### Parameters / Constants
- `ORIGIN_JSON_NAME` = `"origin.json"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/autocompletion.py`

#### Functions
- `autocomplete()`
- `get_path_completion_type(
    cwords: list[str], cword: int, opts: Iterable[Any]
)`
- `auto_complete_paths(current: str, completion_type: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/base_command.py`

#### Classes
- `Command`

#### Functions
- `__init__(self, name: str, summary: str, isolated: bool = False)`
- `add_options(self)`
- `pip_version_check(self, options: Values, args: list[str])`
- `run(self, options: Values, args: list[str])`
- `_run_wrapper(self, level_number: int, options: Values, args: list[str])`
- `_inner_run()`
- `parse_args(self, args: list[str])`
- `main(self, args: list[str])`
- `_main(self, args: list[str])`
- `handler_map(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/cmdoptions.py`

#### Classes
- `PipOption`

#### Functions
- `raise_option_error(parser: OptionParser, option: Option, msg: str)`
- `make_option_group(group: dict[str, Any], parser: ConfigOptionParser)`
- `check_dist_restriction(options: Values, check_target: bool = False)`
- `check_build_constraints(options: Values)`
- `_path_option_check(option: Option, opt: str, value: str)`
- `_package_name_option_check(option: Option, opt: str, value: str)`
- `exists_action()`
- `extra_index_url()`
- `find_links()`
- `_handle_uploaded_prior_to(
    option: Option, opt: str, value: str, parser: OptionParser
)`
- `uploaded_prior_to()`
- `trusted_host()`
- `constraints()`
- `build_constraints()`
- `requirements()`
- `requirements_from_scripts()`
- `editable()`
- `_handle_src(option: Option, opt_str: str, value: str, parser: OptionParser)`
- `_get_format_control(values: Values, option: Option)`
- `_handle_no_binary(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `_handle_only_binary(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `no_binary()`
- `only_binary()`
- `_get_release_control(values: Values, option: Option)`
- `_handle_all_releases(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `_handle_only_final(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `all_releases()`
- `only_final()`
- `check_release_control_exclusive(options: Values)`
- `_convert_python_version(value: str)`
- `_handle_python_version(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `add_target_python_options(cmd_opts: OptionGroup)`
- `make_target_python(options: Values)`
- `prefer_binary()`
- `_handle_no_cache_dir(
    option: Option, opt: str, value: str, parser: OptionParser
)`
- `_handle_dependency_group(
    option: Option, opt: str, value: str, parser: OptionParser
)`
- `_handle_config_settings(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `_handle_merge_hash(
    option: Option, opt_str: str, value: str, parser: OptionParser
)`
- `check_list_path_option(options: Values)`

#### Parameters / Constants
- `TYPES` = `Option.TYPES + ("path", "package_name")`
- `TYPE_CHECKER` = `Option.TYPE_CHECKER.copy()`
- `ALWAYS_ENABLED_FEATURES` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/command_context.py`

#### Classes
- `CommandContextMixIn`

#### Functions
- `__init__(self)`
- `main_context(self)`
- `enter_context(self, context_provider: AbstractContextManager[_T])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/index_command.py`

#### Classes
- `SessionCommandMixin`
- `IndexGroupCommand`

#### Functions
- `_create_truststore_ssl_context()`
- `__init__(self)`
- `_get_index_urls(cls, options: Values)`
- `get_default_session(self, options: Values)`
- `_build_session(
        self,
        options: Values,
        retries: int | None = None,
        timeout: int | None = None,
    )`
- `_pip_self_version_check_fetch(
    session: PipSession, options: Values
)`
- `_pip_self_version_check_emit(upgrade_prompt: UpgradePrompt | None)`
- `should_exclude_prerelease(
        self, options: Values, package_name: NormalizedName
    )`
- `pip_version_check(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/main.py`

#### Functions
- `main(args: list[str] | None = None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/main_parser.py`

#### Functions
- `create_main_parser()`
- `identify_python_interpreter(python: str)`
- `parse_command(args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/parser.py`

#### Classes
- `PrettyHelpFormatter`
- `UpdatingDefaultsHelpFormatter`
- `CustomOptionParser`
- `ConfigOptionParser`

#### Functions
- `__init__(self, *args: Any, **kwargs: Any)`
- `format_option_strings(self, option: optparse.Option)`
- `format_option(self, option: optparse.Option)`
- `format_heading(self, heading: str)`
- `format_usage(self, usage: str)`
- `format_description(self, description: str | None)`
- `format_epilog(self, epilog: str | None)`
- `expand_default(self, option: optparse.Option)`
- `indent_lines(self, text: str, indent: str)`
- `expand_default(self, option: optparse.Option)`
- `insert_option_group(
        self, idx: int, *args: Any, **kwargs: Any
    )`
- `option_list_all(self)`
- `__init__(
        self,
        *args: Any,
        name: str,
        isolated: bool = False,
        **kwargs: Any,
    )`
- `check_default(self, option: optparse.Option, key: str, val: Any)`
- `_get_ordered_configuration_items(
        self,
    )`
- `_update_defaults(self, defaults: dict[str, Any])`
- `get_default_values(self)`
- `error(self, msg: str)`
- `print_help(self, file: Any = None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/progress_bars.py`

#### Functions
- `_rich_download_progress_bar(
    iterable: Iterable[bytes],
    *,
    bar_type: BarType,
    size: int | None,
    initial_progress: int | None = None,
)`
- `_rich_install_progress_bar(
    iterable: Iterable[InstallRequirement], *, total: int
)`
- `_raw_progress_bar(
    iterable: Iterable[bytes],
    *,
    size: int | None,
    initial_progress: int | None = None,
)`
- `write_progress(current: int, total: int)`
- `get_download_progress_renderer(
    *, bar_type: BarType, size: int | None = None, initial_progress: int | None = None
)`
- `get_install_progress_renderer(
    *, bar_type: BarType, total: int
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/req_command.py`

#### Classes
- `RequirementCommand`

#### Functions
- `should_ignore_regular_constraints(options: Values)`
- `with_cleanup(
    func: Callable[[_CommandT, Values, list[str]], int],
)`
- `configure_tempdir_registry(registry: TempDirectoryTypeRegistry)`
- `wrapper(self: _CommandT, options: Values, args: list[str])`
- `parse_constraint_files(
    constraint_files: list[str],
    finder: PackageFinder,
    options: Values,
    session: PipSession,
)`
- `__init__(self, *args: Any, **kw: Any)`
- `determine_resolver_variant(options: Values)`
- `make_requirement_preparer(
        cls,
        temp_build_dir: TempDirectory,
        options: Values,
        build_tracker: BuildTracker,
        session: PipSession,
        finder: PackageFinder,
        use_user_site: bool,
        download_dir: str | None = None,
        verbosity: int = 0,
    )`
- `make_resolver(
        cls,
        preparer: RequirementPreparer,
        finder: PackageFinder,
        options: Values,
        wheel_cache: WheelCache | None = None,
        use_user_site: bool = False,
        ignore_installed: bool = True,
        ignore_requires_python: bool = False,
        force_reinstall: bool = False,
        upgrade_strategy: str = "to-satisfy-only",
        py_version_info: tuple[int, ...] | None = None,
    )`
- `get_requirements(
        self,
        args: list[str],
        options: Values,
        finder: PackageFinder,
        session: PipSession,
    )`
- `trace_basic_info(finder: PackageFinder)`
- `_build_package_finder(
        self,
        options: Values,
        session: PipSession,
        target_python: TargetPython | None = None,
        ignore_requires_python: bool = False,
    )`

#### Parameters / Constants
- `KEEPABLE_TEMPDIR_TYPES` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/spinners.py`

#### Classes
- `SpinnerInterface`
- `InteractiveSpinner`
- `NonInteractiveSpinner`
- `RateLimiter`
- `_PipRichSpinner`

#### Functions
- `spin(self)`
- `finish(self, final_status: str)`
- `__init__(
        self,
        message: str,
        file: IO[str] | None = None,
        spin_chars: str = SPINNER_CHARS,
        # Empirically, 8 updates/second looks nice
        min_update_interval_seconds: float = 1 / SPINS_PER_SECOND,
    )`
- `_write(self, status: str)`
- `spin(self)`
- `finish(self, final_status: str)`
- `__init__(self, message: str, min_update_interval_seconds: float = 60.0)`
- `_update(self, status: str)`
- `spin(self)`
- `finish(self, final_status: str)`
- `__init__(self, min_update_interval_seconds: float)`
- `ready(self)`
- `reset(self)`
- `open_spinner(message: str)`
- `__init__(self, label: str)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `__rich_measure__(
        self, console: Console, options: ConsoleOptions
    )`
- `render(self)`
- `finish(self, status: str)`
- `open_rich_spinner(label: str, console: Console | None = None)`
- `hidden_cursor(file: IO[str])`

#### Parameters / Constants
- `HIDE_CURSOR` = `"\x1b[?25l"`
- `SHOW_CURSOR` = `"\x1b[?25h"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/cli/status_codes.py`

#### Parameters / Constants
- `SUCCESS` = `0`
- `ERROR` = `1`
- `UNKNOWN_ERROR` = `2`
- `VIRTUALENV_NOT_FOUND` = `3`
- `PREVIOUS_BUILD_DIR_ERROR` = `4`
- `NO_MATCHES_FOUND` = `23`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/__init__.py`

#### Functions
- `create_command(name: str, **kwargs: Any)`
- `get_similar_commands(name: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/cache.py`

#### Classes
- `CacheCommand`

#### Functions
- `add_options(self)`
- `handler_map(self)`
- `run(self, options: Values, args: list[str])`
- `get_cache_dir(self, options: Values, args: list[str])`
- `get_cache_info(self, options: Values, args: list[str])`
- `list_cache_items(self, options: Values, args: list[str])`
- `format_for_human(self, files: list[str])`
- `format_for_abspath(self, files: list[str])`
- `remove_cache_items(self, options: Values, args: list[str])`
- `purge_cache(self, options: Values, args: list[str])`
- `_cache_dir(self, options: Values, subdir: str)`
- `_find_http_files(self, options: Values)`
- `_find_wheels(self, options: Values, pattern: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/check.py`

#### Classes
- `CheckCommand`

#### Functions
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/completion.py`

#### Classes
- `CompletionCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

#### Parameters / Constants
- `BASE_COMPLETION` = `"""`
- `COMPLETION_SCRIPTS` = `{`
- `COMPREPLY` = `( $( COMP_WORDS="${{COMP_WORDS[*]}}" \\`
- `COMP_CWORD` = `$COMP_CWORD \\`
- `PIP_AUTO_COMPLETE` = `1 "$1" 2>/dev/null ) )`
- `COMP_CWORD` = `$((CURRENT-1)) \\`
- `PIP_AUTO_COMPLETE` = `1 $words[1] 2>/dev/null )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/configuration.py`

#### Classes
- `ConfigurationCommand`

#### Functions
- `add_options(self)`
- `handler_map(self)`
- `run(self, options: Values, args: list[str])`
- `_determine_file(self, options: Values, need_value: bool)`
- `list_values(self, options: Values, args: list[str])`
- `get_name(self, options: Values, args: list[str])`
- `set_name_value(self, options: Values, args: list[str])`
- `unset_name(self, options: Values, args: list[str])`
- `list_config_values(self, options: Values, args: list[str])`
- `print_config_file_values(self, variant: Kind, fname: str)`
- `print_env_var_values(self)`
- `open_in_editor(self, options: Values, args: list[str])`
- `_get_n_args(self, args: list[str], example: str, n: int)`
- `_save_configuration(self)`
- `_determine_editor(self, options: Values)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/debug.py`

#### Classes
- `DebugCommand`

#### Functions
- `show_value(name: str, value: Any)`
- `show_sys_implementation()`
- `create_vendor_txt_map()`
- `get_module_from_module_name(module_name: str)`
- `get_vendor_version_from_module(module_name: str)`
- `show_actual_vendor_versions(vendor_txt_versions: dict[str, str])`
- `show_vendor_versions()`
- `show_tags(options: Values)`
- `ca_bundle_info(config: Configuration)`
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/download.py`

#### Classes
- `DownloadCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/freeze.py`

#### Classes
- `FreezeCommand`

#### Functions
- `_should_suppress_build_backends()`
- `_dev_pkgs()`
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/hash.py`

#### Classes
- `HashCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`
- `_hash_of_file(path: str, algorithm: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/help.py`

#### Classes
- `HelpCommand`

#### Functions
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/index.py`

#### Classes
- `IndexCommand`

#### Functions
- `add_options(self)`
- `handler_map(self)`
- `run(self, options: Values, args: list[str])`
- `_build_package_finder(
        self,
        options: Values,
        session: PipSession,
        target_python: TargetPython | None = None,
        ignore_requires_python: bool = False,
    )`
- `get_available_package_versions(self, options: Values, args: list[Any])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/inspect.py`

#### Classes
- `InspectCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`
- `_dist_to_dict(self, dist: BaseDistribution)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/install.py`

#### Classes
- `InstallCommand`

#### Functions
- `_prevent_import_hook(name: str, args: tuple[Any, ...])`
- `_eagerly_import_modules()`
- `_prevent_further_imports()`
- `_arg_refers_to_pip(arg: str)`
- `add_options(self)`
- `pip_version_check(self, options: Values, args: list[str])`
- `run(self, options: Values, args: list[str])`
- `_handle_target_dir(
        self, target_dir: str, target_temp_dir: TempDirectory, upgrade: bool
    )`
- `_determine_conflicts(
        self, to_install: list[InstallRequirement]
    )`
- `_warn_about_conflicts(
        self, conflict_details: ConflictDetails, resolver_variant: str
    )`
- `installed_packages_summary(
    installed: list[InstallationResult], env: BaseEnvironment
)`
- `get_lib_location_guesses(
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    isolated: bool = False,
    prefix: str | None = None,
)`
- `site_packages_writable(root: str | None, isolated: bool)`
- `decide_user_install(
    use_user_site: bool | None,
    prefix_path: str | None = None,
    target_dir: str | None = None,
    root_path: str | None = None,
    isolated_mode: bool = False,
)`
- `create_os_error_message(
    error: OSError, show_traceback: bool, using_user_site: bool
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/list.py`

#### Classes
- `_DistWithLatestInfo`
- `ListCommand`

#### Functions
- `add_options(self)`
- `pip_version_check(self, options: Values, args: list[str])`
- `_build_package_finder(
        self, options: Values, session: PipSession
    )`
- `run(self, options: Values, args: list[str])`
- `get_outdated(
        self, packages: _ProcessedDists, options: Values
    )`
- `get_uptodate(
        self, packages: _ProcessedDists, options: Values
    )`
- `get_not_required(
        self, packages: _ProcessedDists, options: Values
    )`
- `iter_packages_latest_infos(
        self, packages: _ProcessedDists, options: Values
    )`
- `latest_info(
                dist: _DistWithLatestInfo,
            )`
- `output_package_listing(
        self, packages: _ProcessedDists, options: Values
    )`
- `output_package_listing_columns(
        self, data: list[list[str]], header: list[str]
    )`
- `format_for_columns(
    pkgs: _ProcessedDists, options: Values
)`
- `wheel_build_tag(dist: BaseDistribution)`
- `format_for_json(packages: _ProcessedDists, options: Values)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/lock.py`

#### Classes
- `LockCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/search.py`

#### Classes
- `TransformedHit`
- `SearchCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`
- `search(self, query: list[str], options: Values)`
- `transform_hits(hits: list[dict[str, str]])`
- `print_dist_installation_info(latest: str, dist: BaseDistribution | None)`
- `get_installed_distribution(name: str)`
- `print_results(
    hits: list[TransformedHit],
    name_column_width: int | None = None,
    terminal_width: int | None = None,
)`
- `highest_version(versions: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/show.py`

#### Classes
- `ShowCommand`
- `_PackageInfo`

#### Functions
- `normalize_project_url_label(label: str)`
- `add_options(self)`
- `run(self, options: Values, args: list[str])`
- `search_packages_info(query: list[str])`
- `_get_requiring_packages(current_dist: BaseDistribution)`
- `print_results(
    distributions: Iterable[_PackageInfo],
    list_files: bool,
    verbose: bool,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/uninstall.py`

#### Classes
- `UninstallCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/commands/wheel.py`

#### Classes
- `WheelCommand`

#### Functions
- `add_options(self)`
- `run(self, options: Values, args: list[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/configuration.py`

#### Classes
- `Configuration`

#### Functions
- `_normalize_name(name: str)`
- `_disassemble_key(name: str)`
- `get_configuration_files()`
- `__init__(self, isolated: bool, load_only: Kind | None = None)`
- `load(self)`
- `get_file_to_edit(self)`
- `items(self)`
- `get_value(self, key: str)`
- `set_value(self, key: str, value: Any)`
- `unset_value(self, key: str)`
- `save(self)`
- `_ensure_have_load_only(self)`
- `_dictionary(self)`
- `_load_config_files(self)`
- `_load_file(self, variant: Kind, fname: str)`
- `_construct_parser(self, fname: str)`
- `_load_environment_vars(self)`
- `_normalized_keys(
        self, section: str, items: Iterable[tuple[str, Any]]
    )`
- `get_environ_vars(self)`
- `iter_config_files(self)`
- `get_values_in_config(self, variant: Kind)`
- `_get_parser_to_modify(self)`
- `_mark_as_modified(self, fname: str, parser: RawConfigParser)`
- `__repr__(self)`

#### Parameters / Constants
- `CONFIG_BASENAME` = `"pip.ini" if WINDOWS else "pip.conf"`
- `ENV_NAMES_IGNORED` = `"version", "help"`
- `USER` = `"user",  # User Specific`
- `GLOBAL` = `"global",  # System Wide`
- `SITE` = `"site",  # [Virtual] Environment Specific`
- `ENV` = `"env",  # from PIP_CONFIG_FILE`
- `ENV_VAR` = `"env-var",  # from Environment Variables`
- `OVERRIDE_ORDER` = `kinds.GLOBAL, kinds.USER, kinds.SITE, kinds.ENV, kinds.ENV_VAR`
- `VALID_LOAD_ONLY` = `kinds.USER, kinds.GLOBAL, kinds.SITE`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/__init__.py`

#### Functions
- `make_distribution_for_install_requirement(
    install_req: InstallRequirement,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/base.py`

#### Classes
- `AbstractDistribution`

#### Functions
- `__init__(self, req: InstallRequirement)`
- `build_tracker_id(self)`
- `get_metadata_distribution(self)`
- `prepare_distribution_metadata(
        self,
        build_env_installer: BuildEnvironmentInstaller,
        build_isolation: bool,
        check_build_deps: bool,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/installed.py`

#### Classes
- `InstalledDistribution`

#### Functions
- `build_tracker_id(self)`
- `get_metadata_distribution(self)`
- `prepare_distribution_metadata(
        self,
        build_env_installer: BuildEnvironmentInstaller,
        build_isolation: bool,
        check_build_deps: bool,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/sdist.py`

#### Classes
- `SourceDistribution`

#### Functions
- `build_tracker_id(self)`
- `get_metadata_distribution(self)`
- `prepare_distribution_metadata(
        self,
        build_env_installer: BuildEnvironmentInstaller,
        build_isolation: bool,
        check_build_deps: bool,
    )`
- `_prepare_build_backend(
        self, build_env_installer: BuildEnvironmentInstaller
    )`
- `_get_build_requires_wheel(self)`
- `_get_build_requires_editable(self)`
- `_install_build_reqs(
        self, build_env_installer: BuildEnvironmentInstaller
    )`
- `_raise_conflicts(
        self, conflicting_with: str, conflicting_reqs: set[tuple[str, str]]
    )`
- `_raise_missing_reqs(self, missing: set[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/distributions/wheel.py`

#### Classes
- `WheelDistribution`

#### Functions
- `build_tracker_id(self)`
- `get_metadata_distribution(self)`
- `prepare_distribution_metadata(
        self,
        build_env_installer: BuildEnvironmentInstaller,
        build_isolation: bool,
        check_build_deps: bool,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/exceptions.py`

#### Classes
- `PipError`
- `DiagnosticPipError`
- `ConfigurationError`
- `InstallationError`
- `FailedToPrepareCandidate`
- `MissingPyProjectBuildRequires`
- `InvalidPyProjectBuildRequires`
- `NoneMetadataError`
- `UserInstallationInvalid`
- `InvalidSchemeCombination`
- `DistributionNotFound`
- `RequirementsFileParseError`
- `BestVersionAlreadyInstalled`
- `BadCommand`
- `CommandError`
- `PreviousBuildDirError`
- `NetworkConnectionError`
- `InvalidWheelFilename`
- `UnsupportedWheel`
- `InvalidWheel`
- `MetadataInconsistent`
- `MetadataInvalid`
- `InstallationSubprocessError`
- `MetadataGenerationFailed`
- `HashErrors`
- `HashError`
- `VcsHashUnsupported`
- `DirectoryUrlHashUnsupported`
- `HashMissing`
- `HashUnpinned`
- `HashMismatch`
- `UnsupportedPythonVersion`
- `ConfigurationFileCouldNotBeLoaded`
- `ExternallyManagedEnvironment`
- `UninstallMissingRecord`
- `LegacyDistutilsInstall`
- `InvalidInstalledPackage`
- `IncompleteDownloadError`
- `ResolutionTooDeepError`
- `InstallWheelBuildError`
- `InvalidEggFragment`
- `BuildDependencyInstallError`

#### Functions
- `_is_kebab_case(s: str)`
- `_prefix_with_indent(
    s: Text | str,
    console: Console,
    *,
    prefix: str,
    indent: str,
)`
- `__init__(
        self,
        *,
        kind: Literal["error", "warning"] = "error",
        reference: str | None = None,
        message: str | Text,
        context: str | Text | None,
        hint_stmt: str | Text | None,
        note_stmt: str | Text | None = None,
        link: str | None = None,
    )`
- `__repr__(self)`
- `__rich_console__(
        self,
        console: Console,
        options: ConsoleOptions,
    )`
- `__init__(
        self, *, package_name: str, requirement_chain: str, failed_step: str
    )`
- `__init__(self, *, package: str)`
- `__init__(self, *, package: str, reason: str)`
- `__init__(
        self,
        dist: BaseDistribution,
        metadata_name: str,
    )`
- `__str__(self)`
- `__str__(self)`
- `__str__(self)`
- `__init__(
        self,
        error_msg: str,
        response: Response | None = None,
        request: Request | PreparedRequest | None = None,
    )`
- `__str__(self)`
- `__init__(self, location: str, name: str)`
- `__str__(self)`
- `__init__(
        self, ireq: InstallRequirement, field: str, f_val: str, m_val: str
    )`
- `__str__(self)`
- `__init__(self, ireq: InstallRequirement, error: str)`
- `__str__(self)`
- `__init__(
        self,
        *,
        command_description: str,
        exit_code: int,
        output_lines: list[str] | None,
    )`
- `__str__(self)`
- `__init__(
        self,
        *,
        package_details: str,
    )`
- `__str__(self)`
- `__init__(self)`
- `append(self, error: HashError)`
- `__str__(self)`
- `__bool__(self)`
- `body(self)`
- `__str__(self)`
- `_requirement_name(self)`
- `__init__(self, gotten_hash: str)`
- `body(self)`
- `__init__(self, allowed: dict[str, list[str]], gots: dict[str, _Hash])`
- `body(self)`
- `_hash_comparison(self)`
- `hash_then_or(hash_name: str)`
- `__init__(
        self,
        reason: str = "could not be loaded",
        fname: str | None = None,
        error: configparser.Error | None = None,
    )`
- `__str__(self)`
- `__init__(self, error: str | None)`
- `_iter_externally_managed_error_keys()`
- `from_config(
        cls,
        config: pathlib.Path | str,
    )`
- `__init__(self, *, distribution: BaseDistribution)`
- `__init__(self, *, distribution: BaseDistribution)`
- `__init__(
        self,
        *,
        dist: BaseDistribution,
        invalid_exc: InvalidRequirement | InvalidVersion,
    )`
- `__init__(self, download: _FileDownload)`
- `__init__(self)`
- `__init__(self, failed: list[InstallRequirement])`
- `__init__(self, link: Link, fragment: str)`
- `__init__(
        self,
        req: InstallRequirement | None,
        build_reqs: Iterable[str],
        *,
        cause: Exception,
        log_lines: list[str] | None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/index/collector.py`

#### Classes
- `_NotAPIContent`
- `_NotHTTP`
- `CacheablePageContent`
- `ParseLinks`
- `IndexContent`
- `HTMLLinkParser`
- `CollectedSources`
- `LinkCollector`

#### Functions
- `_match_vcs_scheme(url: str)`
- `__init__(self, content_type: str, request_desc: str)`
- `_ensure_api_header(response: Response)`
- `_ensure_api_response(url: str, session: PipSession)`
- `_get_simple_response(url: str, session: PipSession)`
- `_get_encoding_from_headers(headers: ResponseHeaders)`
- `__init__(self, page: IndexContent)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `__call__(self, page: IndexContent)`
- `with_cached_index_content(fn: ParseLinks)`
- `wrapper(cacheable_page: CacheablePageContent)`
- `wrapper_wrapper(page: IndexContent)`
- `parse_links(page: IndexContent)`
- `__str__(self)`
- `__init__(self, url: str)`
- `handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]])`
- `get_href(self, attrs: list[tuple[str, str | None]])`
- `_handle_get_simple_fail(
    link: Link,
    reason: str | Exception,
    meth: Callable[..., None] | None = None,
)`
- `_make_index_content(
    response: Response, cache_link_parsing: bool = True
)`
- `_get_index_content(link: Link, *, session: PipSession)`
- `__init__(
        self,
        session: PipSession,
        search_scope: SearchScope,
    )`
- `create(
        cls,
        session: PipSession,
        options: Values,
        suppress_no_index: bool = False,
    )`
- `find_links(self)`
- `fetch_response(self, location: Link)`
- `collect_sources(
        self,
        project_name: str,
        candidates_from_page: CandidatesFromPage,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/index/package_finder.py`

#### Classes
- `LinkType`
- `LinkEvaluator`
- `CandidatePreferences`
- `BestCandidateResult`
- `CandidateEvaluator`
- `PackageFinder`

#### Functions
- `_check_link_requires_python(
    link: Link,
    version_info: tuple[int, int, int],
    ignore_requires_python: bool = False,
)`
- `__init__(
        self,
        project_name: str,
        canonical_name: NormalizedName,
        formats: frozenset[str],
        target_python: TargetPython,
        allow_yanked: bool,
        ignore_requires_python: bool = False,
        uploaded_prior_to: datetime.datetime | None = None,
    )`
- `evaluate_link(self, link: Link)`
- `get_version_sort_key(v: str)`
- `filter_unallowed_hashes(
    candidates: list[InstallationCandidate],
    hashes: Hashes | None,
    project_name: str,
)`
- `__post_init__(self)`
- `create(
        cls,
        project_name: str,
        target_python: TargetPython | None = None,
        prefer_binary: bool = False,
        release_control: ReleaseControl | None = None,
        specifier: specifiers.BaseSpecifier | None = None,
        hashes: Hashes | None = None,
    )`
- `__init__(
        self,
        project_name: str,
        supported_tags: list[Tag],
        specifier: specifiers.BaseSpecifier,
        prefer_binary: bool = False,
        release_control: ReleaseControl | None = None,
        hashes: Hashes | None = None,
    )`
- `get_applicable_candidates(
        self,
        candidates: list[InstallationCandidate],
    )`
- `_sort_key(self, candidate: InstallationCandidate)`
- `sort_best_candidate(
        self,
        candidates: list[InstallationCandidate],
    )`
- `compute_best_candidate(
        self,
        candidates: list[InstallationCandidate],
    )`
- `__init__(
        self,
        link_collector: LinkCollector,
        target_python: TargetPython,
        allow_yanked: bool,
        format_control: FormatControl | None = None,
        candidate_prefs: CandidatePreferences | None = None,
        ignore_requires_python: bool = False,
        uploaded_prior_to: datetime.datetime | None = None,
    )`
- `create(
        cls,
        link_collector: LinkCollector,
        selection_prefs: SelectionPreferences,
        target_python: TargetPython | None = None,
        uploaded_prior_to: datetime.datetime | None = None,
    )`
- `target_python(self)`
- `search_scope(self)`
- `search_scope(self, search_scope: SearchScope)`
- `find_links(self)`
- `index_urls(self)`
- `proxy(self)`
- `trusted_hosts(self)`
- `custom_cert(self)`
- `client_cert(self)`
- `release_control(self)`
- `set_release_control(self, release_control: ReleaseControl)`
- `prefer_binary(self)`
- `set_prefer_binary(self)`
- `uploaded_prior_to(self)`
- `requires_python_skipped_reasons(self)`
- `make_link_evaluator(self, project_name: str)`
- `_sort_links(self, links: Iterable[Link])`
- `_log_skipped_link(self, link: Link, result: LinkType, detail: str)`
- `get_install_candidate(
        self, link_evaluator: LinkEvaluator, link: Link
    )`
- `evaluate_links(
        self, link_evaluator: LinkEvaluator, links: Iterable[Link]
    )`
- `process_project_url(
        self, project_url: Link, link_evaluator: LinkEvaluator
    )`
- `find_all_candidates(self, project_name: str)`
- `make_candidate_evaluator(
        self,
        project_name: str,
        specifier: specifiers.BaseSpecifier | None = None,
        hashes: Hashes | None = None,
    )`
- `find_best_candidate(
        self,
        project_name: str,
        specifier: specifiers.BaseSpecifier | None = None,
        hashes: Hashes | None = None,
    )`
- `find_requirement(
        self, req: InstallRequirement, upgrade: bool
    )`
- `_format_versions(cand_iter: Iterable[InstallationCandidate])`
- `_should_install_candidate(
            candidate: InstallationCandidate | None,
        )`
- `_find_name_version_sep(fragment: str, canonical_name: str)`
- `_extract_version_from_fragment(fragment: str, canonical_name: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/index/sources.py`

#### Classes
- `LinkSource`
- `_FlatDirectoryToUrls`
- `_FlatDirectorySource`
- `_LocalFileSource`
- `_RemoteFileSource`
- `_IndexDirectorySource`

#### Functions
- `link(self)`
- `page_candidates(self)`
- `file_links(self)`
- `_is_html_file(file_url: str)`
- `__init__(self, path: str)`
- `_scan_directory(self)`
- `page_candidates(self)`
- `project_name_to_urls(self)`
- `__init__(
        self,
        candidates_from_page: CandidatesFromPage,
        path: str,
        project_name: str,
    )`
- `link(self)`
- `page_candidates(self)`
- `file_links(self)`
- `__init__(
        self,
        candidates_from_page: CandidatesFromPage,
        link: Link,
    )`
- `link(self)`
- `page_candidates(self)`
- `file_links(self)`
- `__init__(
        self,
        candidates_from_page: CandidatesFromPage,
        page_validator: PageValidator,
        link: Link,
    )`
- `link(self)`
- `page_candidates(self)`
- `file_links(self)`
- `__init__(
        self,
        candidates_from_page: CandidatesFromPage,
        link: Link,
    )`
- `link(self)`
- `page_candidates(self)`
- `file_links(self)`
- `build_source(
    location: str,
    *,
    candidates_from_page: CandidatesFromPage,
    page_validator: PageValidator,
    expand_dir: bool,
    cache_link_parsing: bool,
    project_name: str,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/locations/__init__.py`

#### Functions
- `_should_use_sysconfig()`
- `_looks_like_bpo_44860()`
- `_looks_like_red_hat_patched_platlib_purelib(scheme: dict[str, str])`
- `_looks_like_red_hat_lib()`
- `_looks_like_debian_scheme()`
- `_looks_like_red_hat_scheme()`
- `_looks_like_slackware_scheme()`
- `_looks_like_msys2_mingw_scheme()`
- `_warn_mismatched(old: pathlib.Path, new: pathlib.Path, *, key: str)`
- `_warn_if_mismatch(old: pathlib.Path, new: pathlib.Path, *, key: str)`
- `_log_context(
    *,
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    prefix: str | None = None,
)`
- `get_scheme(
    dist_name: str,
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    isolated: bool = False,
    prefix: str | None = None,
)`
- `get_bin_prefix()`
- `get_bin_user()`
- `_looks_like_deb_system_dist_packages(value: str)`
- `get_purelib()`
- `get_platlib()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/locations/_distutils.py`

#### Functions
- `distutils_scheme(
    dist_name: str,
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    isolated: bool = False,
    prefix: str | None = None,
    *,
    ignore_config_files: bool = False,
)`
- `get_scheme(
    dist_name: str,
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    isolated: bool = False,
    prefix: str | None = None,
)`
- `get_bin_prefix()`
- `get_purelib()`
- `get_platlib()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/locations/_sysconfig.py`

#### Functions
- `_should_use_osx_framework_prefix()`
- `_infer_prefix()`
- `_infer_user()`
- `_infer_home()`
- `get_scheme(
    dist_name: str,
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    isolated: bool = False,
    prefix: str | None = None,
)`
- `get_bin_prefix()`
- `get_purelib()`
- `get_platlib()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/locations/base.py`

#### Functions
- `get_major_minor_version()`
- `change_root(new_root: str, pathname: str)`
- `get_src_prefix()`
- `is_osx_framework()`

#### Parameters / Constants
- `USER_CACHE_DIR` = `appdirs.user_cache_dir("pip")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/main.py`

#### Functions
- `main(args: list[str] | None = None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/__init__.py`

#### Classes
- `Backend`

#### Functions
- `_should_use_importlib_metadata()`
- `_emit_pkg_resources_deprecation_if_needed()`
- `select_backend()`
- `get_default_environment()`
- `get_environment(paths: list[str] | None)`
- `get_directory_distribution(directory: str)`
- `get_wheel_distribution(
    wheel: Wheel, canonical_name: NormalizedName
)`
- `get_metadata_distribution(
    metadata_contents: bytes,
    filename: str,
    canonical_name: str,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/_json.py`

#### Functions
- `json_name(field: str)`
- `msg_to_json(msg: Message)`
- `sanitise_header(h: Header | str)`

#### Parameters / Constants
- `METADATA_FIELDS` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/base.py`

#### Classes
- `BaseEntryPoint`
- `RequiresEntry`
- `BaseDistribution`
- `BaseEnvironment`
- `Wheel`
- `FilesystemWheel`
- `MemoryWheel`

#### Functions
- `name(self)`
- `value(self)`
- `group(self)`
- `_convert_installed_files_path(
    entry: tuple[str, ...],
    info: tuple[str, ...],
)`
- `from_directory(cls, directory: str)`
- `from_metadata_file_contents(
        cls,
        metadata_contents: bytes,
        filename: str,
        project_name: str,
    )`
- `from_wheel(cls, wheel: Wheel, name: str)`
- `__repr__(self)`
- `__str__(self)`
- `location(self)`
- `editable_project_location(self)`
- `installed_location(self)`
- `info_location(self)`
- `installed_by_distutils(self)`
- `installed_as_egg(self)`
- `installed_with_setuptools_egg_info(self)`
- `installed_with_dist_info(self)`
- `canonical_name(self)`
- `version(self)`
- `raw_version(self)`
- `setuptools_filename(self)`
- `direct_url(self)`
- `installer(self)`
- `requested(self)`
- `editable(self)`
- `local(self)`
- `in_usersite(self)`
- `in_site_packages(self)`
- `is_file(self, path: InfoPath)`
- `iter_distutils_script_names(self)`
- `read_text(self, path: InfoPath)`
- `iter_entry_points(self)`
- `_metadata_impl(self)`
- `metadata(self)`
- `metadata_dict(self)`
- `metadata_version(self)`
- `raw_name(self)`
- `requires_python(self)`
- `iter_dependencies(self, extras: Collection[str] = ()`
- `iter_raw_dependencies(self)`
- `iter_provided_extras(self)`
- `_iter_declared_entries_from_record(self)`
- `_iter_declared_entries_from_legacy(self)`
- `iter_declared_entries(self)`
- `_iter_requires_txt_entries(self)`
- `_iter_egg_info_extras(self)`
- `_iter_egg_info_dependencies(self)`
- `_add_egg_info_requires(self, metadata: email.message.Message)`
- `default(cls)`
- `from_paths(cls, paths: list[str] | None)`
- `get_distribution(self, name: str)`
- `_iter_distributions(self)`
- `iter_all_distributions(self)`
- `iter_installed_distributions(
        self,
        local_only: bool = True,
        skip: Container[str] = stdlib_pkgs,
        include_editables: bool = True,
        editables_only: bool = False,
        user_only: bool = False,
    )`
- `as_zipfile(self)`
- `__init__(self, location: str)`
- `as_zipfile(self)`
- `__init__(self, location: str, stream: IO[bytes])`
- `as_zipfile(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/__init__.py`

#### Parameters / Constants
- `NAME` = `"importlib"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/_compat.py`

#### Classes
- `BadMetadata`
- `BasePath`

#### Functions
- `__init__(self, dist: importlib.metadata.Distribution, *, reason: str)`
- `__str__(self)`
- `name(self)`
- `parent(self)`
- `get_info_location(d: importlib.metadata.Distribution)`
- `parse_name_and_version_from_info_directory(
    dist: importlib.metadata.Distribution,
)`
- `get_dist_canonical_name(dist: importlib.metadata.Distribution)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/_dists.py`

#### Classes
- `WheelDistribution`
- `Distribution`

#### Functions
- `__init__(
        self,
        files: Mapping[pathlib.PurePosixPath, bytes],
        info_location: pathlib.PurePosixPath,
    )`
- `from_zipfile(
        cls,
        zf: zipfile.ZipFile,
        name: str,
        location: str,
    )`
- `iterdir(self, path: InfoPath)`
- `read_text(self, filename: str)`
- `locate_file(self, path: str | PathLike[str])`
- `__init__(
        self,
        dist: importlib.metadata.Distribution,
        info_location: BasePath | None,
        installed_location: BasePath | None,
    )`
- `from_directory(cls, directory: str)`
- `from_metadata_file_contents(
        cls,
        metadata_contents: bytes,
        filename: str,
        project_name: str,
    )`
- `from_wheel(cls, wheel: Wheel, name: str)`
- `location(self)`
- `info_location(self)`
- `installed_location(self)`
- `canonical_name(self)`
- `version(self)`
- `raw_version(self)`
- `is_file(self, path: InfoPath)`
- `iter_distutils_script_names(self)`
- `read_text(self, path: InfoPath)`
- `iter_entry_points(self)`
- `_metadata_impl(self)`
- `iter_provided_extras(self)`
- `iter_dependencies(self, extras: Collection[str] = ()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/importlib/_envs.py`

#### Classes
- `_DistributionFinder`
- `Environment`

#### Functions
- `_looks_like_wheel(location: str)`
- `__init__(self)`
- `_find_impl(self, location: str)`
- `find(self, location: str)`
- `find_legacy_editables(self, location: str)`
- `__init__(self, paths: Sequence[str])`
- `default(cls)`
- `from_paths(cls, paths: list[str] | None)`
- `_iter_distributions(self)`
- `get_distribution(self, name: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/metadata/pkg_resources.py`

#### Classes
- `EntryPoint`
- `InMemoryMetadata`
- `Distribution`
- `Environment`

#### Functions
- `__init__(self, metadata: Mapping[str, bytes], wheel_name: str)`
- `has_metadata(self, name: str)`
- `get_metadata(self, name: str)`
- `get_metadata_lines(self, name: str)`
- `metadata_isdir(self, name: str)`
- `metadata_listdir(self, name: str)`
- `run_script(self, script_name: str, namespace: str)`
- `__init__(self, dist: pkg_resources.Distribution)`
- `_extra_mapping(self)`
- `from_directory(cls, directory: str)`
- `from_metadata_file_contents(
        cls,
        metadata_contents: bytes,
        filename: str,
        project_name: str,
    )`
- `from_wheel(cls, wheel: Wheel, name: str)`
- `location(self)`
- `installed_location(self)`
- `info_location(self)`
- `installed_by_distutils(self)`
- `canonical_name(self)`
- `version(self)`
- `raw_version(self)`
- `is_file(self, path: InfoPath)`
- `iter_distutils_script_names(self)`
- `read_text(self, path: InfoPath)`
- `iter_entry_points(self)`
- `_metadata_impl(self)`
- `iter_dependencies(self, extras: Collection[str] = ()`
- `iter_provided_extras(self)`
- `__init__(self, ws: pkg_resources.WorkingSet)`
- `default(cls)`
- `from_paths(cls, paths: list[str] | None)`
- `_iter_distributions(self)`
- `_search_distribution(self, name: str)`
- `get_distribution(self, name: str)`

#### Parameters / Constants
- `NAME` = `"pkg_resources"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/candidate.py`

#### Classes
- `InstallationCandidate`

#### Functions
- `__init__(self, name: str, version: str, link: Link)`
- `__str__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/direct_url.py`

#### Classes
- `DirectUrl`

#### Functions
- `to_dict_compat(self)`
- `from_json(cls, s: str)`
- `to_json(self)`
- `is_local_editable(self)`

#### Parameters / Constants
- `DIRECT_URL_METADATA_NAME` = `"direct_url.json"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/format_control.py`

#### Classes
- `FormatControl`

#### Functions
- `__init__(
        self,
        no_binary: set[str] | None = None,
        only_binary: set[str] | None = None,
    )`
- `__eq__(self, other: object)`
- `__repr__(self)`
- `handle_mutual_excludes(value: str, target: set[str], other: set[str])`
- `get_allowed_formats(self, canonical_name: str)`
- `disallow_binaries(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/index.py`

#### Classes
- `PackageIndex`

#### Functions
- `__init__(self, url: str, file_storage_domain: str)`
- `_url_for_path(self, path: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/installation_report.py`

#### Classes
- `InstallationReport`

#### Functions
- `__init__(self, install_requirements: Sequence[InstallRequirement])`
- `_install_req_to_dict(cls, ireq: InstallRequirement)`
- `to_dict(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/link.py`

#### Classes
- `LinkHash`
- `MetadataFile`
- `Link`
- `_CleanResult`

#### Functions
- `__post_init__(self)`
- `find_hash_url_fragment(cls, url: str)`
- `as_dict(self)`
- `as_hashes(self)`
- `is_hash_allowed(self, hashes: Hashes | None)`
- `__post_init__(self)`
- `supported_hashes(hashes: dict[str, str] | None)`
- `_clean_url_path_part(part: str)`
- `_clean_file_url_path(part: str)`
- `_clean_url_path(path: str, is_local_path: bool)`
- `_ensure_quoted_url(url: str)`
- `_absolute_link_url(base_url: str, url: str)`
- `__init__(
        self,
        url: str,
        comes_from: str | None = None,
        requires_python: str | None = None,
        yanked_reason: str | None = None,
        metadata_file_data: MetadataFile | None = None,
        upload_time: datetime.datetime | None = None,
        cache_link_parsing: bool = True,
        hashes: Mapping[str, str] | None = None,
    )`
- `from_json(
        cls,
        file_data: dict[str, Any],
        page_url: str,
    )`
- `from_element(
        cls,
        anchor_attribs: dict[str, str | None],
        page_url: str,
        base_url: str,
    )`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: Any)`
- `__lt__(self, other: Any)`
- `url(self)`
- `redacted_url(self)`
- `filename(self)`
- `file_path(self)`
- `scheme(self)`
- `netloc(self)`
- `path(self)`
- `splitext(self)`
- `ext(self)`
- `url_without_fragment(self)`
- `_egg_fragment(self)`
- `subdirectory_fragment(self)`
- `metadata_link(self)`
- `as_hashes(self)`
- `hash(self)`
- `hash_name(self)`
- `show_url(self)`
- `is_file(self)`
- `is_existing_dir(self)`
- `is_wheel(self)`
- `is_vcs(self)`
- `is_yanked(self)`
- `has_hash(self)`
- `is_hash_allowed(self, hashes: Hashes | None)`
- `_clean_link(link: Link)`
- `links_equivalent(link1: Link, link2: Link)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/release_control.py`

#### Classes
- `ReleaseControl`

#### Functions
- `handle_mutual_excludes(
        self, value: str, target: set[str], other: set[str], attr_name: str
    )`
- `get_ordered_args(self)`
- `allows_prereleases(self, canonical_name: NormalizedName)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/scheme.py`

#### Classes
- `Scheme`

#### Parameters / Constants
- `SCHEME_KEYS` = `["platlib", "purelib", "headers", "scripts", "data"]`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/search_scope.py`

#### Classes
- `SearchScope`

#### Functions
- `create(
        cls,
        find_links: list[str],
        index_urls: list[str],
        no_index: bool,
    )`
- `get_formatted_locations(self)`
- `get_index_urls_locations(self, project_name: str)`
- `mkurl_pypi_url(url: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/selection_prefs.py`

#### Classes
- `SelectionPreferences`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/target_python.py`

#### Classes
- `TargetPython`

#### Functions
- `__init__(
        self,
        platforms: list[str] | None = None,
        py_version_info: tuple[int, ...] | None = None,
        abis: list[str] | None = None,
        implementation: str | None = None,
    )`
- `format_given(self)`
- `get_sorted_tags(self)`
- `get_unsorted_tags(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/models/wheel.py`

#### Classes
- `Wheel`

#### Functions
- `__init__(self, filename: str)`
- `get_formatted_file_tags(self)`
- `support_index_min(self, tags: list[Tag])`
- `find_most_preferred_tag(
        self, tags: list[Tag], tag_to_priority: dict[Tag, int]
    )`
- `supported(self, tags: Iterable[Tag])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/auth.py`

#### Classes
- `Credentials`
- `KeyRingBaseProvider`
- `KeyRingNullProvider`
- `KeyRingPythonProvider`
- `KeyRingCliProvider`
- `MultiDomainBasicAuth`

#### Functions
- `get_auth_info(self, url: str, username: str | None)`
- `save_auth_info(self, url: str, username: str, password: str)`
- `get_auth_info(self, url: str, username: str | None)`
- `save_auth_info(self, url: str, username: str, password: str)`
- `__init__(self)`
- `get_auth_info(self, url: str, username: str | None)`
- `save_auth_info(self, url: str, username: str, password: str)`
- `__init__(self, cmd: str)`
- `get_auth_info(self, url: str, username: str | None)`
- `save_auth_info(self, url: str, username: str, password: str)`
- `_get_password(self, service_name: str, username: str)`
- `_set_password(self, service_name: str, username: str, password: str)`
- `get_keyring_provider(provider: str)`
- `PATH_as_shutil_which_determines_it()`
- `__init__(
        self,
        prompting: bool = True,
        index_urls: list[str] | None = None,
        keyring_provider: str = "auto",
    )`
- `keyring_provider(self)`
- `keyring_provider(self, provider: str)`
- `use_keyring(self)`
- `_get_keyring_auth(
        self,
        url: str | None,
        username: str | None,
    )`
- `_get_index_url(self, url: str)`
- `_get_new_credentials(
        self,
        original_url: str,
        *,
        allow_netrc: bool = True,
        allow_keyring: bool = False,
    )`
- `_get_url_and_credentials(
        self, original_url: str
    )`
- `__call__(self, req: PreparedRequest)`
- `_prompt_for_password(self, netloc: str)`
- `_should_save_password_to_keyring(self)`
- `handle_401(self, resp: Response, **kwargs: Any)`
- `warn_on_401(self, resp: Response, **kwargs: Any)`
- `save_credentials(self, resp: Response, **kwargs: Any)`

#### Parameters / Constants
- `KEYRING_DISABLED` = `False`
- `KEYRING_DISABLED` = `True`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/cache.py`

#### Classes
- `SafeFileCache`

#### Functions
- `is_from_cache(response: Response)`
- `suppressed_cache_errors()`
- `__init__(self, directory: str)`
- `_get_cache_path(self, name: str)`
- `get(self, key: str)`
- `_write_to_file(self, path: str, writer_func: Callable[[BinaryIO], Any])`
- `_write(self, path: str, data: bytes)`
- `_write_from_io(self, path: str, source_file: BinaryIO)`
- `set(
        self, key: str, value: bytes, expires: int | datetime | None = None
    )`
- `delete(self, key: str)`
- `get_body(self, key: str)`
- `set_body(self, key: str, body: bytes)`
- `set_body_from_io(self, key: str, body_file: BinaryIO)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/download.py`

#### Classes
- `_FileDownload`
- `Downloader`

#### Functions
- `_get_http_response_size(resp: Response)`
- `_get_http_response_etag_or_last_modified(resp: Response)`
- `_log_download(
    resp: Response,
    link: Link,
    progress_bar: BarType,
    total_length: int | None,
    range_start: int | None = 0,
)`
- `sanitize_content_filename(filename: str)`
- `parse_content_disposition(content_disposition: str, default_filename: str)`
- `_get_http_response_filename(resp: Response, link: Link)`
- `is_incomplete(self)`
- `write_chunk(self, data: bytes)`
- `reset_file(self)`
- `__init__(
        self,
        session: PipSession,
        progress_bar: BarType,
    )`
- `batch(
        self, links: Iterable[Link], location: str
    )`
- `__call__(self, link: Link, location: str)`
- `_process_response(self, download: _FileDownload, resp: Response)`
- `_attempt_resumes_or_redownloads(
        self, download: _FileDownload, first_resp: Response
    )`
- `_cache_resumed_download(
        self, download: _FileDownload, original_response: Response
    )`
- `_http_get_resume(
        self, download: _FileDownload, should_match: Response
    )`
- `_http_get(self, link: Link, headers: Mapping[str, str] = HEADERS)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/lazy_wheel.py`

#### Classes
- `HTTPRangeRequestUnsupported`
- `LazyZipOverHTTP`

#### Functions
- `dist_from_wheel_url(
    name: NormalizedName, url: str, session: PipSession
)`
- `__init__(
        self, url: str, session: PipSession, chunk_size: int = CONTENT_CHUNK_SIZE
    )`
- `mode(self)`
- `name(self)`
- `seekable(self)`
- `close(self)`
- `closed(self)`
- `read(self, size: int = -1)`
- `readable(self)`
- `seek(self, offset: int, whence: int = 0)`
- `tell(self)`
- `truncate(self, size: int | None = None)`
- `writable(self)`
- `__enter__(self)`
- `__exit__(self, *exc: Any)`
- `_stay(self)`
- `_check_zip(self)`
- `_stream_response(
        self, start: int, end: int, base_headers: dict[str, str] = HEADERS
    )`
- `_merge(
        self, start: int, end: int, left: int, right: int
    )`
- `_download(self, start: int, end: int)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/session.py`

#### Classes
- `LocalFSAdapter`
- `_SSLContextAdapterMixin`
- `HTTPAdapter`
- `CacheControlAdapter`
- `InsecureHTTPAdapter`
- `InsecureCacheControlAdapter`
- `PipSession`

#### Functions
- `looks_like_ci()`
- `user_agent()`
- `send(
        self,
        request: PreparedRequest,
        stream: bool = False,
        timeout: float | tuple[float, float] | tuple[float, None] | None = None,
        verify: bool | str = True,
        cert: bytes | str | tuple[bytes | str, bytes | str] | None = None,
        proxies: Mapping[str, str] | None = None,
    )`
- `close(self)`
- `__init__(
        self,
        *,
        ssl_context: SSLContext | None = None,
        **kwargs: Any,
    )`
- `init_poolmanager(
        self,
        connections: int,
        maxsize: int,
        block: bool = DEFAULT_POOLBLOCK,
        **pool_kwargs: Any,
    )`
- `proxy_manager_for(self, proxy: str, **proxy_kwargs: Any)`
- `cert_verify(
        self,
        conn: ConnectionPool,
        url: str,
        verify: bool | str,
        cert: str | tuple[str, str] | None,
    )`
- `cert_verify(
        self,
        conn: ConnectionPool,
        url: str,
        verify: bool | str,
        cert: str | tuple[str, str] | None,
    )`
- `__init__(
        self,
        *args: Any,
        retries: int = 0,
        resume_retries: int = 0,
        cache: str | None = None,
        trusted_hosts: Sequence[str] = ()`
- `update_index_urls(self, new_index_urls: list[str])`
- `add_trusted_host(
        self, host: str, source: str | None = None, suppress_logging: bool = False
    )`
- `iter_secure_origins(self)`
- `is_secure_origin(self, location: Link)`
- `request(self, method: str, url: str, *args: Any, **kwargs: Any)`

#### Parameters / Constants
- `CI_ENVIRONMENT_VARIABLES` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/utils.py`

#### Functions
- `raise_for_status(resp: Response)`
- `response_chunks(
    response: Response, chunk_size: int = DOWNLOAD_CHUNK_SIZE
)`

#### Parameters / Constants
- `DOWNLOAD_CHUNK_SIZE` = `256 * 1024`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/network/xmlrpc.py`

#### Classes
- `PipXmlrpcTransport`

#### Functions
- `__init__(
        self, index_url: str, session: PipSession, use_datetime: bool = False
    )`
- `request(
        self,
        host: "_HostType",
        handler: str,
        request_body: "SizedBuffer",
        verbose: bool = False,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/build_tracker.py`

#### Classes
- `TrackerId`
- `BuildTracker`

#### Functions
- `update_env_context_manager(**changes: str)`
- `get_build_tracker()`
- `__init__(self, root: str)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `_entry_path(self, key: TrackerId)`
- `add(self, req: InstallRequirement, key: TrackerId)`
- `remove(self, req: InstallRequirement, key: TrackerId)`
- `cleanup(self)`
- `track(self, req: InstallRequirement, key: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/metadata.py`

#### Functions
- `generate_metadata(
    build_env: BuildEnvironment, backend: BuildBackendHookCaller, details: str
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/metadata_editable.py`

#### Functions
- `generate_editable_metadata(
    build_env: BuildEnvironment, backend: BuildBackendHookCaller, details: str
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/wheel.py`

#### Functions
- `build_wheel_pep517(
    name: str,
    backend: BuildBackendHookCaller,
    metadata_directory: str,
    wheel_directory: str,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/build/wheel_editable.py`

#### Functions
- `build_wheel_editable(
    name: str,
    backend: BuildBackendHookCaller,
    metadata_directory: str,
    wheel_directory: str,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/check.py`

#### Classes
- `PackageDetails`

#### Functions
- `create_package_set_from_installed()`
- `check_package_set(
    package_set: PackageSet, should_ignore: Callable[[str], bool] | None = None
)`
- `check_install_conflicts(to_install: list[InstallRequirement])`
- `check_unsupported(
    packages: Iterable[BaseDistribution],
    supported_tags: Iterable[Tag],
)`
- `_simulate_installation_of(
    to_install: list[InstallRequirement], package_set: PackageSet
)`
- `_create_whitelist(
    would_be_installed: set[NormalizedName], package_set: PackageSet
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/freeze.py`

#### Classes
- `_EditableInfo`
- `FrozenRequirement`

#### Functions
- `freeze(
    requirement: list[str] | None = None,
    local_only: bool = False,
    user_only: bool = False,
    paths: list[str] | None = None,
    isolated: bool = False,
    exclude_editable: bool = False,
    skip: Container[str] = ()`
- `_format_as_name_version(dist: BaseDistribution)`
- `_get_editable_info(dist: BaseDistribution)`
- `canonical_name(self)`
- `from_dist(cls, dist: BaseDistribution)`
- `__str__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/install/wheel.py`

#### Classes
- `File`
- `ZipBackedFile`
- `ScriptFile`
- `MissingCallableSuffix`
- `PipScriptMaker`

#### Functions
- `save(self)`
- `rehash(path: str, blocksize: int = 1 << 20)`
- `csv_io_kwargs(mode: str)`
- `fix_script(path: str)`
- `wheel_root_is_purelib(metadata: Message)`
- `get_entrypoints(dist: BaseDistribution)`
- `message_about_scripts_not_on_PATH(scripts: Sequence[str])`
- `_normalized_outrows(
    outrows: Iterable[InstalledCSVRow],
)`
- `_record_to_fs_path(record_path: RecordPath, lib_dir: str)`
- `_fs_to_record_path(path: str, lib_dir: str)`
- `get_csv_rows_for_installed(
    old_csv_rows: list[list[str]],
    installed: dict[RecordPath, RecordPath],
    changed: set[RecordPath],
    generated: list[str],
    lib_dir: str,
)`
- `get_console_script_specs(console: dict[str, str])`
- `__init__(
        self, src_record_path: RecordPath, dest_path: str, zip_file: ZipFile
    )`
- `_getinfo(self)`
- `save(self)`
- `__init__(self, file: File)`
- `save(self)`
- `__init__(self, entry_point: str)`
- `_raise_for_invalid_entrypoint(specification: str, scripts_dir: str)`
- `make(
        self, specification: str, options: dict[str, Any] | None = None
    )`
- `_install_wheel(  # noqa: C901, PLR0915 function is too long
    name: str,
    wheel_zip: ZipFile,
    wheel_path: str,
    scheme: Scheme,
    pycompile: bool = True,
    warn_script_location: bool = True,
    direct_url: DirectUrl | None = None,
    requested: bool = False,
)`
- `record_installed(
        srcfile: RecordPath, destfile: str, modified: bool = False
    )`
- `is_dir_path(path: RecordPath)`
- `assert_no_path_traversal(dest_dir_path: str, target_path: str)`
- `root_scheme_file_maker(
        zip_file: ZipFile, dest: str
    )`
- `make_root_scheme_file(record_path: RecordPath)`
- `data_scheme_file_maker(
        zip_file: ZipFile, scheme: Scheme
    )`
- `make_data_scheme_file(record_path: RecordPath)`
- `is_data_scheme_path(path: RecordPath)`
- `is_script_scheme_path(path: RecordPath)`
- `is_entrypoint_wrapper(file: File)`
- `pyc_source_file_paths()`
- `pyc_output_path(path: str)`
- `_generate_file(path: str, **kwargs: Any)`
- `req_error_context(req_description: str)`
- `install_wheel(
    name: str,
    wheel_path: str,
    scheme: Scheme,
    req_description: str,
    pycompile: bool = True,
    warn_script_location: bool = True,
    direct_url: DirectUrl | None = None,
    requested: bool = False,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/operations/prepare.py`

#### Classes
- `File`
- `RequirementPreparer`

#### Functions
- `_get_prepared_distribution(
    req: InstallRequirement,
    build_tracker: BuildTracker,
    build_env_installer: BuildEnvironmentInstaller,
    build_isolation: bool,
    check_build_deps: bool,
)`
- `unpack_vcs_link(link: Link, location: str, verbosity: int)`
- `__post_init__(self)`
- `get_http_url(
    link: Link,
    download: Downloader,
    download_dir: str | None = None,
    hashes: Hashes | None = None,
)`
- `get_file_url(
    link: Link, download_dir: str | None = None, hashes: Hashes | None = None
)`
- `unpack_url(
    link: Link,
    location: str,
    download: Downloader,
    verbosity: int,
    download_dir: str | None = None,
    hashes: Hashes | None = None,
)`
- `_check_download_dir(
    link: Link,
    download_dir: str,
    hashes: Hashes | None,
    warn_on_hash_mismatch: bool = True,
)`
- `__init__(
        self,
        *,
        build_dir: str,
        download_dir: str | None,
        src_dir: str,
        build_isolation: bool,
        build_isolation_installer: BuildEnvironmentInstaller,
        check_build_deps: bool,
        build_tracker: BuildTracker,
        session: PipSession,
        progress_bar: BarType,
        finder: PackageFinder,
        require_hashes: bool,
        use_user_site: bool,
        lazy_wheel: bool,
        verbosity: int,
        legacy_resolver: bool,
    )`
- `_log_preparing_link(self, req: InstallRequirement)`
- `_ensure_link_req_src_dir(
        self, req: InstallRequirement, parallel_builds: bool
    )`
- `_get_linked_req_hashes(self, req: InstallRequirement)`
- `_fetch_metadata_only(
        self,
        req: InstallRequirement,
    )`
- `_fetch_metadata_using_link_data_attr(
        self,
        req: InstallRequirement,
    )`
- `_fetch_metadata_using_lazy_wheel(
        self,
        link: Link,
    )`
- `_complete_partial_requirements(
        self,
        partially_downloaded_reqs: Iterable[InstallRequirement],
        parallel_builds: bool = False,
    )`
- `prepare_linked_requirement(
        self, req: InstallRequirement, parallel_builds: bool = False
    )`
- `prepare_linked_requirements_more(
        self, reqs: Iterable[InstallRequirement], parallel_builds: bool = False
    )`
- `_prepare_linked_requirement(
        self, req: InstallRequirement, parallel_builds: bool
    )`
- `save_linked_requirement(self, req: InstallRequirement)`
- `prepare_editable_requirement(
        self,
        req: InstallRequirement,
    )`
- `prepare_installed_requirement(
        self,
        req: InstallRequirement,
        skip_reason: str,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/pyproject.py`

#### Functions
- `_is_list_of_str(obj: Any)`
- `make_pyproject_path(unpacked_source_directory: str)`
- `load_pyproject_toml(
    pyproject_toml: str, setup_py: str, req_name: str
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/__init__.py`

#### Classes
- `InstallationResult`

#### Functions
- `_validate_requirements(
    requirements: list[InstallRequirement],
)`
- `install_given_reqs(
    requirements: list[InstallRequirement],
    root: str | None,
    home: str | None,
    prefix: str | None,
    warn_script_location: bool,
    use_user_site: bool,
    pycompile: bool,
    progress_bar: BarType,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/constructors.py`

#### Classes
- `RequirementParts`

#### Functions
- `_strip_extras(path: str)`
- `convert_extras(extras: str | None)`
- `_set_requirement_extras(req: Requirement, new_extras: set[str])`
- `_parse_direct_url_editable(editable_req: str)`
- `_parse_pip_syntax_editable(editable_req: str)`
- `parse_editable(editable_req: str)`
- `check_first_requirement_in_file(filename: str)`
- `deduce_helpful_msg(req: str)`
- `parse_req_from_editable(editable_req: str)`
- `install_req_from_editable(
    editable_req: str,
    comes_from: InstallRequirement | str | None = None,
    *,
    isolated: bool = False,
    hash_options: dict[str, list[str]] | None = None,
    constraint: bool = False,
    user_supplied: bool = False,
    permit_editable_wheels: bool = False,
    config_settings: dict[str, str | list[str]] | None = None,
)`
- `_looks_like_path(name: str)`
- `_get_url_from_path(path: str, name: str)`
- `parse_req_from_line(name: str, line_source: str | None)`
- `with_source(text: str)`
- `_parse_req_string(req_as_string: str)`
- `install_req_from_line(
    name: str,
    comes_from: str | InstallRequirement | None = None,
    *,
    isolated: bool = False,
    hash_options: dict[str, list[str]] | None = None,
    constraint: bool = False,
    line_source: str | None = None,
    user_supplied: bool = False,
    config_settings: dict[str, str | list[str]] | None = None,
)`
- `install_req_from_req_string(
    req_string: str,
    comes_from: InstallRequirement | None = None,
    isolated: bool = False,
    user_supplied: bool = False,
)`
- `install_req_from_parsed_requirement(
    parsed_req: ParsedRequirement,
    isolated: bool = False,
    user_supplied: bool = False,
    config_settings: dict[str, str | list[str]] | None = None,
)`
- `install_req_from_link_and_ireq(
    link: Link, ireq: InstallRequirement
)`
- `install_req_drop_extras(ireq: InstallRequirement)`
- `install_req_extend_extras(
    ireq: InstallRequirement,
    extras: Collection[str],
)`
- `_pylock_hashes_to_hash_options(hashes: Mapping[str, str])`
- `install_req_from_pylock_package(
    package: pylock.Package,
    package_dist: (
        pylock.PackageVcs
        | pylock.PackageArchive
        | pylock.PackageDirectory
        | pylock.PackageSdist
        | pylock.PackageWheel
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/pep723.py`

#### Classes
- `PEP723Exception`

#### Functions
- `__init__(self, msg: str)`
- `pep723_metadata(scriptfile: str)`

#### Parameters / Constants
- `REGEX` = `r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s(?P<content>(^#(| .*)$\s)+)^# ///$"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_dependency_group.py`

#### Functions
- `parse_dependency_groups(groups: list[tuple[str, str]])`
- `_resolve_all_groups(
    resolvers: dict[str, DependencyGroupResolver], groups: list[tuple[str, str]]
)`
- `_build_resolvers(paths: Iterable[str])`
- `_load_pyproject(path: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_file.py`

#### Classes
- `ParsedRequirement`
- `ParsedLine`
- `RequirementsFileParser`
- `OptionParsingError`

#### Functions
- `is_editable(self)`
- `requirement(self)`
- `parse_requirements(
    filename: str,
    session: PipSession,
    finder: PackageFinder | None = None,
    options: optparse.Values | None = None,
    constraint: bool = False,
)`
- `preprocess(content: str)`
- `handle_requirement_line(
    line: ParsedLine,
    options: optparse.Values | None = None,
)`
- `handle_option_line(
    opts: Values,
    filename: str,
    lineno: int,
    finder: PackageFinder | None = None,
    options: optparse.Values | None = None,
    session: PipSession | None = None,
)`
- `handle_line(
    line: ParsedLine,
    options: optparse.Values | None = None,
    finder: PackageFinder | None = None,
    session: PipSession | None = None,
)`
- `__init__(
        self,
        session: PipSession,
        line_parser: LineParser,
    )`
- `parse(
        self, filename: str, constraint: bool
    )`
- `_parse_and_recurse(
        self,
        filename: str,
        constraint: bool,
        parsed_files_stack: list[dict[str, str | None]],
    )`
- `_parse_file(
        self, filename: str, constraint: bool
    )`
- `get_line_parser(finder: PackageFinder | None)`
- `parse_line(line: str)`
- `break_args_options(line: str)`
- `__init__(self, msg: str)`
- `build_parser()`
- `parser_exit(self: Any, msg: str)`
- `join_lines(lines_enum: ReqFileLines)`
- `ignore_comments(lines_enum: ReqFileLines)`
- `expand_env_variables(lines_enum: ReqFileLines)`
- `get_file_content(
    url: str, session: PipSession, *, constraint: bool = False
)`
- `_decode_req_file(data: bytes, url: str)`

#### Parameters / Constants
- `SCHEME_RE` = `re.compile(r"^(http|https|file):", re.I)`
- `COMMENT_RE` = `re.compile(r"(^|\s+)#.*$")`
- `ENV_VAR_RE` = `re.compile(r"(?P<var>\$\{(?P<name>[A-Z0-9_]+)\})")`
- `SUPPORTED_OPTIONS_REQ_DEST` = `[str(o().dest) for o in SUPPORTED_OPTIONS_REQ]`
- `SUPPORTED_OPTIONS_EDITABLE_REQ_DEST` = `[`
- `PEP263_ENCODING_RE` = `re.compile(rb"coding[:=]\s*([-\w.]+)")`
- `DEFAULT_ENCODING` = `"utf-8"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_install.py`

#### Classes
- `InstallRequirement`

#### Functions
- `__init__(
        self,
        req: Requirement | None,
        comes_from: str | InstallRequirement | None,
        editable: bool = False,
        link: Link | None = None,
        markers: Marker | None = None,
        isolated: bool = False,
        *,
        hash_options: dict[str, list[str]] | None = None,
        config_settings: dict[str, str | list[str]] | None = None,
        constraint: bool = False,
        extras: Collection[str] = ()`
- `__str__(self)`
- `__repr__(self)`
- `format_debug(self)`
- `name(self)`
- `supports_pyproject_editable(self)`
- `specifier(self)`
- `is_direct(self)`
- `is_pinned(self)`
- `match_markers(self, extras_requested: Iterable[str] | None = None)`
- `has_hash_options(self)`
- `hashes(self, trust_internet: bool = True)`
- `from_path(self)`
- `ensure_build_location(
        self, build_dir: str, autodelete: bool, parallel_builds: bool
    )`
- `_set_requirement(self)`
- `warn_on_mismatching_name(self)`
- `check_if_exists(self, use_user_site: bool)`
- `is_wheel(self)`
- `is_wheel_from_cache(self)`
- `unpacked_source_directory(self)`
- `setup_py_path(self)`
- `pyproject_toml_path(self)`
- `load_pyproject_toml(self)`
- `editable_sanity_check(self)`
- `prepare_metadata(self)`
- `metadata(self)`
- `set_dist(self, distribution: BaseDistribution)`
- `get_dist(self)`
- `assert_source_matches_version(self)`
- `ensure_has_source_dir(
        self,
        parent_dir: str,
        autodelete: bool = False,
        parallel_builds: bool = False,
    )`
- `needs_unpacked_archive(self, archive_source: Path)`
- `ensure_pristine_source_checkout(self)`
- `update_editable(self)`
- `uninstall(
        self, auto_confirm: bool = False, verbose: bool = False
    )`
- `_get_archive_name(self, path: str, parentdir: str, rootdir: str)`
- `_clean_zip_name(name: str, prefix: str)`
- `archive(self, build_dir: str | None)`
- `install(
        self,
        root: str | None = None,
        home: str | None = None,
        prefix: str | None = None,
        warn_script_location: bool = True,
        use_user_site: bool = False,
        pycompile: bool = True,
    )`
- `check_invalid_constraint_type(req: InstallRequirement)`
- `_has_option(options: Values, reqs: list[InstallRequirement], option: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_set.py`

#### Classes
- `RequirementSet`

#### Functions
- `__init__(self, check_supported_wheels: bool = True)`
- `__str__(self)`
- `__repr__(self)`
- `add_unnamed_requirement(self, install_req: InstallRequirement)`
- `add_named_requirement(self, install_req: InstallRequirement)`
- `has_requirement(self, name: str)`
- `get_requirement(self, name: str)`
- `all_requirements(self)`
- `requirements_to_install(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/req/req_uninstall.py`

#### Classes
- `StashedUninstallPathSet`
- `UninstallPathSet`
- `UninstallPthEntries`

#### Functions
- `_script_names(
    bin_dir: str, script_name: str, is_gui: bool
)`
- `_unique(
    fn: Callable[..., Generator[Any, None, None]],
)`
- `unique(*args: Any, **kw: Any)`
- `uninstallation_paths(dist: BaseDistribution)`
- `compact(paths: Iterable[str])`
- `compress_for_rename(paths: Iterable[str])`
- `norm_join(*a: str)`
- `compress_for_output_listing(paths: Iterable[str])`
- `__init__(self)`
- `_get_directory_stash(self, path: str)`
- `_get_file_stash(self, path: str)`
- `stash(self, path: str)`
- `commit(self)`
- `rollback(self)`
- `can_rollback(self)`
- `__init__(self, dist: BaseDistribution)`
- `_permitted(self, path: str)`
- `add(self, path: str)`
- `add_pth(self, pth_file: str, entry: str)`
- `remove(self, auto_confirm: bool = False, verbose: bool = False)`
- `_allowed_to_proceed(self, verbose: bool)`
- `_display(msg: str, paths: Iterable[str])`
- `rollback(self)`
- `commit(self)`
- `from_dist(cls, dist: BaseDistribution)`
- `iter_scripts_to_remove(
            dist: BaseDistribution,
            bin_dir: str,
        )`
- `__init__(self, pth_file: str)`
- `add(self, entry: str)`
- `remove(self)`
- `rollback(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/base.py`

#### Classes
- `BaseResolver`

#### Functions
- `resolve(
        self, root_reqs: list[InstallRequirement], check_supported_wheels: bool
    )`
- `get_installation_order(
        self, req_set: RequirementSet
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/legacy/resolver.py`

#### Classes
- `Resolver`

#### Functions
- `_check_dist_requires_python(
    dist: BaseDistribution,
    version_info: tuple[int, int, int],
    ignore_requires_python: bool = False,
)`
- `__init__(
        self,
        preparer: RequirementPreparer,
        finder: PackageFinder,
        wheel_cache: WheelCache | None,
        make_install_req: InstallRequirementProvider,
        use_user_site: bool,
        ignore_dependencies: bool,
        ignore_installed: bool,
        ignore_requires_python: bool,
        force_reinstall: bool,
        upgrade_strategy: str,
        py_version_info: tuple[int, ...] | None = None,
    )`
- `resolve(
        self, root_reqs: list[InstallRequirement], check_supported_wheels: bool
    )`
- `_add_requirement_to_set(
        self,
        requirement_set: RequirementSet,
        install_req: InstallRequirement,
        parent_req_name: str | None = None,
        extras_requested: Iterable[str] | None = None,
    )`
- `_is_upgrade_allowed(self, req: InstallRequirement)`
- `_set_req_to_reinstall(self, req: InstallRequirement)`
- `_check_skip_installed(self, req_to_install: InstallRequirement)`
- `_find_requirement_link(self, req: InstallRequirement)`
- `_populate_link(self, req: InstallRequirement)`
- `_get_dist_for(self, req: InstallRequirement)`
- `_resolve_one(
        self,
        requirement_set: RequirementSet,
        req_to_install: InstallRequirement,
    )`
- `add_req(subreq: Requirement, extras_requested: Iterable[str])`
- `get_installation_order(
        self, req_set: RequirementSet
    )`
- `schedule(req: InstallRequirement)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/base.py`

#### Classes
- `Constraint`
- `Requirement`
- `Candidate`

#### Functions
- `format_name(project: NormalizedName, extras: frozenset[NormalizedName])`
- `empty(cls)`
- `from_ireq(cls, ireq: InstallRequirement)`
- `__bool__(self)`
- `__and__(self, other: InstallRequirement)`
- `is_satisfied_by(self, candidate: Candidate)`
- `format_for_error(self)`
- `project_name(self)`
- `name(self)`
- `is_satisfied_by(self, candidate: Candidate)`
- `get_candidate_lookup(self)`
- `format_for_error(self)`
- `_match_link(link: Link, candidate: Candidate)`
- `project_name(self)`
- `name(self)`
- `version(self)`
- `is_installed(self)`
- `is_editable(self)`
- `source_link(self)`
- `iter_dependencies(self, with_requires: bool)`
- `get_install_requirement(self)`
- `format_for_error(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/candidates.py`

#### Classes
- `_InstallRequirementBackedCandidate`
- `exposes`
- `LinkCandidate`
- `EditableCandidate`
- `AlreadyInstalledCandidate`
- `ExtrasCandidate`
- `RequiresPythonCandidate`

#### Functions
- `as_base_candidate(candidate: Candidate)`
- `make_install_req_from_link(
    link: Link,
    template: InstallRequirement,
    version: Version | None = None,
)`
- `make_install_req_from_editable(
    link: Link, template: InstallRequirement
)`
- `_make_install_req_from_dist(
    dist: BaseDistribution, template: InstallRequirement
)`
- `__init__(
        self,
        link: Link,
        source_link: Link,
        ireq: InstallRequirement,
        factory: Factory,
        name: NormalizedName | None = None,
        version: Version | None = None,
    )`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: Any)`
- `source_link(self)`
- `project_name(self)`
- `name(self)`
- `version(self)`
- `format_for_error(self)`
- `_prepare_distribution(self)`
- `_check_metadata_consistency(self, dist: BaseDistribution)`
- `_prepare(self)`
- `iter_dependencies(self, with_requires: bool)`
- `get_install_requirement(self)`
- `__init__(
        self,
        link: Link,
        template: InstallRequirement,
        factory: Factory,
        name: NormalizedName | None = None,
        version: Version | None = None,
    )`
- `_prepare_distribution(self)`
- `__init__(
        self,
        link: Link,
        template: InstallRequirement,
        factory: Factory,
        name: NormalizedName | None = None,
        version: Version | None = None,
    )`
- `_prepare_distribution(self)`
- `__init__(
        self,
        dist: BaseDistribution,
        template: InstallRequirement,
        factory: Factory,
    )`
- `__str__(self)`
- `__repr__(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `project_name(self)`
- `name(self)`
- `version(self)`
- `is_editable(self)`
- `format_for_error(self)`
- `iter_dependencies(self, with_requires: bool)`
- `get_install_requirement(self)`
- `__init__(
        self,
        base: BaseCandidate,
        extras: frozenset[str],
        *,
        comes_from: InstallRequirement | None = None,
    )`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: Any)`
- `project_name(self)`
- `name(self)`
- `version(self)`
- `format_for_error(self)`
- `is_installed(self)`
- `is_editable(self)`
- `source_link(self)`
- `iter_dependencies(self, with_requires: bool)`
- `get_install_requirement(self)`
- `__init__(self, py_version_info: tuple[int, ...] | None)`
- `__str__(self)`
- `__repr__(self)`
- `project_name(self)`
- `name(self)`
- `version(self)`
- `format_for_error(self)`
- `iter_dependencies(self, with_requires: bool)`
- `get_install_requirement(self)`

#### Parameters / Constants
- `REQUIRES_PYTHON_IDENTIFIER` = `cast(NormalizedName, "<Python from Requires-Python>")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/factory.py`

#### Classes
- `ConflictCause`
- `CollectedRootRequirements`
- `Factory`

#### Functions
- `__init__(
        self,
        finder: PackageFinder,
        preparer: RequirementPreparer,
        make_install_req: InstallRequirementProvider,
        wheel_cache: WheelCache | None,
        use_user_site: bool,
        force_reinstall: bool,
        ignore_installed: bool,
        ignore_requires_python: bool,
        py_version_info: tuple[int, ...] | None = None,
    )`
- `force_reinstall(self)`
- `_fail_if_link_is_unsupported_wheel(self, link: Link)`
- `_make_extras_candidate(
        self,
        base: BaseCandidate,
        extras: frozenset[str],
        *,
        comes_from: InstallRequirement | None = None,
    )`
- `_make_candidate_from_dist(
        self,
        dist: BaseDistribution,
        extras: frozenset[str],
        template: InstallRequirement,
    )`
- `_make_candidate_from_link(
        self,
        link: Link,
        extras: frozenset[str],
        template: InstallRequirement,
        name: NormalizedName | None,
        version: Version | None,
    )`
- `_make_base_candidate_from_link(
        self,
        link: Link,
        template: InstallRequirement,
        name: NormalizedName | None,
        version: Version | None,
    )`
- `_get_locked_installation_candidate(
        self, ireqs: Sequence[InstallRequirement], name: str, specifier: SpecifierSet
    )`
- `_iter_found_candidates(
        self,
        ireqs: Sequence[InstallRequirement],
        specifier: SpecifierSet,
        hashes: Hashes,
        prefers_installed: bool,
        incompatible_ids: set[int],
        constraint_hash_options: dict[str, list[str]] | None = None,
    )`
- `_get_installed_candidate()`
- `iter_index_candidate_infos()`
- `is_pinned(specifier: SpecifierSet)`
- `_iter_explicit_candidates_from_base(
        self,
        base_requirements: Iterable[Requirement],
        extras: frozenset[str],
    )`
- `_iter_candidates_from_constraints(
        self,
        identifier: str,
        constraint: Constraint,
        template: InstallRequirement,
    )`
- `find_candidates(
        self,
        identifier: str,
        requirements: Mapping[str, Iterable[Requirement]],
        incompatibilities: Mapping[str, Iterator[Candidate]],
        constraint: Constraint,
        prefers_installed: bool,
        is_satisfied_by: Callable[[Requirement, Candidate], bool],
    )`
- `_make_requirements_from_install_req(
        self, ireq: InstallRequirement, requested_extras: Iterable[str]
    )`
- `collect_root_requirements(
        self, root_ireqs: list[InstallRequirement]
    )`
- `make_requirement_from_candidate(
        self, candidate: Candidate
    )`
- `make_requirements_from_spec(
        self,
        specifier: str,
        comes_from: InstallRequirement | None,
        requested_extras: Iterable[str] = ()`
- `make_requires_python_requirement(
        self,
        specifier: SpecifierSet,
    )`
- `get_wheel_cache_entry(self, link: Link, name: str | None)`
- `get_dist_to_uninstall(self, candidate: Candidate)`
- `_report_requires_python_error(
        self, causes: Sequence[ConflictCause]
    )`
- `_report_single_requirement_conflict(
        self, req: Requirement, parent: Candidate | None
    )`
- `_has_any_candidates(self, project_name: str)`
- `get_installation_error(
        self,
        e: ResolutionImpossible[Requirement, Candidate],
        constraints: dict[str, Constraint],
    )`
- `text_join(parts: list[str])`
- `describe_trigger(parent: Candidate)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py`

#### Classes
- `FoundCandidates`

#### Functions
- `_iter_built(infos: Iterator[IndexCandidateInfo])`
- `_iter_built_with_prepended(
    installed: Candidate, infos: Iterator[IndexCandidateInfo]
)`
- `_iter_built_with_inserted(
    installed: Candidate, infos: Iterator[IndexCandidateInfo]
)`
- `__init__(
        self,
        get_infos: Callable[[], Iterator[IndexCandidateInfo]],
        installed: Candidate | None,
        prefers_installed: bool,
        incompatible_ids: set[int],
    )`
- `__getitem__(self, index: Any)`
- `__iter__(self)`
- `__len__(self)`
- `__bool__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/provider.py`

#### Classes
- `PipProvider`

#### Functions
- `_get_with_identifier(
    mapping: Mapping[str, V],
    identifier: str,
    default: D,
)`
- `__init__(
        self,
        factory: Factory,
        constraints: dict[str, Constraint],
        ignore_dependencies: bool,
        upgrade_strategy: str,
        user_requested: dict[str, int],
    )`
- `constraints(self)`
- `identify(self, requirement_or_candidate: Requirement | Candidate)`
- `narrow_requirement_selection(
        self,
        identifiers: Iterable[str],
        resolutions: Mapping[str, Candidate],
        candidates: Mapping[str, Iterator[Candidate]],
        information: Mapping[str, Iterator[PreferenceInformation]],
        backtrack_causes: Sequence[PreferenceInformation],
    )`
- `get_preference(
        self,
        identifier: str,
        resolutions: Mapping[str, Candidate],
        candidates: Mapping[str, Iterator[Candidate]],
        information: Mapping[str, Iterable[PreferenceInformation]],
        backtrack_causes: Sequence[PreferenceInformation],
    )`
- `find_matches(
        self,
        identifier: str,
        requirements: Mapping[str, Iterator[Requirement]],
        incompatibilities: Mapping[str, Iterator[Candidate]],
    )`
- `_eligible_for_upgrade(identifier: str)`
- `is_satisfied_by(requirement: Requirement, candidate: Candidate)`
- `get_dependencies(self, candidate: Candidate)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/reporter.py`

#### Classes
- `PipReporter`
- `PipDebuggingReporter`

#### Functions
- `__init__(self, constraints: Mapping[str, Constraint] | None = None)`
- `rejecting_candidate(self, criterion: Any, candidate: Candidate)`
- `starting(self)`
- `starting_round(self, index: int)`
- `ending_round(self, index: int, state: Any)`
- `ending(self, state: Any)`
- `adding_requirement(
        self, requirement: Requirement, parent: Candidate | None
    )`
- `rejecting_candidate(self, criterion: Any, candidate: Candidate)`
- `pinning(self, candidate: Candidate)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/requirements.py`

#### Classes
- `ExplicitRequirement`
- `SpecifierRequirement`
- `SpecifierWithoutExtrasRequirement`
- `RequiresPythonRequirement`
- `UnsatisfiableRequirement`

#### Functions
- `__init__(self, candidate: Candidate)`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: Any)`
- `project_name(self)`
- `name(self)`
- `format_for_error(self)`
- `get_candidate_lookup(self)`
- `is_satisfied_by(self, candidate: Candidate)`
- `__init__(self, ireq: InstallRequirement)`
- `_equal(self)`
- `__str__(self)`
- `__repr__(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `project_name(self)`
- `name(self)`
- `format_for_error(self)`
- `get_candidate_lookup(self)`
- `is_satisfied_by(self, candidate: Candidate)`
- `__init__(self, ireq: InstallRequirement)`
- `_equal(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `__init__(self, specifier: SpecifierSet, match: Candidate)`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: Any)`
- `project_name(self)`
- `name(self)`
- `format_for_error(self)`
- `get_candidate_lookup(self)`
- `is_satisfied_by(self, candidate: Candidate)`
- `__init__(self, name: NormalizedName)`
- `__str__(self)`
- `__repr__(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `project_name(self)`
- `name(self)`
- `format_for_error(self)`
- `get_candidate_lookup(self)`
- `is_satisfied_by(self, candidate: Candidate)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/resolution/resolvelib/resolver.py`

#### Classes
- `Resolver`

#### Functions
- `__init__(
        self,
        preparer: RequirementPreparer,
        finder: PackageFinder,
        wheel_cache: WheelCache | None,
        make_install_req: InstallRequirementProvider,
        use_user_site: bool,
        ignore_dependencies: bool,
        ignore_installed: bool,
        ignore_requires_python: bool,
        force_reinstall: bool,
        upgrade_strategy: str,
        py_version_info: tuple[int, ...] | None = None,
    )`
- `resolve(
        self, root_reqs: list[InstallRequirement], check_supported_wheels: bool
    )`
- `get_installation_order(
        self, req_set: RequirementSet
    )`
- `get_topological_weights(
    graph: DirectedGraph[str | None], requirement_keys: set[str]
)`
- `visit(node: str | None)`
- `_req_set_item_sorter(
    item: tuple[str, InstallRequirement],
    weights: dict[str | None, int],
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/self_outdated_check.py`

#### Classes
- `SelfCheckState`
- `UpgradePrompt`

#### Functions
- `_get_statefile_name(key: str)`
- `__init__(self, cache_dir: str)`
- `key(self)`
- `get(self, current_time: datetime.datetime)`
- `set(self, pypi_version: str, current_time: datetime.datetime)`
- `__rich__(self)`
- `_get_current_remote_pip_version(
    session: PipSession, options: optparse.Values
)`
- `_compute_upgrade_prompt(
    local_version: Version, remote_version_str: str, installed_by_pip: bool
)`
- `pip_self_version_check_fetch(
    session: PipSession, options: optparse.Values
)`
- `pip_self_version_check_emit(upgrade_prompt: UpgradePrompt | None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/_jaraco_text.py`

#### Functions
- `_nonblank(str)`
- `yield_lines(iterable)`
- `_(text)`
- `drop_comment(line)`
- `join_continuation(lines)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/_log.py`

#### Classes
- `VerboseLogger`

#### Functions
- `verbose(self, msg: str, *args: Any, **kwargs: Any)`
- `getLogger(name: str)`
- `init_logging()`

#### Parameters / Constants
- `VERBOSE` = `15`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/appdirs.py`

#### Functions
- `user_cache_dir(appname: str)`
- `_macos_user_config_dir(appname: str, roaming: bool = True)`
- `user_config_dir(appname: str, roaming: bool = True)`
- `site_config_dirs(appname: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/compat.py`

#### Functions
- `has_tls()`
- `get_path_uid(path: str)`
- `open_text_resource(
        package: str, resource: str, encoding: str = "utf-8", errors: str = "strict"
    )`

#### Parameters / Constants
- `WINDOWS` = `sys.platform.startswith("win") or (sys.platform == "cli" and os.name == "nt")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/compatibility_tags.py`

#### Functions
- `version_info_to_nodot(version_info: tuple[int, ...])`
- `_mac_platforms(arch: str)`
- `_ios_platforms(arch: str)`
- `_android_platforms(arch: str)`
- `_custom_manylinux_platforms(arch: str)`
- `_get_custom_platforms(arch: str)`
- `_expand_allowed_platforms(platforms: list[str] | None)`
- `_get_python_version(version: str)`
- `_get_custom_interpreter(
    implementation: str | None = None, version: str | None = None
)`
- `get_supported(
    version: str | None = None,
    platforms: list[str] | None = None,
    impl: str | None = None,
    abis: list[str] | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/datetime.py`

#### Functions
- `today_is_later_than(year: int, month: int, day: int)`
- `parse_iso_datetime(isodate: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/deprecation.py`

#### Classes
- `PipDeprecationWarning`

#### Functions
- `_showwarning(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    file: TextIO | None = None,
    line: str | None = None,
)`
- `install_warning_logger()`
- `deprecated(
    *,
    reason: str,
    replacement: str | None,
    gone_in: str | None,
    feature_flag: str | None = None,
    issue: int | None = None,
    stacklevel: int = 2,
    include_source: bool = False,
)`

#### Parameters / Constants
- `DEPRECATION_MSG_PREFIX` = `"DEPRECATION: "`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/direct_url_helpers.py`

#### Functions
- `direct_url_as_pep440_direct_reference(direct_url: DirectUrl, name: str)`
- `direct_url_for_editable(source_dir: str)`
- `direct_url_from_link(
    link: Link, source_dir: str | None = None, link_is_in_wheel_cache: bool = False
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/egg_link.py`

#### Functions
- `_egg_link_names(raw_name: str)`
- `egg_link_path_from_sys_path(raw_name: str)`
- `egg_link_path_from_location(raw_name: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/entrypoints.py`

#### Functions
- `_wrapper(args: list[str] | None = None)`
- `get_best_invocation_for_this_pip()`
- `get_best_invocation_for_this_python()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/filesystem.py`

#### Functions
- `check_path_owner(path: str)`
- `adjacent_tmp_file(path: str, **kwargs: Any)`
- `test_writable_dir(path: str)`
- `_test_writable_dir_win(path: str)`
- `find_files(path: str, pattern: str)`
- `file_size(path: str)`
- `format_file_size(path: str)`
- `directory_size(path: str)`
- `format_directory_size(path: str)`
- `copy_directory_permissions(directory: str, target_file: BinaryIO)`
- `_subdirs_without_generic(
    path: str, predicate: Callable[[str, list[str]], bool]
)`
- `subdirs_without_files(path: str)`
- `subdirs_without_wheels(path: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/filetypes.py`

#### Functions
- `is_archive_file(name: str)`

#### Parameters / Constants
- `WHEEL_EXTENSION` = `".whl"`
- `ARCHIVE_EXTENSIONS` = `ZIP_EXTENSIONS + BZ2_EXTENSIONS + TAR_EXTENSIONS + XZ_EXTENSIONS`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/glibc.py`

#### Functions
- `glibc_version_string()`
- `glibc_version_string_confstr()`
- `glibc_version_string_ctypes()`
- `libc_ver()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/hashes.py`

#### Classes
- `Hashes`
- `MissingHashes`

#### Functions
- `__init__(self, hashes: dict[str, list[str]] | None = None)`
- `__and__(self, other: Hashes)`
- `digest_count(self)`
- `is_hash_allowed(self, hash_name: str, hex_digest: str)`
- `check_against_chunks(self, chunks: Iterable[bytes])`
- `_raise(self, gots: dict[str, _Hash])`
- `check_against_file(self, file: BinaryIO)`
- `check_against_path(self, path: str)`
- `has_one_of(self, hashes: Mapping[str, str])`
- `__bool__(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `__init__(self)`
- `_raise(self, gots: dict[str, _Hash])`

#### Parameters / Constants
- `FAVORITE_HASH` = `"sha256"`
- `STRONG_HASHES` = `["sha256", "sha384", "sha512"]`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/logging.py`

#### Classes
- `BrokenStdoutLoggingError`
- `IndentingFormatter`
- `IndentedRenderable`
- `PipConsole`
- `RichPipStreamHandler`
- `BetterRotatingFileHandler`
- `MaxLevelFilter`
- `ExcludeLoggerFilter`

#### Functions
- `_is_broken_pipe_error(exc_class: type[BaseException], exc: BaseException)`
- `capture_logging()`
- `indent_log(num: int = 2)`
- `get_indentation()`
- `__init__(
        self,
        *args: Any,
        add_timestamp: bool = False,
        **kwargs: Any,
    )`
- `get_message_start(self, formatted: str, levelno: int)`
- `format(self, record: logging.LogRecord)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `on_broken_pipe(self)`
- `get_console(*, stderr: bool = False)`
- `__init__(self, console: Console)`
- `emit(self, record: logging.LogRecord)`
- `handleError(self, record: logging.LogRecord)`
- `_open(self)`
- `__init__(self, level: int)`
- `filter(self, record: logging.LogRecord)`
- `filter(self, record: logging.LogRecord)`
- `setup_logging(verbosity: int, no_color: bool, user_log_file: str | None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/misc.py`

#### Classes
- `StreamWrapper`
- `HiddenText`
- `ConfiguredBuildBackendHookCaller`

#### Functions
- `get_pip_version()`
- `normalize_version_info(py_version_info: tuple[int, ...])`
- `ensure_dir(path: str)`
- `get_prog()`
- `rmtree(dir: str, ignore_errors: bool = False, onexc: OnExc | None = None)`
- `_onerror_ignore(*_args: Any)`
- `_onerror_reraise(*_args: Any)`
- `rmtree_errorhandler(
    func: FunctionType,
    path: Path,
    exc_info: ExcInfo | BaseException,
    *,
    onexc: OnExc = _onerror_reraise,
)`
- `display_path(path: str)`
- `backup_dir(dir: str, ext: str = ".bak")`
- `ask_path_exists(message: str, options: Iterable[str])`
- `_check_no_input(message: str)`
- `ask(message: str, options: Iterable[str])`
- `ask_input(message: str)`
- `ask_password(message: str)`
- `strtobool(val: str)`
- `format_size(bytes: float)`
- `tabulate(rows: Iterable[Iterable[Any]])`
- `is_installable_dir(path: str)`
- `read_chunks(
    file: BinaryIO, size: int = FILE_CHUNK_SIZE
)`
- `normalize_path(path: str, resolve_symlinks: bool = True)`
- `splitext(path: str)`
- `renames(old: str, new: str)`
- `is_local(path: str)`
- `write_output(msg: Any, *args: Any)`
- `from_stream(cls, orig_stream: TextIO)`
- `encoding(self)`
- `enum(*sequential: Any, **named: Any)`
- `build_netloc(host: str, port: int | None)`
- `build_url_from_netloc(netloc: str, scheme: str = "https")`
- `parse_netloc(netloc: str)`
- `split_auth_from_netloc(netloc: str)`
- `redact_netloc(netloc: str)`
- `_transform_url(
    url: str, transform_netloc: Callable[[str], tuple[Any, ...]]
)`
- `_get_netloc(netloc: str)`
- `_redact_netloc(netloc: str)`
- `split_auth_netloc_from_url(
    url: str,
)`
- `remove_auth_from_url(url: str)`
- `redact_auth_from_url(url: str)`
- `redact_auth_from_requirement(req: Requirement)`
- `__repr__(self)`
- `__str__(self)`
- `__eq__(self, other: object)`
- `hide_value(value: str)`
- `hide_url(url: str)`
- `protect_pip_from_modification_on_windows(modifying_pip: bool)`
- `check_externally_managed()`
- `is_console_interactive()`
- `hash_file(path: str, blocksize: int = 1 << 20)`
- `pairwise(iterable: Iterable[Any])`
- `partition(
    pred: Callable[[T], bool], iterable: Iterable[T]
)`
- `__init__(
        self,
        config_holder: Any,
        source_dir: str,
        build_backend: str,
        backend_path: str | None = None,
        runner: Callable[..., None] | None = None,
        python_executable: str | None = None,
    )`
- `build_wheel(
        self,
        wheel_directory: str,
        config_settings: Mapping[str, Any] | None = None,
        metadata_directory: str | None = None,
    )`
- `build_sdist(
        self,
        sdist_directory: str,
        config_settings: Mapping[str, Any] | None = None,
    )`
- `build_editable(
        self,
        wheel_directory: str,
        config_settings: Mapping[str, Any] | None = None,
        metadata_directory: str | None = None,
    )`
- `get_requires_for_build_wheel(
        self, config_settings: Mapping[str, Any] | None = None
    )`
- `get_requires_for_build_sdist(
        self, config_settings: Mapping[str, Any] | None = None
    )`
- `get_requires_for_build_editable(
        self, config_settings: Mapping[str, Any] | None = None
    )`
- `prepare_metadata_for_build_wheel(
        self,
        metadata_directory: str,
        config_settings: Mapping[str, Any] | None = None,
        _allow_fallback: bool = True,
    )`
- `prepare_metadata_for_build_editable(
        self,
        metadata_directory: str,
        config_settings: Mapping[str, Any] | None = None,
        _allow_fallback: bool = True,
    )`
- `warn_if_run_as_root()`

#### Parameters / Constants
- `FILE_CHUNK_SIZE` = `1024 * 1024`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/packaging.py`

#### Functions
- `check_requires_python(
    requires_python: str | None, version_info: tuple[int, ...]
)`
- `get_requirement(req_string: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/pylock.py`

#### Functions
- `_pylock_package_from_install_requirement(
    ireq: InstallRequirement, base_dir: Path
)`
- `pylock_from_install_requirements(
    install_requirements: Iterable[InstallRequirement], base_dir: Path
)`
- `_is_url(s: str)`
- `is_valid_pylock_filename(filename: str)`
- `_package_dist_url(
    pylock_path_or_url: str, path: str | None, url: str | None
)`
- `package_vcs_requirement_url(
    pylock_path_or_url: str, package_vcs: PackageVcs
)`
- `package_archive_requirement_url(
    pylock_path_or_url: str, package_archive: PackageArchive
)`
- `package_directory_requirement_url(
    pylock_path_or_url: str, package_directory: PackageDirectory
)`
- `package_sdist_requirement_url(
    pylock_path_or_url: str, package_sdist: PackageSdist
)`
- `package_wheel_requirement_url(
    pylock_path_or_url: str, package_wheel: PackageWheel
)`
- `_get_pylock_path_or_url_content(path_or_url: str, session: PipSession)`
- `select_from_pylock_path_or_url(
    pylock_path_or_url: str,
    session: PipSession,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/retry.py`

#### Functions
- `retry(
    wait: float, stop_after_delay: float
)`
- `wrapper(func: Callable[P, T])`
- `retry_wrapped(*args: P.args, **kwargs: P.kwargs)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/subprocess.py`

#### Functions
- `make_command(*args: str | HiddenText | CommandArgs)`
- `format_command_args(args: list[str] | CommandArgs)`
- `reveal_command_args(args: list[str] | CommandArgs)`
- `call_subprocess(
    cmd: list[str] | CommandArgs,
    show_stdout: bool = False,
    cwd: str | None = None,
    on_returncode: Literal["raise", "warn", "ignore"] = "raise",
    extra_ok_returncodes: Iterable[int] | None = None,
    extra_environ: Mapping[str, Any] | None = None,
    unset_environ: Iterable[str] | None = None,
    spinner: SpinnerInterface | None = None,
    log_failed_cmd: bool | None = True,
    stdout_only: bool | None = False,
    *,
    command_desc: str,
)`
- `runner_with_spinner_message(message: str)`
- `runner(
        cmd: list[str],
        cwd: str | None = None,
        extra_environ: Mapping[str, Any] | None = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/temp_dir.py`

#### Classes
- `TempDirectoryTypeRegistry`
- `_Default`
- `TempDirectory`
- `AdjacentTempDirectory`

#### Functions
- `global_tempdir_manager()`
- `__init__(self)`
- `set_delete(self, kind: str, value: bool)`
- `get_delete(self, kind: str)`
- `tempdir_registry()`
- `__init__(
        self,
        path: str | None = None,
        delete: bool | None | _Default = _default,
        kind: str = "temp",
        globally_managed: bool = False,
        ignore_cleanup_errors: bool = True,
    )`
- `path(self)`
- `__repr__(self)`
- `__enter__(self: _T)`
- `__exit__(self, exc: Any, value: Any, tb: Any)`
- `_create(self, kind: str)`
- `cleanup(self)`
- `onerror(
            func: Callable[..., Any],
            path: Path,
            exc_val: BaseException,
        )`
- `__init__(self, original: str, delete: bool | None = None)`
- `_generate_names(cls, name: str)`
- `_create(self, kind: str)`

#### Parameters / Constants
- `BUILD_ENV` = `"build-env",`
- `EPHEM_WHEEL_CACHE` = `"ephem-wheel-cache",`
- `REQ_BUILD` = `"req-build",`
- `LEADING_CHARS` = `"-~.=%0123456789"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/unpacking.py`

#### Functions
- `current_umask()`
- `split_leading_dir(path: str)`
- `has_leading_dir(paths: Iterable[str])`
- `is_within_directory(directory: str, target: str)`
- `_get_default_mode_plus_executable()`
- `set_extracted_file_to_default_mode_plus_executable(path: str)`
- `zip_item_is_executable(info: ZipInfo)`
- `unzip_file(filename: str, location: str, flatten: bool = True)`
- `untar_file(filename: str, location: str)`
- `pip_filter(member: tarfile.TarInfo, path: str)`
- `is_symlink_target_in_tar(tar: tarfile.TarFile, tarinfo: tarfile.TarInfo)`
- `_untar_without_filter(
    filename: str,
    location: str,
    tar: tarfile.TarFile,
    leading: bool,
)`
- `unpack_file(
    filename: str,
    location: str,
    content_type: str | None = None,
)`
- `_unzip()`
- `_untar()`

#### Parameters / Constants
- `SUPPORTED_EXTENSIONS` = `ZIP_EXTENSIONS + TAR_EXTENSIONS`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/urls.py`

#### Functions
- `path_to_url(path: str)`
- `url_to_path(url: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/virtualenv.py`

#### Functions
- `_running_under_venv()`
- `_running_under_legacy_virtualenv()`
- `running_under_virtualenv()`
- `_get_pyvenv_cfg_lines()`
- `_no_global_under_venv()`
- `_no_global_under_legacy_virtualenv()`
- `virtualenv_no_global()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/utils/wheel.py`

#### Functions
- `parse_wheel(wheel_zip: ZipFile, name: str)`
- `wheel_dist_info_dir(source: ZipFile, name: str)`
- `read_wheel_metadata_file(source: ZipFile, path: str)`
- `wheel_metadata(source: ZipFile, dist_info_dir: str)`
- `wheel_version(wheel_data: Message)`
- `check_compatibility(version: tuple[int, ...], name: str)`

#### Parameters / Constants
- `VERSION_COMPATIBLE` = `(1, 0)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/bazaar.py`

#### Classes
- `Bazaar`

#### Functions
- `get_base_rev_args(rev: str)`
- `fetch_new(
        self, dest: str, url: HiddenText, rev_options: RevOptions, verbosity: int
    )`
- `switch(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `update(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `get_url_rev_and_auth(cls, url: str)`
- `get_remote_url(cls, location: str)`
- `get_revision(cls, location: str)`
- `is_commit_id_equal(cls, dest: str, name: str | None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/git.py`

#### Classes
- `Git`

#### Functions
- `looks_like_hash(sha: str)`
- `get_base_rev_args(rev: str)`
- `run_command(cls, *args: Any, **kwargs: Any)`
- `is_immutable_rev_checkout(self, url: str, dest: str)`
- `get_git_version(self)`
- `get_current_branch(cls, location: str)`
- `get_revision_sha(cls, dest: str, rev: str)`
- `_should_fetch(cls, dest: str, rev: str)`
- `resolve_revision(
        cls, dest: str, url: HiddenText, rev_options: RevOptions
    )`
- `is_commit_id_equal(cls, dest: str, name: str | None)`
- `fetch_new(
        self, dest: str, url: HiddenText, rev_options: RevOptions, verbosity: int
    )`
- `switch(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `update(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `get_remote_url(cls, location: str)`
- `_git_remote_to_pip_url(url: str)`
- `has_commit(cls, location: str, rev: str)`
- `get_revision(cls, location: str, rev: str | None = None)`
- `get_subdirectory(cls, location: str)`
- `get_url_rev_and_auth(cls, url: str)`
- `update_submodules(cls, location: str, verbosity: int = 0)`
- `get_repository_root(cls, location: str)`
- `should_add_vcs_url_prefix(repo_url: str)`

#### Parameters / Constants
- `GIT_VERSION_REGEX` = `re.compile(`
- `HASH_REGEX` = `re.compile("^[a-fA-F0-9]{40}$")`
- `SCP_REGEX` = `re.compile(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/mercurial.py`

#### Classes
- `Mercurial`

#### Functions
- `get_base_rev_args(rev: str)`
- `fetch_new(
        self, dest: str, url: HiddenText, rev_options: RevOptions, verbosity: int
    )`
- `switch(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `update(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `get_remote_url(cls, location: str)`
- `get_revision(cls, location: str)`
- `get_requirement_revision(cls, location: str)`
- `is_commit_id_equal(cls, dest: str, name: str | None)`
- `get_subdirectory(cls, location: str)`
- `get_repository_root(cls, location: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/subversion.py`

#### Classes
- `Subversion`

#### Functions
- `should_add_vcs_url_prefix(cls, remote_url: str)`
- `get_base_rev_args(rev: str)`
- `get_revision(cls, location: str)`
- `get_netloc_and_auth(
        cls, netloc: str, scheme: str
    )`
- `get_url_rev_and_auth(cls, url: str)`
- `make_rev_args(username: str | None, password: HiddenText | None)`
- `get_remote_url(cls, location: str)`
- `_get_svn_url_rev(cls, location: str)`
- `is_commit_id_equal(cls, dest: str, name: str | None)`
- `__init__(self, use_interactive: bool | None = None)`
- `call_vcs_version(self)`
- `get_vcs_version(self)`
- `get_remote_call_options(self)`
- `fetch_new(
        self, dest: str, url: HiddenText, rev_options: RevOptions, verbosity: int
    )`
- `switch(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `update(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/vcs/versioncontrol.py`

#### Classes
- `RemoteNotFoundError`
- `RemoteNotValidError`
- `RevOptions`
- `VcsSupport`
- `VersionControl`

#### Functions
- `is_url(name: str)`
- `make_vcs_requirement_url(
    repo_url: str, rev: str, project_name: str, subdir: str | None = None
)`
- `find_path_to_project_root_from_repo_root(
    location: str, repo_root: str
)`
- `__init__(self, url: str)`
- `__repr__(self)`
- `arg_rev(self)`
- `to_args(self)`
- `to_display(self)`
- `make_new(self, rev: str)`
- `__init__(self)`
- `__iter__(self)`
- `backends(self)`
- `dirnames(self)`
- `all_schemes(self)`
- `register(self, cls: type[VersionControl])`
- `unregister(self, name: str)`
- `get_backend_for_dir(self, location: str)`
- `get_backend_for_scheme(self, scheme: str)`
- `get_backend(self, name: str)`
- `should_add_vcs_url_prefix(cls, remote_url: str)`
- `get_subdirectory(cls, location: str)`
- `get_requirement_revision(cls, repo_dir: str)`
- `get_src_requirement(cls, repo_dir: str, project_name: str)`
- `get_base_rev_args(rev: str)`
- `is_immutable_rev_checkout(self, url: str, dest: str)`
- `make_rev_options(
        cls, rev: str | None = None, extra_args: CommandArgs | None = None
    )`
- `_is_local_repository(cls, repo: str)`
- `get_netloc_and_auth(
        cls, netloc: str, scheme: str
    )`
- `get_url_rev_and_auth(cls, url: str)`
- `make_rev_args(username: str | None, password: HiddenText | None)`
- `get_url_rev_options(self, url: HiddenText)`
- `normalize_url(url: str)`
- `compare_urls(cls, url1: str, url2: str)`
- `fetch_new(
        self, dest: str, url: HiddenText, rev_options: RevOptions, verbosity: int
    )`
- `switch(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `update(
        self,
        dest: str,
        url: HiddenText,
        rev_options: RevOptions,
        verbosity: int = 0,
    )`
- `is_commit_id_equal(cls, dest: str, name: str | None)`
- `obtain(self, dest: str, url: HiddenText, verbosity: int)`
- `unpack(self, location: str, url: HiddenText, verbosity: int)`
- `get_remote_url(cls, location: str)`
- `get_revision(cls, location: str)`
- `run_command(
        cls,
        cmd: list[str] | CommandArgs,
        show_stdout: bool = True,
        cwd: str | None = None,
        on_returncode: Literal["raise", "warn", "ignore"] = "raise",
        extra_ok_returncodes: Iterable[int] | None = None,
        command_desc: str | None = None,
        extra_environ: Mapping[str, Any] | None = None,
        spinner: SpinnerInterface | None = None,
        log_failed_cmd: bool = True,
        stdout_only: bool = False,
    )`
- `is_repository_directory(cls, path: str)`
- `get_repository_root(cls, location: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_internal/wheel_builder.py`

#### Functions
- `_contains_egg_info(s: str)`
- `_should_cache(
    req: InstallRequirement,
)`
- `_get_cache_dir(
    req: InstallRequirement,
    wheel_cache: WheelCache,
)`
- `_verify_one(req: InstallRequirement, wheel_path: str)`
- `_build_one(
    req: InstallRequirement,
    output_dir: str,
    verify: bool,
    editable: bool,
)`
- `_build_one_inside_env(
    req: InstallRequirement,
    output_dir: str,
    editable: bool,
)`
- `build(
    requirements: Iterable[InstallRequirement],
    wheel_cache: WheelCache,
    verify: bool,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/__init__.py`

#### Functions
- `vendored(modulename)`

#### Parameters / Constants
- `DEBUNDLED` = `False`
- `WHEEL_DIR` = `os.path.abspath(os.path.dirname(__file__))`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/_cmd.py`

#### Functions
- `setup_logging()`
- `get_session()`
- `get_args()`
- `main()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/adapter.py`

#### Classes
- `CacheControlAdapter`

#### Functions
- `__init__(
        self,
        cache: BaseCache | None = None,
        cache_etags: bool = True,
        controller_class: type[CacheController] | None = None,
        serializer: Serializer | None = None,
        heuristic: BaseHeuristic | None = None,
        cacheable_methods: Collection[str] | None = None,
        *args: Any,
        **kw: Any,
    )`
- `send(
        self,
        request: PreparedRequest,
        stream: bool = False,
        timeout: None | float | tuple[float, float] | tuple[float, None] = None,
        verify: bool | str = True,
        cert: (None | bytes | str | tuple[bytes | str, bytes | str])`
- `build_response(  # type: ignore[override]
        self,
        request: PreparedRequest,
        response: HTTPResponse,
        from_cache: bool = False,
        cacheable_methods: Collection[str] | None = None,
    )`
- `_update_chunk_length(
                        weak_self: weakref.ReferenceType[HTTPResponse],
                    )`
- `close(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/cache.py`

#### Classes
- `BaseCache`
- `DictCache`
- `SeparateBodyBaseCache`

#### Functions
- `get(self, key: str)`
- `set(
        self, key: str, value: bytes, expires: int | datetime | None = None
    )`
- `delete(self, key: str)`
- `close(self)`
- `__init__(self, init_dict: MutableMapping[str, bytes] | None = None)`
- `get(self, key: str)`
- `set(
        self, key: str, value: bytes, expires: int | datetime | None = None
    )`
- `delete(self, key: str)`
- `set_body(self, key: str, body: bytes)`
- `get_body(self, key: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/caches/file_cache.py`

#### Classes
- `_FileCacheMixin`
- `FileCache`
- `SeparateBodyFileCache`

#### Functions
- `__init__(
        self,
        directory: str | Path,
        forever: bool = False,
        filemode: int = 0o0600,
        dirmode: int = 0o0700,
        lock_class: type[BaseFileLock] | None = None,
    )`
- `encode(x: str)`
- `_fn(self, name: str)`
- `get(self, key: str)`
- `set(
        self, key: str, value: bytes, expires: int | datetime | None = None
    )`
- `_write(self, path: str, data: bytes)`
- `_delete(self, key: str, suffix: str)`
- `delete(self, key: str)`
- `get_body(self, key: str)`
- `set_body(self, key: str, body: bytes)`
- `delete(self, key: str)`
- `url_to_file_path(url: str, filecache: FileCache)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/caches/redis_cache.py`

#### Classes
- `RedisCache`

#### Functions
- `__init__(self, conn: Redis[bytes])`
- `get(self, key: str)`
- `set(
        self, key: str, value: bytes, expires: int | datetime | None = None
    )`
- `delete(self, key: str)`
- `clear(self)`
- `close(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/controller.py`

#### Classes
- `CacheController`

#### Functions
- `parse_uri(uri: str)`
- `__init__(
        self,
        cache: BaseCache | None = None,
        cache_etags: bool = True,
        serializer: Serializer | None = None,
        status_codes: Collection[int] | None = None,
    )`
- `_urlnorm(cls, uri: str)`
- `cache_url(cls, uri: str)`
- `parse_cache_control(self, headers: Mapping[str, str])`
- `_load_from_cache(self, request: PreparedRequest)`
- `cached_request(self, request: PreparedRequest)`
- `conditional_headers(self, request: PreparedRequest)`
- `_cache_set(
        self,
        cache_url: str,
        request: PreparedRequest,
        response: HTTPResponse,
        body: bytes | None = None,
        expires_time: int | None = None,
    )`
- `cache_response(
        self,
        request: PreparedRequest,
        response_or_ref: HTTPResponse | weakref.ReferenceType[HTTPResponse],
        body: bytes | None = None,
        status_codes: Collection[int] | None = None,
    )`
- `update_cached_response(
        self, request: PreparedRequest, response: HTTPResponse
    )`

#### Parameters / Constants
- `URI` = `re.compile(r"^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?")`
- `PERMANENT_REDIRECT_STATUSES` = `(301, 308)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/filewrapper.py`

#### Classes
- `CallbackFileWrapper`

#### Functions
- `__init__(
        self, fp: HTTPResponse, callback: Callable[[Buffer], None] | None
    )`
- `__getattr__(self, name: str)`
- `__is_fp_closed(self)`
- `_close(self)`
- `read(self, amt: int | None = None)`
- `_safe_read(self, amt: int)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/heuristics.py`

#### Classes
- `BaseHeuristic`
- `OneDayCache`
- `ExpiresAfter`
- `LastModified`

#### Functions
- `expire_after(delta: timedelta, date: datetime | None = None)`
- `datetime_to_header(dt: datetime)`
- `warning(self, response: HTTPResponse)`
- `update_headers(self, response: HTTPResponse)`
- `apply(self, response: HTTPResponse)`
- `update_headers(self, response: HTTPResponse)`
- `__init__(self, **kw: Any)`
- `update_headers(self, response: HTTPResponse)`
- `warning(self, response: HTTPResponse)`
- `update_headers(self, resp: HTTPResponse)`
- `warning(self, resp: HTTPResponse)`

#### Parameters / Constants
- `TIME_FMT` = `"%a, %d %b %Y %H:%M:%S GMT"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/serialize.py`

#### Classes
- `Serializer`

#### Functions
- `dumps(
        self,
        request: PreparedRequest,
        response: HTTPResponse,
        body: bytes | None = None,
    )`
- `serialize(self, data: dict[str, Any])`
- `loads(
        self,
        request: PreparedRequest,
        data: bytes,
        body_file: IO[bytes] | None = None,
    )`
- `prepare_response(
        self,
        request: PreparedRequest,
        cached: Mapping[str, Any],
        body_file: IO[bytes] | None = None,
    )`
- `_loads_v4(
        self,
        request: PreparedRequest,
        data: bytes,
        body_file: IO[bytes] | None = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/cachecontrol/wrapper.py`

#### Functions
- `CacheControl(
    sess: requests.Session,
    cache: BaseCache | None = None,
    cache_etags: bool = True,
    serializer: Serializer | None = None,
    heuristic: BaseHeuristic | None = None,
    controller_class: type[CacheController] | None = None,
    adapter_class: type[CacheControlAdapter] | None = None,
    cacheable_methods: Collection[str] | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/certifi/core.py`

#### Functions
- `exit_cacert_ctx()`
- `where()`
- `contents()`
- `where()`
- `contents()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/__init__.py`

#### Classes
- `DistlibException`
- `NullHandler`

#### Functions
- `handle(self, record)`
- `emit(self, record)`
- `createLock(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/compat.py`

#### Classes
- `CertificateError`
- `Container`
- `ZipExtFile`
- `ZipFile`
- `ChainMap`
- `OrderedDict`
- `ConvertingDict`
- `ConvertingList`
- `ConvertingTuple`
- `BaseConfigurator`

#### Functions
- `quote(s)`
- `_dnsname_match(dn, hostname, max_wildcards=1)`
- `match_hostname(cert, hostname)`
- `__init__(self, **kwargs)`
- `which(cmd, mode=os.F_OK | os.X_OK, path=None)`
- `_access_check(fn, mode)`
- `__init__(self, base)`
- `__enter__(self)`
- `__exit__(self, *exc_info)`
- `__enter__(self)`
- `__exit__(self, *exc_info)`
- `open(self, *args, **kwargs)`
- `python_implementation()`
- `callable(obj)`
- `fsencode(filename)`
- `fsdecode(filename)`
- `_get_normal_name(orig_enc)`
- `detect_encoding(readline)`
- `read_or_stop()`
- `find_cookie(line)`
- `_recursive_repr(fillvalue='...')`
- `decorating_function(user_function)`
- `wrapper(self)`
- `__init__(self, *maps)`
- `__missing__(self, key)`
- `__getitem__(self, key)`
- `get(self, key, default=None)`
- `__len__(self)`
- `__iter__(self)`
- `__contains__(self, key)`
- `__bool__(self)`
- `__repr__(self)`
- `fromkeys(cls, iterable, *args)`
- `copy(self)`
- `new_child(self)`
- `parents(self)`
- `__setitem__(self, key, value)`
- `__delitem__(self, key)`
- `popitem(self)`
- `pop(self, key, *args)`
- `clear(self)`
- `cache_from_source(path, debug_override=None)`
- `__init__(self, *args, **kwds)`
- `__setitem__(self, key, value, dict_setitem=dict.__setitem__)`
- `__delitem__(self, key, dict_delitem=dict.__delitem__)`
- `__iter__(self)`
- `__reversed__(self)`
- `clear(self)`
- `popitem(self, last=True)`
- `keys(self)`
- `values(self)`
- `items(self)`
- `iterkeys(self)`
- `itervalues(self)`
- `iteritems(self)`
- `update(*args, **kwds)`
- `pop(self, key, default=__marker)`
- `setdefault(self, key, default=None)`
- `__repr__(self, _repr_running=None)`
- `__reduce__(self)`
- `copy(self)`
- `fromkeys(cls, iterable, value=None)`
- `__eq__(self, other)`
- `__ne__(self, other)`
- `viewkeys(self)`
- `viewvalues(self)`
- `viewitems(self)`
- `valid_ident(s)`
- `__getitem__(self, key)`
- `get(self, key, default=None)`
- `pop(self, key, default=None)`
- `__getitem__(self, key)`
- `pop(self, idx=-1)`
- `__getitem__(self, key)`
- `__init__(self, config)`
- `resolve(self, s)`
- `ext_convert(self, value)`
- `cfg_convert(self, value)`
- `convert(self, value)`
- `configure_custom(self, config)`
- `as_tuple(self, value)`

#### Parameters / Constants
- `IDENTIFIER` = `re.compile('^[a-z_][a-z0-9_]*$', re.I)`
- `CONVERT_PATTERN` = `re.compile(r'^(?P<prefix>[a-z]+)://(?P<suffix>.*)$')`
- `WORD_PATTERN` = `re.compile(r'^\s*(\w+)\s*')`
- `DOT_PATTERN` = `re.compile(r'^\.\s*(\w+)\s*')`
- `INDEX_PATTERN` = `re.compile(r'^\[\s*(\w+)\s*\]\s*')`
- `DIGIT_PATTERN` = `re.compile(r'^\d+$')`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/resources.py`

#### Classes
- `ResourceCache`
- `ResourceBase`
- `Resource`
- `ResourceContainer`
- `ResourceFinder`
- `ZipResourceFinder`

#### Functions
- `__init__(self, base=None)`
- `is_stale(self, resource, path)`
- `get(self, resource)`
- `__init__(self, finder, name)`
- `as_stream(self)`
- `file_path(self)`
- `bytes(self)`
- `size(self)`
- `resources(self)`
- `__init__(self, module)`
- `_adjust_path(self, path)`
- `_make_path(self, resource_name)`
- `_find(self, path)`
- `get_cache_info(self, resource)`
- `find(self, resource_name)`
- `get_stream(self, resource)`
- `get_bytes(self, resource)`
- `get_size(self, resource)`
- `get_resources(self, resource)`
- `allowed(f)`
- `is_container(self, resource)`
- `iterator(self, resource_name)`
- `__init__(self, module)`
- `_adjust_path(self, path)`
- `_find(self, path)`
- `get_cache_info(self, resource)`
- `get_bytes(self, resource)`
- `get_stream(self, resource)`
- `get_size(self, resource)`
- `get_resources(self, resource)`
- `_is_directory(self, path)`
- `register_finder(loader, finder_maker)`
- `finder(package)`
- `finder_for_path(path)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/scripts.py`

#### Classes
- `ScriptMaker`

#### Functions
- `enquote_executable(executable)`
- `__init__(self, source_dir, target_dir, add_launchers=True, dry_run=False, fileop=None)`
- `_get_alternate_executable(self, executable, options)`
- `_is_shell(self, executable)`
- `_fix_jython_executable(self, executable)`
- `_build_shebang(self, executable, post_interp)`
- `_get_shebang(self, encoding, post_interp=b'', options=None)`
- `_get_script_text(self, entry)`
- `get_manifest(self, exename)`
- `_write_script(self, names, shebang, script_bytes, filenames, ext)`
- `get_script_filenames(self, name)`
- `_make_script(self, entry, filenames, options=None)`
- `_copy_script(self, script, filenames)`
- `dry_run(self)`
- `dry_run(self, value)`
- `_get_launcher(self, kind)`
- `make(self, specification, options=None)`
- `make_multiple(self, specifications, options=None)`

#### Parameters / Constants
- `FIRST_LINE_RE` = `re.compile(b'^#!.*pythonw?[0-9.]*([ \t].*)?$')`
- `SCRIPT_TEMPLATE` = `r'''# -*- coding: utf-8 -*-`
- `DISTLIB_PACKAGE` = `__name__.rsplit('.', 1)[0]`
- `WRAPPERS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/distlib/util.py`

#### Classes
- `cached_property`
- `FileOperator`
- `ExportEntry`
- `Cache`
- `EventMixin`
- `Sequencer`
- `Progress`
- `HTTPSConnection`
- `HTTPSHandler`
- `HTTPSOnlyHandler`
- `Transport`
- `SafeTransport`
- `ServerProxy`
- `CSVBase`
- `CSVReader`
- `CSVWriter`
- `Configurator`
- `SubprocessMixin`
- `PyPIRCFile`

#### Functions
- `parse_marker(marker_string)`
- `marker_var(remaining)`
- `marker_expr(remaining)`
- `marker_and(remaining)`
- `marker(remaining)`
- `parse_requirement(req)`
- `get_versions(ver_remaining)`
- `get_resources_dests(resources_root, rules)`
- `get_rel_path(root, path)`
- `in_venv()`
- `get_executable()`
- `proceed(prompt, allowed_chars, error_prompt=None, default=None)`
- `extract_by_key(d, keys)`
- `read_exports(stream)`
- `read_stream(cp, stream)`
- `write_exports(exports, stream)`
- `tempdir()`
- `chdir(d)`
- `socket_timeout(seconds=15)`
- `__init__(self, func)`
- `__get__(self, obj, cls=None)`
- `convert_path(pathname)`
- `__init__(self, dry_run=False)`
- `_init_record(self)`
- `record_as_written(self, path)`
- `newer(self, source, target)`
- `copy_file(self, infile, outfile, check=True)`
- `copy_stream(self, instream, outfile, encoding=None)`
- `write_binary_file(self, path, data)`
- `write_text_file(self, path, data, encoding)`
- `set_mode(self, bits, mask, files)`
- `ensure_dir(self, path)`
- `byte_compile(self, path, optimize=False, force=False, prefix=None, hashed_invalidation=False)`
- `ensure_removed(self, path)`
- `is_writable(self, path)`
- `commit(self)`
- `rollback(self)`
- `resolve(module_name, dotted_path)`
- `__init__(self, name, prefix, suffix, flags)`
- `value(self)`
- `__repr__(self)`
- `__eq__(self, other)`
- `get_export_entry(specification)`
- `get_cache_base(suffix=None)`
- `path_to_cache_dir(path, use_abspath=True)`
- `ensure_slash(s)`
- `parse_credentials(netloc)`
- `get_process_umask()`
- `is_string_sequence(seq)`
- `split_filename(filename, project_name=None)`
- `parse_name_and_version(p)`
- `get_extras(requested, available)`
- `_get_external_data(url)`
- `get_project_data(name)`
- `get_package_data(name, version)`
- `__init__(self, base)`
- `prefix_to_dir(self, prefix, use_abspath=True)`
- `clear(self)`
- `__init__(self)`
- `add(self, event, subscriber, append=True)`
- `remove(self, event, subscriber)`
- `get_subscribers(self, event)`
- `publish(self, event, *args, **kwargs)`
- `__init__(self)`
- `add_node(self, node)`
- `remove_node(self, node, edges=False)`
- `add(self, pred, succ)`
- `remove(self, pred, succ)`
- `is_step(self, step)`
- `get_steps(self, final)`
- `strong_connections(self)`
- `strongconnect(node)`
- `dot(self)`
- `unarchive(archive_filename, dest_dir, format=None, check=True)`
- `check_path(path)`
- `extraction_filter(member, path)`
- `zip_dir(directory)`
- `__init__(self, minval=0, maxval=100)`
- `update(self, curval)`
- `increment(self, incr)`
- `start(self)`
- `stop(self)`
- `maximum(self)`
- `percentage(self)`
- `format_duration(self, duration)`
- `ETA(self)`
- `speed(self)`
- `iglob(path_glob)`
- `_iglob(path_glob)`
- `connect(self)`
- `__init__(self, ca_certs, check_domain=True)`
- `_conn_maker(self, *args, **kwargs)`
- `https_open(self, req)`
- `http_open(self, req)`
- `__init__(self, timeout, use_datetime=0)`
- `make_connection(self, host)`
- `__init__(self, timeout, use_datetime=0)`
- `make_connection(self, host)`
- `__init__(self, uri, **kwargs)`
- `_csv_open(fn, mode, **kwargs)`
- `__enter__(self)`
- `__exit__(self, *exc_info)`
- `__init__(self, **kwargs)`
- `__iter__(self)`
- `next(self)`
- `__init__(self, fn, **kwargs)`
- `writerow(self, row)`
- `__init__(self, config, base=None)`
- `configure_custom(self, config)`
- `convert(o)`
- `__getitem__(self, key)`
- `inc_convert(self, value)`
- `__init__(self, verbose=False, progress=None)`
- `reader(self, stream, context)`
- `run_command(self, cmd, **kwargs)`
- `normalize_name(name)`
- `__init__(self, fn=None, url=None)`
- `read(self)`
- `update(self, username, password)`
- `_load_pypirc(index)`
- `_store_pypirc(index)`
- `get_host_platform()`
- `get_platform()`

#### Parameters / Constants
- `IDENTIFIER` = `re.compile(r'^([\w\.-]+)\s*')`
- `VERSION_IDENTIFIER` = `re.compile(r'^([\w\.*+-]+)\s*')`
- `COMPARE_OP` = `re.compile(r'^(<=?|>=?|={2,3}|[~!]=)\s*')`
- `MARKER_OP` = `re.compile(r'^((<=?)|(>=?)|={2,3}|[~!]=|in|not\s+in)\s*')`
- `AND` = `re.compile(r'^and\b\s*')`
- `NON_SPACE` = `re.compile(r'(\S+)\s*')`
- `STRING_CHUNK` = `re.compile(r'([\s\w\.{}()*+#:;,/?!~`@$%^&=|<>\[\]-]+)')`
- `ENTRY_RE` = `re.compile(`
- `PROJECT_NAME_AND_VERSION` = `re.compile('([a-z0-9_]+([.-][a-z_][a-z0-9_]*)*)-'`
- `PYTHON_VERSION` = `re.compile(r'-py(\d\.?\d?)')`
- `NAME_VERSION_RE` = `re.compile(r'(?P<name>[\w .-]+)\s*'`
- `ARCHIVE_EXTENSIONS` = `('.tar.gz', '.tar.bz2', '.tar', '.zip', '.tgz', '.tbz', '.whl')`
- `UNITS` = `('', 'K', 'M', 'G', 'T', 'P')`
- `RICH_GLOB` = `re.compile(r'\{([^}]*)\}')`
- `DEFAULT_REPOSITORY` = `'https://upload.pypi.org/legacy/'`
- `DEFAULT_REALM` = `'pypi'`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/distro/distro.py`

#### Classes
- `VersionDict`
- `InfoDict`
- `cached_property`
- `LinuxDistribution`

#### Functions
- `linux_distribution(full_distribution_name: bool = True)`
- `id()`
- `name(pretty: bool = False)`
- `version(pretty: bool = False, best: bool = False)`
- `version_parts(best: bool = False)`
- `major_version(best: bool = False)`
- `minor_version(best: bool = False)`
- `build_number(best: bool = False)`
- `like()`
- `codename()`
- `info(pretty: bool = False, best: bool = False)`
- `os_release_info()`
- `lsb_release_info()`
- `distro_release_info()`
- `uname_info()`
- `os_release_attr(attribute: str)`
- `lsb_release_attr(attribute: str)`
- `distro_release_attr(attribute: str)`
- `uname_attr(attribute: str)`
- `__init__(self, f: Callable[[Any], Any])`
- `__get__(self, obj: Any, owner: Type[Any])`
- `__init__(
        self,
        include_lsb: Optional[bool] = None,
        os_release_file: str = "",
        distro_release_file: str = "",
        include_uname: Optional[bool] = None,
        root_dir: Optional[str] = None,
        include_oslevel: Optional[bool] = None,
    )`
- `__repr__(self)`
- `linux_distribution(
        self, full_distribution_name: bool = True
    )`
- `id(self)`
- `normalize(distro_id: str, table: Dict[str, str])`
- `name(self, pretty: bool = False)`
- `version(self, pretty: bool = False, best: bool = False)`
- `version_parts(self, best: bool = False)`
- `major_version(self, best: bool = False)`
- `minor_version(self, best: bool = False)`
- `build_number(self, best: bool = False)`
- `like(self)`
- `codename(self)`
- `info(self, pretty: bool = False, best: bool = False)`
- `os_release_info(self)`
- `lsb_release_info(self)`
- `distro_release_info(self)`
- `uname_info(self)`
- `oslevel_info(self)`
- `os_release_attr(self, attribute: str)`
- `lsb_release_attr(self, attribute: str)`
- `distro_release_attr(self, attribute: str)`
- `uname_attr(self, attribute: str)`
- `_os_release_info(self)`
- `_parse_os_release_content(lines: TextIO)`
- `_lsb_release_info(self)`
- `_parse_lsb_release_content(lines: Iterable[str])`
- `_uname_info(self)`
- `_oslevel_info(self)`
- `_debian_version(self)`
- `_parse_uname_content(lines: Sequence[str])`
- `_to_str(bytestring: bytes)`
- `_distro_release_info(self)`
- `_parse_distro_release_file(self, filepath: str)`
- `_parse_distro_release_content(line: str)`
- `main()`

#### Parameters / Constants
- `NORMALIZED_OS_ID` = `{`
- `NORMALIZED_LSB_ID` = `{`
- `NORMALIZED_DISTRO_ID` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/codec.py`

#### Classes
- `Codec`
- `IncrementalEncoder`
- `IncrementalDecoder`
- `StreamWriter`
- `StreamReader`

#### Functions
- `encode(self, data: str, errors: str = "strict")`
- `decode(self, data: bytes, errors: str = "strict")`
- `_buffer_encode(self, data: str, errors: str, final: bool)`
- `_buffer_decode(self, data: Any, errors: str, final: bool)`
- `search_function(name: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/compat.py`

#### Functions
- `ToASCII(label: str)`
- `ToUnicode(label: Union[bytes, bytearray])`
- `nameprep(s: Any)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/core.py`

#### Classes
- `IDNAError`
- `IDNABidiError`
- `InvalidCodepoint`
- `InvalidCodepointContext`

#### Functions
- `_combining_class(cp: int)`
- `_is_script(cp: str, script: str)`
- `_punycode(s: str)`
- `_unot(s: int)`
- `valid_label_length(label: Union[bytes, str])`
- `valid_string_length(label: Union[bytes, str], trailing_dot: bool)`
- `check_bidi(label: str, check_ltr: bool = False)`
- `check_initial_combiner(label: str)`
- `check_hyphen_ok(label: str)`
- `check_nfc(label: str)`
- `valid_contextj(label: str, pos: int)`
- `valid_contexto(label: str, pos: int, exception: bool = False)`
- `check_label(label: Union[str, bytes, bytearray])`
- `alabel(label: str)`
- `ulabel(label: Union[str, bytes, bytearray])`
- `uts46_remap(domain: str, std3_rules: bool = True, transitional: bool = False)`
- `encode(
    s: Union[str, bytes, bytearray],
    strict: bool = False,
    uts46: bool = False,
    std3_rules: bool = False,
    transitional: bool = False,
)`
- `decode(
    s: Union[str, bytes, bytearray],
    strict: bool = False,
    uts46: bool = False,
    std3_rules: bool = False,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/intranges.py`

#### Functions
- `intranges_from_list(list_: List[int])`
- `_encode_range(start: int, end: int)`
- `_decode_range(r: int)`
- `intranges_contain(int_: int, ranges: Tuple[int, ...])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/idna/uts46data.py`

#### Functions
- `_seg_0()`
- `_seg_1()`
- `_seg_2()`
- `_seg_3()`
- `_seg_4()`
- `_seg_5()`
- `_seg_6()`
- `_seg_7()`
- `_seg_8()`
- `_seg_9()`
- `_seg_10()`
- `_seg_11()`
- `_seg_12()`
- `_seg_13()`
- `_seg_14()`
- `_seg_15()`
- `_seg_16()`
- `_seg_17()`
- `_seg_18()`
- `_seg_19()`
- `_seg_20()`
- `_seg_21()`
- `_seg_22()`
- `_seg_23()`
- `_seg_24()`
- `_seg_25()`
- `_seg_26()`
- `_seg_27()`
- `_seg_28()`
- `_seg_29()`
- `_seg_30()`
- `_seg_31()`
- `_seg_32()`
- `_seg_33()`
- `_seg_34()`
- `_seg_35()`
- `_seg_36()`
- `_seg_37()`
- `_seg_38()`
- `_seg_39()`
- `_seg_40()`
- `_seg_41()`
- `_seg_42()`
- `_seg_43()`
- `_seg_44()`
- `_seg_45()`
- `_seg_46()`
- `_seg_47()`
- `_seg_48()`
- `_seg_49()`
- `_seg_50()`
- `_seg_51()`
- `_seg_52()`
- `_seg_53()`
- `_seg_54()`
- `_seg_55()`
- `_seg_56()`
- `_seg_57()`
- `_seg_58()`
- `_seg_59()`
- `_seg_60()`
- `_seg_61()`
- `_seg_62()`
- `_seg_63()`
- `_seg_64()`
- `_seg_65()`
- `_seg_66()`
- `_seg_67()`
- `_seg_68()`
- `_seg_69()`
- `_seg_70()`
- `_seg_71()`
- `_seg_72()`
- `_seg_73()`
- `_seg_74()`
- `_seg_75()`
- `_seg_76()`
- `_seg_77()`
- `_seg_78()`
- `_seg_79()`
- `_seg_80()`
- `_seg_81()`
- `_seg_82()`
- `_seg_83()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/__init__.py`

#### Functions
- `pack(o, stream, **kwargs)`
- `packb(o, **kwargs)`
- `unpack(stream, **kwargs)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/exceptions.py`

#### Classes
- `UnpackException`
- `BufferFull`
- `OutOfData`
- `FormatError`
- `StackError`
- `ExtraData`

#### Functions
- `__init__(self, unpacked, extra)`
- `__str__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/ext.py`

#### Classes
- `ExtType`
- `Timestamp`

#### Functions
- `__new__(cls, code, data)`
- `__init__(self, seconds, nanoseconds=0)`
- `__repr__(self)`
- `__eq__(self, other)`
- `__ne__(self, other)`
- `__hash__(self)`
- `from_bytes(b)`
- `to_bytes(self)`
- `from_unix(unix_sec)`
- `to_unix(self)`
- `from_unix_nano(unix_ns)`
- `to_unix_nano(self)`
- `to_datetime(self)`
- `from_datetime(dt)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/msgpack/fallback.py`

#### Classes
- `BytesIO`
- `Unpacker`
- `Packer`

#### Functions
- `__init__(self, s=b"")`
- `write(self, s)`
- `getvalue(self)`
- `newlist_hint(size)`
- `_check_type_strict(obj, t, type=type, tuple=tuple)`
- `_get_data_from_buffer(obj)`
- `unpackb(packed, **kwargs)`
- `__init__(
        self,
        file_like=None,
        *,
        read_size=0,
        use_list=True,
        raw=False,
        timestamp=0,
        strict_map_key=True,
        object_hook=None,
        object_pairs_hook=None,
        list_hook=None,
        unicode_errors=None,
        max_buffer_size=100 * 1024 * 1024,
        ext_hook=ExtType,
        max_str_len=-1,
        max_bin_len=-1,
        max_array_len=-1,
        max_map_len=-1,
        max_ext_len=-1,
    )`
- `feed(self, next_bytes)`
- `_consume(self)`
- `_got_extradata(self)`
- `_get_extradata(self)`
- `read_bytes(self, n)`
- `_read(self, n, raise_outofdata=True)`
- `_reserve(self, n, raise_outofdata=True)`
- `_read_header(self)`
- `_unpack(self, execute=EX_CONSTRUCT)`
- `__iter__(self)`
- `__next__(self)`
- `skip(self)`
- `unpack(self)`
- `read_array_header(self)`
- `read_map_header(self)`
- `tell(self)`
- `__init__(
        self,
        *,
        default=None,
        use_single_float=False,
        autoreset=True,
        use_bin_type=True,
        strict_types=False,
        datetime=False,
        unicode_errors=None,
        buf_size=None,
    )`
- `_pack(
        self,
        obj,
        nest_limit=DEFAULT_RECURSE_LIMIT,
        check=isinstance,
        check_type_strict=_check_type_strict,
    )`
- `pack(self, obj)`
- `pack_map_pairs(self, pairs)`
- `pack_array_header(self, n)`
- `pack_map_header(self, n)`
- `pack_ext_type(self, typecode, data)`
- `_pack_array_header(self, n)`
- `_pack_map_header(self, n)`
- `_pack_map_pairs(self, n, pairs, nest_limit=DEFAULT_RECURSE_LIMIT)`
- `_pack_raw_header(self, n)`
- `_pack_bin_header(self, n)`
- `bytes(self)`
- `reset(self)`
- `getbuffer(self)`

#### Parameters / Constants
- `EX_SKIP` = `0`
- `EX_CONSTRUCT` = `1`
- `EX_READ_ARRAY_HEADER` = `2`
- `EX_READ_MAP_HEADER` = `3`
- `TYPE_IMMEDIATE` = `0`
- `TYPE_ARRAY` = `1`
- `TYPE_MAP` = `2`
- `TYPE_RAW` = `3`
- `TYPE_BIN` = `4`
- `TYPE_EXT` = `5`
- `DEFAULT_RECURSE_LIMIT` = `511`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_elffile.py`

#### Classes
- `ELFInvalid`
- `EIClass`
- `EIData`
- `EMachine`
- `ELFFile`

#### Functions
- `__init__(self, f: IO[bytes])`
- `_read(self, fmt: str)`
- `interpreter(self)`

#### Parameters / Constants
- `C32` = `1`
- `C64` = `2`
- `I386` = `3`
- `S390` = `22`
- `X8664` = `62`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_manylinux.py`

#### Classes
- `_GLibCVersion`

#### Functions
- `_parse_elf(path: str)`
- `_is_linux_armhf(executable: str)`
- `_is_linux_i686(executable: str)`
- `_have_compatible_abi(executable: str, archs: Sequence[str])`
- `_glibc_version_string_confstr()`
- `_glibc_version_string_ctypes()`
- `_glibc_version_string()`
- `_parse_glibc_version(version_str: str)`
- `_get_glibc_version()`
- `_is_compatible(arch: str, version: _GLibCVersion)`
- `platform_tags(archs: Sequence[str])`

#### Parameters / Constants
- `EF_ARM_ABIMASK` = `0xFF000000`
- `EF_ARM_ABI_VER5` = `0x05000000`
- `EF_ARM_ABI_FLOAT_HARD` = `0x00000400`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_musllinux.py`

#### Classes
- `_MuslVersion`

#### Functions
- `_parse_musl_version(output: str)`
- `_get_musl_version(executable: str)`
- `platform_tags(archs: Sequence[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_parser.py`

#### Classes
- `Node`
- `Variable`
- `Value`
- `Op`
- `ParsedRequirement`

#### Functions
- `__init__(self, value: str)`
- `__str__(self)`
- `__repr__(self)`
- `serialize(self)`
- `__getstate__(self)`
- `_restore_value(self, value: object)`
- `__setstate__(self, state: object)`
- `serialize(self)`
- `serialize(self)`
- `serialize(self)`
- `parse_requirement(source: str)`
- `_parse_requirement(tokenizer: Tokenizer)`
- `_parse_requirement_details(
    tokenizer: Tokenizer,
)`
- `_parse_requirement_marker(
    tokenizer: Tokenizer, *, span_start: int, expected: str
)`
- `_parse_extras(tokenizer: Tokenizer)`
- `_parse_extras_list(tokenizer: Tokenizer)`
- `_parse_specifier(tokenizer: Tokenizer)`
- `_parse_version_many(tokenizer: Tokenizer)`
- `parse_marker(source: str)`
- `_parse_full_marker(tokenizer: Tokenizer)`
- `_parse_marker(tokenizer: Tokenizer)`
- `_parse_marker_atom(tokenizer: Tokenizer)`
- `_parse_marker_item(tokenizer: Tokenizer)`
- `_parse_marker_var(tokenizer: Tokenizer)`
- `process_env_var(env_var: str)`
- `process_python_str(python_str: str)`
- `_parse_marker_op(tokenizer: Tokenizer)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_structures.py`

#### Classes
- `InfinityType`
- `NegativeInfinityType`

#### Functions
- `__repr__(self)`
- `__repr__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/_tokenizer.py`

#### Classes
- `Token`
- `ParserSyntaxError`
- `Tokenizer`

#### Functions
- `__init__(
        self,
        message: str,
        *,
        source: str,
        span: tuple[int, int],
    )`
- `__str__(self)`
- `__init__(
        self,
        source: str,
        *,
        rules: Mapping[str, re.Pattern[str]],
    )`
- `consume(self, name: str)`
- `check(self, name: str, *, peek: bool = False)`
- `expect(self, name: str, *, expected: str)`
- `read(self)`
- `raise_syntax_error(
        self,
        message: str,
        *,
        span_start: int | None = None,
        span_end: int | None = None,
    )`
- `enclosing_tokens(
        self, open_token: str, close_token: str, *, around: str
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/dependency_groups.py`

#### Classes
- `DuplicateGroupNames`
- `CyclicDependencyGroup`
- `InvalidDependencyGroupObject`
- `DependencyGroupInclude`
- `DependencyGroupResolver`

#### Functions
- `__dir__()`
- `__init__(self, requested_group: str, group: str, include_group: str)`
- `__init__(self, include_group: str)`
- `__repr__(self)`
- `__init__(
        self,
        dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    )`
- `lookup(self, group: str)`
- `resolve(self, group: str)`
- `_resolve(
        self, group: str, requested_group: str, errors: _ErrorCollector
    )`
- `_parse_group(
        self, group: str, errors: _ErrorCollector
    )`
- `resolve_dependency_groups(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]], /, *groups: str
)`
- `_normalize_name(name: str)`
- `_normalize_group_names(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    errors: _ErrorCollector,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/direct_url.py`

#### Classes
- `_FromMappingProtocol`
- `DirectUrlValidationError`
- `_DirectUrlRequiredKeyError`
- `VcsInfo`
- `ArchiveInfo`
- `DirInfo`
- `DirectUrl`

#### Functions
- `__dir__()`
- `_from_dict(cls, d: Mapping[str, Any])`
- `_json_dict_factory(data: list[tuple[str, Any]])`
- `_get(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_required(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_object(
    d: Mapping[str, Any], target_type: type[_FromMappingProtocolT], key: str
)`
- `_strip_auth_from_netloc(netloc: str, safe_user_passwords: Collection[str])`
- `_strip_url(url: str, safe_user_passwords: Collection[str])`
- `__init__(
        self,
        cause: str | Exception,
        *,
        context: str | None = None,
    )`
- `__str__(self)`
- `__init__(self, key: str)`
- `__init__(
        self,
        *,
        vcs: str,
        commit_id: str,
        requested_revision: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        hashes: Mapping[str, str] | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        editable: bool | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        url: str,
        archive_info: ArchiveInfo | None = None,
        vcs_info: VcsInfo | None = None,
        dir_info: DirInfo | None = None,
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `from_dict(cls, d: Mapping[str, Any], /)`
- `to_dict(
        self,
        *,
        generate_legacy_hash: bool = False,
        strip_user_password: bool = True,
        safe_user_passwords: Collection[str] = ("git",)`
- `validate(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/errors.py`

#### Classes
- `ExceptionGroup`
- `_ErrorCollector`

#### Functions
- `__dir__()`
- `__init__(self, message: str, exceptions: list[Exception])`
- `__repr__(self)`
- `finalize(self, msg: str)`
- `on_exit(self, msg: str)`
- `collect(self, *err_cls: type[Exception])`
- `error(
        self,
        error: Exception,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/licenses/__init__.py`

#### Classes
- `InvalidLicenseExpression`

#### Functions
- `__dir__()`
- `canonicalize_license_expression(
    raw_license_expression: str,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/licenses/_spdx.py`

#### Classes
- `SPDXLicense`
- `SPDXException`

#### Parameters / Constants
- `VERSION` = `'3.27.0'`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/markers.py`

#### Classes
- `InvalidMarker`
- `UndefinedComparison`
- `UndefinedEnvironmentName`
- `Environment`
- `Marker`

#### Functions
- `__dir__()`
- `_normalize_extras(
    result: MarkerList | MarkerAtom | str,
)`
- `_normalize_extra_values(results: MarkerList)`
- `_format_marker(
    marker: list[str] | MarkerAtom | str, first: bool | None = True
)`
- `_eval_op(lhs: str, op: Op, rhs: str | AbstractSet[str], *, key: str)`
- `_normalize(
    lhs: str, rhs: str | AbstractSet[str], key: str
)`
- `_evaluate_markers(
    markers: MarkerList, environment: dict[str, str | AbstractSet[str]]
)`
- `_format_full_version(info: sys._version_info)`
- `default_environment()`
- `__init__(self, marker: str)`
- `_from_markers(cls, markers: MarkerList)`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `__and__(self, other: Marker)`
- `__or__(self, other: Marker)`
- `evaluate(
        self,
        environment: Mapping[str, str | AbstractSet[str]] | None = None,
        context: EvaluateContext = "metadata",
    )`
- `_repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
)`

#### Parameters / Constants
- `MARKERS_ALLOWING_SET` = `{"extras", "dependency_groups"}`
- `MARKERS_REQUIRING_VERSION` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/metadata.py`

#### Classes
- `InvalidMetadata`
- `RawMetadata`
- `RFC822Policy`
- `RFC822Message`
- `_Validator`
- `Metadata`

#### Functions
- `__dir__()`
- `__init__(self, field: str, message: str)`
- `_parse_keywords(data: str)`
- `_parse_project_urls(data: list[str])`
- `_get_payload(msg: email.message.Message, source: bytes | str)`
- `header_store_parse(self, name: str, value: str)`
- `__init__(self)`
- `as_bytes(
        self, unixfrom: bool = False, policy: email.policy.Policy | None = None
    )`
- `parse_email(data: bytes | str)`
- `__init__(
        self,
        *,
        added: _MetadataVersion = "1.0",
    )`
- `__set_name__(self, _owner: Metadata, name: str)`
- `__get__(self, instance: Metadata, _owner: type[Metadata])`
- `_invalid_metadata(
        self, msg: str, cause: Exception | None = None
    )`
- `_process_metadata_version(self, value: str)`
- `_process_name(self, value: str)`
- `_process_version(self, value: str)`
- `_process_summary(self, value: str)`
- `_process_description_content_type(self, value: str)`
- `_process_dynamic(self, value: list[str])`
- `_process_provides_extra(
        self,
        value: list[str],
    )`
- `_process_requires_python(self, value: str)`
- `_process_requires_dist(
        self,
        value: list[str],
    )`
- `_process_license_expression(self, value: str)`
- `_process_license_files(self, value: list[str])`
- `_process_import_names(self, value: list[str])`
- `from_raw(cls, data: RawMetadata, *, validate: bool = True)`
- `from_email(cls, data: bytes | str, *, validate: bool = True)`
- `as_rfc822(self)`
- `_write_metadata(self, message: RFC822Message)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/pylock.py`

#### Classes
- `_FromMappingProtocol`
- `PylockValidationError`
- `_PylockRequiredKeyError`
- `PylockUnsupportedVersionError`
- `PylockSelectError`
- `PackageVcs`
- `PackageDirectory`
- `PackageArchive`
- `PackageSdist`
- `PackageWheel`
- `Package`
- `Pylock`

#### Functions
- `__dir__()`
- `_from_dict(cls, d: Mapping[str, Any])`
- `is_valid_pylock_path(path: Path)`
- `_toml_key(key: str)`
- `_toml_value(key: str, value: Any)`
- `_toml_dict_factory(data: list[tuple[str, Any]])`
- `_get(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_required(d: Mapping[str, Any], expected_type: type[_T], key: str)`
- `_get_sequence(
    d: Mapping[str, Any], expected_item_type: type[_T], key: str
)`
- `_get_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
)`
- `_get_required_as(
    d: Mapping[str, Any],
    expected_type: type[_T],
    target_type: Callable[[_T], _T2],
    key: str,
)`
- `_get_sequence_as(
    d: Mapping[str, Any],
    expected_item_type: type[_T],
    target_item_type: Callable[[_T], _T2],
    key: str,
)`
- `_get_object(
    d: Mapping[str, Any], target_type: type[_FromMappingProtocolT], key: str
)`
- `_get_sequence_of_objects(
    d: Mapping[str, Any], target_item_type: type[_FromMappingProtocolT], key: str
)`
- `_get_required_sequence_of_objects(
    d: Mapping[str, Any], target_item_type: type[_FromMappingProtocolT], key: str
)`
- `_validate_normalized_name(name: str)`
- `_validate_path_url(path: str | None, url: str | None)`
- `_path_name(path: str | None)`
- `_url_name(url: str | None)`
- `_validate_hashes(hashes: Mapping[str, Any])`
- `__init__(
        self,
        cause: str | Exception,
        *,
        context: str | None = None,
    )`
- `__str__(self)`
- `__init__(self, key: str)`
- `__init__(
        self,
        *,
        type: str,
        url: str | None = None,
        path: str | None = None,
        requested_revision: str | None = None,
        commit_id: str,
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        path: str,
        editable: bool | None = None,
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        url: str | None = None,
        path: str | None = None,
        size: int | None = None,
        upload_time: datetime | None = None,
        hashes: Mapping[str, str],
        subdirectory: str | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `__init__(
        self,
        *,
        name: str | None = None,
        upload_time: datetime | None = None,
        url: str | None = None,
        path: str | None = None,
        size: int | None = None,
        hashes: Mapping[str, str],
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `filename(self)`
- `__init__(
        self,
        *,
        name: str | None = None,
        upload_time: datetime | None = None,
        url: str | None = None,
        path: str | None = None,
        size: int | None = None,
        hashes: Mapping[str, str],
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `filename(self)`
- `__init__(
        self,
        *,
        name: NormalizedName,
        version: Version | None = None,
        marker: Marker | None = None,
        requires_python: SpecifierSet | None = None,
        dependencies: Sequence[Mapping[str, Any]] | None = None,
        vcs: PackageVcs | None = None,
        directory: PackageDirectory | None = None,
        archive: PackageArchive | None = None,
        index: str | None = None,
        sdist: PackageSdist | None = None,
        wheels: Sequence[PackageWheel] | None = None,
        attestation_identities: Sequence[Mapping[str, Any]] | None = None,
        tool: Mapping[str, Any] | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `is_direct(self)`
- `__init__(
        self,
        *,
        lock_version: Version,
        environments: Sequence[Marker] | None = None,
        requires_python: SpecifierSet | None = None,
        extras: Sequence[NormalizedName] | None = None,
        dependency_groups: Sequence[str] | None = None,
        default_groups: Sequence[str] | None = None,
        created_by: str,
        packages: Sequence[Package],
        tool: Mapping[str, Any] | None = None,
    )`
- `_from_dict(cls, d: Mapping[str, Any])`
- `from_dict(cls, d: Mapping[str, Any], /)`
- `to_dict(self)`
- `validate(self)`
- `select(
        self,
        *,
        environment: Environment | None = None,
        tags: Sequence[Tag] | None = None,
        extras: Collection[str] | None = None,
        dependency_groups: Collection[str] | None = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/requirements.py`

#### Classes
- `InvalidRequirement`
- `Requirement`

#### Functions
- `__dir__()`
- `__init__(self, requirement_string: str)`
- `_iter_parts(self, name: str)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `__str__(self)`
- `__repr__(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/specifiers.py`

#### Classes
- `_BoundaryKind`
- `_BoundaryVersion`
- `_LowerBound`
- `_UpperBound`
- `InvalidSpecifier`
- `BaseSpecifier`
- `Specifier`
- `SpecifierSet`

#### Functions
- `__dir__()`
- `_validate_spec(spec: object, /)`
- `_validate_pre(pre: object, /)`
- `_trim_release(release: tuple[int, ...])`
- `__init__(self, version: Version, kind: _BoundaryKind)`
- `_is_family(self, other: Version)`
- `__eq__(self, other: object)`
- `__lt__(self, other: _BoundaryVersion | Version)`
- `__hash__(self)`
- `__repr__(self)`
- `__init__(self, version: _VersionOrBoundary, inclusive: bool)`
- `__eq__(self, other: object)`
- `__lt__(self, other: _LowerBound)`
- `__hash__(self)`
- `__repr__(self)`
- `__init__(self, version: _VersionOrBoundary, inclusive: bool)`
- `__eq__(self, other: object)`
- `__lt__(self, other: _UpperBound)`
- `__hash__(self)`
- `__repr__(self)`
- `_range_is_empty(lower: _LowerBound, upper: _UpperBound)`
- `_intersect_ranges(
    left: Sequence[_VersionRange],
    right: Sequence[_VersionRange],
)`
- `_next_prefix_dev0(version: Version)`
- `_base_dev0(version: Version)`
- `_coerce_version(version: UnparsedVersion)`
- `_public_version(version: Version)`
- `_post_base(version: Version)`
- `_earliest_prerelease(version: Version)`
- `_nearest_non_prerelease(
    v: _VersionOrBoundary,
)`
- `_str(self)`
- `__str__(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`
- `prereleases(self)`
- `prereleases(self, value: bool)`
- `contains(self, item: str, prereleases: bool | None = None)`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], UnparsedVersion] | None = None,
    )`
- `__init__(self, spec: str = "", prereleases: bool | None = None)`
- `_get_spec_version(self, version: str)`
- `_require_spec_version(self, version: str)`
- `_to_ranges(self)`
- `_wildcard_ranges(self, op: str, ver_str: str)`
- `_standard_ranges(self, op: str, ver_str: str)`
- `prereleases(self)`
- `prereleases(self, value: bool | None)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `operator(self)`
- `version(self)`
- `__repr__(self)`
- `__str__(self)`
- `_canonical_spec(self)`
- `__hash__(self)`
- `__eq__(self, other: object)`
- `_get_operator(self, op: str)`
- `_compare_compatible(self, prospective: Version, spec: str)`
- `_get_wildcard_split(self, spec: str)`
- `_compare_equal(self, prospective: Version, spec: str)`
- `_compare_not_equal(self, prospective: Version, spec: str)`
- `_compare_less_than_equal(self, prospective: Version, spec: str)`
- `_compare_greater_than_equal(self, prospective: Version, spec: str)`
- `_compare_less_than(self, prospective: Version, spec_str: str)`
- `_compare_greater_than(self, prospective: Version, spec_str: str)`
- `_compare_arbitrary(self, prospective: Version | str, spec: str)`
- `__contains__(self, item: str | Version)`
- `contains(self, item: UnparsedVersion, prereleases: bool | None = None)`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], UnparsedVersion] | None = None,
    )`
- `_pep440_filter_prereleases(
    iterable: Iterable[Any], key: Callable[[Any], UnparsedVersion] | None
)`
- `_version_split(version: str)`
- `_version_join(components: list[str])`
- `_is_not_suffix(segment: str)`
- `_numeric_prefix_len(split: list[str])`
- `_left_pad(split: list[str], target_numeric_len: int)`
- `_operator_cost(op_entry: tuple[CallableOperator, str, str])`
- `__init__(
        self,
        specifiers: str | Iterable[Specifier] = "",
        prereleases: bool | None = None,
    )`
- `_canonical_specs(self)`
- `prereleases(self)`
- `prereleases(self, value: bool | None)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `__repr__(self)`
- `__str__(self)`
- `__hash__(self)`
- `__and__(self, other: SpecifierSet | str)`
- `__eq__(self, other: object)`
- `__len__(self)`
- `__iter__(self)`
- `_get_ranges(self)`
- `is_unsatisfiable(self)`
- `_check_prerelease_only_ranges(self)`
- `_check_arbitrary_unsatisfiable(self)`
- `__contains__(self, item: UnparsedVersion)`
- `contains(
        self,
        item: UnparsedVersion,
        prereleases: bool | None = None,
        installed: bool | None = None,
    )`
- `filter(
        self,
        iterable: Iterable[UnparsedVersionVar],
        prereleases: bool | None = None,
        key: None = ...,
    )`
- `filter(
        self,
        iterable: Iterable[T],
        prereleases: bool | None = None,
        key: Callable[[T], UnparsedVersion] = ...,
    )`
- `filter(
        self,
        iterable: Iterable[Any],
        prereleases: bool | None = None,
        key: Callable[[Any], UnparsedVersion] | None = None,
    )`
- `_filter_versions(
        self,
        iterable: Iterable[Any],
        key: Callable[[Any], UnparsedVersion] | None,
        prereleases: bool | None = None,
    )`

#### Parameters / Constants
- `AFTER_LOCALS` = `enum.auto()  # after V+local, before V.post0`
- `AFTER_POSTS` = `enum.auto()  # after V.postN, before next release`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/tags.py`

#### Classes
- `UnsortedTagsError`
- `Tag`

#### Functions
- `__dir__()`
- `_compute_32_bit_interpreter()`
- `__init__(self, interpreter: str, abi: str, platform: str)`
- `interpreter(self)`
- `abi(self)`
- `platform(self)`
- `__eq__(self, other: object)`
- `__hash__(self)`
- `__str__(self)`
- `__repr__(self)`
- `__getstate__(self)`
- `__setstate__(self, state: object)`
- `parse_tag(tag: str, *, validate_order: bool = False)`
- `_get_config_var(name: str, warn: bool = False)`
- `_normalize_string(string: str)`
- `_is_threaded_cpython(abis: list[str])`
- `_abi3_applies(python_version: PythonVersion, threading: bool)`
- `_abi3t_applies(python_version: PythonVersion, threading: bool)`
- `_cpython_abis(py_version: PythonVersion, warn: bool = False)`
- `cpython_tags(
    python_version: PythonVersion | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
)`
- `_generic_abi()`
- `generic_tags(
    interpreter: str | None = None,
    abis: Iterable[str] | None = None,
    platforms: Iterable[str] | None = None,
    *,
    warn: bool = False,
)`
- `_py_interpreter_range(py_version: PythonVersion)`
- `compatible_tags(
    python_version: PythonVersion | None = None,
    interpreter: str | None = None,
    platforms: Iterable[str] | None = None,
)`
- `_mac_arch(arch: str, is_32bit: bool = _32_BIT_INTERPRETER)`
- `_mac_binary_formats(version: AppleVersion, cpu_arch: str)`
- `mac_platforms(
    version: AppleVersion | None = None, arch: str | None = None
)`
- `ios_platforms(
    version: AppleVersion | None = None, multiarch: str | None = None
)`
- `android_platforms(
    api_level: int | None = None, abi: str | None = None
)`
- `_linux_platforms(is_32bit: bool = _32_BIT_INTERPRETER)`
- `_emscripten_platforms()`
- `_generic_platforms()`
- `platform_tags()`
- `interpreter_name()`
- `interpreter_version(*, warn: bool = False)`
- `_version_nodot(version: PythonVersion)`
- `sys_tags(*, warn: bool = False)`
- `create_compatible_tags_selector(
    tags: Iterable[Tag],
)`
- `selector(
        tagged_things: Iterable[tuple[_T, AbstractSet[Tag]]],
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/utils.py`

#### Classes
- `InvalidName`
- `InvalidWheelFilename`
- `InvalidSdistFilename`

#### Functions
- `__dir__()`
- `canonicalize_name(name: str, *, validate: bool = False)`
- `is_normalized_name(name: str)`
- `canonicalize_version(
    version: Version | str, *, strip_trailing_zero: bool = True
)`
- `parse_wheel_filename(
    filename: str,
    *,
    validate_order: bool = False,
)`
- `parse_sdist_filename(filename: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/packaging/version.py`

#### Classes
- `_VersionReplace`
- `InvalidVersion`
- `_BaseVersion`
- `_Version`
- `Version`
- `_TrimmedRelease`

#### Functions
- `_deprecated(message: str)`
- `decorator(func: Callable[[...], object])`
- `wrapper(*args: object, **kwargs: object)`
- `__dir__()`
- `normalize_pre(letter: str, /)`
- `parse(version: str)`
- `_key(self)`
- `__hash__(self)`
- `__lt__(self, other: _BaseVersion)`
- `__le__(self, other: _BaseVersion)`
- `__eq__(self, other: object)`
- `__ge__(self, other: _BaseVersion)`
- `__gt__(self, other: _BaseVersion)`
- `__ne__(self, other: object)`
- `_validate_epoch(value: object, /)`
- `_validate_release(value: object, /)`
- `_validate_pre(value: object, /)`
- `_validate_post(value: object, /)`
- `_validate_dev(value: object, /)`
- `_validate_local(value: object, /)`
- `__init__(self, version: str)`
- `from_parts(
        cls,
        *,
        epoch: int = 0,
        release: tuple[int, ...],
        pre: tuple[str, int] | None = None,
        post: int | None = None,
        dev: int | None = None,
        local: str | None = None,
    )`
- `__replace__(self, **kwargs: Unpack[_VersionReplace])`
- `_key(self)`
- `__hash__(self)`
- `__lt__(self, other: _BaseVersion)`
- `__le__(self, other: _BaseVersion)`
- `__eq__(self, other: object)`
- `__ge__(self, other: _BaseVersion)`
- `__gt__(self, other: _BaseVersion)`
- `__ne__(self, other: object)`
- `__getstate__(
        self,
    )`
- `__setstate__(self, state: object)`
- `_version(self)`
- `_version(self, value: _Version)`
- `__repr__(self)`
- `__str__(self)`
- `_str(self)`
- `epoch(self)`
- `release(self)`
- `pre(self)`
- `post(self)`
- `dev(self)`
- `local(self)`
- `public(self)`
- `base_version(self)`
- `is_prerelease(self)`
- `is_postrelease(self)`
- `is_devrelease(self)`
- `major(self)`
- `minor(self)`
- `micro(self)`
- `__init__(self, version: str | Version)`
- `release(self)`
- `_parse_letter_version(
    letter: str | None, number: str | bytes | SupportsInt | None
)`
- `_parse_local_version(local: str | None)`
- `_cmpkey(
    epoch: int,
    release: tuple[int, ...],
    pre: tuple[str, int] | None,
    post: tuple[str, int] | None,
    dev: tuple[str, int] | None,
    local: LocalType | None,
)`

#### Parameters / Constants
- `VERSION_PATTERN` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pkg_resources/__init__.py`

#### Classes
- `_LoaderProtocol`
- `_ZipLoaderModule`
- `PEP440Warning`
- `ResolutionError`
- `VersionConflict`
- `ContextualVersionConflict`
- `DistributionNotFound`
- `UnknownExtra`
- `IMetadataProvider`
- `IResourceProvider`
- `WorkingSet`
- `_ReqExtras`
- `Environment`
- `ExtractionError`
- `ResourceManager`
- `NullProvider`
- `EggProvider`
- `DefaultProvider`
- `EmptyProvider`
- `ZipManifests`
- `MemoizedZipManifests`
- `manifest_mod`
- `ZipProvider`
- `FileMetadata`
- `PathMetadata`
- `EggMetadata`
- `NoDists`
- `EntryPoint`
- `Distribution`
- `EggInfoDistribution`
- `DistInfoDistribution`
- `RequirementParseError`
- `Requirement`
- `PkgResourcesDeprecationWarning`

#### Functions
- `load_module(self, fullname: str, /)`
- `_declare_state(vartype: str, varname: str, initial_value: _T)`
- `__getstate__()`
- `__setstate__(state: dict[str, Any])`
- `_sget_dict(val)`
- `_sset_dict(key, ob, state)`
- `_sget_object(val)`
- `_sset_object(key, ob, state)`
- `get_supported_platform()`
- `__repr__(self)`
- `dist(self)`
- `req(self)`
- `report(self)`
- `with_context(self, required_by: set[Distribution | str])`
- `required_by(self)`
- `req(self)`
- `requirers(self)`
- `requirers_str(self)`
- `report(self)`
- `__str__(self)`
- `register_loader_type(
    loader_type: type[_ModuleLike], provider_factory: _ProviderFactoryType
)`
- `get_provider(moduleOrReq: str)`
- `get_provider(moduleOrReq: Requirement)`
- `get_provider(moduleOrReq: str | Requirement)`
- `_macos_vers()`
- `_macos_arch(machine)`
- `get_build_platform()`
- `compatible_platforms(provided: str | None, required: str | None)`
- `get_distribution(dist: _DistributionT)`
- `get_distribution(dist: _PkgReqType)`
- `get_distribution(dist: Distribution | _PkgReqType)`
- `load_entry_point(dist: _EPDistType, group: str, name: str)`
- `get_entry_map(
    dist: _EPDistType, group: None = None
)`
- `get_entry_map(dist: _EPDistType, group: str)`
- `get_entry_map(dist: _EPDistType, group: str | None = None)`
- `get_entry_info(dist: _EPDistType, group: str, name: str)`
- `has_metadata(self, name: str)`
- `get_metadata(self, name: str)`
- `get_metadata_lines(self, name: str)`
- `metadata_isdir(self, name: str)`
- `metadata_listdir(self, name: str)`
- `run_script(self, script_name: str, namespace: dict[str, Any])`
- `get_resource_filename(
        self, manager: ResourceManager, resource_name: str
    )`
- `get_resource_stream(
        self, manager: ResourceManager, resource_name: str
    )`
- `get_resource_string(
        self, manager: ResourceManager, resource_name: str
    )`
- `has_resource(self, resource_name: str)`
- `resource_isdir(self, resource_name: str)`
- `resource_listdir(self, resource_name: str)`
- `__init__(self, entries: Iterable[str] | None = None)`
- `_build_master(cls)`
- `_build_from_requirements(cls, req_spec)`
- `add_entry(self, entry: str)`
- `__contains__(self, dist: Distribution)`
- `find(self, req: Requirement)`
- `iter_entry_points(self, group: str, name: str | None = None)`
- `run_script(self, requires: str, script_name: str)`
- `__iter__(self)`
- `add(
        self,
        dist: Distribution,
        entry: str | None = None,
        insert: bool = True,
        replace: bool = False,
    )`
- `resolve(
        self,
        requirements: Iterable[Requirement],
        env: Environment | None,
        installer: _InstallerTypeT[_DistributionT],
        replace_conflicting: bool = False,
        extras: tuple[str, ...] | None = None,
    )`
- `resolve(
        self,
        requirements: Iterable[Requirement],
        env: Environment | None = None,
        *,
        installer: _InstallerTypeT[_DistributionT],
        replace_conflicting: bool = False,
        extras: tuple[str, ...] | None = None,
    )`
- `resolve(
        self,
        requirements: Iterable[Requirement],
        env: Environment | None = None,
        installer: _InstallerType | None = None,
        replace_conflicting: bool = False,
        extras: tuple[str, ...] | None = None,
    )`
- `resolve(
        self,
        requirements: Iterable[Requirement],
        env: Environment | None = None,
        installer: _InstallerType | None | _InstallerTypeT[_DistributionT] = None,
        replace_conflicting: bool = False,
        extras: tuple[str, ...] | None = None,
    )`
- `_resolve_dist(
        self, req, best, replace_conflicting, env, installer, required_by, to_activate
    )`
- `find_plugins(
        self,
        plugin_env: Environment,
        full_env: Environment | None,
        installer: _InstallerTypeT[_DistributionT],
        fallback: bool = True,
    )`
- `find_plugins(
        self,
        plugin_env: Environment,
        full_env: Environment | None = None,
        *,
        installer: _InstallerTypeT[_DistributionT],
        fallback: bool = True,
    )`
- `find_plugins(
        self,
        plugin_env: Environment,
        full_env: Environment | None = None,
        installer: _InstallerType | None = None,
        fallback: bool = True,
    )`
- `find_plugins(
        self,
        plugin_env: Environment,
        full_env: Environment | None = None,
        installer: _InstallerType | None | _InstallerTypeT[_DistributionT] = None,
        fallback: bool = True,
    )`
- `require(self, *requirements: _NestedStr)`
- `subscribe(
        self, callback: Callable[[Distribution], object], existing: bool = True
    )`
- `_added_new(self, dist)`
- `__getstate__(self)`
- `__setstate__(self, e_k_b_n_c)`
- `markers_pass(self, req: Requirement, extras: tuple[str, ...] | None = None)`
- `__init__(
        self,
        search_path: Iterable[str] | None = None,
        platform: str | None = get_supported_platform()`
- `can_add(self, dist: Distribution)`
- `remove(self, dist: Distribution)`
- `scan(self, search_path: Iterable[str] | None = None)`
- `__getitem__(self, project_name: str)`
- `add(self, dist: Distribution)`
- `best_match(
        self,
        req: Requirement,
        working_set: WorkingSet,
        installer: _InstallerTypeT[_DistributionT],
        replace_conflicting: bool = False,
    )`
- `best_match(
        self,
        req: Requirement,
        working_set: WorkingSet,
        installer: _InstallerType | None = None,
        replace_conflicting: bool = False,
    )`
- `best_match(
        self,
        req: Requirement,
        working_set: WorkingSet,
        installer: _InstallerType | None | _InstallerTypeT[_DistributionT] = None,
        replace_conflicting: bool = False,
    )`
- `obtain(
        self,
        requirement: Requirement,
        installer: _InstallerTypeT[_DistributionT],
    )`
- `obtain(
        self,
        requirement: Requirement,
        installer: Callable[[Requirement], None] | None = None,
    )`
- `obtain(
        self,
        requirement: Requirement,
        installer: _InstallerType | None = None,
    )`
- `obtain(
        self,
        requirement: Requirement,
        installer: Callable[[Requirement], None]
        | _InstallerType
        | None
        | _InstallerTypeT[_DistributionT] = None,
    )`
- `__iter__(self)`
- `__iadd__(self, other: Distribution | Environment)`
- `__add__(self, other: Distribution | Environment)`
- `__init__(self)`
- `resource_exists(self, package_or_requirement: _PkgReqType, resource_name: str)`
- `resource_isdir(self, package_or_requirement: _PkgReqType, resource_name: str)`
- `resource_filename(
        self, package_or_requirement: _PkgReqType, resource_name: str
    )`
- `resource_stream(self, package_or_requirement: _PkgReqType, resource_name: str)`
- `resource_string(
        self, package_or_requirement: _PkgReqType, resource_name: str
    )`
- `resource_listdir(self, package_or_requirement: _PkgReqType, resource_name: str)`
- `extraction_error(self)`
- `get_cache_path(self, archive_name: str, names: Iterable[StrPath] = ()`
- `_warn_unsafe_extraction_path(path)`
- `postprocess(self, tempname: StrOrBytesPath, filename: StrOrBytesPath)`
- `set_extraction_path(self, path: str)`
- `cleanup_resources(self, force: bool = False)`
- `get_default_cache()`
- `safe_name(name: str)`
- `safe_version(version: str)`
- `_forgiving_version(version)`
- `_safe_segment(segment)`
- `safe_extra(extra: str)`
- `to_filename(name: str)`
- `invalid_marker(text: str)`
- `evaluate_marker(text: str, extra: str | None = None)`
- `__init__(self, module: _ModuleLike)`
- `get_resource_filename(self, manager: ResourceManager, resource_name: str)`
- `get_resource_stream(self, manager: ResourceManager, resource_name: str)`
- `get_resource_string(
        self, manager: ResourceManager, resource_name: str
    )`
- `has_resource(self, resource_name: str)`
- `_get_metadata_path(self, name)`
- `has_metadata(self, name: str)`
- `get_metadata(self, name: str)`
- `get_metadata_lines(self, name: str)`
- `resource_isdir(self, resource_name: str)`
- `metadata_isdir(self, name: str)`
- `resource_listdir(self, resource_name: str)`
- `metadata_listdir(self, name: str)`
- `run_script(self, script_name: str, namespace: dict[str, Any])`
- `_has(self, path)`
- `_isdir(self, path)`
- `_listdir(self, path)`
- `_fn(self, base: str | None, resource_name: str)`
- `_validate_resource_path(path)`
- `_get(self, path)`
- `_parents(path)`
- `__init__(self, module: _ModuleLike)`
- `_setup_prefix(self)`
- `_set_egg(self, path: str)`
- `_has(self, path)`
- `_isdir(self, path)`
- `_listdir(self, path)`
- `get_resource_stream(self, manager: object, resource_name: str)`
- `_get(self, path)`
- `_register(cls)`
- `_get(self, path)`
- `_listdir(self, path)`
- `__init__(self)`
- `build(cls, path: str)`
- `load(self, path: str)`
- `__init__(self, module: _ZipLoaderModule)`
- `_zipinfo_name(self, fspath)`
- `_parts(self, zip_path)`
- `zipinfo(self)`
- `get_resource_filename(self, manager: ResourceManager, resource_name: str)`
- `_get_date_and_size(zip_stat)`
- `_extract_resource(self, manager: ResourceManager, zip_path)`
- `_is_current(self, file_path, zip_path)`
- `_get_eager_resources(self)`
- `_index(self)`
- `_has(self, fspath)`
- `_isdir(self, fspath)`
- `_listdir(self, fspath)`
- `_eager_to_zip(self, resource_name: str)`
- `_resource_to_zip(self, resource_name: str)`
- `__init__(self, path: StrPath)`
- `_get_metadata_path(self, name)`
- `has_metadata(self, name: str)`
- `get_metadata(self, name: str)`
- `_warn_on_replacement(self, metadata)`
- `get_metadata_lines(self, name: str)`
- `__init__(self, path: str, egg_info: str)`
- `__init__(self, importer: zipimport.zipimporter)`
- `register_finder(importer_type: type[_T], distribution_finder: _DistFinderType[_T])`
- `find_distributions(path_item: str, only: bool = False)`
- `find_eggs_in_zip(
    importer: zipimport.zipimporter, path_item: str, only: bool = False
)`
- `find_nothing(
    importer: object | None, path_item: str | None, only: bool | None = False
)`
- `find_on_path(importer: object | None, path_item, only=False)`
- `dist_factory(path_item, entry, only)`
- `__bool__(self)`
- `__call__(self, fullpath)`
- `safe_listdir(path: StrOrBytesPath)`
- `distributions_from_metadata(path: str)`
- `non_empty_lines(path)`
- `resolve_egg_link(path)`
- `register_namespace_handler(
    importer_type: type[_T], namespace_handler: _NSHandlerType[_T]
)`
- `namespace_handler(importer, path_entry, moduleName, module)`
- `_handle_ns(packageName, path_item)`
- `_rebuild_mod_path(orig_path, package_name, module: types.ModuleType)`
- `safe_sys_path_index(entry)`
- `position_in_sys_path(path)`
- `declare_namespace(packageName: str)`
- `fixup_namespace_packages(path_item: str, parent: str | None = None)`
- `file_ns_handler(
    importer: object,
    path_item: StrPath,
    packageName: str,
    module: types.ModuleType,
)`
- `null_ns_handler(
    importer: object,
    path_item: str | None,
    packageName: str | None,
    module: _ModuleLike | None,
)`
- `normalize_path(filename: StrPath)`
- `normalize_path(filename: BytesPath)`
- `normalize_path(filename: StrOrBytesPath)`
- `_cygwin_patch(filename: StrOrBytesPath)`
- `_normalize_cached(filename: StrPath)`
- `_normalize_cached(filename: BytesPath)`
- `_normalize_cached(filename: StrOrBytesPath)`
- `_normalize_cached(filename)`
- `_is_egg_path(path)`
- `_is_zip_egg(path)`
- `_is_unpacked_egg(path)`
- `_set_parent_ns(packageName)`
- `__init__(
        self,
        name: str,
        module_name: str,
        attrs: Iterable[str] = ()`
- `__str__(self)`
- `__repr__(self)`
- `load(
        self,
        require: Literal[True] = True,
        env: Environment | None = None,
        installer: _InstallerType | None = None,
    )`
- `load(
        self,
        require: Literal[False],
        *args: Any,
        **kwargs: Any,
    )`
- `load(
        self,
        require: bool = True,
        *args: Environment | _InstallerType | None,
        **kwargs: Environment | _InstallerType | None,
    )`
- `resolve(self)`
- `require(
        self,
        env: Environment | None = None,
        installer: _InstallerType | None = None,
    )`
- `parse(cls, src: str, dist: Distribution | None = None)`
- `_parse_extras(cls, extras_spec)`
- `parse_group(
        cls,
        group: str,
        lines: _NestedStr,
        dist: Distribution | None = None,
    )`
- `parse_map(
        cls,
        data: str | Iterable[str] | dict[str, str | Iterable[str]],
        dist: Distribution | None = None,
    )`
- `_version_from_file(lines)`
- `is_version_line(line)`
- `__init__(
        self,
        location: str | None = None,
        metadata: _MetadataType = None,
        project_name: str | None = None,
        version: str | None = None,
        py_version: str | None = PY_MAJOR,
        platform: str | None = None,
        precedence: int = EGG_DIST,
    )`
- `from_location(
        cls,
        location: str,
        basename: StrPath,
        metadata: _MetadataType = None,
        **kw: int,  # We could set `precedence` explicitly, but keeping this as `**kw` for full backwards and subclassing compatibility
    )`
- `_reload_version(self)`
- `hashcmp(self)`
- `__hash__(self)`
- `__lt__(self, other: Distribution)`
- `__le__(self, other: Distribution)`
- `__gt__(self, other: Distribution)`
- `__ge__(self, other: Distribution)`
- `__eq__(self, other: object)`
- `__ne__(self, other: object)`
- `key(self)`
- `parsed_version(self)`
- `_forgiving_parsed_version(self)`
- `version(self)`
- `_dep_map(self)`
- `_filter_extras(dm: dict[str | None, list[Requirement]])`
- `_build_dep_map(self)`
- `requires(self, extras: Iterable[str] = ()`
- `_get_metadata_path_for_display(self, name)`
- `_get_metadata(self, name)`
- `_get_version(self)`
- `activate(self, path: list[str] | None = None, replace: bool = False)`
- `egg_name(self)`
- `__repr__(self)`
- `__str__(self)`
- `__getattr__(self, attr)`
- `__dir__(self)`
- `from_filename(
        cls,
        filename: StrPath,
        metadata: _MetadataType = None,
        **kw: int,  # We could set `precedence` explicitly, but keeping this as `**kw` for full backwards and subclassing compatibility
    )`
- `as_requirement(self)`
- `load_entry_point(self, group: str, name: str)`
- `get_entry_map(self, group: None = None)`
- `get_entry_map(self, group: str)`
- `get_entry_map(self, group: str | None = None)`
- `get_entry_info(self, group: str, name: str)`
- `insert_on(  # noqa: C901
        self,
        path: list[str],
        loc=None,
        replace: bool = False,
    )`
- `check_version_conflict(self)`
- `has_version(self)`
- `clone(self, **kw: str | int | IResourceProvider | None)`
- `extras(self)`
- `_reload_version(self)`
- `_parsed_pkg_info(self)`
- `_dep_map(self)`
- `_compute_dependencies(self)`
- `reqs_for_extra(extra)`
- `issue_warning(*args, **kw)`
- `parse_requirements(strs: _NestedStr)`
- `__init__(self, requirement_string: str)`
- `__eq__(self, other: object)`
- `__ne__(self, other)`
- `__contains__(self, item: Distribution | str | tuple[str, ...])`
- `__hash__(self)`
- `__repr__(self)`
- `parse(s: str | Iterable[str])`
- `_always_object(classes)`
- `_find_adapter(registry: Mapping[type, _AdapterT], ob: object)`
- `ensure_directory(path: StrOrBytesPath)`
- `_bypass_ensure_directory(path)`
- `split_sections(s: _NestedStr)`
- `_mkstemp(*args, **kw)`
- `_read_utf8_with_fallback(file: str, fallback_encoding=_LOCALE_ENCODING)`
- `_call_aside(f, *args, **kwargs)`
- `_initialize(g=globals()`
- `_initialize_master_working_set()`

#### Parameters / Constants
- `WRITE_SUPPORT` = `True`
- `WRITE_SUPPORT` = `False`
- `PY_MAJOR` = `'{}.{}'.format(*sys.version_info)`
- `EGG_DIST` = `3`
- `BINARY_DIST` = `2`
- `SOURCE_DIST` = `1`
- `CHECKOUT_DIST` = `0`
- `DEVELOP_DIST` = `-1`
- `MODULE` = `re.compile(r"\w+(\.\w+)*$").match`
- `EGG_NAME` = `re.compile(`
- `PKG_INFO` = `'PKG-INFO'`
- `PKG_INFO` = `'METADATA'`
- `EQEQ` = `re.compile(r"([\(,])\s*(\d.*?)\s*([,\)])")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/__init__.py`

#### Functions
- `_set_platform_dir_class()`
- `user_data_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    roaming: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_data_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    multipath: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_config_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    roaming: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_config_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    multipath: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_cache_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_cache_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_state_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    roaming: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_log_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_documents_dir()`
- `user_downloads_dir()`
- `user_pictures_dir()`
- `user_videos_dir()`
- `user_music_dir()`
- `user_desktop_dir()`
- `user_runtime_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_runtime_dir(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_data_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    roaming: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_data_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    multipath: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_config_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    roaming: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_config_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    multipath: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_cache_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_cache_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_state_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    roaming: bool = False,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_log_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `user_documents_path()`
- `user_downloads_path()`
- `user_pictures_path()`
- `user_videos_path()`
- `user_music_path()`
- `user_desktop_path()`
- `user_runtime_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`
- `site_runtime_path(
    appname: str | None = None,
    appauthor: str | Literal[False] | None = None,
    version: str | None = None,
    opinion: bool = True,  # noqa: FBT001, FBT002
    ensure_exists: bool = False,  # noqa: FBT001, FBT002
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/__main__.py`

#### Functions
- `main()`

#### Parameters / Constants
- `PROPS` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/android.py`

#### Classes
- `Android`

#### Functions
- `user_data_dir(self)`
- `site_data_dir(self)`
- `user_config_dir(self)`
- `site_config_dir(self)`
- `user_cache_dir(self)`
- `site_cache_dir(self)`
- `user_state_dir(self)`
- `user_log_dir(self)`
- `user_documents_dir(self)`
- `user_downloads_dir(self)`
- `user_pictures_dir(self)`
- `user_videos_dir(self)`
- `user_music_dir(self)`
- `user_desktop_dir(self)`
- `user_runtime_dir(self)`
- `site_runtime_dir(self)`
- `_android_folder()`
- `_android_documents_folder()`
- `_android_downloads_folder()`
- `_android_pictures_folder()`
- `_android_videos_folder()`
- `_android_music_folder()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/api.py`

#### Classes
- `PlatformDirsABC`

#### Functions
- `__init__(  # noqa: PLR0913, PLR0917
        self,
        appname: str | None = None,
        appauthor: str | Literal[False] | None = None,
        version: str | None = None,
        roaming: bool = False,  # noqa: FBT001, FBT002
        multipath: bool = False,  # noqa: FBT001, FBT002
        opinion: bool = True,  # noqa: FBT001, FBT002
        ensure_exists: bool = False,  # noqa: FBT001, FBT002
    )`
- `_append_app_name_and_version(self, *base: str)`
- `_optionally_create_directory(self, path: str)`
- `_first_item_as_path_if_multipath(self, directory: str)`
- `user_data_dir(self)`
- `site_data_dir(self)`
- `user_config_dir(self)`
- `site_config_dir(self)`
- `user_cache_dir(self)`
- `site_cache_dir(self)`
- `user_state_dir(self)`
- `user_log_dir(self)`
- `user_documents_dir(self)`
- `user_downloads_dir(self)`
- `user_pictures_dir(self)`
- `user_videos_dir(self)`
- `user_music_dir(self)`
- `user_desktop_dir(self)`
- `user_runtime_dir(self)`
- `site_runtime_dir(self)`
- `user_data_path(self)`
- `site_data_path(self)`
- `user_config_path(self)`
- `site_config_path(self)`
- `user_cache_path(self)`
- `site_cache_path(self)`
- `user_state_path(self)`
- `user_log_path(self)`
- `user_documents_path(self)`
- `user_downloads_path(self)`
- `user_pictures_path(self)`
- `user_videos_path(self)`
- `user_music_path(self)`
- `user_desktop_path(self)`
- `user_runtime_path(self)`
- `site_runtime_path(self)`
- `iter_config_dirs(self)`
- `iter_data_dirs(self)`
- `iter_cache_dirs(self)`
- `iter_runtime_dirs(self)`
- `iter_config_paths(self)`
- `iter_data_paths(self)`
- `iter_cache_paths(self)`
- `iter_runtime_paths(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/macos.py`

#### Classes
- `MacOS`

#### Functions
- `user_data_dir(self)`
- `site_data_dir(self)`
- `site_data_path(self)`
- `user_config_dir(self)`
- `site_config_dir(self)`
- `user_cache_dir(self)`
- `site_cache_dir(self)`
- `site_cache_path(self)`
- `user_state_dir(self)`
- `user_log_dir(self)`
- `user_documents_dir(self)`
- `user_downloads_dir(self)`
- `user_pictures_dir(self)`
- `user_videos_dir(self)`
- `user_music_dir(self)`
- `user_desktop_dir(self)`
- `user_runtime_dir(self)`
- `site_runtime_dir(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/unix.py`

#### Classes
- `Unix`

#### Functions
- `getuid()`
- `user_data_dir(self)`
- `_site_data_dirs(self)`
- `site_data_dir(self)`
- `user_config_dir(self)`
- `_site_config_dirs(self)`
- `site_config_dir(self)`
- `user_cache_dir(self)`
- `site_cache_dir(self)`
- `user_state_dir(self)`
- `user_log_dir(self)`
- `user_documents_dir(self)`
- `user_downloads_dir(self)`
- `user_pictures_dir(self)`
- `user_videos_dir(self)`
- `user_music_dir(self)`
- `user_desktop_dir(self)`
- `user_runtime_dir(self)`
- `site_runtime_dir(self)`
- `site_data_path(self)`
- `site_config_path(self)`
- `site_cache_path(self)`
- `iter_config_dirs(self)`
- `iter_data_dirs(self)`
- `_get_user_media_dir(env_var: str, fallback_tilde_path: str)`
- `_get_user_dirs_folder(key: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/version.py`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`
- `VERSION_TUPLE` = `Tuple[Union[int, str], ...]`
- `COMMIT_ID` = `Union[str, None]`
- `VERSION_TUPLE` = `object`
- `COMMIT_ID` = `object`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/platformdirs/windows.py`

#### Classes
- `Windows`

#### Functions
- `user_data_dir(self)`
- `_append_parts(self, path: str, *, opinion_value: str | None = None)`
- `site_data_dir(self)`
- `user_config_dir(self)`
- `site_config_dir(self)`
- `user_cache_dir(self)`
- `site_cache_dir(self)`
- `user_state_dir(self)`
- `user_log_dir(self)`
- `user_documents_dir(self)`
- `user_downloads_dir(self)`
- `user_pictures_dir(self)`
- `user_videos_dir(self)`
- `user_music_dir(self)`
- `user_desktop_dir(self)`
- `user_runtime_dir(self)`
- `site_runtime_dir(self)`
- `get_win_folder_from_env_vars(csidl_name: str)`
- `get_win_folder_if_csidl_name_not_env_var(csidl_name: str)`
- `get_win_folder_from_registry(csidl_name: str)`
- `get_win_folder_via_ctypes(csidl_name: str)`
- `_pick_get_win_folder()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/__init__.py`

#### Functions
- `lex(code, lexer)`
- `format(tokens, formatter, outfile=None)`
- `highlight(code, lexer, formatter, outfile=None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/console.py`

#### Functions
- `reset_color()`
- `colorize(color_key, text)`
- `ansiformat(attr, text)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/filter.py`

#### Classes
- `Filter`
- `FunctionFilter`

#### Functions
- `apply_filters(stream, filters, lexer=None)`
- `_apply(filter_, stream)`
- `simplefilter(f)`
- `lowercase(self, lexer, stream, options)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/filters/__init__.py`

#### Classes
- `CodeTagFilter`
- `SymbolFilter`
- `KeywordCaseFilter`
- `NameHighlightFilter`
- `ErrorToken`
- `RaiseOnErrorTokenFilter`
- `VisibleWhitespaceFilter`
- `GobbleFilter`
- `TokenMergeFilter`

#### Functions
- `find_filter_class(filtername)`
- `get_filter_by_name(filtername, **options)`
- `get_all_filters()`
- `_replace_special(ttype, value, regex, specialttype,
                     replacefunc=lambda x: x)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`
- `replacefunc(wschar)`
- `__init__(self, **options)`
- `gobble(self, value, left)`
- `filter(self, lexer, stream)`
- `__init__(self, **options)`
- `filter(self, lexer, stream)`

#### Parameters / Constants
- `FILTERS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/formatter.py`

#### Classes
- `Formatter`

#### Functions
- `_lookup_style(style)`
- `__init__(self, **options)`
- `get_style_defs(self, arg='')`
- `format(self, tokensource, outfile)`
- `__class_getitem__(cls, name)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/formatters/__init__.py`

#### Classes
- `_automodule`

#### Functions
- `_fn_matches(fn, glob)`
- `_load_formatters(module_name)`
- `get_all_formatters()`
- `find_formatter_class(alias)`
- `get_formatter_by_name(_alias, **options)`
- `load_formatter_from_file(filename, formattername="CustomFormatter", **options)`
- `get_formatter_for_filename(fn, **options)`
- `__getattr__(self, name)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/formatters/_mapping.py`

#### Parameters / Constants
- `FORMATTERS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexer.py`

#### Classes
- `LexerMeta`
- `Lexer`
- `DelegatingLexer`
- `include`
- `_inherit`
- `combined`
- `_PseudoMatch`
- `_This`
- `default`
- `words`
- `RegexLexerMeta`
- `RegexLexer`
- `LexerContext`
- `ExtendedRegexLexer`
- `ProfilingRegexLexerMeta`
- `ProfilingRegexLexer`

#### Functions
- `__new__(mcs, name, bases, d)`
- `__init__(self, **options)`
- `__init__(self, **options)`
- `__repr__(self)`
- `add_filter(self, filter_, **options)`
- `analyse_text(text)`
- `_preprocess_lexer_input(self, text)`
- `get_tokens(self, text, unfiltered=False)`
- `streamer()`
- `get_tokens_unprocessed(self, text)`
- `__init__(self, _root_lexer, _language_lexer, _needle=Other, **options)`
- `get_tokens_unprocessed(self, text)`
- `__repr__(self)`
- `__new__(cls, *args)`
- `__init__(self, *args)`
- `__init__(self, start, text)`
- `start(self, arg=None)`
- `end(self, arg=None)`
- `group(self, arg=None)`
- `groups(self)`
- `groupdict(self)`
- `bygroups(*args)`
- `callback(lexer, match, ctx=None)`
- `using(_other, **kwargs)`
- `callback(lexer, match, ctx=None)`
- `callback(lexer, match, ctx=None)`
- `__init__(self, state)`
- `__init__(self, words, prefix='', suffix='')`
- `get(self)`
- `_process_regex(cls, regex, rflags, state)`
- `_process_token(cls, token)`
- `_process_new_state(cls, new_state, unprocessed, processed)`
- `_process_state(cls, unprocessed, processed, state)`
- `process_tokendef(cls, name, tokendefs=None)`
- `get_tokendefs(cls)`
- `__call__(cls, *args, **kwds)`
- `get_tokens_unprocessed(self, text, stack=('root',)`
- `__init__(self, text, pos, stack=None, end=None)`
- `__repr__(self)`
- `get_tokens_unprocessed(self, text=None, context=None)`
- `do_insertions(insertions, tokens)`
- `_process_regex(cls, regex, rflags, state)`
- `match_func(text, pos, endpos=sys.maxsize)`
- `get_tokens_unprocessed(self, text, stack=('root',)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexers/__init__.py`

#### Classes
- `is`
- `_automodule`

#### Functions
- `_fn_matches(fn, glob)`
- `_load_lexers(module_name)`
- `get_all_lexers(plugins=True)`
- `find_lexer_class(name)`
- `find_lexer_class_by_name(_alias)`
- `get_lexer_by_name(_alias, **options)`
- `load_lexer_from_file(filename, lexername="CustomLexer", **options)`
- `find_lexer_class_for_filename(_fn, code=None)`
- `get_rating(info)`
- `get_lexer_for_filename(_fn, code=None, **options)`
- `get_lexer_for_mimetype(_mime, **options)`
- `_iter_lexerclasses(plugins=True)`
- `guess_lexer_for_filename(_fn, _text, **options)`
- `type_sort(t)`
- `guess_lexer(_text, **options)`
- `__getattr__(self, name)`

#### Parameters / Constants
- `COMPAT` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexers/_mapping.py`

#### Parameters / Constants
- `LEXERS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/lexers/python.py`

#### Classes
- `PythonLexer`
- `Python2Lexer`
- `_PythonConsoleLexerBase`
- `PythonConsoleLexer`
- `_ReplaceInnerCode`
- `PythonTracebackLexer`
- `Python2TracebackLexer`
- `CythonLexer`
- `DgLexer`
- `NumPyLexer`

#### Functions
- `innerstring_rules(ttype)`
- `fstring_rules(ttype)`
- `analyse_text(text)`
- `innerstring_rules(ttype)`
- `analyse_text(text)`
- `__init__(self, **options)`
- `__init__(self, **options)`
- `get_tokens_unprocessed(self, text)`
- `analyse_text(text)`

#### Parameters / Constants
- `EXTRA_KEYWORDS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/modeline.py`

#### Functions
- `get_filetype_from_line(l)`
- `get_filetype_from_buffer(buf, max_lines=5)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/plugin.py`

#### Functions
- `iter_entry_points(group_name)`
- `find_plugin_lexers()`
- `find_plugin_formatters()`
- `find_plugin_styles()`
- `find_plugin_filters()`

#### Parameters / Constants
- `LEXER_ENTRY_POINT` = `'pygments.lexers'`
- `FORMATTER_ENTRY_POINT` = `'pygments.formatters'`
- `STYLE_ENTRY_POINT` = `'pygments.styles'`
- `FILTER_ENTRY_POINT` = `'pygments.filters'`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/regexopt.py`

#### Functions
- `make_charset(letters)`
- `regex_opt_inner(strings, open_paren)`
- `regex_opt(strings, prefix='', suffix='')`

#### Parameters / Constants
- `CS_ESCAPE` = `re.compile(r'[\[\^\\\-\]]')`
- `FIRST_ELEMENT` = `itemgetter(0)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/scanner.py`

#### Classes
- `EndOfText`
- `Scanner`

#### Functions
- `__init__(self, text, flags=0)`
- `eos(self)`
- `check(self, pattern)`
- `test(self, pattern)`
- `scan(self, pattern)`
- `get_char(self)`
- `__repr__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/sphinxext.py`

#### Classes
- `PygmentsDoc`

#### Functions
- `run(self)`
- `document_lexers_overview(self)`
- `format_link(name, url)`
- `write_row(*columns)`
- `write_seperator()`
- `document_lexers(self)`
- `document_formatters(self)`
- `document_filters(self)`
- `setup(app)`

#### Parameters / Constants
- `MODULEDOC` = `'''`
- `LEXERDOC` = `'''`
- `FMTERDOC` = `'''`
- `FILTERDOC` = `'''`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/style.py`

#### Classes
- `StyleMeta`
- `Style`

#### Functions
- `__new__(mcs, name, bases, dct)`
- `colorformat(text)`
- `style_for_token(cls, token)`
- `list_styles(cls)`
- `styles_token(cls, ttype)`
- `__iter__(cls)`
- `__len__(cls)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/styles/__init__.py`

#### Functions
- `get_style_by_name(name)`
- `get_all_styles()`

#### Parameters / Constants
- `STYLE_MAP` = `{v[1]: v[0].split('.')[-1] + '::' + k for k, v in STYLES.items()}`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/styles/_mapping.py`

#### Parameters / Constants
- `STYLES` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/token.py`

#### Classes
- `_TokenType`

#### Functions
- `split(self)`
- `__init__(self, *args)`
- `__contains__(self, val)`
- `__getattr__(self, val)`
- `__repr__(self)`
- `__copy__(self)`
- `__deepcopy__(self, memo)`
- `is_token_subtype(ttype, other)`
- `string_to_tokentype(s)`

#### Parameters / Constants
- `STANDARD_TYPES` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/unistring.py`

#### Functions
- `combine(*args)`
- `allexcept(*args)`
- `_handle_runs(char_list)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pygments/util.py`

#### Classes
- `ClassNotFound`
- `OptionError`
- `Future`
- `UnclosingTextIOWrapper`

#### Functions
- `get_choice_opt(options, optname, allowed, default=None, normcase=False)`
- `get_bool_opt(options, optname, default=None)`
- `get_int_opt(options, optname, default=None)`
- `get_list_opt(options, optname, default=None)`
- `docstring_headline(obj)`
- `make_analysator(f)`
- `text_analyse(text)`
- `shebang_matches(text, regex)`
- `doctype_matches(text, regex)`
- `html_doctype_matches(text)`
- `looks_like_xml(text)`
- `surrogatepair(c)`
- `format_lines(var_name, seq, raw=False, indent_level=0)`
- `duplicates_removed(it, already_seen=()`
- `get(self)`
- `guess_decode(text)`
- `guess_decode_from_terminal(text, term)`
- `terminal_encoding(term)`
- `close(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/_impl.py`

#### Classes
- `SubprocessRunner`
- `BackendUnavailable`
- `HookMissing`
- `UnsupportedOperation`
- `BuildBackendHookCaller`

#### Functions
- `__call__(
            self,
            cmd: Sequence[str],
            cwd: Optional[str] = None,
            extra_environ: Optional[Mapping[str, str]] = None,
        )`
- `write_json(obj: Mapping[str, Any], path: str, **kwargs)`
- `read_json(path: str)`
- `__init__(
        self,
        traceback: str,
        message: Optional[str] = None,
        backend_name: Optional[str] = None,
        backend_path: Optional[Sequence[str]] = None,
    )`
- `__init__(self, hook_name: str)`
- `__init__(self, traceback: str)`
- `default_subprocess_runner(
    cmd: Sequence[str],
    cwd: Optional[str] = None,
    extra_environ: Optional[Mapping[str, str]] = None,
)`
- `quiet_subprocess_runner(
    cmd: Sequence[str],
    cwd: Optional[str] = None,
    extra_environ: Optional[Mapping[str, str]] = None,
)`
- `norm_and_check(source_tree: str, requested: str)`
- `__init__(
        self,
        source_dir: str,
        build_backend: str,
        backend_path: Optional[Sequence[str]] = None,
        runner: Optional["SubprocessRunner"] = None,
        python_executable: Optional[str] = None,
    )`
- `subprocess_runner(self, runner: "SubprocessRunner")`
- `_supported_features(self)`
- `get_requires_for_build_wheel(
        self,
        config_settings: Optional[Mapping[str, Any]] = None,
    )`
- `prepare_metadata_for_build_wheel(
        self,
        metadata_directory: str,
        config_settings: Optional[Mapping[str, Any]] = None,
        _allow_fallback: bool = True,
    )`
- `build_wheel(
        self,
        wheel_directory: str,
        config_settings: Optional[Mapping[str, Any]] = None,
        metadata_directory: Optional[str] = None,
    )`
- `get_requires_for_build_editable(
        self,
        config_settings: Optional[Mapping[str, Any]] = None,
    )`
- `prepare_metadata_for_build_editable(
        self,
        metadata_directory: str,
        config_settings: Optional[Mapping[str, Any]] = None,
        _allow_fallback: bool = True,
    )`
- `build_editable(
        self,
        wheel_directory: str,
        config_settings: Optional[Mapping[str, Any]] = None,
        metadata_directory: Optional[str] = None,
    )`
- `get_requires_for_build_sdist(
        self,
        config_settings: Optional[Mapping[str, Any]] = None,
    )`
- `build_sdist(
        self,
        sdist_directory: str,
        config_settings: Optional[Mapping[str, Any]] = None,
    )`
- `_call_hook(self, hook_name: str, kwargs: Mapping[str, Any])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/_in_process/__init__.py`

#### Functions
- `_in_proc_script_path()`
- `_in_proc_script_path()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py`

#### Classes
- `BackendUnavailable`
- `HookMissing`
- `_BackendPathFinder`
- `_DummyException`
- `GotUnsupportedOperation`

#### Functions
- `write_json(obj, path, **kwargs)`
- `read_json(path)`
- `__init__(self, message, traceback=None)`
- `__init__(self, hook_name=None)`
- `_build_backend()`
- `__init__(self, backend_path, backend_module)`
- `find_spec(self, fullname, _path, _target=None)`
- `find_distributions(self, context=None)`
- `_supported_features()`
- `get_requires_for_build_wheel(config_settings)`
- `get_requires_for_build_editable(config_settings)`
- `prepare_metadata_for_build_wheel(
    metadata_directory, config_settings, _allow_fallback
)`
- `prepare_metadata_for_build_editable(
    metadata_directory, config_settings, _allow_fallback
)`
- `_dist_info_files(whl_zip)`
- `_get_wheel_metadata_from_wheel(whl_basename, metadata_directory, config_settings)`
- `_find_already_built_wheel(metadata_directory)`
- `build_wheel(wheel_directory, config_settings, metadata_directory=None)`
- `build_editable(wheel_directory, config_settings, metadata_directory=None)`
- `get_requires_for_build_sdist(config_settings)`
- `__init__(self, traceback)`
- `build_sdist(sdist_directory, config_settings)`
- `main()`

#### Parameters / Constants
- `WHEEL_BUILT_MARKER` = `"PYPROJECT_HOOKS_ALREADY_BUILT_WHEEL"`
- `HOOK_NAMES` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/__init__.py`

#### Functions
- `check_compatibility(urllib3_version, chardet_version, charset_normalizer_version)`
- `_check_cryptography(cryptography_version)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/_internal_utils.py`

#### Functions
- `to_native_string(string, encoding="ascii")`
- `unicode_is_ascii(u_string)`

#### Parameters / Constants
- `HEADER_VALIDATORS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/adapters.py`

#### Classes
- `BaseAdapter`
- `HTTPAdapter`

#### Functions
- `SOCKSProxyManager(*args, **kwargs)`
- `_urllib3_request_context(
    request: "PreparedRequest",
    verify: "bool | str | None",
    client_cert: "tuple[str, str] | str | None",
    poolmanager: "PoolManager",
)`
- `__init__(self)`
- `send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    )`
- `close(self)`
- `__init__(
        self,
        pool_connections=DEFAULT_POOLSIZE,
        pool_maxsize=DEFAULT_POOLSIZE,
        max_retries=DEFAULT_RETRIES,
        pool_block=DEFAULT_POOLBLOCK,
    )`
- `__getstate__(self)`
- `__setstate__(self, state)`
- `init_poolmanager(
        self, connections, maxsize, block=DEFAULT_POOLBLOCK, **pool_kwargs
    )`
- `proxy_manager_for(self, proxy, **proxy_kwargs)`
- `cert_verify(self, conn, url, verify, cert)`
- `build_response(self, req, resp)`
- `build_connection_pool_key_attributes(self, request, verify, cert=None)`
- `get_connection_with_tls_context(self, request, verify, proxies=None, cert=None)`
- `get_connection(self, url, proxies=None)`
- `close(self)`
- `request_url(self, request, proxies)`
- `add_headers(self, request, **kwargs)`
- `proxy_headers(self, proxy)`
- `send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    )`

#### Parameters / Constants
- `DEFAULT_POOLBLOCK` = `False`
- `DEFAULT_POOLSIZE` = `10`
- `DEFAULT_RETRIES` = `0`
- `DEFAULT_POOL_TIMEOUT` = `None`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/api.py`

#### Functions
- `request(method, url, **kwargs)`
- `get(url, params=None, **kwargs)`
- `options(url, **kwargs)`
- `head(url, **kwargs)`
- `post(url, data=None, json=None, **kwargs)`
- `put(url, data=None, **kwargs)`
- `patch(url, data=None, **kwargs)`
- `delete(url, **kwargs)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/auth.py`

#### Classes
- `AuthBase`
- `HTTPBasicAuth`
- `HTTPProxyAuth`
- `HTTPDigestAuth`

#### Functions
- `_basic_auth_str(username, password)`
- `__call__(self, r)`
- `__init__(self, username, password)`
- `__eq__(self, other)`
- `__ne__(self, other)`
- `__call__(self, r)`
- `__call__(self, r)`
- `__init__(self, username, password)`
- `init_per_thread_state(self)`
- `build_digest_header(self, method, url)`
- `md5_utf8(x)`
- `sha_utf8(x)`
- `sha256_utf8(x)`
- `sha512_utf8(x)`
- `handle_redirect(self, r, **kwargs)`
- `handle_401(self, r, **kwargs)`
- `__call__(self, r)`
- `__eq__(self, other)`
- `__ne__(self, other)`

#### Parameters / Constants
- `CONTENT_TYPE_FORM_URLENCODED` = `"application/x-www-form-urlencoded"`
- `CONTENT_TYPE_MULTI_PART` = `"multipart/form-data"`
- `HA1` = `hash_utf8(A1)`
- `HA2` = `hash_utf8(A2)`
- `HA1` = `hash_utf8(f"{HA1}:{nonce}:{cnonce}")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/compat.py`

#### Functions
- `_resolve_char_detection()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/cookies.py`

#### Classes
- `MockRequest`
- `MockResponse`
- `CookieConflictError`
- `RequestsCookieJar`

#### Functions
- `__init__(self, request)`
- `get_type(self)`
- `get_host(self)`
- `get_origin_req_host(self)`
- `get_full_url(self)`
- `is_unverifiable(self)`
- `has_header(self, name)`
- `get_header(self, name, default=None)`
- `add_header(self, key, val)`
- `add_unredirected_header(self, name, value)`
- `get_new_headers(self)`
- `unverifiable(self)`
- `origin_req_host(self)`
- `host(self)`
- `__init__(self, headers)`
- `info(self)`
- `getheaders(self, name)`
- `extract_cookies_to_jar(jar, request, response)`
- `get_cookie_header(jar, request)`
- `remove_cookie_by_name(cookiejar, name, domain=None, path=None)`
- `get(self, name, default=None, domain=None, path=None)`
- `set(self, name, value, **kwargs)`
- `iterkeys(self)`
- `keys(self)`
- `itervalues(self)`
- `values(self)`
- `iteritems(self)`
- `items(self)`
- `list_domains(self)`
- `list_paths(self)`
- `multiple_domains(self)`
- `get_dict(self, domain=None, path=None)`
- `__contains__(self, name)`
- `__getitem__(self, name)`
- `__setitem__(self, name, value)`
- `__delitem__(self, name)`
- `set_cookie(self, cookie, *args, **kwargs)`
- `update(self, other)`
- `_find(self, name, domain=None, path=None)`
- `_find_no_duplicates(self, name, domain=None, path=None)`
- `__getstate__(self)`
- `__setstate__(self, state)`
- `copy(self)`
- `get_policy(self)`
- `_copy_cookie_jar(jar)`
- `create_cookie(name, value, **kwargs)`
- `morsel_to_cookie(morsel)`
- `cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)`
- `merge_cookies(cookiejar, cookies)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/exceptions.py`

#### Classes
- `RequestException`
- `InvalidJSONError`
- `JSONDecodeError`
- `HTTPError`
- `ConnectionError`
- `ProxyError`
- `SSLError`
- `Timeout`
- `ConnectTimeout`
- `ReadTimeout`
- `URLRequired`
- `TooManyRedirects`
- `MissingSchema`
- `InvalidSchema`
- `InvalidURL`
- `InvalidHeader`
- `InvalidProxyURL`
- `ChunkedEncodingError`
- `ContentDecodingError`
- `StreamConsumedError`
- `RetryError`
- `UnrewindableBodyError`
- `RequestsWarning`
- `FileModeWarning`
- `RequestsDependencyWarning`

#### Functions
- `__init__(self, *args, **kwargs)`
- `__init__(self, *args, **kwargs)`
- `__reduce__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/help.py`

#### Functions
- `_implementation()`
- `info()`
- `main()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/hooks.py`

#### Functions
- `default_hooks()`
- `dispatch_hook(key, hooks, hook_data, **kwargs)`

#### Parameters / Constants
- `HOOKS` = `["response"]`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/models.py`

#### Classes
- `RequestEncodingMixin`
- `RequestHooksMixin`
- `Request`
- `PreparedRequest`
- `Response`

#### Functions
- `path_url(self)`
- `_encode_params(data)`
- `_encode_files(files, data)`
- `register_hook(self, event, hook)`
- `deregister_hook(self, event, hook)`
- `__init__(
        self,
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None,
    )`
- `__repr__(self)`
- `prepare(self)`
- `__init__(self)`
- `prepare(
        self,
        method=None,
        url=None,
        headers=None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None,
    )`
- `__repr__(self)`
- `copy(self)`
- `prepare_method(self, method)`
- `_get_idna_encoded_host(host)`
- `prepare_url(self, url, params)`
- `prepare_headers(self, headers)`
- `prepare_body(self, data, files, json=None)`
- `prepare_content_length(self, body)`
- `prepare_auth(self, auth, url="")`
- `prepare_cookies(self, cookies)`
- `prepare_hooks(self, hooks)`
- `__init__(self)`
- `__enter__(self)`
- `__exit__(self, *args)`
- `__getstate__(self)`
- `__setstate__(self, state)`
- `__repr__(self)`
- `__bool__(self)`
- `__nonzero__(self)`
- `__iter__(self)`
- `ok(self)`
- `is_redirect(self)`
- `is_permanent_redirect(self)`
- `next(self)`
- `apparent_encoding(self)`
- `iter_content(self, chunk_size=1, decode_unicode=False)`
- `generate()`
- `iter_lines(
        self, chunk_size=ITER_CHUNK_SIZE, decode_unicode=False, delimiter=None
    )`
- `content(self)`
- `text(self)`
- `json(self, **kwargs)`
- `links(self)`
- `raise_for_status(self)`
- `close(self)`

#### Parameters / Constants
- `REDIRECT_STATI` = `(`
- `DEFAULT_REDIRECT_LIMIT` = `30`
- `CONTENT_CHUNK_SIZE` = `10 * 1024`
- `ITER_CHUNK_SIZE` = `512`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/sessions.py`

#### Classes
- `SessionRedirectMixin`
- `Session`

#### Functions
- `merge_setting(request_setting, session_setting, dict_class=OrderedDict)`
- `merge_hooks(request_hooks, session_hooks, dict_class=OrderedDict)`
- `get_redirect_target(self, resp)`
- `should_strip_auth(self, old_url, new_url)`
- `resolve_redirects(
        self,
        resp,
        req,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
        yield_requests=False,
        **adapter_kwargs,
    )`
- `rebuild_auth(self, prepared_request, response)`
- `rebuild_proxies(self, prepared_request, proxies)`
- `rebuild_method(self, prepared_request, response)`
- `__init__(self)`
- `__enter__(self)`
- `__exit__(self, *args)`
- `prepare_request(self, request)`
- `request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    )`
- `get(self, url, **kwargs)`
- `options(self, url, **kwargs)`
- `head(self, url, **kwargs)`
- `post(self, url, data=None, json=None, **kwargs)`
- `put(self, url, data=None, **kwargs)`
- `patch(self, url, data=None, **kwargs)`
- `delete(self, url, **kwargs)`
- `send(self, request, **kwargs)`
- `merge_environment_settings(self, url, proxies, stream, verify, cert)`
- `get_adapter(self, url)`
- `close(self)`
- `mount(self, prefix, adapter)`
- `__getstate__(self)`
- `__setstate__(self, state)`
- `session()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/status_codes.py`

#### Functions
- `_init()`
- `doc(code)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/structures.py`

#### Classes
- `CaseInsensitiveDict`
- `LookupDict`

#### Functions
- `__init__(self, data=None, **kwargs)`
- `__setitem__(self, key, value)`
- `__getitem__(self, key)`
- `__delitem__(self, key)`
- `__iter__(self)`
- `__len__(self)`
- `lower_items(self)`
- `__eq__(self, other)`
- `copy(self)`
- `__repr__(self)`
- `__init__(self, name=None)`
- `__repr__(self)`
- `__getitem__(self, key)`
- `get(self, key, default=None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/requests/utils.py`

#### Functions
- `proxy_bypass_registry(host)`
- `proxy_bypass(host)`
- `dict_to_sequence(d)`
- `super_len(o)`
- `get_netrc_auth(url, raise_errors=False)`
- `guess_filename(obj)`
- `extract_zipped_paths(path)`
- `atomic_open(filename)`
- `from_key_val_list(value)`
- `to_key_val_list(value)`
- `parse_list_header(value)`
- `parse_dict_header(value)`
- `unquote_header_value(value, is_filename=False)`
- `dict_from_cookiejar(cj)`
- `add_dict_to_cookiejar(cj, cookie_dict)`
- `get_encodings_from_content(content)`
- `_parse_content_type_header(header)`
- `get_encoding_from_headers(headers)`
- `stream_decode_response_unicode(iterator, r)`
- `iter_slices(string, slice_length)`
- `get_unicode_from_response(r)`
- `unquote_unreserved(uri)`
- `requote_uri(uri)`
- `address_in_network(ip, net)`
- `dotted_netmask(mask)`
- `is_ipv4_address(string_ip)`
- `is_valid_cidr(string_network)`
- `set_environ(env_name, value)`
- `should_bypass_proxies(url, no_proxy)`
- `get_proxy(key)`
- `get_environ_proxies(url, no_proxy=None)`
- `select_proxy(url, proxies)`
- `resolve_proxies(request, proxies, trust_env=True)`
- `default_user_agent(name="python-requests")`
- `default_headers()`
- `parse_header_links(value)`
- `guess_json_utf(data)`
- `prepend_scheme_if_needed(url, new_scheme)`
- `get_auth_from_url(url)`
- `check_header_validity(header)`
- `_validate_header_part(header, header_part, header_validator_index)`
- `urldefragauth(url)`
- `rewind_body(prepared_request)`

#### Parameters / Constants
- `NETRC_FILES` = `(".netrc", "_netrc")`
- `DEFAULT_CA_BUNDLE_PATH` = `certs.where()`
- `DEFAULT_PORTS` = `{"http": 80, "https": 443}`
- `DEFAULT_ACCEPT_ENCODING` = `", ".join(`
- `UNRESERVED_SET` = `frozenset(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/providers.py`

#### Classes
- `Preference`
- `AbstractProvider`

#### Functions
- `__lt__(self, __other: Any)`
- `identify(self, requirement_or_candidate: RT | CT)`
- `get_preference(
        self,
        identifier: KT,
        resolutions: Mapping[KT, CT],
        candidates: Mapping[KT, Iterator[CT]],
        information: Mapping[KT, Iterator[RequirementInformation[RT, CT]]],
        backtrack_causes: Sequence[RequirementInformation[RT, CT]],
    )`
- `find_matches(
        self,
        identifier: KT,
        requirements: Mapping[KT, Iterator[RT]],
        incompatibilities: Mapping[KT, Iterator[CT]],
    )`
- `is_satisfied_by(self, requirement: RT, candidate: CT)`
- `get_dependencies(self, candidate: CT)`
- `narrow_requirement_selection(
        self,
        identifiers: Iterable[KT],
        resolutions: Mapping[KT, CT],
        candidates: Mapping[KT, Iterator[CT]],
        information: Mapping[KT, Iterator[RequirementInformation[RT, CT]]],
        backtrack_causes: Sequence[RequirementInformation[RT, CT]],
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/reporters.py`

#### Classes
- `BaseReporter`

#### Functions
- `starting(self)`
- `starting_round(self, index: int)`
- `ending_round(self, index: int, state: State[RT, CT, KT])`
- `ending(self, state: State[RT, CT, KT])`
- `adding_requirement(self, requirement: RT, parent: CT | None)`
- `resolving_conflicts(
        self, causes: Collection[RequirementInformation[RT, CT]]
    )`
- `rejecting_candidate(self, criterion: Criterion[RT, CT], candidate: CT)`
- `pinning(self, candidate: CT)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/abstract.py`

#### Classes
- `Result`
- `AbstractResolver`

#### Functions
- `__init__(
        self,
        provider: AbstractProvider[RT, CT, KT],
        reporter: BaseReporter[RT, CT, KT],
    )`
- `resolve(self, requirements: Iterable[RT], **kwargs: Any)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/criterion.py`

#### Classes
- `Criterion`

#### Functions
- `__init__(
        self,
        candidates: Iterable[CT],
        information: Collection[RequirementInformation[RT, CT]],
        incompatibilities: Collection[CT],
    )`
- `__repr__(self)`
- `iter_requirement(self)`
- `iter_parent(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/exceptions.py`

#### Classes
- `ResolverException`
- `RequirementsConflicted`
- `InconsistentCandidate`
- `ResolutionError`
- `ResolutionImpossible`
- `ResolutionTooDeep`

#### Functions
- `__init__(self, criterion: Criterion[RT, CT])`
- `__str__(self)`
- `__init__(self, candidate: CT, criterion: Criterion[RT, CT])`
- `__str__(self)`
- `__init__(self, causes: Collection[RequirementInformation[RT, CT]])`
- `__init__(self, round_count: int)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/resolvers/resolution.py`

#### Classes
- `Resolution`
- `Resolver`

#### Functions
- `_build_result(state: State[RT, CT, KT])`
- `__init__(
        self,
        provider: AbstractProvider[RT, CT, KT],
        reporter: BaseReporter[RT, CT, KT],
    )`
- `state(self)`
- `_push_new_state(self)`
- `_add_to_criteria(
        self,
        criteria: dict[KT, Criterion[RT, CT]],
        requirement: RT,
        parent: CT | None,
    )`
- `_remove_information_from_criteria(
        self, criteria: dict[KT, Criterion[RT, CT]], parents: Collection[KT]
    )`
- `_get_preference(self, name: KT)`
- `_is_current_pin_satisfying(
        self, name: KT, criterion: Criterion[RT, CT]
    )`
- `_get_updated_criteria(self, candidate: CT)`
- `_attempt_to_pin_criterion(self, name: KT)`
- `_patch_criteria(
        self, incompatibilities_from_broken: list[tuple[KT, list[CT]]]
    )`
- `_save_state(self)`
- `_rollback_states(self)`
- `_backjump(self, causes: list[RequirementInformation[RT, CT]])`
- `_extract_causes(
        self, criteron: list[Criterion[RT, CT]]
    )`
- `resolve(self, requirements: Iterable[RT], max_rounds: int)`
- `resolve(  # type: ignore[override]
        self,
        requirements: Iterable[RT],
        max_rounds: int = 100,
    )`
- `_has_route_to_root(
    criteria: Mapping[KT, Criterion[RT, CT]],
    key: KT | None,
    all_keys: dict[int, KT | None],
    connected: set[KT | None],
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/resolvelib/structs.py`

#### Classes
- `RequirementInformation`
- `State`
- `DirectedGraph`
- `IteratorMapping`
- `_FactoryIterableView`
- `_SequenceIterableView`

#### Functions
- `__init__(self)`
- `__iter__(self)`
- `__len__(self)`
- `__contains__(self, key: KT)`
- `copy(self)`
- `add(self, key: KT)`
- `remove(self, key: KT)`
- `connected(self, f: KT, t: KT)`
- `connect(self, f: KT, t: KT)`
- `iter_edges(self)`
- `iter_children(self, key: KT)`
- `iter_parents(self, key: KT)`
- `__init__(
        self,
        mapping: Mapping[KT, RT],
        accessor: Callable[[RT], Iterable[CT]],
        appends: Mapping[KT, Iterable[CT]] | None = None,
    )`
- `__repr__(self)`
- `__bool__(self)`
- `__contains__(self, key: object)`
- `__getitem__(self, k: KT)`
- `__iter__(self)`
- `__len__(self)`
- `__init__(self, factory: Callable[[], Iterable[RT]])`
- `__repr__(self)`
- `__bool__(self)`
- `__iter__(self)`
- `__init__(self, sequence: Sequence[RT])`
- `__repr__(self)`
- `__bool__(self)`
- `__iter__(self)`
- `build_iter_view(matches: Matches[CT])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/__init__.py`

#### Functions
- `get_console()`
- `reconfigure(*args: Any, **kwargs: Any)`
- `print(
    *objects: Any,
    sep: str = " ",
    end: str = "\n",
    file: Optional[IO[str]] = None,
    flush: bool = False,
)`
- `print_json(
    json: Optional[str] = None,
    *,
    data: Any = None,
    indent: Union[None, int, str] = 2,
    highlight: bool = True,
    skip_keys: bool = False,
    ensure_ascii: bool = False,
    check_circular: bool = True,
    allow_nan: bool = True,
    default: Optional[Callable[[Any], Any]] = None,
    sort_keys: bool = False,
)`
- `inspect(
    obj: Any,
    *,
    console: Optional["Console"] = None,
    title: Optional[str] = None,
    help: bool = False,
    methods: bool = False,
    docs: bool = True,
    private: bool = False,
    dunder: bool = False,
    sort: bool = True,
    all: bool = False,
    value: bool = True,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/__main__.py`

#### Classes
- `ColorBox`

#### Functions
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `__rich_measure__(
        self, console: "Console", options: ConsoleOptions
    )`
- `make_test_card()`
- `comparison(renderable1: RenderableType, renderable2: RenderableType)`
- `iter_last(values: Iterable[T])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_cell_widths.py`

#### Parameters / Constants
- `CELL_WIDTHS` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_emoji_codes.py`

#### Parameters / Constants
- `EMOJI` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_emoji_replace.py`

#### Functions
- `_emoji_replace(
    text: str,
    default_variant: Optional[str] = None,
    _emoji_sub: _EmojiSubMethod = re.compile(r"(:(\S*?)`
- `do_replace(match: Match[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_export_format.py`

#### Parameters / Constants
- `CONSOLE_HTML_FORMAT` = `"""\`
- `CONSOLE_SVG_FORMAT` = `"""\`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_extension.py`

#### Functions
- `load_ipython_extension(ip: Any)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_fileno.py`

#### Functions
- `get_fileno(file_like: IO[str])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_inspect.py`

#### Classes
- `Inspect`

#### Functions
- `_first_paragraph(doc: str)`
- `__init__(
        self,
        obj: Any,
        *,
        title: Optional[TextType] = None,
        help: bool = False,
        methods: bool = False,
        docs: bool = True,
        private: bool = False,
        dunder: bool = False,
        sort: bool = True,
        all: bool = True,
        value: bool = True,
    )`
- `_make_title(self, obj: Any)`
- `__rich__(self)`
- `_get_signature(self, name: str, obj: Any)`
- `_render(self)`
- `sort_items(item: Tuple[str, Any])`
- `safe_getattr(attr_name: str)`
- `_get_formatted_doc(self, object_: Any)`
- `get_object_types_mro(obj: Union[object, Type[Any]])`
- `get_object_types_mro_as_strings(obj: object)`
- `is_object_one_of_types(
    obj: object, fully_qualified_types_names: Collection[str]
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_log_render.py`

#### Classes
- `LogRender`

#### Functions
- `__init__(
        self,
        show_time: bool = True,
        show_level: bool = False,
        show_path: bool = True,
        time_format: Union[str, FormatTimeCallable] = "[%x %X]",
        omit_repeated_times: bool = True,
        level_width: Optional[int] = 8,
    )`
- `__call__(
        self,
        console: "Console",
        renderables: Iterable["ConsoleRenderable"],
        log_time: Optional[datetime] = None,
        time_format: Optional[Union[str, FormatTimeCallable]] = None,
        level: TextType = "",
        path: Optional[str] = None,
        line_no: Optional[int] = None,
        link_path: Optional[str] = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_loop.py`

#### Functions
- `loop_first(values: Iterable[T])`
- `loop_last(values: Iterable[T])`
- `loop_first_last(values: Iterable[T])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_null_file.py`

#### Classes
- `NullFile`

#### Functions
- `close(self)`
- `isatty(self)`
- `read(self, __n: int = 1)`
- `readable(self)`
- `readline(self, __limit: int = 1)`
- `readlines(self, __hint: int = 1)`
- `seek(self, __offset: int, __whence: int = 1)`
- `seekable(self)`
- `tell(self)`
- `truncate(self, __size: Optional[int] = 1)`
- `writable(self)`
- `writelines(self, __lines: Iterable[str])`
- `__next__(self)`
- `__iter__(self)`
- `__enter__(self)`
- `__exit__(
        self,
        __t: Optional[Type[BaseException]],
        __value: Optional[BaseException],
        __traceback: Optional[TracebackType],
    )`
- `write(self, text: str)`
- `flush(self)`
- `fileno(self)`

#### Parameters / Constants
- `NULL_FILE` = `NullFile()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_palettes.py`

#### Parameters / Constants
- `WINDOWS_PALETTE` = `Palette(`
- `STANDARD_PALETTE` = `Palette(`
- `EIGHT_BIT_PALETTE` = `Palette(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_pick.py`

#### Functions
- `pick_bool(*values: Optional[bool])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_ratio.py`

#### Classes
- `Edge`
- `E`

#### Functions
- `ratio_resolve(total: int, edges: Sequence[Edge])`
- `ratio_reduce(
    total: int, ratios: List[int], maximums: List[int], values: List[int]
)`
- `ratio_distribute(
    total: int, ratios: List[int], minimums: Optional[List[int]] = None
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_spinners.py`

#### Parameters / Constants
- `SPINNERS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_stack.py`

#### Classes
- `Stack`

#### Functions
- `top(self)`
- `push(self, item: T)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_timer.py`

#### Functions
- `timer(subject: str = "time")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_win32_console.py`

#### Classes
- `LegacyWindowsError`
- `WindowsCoordinates`
- `CONSOLE_SCREEN_BUFFER_INFO`
- `CONSOLE_CURSOR_INFO`
- `LegacyWindowsTerm`

#### Functions
- `from_param(cls, value: "WindowsCoordinates")`
- `GetStdHandle(handle: int = STDOUT)`
- `GetConsoleMode(std_handle: wintypes.HANDLE)`
- `FillConsoleOutputCharacter(
    std_handle: wintypes.HANDLE,
    char: str,
    length: int,
    start: WindowsCoordinates,
)`
- `FillConsoleOutputAttribute(
    std_handle: wintypes.HANDLE,
    attributes: int,
    length: int,
    start: WindowsCoordinates,
)`
- `SetConsoleTextAttribute(
    std_handle: wintypes.HANDLE, attributes: wintypes.WORD
)`
- `GetConsoleScreenBufferInfo(
    std_handle: wintypes.HANDLE,
)`
- `SetConsoleCursorPosition(
    std_handle: wintypes.HANDLE, coords: WindowsCoordinates
)`
- `GetConsoleCursorInfo(
    std_handle: wintypes.HANDLE, cursor_info: CONSOLE_CURSOR_INFO
)`
- `SetConsoleCursorInfo(
    std_handle: wintypes.HANDLE, cursor_info: CONSOLE_CURSOR_INFO
)`
- `SetConsoleTitle(title: str)`
- `__init__(self, file: "IO[str]")`
- `cursor_position(self)`
- `screen_size(self)`
- `write_text(self, text: str)`
- `write_styled(self, text: str, style: Style)`
- `move_cursor_to(self, new_position: WindowsCoordinates)`
- `erase_line(self)`
- `erase_end_of_line(self)`
- `erase_start_of_line(self)`
- `move_cursor_up(self)`
- `move_cursor_down(self)`
- `move_cursor_forward(self)`
- `move_cursor_to_column(self, column: int)`
- `move_cursor_backward(self)`
- `hide_cursor(self)`
- `show_cursor(self)`
- `set_title(self, title: str)`
- `_get_cursor_size(self)`

#### Parameters / Constants
- `STDOUT` = `-11`
- `ENABLE_VIRTUAL_TERMINAL_PROCESSING` = `4`
- `COORD` = `wintypes._COORD`
- `BRIGHT_BIT` = `8`
- `ANSI_TO_WINDOWS` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_windows.py`

#### Classes
- `WindowsConsoleFeatures`

#### Functions
- `get_windows_console_features()`
- `get_windows_console_features()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_windows_renderer.py`

#### Functions
- `legacy_windows_render(buffer: Iterable[Segment], term: LegacyWindowsTerm)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/_wrap.py`

#### Functions
- `words(text: str)`
- `divide_line(text: str, width: int, fold: bool = True)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/abc.py`

#### Classes
- `RichRenderable`
- `Foo`

#### Functions
- `__subclasshook__(cls, other: type)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/align.py`

#### Classes
- `Align`
- `VerticalCenter`

#### Functions
- `__init__(
        self,
        renderable: "RenderableType",
        align: AlignMethod = "left",
        style: Optional[StyleType] = None,
        *,
        vertical: Optional[VerticalAlignMethod] = None,
        pad: bool = True,
        width: Optional[int] = None,
        height: Optional[int] = None,
    )`
- `__repr__(self)`
- `left(
        cls,
        renderable: "RenderableType",
        style: Optional[StyleType] = None,
        *,
        vertical: Optional[VerticalAlignMethod] = None,
        pad: bool = True,
        width: Optional[int] = None,
        height: Optional[int] = None,
    )`
- `center(
        cls,
        renderable: "RenderableType",
        style: Optional[StyleType] = None,
        *,
        vertical: Optional[VerticalAlignMethod] = None,
        pad: bool = True,
        width: Optional[int] = None,
        height: Optional[int] = None,
    )`
- `right(
        cls,
        renderable: "RenderableType",
        style: Optional[StyleType] = None,
        *,
        vertical: Optional[VerticalAlignMethod] = None,
        pad: bool = True,
        width: Optional[int] = None,
        height: Optional[int] = None,
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `generate_segments()`
- `blank_lines(count: int)`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__init__(
        self,
        renderable: "RenderableType",
        style: Optional[StyleType] = None,
    )`
- `__repr__(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `blank_lines(count: int)`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/ansi.py`

#### Classes
- `_AnsiToken`
- `AnsiDecoder`

#### Functions
- `_ansi_tokenize(ansi_text: str)`
- `__init__(self)`
- `decode(self, terminal_text: str)`
- `decode_line(self, line: str)`
- `read(fd: int)`

#### Parameters / Constants
- `SGR_STYLE_MAP` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/bar.py`

#### Classes
- `Bar`

#### Functions
- `__init__(
        self,
        size: float,
        begin: float,
        end: float,
        *,
        width: Optional[int] = None,
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default",
    )`
- `__repr__(self)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `__rich_measure__(
        self, console: Console, options: ConsoleOptions
    )`

#### Parameters / Constants
- `BEGIN_BLOCK_ELEMENTS` = `["█", "█", "█", "▐", "▐", "▐", "▕", "▕"]`
- `END_BLOCK_ELEMENTS` = `[" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]`
- `FULL_BLOCK` = `"█"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/box.py`

#### Classes
- `Box`

#### Functions
- `__init__(self, box: str, *, ascii: bool = False)`
- `__repr__(self)`
- `__str__(self)`
- `substitute(self, options: "ConsoleOptions", safe: bool = True)`
- `get_plain_headed_box(self)`
- `get_top(self, widths: Iterable[int])`
- `get_row(
        self,
        widths: Iterable[int],
        level: Literal["head", "row", "foot", "mid"] = "row",
        edge: bool = True,
    )`
- `get_bottom(self, widths: Iterable[int])`

#### Parameters / Constants
- `LEGACY_WINDOWS_SUBSTITUTIONS` = `{`
- `PLAIN_HEADED_SUBSTITUTIONS` = `{`
- `BOXES` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/cells.py`

#### Functions
- `cached_cell_len(text: str)`
- `cell_len(text: str, _cell_len: Callable[[str], int] = cached_cell_len)`
- `get_character_cell_size(character: str)`
- `set_cell_size(text: str, total: int)`
- `chop_cells(
    text: str,
    width: int,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/color.py`

#### Classes
- `ColorSystem`
- `ColorType`
- `ColorParseError`
- `Color`

#### Functions
- `__repr__(self)`
- `__str__(self)`
- `__repr__(self)`
- `__rich__(self)`
- `__rich_repr__(self)`
- `system(self)`
- `is_system_defined(self)`
- `is_default(self)`
- `get_truecolor(
        self, theme: Optional["TerminalTheme"] = None, foreground: bool = True
    )`
- `from_ansi(cls, number: int)`
- `from_triplet(cls, triplet: "ColorTriplet")`
- `from_rgb(cls, red: float, green: float, blue: float)`
- `default(cls)`
- `parse(cls, color: str)`
- `get_ansi_codes(self, foreground: bool = True)`
- `downgrade(self, system: ColorSystem)`
- `parse_rgb_hex(hex_color: str)`
- `blend_rgb(
    color1: ColorTriplet, color2: ColorTriplet, cross_fade: float = 0.5
)`

#### Parameters / Constants
- `WINDOWS` = `sys.platform == "win32"`
- `STANDARD` = `1`
- `EIGHT_BIT` = `2`
- `TRUECOLOR` = `3`
- `WINDOWS` = `4`
- `DEFAULT` = `0`
- `STANDARD` = `1`
- `EIGHT_BIT` = `2`
- `TRUECOLOR` = `3`
- `WINDOWS` = `4`
- `ANSI_COLOR_NAMES` = `{`
- `RE_COLOR` = `re.compile(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/color_triplet.py`

#### Classes
- `ColorTriplet`

#### Functions
- `hex(self)`
- `rgb(self)`
- `normalized(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/columns.py`

#### Classes
- `Columns`

#### Functions
- `__init__(
        self,
        renderables: Optional[Iterable[RenderableType]] = None,
        padding: PaddingDimensions = (0, 1)`
- `add_renderable(self, renderable: RenderableType)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `iter_renderables(
            column_count: int,
        )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/console.py`

#### Classes
- `NoChange`
- `ConsoleDimensions`
- `ConsoleOptions`
- `RichCast`
- `ConsoleRenderable`
- `CaptureError`
- `NewLine`
- `ScreenUpdate`
- `Capture`
- `ThemeContext`
- `PagerContext`
- `ScreenContext`
- `Group`
- `ConsoleThreadLocals`
- `RenderHook`
- `Console`

#### Functions
- `ascii_only(self)`
- `copy(self)`
- `update(
        self,
        *,
        width: Union[int, NoChange] = NO_CHANGE,
        min_width: Union[int, NoChange] = NO_CHANGE,
        max_width: Union[int, NoChange] = NO_CHANGE,
        justify: Union[Optional[JustifyMethod], NoChange] = NO_CHANGE,
        overflow: Union[Optional[OverflowMethod], NoChange] = NO_CHANGE,
        no_wrap: Union[Optional[bool], NoChange] = NO_CHANGE,
        highlight: Union[Optional[bool], NoChange] = NO_CHANGE,
        markup: Union[Optional[bool], NoChange] = NO_CHANGE,
        height: Union[Optional[int], NoChange] = NO_CHANGE,
    )`
- `update_width(self, width: int)`
- `update_height(self, height: int)`
- `reset_height(self)`
- `update_dimensions(self, width: int, height: int)`
- `__rich__(
        self,
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__init__(self, count: int = 1)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__init__(self, lines: List[List[Segment]], x: int, y: int)`
- `__rich_console__(
        self, console: "Console", options: ConsoleOptions
    )`
- `__init__(self, console: "Console")`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `get(self)`
- `__init__(self, console: "Console", theme: Theme, inherit: bool = True)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `__init__(
        self,
        console: "Console",
        pager: Optional[Pager] = None,
        styles: bool = False,
        links: bool = False,
    )`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `__init__(
        self, console: "Console", hide_cursor: bool, style: StyleType = ""
    )`
- `update(
        self, *renderables: RenderableType, style: Optional[StyleType] = None
    )`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `__init__(self, *renderables: "RenderableType", fit: bool = True)`
- `renderables(self)`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `group(fit: bool = True)`
- `decorator(
        method: Callable[..., Iterable[RenderableType]],
    )`
- `_replace(*args: Any, **kwargs: Any)`
- `_is_jupyter()`
- `process_renderables(
        self, renderables: List[ConsoleRenderable]
    )`
- `get_windows_console_features()`
- `detect_legacy_windows()`
- `__init__(
        self,
        *,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor", "windows"]
        ] = "auto",
        force_terminal: Optional[bool] = None,
        force_jupyter: Optional[bool] = None,
        force_interactive: Optional[bool] = None,
        soft_wrap: bool = False,
        theme: Optional[Theme] = None,
        stderr: bool = False,
        file: Optional[IO[str]] = None,
        quiet: bool = False,
        width: Optional[int] = None,
        height: Optional[int] = None,
        style: Optional[StyleType] = None,
        no_color: Optional[bool] = None,
        tab_size: int = 8,
        record: bool = False,
        markup: bool = True,
        emoji: bool = True,
        emoji_variant: Optional[EmojiVariant] = None,
        highlight: bool = True,
        log_time: bool = True,
        log_path: bool = True,
        log_time_format: Union[str, FormatTimeCallable] = "[%X]",
        highlighter: Optional["HighlighterType"] = ReprHighlighter()`
- `__repr__(self)`
- `file(self)`
- `file(self, new_file: IO[str])`
- `_buffer(self)`
- `_buffer_index(self)`
- `_buffer_index(self, value: int)`
- `_theme_stack(self)`
- `_detect_color_system(self)`
- `_enter_buffer(self)`
- `_exit_buffer(self)`
- `set_live(self, live: "Live")`
- `clear_live(self)`
- `push_render_hook(self, hook: RenderHook)`
- `pop_render_hook(self)`
- `__enter__(self)`
- `__exit__(self, exc_type: Any, exc_value: Any, traceback: Any)`
- `begin_capture(self)`
- `end_capture(self)`
- `push_theme(self, theme: Theme, *, inherit: bool = True)`
- `pop_theme(self)`
- `use_theme(self, theme: Theme, *, inherit: bool = True)`
- `color_system(self)`
- `encoding(self)`
- `is_terminal(self)`
- `is_dumb_terminal(self)`
- `options(self)`
- `size(self)`
- `size(self, new_size: Tuple[int, int])`
- `width(self)`
- `width(self, width: int)`
- `height(self)`
- `height(self, height: int)`
- `bell(self)`
- `capture(self)`
- `pager(
        self, pager: Optional[Pager] = None, styles: bool = False, links: bool = False
    )`
- `line(self, count: int = 1)`
- `clear(self, home: bool = True)`
- `status(
        self,
        status: RenderableType,
        *,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    )`
- `show_cursor(self, show: bool = True)`
- `set_alt_screen(self, enable: bool = True)`
- `is_alt_screen(self)`
- `set_window_title(self, title: str)`
- `screen(
        self, hide_cursor: bool = True, style: Optional[StyleType] = None
    )`
- `measure(
        self, renderable: RenderableType, *, options: Optional[ConsoleOptions] = None
    )`
- `render(
        self, renderable: RenderableType, options: Optional[ConsoleOptions] = None
    )`
- `render_lines(
        self,
        renderable: RenderableType,
        options: Optional[ConsoleOptions] = None,
        *,
        style: Optional[Style] = None,
        pad: bool = True,
        new_lines: bool = False,
    )`
- `render_str(
        self,
        text: str,
        *,
        style: Union[str, Style] = "",
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        highlighter: Optional[HighlighterType] = None,
    )`
- `get_style(
        self, name: Union[str, Style], *, default: Optional[Union[Style, str]] = None
    )`
- `_collect_renderables(
        self,
        objects: Iterable[Any],
        sep: str,
        end: str,
        *,
        justify: Optional[JustifyMethod] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
    )`
- `align_append(renderable: RenderableType)`
- `check_text()`
- `rule(
        self,
        title: TextType = "",
        *,
        characters: str = "─",
        style: Union[str, Style] = "rule.line",
        align: AlignMethod = "center",
    )`
- `control(self, *control: Control)`
- `out(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[Union[str, Style]] = None,
        highlight: Optional[bool] = None,
    )`
- `print(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[Union[str, Style]] = None,
        justify: Optional[JustifyMethod] = None,
        overflow: Optional[OverflowMethod] = None,
        no_wrap: Optional[bool] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        crop: bool = True,
        soft_wrap: Optional[bool] = None,
        new_line_start: bool = False,
    )`
- `print_json(
        self,
        json: Optional[str] = None,
        *,
        data: Any = None,
        indent: Union[None, int, str] = 2,
        highlight: bool = True,
        skip_keys: bool = False,
        ensure_ascii: bool = False,
        check_circular: bool = True,
        allow_nan: bool = True,
        default: Optional[Callable[[Any], Any]] = None,
        sort_keys: bool = False,
    )`
- `update_screen(
        self,
        renderable: RenderableType,
        *,
        region: Optional[Region] = None,
        options: Optional[ConsoleOptions] = None,
    )`
- `update_screen_lines(
        self, lines: List[List[Segment]], x: int = 0, y: int = 0
    )`
- `print_exception(
        self,
        *,
        width: Optional[int] = 100,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        suppress: Iterable[Union[str, ModuleType]] = ()`
- `_caller_frame_info(
        offset: int,
        currentframe: Callable[[], Optional[FrameType]] = inspect.currentframe,
    )`
- `log(
        self,
        *objects: Any,
        sep: str = " ",
        end: str = "\n",
        style: Optional[Union[str, Style]] = None,
        justify: Optional[JustifyMethod] = None,
        emoji: Optional[bool] = None,
        markup: Optional[bool] = None,
        highlight: Optional[bool] = None,
        log_locals: bool = False,
        _stack_offset: int = 1,
    )`
- `on_broken_pipe(self)`
- `_check_buffer(self)`
- `_write_buffer(self)`
- `_render_buffer(self, buffer: Iterable[Segment])`
- `input(
        self,
        prompt: TextType = "",
        *,
        markup: bool = True,
        emoji: bool = True,
        password: bool = False,
        stream: Optional[TextIO] = None,
    )`
- `export_text(self, *, clear: bool = True, styles: bool = False)`
- `save_text(self, path: str, *, clear: bool = True, styles: bool = False)`
- `export_html(
        self,
        *,
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: Optional[str] = None,
        inline_styles: bool = False,
    )`
- `save_html(
        self,
        path: str,
        *,
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: str = CONSOLE_HTML_FORMAT,
        inline_styles: bool = False,
    )`
- `export_svg(
        self,
        *,
        title: str = "Rich",
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: str = CONSOLE_SVG_FORMAT,
        font_aspect_ratio: float = 0.61,
        unique_id: Optional[str] = None,
    )`
- `get_svg_style(style: Style)`
- `escape_text(text: str)`
- `make_tag(
            name: str, content: Optional[str] = None, **attribs: object
        )`
- `stringify(value: object)`
- `save_svg(
        self,
        path: str,
        *,
        title: str = "Rich",
        theme: Optional[TerminalTheme] = None,
        clear: bool = True,
        code_format: str = CONSOLE_SVG_FORMAT,
        font_aspect_ratio: float = 0.61,
        unique_id: Optional[str] = None,
    )`
- `_svg_hash(svg_main_code: str)`

#### Parameters / Constants
- `JUPYTER_DEFAULT_COLUMNS` = `115`
- `JUPYTER_DEFAULT_LINES` = `100`
- `WINDOWS` = `sys.platform == "win32"`
- `NO_CHANGE` = `NoChange()`
- `COLOR_SYSTEMS` = `{`
- `MAX_WRITE` = `32 * 1024 // 4`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/constrain.py`

#### Classes
- `Constrain`

#### Functions
- `__init__(self, renderable: "RenderableType", width: Optional[int] = 80)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/containers.py`

#### Classes
- `Renderables`
- `Lines`

#### Functions
- `__init__(
        self, renderables: Optional[Iterable["RenderableType"]] = None
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `append(self, renderable: "RenderableType")`
- `__iter__(self)`
- `__init__(self, lines: Iterable["Text"] = ()`
- `__repr__(self)`
- `__iter__(self)`
- `__getitem__(self, index: int)`
- `__getitem__(self, index: slice)`
- `__getitem__(self, index: Union[slice, int])`
- `__setitem__(self, index: int, value: "Text")`
- `__len__(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `append(self, line: "Text")`
- `extend(self, lines: Iterable["Text"])`
- `pop(self, index: int = -1)`
- `justify(
        self,
        console: "Console",
        width: int,
        justify: "JustifyMethod" = "left",
        overflow: "OverflowMethod" = "fold",
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/control.py`

#### Classes
- `Control`

#### Functions
- `__init__(self, *codes: Union[ControlType, ControlCode])`
- `bell(cls)`
- `home(cls)`
- `move(cls, x: int = 0, y: int = 0)`
- `get_codes()`
- `move_to_column(cls, x: int, y: int = 0)`
- `move_to(cls, x: int, y: int)`
- `clear(cls)`
- `show_cursor(cls, show: bool)`
- `alt_screen(cls, enable: bool)`
- `title(cls, title: str)`
- `__str__(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `strip_control_codes(
    text: str, _translate_table: Dict[int, None] = _CONTROL_STRIP_TRANSLATE
)`
- `escape_control_codes(
    text: str,
    _translate_table: Dict[int, str] = CONTROL_ESCAPE,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/diagnose.py`

#### Functions
- `report()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/emoji.py`

#### Classes
- `NoEmoji`
- `Emoji`

#### Functions
- `__init__(
        self,
        name: str,
        style: Union[str, Style] = "none",
        variant: Optional[EmojiVariant] = None,
    )`
- `replace(cls, text: str)`
- `__repr__(self)`
- `__str__(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`

#### Parameters / Constants
- `VARIANTS` = `{"text": "\uFE0E", "emoji": "\uFE0F"}`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/errors.py`

#### Classes
- `ConsoleError`
- `StyleError`
- `StyleSyntaxError`
- `MissingStyle`
- `StyleStackError`
- `NotRenderableError`
- `MarkupError`
- `LiveError`
- `NoAltScreen`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/file_proxy.py`

#### Classes
- `FileProxy`

#### Functions
- `__init__(self, console: "Console", file: IO[str])`
- `rich_proxied_file(self)`
- `__getattr__(self, name: str)`
- `write(self, text: str)`
- `flush(self)`
- `fileno(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/filesize.py`

#### Functions
- `_to_str(
    size: int,
    suffixes: Iterable[str],
    base: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
)`
- `pick_unit_and_suffix(size: int, suffixes: List[str], base: int)`
- `decimal(
    size: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/highlighter.py`

#### Classes
- `Highlighter`
- `NullHighlighter`
- `RegexHighlighter`
- `ReprHighlighter`
- `JSONHighlighter`
- `ISO8601Highlighter`

#### Functions
- `_combine_regex(*regexes: str)`
- `__call__(self, text: Union[str, Text])`
- `highlight(self, text: Text)`
- `highlight(self, text: Text)`
- `highlight(self, text: Text)`
- `highlight(self, text: Text)`

#### Parameters / Constants
- `JSON_STR` = `r"(?<![\\\w])(?P<str>b?\".*?(?<!\\)\")"`
- `JSON_WHITESPACE` = `{" ", "\n", "\r", "\t"}`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/json.py`

#### Classes
- `JSON`

#### Functions
- `__init__(
        self,
        json: str,
        indent: Union[None, int, str] = 2,
        highlight: bool = True,
        skip_keys: bool = False,
        ensure_ascii: bool = False,
        check_circular: bool = True,
        allow_nan: bool = True,
        default: Optional[Callable[[Any], Any]] = None,
        sort_keys: bool = False,
    )`
- `from_data(
        cls,
        data: Any,
        indent: Union[None, int, str] = 2,
        highlight: bool = True,
        skip_keys: bool = False,
        ensure_ascii: bool = False,
        check_circular: bool = True,
        allow_nan: bool = True,
        default: Optional[Callable[[Any], Any]] = None,
        sort_keys: bool = False,
    )`
- `__rich__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/jupyter.py`

#### Classes
- `JupyterRenderable`
- `JupyterMixin`

#### Functions
- `__init__(self, html: str, text: str)`
- `_repr_mimebundle_(
        self, include: Sequence[str], exclude: Sequence[str], **kwargs: Any
    )`
- `_repr_mimebundle_(
        self: "ConsoleRenderable",
        include: Sequence[str],
        exclude: Sequence[str],
        **kwargs: Any,
    )`
- `_render_segments(segments: Iterable[Segment])`
- `escape(text: str)`
- `display(segments: Iterable[Segment], text: str)`
- `print(*args: Any, **kwargs: Any)`

#### Parameters / Constants
- `JUPYTER_HTML_FORMAT` = `"""\`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/layout.py`

#### Classes
- `LayoutRender`
- `LayoutError`
- `NoSplitter`
- `_Placeholder`
- `Splitter`
- `RowSplitter`
- `ColumnSplitter`
- `Layout`

#### Functions
- `__init__(self, layout: "Layout", style: StyleType = "")`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `get_tree_icon(self)`
- `divide(
        self, children: Sequence["Layout"], region: Region
    )`
- `get_tree_icon(self)`
- `divide(
        self, children: Sequence["Layout"], region: Region
    )`
- `get_tree_icon(self)`
- `divide(
        self, children: Sequence["Layout"], region: Region
    )`
- `__init__(
        self,
        renderable: Optional[RenderableType] = None,
        *,
        name: Optional[str] = None,
        size: Optional[int] = None,
        minimum_size: int = 1,
        ratio: int = 1,
        visible: bool = True,
    )`
- `__rich_repr__(self)`
- `renderable(self)`
- `children(self)`
- `map(self)`
- `get(self, name: str)`
- `__getitem__(self, name: str)`
- `tree(self)`
- `summary(layout: "Layout")`
- `recurse(tree: "Tree", layout: "Layout")`
- `split(
        self,
        *layouts: Union["Layout", RenderableType],
        splitter: Union[Splitter, str] = "column",
    )`
- `add_split(self, *layouts: Union["Layout", RenderableType])`
- `split_row(self, *layouts: Union["Layout", RenderableType])`
- `split_column(self, *layouts: Union["Layout", RenderableType])`
- `unsplit(self)`
- `update(self, renderable: RenderableType)`
- `refresh_screen(self, console: "Console", layout_name: str)`
- `_make_region_map(self, width: int, height: int)`
- `render(self, console: Console, options: ConsoleOptions)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/live.py`

#### Classes
- `_RefreshThread`
- `Live`

#### Functions
- `__init__(self, live: "Live", refresh_per_second: float)`
- `stop(self)`
- `run(self)`
- `__init__(
        self,
        renderable: Optional[RenderableType] = None,
        *,
        console: Optional[Console] = None,
        screen: bool = False,
        auto_refresh: bool = True,
        refresh_per_second: float = 4,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        vertical_overflow: VerticalOverflowMethod = "ellipsis",
        get_renderable: Optional[Callable[[], RenderableType]] = None,
    )`
- `is_started(self)`
- `get_renderable(self)`
- `start(self, refresh: bool = False)`
- `stop(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `_enable_redirect_io(self)`
- `_disable_redirect_io(self)`
- `renderable(self)`
- `update(self, renderable: RenderableType, *, refresh: bool = False)`
- `refresh(self)`
- `process_renderables(
        self, renderables: List[ConsoleRenderable]
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/live_render.py`

#### Classes
- `LiveRender`

#### Functions
- `__init__(
        self,
        renderable: RenderableType,
        style: StyleType = "",
        vertical_overflow: VerticalOverflowMethod = "ellipsis",
    )`
- `set_renderable(self, renderable: RenderableType)`
- `position_cursor(self)`
- `restore_cursor(self)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/logging.py`

#### Classes
- `RichHandler`

#### Functions
- `__init__(
        self,
        level: Union[int, str] = logging.NOTSET,
        console: Optional[Console] = None,
        *,
        show_time: bool = True,
        omit_repeated_times: bool = True,
        show_level: bool = True,
        show_path: bool = True,
        enable_link_path: bool = True,
        highlighter: Optional[Highlighter] = None,
        markup: bool = False,
        rich_tracebacks: bool = False,
        tracebacks_width: Optional[int] = None,
        tracebacks_code_width: Optional[int] = 88,
        tracebacks_extra_lines: int = 3,
        tracebacks_theme: Optional[str] = None,
        tracebacks_word_wrap: bool = True,
        tracebacks_show_locals: bool = False,
        tracebacks_suppress: Iterable[Union[str, ModuleType]] = ()`
- `get_level_text(self, record: LogRecord)`
- `emit(self, record: LogRecord)`
- `render_message(self, record: LogRecord, message: str)`
- `render(
        self,
        *,
        record: LogRecord,
        traceback: Optional[Traceback],
        message_renderable: "ConsoleRenderable",
    )`
- `divide()`

#### Parameters / Constants
- `FORMAT` = `"%(message)s"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/markup.py`

#### Classes
- `Tag`

#### Functions
- `__str__(self)`
- `markup(self)`
- `escape(
    markup: str,
    _escape: _EscapeSubMethod = re.compile(r"(\\*)`
- `escape_backslashes(match: Match[str])`
- `_parse(markup: str)`
- `render(
    markup: str,
    style: Union[str, Style] = "",
    emoji: bool = True,
    emoji_variant: Optional[EmojiVariant] = None,
)`
- `pop_style(style_name: str)`

#### Parameters / Constants
- `RE_TAGS` = `re.compile(`
- `RE_HANDLER` = `re.compile(r"^([\w.]*?)(\(.*?\))?$")`
- `MARKUP` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/measure.py`

#### Classes
- `Measurement`

#### Functions
- `span(self)`
- `normalize(self)`
- `with_maximum(self, width: int)`
- `with_minimum(self, width: int)`
- `clamp(
        self, min_width: Optional[int] = None, max_width: Optional[int] = None
    )`
- `get(
        cls, console: "Console", options: "ConsoleOptions", renderable: "RenderableType"
    )`
- `measure_renderables(
    console: "Console",
    options: "ConsoleOptions",
    renderables: Sequence["RenderableType"],
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/padding.py`

#### Classes
- `Padding`

#### Functions
- `__init__(
        self,
        renderable: "RenderableType",
        pad: "PaddingDimensions" = (0, 0, 0, 0)`
- `indent(cls, renderable: "RenderableType", level: int)`
- `unpack(pad: "PaddingDimensions")`
- `__repr__(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/pager.py`

#### Classes
- `Pager`
- `SystemPager`

#### Functions
- `show(self, content: str)`
- `_pager(self, content: str)`
- `show(self, content: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/palette.py`

#### Classes
- `Palette`
- `ColorBox`

#### Functions
- `__init__(self, colors: Sequence[Tuple[int, int, int]])`
- `__getitem__(self, number: int)`
- `__rich__(self)`
- `match(self, color: Tuple[int, int, int])`
- `get_color_distance(index: int)`
- `__rich_console__(
            self, console: Console, options: ConsoleOptions
        )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/panel.py`

#### Classes
- `Panel`

#### Functions
- `__init__(
        self,
        renderable: "RenderableType",
        box: Box = ROUNDED,
        *,
        title: Optional[TextType] = None,
        title_align: AlignMethod = "center",
        subtitle: Optional[TextType] = None,
        subtitle_align: AlignMethod = "center",
        safe_box: Optional[bool] = None,
        expand: bool = True,
        style: StyleType = "none",
        border_style: StyleType = "none",
        width: Optional[int] = None,
        height: Optional[int] = None,
        padding: PaddingDimensions = (0, 1)`
- `fit(
        cls,
        renderable: "RenderableType",
        box: Box = ROUNDED,
        *,
        title: Optional[TextType] = None,
        title_align: AlignMethod = "center",
        subtitle: Optional[TextType] = None,
        subtitle_align: AlignMethod = "center",
        safe_box: Optional[bool] = None,
        style: StyleType = "none",
        border_style: StyleType = "none",
        width: Optional[int] = None,
        height: Optional[int] = None,
        padding: PaddingDimensions = (0, 1)`
- `_title(self)`
- `_subtitle(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `align_text(
            text: Text, width: int, align: str, character: str, style: Style
        )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/pretty.py`

#### Classes
- `RichFormatter`
- `Pretty`
- `Node`
- `_Line`
- `BrokenRepr`
- `StockKeepingUnit`
- `Thing`

#### Functions
- `_is_attr_object(obj: Any)`
- `_get_attr_fields(obj: Any)`
- `_is_dataclass_repr(obj: object)`
- `_has_default_namedtuple_repr(obj: object)`
- `_ipy_display_hook(
    value: Any,
    console: Optional["Console"] = None,
    overflow: "OverflowMethod" = "ignore",
    crop: bool = False,
    indent_guides: bool = False,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
    expand_all: bool = False,
)`
- `_safe_isinstance(
    obj: object, class_or_tuple: Union[type, Tuple[type, ...]]
)`
- `install(
    console: Optional["Console"] = None,
    overflow: "OverflowMethod" = "ignore",
    crop: bool = False,
    indent_guides: bool = False,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
    expand_all: bool = False,
)`
- `display_hook(value: Any)`
- `__call__(self, value: Any)`
- `__init__(
        self,
        _object: Any,
        highlighter: Optional["HighlighterType"] = None,
        *,
        indent_size: int = 4,
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
        no_wrap: Optional[bool] = False,
        indent_guides: bool = False,
        max_length: Optional[int] = None,
        max_string: Optional[int] = None,
        max_depth: Optional[int] = None,
        expand_all: bool = False,
        margin: int = 0,
        insert_line: bool = False,
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `_get_braces_for_defaultdict(_object: DefaultDict[Any, Any])`
- `_get_braces_for_deque(_object: Deque[Any])`
- `_get_braces_for_array(_object: "array[Any]")`
- `is_expandable(obj: Any)`
- `iter_tokens(self)`
- `check_length(self, start_length: int, max_length: int)`
- `__str__(self)`
- `render(
        self, max_width: int = 80, indent_size: int = 4, expand_all: bool = False
    )`
- `expandable(self)`
- `check_length(self, max_length: int)`
- `expand(self, indent_size: int)`
- `__str__(self)`
- `_is_namedtuple(obj: Any)`
- `traverse(
    _object: Any,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
)`
- `to_repr(obj: Any)`
- `_traverse(obj: Any, root: bool = False, depth: int = 0)`
- `iter_rich_args(rich_args: Any)`
- `iter_attrs()`
- `pretty_repr(
    _object: Any,
    *,
    max_width: int = 80,
    indent_size: int = 4,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
    expand_all: bool = False,
)`
- `pprint(
    _object: Any,
    *,
    console: Optional["Console"] = None,
    indent_guides: bool = True,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
    max_depth: Optional[int] = None,
    expand_all: bool = False,
)`
- `__repr__(self)`
- `__repr__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/progress.py`

#### Classes
- `_TrackThread`
- `_Reader`
- `_ReadContext`
- `ProgressColumn`
- `RenderableColumn`
- `SpinnerColumn`
- `TextColumn`
- `BarColumn`
- `TimeElapsedColumn`
- `TaskProgressColumn`
- `TimeRemainingColumn`
- `FileSizeColumn`
- `TotalFileSizeColumn`
- `MofNCompleteColumn`
- `DownloadColumn`
- `TransferSpeedColumn`
- `ProgressSample`
- `Task`
- `Progress`

#### Functions
- `__init__(self, progress: "Progress", task_id: "TaskID", update_period: float)`
- `run(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `track(
    sequence: Iterable[ProgressType],
    description: str = "Working...",
    total: Optional[float] = None,
    completed: int = 0,
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    update_period: float = 0.1,
    disable: bool = False,
    show_speed: bool = True,
)`
- `__init__(
        self,
        handle: BinaryIO,
        progress: "Progress",
        task: TaskID,
        close_handle: bool = True,
    )`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `__iter__(self)`
- `__next__(self)`
- `closed(self)`
- `fileno(self)`
- `isatty(self)`
- `mode(self)`
- `name(self)`
- `readable(self)`
- `seekable(self)`
- `writable(self)`
- `read(self, size: int = -1)`
- `readinto(self, b: Union[bytearray, memoryview, mmap])`
- `readline(self, size: int = -1)`
- `readlines(self, hint: int = -1)`
- `close(self)`
- `seek(self, offset: int, whence: int = 0)`
- `tell(self)`
- `write(self, s: Any)`
- `writelines(self, lines: Iterable[Any])`
- `__init__(self, progress: "Progress", reader: _I)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `wrap_file(
    file: BinaryIO,
    total: int,
    *,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
)`
- `open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Union[Literal["rt"], Literal["r"]],
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
)`
- `open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Literal["rb"],
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
)`
- `open(
    file: Union[str, "PathLike[str]", bytes],
    mode: Union[Literal["rb"], Literal["rt"], Literal["r"]] = "r",
    buffering: int = -1,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    *,
    total: Optional[int] = None,
    description: str = "Reading...",
    auto_refresh: bool = True,
    console: Optional[Console] = None,
    transient: bool = False,
    get_time: Optional[Callable[[], float]] = None,
    refresh_per_second: float = 10,
    style: StyleType = "bar.back",
    complete_style: StyleType = "bar.complete",
    finished_style: StyleType = "bar.finished",
    pulse_style: StyleType = "bar.pulse",
    disable: bool = False,
)`
- `__init__(self, table_column: Optional[Column] = None)`
- `get_table_column(self)`
- `__call__(self, task: "Task")`
- `render(self, task: "Task")`
- `__init__(
        self, renderable: RenderableType = "", *, table_column: Optional[Column] = None
    )`
- `render(self, task: "Task")`
- `__init__(
        self,
        spinner_name: str = "dots",
        style: Optional[StyleType] = "progress.spinner",
        speed: float = 1.0,
        finished_text: TextType = " ",
        table_column: Optional[Column] = None,
    )`
- `set_spinner(
        self,
        spinner_name: str,
        spinner_style: Optional[StyleType] = "progress.spinner",
        speed: float = 1.0,
    )`
- `render(self, task: "Task")`
- `__init__(
        self,
        text_format: str,
        style: StyleType = "none",
        justify: JustifyMethod = "left",
        markup: bool = True,
        highlighter: Optional[Highlighter] = None,
        table_column: Optional[Column] = None,
    )`
- `render(self, task: "Task")`
- `__init__(
        self,
        bar_width: Optional[int] = 40,
        style: StyleType = "bar.back",
        complete_style: StyleType = "bar.complete",
        finished_style: StyleType = "bar.finished",
        pulse_style: StyleType = "bar.pulse",
        table_column: Optional[Column] = None,
    )`
- `render(self, task: "Task")`
- `render(self, task: "Task")`
- `__init__(
        self,
        text_format: str = "[progress.percentage]{task.percentage:>3.0f}%",
        text_format_no_percentage: str = "",
        style: StyleType = "none",
        justify: JustifyMethod = "left",
        markup: bool = True,
        highlighter: Optional[Highlighter] = None,
        table_column: Optional[Column] = None,
        show_speed: bool = False,
    )`
- `render_speed(cls, speed: Optional[float])`
- `render(self, task: "Task")`
- `__init__(
        self,
        compact: bool = False,
        elapsed_when_finished: bool = False,
        table_column: Optional[Column] = None,
    )`
- `render(self, task: "Task")`
- `render(self, task: "Task")`
- `render(self, task: "Task")`
- `__init__(self, separator: str = "/", table_column: Optional[Column] = None)`
- `render(self, task: "Task")`
- `__init__(
        self, binary_units: bool = False, table_column: Optional[Column] = None
    )`
- `render(self, task: "Task")`
- `render(self, task: "Task")`
- `get_time(self)`
- `started(self)`
- `remaining(self)`
- `elapsed(self)`
- `finished(self)`
- `percentage(self)`
- `speed(self)`
- `time_remaining(self)`
- `_reset(self)`
- `__init__(
        self,
        *columns: Union[str, ProgressColumn],
        console: Optional[Console] = None,
        auto_refresh: bool = True,
        refresh_per_second: float = 10,
        speed_estimate_period: float = 30.0,
        transient: bool = False,
        redirect_stdout: bool = True,
        redirect_stderr: bool = True,
        get_time: Optional[GetTimeCallable] = None,
        disable: bool = False,
        expand: bool = False,
    )`
- `get_default_columns(cls)`
- `console(self)`
- `tasks(self)`
- `task_ids(self)`
- `finished(self)`
- `start(self)`
- `stop(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`
- `track(
        self,
        sequence: Iterable[ProgressType],
        total: Optional[float] = None,
        completed: int = 0,
        task_id: Optional[TaskID] = None,
        description: str = "Working...",
        update_period: float = 0.1,
    )`
- `wrap_file(
        self,
        file: BinaryIO,
        total: Optional[int] = None,
        *,
        task_id: Optional[TaskID] = None,
        description: str = "Reading...",
    )`
- `open(
        self,
        file: Union[str, "PathLike[str]", bytes],
        mode: Literal["rb"],
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
        *,
        total: Optional[int] = None,
        task_id: Optional[TaskID] = None,
        description: str = "Reading...",
    )`
- `open(
        self,
        file: Union[str, "PathLike[str]", bytes],
        mode: Union[Literal["r"], Literal["rt"]],
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
        *,
        total: Optional[int] = None,
        task_id: Optional[TaskID] = None,
        description: str = "Reading...",
    )`
- `open(
        self,
        file: Union[str, "PathLike[str]", bytes],
        mode: Union[Literal["rb"], Literal["rt"], Literal["r"]] = "r",
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
        *,
        total: Optional[int] = None,
        task_id: Optional[TaskID] = None,
        description: str = "Reading...",
    )`
- `start_task(self, task_id: TaskID)`
- `stop_task(self, task_id: TaskID)`
- `update(
        self,
        task_id: TaskID,
        *,
        total: Optional[float] = None,
        completed: Optional[float] = None,
        advance: Optional[float] = None,
        description: Optional[str] = None,
        visible: Optional[bool] = None,
        refresh: bool = False,
        **fields: Any,
    )`
- `reset(
        self,
        task_id: TaskID,
        *,
        start: bool = True,
        total: Optional[float] = None,
        completed: int = 0,
        visible: Optional[bool] = None,
        description: Optional[str] = None,
        **fields: Any,
    )`
- `advance(self, task_id: TaskID, advance: float = 1)`
- `refresh(self)`
- `get_renderable(self)`
- `get_renderables(self)`
- `make_tasks_table(self, tasks: Iterable[Task])`
- `__rich__(self)`
- `add_task(
        self,
        description: str,
        start: bool = True,
        total: Optional[float] = 100.0,
        completed: int = 0,
        visible: bool = True,
        **fields: Any,
    )`
- `remove_task(self, task_id: TaskID)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/progress_bar.py`

#### Classes
- `ProgressBar`

#### Functions
- `__init__(
        self,
        total: Optional[float] = 100.0,
        completed: float = 0,
        width: Optional[int] = None,
        pulse: bool = False,
        style: StyleType = "bar.back",
        complete_style: StyleType = "bar.complete",
        finished_style: StyleType = "bar.finished",
        pulse_style: StyleType = "bar.pulse",
        animation_time: Optional[float] = None,
    )`
- `__repr__(self)`
- `percentage_completed(self)`
- `_get_pulse_segments(
        self,
        fore_style: Style,
        back_style: Style,
        color_system: str,
        no_color: bool,
        ascii: bool = False,
    )`
- `update(self, completed: float, total: Optional[float] = None)`
- `_render_pulse(
        self, console: Console, width: int, ascii: bool = False
    )`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `__rich_measure__(
        self, console: Console, options: ConsoleOptions
    )`

#### Parameters / Constants
- `PULSE_SIZE` = `20`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/prompt.py`

#### Classes
- `PromptError`
- `InvalidResponse`
- `PromptBase`
- `Prompt`
- `IntPrompt`
- `FloatPrompt`
- `Confirm`

#### Functions
- `__init__(self, message: TextType)`
- `__rich__(self)`
- `__init__(
        self,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        case_sensitive: bool = True,
        show_default: bool = True,
        show_choices: bool = True,
    )`
- `ask(
        cls,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        case_sensitive: bool = True,
        show_default: bool = True,
        show_choices: bool = True,
        default: DefaultType,
        stream: Optional[TextIO] = None,
    )`
- `ask(
        cls,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        case_sensitive: bool = True,
        show_default: bool = True,
        show_choices: bool = True,
        stream: Optional[TextIO] = None,
    )`
- `ask(
        cls,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        case_sensitive: bool = True,
        show_default: bool = True,
        show_choices: bool = True,
        default: Any = ...,
        stream: Optional[TextIO] = None,
    )`
- `render_default(self, default: DefaultType)`
- `make_prompt(self, default: DefaultType)`
- `get_input(
        cls,
        console: Console,
        prompt: TextType,
        password: bool,
        stream: Optional[TextIO] = None,
    )`
- `check_choice(self, value: str)`
- `process_response(self, value: str)`
- `on_validate_error(self, value: str, error: InvalidResponse)`
- `pre_prompt(self)`
- `__call__(self, *, stream: Optional[TextIO] = None)`
- `__call__(
        self, *, default: DefaultType, stream: Optional[TextIO] = None
    )`
- `__call__(self, *, default: Any = ..., stream: Optional[TextIO] = None)`
- `render_default(self, default: DefaultType)`
- `process_response(self, value: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/protocol.py`

#### Functions
- `is_renderable(check_object: Any)`
- `rich_cast(renderable: object)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/region.py`

#### Classes
- `Region`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/repr.py`

#### Classes
- `ReprError`
- `Foo`

#### Functions
- `auto(cls: Optional[Type[T]])`
- `auto(*, angular: bool = False)`
- `auto(
    cls: Optional[Type[T]] = None, *, angular: Optional[bool] = None
)`
- `do_replace(cls: Type[T], angular: Optional[bool] = None)`
- `auto_repr(self: T)`
- `auto_rich_repr(self: Type[T])`
- `rich_repr(cls: Optional[Type[T]])`
- `rich_repr(*, angular: bool = False)`
- `rich_repr(
    cls: Optional[Type[T]] = None, *, angular: bool = False
)`
- `__rich_repr__(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/rule.py`

#### Classes
- `Rule`

#### Functions
- `__init__(
        self,
        title: Union[str, Text] = "",
        *,
        characters: str = "─",
        style: Union[str, Style] = "rule.line",
        end: str = "\n",
        align: AlignMethod = "center",
    )`
- `__repr__(self)`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `_rule_line(self, chars_len: int, width: int)`
- `__rich_measure__(
        self, console: Console, options: ConsoleOptions
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/scope.py`

#### Functions
- `render_scope(
    scope: "Mapping[str, Any]",
    *,
    title: Optional[TextType] = None,
    sort_keys: bool = True,
    indent_guides: bool = False,
    max_length: Optional[int] = None,
    max_string: Optional[int] = None,
)`
- `sort_items(item: Tuple[str, Any])`
- `test(foo: float, bar: float)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/screen.py`

#### Classes
- `Screen`

#### Functions
- `__init__(
        self,
        *renderables: "RenderableType",
        style: Optional[StyleType] = None,
        application_mode: bool = False,
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/segment.py`

#### Classes
- `ControlType`
- `Segment`
- `Segments`
- `SegmentLines`

#### Functions
- `cell_length(self)`
- `__rich_repr__(self)`
- `__bool__(self)`
- `is_control(self)`
- `_split_cells(cls, segment: "Segment", cut: int)`
- `split_cells(self, cut: int)`
- `line(cls)`
- `apply_style(
        cls,
        segments: Iterable["Segment"],
        style: Optional[Style] = None,
        post_style: Optional[Style] = None,
    )`
- `filter_control(
        cls, segments: Iterable["Segment"], is_control: bool = False
    )`
- `split_lines(cls, segments: Iterable["Segment"])`
- `split_and_crop_lines(
        cls,
        segments: Iterable["Segment"],
        length: int,
        style: Optional[Style] = None,
        pad: bool = True,
        include_new_lines: bool = True,
    )`
- `adjust_line_length(
        cls,
        line: List["Segment"],
        length: int,
        style: Optional[Style] = None,
        pad: bool = True,
    )`
- `get_line_length(cls, line: List["Segment"])`
- `get_shape(cls, lines: List[List["Segment"]])`
- `set_shape(
        cls,
        lines: List[List["Segment"]],
        width: int,
        height: Optional[int] = None,
        style: Optional[Style] = None,
        new_lines: bool = False,
    )`
- `align_top(
        cls: Type["Segment"],
        lines: List[List["Segment"]],
        width: int,
        height: int,
        style: Style,
        new_lines: bool = False,
    )`
- `align_bottom(
        cls: Type["Segment"],
        lines: List[List["Segment"]],
        width: int,
        height: int,
        style: Style,
        new_lines: bool = False,
    )`
- `align_middle(
        cls: Type["Segment"],
        lines: List[List["Segment"]],
        width: int,
        height: int,
        style: Style,
        new_lines: bool = False,
    )`
- `simplify(cls, segments: Iterable["Segment"])`
- `strip_links(cls, segments: Iterable["Segment"])`
- `strip_styles(cls, segments: Iterable["Segment"])`
- `remove_color(cls, segments: Iterable["Segment"])`
- `divide(
        cls, segments: Iterable["Segment"], cuts: Iterable[int]
    )`
- `__init__(self, segments: Iterable[Segment], new_lines: bool = False)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__init__(self, lines: Iterable[List[Segment]], new_lines: bool = False)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`

#### Parameters / Constants
- `BELL` = `1`
- `CARRIAGE_RETURN` = `2`
- `HOME` = `3`
- `CLEAR` = `4`
- `SHOW_CURSOR` = `5`
- `HIDE_CURSOR` = `6`
- `ENABLE_ALT_SCREEN` = `7`
- `DISABLE_ALT_SCREEN` = `8`
- `CURSOR_UP` = `9`
- `CURSOR_DOWN` = `10`
- `CURSOR_FORWARD` = `11`
- `CURSOR_BACKWARD` = `12`
- `CURSOR_MOVE_TO_COLUMN` = `13`
- `CURSOR_MOVE_TO` = `14`
- `ERASE_IN_LINE` = `15`
- `SET_WINDOW_TITLE` = `16`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/spinner.py`

#### Classes
- `Spinner`

#### Functions
- `__init__(
        self,
        name: str,
        text: "RenderableType" = "",
        *,
        style: Optional["StyleType"] = None,
        speed: float = 1.0,
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `render(self, time: float)`
- `update(
        self,
        *,
        text: "RenderableType" = "",
        style: Optional["StyleType"] = None,
        speed: Optional[float] = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/status.py`

#### Classes
- `Status`

#### Functions
- `__init__(
        self,
        status: RenderableType,
        *,
        console: Optional[Console] = None,
        spinner: str = "dots",
        spinner_style: StyleType = "status.spinner",
        speed: float = 1.0,
        refresh_per_second: float = 12.5,
    )`
- `renderable(self)`
- `console(self)`
- `update(
        self,
        status: Optional[RenderableType] = None,
        *,
        spinner: Optional[str] = None,
        spinner_style: Optional[StyleType] = None,
        speed: Optional[float] = None,
    )`
- `start(self)`
- `stop(self)`
- `__rich__(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/style.py`

#### Classes
- `_Bit`
- `Style`
- `StyleStack`

#### Functions
- `__init__(self, bit_no: int)`
- `__get__(self, obj: "Style", objtype: Type["Style"])`
- `__init__(
        self,
        *,
        color: Optional[Union[Color, str]] = None,
        bgcolor: Optional[Union[Color, str]] = None,
        bold: Optional[bool] = None,
        dim: Optional[bool] = None,
        italic: Optional[bool] = None,
        underline: Optional[bool] = None,
        blink: Optional[bool] = None,
        blink2: Optional[bool] = None,
        reverse: Optional[bool] = None,
        conceal: Optional[bool] = None,
        strike: Optional[bool] = None,
        underline2: Optional[bool] = None,
        frame: Optional[bool] = None,
        encircle: Optional[bool] = None,
        overline: Optional[bool] = None,
        link: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None,
    )`
- `_make_color(color: Union[Color, str])`
- `null(cls)`
- `from_color(
        cls, color: Optional[Color] = None, bgcolor: Optional[Color] = None
    )`
- `from_meta(cls, meta: Optional[Dict[str, Any]])`
- `on(cls, meta: Optional[Dict[str, Any]] = None, **handlers: Any)`
- `link_id(self)`
- `__str__(self)`
- `__bool__(self)`
- `_make_ansi_codes(self, color_system: ColorSystem)`
- `normalize(cls, style: str)`
- `pick_first(cls, *values: Optional[StyleType])`
- `__rich_repr__(self)`
- `__eq__(self, other: Any)`
- `__ne__(self, other: Any)`
- `__hash__(self)`
- `color(self)`
- `bgcolor(self)`
- `link(self)`
- `transparent_background(self)`
- `background_style(self)`
- `meta(self)`
- `without_color(self)`
- `parse(cls, style_definition: str)`
- `get_html_style(self, theme: Optional[TerminalTheme] = None)`
- `combine(cls, styles: Iterable["Style"])`
- `chain(cls, *styles: "Style")`
- `copy(self)`
- `clear_meta_and_links(self)`
- `update_link(self, link: Optional[str] = None)`
- `render(
        self,
        text: str = "",
        *,
        color_system: Optional[ColorSystem] = ColorSystem.TRUECOLOR,
        legacy_windows: bool = False,
    )`
- `test(self, text: Optional[str] = None)`
- `_add(self, style: Optional["Style"])`
- `__add__(self, style: Optional["Style"])`
- `__init__(self, default_style: "Style")`
- `__repr__(self)`
- `current(self)`
- `push(self, style: Style)`
- `pop(self)`

#### Parameters / Constants
- `STYLE_ATTRIBUTES` = `{`
- `STYLE_ATTRIBUTES` = `cls.STYLE_ATTRIBUTES`
- `NULL_STYLE` = `Style()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/styled.py`

#### Classes
- `Styled`

#### Functions
- `__init__(self, renderable: "RenderableType", style: "StyleType")`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/syntax.py`

#### Classes
- `SyntaxTheme`
- `PygmentsSyntaxTheme`
- `ANSISyntaxTheme`
- `_SyntaxHighlightRange`
- `PaddingProperty`
- `Syntax`

#### Functions
- `get_style_for_token(self, token_type: TokenType)`
- `get_background_style(self)`
- `__init__(self, theme: Union[str, Type[PygmentsStyle]])`
- `get_style_for_token(self, token_type: TokenType)`
- `get_background_style(self)`
- `__init__(self, style_map: Dict[TokenType, Style])`
- `get_style_for_token(self, token_type: TokenType)`
- `get_background_style(self)`
- `__get__(self, obj: Syntax, objtype: Type[Syntax])`
- `__set__(self, obj: Syntax, padding: PaddingDimensions)`
- `get_theme(cls, name: Union[str, SyntaxTheme])`
- `__init__(
        self,
        code: str,
        lexer: Union[Lexer, str],
        *,
        theme: Union[str, SyntaxTheme] = DEFAULT_THEME,
        dedent: bool = False,
        line_numbers: bool = False,
        start_line: int = 1,
        line_range: Optional[Tuple[Optional[int], Optional[int]]] = None,
        highlight_lines: Optional[Set[int]] = None,
        code_width: Optional[int] = None,
        tab_size: int = 4,
        word_wrap: bool = False,
        background_color: Optional[str] = None,
        indent_guides: bool = False,
        padding: PaddingDimensions = 0,
    )`
- `from_path(
        cls,
        path: str,
        encoding: str = "utf-8",
        lexer: Optional[Union[Lexer, str]] = None,
        theme: Union[str, SyntaxTheme] = DEFAULT_THEME,
        dedent: bool = False,
        line_numbers: bool = False,
        line_range: Optional[Tuple[int, int]] = None,
        start_line: int = 1,
        highlight_lines: Optional[Set[int]] = None,
        code_width: Optional[int] = None,
        tab_size: int = 4,
        word_wrap: bool = False,
        background_color: Optional[str] = None,
        indent_guides: bool = False,
        padding: PaddingDimensions = 0,
    )`
- `guess_lexer(cls, path: str, code: Optional[str] = None)`
- `_get_base_style(self)`
- `_get_token_color(self, token_type: TokenType)`
- `lexer(self)`
- `default_lexer(self)`
- `highlight(
        self,
        code: str,
        line_range: Optional[Tuple[Optional[int], Optional[int]]] = None,
    )`
- `line_tokenize()`
- `tokens_to_spans()`
- `stylize_range(
        self,
        style: StyleType,
        start: SyntaxPosition,
        end: SyntaxPosition,
        style_before: bool = False,
    )`
- `_get_line_numbers_color(self, blend: float = 0.3)`
- `_numbers_column_width(self)`
- `_get_number_styles(self, console: Console)`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `_get_syntax(
        self,
        console: Console,
        options: ConsoleOptions,
    )`
- `_apply_stylized_ranges(self, text: Text)`
- `_process_code(self, code: str)`
- `_get_code_index_for_syntax_position(
    newlines_offsets: Sequence[int], position: SyntaxPosition
)`

#### Parameters / Constants
- `WINDOWS` = `sys.platform == "win32"`
- `DEFAULT_THEME` = `"monokai"`
- `RICH_SYNTAX_THEMES` = `{"ansi_light": ANSI_LIGHT, "ansi_dark": ANSI_DARK}`
- `NUMBERS_COLUMN_DEFAULT_PADDING` = `2`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/table.py`

#### Classes
- `Column`
- `Row`
- `_Cell`
- `Table`

#### Functions
- `copy(self)`
- `cells(self)`
- `flexible(self)`
- `__init__(
        self,
        *headers: Union[Column, str],
        title: Optional[TextType] = None,
        caption: Optional[TextType] = None,
        width: Optional[int] = None,
        min_width: Optional[int] = None,
        box: Optional[box.Box] = box.HEAVY_HEAD,
        safe_box: Optional[bool] = None,
        padding: PaddingDimensions = (0, 1)`
- `grid(
        cls,
        *headers: Union[Column, str],
        padding: PaddingDimensions = 0,
        collapse_padding: bool = True,
        pad_edge: bool = False,
        expand: bool = False,
    )`
- `expand(self)`
- `expand(self, expand: bool)`
- `_extra_width(self)`
- `row_count(self)`
- `get_row_style(self, console: "Console", index: int)`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `padding(self)`
- `padding(self, padding: PaddingDimensions)`
- `add_column(
        self,
        header: "RenderableType" = "",
        footer: "RenderableType" = "",
        *,
        header_style: Optional[StyleType] = None,
        highlight: Optional[bool] = None,
        footer_style: Optional[StyleType] = None,
        style: Optional[StyleType] = None,
        justify: "JustifyMethod" = "left",
        vertical: "VerticalAlignMethod" = "top",
        overflow: "OverflowMethod" = "ellipsis",
        width: Optional[int] = None,
        min_width: Optional[int] = None,
        max_width: Optional[int] = None,
        ratio: Optional[int] = None,
        no_wrap: bool = False,
    )`
- `add_row(
        self,
        *renderables: Optional["RenderableType"],
        style: Optional[StyleType] = None,
        end_section: bool = False,
    )`
- `add_cell(column: Column, renderable: "RenderableType")`
- `add_section(self)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `render_annotation(
            text: TextType, style: StyleType, justify: "JustifyMethod" = "center"
        )`
- `_calculate_column_widths(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `_collapse_widths(
        cls, widths: List[int], wrapable: List[bool], max_width: int
    )`
- `_get_cells(
        self, console: "Console", column_index: int, column: Column
    )`
- `get_padding(first_row: bool, last_row: bool)`
- `_get_padding_width(self, column_index: int)`
- `_measure_column(
        self,
        console: "Console",
        options: "ConsoleOptions",
        column: Column,
    )`
- `_render(
        self, console: "Console", options: "ConsoleOptions", widths: List[int]
    )`
- `align_cell(
                cell: List[List[Segment]],
                vertical: "VerticalAlignMethod",
                width: int,
                style: Style,
            )`
- `header(text: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/terminal_theme.py`

#### Classes
- `TerminalTheme`

#### Functions
- `__init__(
        self,
        background: _ColorTuple,
        foreground: _ColorTuple,
        normal: List[_ColorTuple],
        bright: Optional[List[_ColorTuple]] = None,
    )`

#### Parameters / Constants
- `DEFAULT_TERMINAL_THEME` = `TerminalTheme(`
- `MONOKAI` = `TerminalTheme(`
- `DIMMED_MONOKAI` = `TerminalTheme(`
- `NIGHT_OWLISH` = `TerminalTheme(`
- `SVG_EXPORT_THEME` = `TerminalTheme(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/text.py`

#### Classes
- `Span`
- `Text`

#### Functions
- `__repr__(self)`
- `__bool__(self)`
- `split(self, offset: int)`
- `move(self, offset: int)`
- `right_crop(self, offset: int)`
- `extend(self, cells: int)`
- `__init__(
        self,
        text: str = "",
        style: Union[str, Style] = "",
        *,
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = None,
        spans: Optional[List[Span]] = None,
    )`
- `__len__(self)`
- `__bool__(self)`
- `__str__(self)`
- `__repr__(self)`
- `__add__(self, other: Any)`
- `__eq__(self, other: object)`
- `__contains__(self, other: object)`
- `__getitem__(self, slice: Union[int, slice])`
- `get_text_at(offset: int)`
- `cell_len(self)`
- `markup(self)`
- `from_markup(
        cls,
        text: str,
        *,
        style: Union[str, Style] = "",
        emoji: bool = True,
        emoji_variant: Optional[EmojiVariant] = None,
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
        end: str = "\n",
    )`
- `from_ansi(
        cls,
        text: str,
        *,
        style: Union[str, Style] = "",
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: Optional[int] = 8,
    )`
- `styled(
        cls,
        text: str,
        style: StyleType = "",
        *,
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
    )`
- `assemble(
        cls,
        *parts: Union[str, "Text", Tuple[str, StyleType]],
        style: Union[str, Style] = "",
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
        no_wrap: Optional[bool] = None,
        end: str = "\n",
        tab_size: int = 8,
        meta: Optional[Dict[str, Any]] = None,
    )`
- `plain(self)`
- `plain(self, new_text: str)`
- `spans(self)`
- `spans(self, spans: List[Span])`
- `blank_copy(self, plain: str = "")`
- `copy(self)`
- `stylize(
        self,
        style: Union[str, Style],
        start: int = 0,
        end: Optional[int] = None,
    )`
- `stylize_before(
        self,
        style: Union[str, Style],
        start: int = 0,
        end: Optional[int] = None,
    )`
- `apply_meta(
        self, meta: Dict[str, Any], start: int = 0, end: Optional[int] = None
    )`
- `on(self, meta: Optional[Dict[str, Any]] = None, **handlers: Any)`
- `remove_suffix(self, suffix: str)`
- `get_style_at_offset(self, console: "Console", offset: int)`
- `extend_style(self, spaces: int)`
- `highlight_regex(
        self,
        re_highlight: Union[Pattern[str], str],
        style: Optional[Union[GetStyleCallable, StyleType]] = None,
        *,
        style_prefix: str = "",
    )`
- `highlight_words(
        self,
        words: Iterable[str],
        style: Union[str, Style],
        *,
        case_sensitive: bool = True,
    )`
- `rstrip(self)`
- `rstrip_end(self, size: int)`
- `set_length(self, new_length: int)`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `render(self, console: "Console", end: str = "")`
- `get_current_style()`
- `join(self, lines: Iterable["Text"])`
- `iter_text()`
- `expand_tabs(self, tab_size: Optional[int] = None)`
- `truncate(
        self,
        max_width: int,
        *,
        overflow: Optional["OverflowMethod"] = None,
        pad: bool = False,
    )`
- `_trim_spans(self)`
- `pad(self, count: int, character: str = " ")`
- `pad_left(self, count: int, character: str = " ")`
- `pad_right(self, count: int, character: str = " ")`
- `align(self, align: AlignMethod, width: int, character: str = " ")`
- `append(
        self, text: Union["Text", str], style: Optional[Union[str, "Style"]] = None
    )`
- `append_text(self, text: "Text")`
- `append_tokens(
        self, tokens: Iterable[Tuple[str, Optional[StyleType]]]
    )`
- `copy_styles(self, text: "Text")`
- `split(
        self,
        separator: str = "\n",
        *,
        include_separator: bool = False,
        allow_blank: bool = False,
    )`
- `flatten_spans()`
- `divide(self, offsets: Iterable[int])`
- `right_crop(self, amount: int = 1)`
- `wrap(
        self,
        console: "Console",
        width: int,
        *,
        justify: Optional["JustifyMethod"] = None,
        overflow: Optional["OverflowMethod"] = None,
        tab_size: int = 8,
        no_wrap: Optional[bool] = None,
    )`
- `fit(self, width: int)`
- `detect_indentation(self)`
- `with_indent_guides(
        self,
        indent_size: Optional[int] = None,
        *,
        character: str = "│",
        style: StyleType = "dim green",
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/theme.py`

#### Classes
- `Theme`
- `ThemeStackError`
- `ThemeStack`

#### Functions
- `__init__(
        self, styles: Optional[Mapping[str, StyleType]] = None, inherit: bool = True
    )`
- `config(self)`
- `from_file(
        cls, config_file: IO[str], source: Optional[str] = None, inherit: bool = True
    )`
- `read(
        cls, path: str, inherit: bool = True, encoding: Optional[str] = None
    )`
- `__init__(self, theme: Theme)`
- `push_theme(self, theme: Theme, inherit: bool = True)`
- `pop_theme(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/themes.py`

#### Parameters / Constants
- `DEFAULT` = `Theme(DEFAULT_STYLES)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/traceback.py`

#### Classes
- `Frame`
- `_SyntaxError`
- `Stack`
- `Trace`
- `PathHighlighter`
- `Traceback`

#### Functions
- `_iter_syntax_lines(
    start: SyntaxPosition, end: SyntaxPosition
)`
- `install(
    *,
    console: Optional[Console] = None,
    width: Optional[int] = 100,
    code_width: Optional[int] = 88,
    extra_lines: int = 3,
    theme: Optional[str] = None,
    word_wrap: bool = False,
    show_locals: bool = False,
    locals_max_length: int = LOCALS_MAX_LENGTH,
    locals_max_string: int = LOCALS_MAX_STRING,
    locals_hide_dunder: bool = True,
    locals_hide_sunder: Optional[bool] = None,
    indent_guides: bool = True,
    suppress: Iterable[Union[str, ModuleType]] = ()`
- `excepthook(
        type_: Type[BaseException],
        value: BaseException,
        traceback: Optional[TracebackType],
    )`
- `ipy_excepthook_closure(ip: Any)`
- `ipy_show_traceback(*args: Any, **kwargs: Any)`
- `ipy_display_traceback(
            *args: Any, is_syntax: bool = False, **kwargs: Any
        )`
- `__init__(
        self,
        trace: Optional[Trace] = None,
        *,
        width: Optional[int] = 100,
        code_width: Optional[int] = 88,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        locals_max_length: int = LOCALS_MAX_LENGTH,
        locals_max_string: int = LOCALS_MAX_STRING,
        locals_hide_dunder: bool = True,
        locals_hide_sunder: bool = False,
        indent_guides: bool = True,
        suppress: Iterable[Union[str, ModuleType]] = ()`
- `from_exception(
        cls,
        exc_type: Type[Any],
        exc_value: BaseException,
        traceback: Optional[TracebackType],
        *,
        width: Optional[int] = 100,
        code_width: Optional[int] = 88,
        extra_lines: int = 3,
        theme: Optional[str] = None,
        word_wrap: bool = False,
        show_locals: bool = False,
        locals_max_length: int = LOCALS_MAX_LENGTH,
        locals_max_string: int = LOCALS_MAX_STRING,
        locals_hide_dunder: bool = True,
        locals_hide_sunder: bool = False,
        indent_guides: bool = True,
        suppress: Iterable[Union[str, ModuleType]] = ()`
- `extract(
        cls,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: Optional[TracebackType],
        *,
        show_locals: bool = False,
        locals_max_length: int = LOCALS_MAX_LENGTH,
        locals_max_string: int = LOCALS_MAX_STRING,
        locals_hide_dunder: bool = True,
        locals_hide_sunder: bool = False,
        _visited_exceptions: Optional[Set[BaseException]] = None,
    )`
- `safe_str(_object: Any)`
- `get_locals(
                iter_locals: Iterable[Tuple[str, object]],
            )`
- `__rich_console__(
        self, console: Console, options: ConsoleOptions
    )`
- `render_stack(stack: Stack, last: bool)`
- `_render_syntax_error(self, syntax_error: _SyntaxError)`
- `_guess_lexer(cls, filename: str, code: str)`
- `_render_stack(self, stack: Stack)`
- `render_locals(frame: Frame)`
- `bar(
        a: Any,
    )`
- `foo(a: Any)`
- `error()`

#### Parameters / Constants
- `WINDOWS` = `sys.platform == "win32"`
- `LOCALS_MAX_LENGTH` = `10`
- `LOCALS_MAX_STRING` = `80`
- `LEXERS` = `{`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/rich/tree.py`

#### Classes
- `Tree`
- `Segment`

#### Functions
- `__init__(
        self,
        label: RenderableType,
        *,
        style: StyleType = "tree",
        guide_style: StyleType = "tree.line",
        expanded: bool = True,
        highlight: bool = False,
        hide_root: bool = False,
    )`
- `add(
        self,
        label: RenderableType,
        *,
        style: Optional[StyleType] = None,
        guide_style: Optional[StyleType] = None,
        expanded: bool = True,
        highlight: Optional[bool] = False,
    )`
- `__rich_console__(
        self, console: "Console", options: "ConsoleOptions"
    )`
- `make_guide(index: int, style: Style)`
- `__rich_measure__(
        self, console: "Console", options: "ConsoleOptions"
    )`

#### Parameters / Constants
- `ASCII_GUIDES` = `("    ", "|   ", "+-- ", "`-- ")`
- `TREE_GUIDES` = `[`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli/_parser.py`

#### Classes
- `DEPRECATED_DEFAULT`
- `TOMLDecodeError`
- `Flags`
- `NestedDict`
- `Output`

#### Functions
- `__init__(
        self,
        msg: str | type[DEPRECATED_DEFAULT] = DEPRECATED_DEFAULT,
        doc: str | type[DEPRECATED_DEFAULT] = DEPRECATED_DEFAULT,
        pos: Pos | type[DEPRECATED_DEFAULT] = DEPRECATED_DEFAULT,
        *args: Any,
    )`
- `load(__fp: IO[bytes], *, parse_float: ParseFloat = float)`
- `loads(__s: str, *, parse_float: ParseFloat = float)`
- `__init__(self)`
- `add_pending(self, key: Key, flag: int)`
- `finalize_pending(self)`
- `unset_all(self, key: Key)`
- `set(self, key: Key, flag: int, *, recursive: bool)`
- `is_(self, key: Key, flag: int)`
- `__init__(self)`
- `get_or_create_nest(
        self,
        key: Key,
        *,
        access_lists: bool = True,
    )`
- `append_nest_to_list(self, key: Key)`
- `__init__(self)`
- `skip_chars(src: str, pos: Pos, chars: Iterable[str])`
- `skip_until(
    src: str,
    pos: Pos,
    expect: str,
    *,
    error_on: frozenset[str],
    error_on_eof: bool,
)`
- `skip_comment(src: str, pos: Pos)`
- `skip_comments_and_array_ws(src: str, pos: Pos)`
- `create_dict_rule(src: str, pos: Pos, out: Output)`
- `create_list_rule(src: str, pos: Pos, out: Output)`
- `key_value_rule(
    src: str, pos: Pos, out: Output, header: Key, parse_float: ParseFloat
)`
- `parse_key_value_pair(
    src: str, pos: Pos, parse_float: ParseFloat, nest_lvl: int
)`
- `parse_key(src: str, pos: Pos)`
- `parse_key_part(src: str, pos: Pos)`
- `parse_one_line_basic_str(src: str, pos: Pos)`
- `parse_array(
    src: str, pos: Pos, parse_float: ParseFloat, nest_lvl: int
)`
- `parse_inline_table(
    src: str, pos: Pos, parse_float: ParseFloat, nest_lvl: int
)`
- `parse_basic_str_escape(
    src: str, pos: Pos, *, multiline: bool = False
)`
- `parse_basic_str_escape_multiline(src: str, pos: Pos)`
- `parse_hex_char(src: str, pos: Pos, hex_len: int)`
- `parse_literal_str(src: str, pos: Pos)`
- `parse_multiline_str(src: str, pos: Pos, *, literal: bool)`
- `parse_basic_str(src: str, pos: Pos, *, multiline: bool)`
- `parse_value(
    src: str, pos: Pos, parse_float: ParseFloat, nest_lvl: int
)`
- `is_unicode_scalar_value(codepoint: int)`
- `make_safe_parse_float(parse_float: ParseFloat)`
- `safe_parse_float(float_str: str)`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli/_re.py`

#### Functions
- `match_to_datetime(match: re.Match[str])`
- `cached_tz(hour_str: str, minute_str: str, sign_str: str)`
- `match_to_localtime(match: re.Match[str])`
- `match_to_number(match: re.Match[str], parse_float: ParseFloat)`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/tomli_w/_writer.py`

#### Classes
- `Context`

#### Functions
- `__init__(self, allow_multiline: bool, indent: int)`
- `dump(
    obj: Mapping[str, Any],
    fp: IO[bytes],
    /,
    *,
    multiline_strings: bool = False,
    indent: int = 4,
)`
- `dumps(
    obj: Mapping[str, Any], /, *, multiline_strings: bool = False, indent: int = 4
)`
- `gen_table_chunks(
    table: Mapping[str, Any],
    ctx: Context,
    *,
    name: str,
    inside_aot: bool = False,
)`
- `format_literal(obj: object, ctx: Context, *, nest_level: int = 0)`
- `format_decimal(obj: Decimal)`
- `format_inline_table(obj: Mapping, ctx: Context)`
- `format_inline_array(obj: tuple | list, ctx: Context, nest_level: int)`
- `format_key_part(part: str)`
- `format_string(s: str, *, allow_multiline: bool)`
- `is_aot(obj: Any)`
- `is_suitable_inline_table(obj: Mapping, ctx: Context)`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`
- `ASCII_CTRL` = `frozenset(chr(i) for i in range(32)) | frozenset(chr(127))`
- `ILLEGAL_BASIC_STR_CHARS` = `frozenset('"\\') | ASCII_CTRL - frozenset("\t")`
- `BARE_KEY_CHARS` = `frozenset(`
- `ARRAY_TYPES` = `(list, tuple)`
- `MAX_LINE_LENGTH` = `100`
- `COMPACT_ESCAPES` = `MappingProxyType(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_api.py`

#### Classes
- `SSLContext`
- `TruststoreSSLObject`

#### Functions
- `inject_into_ssl()`
- `extract_from_ssl()`
- `__class__(self)`
- `__init__(self, protocol: int = None)`
- `do_handshake(self)`
- `wrap_socket(
        self,
        sock: socket.socket,
        server_side: bool = False,
        do_handshake_on_connect: bool = True,
        suppress_ragged_eofs: bool = True,
        server_hostname: str | None = None,
        session: ssl.SSLSession | None = None,
    )`
- `wrap_bio(
        self,
        incoming: ssl.MemoryBIO,
        outgoing: ssl.MemoryBIO,
        server_side: bool = False,
        server_hostname: str | None = None,
        session: ssl.SSLSession | None = None,
    )`
- `load_verify_locations(
        self,
        cafile: str | bytes | os.PathLike[str] | os.PathLike[bytes] | None = None,
        capath: str | bytes | os.PathLike[str] | os.PathLike[bytes] | None = None,
        cadata: typing.Union[str, "Buffer", None] = None,
    )`
- `load_cert_chain(
        self,
        certfile: _StrOrBytesPath,
        keyfile: _StrOrBytesPath | None = None,
        password: _PasswordType | None = None,
    )`
- `load_default_certs(
        self, purpose: ssl.Purpose = ssl.Purpose.SERVER_AUTH
    )`
- `set_alpn_protocols(self, alpn_protocols: typing.Iterable[str])`
- `set_npn_protocols(self, npn_protocols: typing.Iterable[str])`
- `set_ciphers(self, __cipherlist: str)`
- `get_ciphers(self)`
- `session_stats(self)`
- `cert_store_stats(self)`
- `set_default_verify_paths(self)`
- `get_ca_certs(
        self, binary_form: typing.Literal[False] = ...
    )`
- `get_ca_certs(self, binary_form: typing.Literal[True] = ...)`
- `get_ca_certs(self, binary_form: bool = ...)`
- `get_ca_certs(self, binary_form: bool = False)`
- `check_hostname(self)`
- `check_hostname(self, value: bool)`
- `hostname_checks_common_name(self)`
- `hostname_checks_common_name(self, value: bool)`
- `keylog_filename(self)`
- `keylog_filename(self, value: str)`
- `maximum_version(self)`
- `maximum_version(self, value: ssl.TLSVersion)`
- `minimum_version(self)`
- `minimum_version(self, value: ssl.TLSVersion)`
- `options(self)`
- `options(self, value: ssl.Options)`
- `post_handshake_auth(self)`
- `post_handshake_auth(self, value: bool)`
- `protocol(self)`
- `security_level(self)`
- `verify_flags(self)`
- `verify_flags(self, value: ssl.VerifyFlags)`
- `verify_mode(self)`
- `verify_mode(self, value: ssl.VerifyMode)`
- `_get_unverified_chain_bytes(sslobj: ssl.SSLObject)`
- `_get_unverified_chain_bytes(sslobj: ssl.SSLObject)`
- `_verify_peercerts(
    sock_or_sslobj: ssl.SSLSocket | ssl.SSLObject, server_hostname: str | None
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_macos.py`

#### Classes
- `CFConst`

#### Functions
- `_load_cdll(name: str, macos10_16_path: str)`
- `_handle_osstatus(result: OSStatus, _: typing.Any, args: typing.Any)`
- `_bytes_to_cf_data_ref(value: bytes)`
- `_bytes_to_cf_string(value: bytes)`
- `_cf_string_ref_to_str(cf_string_ref: CFStringRef)`
- `_der_certs_to_cf_cert_array(certs: list[bytes])`
- `_configure_context(ctx: ssl.SSLContext)`
- `_verify_peercerts_impl(
    ssl_context: ssl.SSLContext,
    cert_chain: list[bytes],
    server_hostname: str | None = None,
)`
- `_verify_peercerts_impl_macos_10_13(
    ssl_context: ssl.SSLContext, sec_trust_ref: typing.Any
)`
- `_verify_peercerts_impl_macos_10_14(
    ssl_context: ssl.SSLContext, sec_trust_ref: typing.Any
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_openssl.py`

#### Functions
- `_configure_context(ctx: ssl.SSLContext)`
- `_capath_contains_certs(capath: str)`
- `_verify_peercerts_impl(
    ssl_context: ssl.SSLContext,
    cert_chain: list[bytes],
    server_hostname: str | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_ssl_constants.py`

#### Functions
- `_set_ssl_context_verify_mode(
    ssl_context: ssl.SSLContext, verify_mode: ssl.VerifyMode
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/truststore/_windows.py`

#### Classes
- `CERT_CONTEXT`
- `CERT_ENHKEY_USAGE`
- `CERT_USAGE_MATCH`
- `CERT_CHAIN_PARA`
- `CERT_TRUST_STATUS`
- `CERT_CHAIN_ELEMENT`
- `CERT_SIMPLE_CHAIN`
- `CERT_CHAIN_CONTEXT`
- `SSL_EXTRA_CERT_CHAIN_POLICY_PARA`
- `CERT_CHAIN_POLICY_PARA`
- `CERT_CHAIN_POLICY_STATUS`
- `CERT_CHAIN_ENGINE_CONFIG`

#### Functions
- `_handle_win_error(result: bool, _: Any, args: Any)`
- `_verify_peercerts_impl(
    ssl_context: ssl.SSLContext,
    cert_chain: list[bytes],
    server_hostname: str | None = None,
)`
- `_get_and_verify_cert_chain(
    ssl_context: ssl.SSLContext,
    hChainEngine: HCERTCHAINENGINE | None,
    hIntermediateCertStore: HCERTSTORE,
    pPeerCertContext: c_void_p,
    pChainPara: PCERT_CHAIN_PARA,  # type: ignore[valid-type]
    server_hostname: str | None,
    chain_flags: int,
)`
- `_verify_using_custom_ca_certs(
    ssl_context: ssl.SSLContext,
    custom_ca_certs: list[bytes],
    hIntermediateCertStore: HCERTSTORE,
    pPeerCertContext: c_void_p,
    pChainPara: PCERT_CHAIN_PARA,  # type: ignore[valid-type]
    server_hostname: str | None,
    chain_flags: int,
)`
- `_configure_context(ctx: ssl.SSLContext)`

#### Parameters / Constants
- `HCERTCHAINENGINE` = `HANDLE`
- `HCERTSTORE` = `HANDLE`
- `HCRYPTPROV_LEGACY` = `HANDLE`
- `PCERT_CONTEXT` = `POINTER(CERT_CONTEXT)`
- `PCCERT_CONTEXT` = `POINTER(PCERT_CONTEXT)`
- `PCERT_ENHKEY_USAGE` = `POINTER(CERT_ENHKEY_USAGE)`
- `PCERT_CHAIN_PARA` = `pointer[CERT_CHAIN_PARA]  # type: ignore[misc]`
- `PCERT_CHAIN_PARA` = `POINTER(CERT_CHAIN_PARA)`
- `PCERT_CHAIN_ELEMENT` = `POINTER(CERT_CHAIN_ELEMENT)`
- `PCERT_SIMPLE_CHAIN` = `POINTER(CERT_SIMPLE_CHAIN)`
- `PCERT_CHAIN_CONTEXT` = `POINTER(CERT_CHAIN_CONTEXT)`
- `PCCERT_CHAIN_CONTEXT` = `POINTER(PCERT_CHAIN_CONTEXT)`
- `PCERT_CHAIN_POLICY_PARA` = `POINTER(CERT_CHAIN_POLICY_PARA)`
- `PCERT_CHAIN_POLICY_STATUS` = `POINTER(CERT_CHAIN_POLICY_STATUS)`
- `PCERT_CHAIN_ENGINE_CONFIG` = `POINTER(CERT_CHAIN_ENGINE_CONFIG)`
- `PHCERTCHAINENGINE` = `POINTER(HCERTCHAINENGINE)`
- `X509_ASN_ENCODING` = `0x00000001`
- `PKCS_7_ASN_ENCODING` = `0x00010000`
- `CERT_STORE_PROV_MEMORY` = `b"Memory"`
- `CERT_STORE_ADD_USE_EXISTING` = `2`
- `USAGE_MATCH_TYPE_OR` = `1`
- `OID_PKIX_KP_SERVER_AUTH` = `c_char_p(b"1.3.6.1.5.5.7.3.1")`
- `CERT_CHAIN_REVOCATION_CHECK_END_CERT` = `0x10000000`
- `CERT_CHAIN_REVOCATION_CHECK_CHAIN` = `0x20000000`
- `CERT_CHAIN_POLICY_IGNORE_ALL_NOT_TIME_VALID_FLAGS` = `0x00000007`
- `CERT_CHAIN_POLICY_IGNORE_INVALID_BASIC_CONSTRAINTS_FLAG` = `0x00000008`
- `CERT_CHAIN_POLICY_ALLOW_UNKNOWN_CA_FLAG` = `0x00000010`
- `CERT_CHAIN_POLICY_IGNORE_INVALID_NAME_FLAG` = `0x00000040`
- `CERT_CHAIN_POLICY_IGNORE_WRONG_USAGE_FLAG` = `0x00000020`
- `CERT_CHAIN_POLICY_IGNORE_INVALID_POLICY_FLAG` = `0x00000080`
- `CERT_CHAIN_POLICY_IGNORE_ALL_REV_UNKNOWN_FLAGS` = `0x00000F00`
- `CERT_CHAIN_POLICY_ALLOW_TESTROOT_FLAG` = `0x00008000`
- `CERT_CHAIN_POLICY_TRUST_TESTROOT_FLAG` = `0x00004000`
- `SECURITY_FLAG_IGNORE_CERT_CN_INVALID` = `0x00001000`
- `AUTHTYPE_SERVER` = `2`
- `CERT_CHAIN_POLICY_SSL` = `4`
- `FORMAT_MESSAGE_FROM_SYSTEM` = `0x00001000`
- `FORMAT_MESSAGE_IGNORE_INSERTS` = `0x00000200`
- `CERT_CHAIN_POLICY_VERIFY_MODE_NONE_FLAGS` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/__init__.py`

#### Functions
- `add_stderr_logger(
    level: int = logging.DEBUG,
)`
- `disable_warnings(category: type[Warning] = exceptions.HTTPWarning)`
- `request(
    method: str,
    url: str,
    *,
    body: _TYPE_BODY | None = None,
    fields: _TYPE_FIELDS | None = None,
    headers: typing.Mapping[str, str] | None = None,
    preload_content: bool | None = True,
    decode_content: bool | None = True,
    redirect: bool | None = True,
    retries: Retry | bool | int | None = None,
    timeout: Timeout | float | int | None = 3,
    json: typing.Any | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_base_connection.py`

#### Classes
- `ProxyConfig`
- `_ResponseOptions`
- `BaseHTTPConnection`
- `BaseHTTPSConnection`

#### Functions
- `__init__(
            self,
            host: str,
            port: int | None = None,
            *,
            timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
            source_address: tuple[str, int] | None = None,
            blocksize: int = 8192,
            socket_options: _TYPE_SOCKET_OPTIONS | None = ...,
            proxy: Url | None = None,
            proxy_config: ProxyConfig | None = None,
        )`
- `set_tunnel(
            self,
            host: str,
            port: int | None = None,
            headers: typing.Mapping[str, str] | None = None,
            scheme: str = "http",
        )`
- `connect(self)`
- `request(
            self,
            method: str,
            url: str,
            body: _TYPE_BODY | None = None,
            headers: typing.Mapping[str, str] | None = None,
            # We know *at least* botocore is depending on the order of the
            # first 3 parameters so to be safe we only mark the later ones
            # as keyword-only to ensure we have space to extend.
            *,
            chunked: bool = False,
            preload_content: bool = True,
            decode_content: bool = True,
            enforce_content_length: bool = True,
        )`
- `getresponse(self)`
- `close(self)`
- `is_closed(self)`
- `is_connected(self)`
- `has_connected_to_proxy(self)`
- `__init__(
            self,
            host: str,
            port: int | None = None,
            *,
            timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
            source_address: tuple[str, int] | None = None,
            blocksize: int = 16384,
            socket_options: _TYPE_SOCKET_OPTIONS | None = ...,
            proxy: Url | None = None,
            proxy_config: ProxyConfig | None = None,
            cert_reqs: int | str | None = None,
            assert_hostname: None | str | typing.Literal[False] = None,
            assert_fingerprint: str | None = None,
            server_hostname: str | None = None,
            ssl_context: ssl.SSLContext | None = None,
            ca_certs: str | None = None,
            ca_cert_dir: str | None = None,
            ca_cert_data: None | str | bytes = None,
            ssl_minimum_version: int | None = None,
            ssl_maximum_version: int | None = None,
            ssl_version: int | str | None = None,  # Deprecated
            cert_file: str | None = None,
            key_file: str | None = None,
            key_password: str | None = None,
        )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_collections.py`

#### Classes
- `HasGettableStringKeys`
- `_Sentinel`
- `RecentlyUsedContainer`
- `HTTPHeaderDictItemView`
- `HTTPHeaderDict`

#### Functions
- `keys(self)`
- `__getitem__(self, key: str)`
- `ensure_can_construct_http_header_dict(
    potential: object,
)`
- `__init__(
        self,
        maxsize: int = 10,
        dispose_func: typing.Callable[[_VT], None] | None = None,
    )`
- `__getitem__(self, key: _KT)`
- `__setitem__(self, key: _KT, value: _VT)`
- `__delitem__(self, key: _KT)`
- `__len__(self)`
- `__iter__(self)`
- `clear(self)`
- `keys(self)`
- `__init__(self, headers: HTTPHeaderDict)`
- `__len__(self)`
- `__iter__(self)`
- `__contains__(self, item: object)`
- `__init__(self, headers: ValidHTTPHeaderSource | None = None, **kwargs: str)`
- `__setitem__(self, key: str, val: str)`
- `__getitem__(self, key: str)`
- `__delitem__(self, key: str)`
- `__contains__(self, key: object)`
- `setdefault(self, key: str, default: str = "")`
- `__eq__(self, other: object)`
- `__ne__(self, other: object)`
- `__len__(self)`
- `__iter__(self)`
- `discard(self, key: str)`
- `add(self, key: str, val: str, *, combine: bool = False)`
- `extend(self, *args: ValidHTTPHeaderSource, **kwargs: str)`
- `getlist(self, key: str)`
- `getlist(self, key: str, default: _DT)`
- `getlist(
        self, key: str, default: _Sentinel | _DT = _Sentinel.not_passed
    )`
- `_prepare_for_method_change(self)`
- `__repr__(self)`
- `_copy_from(self, other: HTTPHeaderDict)`
- `copy(self)`
- `iteritems(self)`
- `itermerged(self)`
- `items(self)`
- `_has_value_for_header(self, header_name: str, potential_value: str)`
- `__ior__(self, other: object)`
- `__or__(self, other: object)`
- `__ror__(self, other: object)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_request_methods.py`

#### Classes
- `RequestMethods`

#### Functions
- `__init__(self, headers: typing.Mapping[str, str] | None = None)`
- `urlopen(
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        encode_multipart: bool = True,
        multipart_boundary: str | None = None,
        **kw: typing.Any,
    )`
- `request(
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        fields: _TYPE_FIELDS | None = None,
        headers: typing.Mapping[str, str] | None = None,
        json: typing.Any | None = None,
        **urlopen_kw: typing.Any,
    )`
- `request_encode_url(
        self,
        method: str,
        url: str,
        fields: _TYPE_ENCODE_URL_FIELDS | None = None,
        headers: typing.Mapping[str, str] | None = None,
        **urlopen_kw: str,
    )`
- `request_encode_body(
        self,
        method: str,
        url: str,
        fields: _TYPE_FIELDS | None = None,
        headers: typing.Mapping[str, str] | None = None,
        encode_multipart: bool = True,
        multipart_boundary: str | None = None,
        **urlopen_kw: str,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/_version.py`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`
- `VERSION_TUPLE` = `Tuple[Union[int, str], ...]`
- `COMMIT_ID` = `Union[str, None]`
- `VERSION_TUPLE` = `object`
- `COMMIT_ID` = `object`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/connection.py`

#### Classes
- `BaseSSLError`
- `HTTPConnection`
- `HTTPSConnection`
- `_WrappedAndVerifiedSocket`
- `DummyConnection`

#### Functions
- `__init__(
        self,
        host: str,
        port: int | None = None,
        *,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        source_address: tuple[str, int] | None = None,
        blocksize: int = 16384,
        socket_options: None | (
            connection._TYPE_SOCKET_OPTIONS
        )`
- `__str__(self)`
- `__repr__(self)`
- `host(self)`
- `host(self, value: str)`
- `_new_conn(self)`
- `set_tunnel(
        self,
        host: str,
        port: int | None = None,
        headers: typing.Mapping[str, str] | None = None,
        scheme: str = "http",
    )`
- `_wrap_ipv6(self, ip: bytes)`
- `_tunnel(self)`
- `_tunnel(self)`
- `connect(self)`
- `is_closed(self)`
- `is_connected(self)`
- `has_connected_to_proxy(self)`
- `proxy_is_forwarding(self)`
- `proxy_is_tunneling(self)`
- `close(self)`
- `putrequest(
        self,
        method: str,
        url: str,
        skip_host: bool = False,
        skip_accept_encoding: bool = False,
    )`
- `putheader(self, header: str, *values: str)`
- `request(  # type: ignore[override]
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        *,
        chunked: bool = False,
        preload_content: bool = True,
        decode_content: bool = True,
        enforce_content_length: bool = True,
    )`
- `request_chunked(
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
    )`
- `getresponse(  # type: ignore[override]
        self,
    )`
- `__init__(
        self,
        host: str,
        port: int | None = None,
        *,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        source_address: tuple[str, int] | None = None,
        blocksize: int = 16384,
        socket_options: None | (
            connection._TYPE_SOCKET_OPTIONS
        )`
- `set_cert(
        self,
        key_file: str | None = None,
        cert_file: str | None = None,
        cert_reqs: int | str | None = None,
        key_password: str | None = None,
        ca_certs: str | None = None,
        assert_hostname: None | str | typing.Literal[False] = None,
        assert_fingerprint: str | None = None,
        ca_cert_dir: str | None = None,
        ca_cert_data: None | str | bytes = None,
    )`
- `connect(self)`
- `_connect_tls_proxy(self, hostname: str, sock: socket.socket)`
- `_ssl_wrap_socket_and_match_hostname(
    sock: socket.socket,
    *,
    cert_reqs: None | str | int,
    ssl_version: None | str | int,
    ssl_minimum_version: int | None,
    ssl_maximum_version: int | None,
    cert_file: str | None,
    key_file: str | None,
    key_password: str | None,
    ca_certs: str | None,
    ca_cert_dir: str | None,
    ca_cert_data: None | str | bytes,
    assert_hostname: None | str | typing.Literal[False],
    assert_fingerprint: str | None,
    server_hostname: str | None,
    ssl_context: ssl.SSLContext | None,
    tls_in_tls: bool = False,
)`
- `_match_hostname(
    cert: _TYPE_PEER_CERT_RET_DICT | None,
    asserted_hostname: str,
    hostname_checks_common_name: bool = False,
)`
- `_wrap_proxy_error(err: Exception, proxy_scheme: str | None)`
- `_get_default_user_agent()`
- `_url_from_connection(
    conn: HTTPConnection | HTTPSConnection, path: str | None = None
)`

#### Parameters / Constants
- `RECENT_DATE` = `datetime.date(2025, 1, 1)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/connectionpool.py`

#### Classes
- `ConnectionPool`
- `HTTPConnectionPool`
- `HTTPSConnectionPool`

#### Functions
- `__init__(self, host: str, port: int | None = None)`
- `__str__(self)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `close(self)`
- `__init__(
        self,
        host: str,
        port: int | None = None,
        timeout: _TYPE_TIMEOUT | None = _DEFAULT_TIMEOUT,
        maxsize: int = 1,
        block: bool = False,
        headers: typing.Mapping[str, str] | None = None,
        retries: Retry | bool | int | None = None,
        _proxy: Url | None = None,
        _proxy_headers: typing.Mapping[str, str] | None = None,
        _proxy_config: ProxyConfig | None = None,
        **conn_kw: typing.Any,
    )`
- `_new_conn(self)`
- `_get_conn(self, timeout: float | None = None)`
- `_put_conn(self, conn: BaseHTTPConnection | None)`
- `_validate_conn(self, conn: BaseHTTPConnection)`
- `_prepare_proxy(self, conn: BaseHTTPConnection)`
- `_get_timeout(self, timeout: _TYPE_TIMEOUT)`
- `_raise_timeout(
        self,
        err: BaseSSLError | OSError | SocketTimeout,
        url: str,
        timeout_value: _TYPE_TIMEOUT | None,
    )`
- `_make_request(
        self,
        conn: BaseHTTPConnection,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        retries: Retry | None = None,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        chunked: bool = False,
        response_conn: BaseHTTPConnection | None = None,
        preload_content: bool = True,
        decode_content: bool = True,
        enforce_content_length: bool = True,
    )`
- `close(self)`
- `is_same_host(self, url: str)`
- `urlopen(  # type: ignore[override]
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        retries: Retry | bool | int | None = None,
        redirect: bool = True,
        assert_same_host: bool = True,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        pool_timeout: int | None = None,
        release_conn: bool | None = None,
        chunked: bool = False,
        body_pos: _TYPE_BODY_POSITION | None = None,
        preload_content: bool = True,
        decode_content: bool = True,
        **response_kw: typing.Any,
    )`
- `__init__(
        self,
        host: str,
        port: int | None = None,
        timeout: _TYPE_TIMEOUT | None = _DEFAULT_TIMEOUT,
        maxsize: int = 1,
        block: bool = False,
        headers: typing.Mapping[str, str] | None = None,
        retries: Retry | bool | int | None = None,
        _proxy: Url | None = None,
        _proxy_headers: typing.Mapping[str, str] | None = None,
        key_file: str | None = None,
        cert_file: str | None = None,
        cert_reqs: int | str | None = None,
        key_password: str | None = None,
        ca_certs: str | None = None,
        ssl_version: int | str | None = None,
        ssl_minimum_version: ssl.TLSVersion | None = None,
        ssl_maximum_version: ssl.TLSVersion | None = None,
        assert_hostname: str | typing.Literal[False] | None = None,
        assert_fingerprint: str | None = None,
        ca_cert_dir: str | None = None,
        **conn_kw: typing.Any,
    )`
- `_prepare_proxy(self, conn: HTTPSConnection)`
- `_new_conn(self)`
- `_validate_conn(self, conn: BaseHTTPConnection)`
- `connection_from_url(url: str, **kw: typing.Any)`
- `_normalize_host(host: None, scheme: str | None)`
- `_normalize_host(host: str, scheme: str | None)`
- `_normalize_host(host: str | None, scheme: str | None)`
- `_url_from_pool(
    pool: HTTPConnectionPool | HTTPSConnectionPool, path: str | None = None
)`
- `_close_pool_connections(pool: queue.LifoQueue[typing.Any])`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/__init__.py`

#### Functions
- `inject_into_urllib3()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/connection.py`

#### Classes
- `EmscriptenHTTPConnection`
- `EmscriptenHTTPSConnection`

#### Functions
- `__init__(
        self,
        host: str,
        port: int = 0,
        *,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        source_address: tuple[str, int] | None = None,
        blocksize: int = 8192,
        socket_options: _TYPE_SOCKET_OPTIONS | None = None,
        proxy: Url | None = None,
        proxy_config: ProxyConfig | None = None,
    )`
- `set_tunnel(
        self,
        host: str,
        port: int | None = 0,
        headers: typing.Mapping[str, str] | None = None,
        scheme: str = "http",
    )`
- `connect(self)`
- `request(
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        # We know *at least* botocore is depending on the order of the
        # first 3 parameters so to be safe we only mark the later ones
        # as keyword-only to ensure we have space to extend.
        *,
        chunked: bool = False,
        preload_content: bool = True,
        decode_content: bool = True,
        enforce_content_length: bool = True,
    )`
- `getresponse(self)`
- `close(self)`
- `is_closed(self)`
- `is_connected(self)`
- `has_connected_to_proxy(self)`
- `__init__(
        self,
        host: str,
        port: int = 0,
        *,
        timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        source_address: tuple[str, int] | None = None,
        blocksize: int = 16384,
        socket_options: (
            None | _TYPE_SOCKET_OPTIONS
        )`
- `set_cert(
        self,
        key_file: str | None = None,
        cert_file: str | None = None,
        cert_reqs: int | str | None = None,
        key_password: str | None = None,
        ca_certs: str | None = None,
        assert_hostname: None | str | typing.Literal[False] = None,
        assert_fingerprint: str | None = None,
        ca_cert_dir: str | None = None,
        ca_cert_data: None | str | bytes = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/fetch.py`

#### Classes
- `_RequestError`
- `_StreamingError`
- `_TimeoutError`
- `_ReadStream`
- `_StreamingFetcher`
- `_JSPIReadStream`

#### Functions
- `__init__(
        self,
        message: str | None = None,
        *,
        request: EmscriptenRequest | None = None,
        response: EmscriptenResponse | None = None,
    )`
- `_obj_from_dict(dict_val: dict[str, Any])`
- `__init__(
        self,
        int_buffer: JsArray,
        byte_buffer: JsArray,
        timeout: float,
        worker: JsProxy,
        connection_id: int,
        request: EmscriptenRequest,
    )`
- `__del__(self)`
- `is_closed(self)`
- `closed(self)`
- `close(self)`
- `readable(self)`
- `writable(self)`
- `seekable(self)`
- `readinto(self, byte_obj: Buffer)`
- `__init__(self)`
- `promise_resolver(js_resolve_fn: JsProxy, js_reject_fn: JsProxy)`
- `onMsg(e: JsProxy)`
- `onErr(e: JsProxy)`
- `send(self, request: EmscriptenRequest)`
- `__init__(
        self,
        js_read_stream: Any,
        timeout: float,
        request: EmscriptenRequest,
        response: EmscriptenResponse,
        js_abort_controller: Any,  # JavaScript AbortController for timeouts
    )`
- `__del__(self)`
- `is_closed(self)`
- `closed(self)`
- `close(self)`
- `readable(self)`
- `writable(self)`
- `seekable(self)`
- `_get_next_buffer(self)`
- `readinto(self, byte_obj: Buffer)`
- `is_in_browser_main_thread()`
- `is_cross_origin_isolated()`
- `is_in_node()`
- `is_worker_available()`
- `send_streaming_request(request: EmscriptenRequest)`
- `_show_timeout_warning()`
- `_show_streaming_warning()`
- `send_request(request: EmscriptenRequest)`
- `send_jspi_request(
    request: EmscriptenRequest, streaming: bool
)`
- `_run_sync_with_timeout(
    promise: Any,
    timeout: float,
    js_abort_controller: Any,
    request: EmscriptenRequest | None,
    response: EmscriptenResponse | None,
)`
- `has_jspi()`
- `_is_node_js()`
- `streaming_ready()`

#### Parameters / Constants
- `HEADERS_TO_IGNORE` = `("user-agent",)`
- `SUCCESS_HEADER` = `-1`
- `SUCCESS_EOF` = `-2`
- `ERROR_TIMEOUT` = `-3`
- `ERROR_EXCEPTION` = `-4`
- `NODE_JSPI_ERROR` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/request.py`

#### Classes
- `EmscriptenRequest`

#### Functions
- `set_header(self, name: str, value: str)`
- `set_body(self, body: _TYPE_BODY | None)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/emscripten/response.py`

#### Classes
- `EmscriptenResponse`
- `EmscriptenHttpResponseWrapper`

#### Functions
- `__init__(
        self,
        internal_response: EmscriptenResponse,
        url: str | None = None,
        connection: BaseHTTPConnection | BaseHTTPSConnection | None = None,
    )`
- `url(self)`
- `url(self, url: str | None)`
- `connection(self)`
- `retries(self)`
- `retries(self, retries: Retry | None)`
- `stream(
        self, amt: int | None = 2**16, decode_content: bool | None = None
    )`
- `_init_length(self, request_method: str | None)`
- `read(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,  # ignored because browser decodes always
        cache_content: bool = False,
    )`
- `read_chunked(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,
    )`
- `release_conn(self)`
- `drain_conn(self)`
- `data(self)`
- `json(self)`
- `close(self)`
- `_error_catcher(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/pyopenssl.py`

#### Classes
- `UnsupportedExtension`
- `WrappedSocket`
- `PyOpenSSLContext`

#### Functions
- `inject_into_urllib3()`
- `extract_from_urllib3()`
- `_validate_dependencies_met()`
- `_dnsname_to_stdlib(name: str)`
- `idna_encode(name: str)`
- `get_subj_alt_name(peer_cert: X509)`
- `__init__(
        self,
        connection: OpenSSL.SSL.Connection,
        socket: socket_cls,
        suppress_ragged_eofs: bool = True,
    )`
- `fileno(self)`
- `_decref_socketios(self)`
- `recv(self, *args: typing.Any, **kwargs: typing.Any)`
- `recv_into(self, *args: typing.Any, **kwargs: typing.Any)`
- `settimeout(self, timeout: float)`
- `_send_until_done(self, data: bytes)`
- `sendall(self, data: bytes)`
- `shutdown(self, how: int)`
- `close(self)`
- `_real_close(self)`
- `getpeercert(
        self, binary_form: bool = False
    )`
- `version(self)`
- `selected_alpn_protocol(self)`
- `__init__(self, protocol: int)`
- `options(self)`
- `options(self, value: int)`
- `verify_flags(self)`
- `verify_flags(self, value: int)`
- `verify_mode(self)`
- `verify_mode(self, value: ssl.VerifyMode)`
- `set_default_verify_paths(self)`
- `set_ciphers(self, ciphers: bytes | str)`
- `load_verify_locations(
        self,
        cafile: str | None = None,
        capath: str | None = None,
        cadata: bytes | None = None,
    )`
- `load_cert_chain(
        self,
        certfile: str,
        keyfile: str | None = None,
        password: str | None = None,
    )`
- `set_alpn_protocols(self, protocols: list[bytes | str])`
- `wrap_socket(
        self,
        sock: socket_cls,
        server_side: bool = False,
        do_handshake_on_connect: bool = True,
        suppress_ragged_eofs: bool = True,
        server_hostname: bytes | str | None = None,
    )`
- `_set_ctx_options(self)`
- `minimum_version(self)`
- `minimum_version(self, minimum_version: int)`
- `maximum_version(self)`
- `maximum_version(self, maximum_version: int)`
- `_verify_callback(
    cnx: OpenSSL.SSL.Connection,
    x509: X509,
    err_no: int,
    err_depth: int,
    return_code: int,
)`

#### Parameters / Constants
- `SSL_WRITE_BLOCKSIZE` = `16384`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/contrib/socks.py`

#### Classes
- `_TYPE_SOCKS_OPTIONS`
- `SOCKSConnection`
- `SOCKSHTTPSConnection`
- `SOCKSHTTPConnectionPool`
- `SOCKSHTTPSConnectionPool`
- `SOCKSProxyManager`

#### Functions
- `__init__(
        self,
        _socks_options: _TYPE_SOCKS_OPTIONS,
        *args: typing.Any,
        **kwargs: typing.Any,
    )`
- `_new_conn(self)`
- `__init__(
        self,
        proxy_url: str,
        username: str | None = None,
        password: str | None = None,
        num_pools: int = 10,
        headers: typing.Mapping[str, str] | None = None,
        **connection_pool_kw: typing.Any,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/exceptions.py`

#### Classes
- `HTTPError`
- `HTTPWarning`
- `PoolError`
- `RequestError`
- `SSLError`
- `ProxyError`
- `DecodeError`
- `ProtocolError`
- `MaxRetryError`
- `HostChangedError`
- `TimeoutStateError`
- `TimeoutError`
- `ReadTimeoutError`
- `ConnectTimeoutError`
- `NewConnectionError`
- `NameResolutionError`
- `EmptyPoolError`
- `FullPoolError`
- `ClosedPoolError`
- `LocationValueError`
- `LocationParseError`
- `URLSchemeUnknown`
- `ResponseError`
- `SecurityWarning`
- `InsecureRequestWarning`
- `NotOpenSSLWarning`
- `SystemTimeWarning`
- `InsecurePlatformWarning`
- `DependencyWarning`
- `ResponseNotChunked`
- `BodyNotHttplibCompatible`
- `IncompleteRead`
- `InvalidChunkLength`
- `InvalidHeader`
- `ProxySchemeUnknown`
- `ProxySchemeUnsupported`
- `HeaderParsingError`
- `UnrewindableBodyError`

#### Functions
- `__init__(self, pool: ConnectionPool, message: str)`
- `__reduce__(self)`
- `__init__(self, pool: ConnectionPool, url: str | None, message: str)`
- `__reduce__(self)`
- `__init__(self, message: str, error: Exception)`
- `__init__(
        self, pool: ConnectionPool, url: str | None, reason: Exception | None = None
    )`
- `__reduce__(self)`
- `__init__(
        self, pool: ConnectionPool, url: str, retries: Retry | int = 3
    )`
- `__init__(self, conn: HTTPConnection, message: str)`
- `__reduce__(self)`
- `pool(self)`
- `__init__(self, host: str, conn: HTTPConnection, reason: socket.gaierror)`
- `__reduce__(self)`
- `__init__(self, location: str)`
- `__init__(self, scheme: str)`
- `__init__(self, partial: int, expected: int)`
- `__repr__(self)`
- `__init__(self, response: HTTPResponse, length: bytes)`
- `__repr__(self)`
- `__init__(self, scheme: str | None)`
- `__init__(
        self, defects: list[MessageDefect], unparsed_data: bytes | str | None
    )`

#### Parameters / Constants
- `GENERIC_ERROR` = `"too many error responses"`
- `SPECIFIC_ERROR` = `"too many {status_code} error responses"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/fields.py`

#### Classes
- `RequestField`

#### Functions
- `guess_content_type(
    filename: str | None, default: str = "application/octet-stream"
)`
- `format_header_param_rfc2231(name: str, value: _TYPE_FIELD_VALUE)`
- `format_multipart_header_param(name: str, value: _TYPE_FIELD_VALUE)`
- `format_header_param_html5(name: str, value: _TYPE_FIELD_VALUE)`
- `format_header_param(name: str, value: _TYPE_FIELD_VALUE)`
- `__init__(
        self,
        name: str,
        data: _TYPE_FIELD_VALUE,
        filename: str | None = None,
        headers: typing.Mapping[str, str] | None = None,
        header_formatter: typing.Callable[[str, _TYPE_FIELD_VALUE], str] | None = None,
    )`
- `from_tuples(
        cls,
        fieldname: str,
        value: _TYPE_FIELD_VALUE_TUPLE,
        header_formatter: typing.Callable[[str, _TYPE_FIELD_VALUE], str] | None = None,
    )`
- `_render_part(self, name: str, value: _TYPE_FIELD_VALUE)`
- `_render_parts(
        self,
        header_parts: (
            dict[str, _TYPE_FIELD_VALUE | None]
            | typing.Sequence[tuple[str, _TYPE_FIELD_VALUE | None]]
        )`
- `render_headers(self)`
- `make_multipart(
        self,
        content_disposition: str | None = None,
        content_type: str | None = None,
        content_location: str | None = None,
    )`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/filepost.py`

#### Functions
- `choose_boundary()`
- `iter_field_objects(fields: _TYPE_FIELDS)`
- `encode_multipart_formdata(
    fields: _TYPE_FIELDS, boundary: str | None = None
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/http2/__init__.py`

#### Functions
- `inject_into_urllib3()`
- `extract_from_urllib3()`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/http2/connection.py`

#### Classes
- `_LockedObject`
- `HTTP2Connection`
- `HTTP2Response`

#### Functions
- `_is_legal_header_name(name: bytes)`
- `_is_illegal_header_value(value: bytes)`
- `__init__(self, obj: T)`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    )`
- `__init__(
        self, host: str, port: int | None = None, **kwargs: typing.Any
    )`
- `_new_h2_conn(self)`
- `connect(self)`
- `putrequest(  # type: ignore[override]
        self,
        method: str,
        url: str,
        **kwargs: typing.Any,
    )`
- `putheader(self, header: str | bytes, *values: str | bytes)`
- `endheaders(self, message_body: typing.Any = None)`
- `send(self, data: typing.Any)`
- `set_tunnel(
        self,
        host: str,
        port: int | None = None,
        headers: typing.Mapping[str, str] | None = None,
        scheme: str = "http",
    )`
- `getresponse(  # type: ignore[override]
        self,
    )`
- `request(  # type: ignore[override]
        self,
        method: str,
        url: str,
        body: _TYPE_BODY | None = None,
        headers: typing.Mapping[str, str] | None = None,
        *,
        preload_content: bool = True,
        decode_content: bool = True,
        enforce_content_length: bool = True,
        **kwargs: typing.Any,
    )`
- `close(self)`
- `__init__(
        self,
        status: int,
        headers: HTTPHeaderDict,
        request_url: str,
        data: bytes,
        decode_content: bool = False,  # TODO: support decoding
    )`
- `data(self)`
- `get_redirect_location(self)`
- `close(self)`

#### Parameters / Constants
- `RE_IS_LEGAL_HEADER_NAME` = `re.compile(rb"^[!#$%&'*+\-.^_`|~0-9a-z]+$")`
- `RE_IS_ILLEGAL_HEADER_VALUE` = `re.compile(rb"[\0\x00\x0a\x0d\r\n]|^[ \r\n\t]|[ \r\n\t]$")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/http2/probe.py`

#### Classes
- `_HTTP2ProbeCache`

#### Functions
- `__init__(self)`
- `acquire_and_get(self, host: str, port: int)`
- `set_and_release(
        self, host: str, port: int, supports_http2: bool | None
    )`
- `_values(self)`
- `_reset(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/poolmanager.py`

#### Classes
- `PoolKey`
- `PoolManager`
- `ProxyManager`

#### Functions
- `_default_key_normalizer(
    key_class: type[PoolKey], request_context: dict[str, typing.Any]
)`
- `__init__(
        self,
        num_pools: int = 10,
        headers: typing.Mapping[str, str] | None = None,
        **connection_pool_kw: typing.Any,
    )`
- `__enter__(self)`
- `__exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    )`
- `_new_pool(
        self,
        scheme: str,
        host: str,
        port: int,
        request_context: dict[str, typing.Any] | None = None,
    )`
- `clear(self)`
- `connection_from_host(
        self,
        host: str | None,
        port: int | None = None,
        scheme: str | None = "http",
        pool_kwargs: dict[str, typing.Any] | None = None,
    )`
- `connection_from_context(
        self, request_context: dict[str, typing.Any]
    )`
- `connection_from_pool_key(
        self, pool_key: PoolKey, request_context: dict[str, typing.Any]
    )`
- `connection_from_url(
        self, url: str, pool_kwargs: dict[str, typing.Any] | None = None
    )`
- `_merge_pool_kwargs(
        self, override: dict[str, typing.Any] | None
    )`
- `_proxy_requires_url_absolute_form(self, parsed_url: Url)`
- `urlopen(  # type: ignore[override]
        self, method: str, url: str, redirect: bool = True, **kw: typing.Any
    )`
- `__init__(
        self,
        proxy_url: str,
        num_pools: int = 10,
        headers: typing.Mapping[str, str] | None = None,
        proxy_headers: typing.Mapping[str, str] | None = None,
        proxy_ssl_context: ssl.SSLContext | None = None,
        use_forwarding_for_https: bool = False,
        proxy_assert_hostname: None | str | typing.Literal[False] = None,
        proxy_assert_fingerprint: str | None = None,
        **connection_pool_kw: typing.Any,
    )`
- `connection_from_host(
        self,
        host: str | None,
        port: int | None = None,
        scheme: str | None = "http",
        pool_kwargs: dict[str, typing.Any] | None = None,
    )`
- `_set_proxy_headers(
        self, url: str, headers: typing.Mapping[str, str] | None = None
    )`
- `urlopen(  # type: ignore[override]
        self, method: str, url: str, redirect: bool = True, **kw: typing.Any
    )`
- `proxy_from_url(url: str, **kw: typing.Any)`

#### Parameters / Constants
- `SSL_KEYWORDS` = `(`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/response.py`

#### Classes
- `ContentDecoder`
- `DeflateDecoder`
- `GzipDecoderState`
- `GzipDecoder`
- `BrotliDecoder`
- `ZstdDecoder`
- `MultiDecoder`
- `BytesQueueBuffer`
- `BaseHTTPResponse`
- `HTTPResponse`
- `is`

#### Functions
- `decompress(self, data: bytes, max_length: int = -1)`
- `has_unconsumed_tail(self)`
- `flush(self)`
- `__init__(self)`
- `decompress(self, data: bytes, max_length: int = -1)`
- `has_unconsumed_tail(self)`
- `flush(self)`
- `__init__(self)`
- `decompress(self, data: bytes, max_length: int = -1)`
- `has_unconsumed_tail(self)`
- `flush(self)`
- `__init__(self)`
- `_decompress(self, data: bytes, output_buffer_limit: int = -1)`
- `decompress(self, data: bytes, max_length: int = -1)`
- `has_unconsumed_tail(self)`
- `flush(self)`
- `__init__(self)`
- `decompress(self, data: bytes, max_length: int = -1)`
- `has_unconsumed_tail(self)`
- `flush(self)`
- `__init__(self, modes: str)`
- `flush(self)`
- `decompress(self, data: bytes, max_length: int = -1)`
- `has_unconsumed_tail(self)`
- `_get_decoder(mode: str)`
- `__init__(self)`
- `__len__(self)`
- `put(self, data: bytes)`
- `get(self, n: int)`
- `get_all(self)`
- `__init__(
        self,
        *,
        headers: typing.Mapping[str, str] | typing.Mapping[bytes, bytes] | None = None,
        status: int,
        version: int,
        version_string: str,
        reason: str | None,
        decode_content: bool,
        request_url: str | None,
        retries: Retry | None = None,
    )`
- `get_redirect_location(self)`
- `data(self)`
- `json(self)`
- `url(self)`
- `url(self, url: str | None)`
- `connection(self)`
- `retries(self)`
- `retries(self, retries: Retry | None)`
- `stream(
        self, amt: int | None = 2**16, decode_content: bool | None = None
    )`
- `read(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,
        cache_content: bool = False,
    )`
- `read1(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,
    )`
- `read_chunked(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,
    )`
- `release_conn(self)`
- `drain_conn(self)`
- `shutdown(self)`
- `close(self)`
- `_init_decoder(self)`
- `_decode(
        self,
        data: bytes,
        decode_content: bool | None,
        flush_decoder: bool,
        max_length: int | None = None,
    )`
- `_flush_decoder(self)`
- `readinto(self, b: bytearray)`
- `getheaders(self)`
- `getheader(self, name: str, default: str | None = None)`
- `info(self)`
- `geturl(self)`
- `__init__(
        self,
        body: _TYPE_BODY = "",
        headers: typing.Mapping[str, str] | typing.Mapping[bytes, bytes] | None = None,
        status: int = 0,
        version: int = 0,
        version_string: str = "HTTP/?",
        reason: str | None = None,
        preload_content: bool = True,
        decode_content: bool = True,
        original_response: _HttplibHTTPResponse | None = None,
        pool: HTTPConnectionPool | None = None,
        connection: HTTPConnection | None = None,
        msg: _HttplibHTTPMessage | None = None,
        retries: Retry | None = None,
        enforce_content_length: bool = True,
        request_method: str | None = None,
        request_url: str | None = None,
        auto_close: bool = True,
        sock_shutdown: typing.Callable[[int], None] | None = None,
    )`
- `release_conn(self)`
- `drain_conn(self)`
- `data(self)`
- `connection(self)`
- `isclosed(self)`
- `tell(self)`
- `_init_length(self, request_method: str | None)`
- `_error_catcher(self)`
- `_fp_read(
        self,
        amt: int | None = None,
        *,
        read1: bool = False,
    )`
- `_raw_read(
        self,
        amt: int | None = None,
        *,
        read1: bool = False,
    )`
- `read(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,
        cache_content: bool = False,
    )`
- `read1(
        self,
        amt: int | None = None,
        decode_content: bool | None = None,
    )`
- `stream(
        self, amt: int | None = 2**16, decode_content: bool | None = None
    )`
- `readable(self)`
- `shutdown(self)`
- `close(self)`
- `closed(self)`
- `fileno(self)`
- `flush(self)`
- `supports_chunked_reads(self)`
- `_update_chunk_length(self)`
- `_handle_chunk(self, amt: int | None)`
- `read_chunked(
        self, amt: int | None = None, decode_content: bool | None = None
    )`
- `url(self)`
- `url(self, url: str | None)`
- `__iter__(self)`

#### Parameters / Constants
- `FIRST_MEMBER` = `0`
- `OTHER_MEMBERS` = `1`
- `SWALLOW_DATA` = `2`
- `HAS_ZSTD` = `False`
- `HAS_ZSTD` = `True`
- `CONTENT_DECODERS` = `["gzip", "x-gzip", "deflate"]`
- `REDIRECT_STATUSES` = `[301, 302, 303, 307, 308]`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/connection.py`

#### Functions
- `is_connection_dropped(conn: BaseHTTPConnection)`
- `create_connection(
    address: tuple[str, int],
    timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
    source_address: tuple[str, int] | None = None,
    socket_options: _TYPE_SOCKET_OPTIONS | None = None,
)`
- `_set_socket_options(
    sock: socket.socket, options: _TYPE_SOCKET_OPTIONS | None
)`
- `allowed_gai_family()`
- `_has_ipv6(host: str)`

#### Parameters / Constants
- `HAS_IPV6` = `_has_ipv6("::1")`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/proxy.py`

#### Functions
- `connection_requires_http_tunnel(
    proxy_url: Url | None = None,
    proxy_config: ProxyConfig | None = None,
    destination_scheme: str | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/request.py`

#### Classes
- `_TYPE_FAILEDTELL`
- `ChunksAndContentLength`

#### Functions
- `make_headers(
    keep_alive: bool | None = None,
    accept_encoding: bool | list[str] | str | None = None,
    user_agent: str | None = None,
    basic_auth: str | None = None,
    proxy_basic_auth: str | None = None,
    disable_cache: bool | None = None,
)`
- `set_file_position(
    body: typing.Any, pos: _TYPE_BODY_POSITION | None
)`
- `rewind_body(body: typing.IO[typing.AnyStr], body_pos: _TYPE_BODY_POSITION)`
- `body_to_chunks(
    body: typing.Any | None, method: str, blocksize: int
)`
- `chunk_readable()`

#### Parameters / Constants
- `SKIP_HEADER` = `"@@@SKIP_HEADER@@@"`
- `SKIPPABLE_HEADERS` = `frozenset(["accept-encoding", "host", "user-agent"])`
- `ACCEPT_ENCODING` = `"gzip,deflate"`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/response.py`

#### Functions
- `is_fp_closed(obj: object)`
- `assert_header_parsing(headers: httplib.HTTPMessage)`
- `is_response_to_head(response: httplib.HTTPResponse)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/retry.py`

#### Classes
- `RequestHistory`
- `Retry`

#### Functions
- `__init__(
        self,
        total: bool | int | None = 10,
        connect: int | None = None,
        read: int | None = None,
        redirect: bool | int | None = None,
        status: int | None = None,
        other: int | None = None,
        allowed_methods: typing.Collection[str] | None = DEFAULT_ALLOWED_METHODS,
        status_forcelist: typing.Collection[int] | None = None,
        backoff_factor: float = 0,
        backoff_max: float = DEFAULT_BACKOFF_MAX,
        raise_on_redirect: bool = True,
        raise_on_status: bool = True,
        history: tuple[RequestHistory, ...] | None = None,
        respect_retry_after_header: bool = True,
        remove_headers_on_redirect: typing.Collection[
            str
        ] = DEFAULT_REMOVE_HEADERS_ON_REDIRECT,
        backoff_jitter: float = 0.0,
        retry_after_max: int = DEFAULT_RETRY_AFTER_MAX,
    )`
- `new(self, **kw: typing.Any)`
- `from_int(
        cls,
        retries: Retry | bool | int | None,
        redirect: bool | int | None = True,
        default: Retry | bool | int | None = None,
    )`
- `get_backoff_time(self)`
- `parse_retry_after(self, retry_after: str)`
- `get_retry_after(self, response: BaseHTTPResponse)`
- `sleep_for_retry(self, response: BaseHTTPResponse)`
- `_sleep_backoff(self)`
- `sleep(self, response: BaseHTTPResponse | None = None)`
- `_is_connection_error(self, err: Exception)`
- `_is_read_error(self, err: Exception)`
- `_is_method_retryable(self, method: str)`
- `is_retry(
        self, method: str, status_code: int, has_retry_after: bool = False
    )`
- `is_exhausted(self)`
- `increment(
        self,
        method: str | None = None,
        url: str | None = None,
        response: BaseHTTPResponse | None = None,
        error: Exception | None = None,
        _pool: ConnectionPool | None = None,
        _stacktrace: TracebackType | None = None,
    )`
- `__repr__(self)`

#### Parameters / Constants
- `DEFAULT_ALLOWED_METHODS` = `frozenset(`
- `RETRY_AFTER_STATUS_CODES` = `frozenset([413, 429, 503])`
- `DEFAULT_REMOVE_HEADERS_ON_REDIRECT` = `frozenset(`
- `DEFAULT_BACKOFF_MAX` = `120`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/ssl_.py`

#### Classes
- `_TYPE_PEER_CERT_RET_DICT`

#### Functions
- `_is_bpo_43522_fixed(
    implementation_name: str,
    version_info: _TYPE_VERSION_INFO,
    pypy_version_info: _TYPE_VERSION_INFO | None,
)`
- `_is_has_never_check_common_name_reliable(
    openssl_version: str,
    openssl_version_number: int,
    implementation_name: str,
    version_info: _TYPE_VERSION_INFO,
    pypy_version_info: _TYPE_VERSION_INFO | None,
)`
- `assert_fingerprint(cert: bytes | None, fingerprint: str)`
- `resolve_cert_reqs(candidate: None | int | str)`
- `resolve_ssl_version(candidate: None | int | str)`
- `create_urllib3_context(
    ssl_version: int | None = None,
    cert_reqs: int | None = None,
    options: int | None = None,
    ciphers: str | None = None,
    ssl_minimum_version: int | None = None,
    ssl_maximum_version: int | None = None,
    verify_flags: int | None = None,
)`
- `ssl_wrap_socket(
    sock: socket.socket,
    keyfile: str | None = ...,
    certfile: str | None = ...,
    cert_reqs: int | None = ...,
    ca_certs: str | None = ...,
    server_hostname: str | None = ...,
    ssl_version: int | None = ...,
    ciphers: str | None = ...,
    ssl_context: ssl.SSLContext | None = ...,
    ca_cert_dir: str | None = ...,
    key_password: str | None = ...,
    ca_cert_data: None | str | bytes = ...,
    tls_in_tls: typing.Literal[False] = ...,
)`
- `ssl_wrap_socket(
    sock: socket.socket,
    keyfile: str | None = ...,
    certfile: str | None = ...,
    cert_reqs: int | None = ...,
    ca_certs: str | None = ...,
    server_hostname: str | None = ...,
    ssl_version: int | None = ...,
    ciphers: str | None = ...,
    ssl_context: ssl.SSLContext | None = ...,
    ca_cert_dir: str | None = ...,
    key_password: str | None = ...,
    ca_cert_data: None | str | bytes = ...,
    tls_in_tls: bool = ...,
)`
- `ssl_wrap_socket(
    sock: socket.socket,
    keyfile: str | None = None,
    certfile: str | None = None,
    cert_reqs: int | None = None,
    ca_certs: str | None = None,
    server_hostname: str | None = None,
    ssl_version: int | None = None,
    ciphers: str | None = None,
    ssl_context: ssl.SSLContext | None = None,
    ca_cert_dir: str | None = None,
    key_password: str | None = None,
    ca_cert_data: None | str | bytes = None,
    tls_in_tls: bool = False,
)`
- `is_ipaddress(hostname: str | bytes)`
- `_is_key_file_encrypted(key_file: str)`
- `_ssl_wrap_socket_impl(
    sock: socket.socket,
    ssl_context: ssl.SSLContext,
    tls_in_tls: bool,
    server_hostname: str | None = None,
)`

#### Parameters / Constants
- `HAS_NEVER_CHECK_COMMON_NAME` = `False`
- `IS_PYOPENSSL` = `False`
- `ALPN_PROTOCOLS` = `["http/1.1"]`
- `HASHFUNC_MAP` = `{`
- `VERIFY_X509_PARTIAL_CHAIN` = `getattr(ssl, "VERIFY_X509_PARTIAL_CHAIN", 0x80000)`
- `HAS_NEVER_CHECK_COMMON_NAME` = `False`
- `OP_NO_COMPRESSION` = `0x20000  # type: ignore[assignment, misc]`
- `OP_NO_TICKET` = `0x4000  # type: ignore[assignment, misc]`
- `PROTOCOL_TLS_CLIENT` = `16  # type: ignore[assignment, misc]`
- `VERIFY_X509_PARTIAL_CHAIN` = `0x80000`
- `VERIFY_X509_STRICT` = `0x20  # type: ignore[assignment, misc]`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/ssl_match_hostname.py`

#### Classes
- `CertificateError`

#### Functions
- `_dnsname_match(
    dn: typing.Any, hostname: str, max_wildcards: int = 1
)`
- `_ipaddress_match(ipname: str, host_ip: IPv4Address | IPv6Address)`
- `match_hostname(
    cert: _TYPE_PEER_CERT_RET_DICT | None,
    hostname: str,
    hostname_checks_common_name: bool = False,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/ssltransport.py`

#### Classes
- `SSLTransport`

#### Functions
- `_validate_ssl_context_for_tls_in_tls(ssl_context: ssl.SSLContext)`
- `__init__(
        self,
        socket: socket.socket,
        ssl_context: ssl.SSLContext,
        server_hostname: str | None = None,
        suppress_ragged_eofs: bool = True,
    )`
- `__enter__(self)`
- `__exit__(self, *_: typing.Any)`
- `fileno(self)`
- `read(self, len: int = 1024, buffer: typing.Any | None = None)`
- `recv(self, buflen: int = 1024, flags: int = 0)`
- `recv_into(
        self,
        buffer: _WriteBuffer,
        nbytes: int | None = None,
        flags: int = 0,
    )`
- `sendall(self, data: bytes, flags: int = 0)`
- `send(self, data: bytes, flags: int = 0)`
- `makefile(
        self,
        mode: str,
        buffering: int | None = None,
        *,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    )`
- `unwrap(self)`
- `close(self)`
- `getpeercert(
        self, binary_form: typing.Literal[False] = ...
    )`
- `getpeercert(self, binary_form: typing.Literal[True])`
- `getpeercert(self, binary_form: bool = False)`
- `version(self)`
- `cipher(self)`
- `selected_alpn_protocol(self)`
- `shared_ciphers(self)`
- `compression(self)`
- `settimeout(self, value: float | None)`
- `gettimeout(self)`
- `_decref_socketios(self)`
- `_wrap_ssl_read(self, len: int, buffer: bytearray | None = None)`
- `_ssl_io_loop(self, func: typing.Callable[[], None])`
- `_ssl_io_loop(self, func: typing.Callable[[bytes], int], arg1: bytes)`
- `_ssl_io_loop(
        self,
        func: typing.Callable[[int, bytearray | None], bytes],
        arg1: int,
        arg2: bytearray | None,
    )`
- `_ssl_io_loop(
        self,
        func: typing.Callable[..., _ReturnValue],
        arg1: None | bytes | int = None,
        arg2: bytearray | None = None,
    )`

#### Parameters / Constants
- `SSL_BLOCKSIZE` = `16384`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/timeout.py`

#### Classes
- `_TYPE_DEFAULT`
- `Timeout`

#### Functions
- `__init__(
        self,
        total: _TYPE_TIMEOUT = None,
        connect: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
        read: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT,
    )`
- `__repr__(self)`
- `resolve_default_timeout(timeout: _TYPE_TIMEOUT)`
- `_validate_timeout(cls, value: _TYPE_TIMEOUT, name: str)`
- `from_float(cls, timeout: _TYPE_TIMEOUT)`
- `clone(self)`
- `start_connect(self)`
- `get_connect_duration(self)`
- `connect_timeout(self)`
- `read_timeout(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/url.py`

#### Classes
- `Url`

#### Functions
- `__new__(  # type: ignore[no-untyped-def]
        cls,
        scheme: str | None = None,
        auth: str | None = None,
        host: str | None = None,
        port: int | None = None,
        path: str | None = None,
        query: str | None = None,
        fragment: str | None = None,
    )`
- `hostname(self)`
- `request_uri(self)`
- `authority(self)`
- `netloc(self)`
- `url(self)`
- `__str__(self)`
- `_encode_invalid_chars(
    component: str, allowed_chars: typing.Container[str]
)`
- `_encode_invalid_chars(
    component: None, allowed_chars: typing.Container[str]
)`
- `_encode_invalid_chars(
    component: str | None, allowed_chars: typing.Container[str]
)`
- `_remove_path_dot_segments(path: str)`
- `_normalize_host(host: None, scheme: str | None)`
- `_normalize_host(host: str, scheme: str | None)`
- `_normalize_host(host: str | None, scheme: str | None)`
- `_idna_encode(name: str)`
- `_encode_target(target: str)`
- `parse_url(url: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/util.py`

#### Functions
- `to_bytes(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
)`
- `to_str(
    x: str | bytes, encoding: str | None = None, errors: str | None = None
)`
- `reraise(
    tp: type[BaseException] | None,
    value: BaseException,
    tb: TracebackType | None = None,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pip/_vendor/urllib3/util/wait.py`

#### Functions
- `select_wait_for_socket(
    sock: socket.socket,
    read: bool = False,
    write: bool = False,
    timeout: float | None = None,
)`
- `poll_wait_for_socket(
    sock: socket.socket,
    read: bool = False,
    write: bool = False,
    timeout: float | None = None,
)`
- `do_poll(t: float | None)`
- `_have_working_poll()`
- `wait_for_socket(
    sock: socket.socket,
    read: bool = False,
    write: bool = False,
    timeout: float | None = None,
)`
- `wait_for_read(sock: socket.socket, timeout: float | None = None)`
- `wait_for_write(sock: socket.socket, timeout: float | None = None)`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_callers.py`

#### Functions
- `run_old_style_hookwrapper(
    hook_impl: HookImpl, hook_name: str, args: Sequence[object]
)`
- `_raise_wrapfail(
    wrap_controller: Generator[None, object, object],
    msg: str,
)`
- `_warn_teardown_exception(
    hook_name: str, hook_impl: HookImpl, e: BaseException
)`
- `_multicall(
    hook_name: str,
    hook_impls: Sequence[HookImpl],
    caller_kwargs: Mapping[str, object],
    firstresult: bool,
)`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_hooks.py`

#### Classes
- `HookspecOpts`
- `HookimplOpts`
- `HookspecMarker`
- `HookimplMarker`
- `HookRelay`
- `HookCaller`
- `_SubsetHookCaller`
- `HookImpl`
- `HookSpec`

#### Functions
- `__init__(self, project_name: str)`
- `__call__(
        self,
        function: _F,
        firstresult: bool = False,
        historic: bool = False,
        warn_on_impl: Warning | None = None,
        warn_on_impl_args: Mapping[str, Warning] | None = None,
    )`
- `__call__(  # noqa: F811
        self,
        function: None = ...,
        firstresult: bool = ...,
        historic: bool = ...,
        warn_on_impl: Warning | None = ...,
        warn_on_impl_args: Mapping[str, Warning] | None = ...,
    )`
- `__call__(  # noqa: F811
        self,
        function: _F | None = None,
        firstresult: bool = False,
        historic: bool = False,
        warn_on_impl: Warning | None = None,
        warn_on_impl_args: Mapping[str, Warning] | None = None,
    )`
- `setattr_hookspec_opts(func: _F)`
- `__init__(self, project_name: str)`
- `__call__(
        self,
        function: _F,
        hookwrapper: bool = ...,
        optionalhook: bool = ...,
        tryfirst: bool = ...,
        trylast: bool = ...,
        specname: str | None = ...,
        wrapper: bool = ...,
    )`
- `__call__(  # noqa: F811
        self,
        function: None = ...,
        hookwrapper: bool = ...,
        optionalhook: bool = ...,
        tryfirst: bool = ...,
        trylast: bool = ...,
        specname: str | None = ...,
        wrapper: bool = ...,
    )`
- `__call__(  # noqa: F811
        self,
        function: _F | None = None,
        hookwrapper: bool = False,
        optionalhook: bool = False,
        tryfirst: bool = False,
        trylast: bool = False,
        specname: str | None = None,
        wrapper: bool = False,
    )`
- `setattr_hookimpl_opts(func: _F)`
- `normalize_hookimpl_opts(opts: HookimplOpts)`
- `varnames(func: object)`
- `__init__(self)`
- `__getattr__(self, name: str)`
- `__init__(
        self,
        name: str,
        hook_execute: _HookExec,
        specmodule_or_class: _Namespace | None = None,
        spec_opts: HookspecOpts | None = None,
    )`
- `has_spec(self)`
- `set_specification(
        self,
        specmodule_or_class: _Namespace,
        spec_opts: HookspecOpts,
    )`
- `is_historic(self)`
- `_remove_plugin(self, plugin: _Plugin)`
- `get_hookimpls(self)`
- `_add_hookimpl(self, hookimpl: HookImpl)`
- `__repr__(self)`
- `_verify_all_args_are_provided(self, kwargs: Mapping[str, object])`
- `__call__(self, **kwargs: object)`
- `call_historic(
        self,
        result_callback: Callable[[Any], None] | None = None,
        kwargs: Mapping[str, object] | None = None,
    )`
- `call_extra(
        self, methods: Sequence[Callable[..., object]], kwargs: Mapping[str, object]
    )`
- `_maybe_apply_history(self, method: HookImpl)`
- `__init__(self, orig: HookCaller, remove_plugins: Set[_Plugin])`
- `_hookimpls(self)`
- `spec(self)`
- `_call_history(self)`
- `__repr__(self)`
- `__init__(
        self,
        plugin: _Plugin,
        plugin_name: str,
        function: _HookImplFunction[object],
        hook_impl_opts: HookimplOpts,
    )`
- `__repr__(self)`
- `__init__(self, namespace: _Namespace, name: str, opts: HookspecOpts)`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_manager.py`

#### Classes
- `PluginValidationError`
- `DistFacade`
- `PluginManager`

#### Functions
- `_warn_for_function(warning: Warning, function: Callable[..., object])`
- `__init__(self, plugin: _Plugin, message: str)`
- `__init__(self, dist: importlib.metadata.Distribution)`
- `project_name(self)`
- `__getattr__(self, attr: str, default: Any | None = None)`
- `__dir__(self)`
- `__init__(self, project_name: str)`
- `_hookexec(
        self,
        hook_name: str,
        methods: Sequence[HookImpl],
        kwargs: Mapping[str, object],
        firstresult: bool,
    )`
- `register(self, plugin: _Plugin, name: str | None = None)`
- `parse_hookimpl_opts(self, plugin: _Plugin, name: str)`
- `unregister(
        self, plugin: _Plugin | None = None, name: str | None = None
    )`
- `set_blocked(self, name: str)`
- `is_blocked(self, name: str)`
- `unblock(self, name: str)`
- `add_hookspecs(self, module_or_class: _Namespace)`
- `parse_hookspec_opts(
        self, module_or_class: _Namespace, name: str
    )`
- `get_plugins(self)`
- `is_registered(self, plugin: _Plugin)`
- `get_canonical_name(self, plugin: _Plugin)`
- `get_plugin(self, name: str)`
- `has_plugin(self, name: str)`
- `get_name(self, plugin: _Plugin)`
- `_verify_hook(self, hook: HookCaller, hookimpl: HookImpl)`
- `check_pending(self)`
- `load_setuptools_entrypoints(self, group: str, name: str | None = None)`
- `list_plugin_distinfo(self)`
- `list_name_plugin(self)`
- `get_hookcallers(self, plugin: _Plugin)`
- `add_hookcall_monitoring(
        self, before: _BeforeTrace, after: _AfterTrace
    )`
- `traced_hookexec(
            hook_name: str,
            hook_impls: Sequence[HookImpl],
            caller_kwargs: Mapping[str, object],
            firstresult: bool,
        )`
- `undo()`
- `enable_tracing(self)`
- `before(
            hook_name: str, methods: Sequence[HookImpl], kwargs: Mapping[str, object]
        )`
- `after(
            outcome: Result[object],
            hook_name: str,
            methods: Sequence[HookImpl],
            kwargs: Mapping[str, object],
        )`
- `subset_hook_caller(
        self, name: str, remove_plugins: Iterable[_Plugin]
    )`
- `_formatdef(func: Callable[..., object])`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_result.py`

#### Classes
- `HookCallError`
- `Result`

#### Functions
- `__init__(
        self,
        result: ResultType | None,
        exception: BaseException | None,
    )`
- `excinfo(self)`
- `exception(self)`
- `from_call(cls, func: Callable[[], ResultType])`
- `force_result(self, result: ResultType)`
- `force_exception(self, exception: BaseException)`
- `get_result(self)`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_tracing.py`

#### Classes
- `TagTracer`
- `TagTracerSub`

#### Functions
- `__init__(self)`
- `get(self, name: str)`
- `_format_message(self, tags: Sequence[str], args: Sequence[object])`
- `_processmessage(self, tags: tuple[str, ...], args: tuple[object, ...])`
- `setwriter(self, writer: _Writer | None)`
- `setprocessor(self, tags: str | tuple[str, ...], processor: _Processor)`
- `__init__(self, root: TagTracer, tags: tuple[str, ...])`
- `__call__(self, *args: object)`
- `get(self, name: str)`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_version.py`

#### Parameters / Constants
- `TYPE_CHECKING` = `False`
- `VERSION_TUPLE` = `Tuple[Union[int, str], ...]`
- `VERSION_TUPLE` = `object`

### FILE: `parity_env/lib/python3.14/site-packages/pluggy/_warnings.py`

#### Classes
- `PluggyWarning`
- `PluggyTeardownRaisedWarning`

### FILE: `parity_lab/AUTO_REPAIR_ALL.py`

#### Functions
- `say(x="")`
- `sha256(p)`
- `snapshot()`
- `backup_all()`
- `restore_all()`
- `run(cmd)`
- `count_mismatches(text)`
- `run_full_tests(label)`
- `replace_once(path, old, new, reason)`

#### Parameters / Constants
- `ROOT` = `Path.cwd()`
- `LAB` = `ROOT / "parity_lab"`
- `STAMP` = `datetime.now().strftime("%Y%m%d_%H%M%S")`
- `BACKUP` = `LAB / f"AUTO_REPAIR_BACKUP_{STAMP}"`
- `REPORT` = `LAB / f"AUTO_REPAIR_FINAL_{STAMP}.md"`
- `LOG` = `LAB / f"AUTO_REPAIR_LOG_{STAMP}.txt"`
- `TARGETS` = `[`
- `TESTS` = `[`

### FILE: `parity_lab/FORENSIC_AUTO_REPAIR.py`

#### Functions
- `say(x="")`
- `digest(p)`
- `snapshot()`
- `backup()`
- `restore()`
- `run(cmd, timeout=180)`
- `run_tools(tag)`
- `score(text)`
- `source_text()`
- `save_candidate(path, original)`
- `restore_candidate(path, original)`
- `apply_candidate(path, new_text, reason, evidence)`

#### Parameters / Constants
- `ROOT` = `Path.cwd()`
- `LAB` = `ROOT / "parity_lab"`
- `STAMP` = `datetime.now().strftime("%Y%m%d_%H%M%S")`
- `BACKUP` = `LAB / f"FORENSIC_BACKUP_{STAMP}"`
- `REPORT` = `LAB / f"FORENSIC_REPAIR_REPORT_{STAMP}.md"`
- `CONSOLE` = `LAB / f"FORENSIC_REPAIR_LOG_{STAMP}.txt"`
- `TARGETS` = `[`
- `SYMBOLS` = `["BNBUSDT", "DOGEUSDT", "ETHUSDT", "LTCUSDT"]`
- `TOOLS` = `[`
- `CURRENT_SCORE` = `[baseline_score]`

### FILE: `parity_lab/auto_parity_auditor.py`

#### Functions
- `issue(severity, area, problem, evidence, cause, fix)`
- `read(path)`
- `check_file(path)`
- `rows(path)`
- `csv_header(path)`

#### Parameters / Constants
- `ROOT` = `Path.cwd()`
- `LAB` = `ROOT / "parity_lab"`

### FILE: `parity_lab/deep_analyzer.py`

#### Functions
- `run(cmd)`
- `section(title)`

#### Parameters / Constants
- `ROOT` = `Path.home() / "dtm-new-bot"`
- `OUT` = `ROOT / "parity_lab" / "DEEP_ANALYSIS_REPORT.md"`
- `PY_FILES` = `list(ROOT.glob("*.py")) + list((ROOT / "parity_lab").glob("*.py"))`
- `CSV_FILES` = `sorted(ROOT.glob("pine_*.csv"))`

### FILE: `parity_lab/fast_spot_check.py`

#### Parameters / Constants
- `RAW` = `{`
- `PINE` = `{`
- `SIG` = `re.compile(r"🔔\s*(CD\+|CD-|HD\+|HD-)")`
- `CUR` = `re.compile(r"📌\s*کندل فعلی:\s*(\d+)")`

### FILE: `parity_lab/pine_pivot_price_locator.py`

#### Functions
- `nearest_price(raw, price, center, radius=30)`

#### Parameters / Constants
- `RAW` = `{`
- `PINE` = `{`
- `PAT_SIG` = `re.compile(r"🔔\s*(CD\+|CD-|HD\+|HD-)")`
- `PAT_CUR` = `re.compile(r"📌\s*کندل فعلی:\s*(\d+)")`
- `PAT_P1` = `re.compile(`
- `PAT_P2` = `re.compile(`

### FILE: `parity_lab/pine_timestamp_ohlc_check.py`

#### Parameters / Constants
- `RAW` = `{`
- `PINE` = `{`

### FILE: `strategy.py`

#### Functions
- `rma(s, length)`
- `ema(s, length)`
- `rsi(close, length=RSI_LEN)`
- `macd(close, fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIG)`
- `atr(high, low, close, length=14)`
- `pivot_high(high, left=LEFT_BARS, right=RIGHT_BARS)`
- `pivot_low(low, left=LEFT_BARS, right=RIGHT_BARS)`
- `calculate_signals(df)`

#### Parameters / Constants
- `LEFT_BARS` = `5`
- `RIGHT_BARS` = `3`
- `RSI_LEN` = `14`
- `MACD_FAST` = `12`
- `MACD_SLOW` = `26`
- `MACD_SIG` = `9`

### FILE: `web.py`

#### Functions
- `health()`

## FINAL REQUIREMENT

قبل از هر اصلاح، برای هر مورد باید مشخص شود: FILE → FUNCTION → PARAMETER → CURRENT BEHAVIOR → PINE BEHAVIOR → ROOT CAUSE → REQUIRED CHANGE → VERIFICATION TEST.

هدف نهایی فقط کم کردن تعداد mismatch نیست؛ هدف این است که bar identity، pivot، state، indicator، divergence، Fibonacci، candle filters، score و signal در سطح semantics با Pine یکسان شوند.