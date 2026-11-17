Rows to consider (USD, in Q3, deduped):
- id 1: 120.50
- id 2: -30.00
- id 3: 99.99 (first occurrence)
- id 5: 0.00
- id 6: 45.25

Sum: 120.50 - 30.00 + 99.99 + 0.00 + 45.25 = 235.74

TOTAL: 235.74

Excluded/deduplicated rows:
- id 3 (second occurrence, 2026-08-01, USD, 99.99) — deduplicated (id already counted).
- id 4 (2026-08-20, EUR, 250.00) — excluded (non-USD currency).
- id 7 (2026-10-01, USD, 999.00) — excluded (date outside 2026-Q3).