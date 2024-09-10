import pandas as pd
from datetime import datetime
import numpy as np

# Exercice 1 : 

def impute_region(df: pd.DataFrame) -> pd.DataFrame:
    country_to_region = {
        'Japan': 'Japan',
        'China': 'APAC',
        'Australia': 'APAC',
        'France': 'EMEA',
        'Germany': 'EMEA',
        'UK': 'EMEA',
        'USA': 'NA',
        'Canada': 'NA',
        'Norway': 'EMEA',
        'Finland': 'EMEA',
        'Austria': 'EMEA'
    }
    df['region'] = df.apply(lambda row: country_to_region.get(row['country'], row['region']) 
    if pd.notna(row['country']) else row['region'], axis=1)
    df = df.dropna(subset=['region'])
    df.reset_index(drop=True, inplace=True)
    df['region'].fillna('Unknown', inplace=True)
    return df

def impute_quantity(df: pd.DataFrame) -> pd.DataFrame:
    quantity_mean = df['quantity'].mean()
    df['quantity'] = df['quantity'].fillna(quantity_mean)
    return df

def impute_category(df: pd.DataFrame) -> pd.DataFrame:
    most_frequent_category = df['category'].mode()[0]
    df['category'] = df['category'].fillna(most_frequent_category)
    return df

# Exercice 2 :

def handle_inconsistent_dealsize(df: pd.DataFrame) -> pd.DataFrame:
    def standardize_dealsize(size):
        size = str(size).strip().lower()
        if size in ['s', 'small', '1']:
            return 'S'
        elif size in ['m', 'medium', '2']:
            return 'M'
        elif size in ['l', 'large', '3']:
            return 'L'
        else:
            return 'M'
    df['dealsize'] = df['dealsize'].apply(standardize_dealsize)
    return df

def handle_inconsistent_dates(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

# Exercice 3 :

def retrieve_quantity_outliers(df: pd.DataFrame) -> pd.DataFrame:
    Q1 = df['quantity'].quantile(0.25)
    Q3 = df['quantity'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 0.5 * IQR
    upper_bound = Q3 + 0.5 * IQR
    print(f"Q1: {Q1}, Q3: {Q3}, IQR: {IQR}")
    print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
    outliers = df[(df['quantity'] < lower_bound) | (df['quantity'] > upper_bound)]
    outliers_sorted = outliers.sort_values(by='quantity')
    return outliers_sorted

def handle_unit_price_outliers(df: pd.DataFrame) -> pd.DataFrame:
    Q1 = df['unit_price'].quantile(0.25)
    Q3 = df['unit_price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1
    upper_bound = Q3 + 1.5 * IQR
    df['unit_price'] = df['unit_price'].apply(
        lambda x: min(x, upper_bound) if x > upper_bound else x
    )
    df = df[df['unit_price'] >= lower_bound]
    df_sorted = df.sort_values(by='unit_price')
    return df_sorted

# Exercice 4 :

def normalize_total_price(df: pd.DataFrame) -> pd.DataFrame:
    df['total_price'] = df['total_price'].apply(lambda x: np.log1p(x))
    df['total_price'] = df['total_price'].round(10)
    return df

def normalize_quantity(df: pd.DataFrame) -> pd.DataFrame:
    mean_quantity = df['quantity'].mean()
    std_quantity = df['quantity'].std()
    df['quantity'] = (df['quantity'] - mean_quantity) / std_quantity
    df['quantity'] = df['quantity'].round(10)
    return df

def normalize_unit_price(df: pd.DataFrame) -> pd.DataFrame:
    min_price = df['unit_price'].min()
    max_price = df['unit_price'].max()
    df['unit_price'] = (df['unit_price'] - min_price) / (max_price - min_price)
    df['unit_price'] = df['unit_price'].round(10)
    return df