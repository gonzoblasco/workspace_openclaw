def invoice_total(lines, discount_pct, tax_pct):
    subtotal = 0.0
    for qty, unit in lines:
        line = round(qty * unit, 2)
        subtotal += line
    discount = round(subtotal * discount_pct / 100, 2)
    tax = round((subtotal - discount) * tax_pct / 100, 2)
    return round(subtotal - discount + tax, 2)
