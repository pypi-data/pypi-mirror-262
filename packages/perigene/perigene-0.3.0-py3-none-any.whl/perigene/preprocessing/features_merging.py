from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass
from io import StringIO
from itertools import islice
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import (
    MinMaxScaler,
    QuantileTransformer,
    RobustScaler,
    StandardScaler,
)

from .. import data_tables as pg_tables
from ..constants import ColInternal
from ..perigene_types import FilePrefix
from ..utils import identity

logger = logging.getLogger(__name__)


@dataclass
class MissingnessThresholds:
    """
    Missingness thresholds to use for filtering features and genes.
    """

    gene: float
    """Max proportion of missing values for a gene to be kept"""
    quant_feature: float
    """Max proportion of missing values for a quantitative feature to be kept"""
    gene_set: int
    """Min number of genes in a gene sets for it to be kept"""


def iter_feature_files(
    path_features: Sequence[Path],
    batch_cols: int = 5000,
):
    """
    Iterate over all feature files in `path_features`, process them and yield them as
    batches of `batch_cols` columns.
    """

    leftover_features: pd.DataFrame | None = None
    for file_ in path_features:
        logger.info("Reading data from %s", file_)

        # Read features matrix from file
        factory = (
            pg_tables.GMTFeatures.from_path
            if file_.name.endswith(pg_tables.EXT_GMT)
            else pg_tables.RawFeatures.from_path
        )

        try:
            df = factory(file_).data.set_index(ColInternal.GENE)
        except Exception as e:
            logger.error(f"Unexpected error while reading {file_}")
            raise e

        # Join with leftover features from previous file if any
        if leftover_features is not None:
            df = df.join(leftover_features, how="outer")
            # Reset `leftover_features` to `None` to avoid joining it again
            leftover_features = None

        iter_cols = iter(df.columns)

        # Yield batches of `batch_cols` columns
        while cols_batch := tuple(islice(iter_cols, batch_cols)):
            df_batch = df.loc[:, cols_batch]
            if df_batch.shape[1] < batch_cols:
                leftover_features = [df_batch]
                break
            yield df_batch
    if leftover_features:
        yield pd.concat(leftover_features, axis=1)


def _convert_float_dtypes(df: pd.DataFrame, float_dtype: str) -> pd.DataFrame:
    """Converts all float columns to the specified dtype. Note that this mutates the
    original dataframe instead of creating a new one to limit impact on memory.

    The return value allows chaining this method with pipes
    """

    logger.debug("Converting dtypes. float: %s.", float_dtype)
    # Convert all float columns to the specified dtype
    # Note that we're using np.floating to select all numpy's float types
    float_cols = df.select_dtypes(np.floating).columns
    df[float_cols] = df[float_cols].astype(float_dtype)

    return df


def _convert_gene_sets_dtypes(df):
    # Convert binary columns to pd.UInt8Dt  ype to save memory and allow NaNs
    # At this point, binary columns can have any type as long as they only contain
    # 0, 1 or NaN
    binary_cols = _identify_binary_cols_raw_df(df).columns
    logger.debug("Converting %i binary columns to UInt8", len(binary_cols))
    df[binary_cols] = df[binary_cols].astype(pd.UInt8Dtype())
    return df


def _apply_winsorization(df: pd.DataFrame, q: float) -> pd.DataFrame:
    """Winsorize all float columns to the specified quantile"""

    logger.debug("Windsorising with quantile %f (df: %i rows; %i cols)", q, *df.shape)
    # Apply only to float columns
    df_floats = df.select_dtypes("float")
    if df_floats.empty:
        logger.debug("No quantitative features to winsorize!")
        return df
    # Get lower bounds
    lower_bounds = df_floats.quantile(q)
    # Get upper bounds
    upper_bounds = df_floats.quantile(1 - q)
    # Apply winsorization
    df.loc[:, df_floats.columns] = df_floats.clip(lower_bounds, upper_bounds, axis=1)
    return df


