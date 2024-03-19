import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np
import pandas as pd
import scipy.stats as st

from .constants import ColInternal
from .data_tables import GeneScores, ParquetFeatures
from .index import IndexDict, ModelDataIndex
from .perigene_types import Region

logger = logging.getLogger(__name__)

MAX_RFE_DEPTH = 5


class FilteringFct(Protocol):
    def __call__(
        self, grps: pd.Series, y: pd.Series, **kwargs
    ) -> tuple[float, float]: ...


@dataclass
class FeatureSelectionParams:
    excluded_regions: Sequence[Region]
    """Regions to exclude when selecting features."""
    excluded_features: Sequence[str]
    """Manually excluded features."""
    min_var: float
    """Minimum feature variance."""
    max_var_diff: float
    """Maximum ratio of variance between training and test genes."""
    max_p: float
    """p-value threshold for univariate tests."""
    max_cross_corr: float
    """Maximum correlation between features."""
    n_features_post_univ: int
    """Maximum number of features to keep after univariate filtering."""
    batch_size: int
    """Number of features to process at once."""
    rfe_n_thres: int
    """Number of features below which the recursive random forest feature elimination
    stops."""
    rfe_step_shrink_thres: float
    """Threshold for the proportion of features to drop at each step of the recursive
    random forest feature elimination."""


IDX_NAME_P = "p"


def create_index_single_model(
    *,
    scores: GeneScores,
    fname_features: Path,
    target_chrom: str,
    params: FeatureSelectionParams,
) -> ModelDataIndex:
    train_genes, test_genes = split_train_test_genes(
        scores, target_chrom, params.excluded_regions
    )

    y_train = scores.get_scores(train_genes)

    kept_features_list = []

    logger.info(
        "Univariate features filtering (batches of %d columns)", params.batch_size
    )
    # Iterate over features
    features_iterator = ParquetFeatures.batch_iter(fname_features, params.batch_size)
    for batch_nb, features in enumerate(features_iterator, start=1):
        logger.info("Loading and selecting features on batch %i", batch_nb)
        kept_features_list.append(
            univariate_selection(
                features.data,
                y_train,
                train_genes,
                test_genes,
                params,
            )
        )
    try:
        logger.info("Concatenating kept features from %i batches", batch_nb)
        # Concatenate kept features from all batches and order columns by p-value
        df_kept = pd.concat([d for d in kept_features_list if not d.empty], axis=1)
    except ValueError as e:
        if "No objects to concatenate" in str(e):
            raise ValueError(
                "No features were kept after univariate filtering. "
                "Check the parameters of the feature selection."
            ) from e
        else:
            raise e

    logger.info("%i features left after univariate filtering", df_kept.shape[1])

    # Sort columns by p-value if present in the index
    if IDX_NAME_P in df_kept.columns.names:
        df_kept.sort_index(axis=1, level=IDX_NAME_P, inplace=True)
    else:
        raise ValueError("P-values should be present in the index!")

    n_features = df_kept.shape[1]
    names = df_kept.columns.get_level_values(None)
    pvals = df_kept.columns.get_level_values(IDX_NAME_P)

    logger.info("%i features left after univariate filtering.", n_features)
    logger.debug(
        "Most significantly associated feature is %s (pval=%.3g)", names[0], pvals[0]
    )
    logger.debug("Weakest kept feature is %s (pval=%.3g)", names[-1], pvals[-1])

    if (max_cols := params.n_features_post_univ) < n_features:
        logger.info("Keeping only the %i most significant features", max_cols)
        df_kept = df_kept.iloc[:, :max_cols]
        names = df_kept.columns.get_level_values(None)
        pvals = df_kept.columns.get_level_values(IDX_NAME_P)
        logger.debug(
            "Weakest kept feature after filtering is %s (pval=%.3g)",
            names[-1],
            pvals[-1],
        )

    # Remove the p-value level from the index
    df_kept.columns = df_kept.columns.droplevel(IDX_NAME_P)

    # Remove highly correlated features
    df_kept = filter_correlated_columns_bin_and_quant(df_kept, params)
    logger.info(
        "%i features left after cross-features correlation filtering",
        df_kept.shape[1],
    )

    # Use recursive random forest feature elimination
    df_kept = rf_recursive_feature_elimination(df_kept, y_train, params)
    logger.info(
        "%i features left after recursive random forest feature elimination",
        df_kept.shape[1],
    )

    return ModelDataIndex(train_genes, test_genes, df_kept.columns)


