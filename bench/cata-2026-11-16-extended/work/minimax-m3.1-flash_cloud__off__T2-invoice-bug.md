```python
def invoice_total(lines, discount_pct, tax_pct):
    subtotal = 0.0
    for qty, unit in lines:
        subtotal += qty * unit
    discount = subtotal * discount_pct / 100
    tax = (subtotal - discount) * tax_pct / 100
    return round(subtotal - discount + tax, 2)
```