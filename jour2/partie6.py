import pandas as pd

def pandas_json_read(file: str) -> pd.DataFrame:
    df = pd.read_json(file)
    return df

def pandas_json_write(file: str, data: pd.DataFrame):
    data.to_json(file, orient='records', lines=False, indent=4)