def _apply_scaling(df: pd.DataFrame, method: str = "zscore") -> pd.DataFrame:
    """Scale all float columns to the specified quantile"""

    logger.debug("Scaling ('%s'; df: %i rows; %i cols)", method, *df.shape)

    n_genes = len(df)
    data_scalers = {
        "zscore": StandardScaler,
        "minmax": MinMaxScaler,
        "rank": lambda: QuantileTransformer(
            output_distribution="normal", n_quantiles=n_genes, subsample=n_genes
        ),
        "robust": RobustScaler,
    }

    cls_scaler = data_scalers.get(method)
    if cls_scaler is None:
        raise ValueError(f"Unknown scaler: {method}")
    scaler = cls_scaler()

    # Apply only to float columns
    df_floats = df.select_dtypes("float")

    if df_floats.empty:
        logger.debug("No quantitative features to scale!")
        return df

    df.loc[:, df_floats.columns] = scaler.fit_transform(df_floats)
    return df


def apply_gene_sets_weighting(
    df: pd.DataFrame, scale: str | None, float_dtype: str
) -> pd.DataFrame:
    """Weight gene sets by their size"""

    logger.debug("Weighting binary features (df: %i rows; %i cols)", *df.shape)

    df_bin = (
        # Assume binary columns have been converted to UInt8 at this point
        df.copy().select_dtypes("UInt8")
    )

    # Get the number of features in which each gene appears
    n_sets_per_gene = df_bin.sum(axis=1)
    n_genes_in_multiple_sets = (n_sets_per_gene > 1).sum()

    if n_genes_in_multiple_sets == 0:
        logger.debug("No genes present in multiple gene sets. Skipping weighting.")
        return df

    logger.debug(
        "Weighting %i genes present in multiple gene sets", n_genes_in_multiple_sets
    )

    # Divide each gene's values by the number of gene sets in which it appears
    df_bin = df_bin.div(n_sets_per_gene, axis=0)

    # Robust scale the weighted values that have been
    if scale is not None:
        df_bin = _apply_scaling(df_bin, method=scale)

    # Replace the binary columns with the weighted ones
    df.loc[:, df_bin.columns] = _convert_float_dtypes(df_bin, float_dtype=float_dtype)

    return df


def _identify_binary_cols_raw_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the subset of columns of `df` that contain only binary values (0 or 1 or
    null)
    """
    # Using fillna as numpy's isin does not pandas NA values
    # Numpy's isin is faster than pandas isin when the number of values to check is
    # small
    binary_mask = np.isin(df.fillna(0), [0, 1, 0.0, 1.0])
    return df.loc[:, binary_mask.all(axis=0)]


def _filter_high_missing_cols(
    df: pd.DataFrame, thresholds: MissingnessThresholds
) -> pd.DataFrame:
    """
    Filter features based on the number of genes present in each set
    """

    # First filter gene sets
    is_high_missingness_bin = _get_high_missing_gene_sets_cols(df, thresholds.gene_set)
    n_bin = is_high_missingness_bin.sum()

    # Then filter quantitative features
    is_high_missingness_quant = _get_high_missing_quant_cols(
        df, thresholds.quant_feature
    )
    n_quant = is_high_missingness_quant.sum()

    # Combine both filters
    is_high_missingness_tot = is_high_missingness_bin | is_high_missingness_quant
    n_tot = is_high_missingness_tot.sum()

    logger.debug(
        "Dropping %i features for missingness (gene sets: %i; quant: %i)",
        *(n_tot, n_bin, n_quant),
    )
    return df.loc[:, ~is_high_missingness_tot]


def _get_high_missing_quant_cols(
    df: pd.DataFrame, max_missingness: float
) -> pd.Series[bool]:
    is_high_missingness = pd.Series(False, index=df.columns)

    # Assume binary columns have been converted to UInt8 at this point
    df_quant = df.drop(columns=df.select_dtypes("UInt8").columns)
    if df_quant.empty:
        return is_high_missingness

    missingness = df_quant.isnull().mean(axis=0)
    is_high_missingness.loc[missingness.index] = missingness > max_missingness

    logger.debug(
        "%i/%i quantitative features have missingness higher than %f",
        is_high_missingness.sum(),
        df_quant.shape[1],
        max_missingness,
    )

    return is_high_missingness


def _get_high_missing_gene_sets_cols(
    df: pd.DataFrame, min_size: int
) -> pd.Series[bool]:
    is_high_missingness = pd.Series(False, index=df.columns)

    logger.debug("Filtering gene sets with less than %i genes", min_size)

    # Assume binary columns have been converted to UInt8 at this point
    df_bin = df.select_dtypes("UInt8")
    if df_bin.empty:
        logging.info("No binary features to filter")
        return is_high_missingness

    gene_counts = df_bin.sum(axis=0)
    is_high_missingness.loc[gene_counts.index] = gene_counts < min_size

    logger.debug(
        "%i/%i gene sets have less than %i genes",
        is_high_missingness.sum(),
        df_bin.shape[1],
        min_size,
    )

    return is_high_missingness


def _filter_genes_missingness(df: pd.DataFrame, max_missingness: float) -> pd.DataFrame:
    """
    Drop genes with missingness higher than `max_missingness`. Note that a gene is
    considered missing if it is absent from a gene set (0) or has a missing value (NaN)
    """
    logger.debug("Dropping genes with missingness higher than %f", max_missingness)

    # Assume binary columns have been converted to UInt8 at this point
    df_bin = df.select_dtypes("UInt8")
    n_missing_bin = df_bin.shape[1] - df_bin.sum(axis=1)
    n_missing_others = df.drop(df_bin.columns, axis=1).isnull().sum(axis=1)

    missingness = (n_missing_bin + n_missing_others) / df.shape[1]

    is_high_missingness = missingness > max_missingness
    logger.debug("Dropping %i genes for missingness", is_high_missingness.sum())
    return df.loc[~is_high_missingness, :]


def _impute_missing_binary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simply sets all genes absent from a gene set to 0
    """

    # Assume binary columns have been converted to UInt8 at this point
    bin_cols = df.select_dtypes("UInt8").columns

    logger.debug("Setting missing gene sets values to 0 (%i cols)", len(bin_cols))
    df.loc[:, bin_cols] = df.loc[:, bin_cols].fillna(0)

    return df


