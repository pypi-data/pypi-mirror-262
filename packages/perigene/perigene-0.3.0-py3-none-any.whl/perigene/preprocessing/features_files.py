from __future__ import annotations

import logging
import textwrap
from collections.abc import Callable, Sequence
from glob import glob
from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd
import scipy.stats as st

from ..constants import ColInternal
from ..feature_selection import filter_correlated_columns
from ..perigene_types import FilePrefix

logger = logging.getLogger(__name__)


class FilteringParams(NamedTuple):
    max_p: float
    min_gene_set_size: int


class RFEParams(NamedTuple):
    n_thres: int
    step_shrink_thres: float
    n_jobs: int


def process_features_batch(
    X: pd.DataFrame, y: pd.Series, params: FilteringParams
) -> pd.DataFrame:
    # Drop columns with constant values
    X = X.loc[:, (X != X.iloc[0]).any()]
    # Re-index to match gene scores
    X = X.copy().reindex(y.index)
    # Process binary and quantitative features separately
    X_bin, X_quant = split_binary_quant_cols(X)
    X_bin = filter_binary_features_batch(y, params, X_bin)

    X_quant = filter_quant_features_batch(y, params, X_quant)
    if not X_quant.empty:
        float64_cols = X_quant.select_dtypes("float64").columns
        X_quant[float64_cols] = X_quant[float64_cols].astype(np.float32)

        # Restrict fillna to nan columns to avoid calculating median for columns where
        # it's not necessary
        na_cols = X_quant.isna().any()
        X_quant.loc[:, na_cols] = X_quant.loc[:, na_cols].fillna(
            X_quant.loc[:, na_cols].median()
        )

    # Set column names and index names for empty dataframes
    for df in (X_bin, X_quant):
        if df.empty:
            df.columns = pd.MultiIndex.from_tuples([], names=["GENE_SET", "p"])

    return pd.concat([X_bin, X_quant], axis=1)


def filter_quant_features_batch(y, params, X_quant):
    n_cols = X_quant.shape[1]
    # Use spearman's correlation between feature and gene score
    if not X_quant.empty:
        X_quant = univariate_selection(X_quant, y, st.spearmanr, params.max_p)
    logger.info(
        "Quantitative features: keeping %i/%i features", X_quant.shape[1], n_cols
    )
    return X_quant


def filter_binary_features_batch(y, params, X_bin):
    n_cols = X_bin.shape[1]

    # Types are converted to float if there is any nan values in a column
    # Convert binary df back to integers.
    X_bin = X_bin.fillna(0).astype(np.int8)

    # Drop columns with small gene sets
    X_bin = X_bin.loc[:, X_bin.sum() >= params.min_gene_set_size]

    if not X_bin.empty:

        def mann_whitney_grps(
            grps: pd.Series, y: pd.Series, **kwargs
        ) -> Sequence[float]:
            assert grps.isin({0, 1}).all()
            y_others, y_gs = tuple(y.loc[grps == i] for i in (0, 1))
            return st.mannwhitneyu(y_others, y_gs, **kwargs)

        # Use difference in mean gene score between genes in gene set and others
        X_bin = univariate_selection(X_bin, y, mann_whitney_grps, params.max_p)

    logger.info("Binary features: keeping %i/%i features", X_bin.shape[1], n_cols)
    return X_bin


def read_data_file(file_: Path) -> pd.DataFrame:
    logger.info("Reading data from %s", file_)
    if file_.name.endswith((".parq", ".parquet", ".pq")):
        df = pd.read_parquet(file_)
    else:
        df = pd.read_table(file_, index_col=ColInternal.GENE)
    # Make sure gene ids are treated as strings
    df.index = df.index.astype(str)
    return df


def read_all_features(
    *paths: Path, y: pd.Series, params: FilteringParams
) -> pd.DataFrame:
    return pd.concat(
        [
            process_features_batch(read_data_file(Path(f)), y, params)
            for p in paths
            for f in glob(str(p))
        ],
        axis=1,
    )


