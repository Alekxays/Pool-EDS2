import pandas as pd
def pandas_csv_read(file: str) -> pd.DataFrame:
    df = pd.read_csv(file)
    return df

def pandas_csv_write(file: str, headers: list, data: list[tuple]):
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(file, index=False, encoding='utf-8')