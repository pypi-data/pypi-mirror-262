from __future__ import annotations

import json
import logging
import os
from collections import OrderedDict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

import filelock

from perigene import models
from perigene.exceptions import MissingInfoParamException
from perigene.utils import natural_sort

from . import __version__
from .constants import FileSuffix
from .perigene_types import FilePrefix, ModelParametersDict, Region

InfoParameter = str | Path | float | Sequence[Region] | ModelParametersDict | None
T = TypeVar("T")

logger = logging.getLogger(__name__)


def filter_none_values(d: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in d.items() if v is not None}


def nested_update(d: dict[str, Any], u: dict[str, Any]) -> dict[str, Any]:
    for k, v in filter_none_values(u).items():
        if isinstance(v, Mapping):
            d[k] = nested_update(d.get(k, {}), v)  # type: ignore
        else:
            d[k] = v
    return d


def load_json(fname: str | Path) -> dict[str, Any]:
    try:
        with open(fname) as f_in:
            logger.debug(f"Loading JSON file {fname}.")
            json_dict = json.load(f_in)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not find info file at {fname}.") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse info file at {fname}.") from e
    return json_dict


def _get_abs_path(str_path: str | None, path_info_file_parent: Path) -> Path | None:
    if str_path is None:
        return None
    try:
        # Replace environment variables before resolving path
        path = Path(os.path.expandvars(str_path))
        if not path.is_absolute():
            path = (path_info_file_parent / path).resolve()
        return path
    except Exception as e:
        raise ValueError(f"Could not get {str_path}'s absolute path.") from e


def _check_param_exists(param: T | None, param_str: str) -> T:
    if param is None:
        raise MissingInfoParamException(f"{param_str} is not set.")
    return param


class _InfoKey:
    version = "version"
    paths = "paths"
    feature_selection = "feature_selection"
    masked_regions = "masked_regions"
    model_type = "model_type"
    model_params = "model_params"

    fs_min_variance = "min_variance"
    fs_max_var_diff = "max_var_diff"
    fs_max_pvalue = "max_pvalue"
    fs_max_cross_corr = "max_cross_corr"
    fs_max_features = "max_features"
    fs_excluded_features = "excluded_features"

    paths_features = "features"
    paths_scores = "scores"
    paths_optuna_storage = "optuna_storage"


@dataclass
class PathsInfo:
    _features: Path | None = None
    _scores: Path | None = None
    _optuna_storage: Path | None = None

    @property
    def features(self) -> Path:
        return _check_param_exists(self._features, "Path to feature file")

    @features.setter
    def features(self, features: Path):
        self._features = features

    @property
    def scores(self) -> Path:
        return _check_param_exists(self._scores, "Path to score file")

    @scores.setter
    def scores(self, scores: Path):
        self._scores = scores

    @property
    def optuna_storage(self) -> Path:
        return _check_param_exists(self._optuna_storage, "Path to Optuna storage")

    @optuna_storage.setter
    def optuna_storage(self, optuna_storage: Path):
        self._optuna_storage = optuna_storage

    @classmethod
    def from_dict(
        cls, paths_dict: dict[str, Any], path_conf_loc: Path | None = None
    ) -> PathsInfo:
        if path_conf_loc is None:
            path_conf_loc = Path.cwd()

        return cls(
            _features=_get_abs_path(
                paths_dict.get(_InfoKey.paths_features), path_conf_loc
            ),
            _scores=_get_abs_path(paths_dict.get(_InfoKey.paths_scores), path_conf_loc),
            _optuna_storage=_get_abs_path(
                paths_dict.get(_InfoKey.paths_optuna_storage), path_conf_loc
            ),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            name: str(path)
            for name, path in [
                (_InfoKey.paths_features, self._features),
                (_InfoKey.paths_scores, self._scores),
                (_InfoKey.paths_optuna_storage, self._optuna_storage),
            ]
            if path is not None
        }

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self.to_dict())