def filter_correlated_columns_bin_and_quant(
    df: pd.DataFrame, params: FeatureSelectionParams
) -> pd.DataFrame:
    # Remove features with high correlation
    X_bin, X_quant = _split_binary_quant_cols(df)
    corr_thres = params.max_cross_corr
    logger.info("Filtering overlapping binary features (Jaccard > %f)", corr_thres)
    X_bin = filter_correlated_columns(X_bin, corr_thres, method="jaccard")
    logger.info("Filtering correlated quantitative features (corr > %f)", corr_thres)
    X_quant = filter_correlated_columns(X_quant, corr_thres)

    # Filtering with "drop" to preserve the order of the columns
    dropped_cols = df.columns.difference(X_bin.columns.union(X_quant.columns))
    return df.drop(columns=dropped_cols)


def univariate_selection(
    X: pd.DataFrame,
    y_train: pd.Series,
    train_genes: pd.Series,
    test_genes: pd.Series,
    params: FeatureSelectionParams,
) -> pd.DataFrame:
    """Apply all univariate filters to the features matrix X and return the kept
    features values for the training genes.
    """
    n_start = X.shape[1]

    X = filter_manually_excluded(X, params)
    logger.debug("%i/%i features remaining after manual exclusion", X.shape[1], n_start)

    # Applying var diff filter only if we know the target genes
    X = filter_variance_train_test(X, train_genes, test_genes, params)
    logger.debug(
        "%i/%i features remaining after variance filtering", X.shape[1], n_start
    )

    X = filter_univariate_test(X, y_train, train_genes, params)

    logger.info("Keeping %i/%i features", X.shape[1], n_start)
    return X


def filter_univariate_test(
    X: pd.DataFrame,
    y_train: pd.Series,
    train_genes: pd.Series,
    params: FeatureSelectionParams,
) -> pd.DataFrame:
    # Process binary and quantitative features separately (using only training genes)
    X_bin, X_quant = _split_binary_quant_cols(X.loc[train_genes])

    logger.debug("Selecting gene sets associated with gene scores")
    X_bin = _test_association_binary_features(y_train, X_bin, params)

    logger.debug("Selecting quantitative features correlated with gene scores")
    X_quant = _test_association_quant_features(y_train, X_quant, params)

    if X_bin.empty and X_quant.empty:
        return pd.DataFrame()
    elif X_bin.empty:
        return X_quant
    elif X_quant.empty:
        return X_bin
    else:
        return X_bin.join(X_quant)


def filter_manually_excluded(
    X: pd.DataFrame, params: FeatureSelectionParams
) -> pd.DataFrame:
    logger.debug("Removing manually excluded features")
    return X.drop(columns=list(params.excluded_features), errors="ignore")


def filter_variance_train_test(
    X: pd.DataFrame,
    train_genes: pd.Series,
    test_genes: pd.Series,
    params: FeatureSelectionParams,
) -> pd.DataFrame:
    logger.debug("Removing features with high variance difference between train/test")

    var_train = X.loc[train_genes].var()
    mask_low_var_train = var_train < params.min_var

    logger.debug(
        "%i features with low variance (var < %.3g) on training genes.",
        mask_low_var_train.sum(),
        params.min_var,
    )

    # If we don't have the test genes, we can only remove features with low variance
    # on the training set
    if test_genes.empty:
        return X.drop(columns=X.columns[mask_low_var_train])

    # Otherwise, we can also remove features with low variance on the target chromosome
    var_target = X.loc[test_genes].var()
    mask_low_var_target = var_target < params.min_var

    logger.debug(
        "%i features with low variance (var < %.3g) on target genes.",
        mask_low_var_target.sum(),
        params.min_var,
    )

    # And features with a different variance between train and target genes
    var_ratio = var_train / var_target

    mask_var_ratio = (var_ratio > params.max_var_diff) | (
        var_ratio < 1 / params.max_var_diff
    )

    logger.debug(
        "%i features with variance ratio > %f",
        mask_var_ratio.sum(),
        params.max_var_diff,
    )

    dropped_cols = X.columns[mask_var_ratio | mask_low_var_train | mask_low_var_target]

    return X.drop(columns=dropped_cols)


