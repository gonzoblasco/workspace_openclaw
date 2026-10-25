"""Adversarial probe (Agent B) - explores required edge cases, not a test file."""
from datetime import date
import traceback
import daterange as dr

def show(label, fn):
    try:
        print(f"{label} => {fn()!r}")
    except Exception as e:
        print(f"{label} => {type(e).__name__}: {e}")

print("--- add_months ---")
show("add_months(2023-01-31, 1)", lambda: dr.add_months(date(2023,1,31), 1))
show("add_months(2024-01-31, 1)", lambda: dr.add_months(date(2024,1,31), 1))
show("add_months(2023-03-31,-1)", lambda: dr.add_months(date(2023,3,31), -1))
show("add_months(2023-01-30, 1)", lambda: dr.add_months(date(2023,1,30), 1))
show("add_months(2023-01-15, 1)", lambda: dr.add_months(date(2023,1,15), 1))
show("add_months(2023-08-31, 1)", lambda: dr.add_months(date(2023,8,31), 1))
show("add_months(2023-03-31, 0)", lambda: dr.add_months(date(2023,3,31), 0))
show("add_months(2023-01-31, 120)", lambda: dr.add_months(date(2023,1,31), 120))
show("add_months(2023-01-31,-120)", lambda: dr.add_months(date(2023,1,31), -120))
show("add_months(2024-02-29, 12)", lambda: dr.add_months(date(2024,2,29), 12))
show("add_months(2023-12-31, 2)", lambda: dr.add_months(date(2023,12,31), 2))
show("add_months(2023-01-31,-1)", lambda: dr.add_months(date(2023,1,31), -1))

print("--- month_end ---")
for y, m in [(2024,2),(2023,2),(2023,4),(2023,12),(2023,0),(2023,13),(2023,-1),(2000,2),(1900,2)]:
    show(f"month_end({y},{m})", lambda y=y, m=m: dr.month_end(y, m))

print("--- is_leap ---")
for y in (2024, 2023, 1900, 2000, 2100, 2400):
    show(f"is_leap({y})", lambda y=y: dr.is_leap(y))

print("--- daterange ---")
show("daterange(same)", lambda: dr.daterange(date(2023,1,1), date(2023,1,1)))
show("daterange(inverted)", lambda: dr.daterange(date(2023,1,2), date(2023,1,1)))
show("single day count", lambda: len(dr.daterange(date(2023,1,1), date(2023,1,2))))
r = dr.daterange(date(2022,1,1), date(2025,1,1))
show("3-year count", lambda: len(r))
print("3-year first/last:", r[0], r[-1])
show("leap crossing 2024-02-01..2024-03-01 count", lambda: len(dr.daterange(date(2024,2,1), date(2024,3,1))))
show("leap crossing contains 29", lambda: date(2024,2,29) in dr.daterange(date(2024,2,1), date(2024,3,1)))
# big range: does it include duplicates / weird entries?
r2 = dr.daterange(date(2024,1,30), date(2024,3,5))
print("2024-01-30..2024-03-05 len:", len(r2))
print(r2[:8], "...", r2[-3:])
show("duplicates?", lambda: len(r2) != len(set(r2)))
show("sorted?", lambda: list(r2) == sorted(r2))

print("--- parse_iso ---")
for s in ("2023-13-01", "no-es-fecha", "", "2023-07-15", "2023-02-30", None):
    show(f"parse_iso({s!r})", lambda s=s: dr.parse_iso(s))
