# Exercice 1

def multiply(a, b):
    return a * b

# Exercice 2

def compare(a,b):
    if a > b:
        return "Le premier nombre est plus grand que le second"
    elif a < b:
        return "Le premier nombre est plus petit que le second"
    else:
        return "Les deux nombres sont égaux"
    
# Exercice 3

def couting(x) :
    for i in range(1, x+1, 2):
        print(i, end=' ')
    return

# Exercice 4

def ask_user():
    mot = input("Entrer un mot :")
    print(f"Vous avez entré : {mot}")
    while (mot !="exit"):
        mot = input("Entrer un mot :")
        print(f"Vous avez entré : {mot}")
        if (mot == "exit") :
            break

# Exercice 5

def safe_divide(a,b):    
    try:
        return a/b
    except ZeroDivisionError:
        return "Division par zéro impossible"
    
# Exercice 6

def display_square(x, y):
    for _ in range(x):
        print(x*y)