def _impute_missing_quantitative(
    df: pd.DataFrame, method: str = "mean"
) -> pd.DataFrame:
    """
    Impute missing values float columns to the specified method
    """

    df_floats = df.select_dtypes("float")
    if df_floats.empty:
        logger.debug("No quantitative features to impute!")
        return df

    if method == "mean":
        imp_value = df_floats.mean()
    elif method == "median":
        imp_value = df_floats.median()
    else:
        raise ValueError(f"Unknown imputation method: {method}")

    logger.debug(
        "Calculating %s per column (df: %i rows; %i cols)...", method, *df.shape
    )

    logger.debug("Replacing NaNs with %s...", method)
    df.loc[:, df_floats.columns] = df_floats.fillna(imp_value)

    return df


def _display_df_info(df: pd.DataFrame, msg: str | None = None) -> pd.DataFrame:
    """
    Display information about a dataframe
    """
    # Skip if not in debug mode
    if logger.level > logging.DEBUG:
        return df

    if msg is not None:
        logger.debug(msg)

    logger.debug("Shape: %i rows; %i cols", *df.shape)

    # Get human readable memory usage
    buffer = StringIO()
    df.info(memory_usage="deep", buf=buffer, verbose=False)
    str_info = buffer.getvalue()
    # Remove the first line (the dataframe type)
    for line in str_info.split("\n")[1:]:
        if line.strip():
            logger.debug(line)

    return df


