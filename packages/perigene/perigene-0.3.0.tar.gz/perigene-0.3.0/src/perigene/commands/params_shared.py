import functools
from collections.abc import Callable
from pathlib import Path

import click
from click_option_group import optgroup

from .callbacks import get_model_cls, get_region_list, make_file_prefix, read_lines

__all__ = [
    "param_prefix_analyses",
    "param_target_chromosome",
    "param_path_features",
    "param_path_gene_scores",
    "param_model_cls",
    "param_mask_region",
    "param_grp_feature_selection",
    "param_grp_tuning",
]


def param_prefix_analyses(func: Callable) -> Callable:
    """Wrapper adding '--prefix' to a command"""

    @optgroup.option(
        "--prefix",
        "-p",
        default="PERiGene",
        metavar="<prefix>",
        help="Prefix for the analysis, including the path to the folder.",
        type=click.Path(file_okay=False, path_type=Path),
        callback=make_file_prefix,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_skip_existing(func: Callable) -> Callable:
    """Wrapper adding '--skip-existing' to a command"""

    @optgroup.option(
        "--skip-existing",
        is_flag=True,
        default=False,
        help="""
        Skip steps that have already been completed in a previous run.
        [WARNING] This is currently ignored!
        """,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_target_chromosome(func: Callable) -> Callable:
    """
    Wrapper adding the '--target-chromosome' to a command
    (variable name: target_chromosome)
    """

    @optgroup.option(
        "--target-chromosome",
        metavar="<str>",
        type=click.Choice([str(i) for i in range(1, 23)] + ["X", "Y", "all"]),
        default="all",
        help="""
        Chromosome for which to make predictions (i.e. '1', '2', '3', etc. or 'X',
        'y' or 'all'). PERiGene will only use information from genes on other
        chromosomes to 1. select features and 2. train a model for a target chromosome.
        When using 'all', PERiGene makes the feature selection iteratively for each
        chromosome found in the genes loc file. If the target chromosome is absent
        from the genes loc file, PERiGene will use all the genes. This option can be
        used to make predictions on a chromosome for which gene scores are not
        available (e.g. for sex chromosomes).
        """,
        show_default=True,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_path_features(func: Callable) -> Callable:
    """
    Wrapper adding the '--features' to a command (variable name: fname_features)
    """

    @optgroup.option(
        "--features",
        "fname_features",
        metavar="<file>",
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        help="""Path to parquet file containing the feature matrix.
            """,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_path_gene_scores(func: Callable) -> Callable:
    """
    Wrapper adding the '--gene-scores' to a command (variable name: fname_gene_scores)
    """

    @optgroup.option(
        "--gene-scores",
        "fname_gene_scores",
        metavar="<file>",
        help="""Path to bed file containing the gene scores.""",
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_model_cls(func: Callable) -> Callable:
    """
    Wrapper adding the '--model' to a command (variable name: model_cls)
    """
    # WARNING: This list should match the keys in perigene.models.MODELS_STR_MAP!
    # We are not importing MODELS_STR_MAP directly for performance reasons
    models_str = [
        "reg-lasso",
        "reg-ridge",
        "reg-elasticnet",
        # "reg-gb",
    ]

    @optgroup.option(
        "--model",
        "model_cls",
        metavar="<str>",
        type=click.Choice(models_str),
        default="reg-ridge",
        show_default=True,
        help=f"""
        Model used for the predicted score. Choice between: {', '.join(models_str)}
        """,
        callback=get_model_cls,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_mask_region(func: Callable) -> Callable:
    """
    Wrapper adding the '--mask-region' to a command (variable name: excluded_regions)
    """

    @optgroup.option(
        "--mask-region",
        "excluded_regions",
        metavar="<chr:start-end>",
        multiple=True,
        default=list(),
        help="""Region (CHR:START-END) to mask from the training data (e.g. to remove
            HLA from training).
            This argument can be used more than once to exclude several regions.
            Masked regions are also ignored when selecting features and searching for
            optimal hyperparameters.
            """,
        type=str,
        callback=get_region_list,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_grp_feature_selection(func: Callable) -> Callable:
    """
    Wrapper adding the following options to a command:

    --excluded-features (variable name: excluded_features)
    --min-var (variable name: min_var)
    --max-var-diff (variable name: max_var_diff)
    --max-p (variable name: max_p)
    --max-cross-corr (variable name: max_cross_corr)
    --max-features-post-univariate (variable name: max_features)
    --batch-size (variable name: batch_size)
    --rfe-n-thresholds (variable name: rfe_n_thresholds)
    --rfe-shrink-threshold (variable name: rfe_shrink_threshold)
    """

    @optgroup.option(
        "--excluded-features",
        metavar="<file>",
        type=click.Path(exists=True, dir_okay=False, path_type=Path),
        default=None,
        show_default=True,
        help="""Path to file containing a list of features to exclude from the analysis.
            The file should contain one feature name per line.
            """,
        callback=read_lines,
    )
    @optgroup.option(
        "--min-var",
        metavar="<float>",
        default=1e-9,
        type=click.FloatRange(min=0),
        show_default=True,
        help="""Minimum feature variance on the training or target chromosome
        (if present). Features with a variance lower than this will be removed. Note
        that this is applied to both quantitative features and gene sets and
        can therefore remove gene sets containing few genes if the threshold is
        too high. Use a low value (e.g. 1e-9) to remove only constant features.
        """,
    )
    @optgroup.option(
        "--max-var-diff",
        metavar="<float>",
        default=3,
        type=click.FLOAT,
        show_default=True,
        help="""
        Maximal feature variance difference between the target chromosome and the other
        chromosomes. For instance a value of 3 means that feature variance on the target
        chromosome (V_target) should be in the range [V_other/3, 3*V_other], where
        V_other is the variance of the feature on the other/training chromosomes.
        Features outside this range will be removed.
        """,
    )
    @optgroup.option(
        "--max-p",
        metavar="<float>",
        help="""pvalue threshold under which features are kept.
        Assuming continuous gene scores, we use Mann-Whitney tests for binary features
        - testing for a difference in median gene scores between the two groups - and
        Spearman's rho for quantitative ones.
        """,
        default=0.001,
        show_default=True,
        type=click.FloatRange(min=0, max=1, max_open=True),
    )
    @optgroup.option(
        "--max-features-post-univariate",
        "max_features",
        metavar="int",
        help="""
        Maximum number of features to keep after the univariate filtering step.
        If applied, only the top N with the lowest pvalues for association with the
        gene scores are kept. Note that this is applied before the cross-correlation
        and RFE steps, so the final number of features can be lower.
        """,
        default=10_000,
        show_default=True,
        type=click.IntRange(min=1),
    )
    @optgroup.option(
        "--max-cross-corr",
        metavar="<float>",
        help="""Filter out highly correlated features. If two features are correlated,
        we only keep the one with the lowest pvalue.
        Binary and quantitative features are tested separately: using either
        Jaccard coefficient or Spearman's rho.
        """,
        default=0.9,
        show_default=True,
        type=click.FloatRange(min=0, max=1, max_open=True),
    )
    @optgroup.option(
        "--batch-size",
        metavar="<int>",
        help="""
        Number of features to load at once when performing the univariate
        filtering step.
        """,
        default=10_000,
        show_default=True,
        type=click.IntRange(min=1),
    )
    @optgroup.option(
        "--rfe-n-thresholds",
        "rfe_n_thresholds",
        metavar="<int>",
        help="""
        Number of features below which the RFE algorithm is stopped.

        /!\\ If this number is larger than the number of features remaining
        after the univariate filtering step, the RFE algorithm will be skipped
        entirely.
        """,
        default=2500,
        show_default=True,
        type=click.IntRange(min=1),
    )
    @optgroup.option(
        "--rfe-shrink-threshold",
        "rfe_shrink_threshold",
        metavar="<float>",
        help="""
        Minimum proportion of features to remove at each iteration of the RFE algorithm.
        If the proportion of features removed after a step of RFE is smaller than
        this value, the algorithm is stopped and the remaining features are kept.
        For instance, a value of 0.1 means that the algorithm will stop if the
        proportion of features dropped at a step is less than 10%.
        Note that setting this value to 1 does not prevent the algorithm from running
        the first RFE step. To skip RFE entirely, set '--rfe-n-thresholds' to a value
        larger than the number of features remaining after the univariate filtering.
        """,
        default=0.1,
        show_default=True,
        type=click.FloatRange(min=0, max=1, max_open=True),
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def param_grp_tuning(func: Callable) -> Callable:
    """
    Wrapper adding the following options to a command:

    --ntrials (variable name: ntrials)
    --storage (variable name: storage)
    --overwrite/--no-overwrite (variable name: overwrite_existing_studies)
    """

    def _erase_callback(ctx, param, value) -> bool:
        # Flag value takes precedence over default
        if value is not None:
            return value

        # Otherwise, default depends on storage (erase if storage is not given)
        storage = ctx.params.get("storage")
        return storage is None

    @optgroup.option(
        "--storage",
        metavar="<str>",
        help="""
            Journal file used by optuna to store trial results. By default, creates this
            file in the analysis directory ('<prefix>.optuna.journal')
            """,
        type=str,
        default=None,
    )
    @optgroup.option(
        "--ntrials",
        metavar="<int>",
        help="""
            Number of combinations of hyperparameters tested.
            """,
        type=click.IntRange(min=1),
        default=20,
    )
    @optgroup.option(
        "--overwrite/--no-overwrite",
        "overwrite_existing_studies",
        metavar="<bool>",
        help="""
            Whether to overwrite any pre-existing study corresponding to the target
            chromosome if they already exist or not.
            Default is to erase old studies before starting hyperparameter tuning
            if the storage parameter is not supplied and not to erase it otherwise.
            """,
        type=click.BOOL,
        default=None,
        callback=_erase_callback,
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
