from collections.abc import Sequence
from pathlib import Path

import click
from click_option_group import RequiredAllOptionGroup, optgroup

from perigene.perigene_types import FilePrefix, Region

from .. import params_shared
from ..params_utils import log_arguments


@click.command(name="feature-selection", no_args_is_help=True)
@optgroup.group("Mandatory", cls=RequiredAllOptionGroup)
@params_shared.param_prefix_analyses
@params_shared.param_path_features
@params_shared.param_path_gene_scores
@optgroup.group("Optional")
@params_shared.param_target_chromosome
@params_shared.param_mask_region
@params_shared.param_grp_feature_selection
@log_arguments
def feature_selection(
    prefix: FilePrefix,
    fname_features: Path,
    fname_gene_scores: Path,
    target_chromosome: str,
    excluded_regions: Sequence[Region],
    excluded_features: Sequence[str],
    min_var: float,
    max_var_diff: float,
    max_p: float,
    max_cross_corr: float,
    max_features: int,
    batch_size: int,
    rfe_n_thresholds: int,
    rfe_shrink_threshold: float,
) -> None:
    """
    Selection of features individually associated with the gene scores. The feature
    selection is done from a set of features contained in a parquet file (c.f.
    pre-processing command 'merge-features') and requires a bed containing gene scores
    with the following columns: 'chrom', 'start', 'end', 'gene', 'score'
    Features are selected separately on the training genes used for each model.
    """

    from perigene import info
    from perigene.constants import ColInternal, FileSuffix
    from perigene.data_tables import GeneScores
    from perigene.feature_selection import FeatureSelectionParams, create_index_dict

    scores = GeneScores.from_path(fname_gene_scores)

    if target_chromosome == "all":
        list_target_chromosomes = scores.data[ColInternal.CHR].unique()
    else:
        list_target_chromosomes = [target_chromosome]

    params = FeatureSelectionParams(
        excluded_regions=excluded_regions,
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
    index_dict = create_index_dict(
        scores=scores,
        fname_features=fname_features,
        target_chromosomes=list_target_chromosomes,
        params=params,
    )

    # Save index files
    index_dict.save(prefix)

    if prefix.join(FileSuffix.INFO).is_file():
        perigene_info = info.PERiGeneInfo.read(prefix)
    else:
        perigene_info = info.PERiGeneInfo()

    # Save info regarding feature selection to JSON file
    perigene_info = perigene_info.set_attrs(
        path_features=fname_features,
        path_scores=fname_gene_scores,
        fs_excluded_features=excluded_features,
        fs_min_variance=min_var,
        fs_max_var_diff=max_var_diff,
        fs_max_pvalue=max_p,
        fs_max_cross_corr=max_cross_corr,
        fs_max_features=max_features,
        excluded_regions=excluded_regions,
    )

    perigene_info.save(prefix)
