import sys

def list_discovery() -> list:
    args = sys.argv[1:7]
    
    if len(args) < 6:
        raise ValueError("Not enough arguments provided. Please provide at least 6 arguments.")
    
    numbers = list(map(int, args[:5]))
    numbers.sort(reverse=True)
    numbers.pop()
    print(f"Numbers has {len(numbers)} elements and the sum of them all is {sum(numbers)}.")
    numbers.append(int(args[5]))  # Convert the sixth argument to int before appending
    return numbers

def dict_creation() -> dict:
    args = sys.argv[1:]
    return dict(zip(args[::2], args[1::2]))

def dict_display(dico: dict):
    print("\n".join(dico.keys()))
    print("\n".join(dico.values()))
    print("\n".join(f"Key: {k} - Value: {v}" for k, v in dico.items()))

def tuple_discovery(a, b, c, d) -> tuple:
    return (d, c, b, a)

def tuple_display(tpl: tuple):
    print("\n".join(map(str, tpl)))

def set_discovery(l1: list, l2: list) -> tuple:
    set1 = set(l1)
    set2 = set(l2)
    
    union_set = set1 | set2  # or set1.union(set2)
    intersection_set = set1 & set2  # or set1.intersection(set2)
    difference_set = set1 - set2  # or set1.difference(set2)
    symmetric_difference_set = set1 ^ set2  # or set1.symmetric_difference(set2)
    
    return (set1, set2, union_set, intersection_set, difference_set, symmetric_difference_set)

def power_via_comprehension(numbers: list[int]) -> list[int]:
    return [x**2 if x < 0 else -x for x in numbers]

if __name__ == "__main__":
    try:
        print(list_discovery())
    except ValueError as e:
        print(f"Error: {e}")
    
    dico = dict_creation()
    dict_display(dico)
    
    tpl = tuple_discovery(1, 2, 3, 4)
    tuple_display(tpl)
    
    try:
        tpl[0] = 10
    except TypeError as e:
        print(f"Error: {e}")
    
    l1 = [1, 2, 3, 4]
    l2 = [3, 4, 5, 6]
    sets = set_discovery(l1, l2)
    print("Set1:", sets[0])
    print("Set2:", sets[1])
    print("Union:", sets[2])
    print("Intersection:", sets[3])
    print("Difference:", sets[4])
    print("Symmetric Difference:", sets[5])
    set1 = sets[0]
    set1.add(1)
    set1.add(2)
    print("Set1 after adding duplicates:", set1)
    
    numbers = [-3, -2, -1, 0, 1, 2, 3]
    print("Original numbers:", numbers)
    print("Transformed numbers:", power_via_comprehension(numbers))