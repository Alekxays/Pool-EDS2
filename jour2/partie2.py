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

