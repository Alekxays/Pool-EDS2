import operations.basic_ops
import operations.advanced_ops

def do_op(a, b, c):
    if c == '+':
        return operations.basic_ops.add(a, b)
    elif c == '-':
        return operations.basic_ops.subtract(a, b)
    elif c == '*':
        return operations.advanced_ops.multiply(a, b)
    elif c == '/':
        return operations.advanced_ops.safe_divide(a, b)
    else:
        return "Opération non reconnue"

