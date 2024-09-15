def native_csv_read(file: str) -> list[tuple]:
    result = []
    with open(file, 'r', encoding='utf-8') as csvfile:
        next(csvfile)
        for index, line in enumerate(csvfile):
            columns = line.strip().split(';')
            result.append((index,) + tuple(columns))
    return result

import csv
def native_csv_write(file: str, headers: list, data: list[tuple]):
    with open(file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(headers)
        for row in data:
            writer.writerow(row[1:])




