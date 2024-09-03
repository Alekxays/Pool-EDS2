def multiply(a, b):
    return a * b

print(multiply(5, 5))

def compare(a,b):
    if a > b:
        return "Le premier nombre est plus grand que le second"
    elif a < b:
        return "Le premier nombre est plus petit que le second"
    else:
        return "Les deux nombres sont égaux"
    
print(compare(5, 5))
print(compare(5, 10))
print(compare(10, 5))

def couting(x) :
    for i in range(1, x+1, 2):
        print(i, end=' ')
    return

print(couting(5))
print(couting(10))
print(couting(15))

def ask_user():
    mot = input("Entrer un mot :")
    print(f"Vous avez entré : {mot}")
    while (mot !="exit"):
        mot = input("Entrer un mot :")
        print(f"Vous avez entré : {mot}")
        if (mot == "exit") :
            break

ask_user()

def safe_divide(a,b):    
    try:
        return a/b
    except ZeroDivisionError:
        return "Division par zéro impossible"
    
print(safe_divide(5, 0))
print(safe_divide(5, 5))

def display_square(x, y):
    for _ in range(x):
        print(x*y)

display_square(5, "a")