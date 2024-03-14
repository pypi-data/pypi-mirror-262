from datetime import datetime
from typing import List, Union

import pandas as pd


def ensure_feature_axis(
    df: pd.DataFrame,
    h3_indices: List[str],
    timestamps: Union[List[Union[str, datetime]], pd.DatetimeIndex],
    timestamp_col_name: str = "timestamp",
    h3_index_col_name: str = "h3_index",
    values_col_name: str = "value",
) -> pd.DataFrame:
    """Ensure the return from remote has the correct columns and rows."""

    # ensure the columns are correct
    assert timestamp_col_name in df.columns, f"{timestamp_col_name} must be in the dataframe"
    assert h3_index_col_name in df.columns, f"{h3_index_col_name} must be in the dataframe"
    assert values_col_name in df.columns, f"{values_col_name} must be in the dataframe"

    df[timestamp_col_name] = pd.to_datetime(df[timestamp_col_name])
    df = df.pivot(index=timestamp_col_name, columns=h3_index_col_name, values=values_col_name).reindex(index=timestamps, columns=h3_indices)
    df = df.reset_index()
    df = df.rename(columns={"index": timestamp_col_name})
    df = df.melt(id_vars=timestamp_col_name, value_vars=h3_indices, var_name=h3_index_col_name, value_name=values_col_name)
    
    return df
