"""Wrapper around the different pre-processing commands.
"""

import click

from .params_utils import NaturalOrderGroup
from .subcmds_preprocessing.subcmd_magma import process_magma_output
from .subcmds_preprocessing.subcmd_merge_features import merge_features


@click.group(
    name="pre-processing",
    no_args_is_help=True,
    options_metavar="",
    invoke_without_command=True,
    cls=NaturalOrderGroup,
)
def preprocessing() -> None:
    """Process and format data files used to run the prioritization."""
    pass


preprocessing.add_command(process_magma_output)
preprocessing.add_command(merge_features)
