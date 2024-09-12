import pandas as pd
import csv

# Exercice 1:

def create_series(*args) -> pd.Series:
    if all(isinstance(arg, int) for arg in args):
        if len(args) == 0:
            return pd.Series(dtype=int)
        return pd.Series(args)
    else:
        raise ValueError("All arguments must be of type int")
    
# Exercice 2:

def series_operations(series: pd.Series) -> (int, float, float):
    somme = series.sum()
    moyenne = series.mean()
    ecart_type = series.std()

    return (somme, moyenne, ecart_type)

# Exercice 3:

def native_csv_read(file: str) -> list[tuple]:
    with open(file, 'r') as csvfile:
        csv_r = csv.reader(csvfile, delimiter=',')
        next(csv_r)
        result = []

        for index, row in enumerate(csv_r):
            result.append((index, *row))
        
        return result

def create_dataframe(products: list[str], quantities: list[int], prices: list[float]) -> pd.DataFrame:
    data = {
        "product": products,
        "quantity": quantities,
        "total_price": [q * p for q, p in zip(quantities, prices)]
    }
    df = pd.DataFrame(data)

    return df

# Exercice 4:

def dataframe_accession(data: pd.DataFrame) -> tuple:
    products_list = data['Product'].tolist()
    second_dict = data.iloc[1].to_dict()
    third_product_q = data.loc[2, 'Quantity']
    return (products_list, second_dict, third_product_q)
