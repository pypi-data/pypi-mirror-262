#!/usr/bin/env python

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra import numpy as npst

from perigene import feature_selection as fs


@st.composite
def corr_matrix_strategy(draw: st.DrawFn, min_size=1, max_size=4):
    size = draw(st.integers(min_value=min_size, max_value=max_size))
    data = draw(
        npst.arrays(
            dtype=float,
            shape=(size, size),
            elements=st.floats(
                allow_nan=False, allow_infinity=False, min_value=-1.0, max_value=1.0
            ),
        )
    )

    # Make symetric
    corr = (data + data.T) / 2  # type: ignore

    # Make sure diagonal is 1
    np.fill_diagonal(corr, 1)

    index = list("abcdefghij")[:size]
    return pd.DataFrame(corr, index=index, columns=index)


@given(
    corr_matrix_strategy(),
    st.floats(allow_nan=False, allow_infinity=False, min_value=0.0, max_value=1.0),
)
@settings(max_examples=50)
def test_find_correlated(corr_matrix: pd.DataFrame, threshold: float) -> None:
    # Call the function with the correlation matrix and threshold
    result = fs.find_correlated(corr_matrix, threshold)

    # Assert that the result is a set
    assert isinstance(result, set)

    # Assert that all elements in the result are strings
    assert all(isinstance(item, str) for item in result)


def test_find_correlated_raises_on_non_symmetric_matrix():
    # Create a non-symmetric correlation matrix
    corr_matrix = pd.DataFrame([[1, 2], [3, 4]], index=list("ab"), columns=list("bc"))

    # Assert that calling the function with the non-symmetric matrix raises a ValueError
    with pytest.raises(ValueError):
        fs.find_correlated(corr_matrix, 0.5)


def test_find_correlated_raises_on_threshold_out_of_range():
    # Create a non-symmetric correlation matrix
    corr_matrix = pd.DataFrame([[1, 2], [3, 4]], index=list("ab"), columns=list("ab"))

    # Assert that calling the function with the non-symmetric matrix raises a ValueError
    with pytest.raises(ValueError):
        fs.find_correlated(corr_matrix, 1.1)

    with pytest.raises(ValueError):
        fs.find_correlated(corr_matrix, -0.1)


def test_jaccard_sim_empty_df():
    # Arrange
    df_in = pd.DataFrame()
    expected = pd.DataFrame()
    # Act
    df_out = fs._jaccard_sim(df_in)
    # Assert
    assert df_out.equals(expected)


def test_jaccard_sim_only_zeros():
    # Arrange
    df_in = pd.DataFrame(np.zeros((10, 3)), columns=list("ABC"))
    # Act
    # Assert
    with pytest.raises(ValueError):
        fs._jaccard_sim(df_in)


def test_jaccard_sim_non_integer_columns():
    # Arrange
    df_in = pd.DataFrame(np.random.normal(size=(10, 3)), columns=list("ABC"))
    # Act
    # Assert
    with pytest.raises(ValueError):
        fs._jaccard_sim(df_in)


def test_jaccard_sim_non_binary_columns():
    # Arrange
    df_in = pd.DataFrame(dict(A=[1] * 10, B=[0] * 10, C=[1] * 9 + [2]))
    # Act
    # Assert
    with pytest.raises(ValueError):
        fs._jaccard_sim(df_in)


def test_jaccard_sim_only_ones():
    # Arrange
    df_in = pd.DataFrame(np.ones((10, 3)), columns=list("ABC"))
    expected = pd.DataFrame(np.ones((3, 3)), columns=list("ABC"), index=list("ABC"))
    # Act
    df_out = fs._jaccard_sim(df_in)
    # Assert
    assert df_out.equals(expected)


def test_jaccard_sim_valid_matrix_1():
    # Arrange
    df_in = pd.DataFrame(
        [[1, 0, 1, 1], [0, 1, 0, 0], [1, 1, 0, 1], [0, 1, 0, 0]], columns=list("ABCD")
    )
    expected = pd.DataFrame(
        [
            [1.0, 0.25, 0.5, 1.0],
            [0.25, 1.0, 0.0, 0.25],
            [0.5, 0.0, 1.0, 0.5],
            [1.0, 0.25, 0.5, 1.0],
        ],
        columns=list("ABCD"),
        index=list("ABCD"),
    )
    # Act
    df_out = fs._jaccard_sim(df_in)
    # Assert
    assert df_out.equals(expected)
