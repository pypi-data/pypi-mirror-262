from __future__ import annotations

import json
import math
from collections.abc import Sequence
from pathlib import Path
from unittest.mock import mock_open

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings

from perigene.perigene_types import Region
from tests.helpers.strategies import path_strategy, str_region_pattern_strategy

pytestmark = pytest.mark.skip(
    "Config is not used anymore. Keeping tests that can be reused for info.py"
)


# Define a strategy to generate dictionaries with currently accepted parameters
json_config_strategy = st.fixed_dictionaries(
    {
        "model": st.sampled_from(
            [
                "reg-lasso",
                "reg-ridge",
                "reg-elasticnet",
                "reg-gb",
            ]
        ),
        "path_features": st.builds(str, path_strategy(max_size=3)),
        "path_scores": st.builds(str, path_strategy(max_size=3)),
        "max_var_diff": st.floats(min_value=0.0, max_value=3.0),
        "excluded_regions": st.lists(str_region_pattern_strategy(), max_size=3),
        "model_params": st.dictionaries(
            keys=st.from_type(str), values=st.from_type(str), max_size=2
        ),
        "hpt_storage": st.builds(str, path_strategy(max_size=2)),
    }
)


@pytest.mark.parametrize(
    "config,context",
    [
        (
            dict(non_existing_parameter=True),
            pytest.raises(
                TypeError, match=r"unexpected keyword argument 'non_existing_parameter'"
            ),
        ),
    ],
)
def test_config_read_invalid_parameters(monkeypatch, config, context):
    """
    Test that error is raised is case of non existing/invalid parameters.
    """

    # Arrange
    def mock_json_load(*_args, **_kwargs) -> dict:
        return dict(model="", path_features="", path_scores="", **config)

    monkeypatch.setattr("builtins.open", mock_open())
    monkeypatch.setattr("json.load", mock_json_load)
    # Act
    # Assert
    with context:
        config = tc.Config.read("/dummy/path")  # type: ignore # noqa


@pytest.mark.parametrize(
    "path",
    [
        "./a/b/c",
        "../a/b/c",
        "./a/../b/c",
    ],
)
def test_config_read_convert_relative_path(monkeypatch, path):
    """
    Test that relative paths are converted to absolute path taking the config file's
    folder as a reference.
    """

    # Arrange
    def mock_json_load(*_args, **_kwargs) -> dict:
        return dict(
            model="",
            path_features=path,
            path_scores=path,
        )

    monkeypatch.setattr("builtins.open", mock_open())
    monkeypatch.setattr("json.load", mock_json_load)

    config_path = Path("/dummy/path/config.json")
    expected_path = (config_path.parent / path).resolve()
    # Act
    config = tc.Config.read(config_path)  # type: ignore # noqa
    # Assert
    assert config.path_features.is_absolute()
    assert config.path_features == expected_path
    assert config.path_scores.is_absolute()
    assert config.path_scores == expected_path


def test_Config_constructor():
    model = "test_model"
    path_features = "test_path_features"
    path_scores = "test_path_scores"

    config = tc.Config(model, path_features, path_scores)  # type: ignore # noqa

    assert config.model == model
    assert config.path_features == path_features
    assert config.path_scores == path_scores


@given(config_dict=st.one_of(json_config_strategy))
@settings(max_examples=20)
def test_load_json(config_dict: dict) -> None:
    with pytest.MonkeyPatch().context() as m:
        # Monkeypatch the following functions:
        # 1) A mocked open function that returns a mocked file object
        mock_open_fct = mock_open()
        m.setattr("builtins.open", mock_open_fct)

        # 2) A mocked json.load function that returns the input dictionary
        def mock_json_load(*_args, **_kwargs) -> dict:
            return config_dict

        m.setattr("json.load", mock_json_load)

        # Load the JSON file using the _load_json function
        json_dict = tc._load_json("config.json")  # type: ignore # noqa

        # Check that the dictionary contains the expected keys
        assert set(json_dict.keys()) == config_dict.keys()

        # Tests that the open function was called with the correct arguments
        mock_open_fct.assert_called_with("config.json")

        # Check that the values in the dictionary are serializable
        try:
            json.dumps(json_dict)
        except TypeError:
            pytest.fail("Values in json dict should be serializable")


@given(
    value=st.one_of(
        path_strategy(),
        st.builds(Region.from_str, str_region_pattern_strategy()),
        st.integers(),
        st.floats(),
        st.none(),
        st.lists(st.text(), max_size=5),
    )
)
@settings(max_examples=30, deadline=None)
def test_convert_config_parameter_to_serializable(value):
    result = tc._convert_config_parameter_to_serializable(value)  # type: ignore # noqa
    assert isinstance(result, (float, int, str, list, dict, type(None)))
    if isinstance(value, (Path, Region)):
        assert result == str(value)
    elif isinstance(value, Sequence) and not isinstance(value, str):
        assert result == [str(r) for r in value]
    elif isinstance(value, float) and math.isnan(value):
        assert math.isnan(result)
    else:
        assert result == value
