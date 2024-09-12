import pandas as pd

# Exercice 1:

def pandas_csv_read(file: str) -> pd.DataFrame:
    return pd.read_csv(file)

# Exercice 2:

def pandas_csv_write(file: str, headers: list, data: list[tuple]):
    cleaned_data = [row[1:] for row in data]
    df = pd.DataFrame(cleaned_data, columns=headers)
    df.to_csv(file, index=False)
