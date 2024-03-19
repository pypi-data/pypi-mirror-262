from pathlib import Path

import click
from click_option_group import RequiredAllOptionGroup, optgroup

from perigene.models import Model
from perigene.perigene_types import FilePrefix

from .. import params_shared
from ..params_utils import log_arguments


@click.command(name="tuning", no_args_is_help=True)
@optgroup.group(
    "Mandatory",
    cls=RequiredAllOptionGroup,
)
@params_shared.param_prefix_analyses
@optgroup.group("Optional")
@params_shared.param_target_chromosome
@params_shared.param_model_cls
@params_shared.param_path_features
@params_shared.param_path_gene_scores
@params_shared.param_grp_tuning
@log_arguments
def model_tuning(
    prefix: FilePrefix,
    target_chromosome: str,
    model_cls: type[Model] | None,
    fname_features: Path | None,
    fname_gene_scores: Path | None,
    ntrials: int,
    storage: str,
    overwrite_existing_studies: bool,
) -> None:
    """Hyperparameter search using 10-fold cross validation with optuna."""
    from perigene.data import Data
    from perigene.info import PERiGeneInfo
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

    m.hyperparameter_tuning(
        ntrials=ntrials, storage=storage, overwrite_study=overwrite_existing_studies
    )
    m.save()

    # Saving info separately as not handled by TrainingManager
    m.info.save(prefix)
