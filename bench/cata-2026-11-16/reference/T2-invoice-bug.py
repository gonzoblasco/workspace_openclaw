def invoice_total(lines, discount_pct, tax_pct):
    subtotal = sum(qty * unit for qty, unit in lines)
    discount = subtotal * discount_pct / 100
    tax = (subtotal - discount) * tax_pct / 100
    return round(subtotal - discount + tax, 2)
