"""Data class with base functions to manipulate gene scores + generate,
index and query training and testing sets.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, Sequence
from pathlib import Path

import pandas as pd

from .constants import ColInternal
from .data_tables import GeneScores, ParquetFeatures
from .exceptions import MissingTargetDataException
from .index import DataSubsetCategory, IndexDict
from .perigene_types import FilePrefix, ModelData

logger = logging.getLogger(__name__)
IS_DEBUG_ON = logger.isEnabledFor(logging.DEBUG)

# alias for DataSubsetCategory to reduce verbosity
CAT_TRAIN = DataSubsetCategory.TRAIN
CAT_TEST = DataSubsetCategory.TEST


class Data:
    """Stores and indexes features and genes scores. Provides functions to
    query subsets of the data.
    """

    _index: IndexDict
    _ordered_genes: pd.Index = None
    _X: pd.DataFrame
    _y: pd.Series
    _y_pred: pd.Series = None
    _genes_loc: pd.DataFrame

    # Using property setters to enforce consistent gene order when data is loaded
    @property
    def X(self) -> pd.DataFrame:
        return self._X

    @X.setter
    def X(self, X: pd.DataFrame) -> None:
        self._X = X.rename_axis(index=ColInternal.GENE)

    @property
    def y(self) -> pd.Series:
        return self._y

    @y.setter
    def y(self, y: pd.Series) -> None:
        self._y = y.rename_axis(index=ColInternal.GENE)

    @property
    def genes_loc(self) -> pd.DataFrame:
        return self._genes_loc

    @genes_loc.setter
    def genes_loc(self, genes_loc: pd.DataFrame) -> None:
        self._genes_loc = genes_loc.rename_axis(index=ColInternal.GENE)

    @property
    def index(self) -> IndexDict:
        return self._index

    @index.setter
    def index(self, index: IndexDict):
        self._assert_data_loaded()
        logger.debug("Checking that index keys are all in the feature matrix...")
        for name, model_index in index.items():
            try:
                model_index.query_features(self.X, CAT_TRAIN)
                model_index.query_features(self.X, CAT_TEST)
            except MissingTargetDataException:
                logger.info(
                    "Index contains no test data for model %s. "
                    "This model will be trained but not used for predictions. ",
                    name,
                )
            except Exception as e:
                logger.error(
                    "Error when trying to query genes or features for model %s. ",
                    name,
                )
                raise e
        self._index = index

    @property
    def y_pred(self):
        return self._y_pred

    @y_pred.setter
    def y_pred(self, y_pred):
        self._y_pred = y_pred

    def __init__(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        genes_loc: pd.DataFrame,
        index: IndexDict | None = None,
    ) -> None:
        self.X = X
        self.y = y
        self.genes_loc = genes_loc
        if index is not None:
            self.index = index

    @staticmethod
    def load(
        *,
        prefix: FilePrefix,
        path_features: Path,
        path_scores: Path,
        subset_models: Sequence[str] | None = None,
    ) -> Data:
        index = IndexDict.load(prefix, subset_models=subset_models)
        scores = GeneScores.from_path(path_scores)
        features = ParquetFeatures.from_path_match_index(path_features, index=index)

        return Data(
            features.data, scores.get_scores(), scores.get_genes_loc(), index=index
        )

    def get(
        self,
        key_model: str,
        subset: DataSubsetCategory,
    ) -> tuple[pd.DataFrame, pd.Series]:
        """Valid options for `kind` are DataSubsetCategory.TRAIN and
        DataSubsetCategory.TEST.
        """
        assert hasattr(self, "index"), "Need to index the data!"
        assert subset in (CAT_TRAIN, CAT_TEST)

        X = self.index.get_model_features(self.X, key_model, subset)
        y = self.y.loc[X.index]
        return X, y

    def __iter__(self) -> Iterator[tuple[str, ModelData]]:
        for key_model in self.index:
            data_model = {
                CAT_TRAIN: self.get(key_model, CAT_TRAIN),
            }

            try:
                data_model[CAT_TEST] = self.get(key_model, CAT_TEST)
            except MissingTargetDataException:
                logger.info("No test data for model %s. ", key_model)

            yield key_model, data_model

    def __len__(self):
        return len(self.index)

    def _assert_data_loaded(self):
        try:
            assert hasattr(self, "X")
            assert hasattr(self, "y")
            assert hasattr(self, "genes_loc")
        except AssertionError as e:
            logger.error(
                "Features, scores and gene locations need to be loaded "
                "before index can be set/made."
            )
            raise e

    def _assert_known_gene_ids(self, obj: pd.Series | pd.DataFrame) -> None:
        unknown_ids = set(obj.index) - set(self._ordered_genes)
        assert len(unknown_ids) == 0, (
            f"Received object contains {len(unknown_ids)} ids that were "
            f"absent from previously loaded data: {unknown_ids}"
        )

        missing_ids = set(self._ordered_genes) - set(obj.index)
        assert len(missing_ids) == 0, (
            f"Received object is missing {len(missing_ids)} gene ids that were "
            f"present in previously loaded data: {missing_ids}"
        )
