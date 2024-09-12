import sys

# Exercice 1

def list_discovery() -> list:
    args = sys.argv[1:7]
    
    if len(args) < 6:
        raise ValueError("Not enough arguments provided. Please provide at least 6 arguments.")
    
    numbers = list(map(int, args[:5]))
    numbers.sort(reverse=True)
    numbers.pop()
    print(f"Numbers has {len(numbers)} elements and the sum of them all is {sum(numbers)}.")
    numbers.append(int(args[5]))
    return numbers

# Exercice 2

def dict_creation() -> dict:
    args = sys.argv[1:]
    return dict(zip(args[::2], args[1::2]))

def dict_display(dico: dict):
    print("\n".join(dico.keys()))
    print("\n".join(dico.values()))
    print("\n".join(f"Key: {k} - Value: {v}" for k, v in dico.items()))

# Exercice 3

def tuple_discovery(a, b, c, d) -> tuple:
    return (d, c, b, a)

def tuple_display(tpl: tuple):
    print("\n".join(map(str, tpl)))

# Exercice 4

def set_discovery(l1: list, l2: list) -> tuple:
    set1 = set(l1)
    set2 = set(l2)
    union_set = set1 | set2 
    intersection_set = set1 & set2 
    difference_set = set1 - set2
    symmetric_difference_set = set1 ^ set2
    return (union_set, intersection_set, difference_set, symmetric_difference_set)

# Exercice 5

def power_via_comprehension(numbers: list[int]) -> list[int]:
    return [x**2 if x < 0 else -x for x in numbers]