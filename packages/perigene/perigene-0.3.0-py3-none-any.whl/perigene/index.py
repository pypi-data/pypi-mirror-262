"""Class to manipulate indexes of the genes and features used to train the different
models.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator, MutableMapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from perigene.exceptions import MissingTargetDataException

from .constants import ColInternal, FileSuffix
from .perigene_types import DataSubsetCategory, FilePrefix
from .utils import read_multi_model_df, save_multi_model_df

logger = logging.getLogger(__name__)


@dataclass
class ModelDataIndex:
    """
    Class holding the genes and features used to train a given model. It can optionally
    also hold the genes for which the model has to calculate scores.
    """

    train_genes: pd.Series
    test_genes: pd.Series | None
    features: pd.Series

    def read_features(
        self, path: Path, subset: DataSubsetCategory = DataSubsetCategory.TRAIN
    ) -> pd.DataFrame:
        """Load genes features for the corresponding model from a parquet file."""

        df = pd.read_parquet(path, columns=self.features)
        return self.query_features(df, subset)

    def query_features(
        self,
        df_features: pd.DataFrame,
        subset: DataSubsetCategory = DataSubsetCategory.TRAIN,
    ) -> pd.DataFrame:
        """Subset features for a given model from a provided dataframe."""

        if subset == DataSubsetCategory.ALL:
            return df_features.loc[:, self.features]

        return df_features.loc[self._get_genes(subset), self.features]

    def to_series(self) -> tuple[pd.Series, pd.Series]:
        train_genes = pd.Series(DataSubsetCategory.TRAIN, index=self.train_genes)
        test_genes = pd.Series(
            DataSubsetCategory.TEST,
            index=self.test_genes if self.test_genes is not None else [],
        )
        genes = pd.concat([train_genes, test_genes])

        features = pd.Series(True, index=self.features)
        return genes, features

    def _get_genes(self, subset: DataSubsetCategory) -> pd.Series:
        if subset == DataSubsetCategory.TRAIN:
            idx = self.train_genes
        elif subset == DataSubsetCategory.TEST and self.test_genes is not None:
            idx = self.test_genes
        elif subset == DataSubsetCategory.TEST:
            raise MissingTargetDataException(
                "No target genes are present for this model."
            )
        else:
            raise ValueError(f"Unknown gene set: {subset}. Expected 'train' or 'test'.")
        return idx


class IndexDict(MutableMapping[str, ModelDataIndex]):
    """Class holding a collection of ModelDataIndex objects for multiple models."""

    indexes: dict[str, ModelDataIndex]

    def __init__(self, **index: ModelDataIndex) -> None:
        self.indexes = index

    def __getitem__(self, key: str) -> ModelDataIndex:
        return self.indexes[key]

    def __setitem__(self, key: str, value: ModelDataIndex) -> None:
        self.indexes[key] = value

    def __delitem__(self, key: str) -> None:
        del self.indexes[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.indexes)

    def __len__(self) -> int:
        return len(self.indexes)

    @classmethod
    def load(
        cls, prefix: FilePrefix, subset_models: Sequence[str] | None = None
    ) -> IndexDict:
        """Load index from tab-separated files."""

        fname_features = prefix.join(FileSuffix.INDEX_FEATURES)
        fname_genes = prefix.join(FileSuffix.INDEX_GENES)

        logger.debug(f"Loading index from {fname_features} and {fname_genes}.")

        # Read and map string values to enums
        df_genes = (
            read_multi_model_df(
                fname_genes, index_col=ColInternal.GENE, dtype=pd.CategoricalDtype()
            )
            # Restrict columns to subset_models if provided
            .pipe(lambda df: df.loc[:, subset_models] if subset_models else df).apply(
                lambda col: col.map(DataSubsetCategory)
            )
        )

        df_features = read_multi_model_df(
            fname_features,
            index_col=ColInternal.FEATURE,
        ).pipe(lambda df: df.loc[:, subset_models] if subset_models else df)

        return cls.from_frames(df_genes, df_features)

    @classmethod
    def from_frames(
        cls, df_genes: pd.DataFrame, df_features: pd.DataFrame
    ) -> IndexDict:
        """Load index from tab-separated files."""

        dict_index = dict()

        if not df_genes.columns.equals(df_features.columns):
            logger.warning(
                f"Columns in {df_genes.columns} and {df_features.columns} do not match."
                "Using only models present in both dataframes."
            )
            columns = df_genes.columns.intersection(df_features.columns)
        else:
            columns = df_genes.columns

        if columns.empty:
            raise ValueError("No models found in index files.")

        for key_model in df_genes.columns:
            col_genes = df_genes[key_model]
            train_genes = col_genes.loc[
                col_genes == DataSubsetCategory.TRAIN
            ].index.to_series()
            test_genes = col_genes.loc[
                col_genes == DataSubsetCategory.TEST
            ].index.to_series()
            if test_genes.empty:
                test_genes = None

            col_features = df_features[key_model]
            features = col_features.loc[col_features].index.to_series()

            dict_index[key_model] = ModelDataIndex(train_genes, test_genes, features)
        return cls(**dict_index)

    def to_frames(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Converts index to two dataframes containing the genes and features of each
        model. These dataframes have one column per model and one row per gene or
        feature.

        The genes dataframe's values can be either "train", "test" or "masked".

        The features dataframe's values are either True or False.
        """
        list_genes: list[pd.Series] = []
        list_features: list[pd.Series] = []

        for key_model, index_model in self.indexes.items():
            genes, features = index_model.to_series()
            list_genes.append(genes.rename(key_model))
            list_features.append(features.rename(key_model))

        df_genes = pd.concat(list_genes, axis=1).fillna(DataSubsetCategory.MASKED)
        df_genes.index.name = ColInternal.GENE

        df_features = pd.concat(list_features, axis=1).fillna(False)
        df_features.index.name = ColInternal.FEATURE

        return df_genes, df_features

    def save(self, prefix: FilePrefix) -> None:
        """Save index to tab-separated files."""
        df_genes, df_features = self.to_frames()

        # Map enums to strings
        df_genes = df_genes.apply(lambda col: col.map(lambda x: x.name))

        save_multi_model_df(
            df_genes,
            prefix.join(FileSuffix.INDEX_GENES),
            na_fill=DataSubsetCategory.MASKED.name,
        )
        save_multi_model_df(
            df_features, prefix.join(FileSuffix.INDEX_FEATURES), na_fill=False
        )

    def get_features_names(self, subset_models: list[str] | None = None) -> pd.Series:
        keys = self.indexes.keys() if subset_models is None else subset_models
        return pd.concat([self.indexes[k].features for k in keys]).unique()

    def get_model_features(
        self, df_features: pd.DataFrame, key_model: str, subset: DataSubsetCategory
    ):
        """
        Returns a subset of the dataframe corresponding to features used by the model
        and the specified subset of genes (e.g. all, train or test genes).

        Args:
            df_features (pd.DataFrame): Dataframe containing the features to subset.
            model_name (str): Name of the model.
            subset (DataSubsetCategory): Subset to use.

        Returns:
            pd.DataFrame: Subset of the original dataframe.
        """
        return self.indexes[key_model].query_features(df_features, subset)
