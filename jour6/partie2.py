import pandas as pd

# Exercice 1 :

def create_multi_index_df(df: pd.DataFrame) -> pd.DataFrame:
    multi_index_df = df.set_index(['year', 'region']).sort_index()
    return multi_index_df

# Exercice 2 :

def retrieve_multi_index_data(df: pd.DataFrame, year: int, region: str) -> pd.DataFrame:
    return df.loc[(year, region)]

# Exercice 3 :

def multi_index_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    agg_df = df.groupby(['year', 'region']).agg(
        quantity=('quantity', 'sum'),
        total_price=('total_price', 'sum')
    ).round(2)
    return agg_df

# Exercice 4 :

def columns_multi_index(df: pd.DataFrame) -> pd.DataFrame:
    agg_df = df.groupby(['year', 'region', 'category']).agg(
        quantity=('quantity', 'sum'),
        total_price=('total_price', 'sum')
    ).round(2)
    multi_index_df = agg_df.unstack(level='category')
    return multi_index_df

# Exercice 5 :

def swap_columns_multi_index(df: pd.DataFrame) -> pd.DataFrame:
    swapped_df = df.swaplevel(axis=1).sort_index(axis=1)
    return swapped_df

# Exercice 6 :

def retrieve_multi_index_column(df: pd.DataFrame, category: str) -> pd.DataFrame:
    return df[category]

def retrieve_multi_index_basic(df: pd.DataFrame, category: str, year: int) -> pd.DataFrame:
    return df.loc[year, :][category]

def retrieve_multi_index_advanced(df: pd.DataFrame, region: str, sub_column: str) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        try:
            region_df = df.xs(key=region, level='region')
            result = region_df.xs(key=sub_column, axis=1, level=1)
            return result
        except KeyError as e:
            raise KeyError(f"Erreur: {str(e)}")
    else:
        raise ValueError("Les colonnes du DataFrame ne sont pas un MultiIndex")


# Exercice 7 :

def create_pivot_table_basic(df: pd.DataFrame) -> pd.DataFrame:
    pivot_df = pd.pivot_table(
        df,
        values=['quantity', 'total_price'],
        index=['year', 'region'],
        columns='category',
        aggfunc={'quantity': 'sum', 'total_price': 'sum'}
    ).round(2)
    return pivot_df

def create_pivot_table_advanced(df: pd.DataFrame) -> pd.DataFrame:
    pivot_df = pd.pivot_table(
        df,
        values=['quantity', 'total_price'],
        index=['year', 'region'],
        columns='category',
        aggfunc={
            'quantity': ['count', 'mean', 'sum'],
            'total_price': ['mean', 'sum']
        },
        margins=False
    ).round(2)
    pivot_df = pivot_df.sort_index(axis=1)
    return pivot_df

# Exercice 8 :

def avg_price_rolling_window(df: pd.DataFrame) -> pd.DataFrame:
    df['rolling_avg'] = df['quantity'].rolling(window=7, min_periods=3).mean().round(2)
    return df


# Exercice 9 :

def highlight_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df['highlight'] = df.apply(lambda row: row['quantity'] > 2.5 * row['rolling_avg'], axis=1)
    return df