@dataclass
class FeatureSelectionInfo:
    _min_variance: float | None = None
    _max_var_diff: float | None = None
    _max_pvalue: float | None = None
    _max_cross_corr: float | None = None
    _max_features: int | None = None
    _excluded_features: list[str] = field(default_factory=list)

    @property
    def min_variance(self) -> float:
        return _check_param_exists(self._min_variance, "Min variance threshold")

    @min_variance.setter
    def min_variance(self, min_variance: float):
        self._min_variance = min_variance

    @property
    def max_var_diff(self) -> float:
        return _check_param_exists(self._max_var_diff, "Maximum variance difference")

    @max_var_diff.setter
    def max_var_diff(self, max_var_diff: float):
        self._max_var_diff = max_var_diff

    @property
    def max_pvalue(self) -> float:
        return _check_param_exists(self._max_pvalue, "pvalue thresold")

    @max_pvalue.setter
    def max_pvalue(self, max_pvalue: float):
        self._max_pvalue = max_pvalue

    @property
    def max_cross_corr(self) -> float:
        return _check_param_exists(
            self._max_cross_corr, "Maximum correlation between features"
        )

    @max_cross_corr.setter
    def max_cross_corr(self, max_cross_corr: float):
        self._max_cross_corr = max_cross_corr

    @property
    def max_features(self) -> int:
        return _check_param_exists(self._max_features, "Maximum number of features")

    @max_features.setter
    def max_features(self, max_features: int):
        self._max_features = max_features

    @property
    def excluded_features(self) -> list[str]:
        return self._excluded_features

    @excluded_features.setter
    def excluded_features(self, excluded_features: Sequence[str]):
        self._excluded_features = list(excluded_features)

    @classmethod
    def from_dict(cls, feature_selection_dict: dict[str, Any]) -> FeatureSelectionInfo:
        min_variance = feature_selection_dict.get(_InfoKey.fs_min_variance)
        max_var_diff = feature_selection_dict.get(_InfoKey.fs_max_var_diff)
        max_pvalue = feature_selection_dict.get(_InfoKey.fs_max_pvalue)
        max_cross_corr = feature_selection_dict.get(_InfoKey.fs_max_cross_corr)
        max_features = feature_selection_dict.get(_InfoKey.fs_max_features)
        excluded_features = feature_selection_dict.get(
            _InfoKey.fs_excluded_features, []
        )
        return cls(
            _min_variance=min_variance,
            _max_var_diff=max_var_diff,
            _max_pvalue=max_pvalue,
            _max_cross_corr=max_cross_corr,
            _max_features=max_features,
            _excluded_features=excluded_features,
        )

    def to_dict(self) -> dict[str, Any]:
        return filter_none_values(
            {
                _InfoKey.fs_min_variance: self._min_variance,
                _InfoKey.fs_max_var_diff: self._max_var_diff,
                _InfoKey.fs_max_pvalue: self._max_pvalue,
                _InfoKey.fs_max_cross_corr: self._max_cross_corr,
                _InfoKey.fs_max_features: self._max_features,
                _InfoKey.fs_excluded_features: self._excluded_features,
            }
        )

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return str(self.to_dict())


