import numpy as np
import pandas as pd
from hypothesis import given, settings
from hypothesis import strategies as st

from perigene.preprocessing import features_merging
from tests.helpers.strategies import simple_mixed_dataframe_strategy


@given(
    df=simple_mixed_dataframe_strategy(n_floats=3, n_int=1, n_str=1),
    float_dtype=st.sampled_from(("float16", "float32", "float64")),
)
@settings(max_examples=50)
def test_convert_float_dtypes(df: pd.DataFrame, float_dtype: str) -> None:
    # Arrange
    float_cols = df.select_dtypes(np.floating).columns

    # Act
    df_converted = features_merging._convert_float_dtypes(df, float_dtype)
    float_cols_converted = df_converted.select_dtypes(float_dtype).columns

    # Assert
    assert float_cols.equals(
        float_cols_converted
    ), "Converted columns do not match original float columns"
    assert df.drop(columns=float_cols).equals(
        df_converted.drop(columns=float_cols_converted)
    ), "Non-float columns have been modified"
