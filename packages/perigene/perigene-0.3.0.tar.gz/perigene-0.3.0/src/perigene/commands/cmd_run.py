import logging
from collections.abc import Sequence
from pathlib import Path

import click
from click_option_group import RequiredAllOptionGroup, optgroup

from perigene.commands import params_shared
from perigene.commands import params_utils as utils

__all__ = ["run"]

logger = logging.getLogger(__name__)

MODELS: list[str] = [
    "reg-lasso",
    "reg-ridge",
    "reg-elasticnet",
    # "reg-gb",
]


@click.command(name="run", no_args_is_help=True)
@optgroup.group(
    "Mandatory",
    cls=RequiredAllOptionGroup,
)
@params_shared.param_prefix_analyses
@params_shared.param_path_features
@params_shared.param_path_gene_scores
@optgroup.group("Optional")
@params_shared.param_skip_existing
@params_shared.param_target_chromosome
@params_shared.param_mask_region
@params_shared.param_model_cls
@optgroup.group("Feature selection")
@params_shared.param_grp_feature_selection
@optgroup.group("Model tuning")
@params_shared.param_grp_tuning
@utils.log_arguments
def run(
    prefix: utils.FilePrefixProtocol,
    fname_features: Path,
    fname_gene_scores: Path,
    skip_existing: bool,
    target_chromosome: str,
    excluded_regions: Sequence[utils.RegionProtocol],
    model_cls: type[utils.ModelProtocol] | None,
    excluded_features: Sequence[str],
    min_var: float,
    max_var_diff: float,
    max_p: float,
    max_cross_corr: float,
    max_features: int,
    batch_size: int,
    rfe_n_thresholds: int,
    rfe_shrink_threshold: float,
    ntrials: int,
    storage: str,
    overwrite_existing_studies: bool,
) -> None:
    """Run the complete prioritization pipeline."""
    from typing import cast

    import perigene.feature_selection as pg_fs
    import perigene.info as pg_info
    from perigene.constants import ColInternal, FileSuffix
    from perigene.data import Data
    from perigene.data_tables import GeneScores
    from perigene.models import Model
    from perigene.perigene_types import FilePrefix, Region
    from perigene.training import TrainingManager

    # Cast FilePrefixProtocol to FilePrefix, RegionProtocol to Region
    prefix_ = cast(FilePrefix, prefix)
    excluded_regions_ = [cast(Region, r) for r in excluded_regions]
    model_cls_ = cast(type[Model], model_cls)

    scores = GeneScores.from_path(fname_gene_scores)

    if target_chromosome == "all":
        subset_models = scores.data[ColInternal.CHR].unique()
    else:
        subset_models = [target_chromosome]

    # ############################
    # Feature selection
    # ############################

    params = pg_fs.FeatureSelectionParams(
        excluded_regions=excluded_regions_,
        excluded_features=excluded_features,
        min_var=min_var,
        max_var_diff=max_var_diff,
        max_p=max_p,
        max_cross_corr=max_cross_corr,
        n_features_post_univ=max_features,
        batch_size=batch_size,
        rfe_n_thres=rfe_n_thresholds,
        rfe_step_shrink_thres=rfe_shrink_threshold,
    )

    if skip_existing and prefix_.join(FileSuffix.INDEX_FEATURES).is_file():
        existing_index = pg_fs.IndexDict.load(prefix_, subset_models)
        subset_models_fs = [
            name for name in subset_models if name not in existing_index.keys()
        ]
    else:
        subset_models_fs = subset_models
        existing_index = pg_fs.IndexDict()

    index_dict = pg_fs.create_index_dict(
        scores=scores,
        fname_features=fname_features,
        target_chromosomes=subset_models_fs,
        params=params,
    )

    # Save index files
    index_dict.save(prefix_)

    if prefix_.join(FileSuffix.INFO).is_file():
        info = pg_info.PERiGeneInfo.read(prefix_)
    else:
        info = pg_info.PERiGeneInfo()

    # Save info regarding feature selection to JSON file
    info = info.set_attrs(
        path_features=fname_features,
        path_scores=fname_gene_scores,
        fs_excluded_features=excluded_features,
        fs_min_variance=min_var,
        fs_max_var_diff=max_var_diff,
        fs_max_pvalue=max_p,
        fs_max_cross_corr=max_cross_corr,
        fs_max_features=max_features,
        excluded_regions=excluded_regions_,
    )

    info.save(prefix_)

    # ############################
    # Tuning
    # ############################

    # Add model class to info
    info = info.set_attrs(model=model_cls_)

    data = Data.load(
        prefix=prefix_,
        path_features=info.paths.features,
        path_scores=info.paths.scores,
        subset_models=subset_models,
    )

    training_manager = (
        TrainingManager.new(prefix_, data, info)
        .hyperparameter_tuning(
            ntrials=ntrials, storage=storage, overwrite_study=overwrite_existing_studies
        )
        .train()
    )
    info.save(prefix_)

    # ############################
    # Prediction
    # ############################

    training_manager.predict_from_models().save()
    info.save(prefix_)
