# Exercice 1 : 

import csv

def native_csv_read(file: str) -> list[tuple]:
    with open(file, 'r') as csvfile:
        csv_r = csv.reader(csvfile, delimiter=';')
        next(csv_r)
        result = []

        for index, row in enumerate(csv_r):
            result.append((index, *row))
        
        return result
    
# Exercice 2 :

def native_csv_write(file: str, headers: list, data: list[tuple]):
    with open(file, 'w', newline='') as csvfile:
        csv_w = csv.writer(csvfile, delimiter=',')
        csv_w.writerow(headers)

        for row in data:
            csv_w.writerow(row[1:])

    
if __name__ == "__main__":
    csv_file = "Day2/assets/orders_semicolon.csv"
    print(native_csv_read(csv_file))
    
    native_csv_write('output.csv', ["OrderID", "Product", "Quantity"], [(1, "Banana", 10), (2, "Apple", 5), (3, "Orange", 3)])