@dataclass
class PERiGeneInfo:
    _version: str = __version__
    _model: str | None = None
    _paths: PathsInfo = field(default_factory=lambda: PathsInfo())
    _feature_selection: FeatureSelectionInfo = field(
        default_factory=lambda: FeatureSelectionInfo()
    )
    _excluded_regions: list[Region] = field(default_factory=list)
    _model_params: dict[str, ModelParametersDict] = field(default_factory=dict)

    def __post_init__(self):
        # Sets collections to default values if they were initialized to None

        default_classes = [
            ("_model_params", dict),
            ("_excluded_regions", list),
            ("_feature_selection", FeatureSelectionInfo),
            ("_paths", PathsInfo),
        ]

        for attr, cls in default_classes:
            if getattr(self, attr) is None:
                logger.debug(f"{attr} is None, setting it to an empty {cls}.")
                setattr(self, attr, cls())

    @property
    def version(self) -> str:
        return _check_param_exists(self._version, "PERiGene version")

    @version.setter
    def version(self, version: str):
        self._version = version

    @property
    def model(self) -> type[models.Model]:
        """ """
        str_model = _check_param_exists(self._model, "Model")
        return getattr(models, str_model)

    @model.setter
    def model(self, model: str | type[models.Model]):
        """Keep model representation as a string to simplify JSON serialization."""
        if isinstance(model, type) and issubclass(model, models.Model):
            self._model = model.__name__
        elif isinstance(model, str):
            self._model = model
        else:
            raise TypeError("Model must be a string or a model class.")

    @property
    def excluded_regions(self) -> list[Region]:
        return _check_param_exists(self._excluded_regions, "Excluded regions")

    @excluded_regions.setter
    def excluded_regions(self, excluded_regions: Sequence[Region]):
        self._excluded_regions = list(excluded_regions)

    @property
    def model_params(self) -> dict[str, ModelParametersDict]:
        return _check_param_exists(self._model_params, "Model parameters")

    @property
    def paths(self) -> PathsInfo:
        return self._paths

    @paths.setter
    def paths(self, paths: PathsInfo):
        self._paths = paths

    @property
    def feature_selection(self) -> FeatureSelectionInfo:
        return self._feature_selection

    @feature_selection.setter
    def feature_selection(self, feature_selection: FeatureSelectionInfo):
        self._feature_selection = feature_selection

    @classmethod
    def read(cls, prefix: FilePrefix) -> PERiGeneInfo:
        info_json = load_json(prefix.join(FileSuffix.INFO))

        version = info_json.pop(_InfoKey.version, __version__)
        # Raise warning if the version of perigene used to create the info file
        # is different from the current version
        if version != __version__:
            logger.warning(
                f"Info file was created with perigene version {version}, "
                f"but the current version is {__version__}."
            )

        paths = PathsInfo.from_dict(info_json.pop(_InfoKey.paths, {}), prefix.parent)
        feature_selection = FeatureSelectionInfo.from_dict(
            info_json.pop(_InfoKey.feature_selection, {})
        )

        excluded_regions = [
            Region.from_str(r) for r in info_json.pop(_InfoKey.masked_regions, [])
        ]

        model_type = info_json.pop(_InfoKey.model_type, None)
        model_params = info_json.pop(_InfoKey.model_params, {})

        return PERiGeneInfo(
            _version=version,
            _model=model_type,
            _paths=paths,
            _feature_selection=feature_selection,
            _excluded_regions=excluded_regions,
            _model_params=model_params,
            **info_json,
        )

    def save(self, prefix: FilePrefix) -> None:
        """
        Update existing JSON file with the current info.
        """

        fname_json = prefix.join(FileSuffix.INFO)
        fname_lock = fname_json.parent / f"{fname_json.name}.lock"

        # Convert info attributes to serializable dictionary
        new_info_dict = self._to_dict()

        with filelock.SoftFileLock(fname_lock):
            # Re-load existing JSON file if it exists as some info may have been updated
            try:
                old_info_dict = load_json(fname_json)
            except (FileNotFoundError, ValueError):
                logger.debug(f"Creating new info file {fname_json}.")
                old_info_dict = {}

            # Update existing_info with the current info
            old_info_dict = nested_update(old_info_dict, new_info_dict)

            # Comvert dicts to sorted dict for better readability
            model_params_dict = old_info_dict[_InfoKey.model_params]
            old_info_dict[_InfoKey.model_params] = OrderedDict(
                **{
                    k: model_params_dict[k]
                    for k in natural_sort(model_params_dict.keys())
                }
            )

            # Save the updated info to the JSON file
            with open(fname_json, "w") as f_out:
                json.dump(old_info_dict, f_out, indent="\t")

    def set_attrs(
        self,
        version: str | None = None,
        model: str | type[models.Model] | None = None,
        path_features: Path | None = None,
        path_scores: Path | None = None,
        path_optuna_storage: Path | None = None,
        fs_min_variance: float | None = None,
        fs_max_var_diff: float | None = None,
        fs_max_pvalue: float | None = None,
        fs_max_cross_corr: float | None = None,
        fs_max_features: int | None = None,
        fs_excluded_features: Sequence[str] | None = None,
        excluded_regions: Sequence[Region] | None = None,
        model_params: dict[str, ModelParametersDict] | None = None,
    ) -> PERiGeneInfo:
        """
        Update the PERiGeneInfo object with the provided arguments. None values
        are ignored.
        """
        # Get all arguments passed to the function
        param_values = filter_none_values(locals())
        param_values.pop("self")

        # Iterate over all arguments and update the corresponding attribute if
        # the argument is not None
        for attr, val in param_values.items():
            # Warning: these prefixes have to be changed if the function parameters
            # or the PERiGeneInfo attributes are renamed
            if attr.startswith("path_"):
                attr = attr.removeprefix("path_")
                logger.debug(f"Setting paths.{attr} to {val}.")
                self.paths.__setattr__(attr, val)
            elif attr.startswith("fs_"):
                attr = attr.removeprefix("fs_")
                logger.debug(f"Setting feature_selection.{attr} to {val}.")
                self.feature_selection.__setattr__(attr, val)
            elif attr == "model":
                self.model = val
            else:
                logger.debug(f"Setting {attr} to {val}.")
                # Add underscore to set the private attribute directly
                self.__setattr__("_" + attr, val)

        return self

    def _to_dict(self) -> dict[str, Any]:
        """
        Convert the PERiGeneInfo object to a dictionary.

        Returns:
            A dictionary representation of the PERiGeneInfo object.
        """

        return {
            _InfoKey.version: self._version,
            _InfoKey.paths: self.paths.to_dict(),
            _InfoKey.feature_selection: self.feature_selection.to_dict(),
            _InfoKey.masked_regions: [str(region) for region in self.excluded_regions],
            _InfoKey.model_type: self._model,
            _InfoKey.model_params: self.model_params,
        }

    def __str__(self) -> str:
        return str(self._to_dict())

    def __repr__(self) -> str:
        return str(self._to_dict())
