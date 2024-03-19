from pathlib import Path

import click
from click_option_group import RequiredAllOptionGroup, optgroup

from perigene.data import Data
from perigene.info import PERiGeneInfo
from perigene.models import Model
from perigene.perigene_types import FilePrefix

from .. import params_shared
from ..params_utils import log_arguments


@click.command(name="predict", no_args_is_help=True)
@optgroup.group(
    "Mandatory",
    cls=RequiredAllOptionGroup,
)
@params_shared.param_prefix_analyses
@optgroup.group("Optional")
@params_shared.param_model_cls
@params_shared.param_path_features
@params_shared.param_path_gene_scores
@params_shared.param_target_chromosome
@log_arguments
def predict(
    prefix: FilePrefix,
    model_cls: type[Model] | None,
    fname_features: Path | None,
    fname_gene_scores: Path | None,
    target_chromosome: str,
) -> None:
    """Trains models and calculates scores for the selected target chromosome.

    Trains models and predict scores using leave-one-chromosme out approach using all
    training sets. Saves predicted scores as well as models weights.
    """
    from perigene.training import TrainingManager

    info = PERiGeneInfo.read(prefix).set_attrs(
        model=model_cls,
        path_features=fname_features,
        path_scores=fname_gene_scores,
    )

    if info.model is None:
        raise ValueError("No model has been specified.")
    if info.paths.features is None:
        raise ValueError("Features file has not been specified.")
    if info.paths.scores is None:
        raise ValueError("Gene scores file has not been specified.")

    subset_models = None if target_chromosome == "all" else [target_chromosome]

    data = Data.load(
        prefix=prefix,
        path_features=info.paths.features,
        path_scores=info.paths.scores,
        subset_models=subset_models,
    )

    m = TrainingManager.new(prefix, data, info)
    m.train().predict_from_models().save()

    info.save(prefix)
