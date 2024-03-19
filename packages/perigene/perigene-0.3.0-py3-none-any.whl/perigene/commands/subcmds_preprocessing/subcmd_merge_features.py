from pathlib import Path

import click
from click_option_group import RequiredAllOptionGroup, optgroup

from ..callbacks import make_file_prefix
from ..params_utils import FilePrefixProtocol, log_arguments


@click.command(name="merge-features", no_args_is_help=True)
###############################################################################
@optgroup.group("Mandatory parameters", cls=RequiredAllOptionGroup)
@optgroup.option(
    "--path-features",
    metavar="<file>",
    help="""Path to feature file. This option can be used multiple times to provide more
    than one path. File names can contain glob patterns (*, ?), which will be expanded
    (If using a glob pattern in a shell script you may need to put the path in quotes
    and/or use the 'set -f' option to prevent the shell from expanding it).
    Can read feature from tab-separated, comma-separated, parquet and gmt files. Unless
    the file is a gmt file, the files should have a header with the feature names and a
    column named 'GENE' containing the gene names.
    """,
    type=click.Path(dir_okay=False, path_type=Path),
    multiple=True,
)
@optgroup.option(
    "--prefix-out",
    metavar="<path/to/folder/prefix>",
    help="Prefix of output including path to directory.",
    default="./features",
    type=click.Path(file_okay=False, path_type=Path),
    callback=make_file_prefix,
)
###############################################################################
@optgroup.group("Optional parameters")
@optgroup.option(
    "--winsorize",
    metavar="<float>",
    help="""Winsorize features to remove outliers. Winsorization is done by replacing
    values above q with the value at q and values below 1-q with the value at 1-q,
    where q is the provided quantile. Winsorization is applied before scaling and
    can be used to prevent it from being affected by outliers (e.g. when using
    minmax or zscore scaling).
    By default, walues are winsorized at 0.01 (i.e. values below the 1st percentile and
    above the 99th percentile are replaced with the values at the 1st and 99th).
    The winsorization can be disabled by setting this parameter to 0.
    """,
    default=0.01,
    show_default=True,
    type=click.FloatRange(min=0, max=1, max_open=False),
    # Convert 0 to None
    callback=lambda ctx, param, value: None if value == 0 else value,
)
@optgroup.option(
    "--scale",
    metavar="<str>",
    help="""Scale features. By default, no scaling is done. If a value is provided,
    it should be one of: zscore, minmax, rank or robust.
    """,
    default="minmax",
    show_default=True,
    type=click.Choice(["zscore", "minmax", "rank", "robust"]),
)
@optgroup.option(
    "--weight-gene-sets",
    help="""Weight gene sets by the number of genes in the set. By default, gene sets
    are not weighted.
    """,
    is_flag=True,
    default=False,
    show_default=True,
)
@optgroup.option(
    "--batch-size",
    metavar="<int>",
    help="""Number of features to process at a time (for the dtype conversion,
    winsorization and scaling steps). By default, features are processed in chunks of
    10000 columns. Note that some steps after the dtype conversion are
    still done with all features in memory (e.g. gene set weighting, imputation).
    """,
    default=15_000,
    show_default=True,
    type=click.IntRange(min=1),
)
@optgroup.option(
    "--impute",
    metavar="<str>",
    help="""Impute missing values. By default, no imputation is done. If a value is
    provided, it should be one of: mean or median.
    """,
    default=None,
    show_default=True,
    type=click.Choice(["mean", "median", "none"]),
    callback=lambda ctx, param, value: None if value == "none" else value,
)
@optgroup.option(
    "--max-quant-feature-missingness",
    metavar="<float>",
    help="""Maximum missingness allowed for a quantitative feature. If a feature has a
    fraction of missing values higher than the provided value, it will be dropped.
    By default, this is set to 0.2.
    """,
    default=0.2,
    show_default=True,
    type=click.FloatRange(min=0, max=1),
)
@optgroup.option(
    "--min-gene-set-size",
    metavar="<int>",
    help="""Minimum number of genes in a gene set. Gene sets with fewer genes will be
    dropped. By default, this is set to 10.
    """,
    default=10,
    show_default=True,
    type=click.IntRange(min=1),
)
@optgroup.option(
    "--max-gene-missingness",
    metavar="<float>",
    help="""Maximum missingness allowed for a gene. If a gene has a fraction of
    missing values higher than the provided value, it will be dropped. Note: tolerates
    a higher fraction of missing values than max-feature-missingness because some genes
    may be present in very few gene sets or absent from some gmt files. This can result
    in many NaN values when converted to matrices that are merged together.
    By default, this is set to 0.95.
    """,
    default=0.95,
    show_default=True,
    type=click.FloatRange(min=0, max=1),
)
@optgroup.option(
    "--float-dtype",
    metavar="<str>",
    help="""Data type to use for the output. By default, features are written as
    float32. If a value is provided, it should be one of: float32 or float64.
    Note that the default may round some small values to 0.
    """,
    default="float32",
    show_default=True,
    type=click.Choice(["float32", "float64"]),
)
@log_arguments
def merge_features(
    path_features: list[Path],
    prefix_out: FilePrefixProtocol,
    winsorize: float | None,
    weight_gene_sets: bool,
    scale: str | None,
    batch_size: int,
    impute: str | None,
    max_quant_feature_missingness: float,
    min_gene_set_size: int,
    max_gene_missingness: float,
    float_dtype: str = "float32",
) -> None:
    """Merges multiple features files into a single parquet file. Applies some
    minimal pre-processing steps (dtype conversion, winsorization, scaling, imputation
    and missingness filtering) to the features before merging them.

    Example:

    perigene pre-processing merge-features \\ \n
        --path-features ./features/*.tsv.gz \\ \n
        --path-features ./other_features.gmt \\ \n
        --prefix-out ./merged_features

    """

    from typing import cast

    from perigene.perigene_types import FilePrefix
    from perigene.preprocessing.features_merging import (
        MissingnessThresholds,
        write_merged_features_file,
    )

    # Expand glob patterns
    path_features = [p for p in path_features for p in p.parent.glob(p.name)]

    write_merged_features_file(
        path_features,
        cast(FilePrefix, prefix_out),
        batch_size=batch_size,
        scale=scale,
        weight_gene_sets=weight_gene_sets,
        winsorize=winsorize,
        missingness_thresholds=MissingnessThresholds(
            gene=max_gene_missingness,
            quant_feature=max_quant_feature_missingness,
            gene_set=min_gene_set_size,
        ),
        impute=impute,
        float_dtype=float_dtype,
    )
