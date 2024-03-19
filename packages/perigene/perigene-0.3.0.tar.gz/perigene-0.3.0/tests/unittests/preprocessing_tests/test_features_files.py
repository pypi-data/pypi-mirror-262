import numpy as np
import pandas as pd
import pytest
from scipy.stats import spearmanr

from perigene.preprocessing.features_files import univariate_selection


@pytest.fixture
def X():
    return pd.DataFrame(
        [
            [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            [0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
            [0.3, 0.4, 0.5, 1.3, 0.7, 0.8],
            [0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            [0.5, 0.2, 0.7, 0.8, 0.9, 1.0],
            [0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
            [0.7, 0.5, 0.9, 0.0, 1.0, 1.1],
        ],
        columns=["A", "B", "C", "D", "E", "F"],
    )


@pytest.fixture
def y():
    return pd.Series([0, 0, 1, 1, 1, 1, 0.5])


def test_univariate_selection(X, y) -> None:
    # Append y to X to make sure that at least one feature is selected
    X["y"] = y
    threshold = 0.05
    X_filtered = univariate_selection(X, y, spearmanr, threshold)
    assert isinstance(X_filtered, pd.DataFrame)
    assert X_filtered.shape[0] == X.shape[0]
    assert X_filtered.shape[1] <= X.shape[1]

    assert "y" in X_filtered.columns.get_level_values(0)

    assert X_filtered.columns.nlevels == 2
    pvalues = X_filtered.columns.get_level_values(1)
    assert pvalues.dtype == float
    assert (pvalues < threshold).all()
    assert (pvalues >= 0).all()


def test_univariate_selection_with_nan_values(X, y) -> None:
    X.loc[0, "B"] = np.nan
    X.loc[1, "C"] = np.nan

    threshold = 0.05
    X_filtered = univariate_selection(X, y, spearmanr, threshold)
    assert isinstance(X_filtered, pd.DataFrame)


def test_univariate_selection_fails_when_y_is_not_a_series() -> None:
    X = pd.DataFrame([[1, 2], [3, 4], [5, 6]])
    y = pd.DataFrame([0, 1, 2])
    threshold = 0.05
    with pytest.raises(TypeError):
        univariate_selection(X, y, spearmanr, threshold)


def test_univariate_selection_fails_when_X_and_y_have_different_number_of_rows() -> (
    None
):
    X = pd.DataFrame([[1, 2], [3, 4], [5, 6]])
    y = pd.Series([0, 1, 2, 3])
    threshold = 0.05
    with pytest.raises(ValueError):
        univariate_selection(X, y, spearmanr, threshold)


def test_univariate_selection_fails_when_data_is_too_small_to_perform_test() -> None:
    X = pd.DataFrame(
        [
            [1, 2],
        ]
    )
    y = pd.Series(
        [
            0,
        ]
    )
    threshold = 0.05
    with pytest.raises(ValueError):
        univariate_selection(X, y, spearmanr, threshold)
