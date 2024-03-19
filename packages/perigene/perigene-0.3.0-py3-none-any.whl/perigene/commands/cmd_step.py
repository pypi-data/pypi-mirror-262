import logging

import click

from perigene.commands.params_utils import NaturalOrderGroup

from .subcmds_step.subcmd_feature_selection import feature_selection
from .subcmds_step.subcmd_predict import predict
from .subcmds_step.subcmd_tuning import model_tuning

logger = logging.getLogger(__name__)


@click.group(
    name="step",
    no_args_is_help=True,
    options_metavar="",
    invoke_without_command=True,
    cls=NaturalOrderGroup,
)
def step() -> None:
    """Initialize analysis folder, tune and train models and run predictions."""
    pass


step.add_command(feature_selection)
step.add_command(model_tuning)
step.add_command(predict)
