def multiply(a, b):
    return a * b

def safe_divide(a,b):    
    try:
        return a/b
    except ZeroDivisionError:
        return "Division par zéro impossible"