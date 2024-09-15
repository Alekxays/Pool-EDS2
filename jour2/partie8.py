import pandas as pd

def static_suppression(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=['total_price'])
    df = df.drop(df.index[5:13]).reset_index(drop=True)
    return df

def missing_data_suppression(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(subset=['total_price']).reset_index(drop=True)

def duplicate_data_suppression(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates().reset_index(drop=True)

def number_uniformisation(df: pd.DataFrame) -> pd.DataFrame:
    df['quantity'] = df['quantity'].astype(int)
    df['total_price'] = df['total_price'].astype(float).round(2)
    return df

def string_uniformisation(df: pd.DataFrame) -> pd.DataFrame:
    df['product'] = df['product'].str.lower()
    return df

def number_validation(df: pd.DataFrame) -> bool:
    return df['total_price'].gt(0).all() and df['quantity'].between(1, 10).all()

def enum_validation(df: pd.DataFrame, products: list) -> pd.DataFrame:
    return df[~df['product'].isin(products)].reset_index(drop=True)

def cross_column_validation(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['unit_price'] > df['total_price']].reset_index(drop=True)
