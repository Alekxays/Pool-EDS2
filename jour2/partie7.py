import pandas as pd

def sort_dataframe_simple(data: pd.DataFrame) -> pd.DataFrame:
    return data.sort_values(by='product', ascending=False)

def sort_dataframe_advanced(data: pd.DataFrame) -> pd.DataFrame:
    return data.sort_values(by=['quantity', 'total_price', 'product'], ascending=[True, False, True])

def add_columns(data: pd.DataFrame) -> pd.DataFrame:
    data['order_number'] = data.index % 100000
    data['unit_price'] = (data['total_price'] / data['quantity']).round(2)
    return data

def filter_dataframe_simple(data: pd.DataFrame, product: str) -> pd.DataFrame:
    return data[(data['product'] == product) & (data['quantity'] >= 5)]

def filter_dataframe_advanced(data: pd.DataFrame) -> pd.DataFrame:
    filtered = data[data['order_number'].astype(str).str.startswith('1')]
    return filtered[(filtered['unit_price'] >= 0) & (filtered['unit_price'] <= 2)].sort_values(by='product')

def dataframe_operations(data: pd.DataFrame) -> (float, int, float, float, float):
    total_amount = data['total_price'].sum().round(2)
    total_quantity = data['quantity'].sum()
    mean_price = (total_amount / len(data)).round(2)
    max_price = data['total_price'].max().round(2)
    min_price = data['total_price'].min().round(2)
    return total_amount, total_quantity, mean_price, max_price, min_price