def split_binary_quant_cols(X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the received DataFrame in 2: 1 with binary columns, the other with the
    other columns.

    Args:
        X (pd.DataFrame): _description_

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: _description_
    """
    binary_mask = X.fillna(0).isin({0, 1, 0.0, 1.0}).all()
    return X.loc[:, binary_mask], X.loc[:, ~binary_mask]


def preprocess_features(
    *,
    file_scores: Path,
    path_features: list[Path],
    prefix_out: FilePrefix,
    max_p: float,
    min_gene_set_size: int,
    max_corr=0.7,
    rfe_params: RFEParams | None = None,
) -> None:
    params = FilteringParams(max_p=max_p, min_gene_set_size=min_gene_set_size)
    logger.info("Loading scores...")
    y = read_scores(file_scores)
    logger.info("Loading features from \n" + "\n".join(str(p) for p in path_features))
    X = read_all_features(*path_features, y=y, params=params)

    if max_p < 1:
        # Order features by pvalue
        logger.debug("Ordering features by pvalue...")
        X = X.sort_index(axis=1, level="p").droplevel("p", axis=1)

    X_bin, X_quant = split_binary_quant_cols(X)
    msg = f"""
    {'-' * 80}
    Keeping {{n_tot}} features after {{step}}
    Binary -> {{n_bin}}
    Quantitative -> {{n_quant}}
    """
    logger.info(
        textwrap.dedent(
            msg.format(
                step="1st pass filtering",
                n_tot=X.shape[1],
                n_bin=X_bin.shape[1],
                n_quant=X_quant.shape[1],
            )
        )
    )

    logger.info("Filtering overlapping binary features (Jaccard index > %f)", max_corr)
    X_bin = filter_correlated_columns(X_bin, max_corr, method="jaccard")
    logger.info("Filtering correlated quantitative features (corr > %f)", max_corr)
    X_quant = filter_correlated_columns(X_quant, max_corr)
    X = X_bin.join(X_quant)
    logger.info(
        textwrap.dedent(
            msg.format(
                step="removing highly correlated columns",
                n_tot=X.shape[1],
                n_bin=X_bin.shape[1],
                n_quant=X_quant.shape[1],
            )
        )
    )
    del X_bin, X_quant

    if rfe_params is not None:
        logger.info(
            "Applying recursive random forest feature elimination with %i jobs "
            "(this may take a while)...",
            rfe_params.n_jobs,
        )
        X = rf_rfe_features_elimination(X, y, rfe_params)

    f_out = prefix_out.join(".preprocessed.parquet")
    logger.info("Saving features to %s", f_out)
    X.to_parquet(str(f_out), index=True)


def rf_rfe_features_elimination(
    X: pd.DataFrame, y: pd.Series, rfe_params: RFEParams
) -> pd.DataFrame:
    import xgboost as xgb
    from sklearn.model_selection import KFold, cross_validate

    X = X.copy()
    n_col_start = X.shape[1]
    logger.info(
        "Starting a recursion step of feature elimination with %i features", n_col_start
    )

    if n_col_start <= rfe_params.n_thres:
        logger.warn(
            "Feature matrix already below desired size (%i)", rfe_params.n_thres
        )
        return X

    out = cross_validate(
        xgb.XGBRFRegressor(n_jobs=rfe_params.n_jobs, tree_method="hist"),
        X,
        y,
        return_estimator=True,
        verbose=2,
        cv=KFold(10, shuffle=True),
    )
    df_summary_rf = pd.DataFrame(
        pd.Series(m.feature_importances_, index=m.feature_names_in_)
        for m in out["estimator"]
    )
    to_drop = df_summary_rf.max() <= 0
    n_drop = to_drop.sum()
    step_shrinkage = n_drop / n_col_start
    logger.info(
        "Dropping %i features with null feature importance (%.1f%% of remaining).",
        n_drop,
        step_shrinkage * 100,
    )

    X = X.loc[:, ~to_drop]

    # Exit if not dropping enough features or less features remainning than threshold
    if (step_shrinkage <= rfe_params.step_shrink_thres) or (
        X.shape[1] <= rfe_params.n_thres
    ):
        return X
    return rf_rfe_features_elimination(X, y, rfe_params)


def read_scores(file_scores):
    y = read_data_file(file_scores)
    assert y.shape[1] == 1, "Expecting only one data field in score file"
    return y.iloc[:, 0]


def univariate_selection(
    X: pd.DataFrame,
    y: pd.Series,
    test_fct: Callable[[pd.Series, pd.Series], tuple[float, float]],
    threshold: float,
):
    """
    Filter features based on a univariate test between each feature and the target
    variable.
    Args:
        X (pd.DataFrame): Features matrix
        y (pd.Series): Target variable
        test_fct (Callable[[pd.Series, pd.Series], Tuple[float, float]]]): Test
        function from scipy.stats taking two pd.Series as input and returning the
        test statistic and p-value
        threshold (float): Maximum p-value to keep a feature
    """
    if threshold >= 1:
        return X
    if not isinstance(y, pd.Series):
        raise TypeError(f"y must be a pd.Series, got {type(y)}")
    elif len(y) != len(X):
        raise ValueError(
            f"X and y must have the same length (X: {len(X)}, y: {len(y)})"
        )
    elif len(y) <= 1:
        raise ValueError("X and y must have at least 2 elements")

    test_results = (
        X.apply(test_fct, args=(y,), nan_policy="omit").set_axis(["_", "p"]).T
    )

    ps = test_results.p.reset_index()
    X.columns = pd.MultiIndex.from_frame(ps)
    return X.loc[:, X.columns.get_level_values("p") < threshold]