def merge_features(
    path_features: Sequence[Path],
    float_dtype: str = "float32",
    weight_gene_sets: bool = False,
    winsorize: float | None = None,
    scale: str | None = "robust",  # "zscore", "minmax", "rank", "robust"
    batch_size: int = 5000,
    miss_thres: MissingnessThresholds | None = None,
    impute: str | None = None,  # "mean", "median"
) -> pd.DataFrame:
    """
    Merge all feature files in `path_features` into a single matrix.

    """

    logger.info("Merging features from %i files", len(path_features))

    if miss_thres is None:
        miss_thres = MissingnessThresholds(
            gene=0.95,
            gene_set=10,
            quant_feature=0.95,
        )

    # Note that the `identity` function is used when a step is skipped
    df_merged = (
        pd.concat(
            [
                df_batch
                # First try to convert binary columns to UInt8 to save memory
                # and allow NaNs. This also allows to identify binary columns
                # more efficiently for the following steps
                .pipe(_convert_gene_sets_dtypes)
                # Use `identity` when no winsorization is requested
                .pipe(
                    _apply_winsorization if winsorize is not None else identity,
                    q=winsorize,
                )
                # Same for scaling
                .pipe(_apply_scaling if scale is not None else identity, method=scale)
                # Convert dtypes only after winsorization and scaling to limit
                # consequences of rounding errors
                .pipe(_convert_float_dtypes, float_dtype=float_dtype).pipe(
                    _display_df_info, msg="Processed chunk info:"
                )
                for df_batch in iter_feature_files(path_features, batch_cols=batch_size)
            ],
            axis=1,
        )
        .pipe(_display_df_info, msg="Merged dataframe info:")
        # Filter features with high missingness. Doing this after merging all features
        # as some genes may not be present in all feature files
        .pipe(_filter_high_missing_cols, thresholds=miss_thres)
        # Filter genes with high missingness
        .pipe(_filter_genes_missingness, max_missingness=miss_thres.gene)
        # Show info after filtering
        .pipe(
            _display_df_info, msg="Merged dataframe info after missingness filtering:"
        )
        # Set missing binary values to 0
        .pipe(_impute_missing_binary)
        # Impute missing values for remaining features
        .pipe(
            _impute_missing_quantitative if impute is not None else identity,
            method=impute,
        )
        # Apply gene sets weighting if requested only after all features have been
        # merged as it requires the number of gene sets in which each gene
        .pipe(
            apply_gene_sets_weighting if weight_gene_sets else identity,
            scale=scale,
            float_dtype=float_dtype,
        )
        .pipe(_display_df_info, msg="Processed dataframe info:")
    )

    if df_merged.isnull().any().any():
        nan_cols = df_merged.columns[df_merged.isnull().any()]
        logger.warning(
            f"NaNs found in the final features matrix. {len(nan_cols)} columns "
            f"affected: {nan_cols.values}"
        )
        logger.warning(
            "If this is unexpected, please check that an imputation method was "
            "specified and that the missingness threshold is properly set."
        )

    return df_merged


def write_merged_features_file(
    path_features: Sequence[Path],
    prefix_output: FilePrefix,
    float_dtype: str = "float32",
    weight_gene_sets: bool = False,
    winsorize: float | None = None,
    scale: str | None = "robust",  # "zscore", "minmax", "rank", "robust"
    batch_size: int = 5000,
    missingness_thresholds: MissingnessThresholds | None = None,
    impute: str | None = None,  # "mean", "median"
) -> None:
    """
    Merge all feature files in `path_features` into a single dataframe and save it
    as a parquet file with name `path_output`.

    Args:
        path_features (Sequence[Path]): List of paths to feature files.
        prefix_output (FilePrefix): Prefix of output including path to directory.
        float_dtype (str, optional): Data type for float columns. Defaults to "float32".
        weight_gene_sets (bool, optional): Whether to weight gene sets by their size.
            Defaults to False.
        winsorize (float | None, optional): Quantile to use for winsorization. Defaults
            to None.
        scale (str | None, optional): Scaling method to use. Defaults to "robust".
        batch_size (int, optional): Number of columns to read at a time. Defaults to
            5000.
        missingness_thresholds (MissingnessThresholds | None, optional): Missingness
            thresholds to use. Defaults to None.
        impute (str | None, optional): Imputation method to use. Defaults to None.
    """

    if not prefix_output.parent.is_dir():
        raise Exception(f"prefix_output: {prefix_output}")

    df_merged = merge_features(
        path_features,
        float_dtype=float_dtype,
        weight_gene_sets=weight_gene_sets,
        winsorize=winsorize,
        scale=scale,
        batch_size=batch_size,
        miss_thres=missingness_thresholds,
        impute=impute,
    )

    f_out = prefix_output.join(pg_tables.EXT_PARQUET)
    logger.info("Saving merged features to %s", f_out)

    df_merged.to_parquet(f_out, compression="snappy", index=True)

    # Save column names to a file. This is useful to extract specific features from
    # the parquet file later on
    f_cols = prefix_output.join(".columns.gz")
    df_merged.columns.to_series().to_csv(f_cols, index=False, compression="gzip")
