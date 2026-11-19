def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("division por cero")
    return a / b
