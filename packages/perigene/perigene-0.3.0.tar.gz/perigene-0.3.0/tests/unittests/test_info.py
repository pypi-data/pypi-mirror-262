from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st

import perigene.models as pg_models
import perigene.perigene_types as pg_types
from perigene.info import FeatureSelectionInfo, PathsInfo, PERiGeneInfo
from tests.helpers.strategies import path_strategy

_models_str = [m.__name__ for m in pg_models.MODELS_STR_MAP.values()]


def make_nullable(strategy: st.SearchStrategy) -> st.SearchStrategy:
    return st.one_of(st.none(), strategy)


# Define strategies for generating random inputs
none_or_str = make_nullable(st.text())
none_or_path = make_nullable(path_strategy())
none_or_float = make_nullable(st.floats(allow_nan=False, allow_infinity=False))
none_or_int = make_nullable(st.integers())
none_or_seq_str = make_nullable(st.lists(st.text()))
none_or_model_str = make_nullable(st.sampled_from(_models_str))
# none_or_seq_region = st.one_of(st.none(), st.lists(st.from_type(pgt.Region)))
none_or_dict_str_modelparams = make_nullable(
    st.dictionaries(st.text(), st.from_type(pg_types.ModelParametersDict))
)


@st.composite
def attribute_dict_strategies(draw: st.DrawFn) -> dict[str, Any]:
    return dict(
        version=draw(none_or_str),
        model=draw(none_or_model_str),
        path_features=draw(none_or_path),
        path_scores=draw(none_or_path),
        path_optuna_storage=draw(none_or_path),
        fs_min_variance=draw(none_or_float),
        fs_max_var_diff=draw(none_or_float),
        fs_max_pvalue=draw(none_or_float),
        fs_max_cross_corr=draw(none_or_float),
        fs_max_features=draw(none_or_int),
        fs_excluded_features=draw(none_or_seq_str),
        # excluded_regions=draw(none_or_seq_region),
        model_params=draw(none_or_dict_str_modelparams),
    )


# @reproduce_failure('6.93.1', b'AXicY2DAChgZAAAbAAI=')
@given(
    old_params=attribute_dict_strategies(),
    new_params=attribute_dict_strategies(),
)
@settings(max_examples=50, report_multiple_bugs=False)
def test_set_attrs(
    old_params: dict[str, Any],
    new_params: dict[str, Any],
):
    # Arrange

    # Create a PERiGeneInfo object
    info = PERiGeneInfo(
        _version=old_params["version"],
        _model=old_params["model"],
        _paths=PathsInfo(
            _features=old_params["path_features"],
            _scores=old_params["path_scores"],
            _optuna_storage=old_params["path_optuna_storage"],
        ),
        _feature_selection=FeatureSelectionInfo(
            _min_variance=old_params["fs_min_variance"],
            _max_var_diff=old_params["fs_max_var_diff"],
            _max_pvalue=old_params["fs_max_pvalue"],
            _max_cross_corr=old_params["fs_max_cross_corr"],
            _max_features=old_params["fs_max_features"],
            _excluded_features=old_params["fs_excluded_features"],
        ),
        # excluded_regions=old_params["excluded_regions"],
        _model_params=old_params["model_params"],
    )

    # Read values of attributes containing collections directly  from the
    # object as __post_init__ can initialize them if they were None
    # old_params["excluded_regions"] = info.excluded_regions
    old_params["model_params"] = info.model_params

    # Act

    # Call the function with the generated inputs
    info.set_attrs(**new_params)

    # Assert
    obj: PERiGeneInfo | PathsInfo | FeatureSelectionInfo
    for dict_key, new_dict_value in new_params.items():
        if dict_key.startswith("fs_"):
            obj = info.feature_selection
            attr = dict_key.removeprefix("fs")
        elif dict_key.startswith("path_"):
            obj = info.paths
            attr = dict_key.removeprefix("path")
        else:
            obj = info
            # Add underscore to check the private attribute and not the property method
            attr = "_" + dict_key

        obj_value = getattr(obj, attr)
        if new_dict_value is None:
            msg = f"The value of attribute {dict_key} should not have changed."
            assert obj_value is old_params[dict_key], msg
        else:
            msg = f"The value of attribute {dict_key} should have been updated."
            assert obj_value == new_dict_value, msg
