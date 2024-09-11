def multiply(a, b):
    return a * b

def safe_divide(a: int, b: int) -> float | None:
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return None