import pandas as pd
import pyarrow.parquet as pq

# Exercice 1 :
def read_parquet(filename: str) -> pd.DataFrame:
    df = pd.read_parquet(filename)
    return df.head(10)

# Exercice 2 :
def read_parquet_columns(filename: str, columns: list) -> pd.DataFrame:
    df = pd.read_parquet(filename, columns=columns)
    return df

# Exercice 3 :
def read_parquet_batch(filename: str, batch_size: int) -> pd.DataFrame:
    parquet_file = pq.ParquetFile(filename)
    dfs = []
    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df = batch.to_pandas().head(2).reset_index(drop=True)
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)