def create_index_dict(
    *,
    scores: GeneScores,
    fname_features: Path,
    target_chromosomes: Sequence[str],
    params: FeatureSelectionParams,
) -> IndexDict:
    index_dict = IndexDict()
    for target_chromosome in target_chromosomes:
        index_dict[target_chromosome] = create_index_single_model(
            scores=scores,
            fname_features=fname_features,
            target_chrom=target_chromosome,
            params=params,
        )
    return index_dict


def split_train_test_genes(
    scores: GeneScores, target_chrom: str, excluded_regions: Sequence[Region]
) -> tuple[pd.Series, pd.Series]:
    logger.debug(
        "Splitting genes in training and test sets for target chromosome %s",
        target_chrom,
    )

    # Make a region covering the whole target chromosome
    region_target_chrom = Region(target_chrom, 0, int(1e12))

    # Exclude the target chromosome as well as the masked regions from training
    train_scores = scores.drop_regions(region_target_chrom, *excluded_regions)

    train_genes = train_scores[ColInternal.GENE]
    test_genes = scores.get_region(region_target_chrom)[ColInternal.GENE]
    return train_genes.rename(None), test_genes.rename(None)


def _split_binary_quant_cols(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Splits the data in 2 dataframes: one with binary columns and the other one
    with quantitative columns. Relies on the assumption that binary columns are of type
    UInt8.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: the first dataframe contains the binary
            columns, the second one the quantitative columns.
    """
    df_bin = df.select_dtypes(pd.UInt8Dtype())
    return df_bin, df.drop(columns=df_bin.columns)


def _test_association_binary_features(
    y: pd.Series, X_bin: pd.DataFrame, params: FeatureSelectionParams
) -> pd.DataFrame:
    if not _check_compute_univariate_test(X_bin, y, params):
        return X_bin

    logger.debug(
        "Binary features: testing association between gene scores and gene sets"
    )

    # Use Mann-Whitney U test to compare the distribution of gene scores between genes
    # in the gene set (1) and others (0)
    def pval_mann_whitney_grps(grps: pd.Series, y: pd.Series) -> tuple[float, float]:
        # Split features in 2 groups: those with 1 and those with 0
        y_others, y_gs = tuple(y.loc[grps == i] for i in (0, 1))
        return st.mannwhitneyu(y_others, y_gs).pvalue

    p_vals = np.array(list(pval_mann_whitney_grps(X_bin[col], y) for col in X_bin))
    return _filter_low_pval(X_bin, params, p_vals)


def _test_association_quant_features(
    y: pd.Series, X_quant: pd.DataFrame, params: FeatureSelectionParams
) -> pd.DataFrame:
    # Use spearman's correlation between feature and gene score

    if not _check_compute_univariate_test(X_quant, y, params):
        return X_quant
    logger.debug(
        "Quantitative features: testing association between gene scores and features"
    )

    # Note: we are not using `spearmanr(X_quant, y)` here as it calculates all
    # pairwise correlations (including those between features) which is not needed
    # and can be slow and memory-consuming for large datasets.
    p_vals = np.array(list(st.spearmanr(X_quant[col], y).pvalue for col in X_quant))
    return _filter_low_pval(X_quant, params, p_vals)


def _check_compute_univariate_test(
    X: pd.DataFrame, y: pd.Series, params: FeatureSelectionParams
) -> bool:
    """
    Check if the univariate test should be computed or skipped based on the parameters
    and raise an error if the input is not valid.
    """
    # If the p threshold is 1 but the max cross correlation is < 1, we still need to
    # calculate the tests as features are ordered by p-value
    if params.max_p >= 1 and params.max_cross_corr >= 1:
        logger.debug("Skipping univariate test as max_p and max_cross_corr are >= 1")
        return False
    if X.empty:
        logger.debug("Skipping univariate test as X is empty")
        return False
    if not isinstance(y, pd.Series):
        raise TypeError(f"y must be a pd.Series, got {type(y)} instead.")
    elif len(y) != len(X):
        raise ValueError(
            f"X and y must have the same length (X: {len(X)}, y: {len(y)})"
        )
    elif len(y) <= 1:
        raise ValueError("X and y must have at least 2 elements")
    return True


def _filter_low_pval(
    X: pd.DataFrame, params: FeatureSelectionParams, p_vals: np.ndarray
):
    """
    Filter features based on p-values and return a new dataframe with only the
    significant features.

    Args:
        X (pd.DataFrame): Dataframe of features
        params (FeatureSelectionParams): Parameters for the feature selection
        p_vals (np.ndarray): p-values of the univariate tests

    Returns:
        pd.DataFrame: Dataframe with only the significant features. The columns are
            multi-indexed with the p-values.
    """
    n_cols = X.shape[1]
    mask_pval = p_vals <= params.max_p
    new_cols = pd.MultiIndex.from_arrays([X.columns, p_vals], names=[None, IDX_NAME_P])
    logger.debug("Keeping %i/%i features", mask_pval.sum(), n_cols)
    return X.set_axis(new_cols, axis=1).loc[:, mask_pval]


def _jaccard_sim(df: pd.DataFrame) -> pd.DataFrame:
    """Jaccard similarity between columns of a dataframe. Note that when

    Args:
        df (pd.DataFrame)
    """
    from sklearn.metrics import pairwise_distances

    logger.debug("Calculating Jaccard similarity between columns...")

    if not df.isin({0, 1}).all().all():
        raise ValueError("Columns should only contain 0 or 1.")
    if (df == 0).all().any():
        raise ValueError("Columns should contain a least one positive value.")
    if df.empty:
        return pd.DataFrame(index=df.columns, columns=df.columns)

    idx = df.columns
    mat = df.astype(bool).values.T
    # This is the distance, not the similarity
    # Note that sklearn's pairwise distance is a lot faster than pandas corr
    dist = pairwise_distances(mat, metric="jaccard")
    # 1 - distance to get similarity
    sim = 1 - dist
    return pd.DataFrame(sim, index=idx, columns=idx)


def filter_correlated_columns(
    df: pd.DataFrame,
    threshold: float,
    n_start_cols: int | None = None,
    method="spearman",
) -> pd.DataFrame:
    """Calculate pairwise correlation between columns and drops highly
    correlated ones. As this function iterates over columns, their order
    matters!

    Warnings:

    - This function assumes that there are no missing values in the dataframe.
    - This function can be very resource-intensive for large dataframes as it calculates
    the full correlation matrix.

    Args:
        df (pd.DataFrame): Dataframe to be filtered
        threshold (float): absolute correlation threshold
        n_start_cols (int): Number of columns to consider for the first iteration.
        method (str, optional): Method used to estimate the pairwise
        similarity between columns. Defaults to "spearman".

    Raises:
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """

    logger.debug(
        "Filtering highly correlated columns of dataframe (shape: %s). "
        "Method = %s, threshold = %.3g.",
        df.shape,
        method,
        threshold,
    )

    # Skip if there is less than two columns or if the threshold is 1
    if threshold >= 1:
        logger.debug("Skipping correlation filtering as threshold is >= 1.")
        return df

    if df.shape[1] <= 1:
        logger.debug("Skipping correlation filtering as there are less than 2 columns.")
        return df

    if df.isna().any().any():
        raise ValueError("For efficiency, this method assumes no missing values.")

    if n_start_cols is None:
        n_start_cols = df.shape[1]

    corr_fct = dict(
        spearman=_spearman_corr,
        jaccard=_jaccard_sim,
    )

    if method not in corr_fct.keys():
        raise ValueError(
            f"Unknown correlation method received: {method}. "
            f"Should be one of {', '.join(corr_fct.keys())}"
        )

    # Calculate correlation matrix of the n_first columns
    coeffs_ = corr_fct[method](df)
    # Determine which columns are to be dropped in this subset
    to_drop = find_correlated(coeffs_, threshold)
    logger.debug("Dropping %i correlated columns.", len(to_drop))
    return df.drop(columns=to_drop)


def find_correlated(corr_matrix: pd.DataFrame, threshold: float) -> set[str]:
    """
    Determines, which elements are above a threshold from a correlation matrix.
    Columns are first compared to the left-most column.

    Args:
        corr_matrix (pd.DataFrame): Correlation matrix. Expected to be symmetric with
        index and columns being the names of the elements.
        threshold (float): Threshold above which elements are considered correlated.

    Returns:
        set[str]: Set of elements that are correlated above the threshold.
    """
    if not corr_matrix.index.equals(corr_matrix.columns):
        raise ValueError("Correlation matrix should be symmetric.")

    if (threshold < 0) or (threshold > 1):
        raise ValueError("Threshold should be between 0 and 1.")

    correlated_cols_above_thres: set[str] = set()
    for colx, corr in corr_matrix.items():
        if colx in correlated_cols_above_thres:
            continue
        cols_corr_with_colx = (
            corr.loc[corr.abs() >= threshold].drop(colx, errors="ignore").index
        )
        correlated_cols_above_thres.update(cols_corr_with_colx)
    return correlated_cols_above_thres


def _spearman_corr(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the Spearman correlation between columns of a dataframe and returns
    the correlation matrix as a DataFrame

    Args:
        df (pd.DataFrame): dataframe on which to calculate the correlations

    Returns:
        pd.DataFrame: dataframe of size n_cols x n_cols representing the correlation
        between df's columns.
    """
    logger.debug("Calculating Spearman correlation between columns...")
    idx = df.columns
    # As we don't need p-values, using numpy's corrcoeff on ranks is slightly more
    # efficient than scipy's spearmanr on large matrices (slightly underperforms
    # for smallish matrices (< few k cols) which should not be the case here)
    logger.debug("Pre-calculating ranks...")
    ranks = df.rank().values
    logger.debug("Calculating Pearson correlation on ranks...")
    coeffs = pd.DataFrame(np.corrcoef(ranks, rowvar=False), index=idx, columns=idx)
    return coeffs


def rf_recursive_feature_elimination(
    X: pd.DataFrame, y: pd.Series, params: FeatureSelectionParams, _depth=0
) -> pd.DataFrame:
    import xgboost as xgb
    from sklearn.model_selection import KFold, cross_validate

    n_col_start = X.shape[1]
    if n_col_start <= params.rfe_n_thres:
        logger.warn(
            "Feature matrix already below desired size (%i).", params.rfe_n_thres
        )
        return X

    if _depth >= MAX_RFE_DEPTH:
        logger.warn(
            "Maximum depth of recursive random forest feature elimination "
            "reached (%i). Exiting.",
            MAX_RFE_DEPTH,
        )
        return X

    X = X.copy()
    logger.info(
        "Starting a recursion step of feature elimination with %i features", n_col_start
    )

    out = cross_validate(
        xgb.XGBRFRegressor(tree_method="hist"),
        X,
        y,
        return_estimator=True,
        verbose=0,
        cv=KFold(5, shuffle=True),
    )
    df_summary_rf = pd.DataFrame(
        pd.Series(m.feature_importances_, index=m.feature_names_in_)
        for m in out["estimator"]
    )
    to_drop = df_summary_rf.max() <= 0
    n_drop = to_drop.sum()
    step_shrinkage = n_drop / n_col_start
    logger.info(
        "Dropping %i features with null feature importance (%.1f%%).",
        n_drop,
        step_shrinkage * 100,
    )

    X = X.loc[:, ~to_drop]

    # Exit if not dropping enough features (e.g less than 10% of the remaining features)
    # or if the number of features is below the threshold (e.g. 2500)
    if step_shrinkage <= params.rfe_step_shrink_thres:
        logger.info(
            "Stopping RFE as less than %.1f%% features were dropped",
            params.rfe_step_shrink_thres * 100,
        )
        return X
    if X.shape[1] <= params.rfe_n_thres:
        logger.info(
            "Stopping RFE as less than %i features remain",
            params.rfe_n_thres,
        )
        return X

    return rf_recursive_feature_elimination(X, y, params, _depth=_depth + 1)
