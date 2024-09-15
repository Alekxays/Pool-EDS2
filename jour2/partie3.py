import pandas as pd

def create_series() -> pd.Series:
    data = [10, 20, 30]
    series = pd.Series(data)
    return series



def series_operations(series: pd.Series) -> (int, float, float):
    total_sum = series.sum()
    mean = series.mean()
    std_dev = series.std()
    return (total_sum, mean, std_dev)



def create_dataframe_from_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df
file_path = 'orders.csv'


def dataframe_accession(data: pd.DataFrame) -> tuple:
    product_list = data['product'].tolist()
    second_row = data.iloc[1].to_dict()
    third_product_quantity = data.iloc[2]['quantity']
    return (product_list, second_row, third_product_quantity)

def create_dataframe(products: list[str], quantities: list[int], prices: list[float]) -> pd.DataFrame:
    data = {
        'product': products,
        'quantity': quantities,
        'total_price': prices
    }
    df = pd.DataFrame(data)
    return df

