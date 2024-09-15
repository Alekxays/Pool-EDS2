import pandas as pd
def pandas_excel_read(file: str, sheet: str) -> pd.DataFrame:
    df = pd.read_excel(file, sheet_name=sheet)
    return df

def pandas_excel_write(data: pd.DataFrame, filename: str):
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        data.to_excel(writer, sheet_name='orders', index=False)




