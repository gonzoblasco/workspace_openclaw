```python
def invoice_total(lines, discount_pct, tax_pct):
    subtotal = sum(qty * unit for qty, unit in lines)
    discount = subtotal * discount_pct / 100
    discounted_subtotal = subtotal - discount
    tax = discounted_subtotal * tax_pct / 100
    total = subtotal - discount + tax
    return round(total, 2)
```