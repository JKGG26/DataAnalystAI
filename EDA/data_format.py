import pandas as pd
import numpy as np


def replace_empties_df(df: pd.DataFrame, columns: list = None, no_columns: list = None):
    if columns is None and no_columns is None:
        columns = list(df.keys())
    elif isinstance(no_columns, list):
        columns = [col for col in list(df.keys()) if col not in no_columns]

    for column in columns:
        mean = df[column].mean()
        df[column] = df[column].replace({
            pd.NA: mean,
            np.nan: mean,
            np.NaN: mean,
            np.NAN: mean
            })

    return df