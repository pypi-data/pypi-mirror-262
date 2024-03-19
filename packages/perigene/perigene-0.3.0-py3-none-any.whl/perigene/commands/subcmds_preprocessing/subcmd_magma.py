from collections.abc import Sequence
from pathlib import Path

import click
from click_option_group import RequiredAllOptionGroup, optgroup

from ..callbacks import get_nullable_str, make_file_prefix, split_commas
from ..params_utils import FilePrefixProtocol, log_arguments


@click.command(name="magma", no_args_is_help=True)
###############################################################################
@optgroup.group(
    "Mandatory parameters",
    cls=RequiredAllOptionGroup,
)
@optgroup.option(
    "--prefix-magma",
    metavar="</path/to/folder/prefix>",
    help="""Prefix of MAGMA files including path. Required files are
    '<prefix>.genes.out' and '<prefix>.genes.raw'.
    """,
    default="./magma",
    type=click.Path(path_type=Path),
    callback=make_file_prefix,
)
@optgroup.option(
    "--prefix-out",
    metavar="</path/to/folder/prefix>",
    help="""Prefix of output files including path. Output files are
    '<prefix>.genes.zscores' and '<prefix>.genes.locations'.""",
    type=click.Path(file_okay=False, path_type=Path),
    default="./magma.formatted",
    callback=make_file_prefix,
)
@optgroup.group("Optional parameters")
@optgroup.option(
    "--subset-covariates",
    metavar="<str>",
    help="""Comma-separated list of covariates to use. If empty,
    using all the covariates used by MAGMA. Possible covariates are:
    'GENE_SIZE', 'INV_MAC', 'DENSITY', 'LOG_GENE_SIZE', 'LOG_INV_MAC', 'LOG_DENSITY'
    """,
    type=str,
    default=None,
    callback=split_commas,
)
@optgroup.option(
    "--transform",
    metavar="<str>",
    help="""Transform to apply to the projected MAGMA z-scores. Possible values are:
    'minmax', 'log' or 'none'.
    """,
    default="minmax",
    type=click.Choice(["log", "minmax", "none"]),
    show_default=True,
    callback=get_nullable_str,
)
@optgroup.option(
    "--save-raw",
    metavar="<bool>",
    help="""Whether to save raw z-scores. If this flag is used, raw z-scores are
    saved in a separate bed file '<prefix-out>.scores.raw.bed'.
    """,
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
)
@optgroup.option(
    "--save-covariates",
    metavar="<bool>",
    help="""Whether to save covariates. If this flag is used, covariates are
    a separate file '<prefix-out>.covariates.tsv'.
    """,
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
)
@optgroup.option(
    "--save-correlation",
    metavar="<bool>",
    help="""Whether to save correlation matrix. If this flag is used, the correlation
    matrix is saved as a block diagonal matrix in a numpy file
    '<prefix-out>.block_corr.npz'.
    """,
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
)
@optgroup.option(
    "--min-offset-covariance",
    metavar="<float>",
    help="""Minimum offset to add to the covariance matrix diagonal
    to avoid singular matrix. You can try to increase this value if you
    get a singular matrix error.
    """,
    type=click.FloatRange(min=0.0),
    default=0.5,
    show_default=True,
)
@log_arguments
def process_magma_output(
    prefix_magma: FilePrefixProtocol,
    prefix_out: FilePrefixProtocol,
    subset_covariates: Sequence[str],
    transform: str | None,
    save_raw: bool,
    save_covariates: bool,
    save_correlation: bool,
    min_offset_covariance: float,
) -> None:
    """Formats the gene zscores from a MAGMA output to be used as input for PeriGene."""
    from typing import cast

    from perigene.perigene_types import FilePrefix
    from perigene.preprocessing.magma_output import format_magma_output

    if not subset_covariates or len(subset_covariates) == 0:
        covariates_names = None
    else:
        covariates_names = list(subset_covariates)

    # Cast to FilePrefix
    prefix_magma = cast(FilePrefix, prefix_magma)
    prefix_out = cast(FilePrefix, prefix_out)

    format_magma_output(
        magma_prefix=prefix_magma,
        prefix_out=prefix_out,
        covariates_names=covariates_names,
        min_offset_covariance=min_offset_covariance,
        transform=transform,
        save_raw=save_raw,
        save_covariates=save_covariates,
        save_correlation=save_correlation,
    )
