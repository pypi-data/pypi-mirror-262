from __future__ import annotations

import copy
import logging
from abc import ABC
from collections.abc import Collection, Iterator
from pathlib import Path
from typing import Any, Final, TypeVar

import filelock
import numpy as np
import pandas as pd
import pyarrow.parquet

from .constants import PD_FLOAT_FORMAT, ColFeatures, ColInternal, ColScores
from .exceptions import MissingColumnException
from .index import IndexDict
from .perigene_types import Region
from .utils import batched

logger = logging.getLogger(__name__)

# Recognized file extensions
EXT_PARQUET = ".parquet"
EXT_TSV = ".tsv", ".txt", ".tab", ".tsv.gz", ".txt.gz", ".tab.gz", ".bed"
EXT_CSV = ".csv", ".csv.gz"
EXT_GMT = ".gmt"

# Extract names used multiple times to reduce lengthy syntax below

DEFAULT_DTYPES: Final[dict[str, Any]] = {
    ColInternal.GENE: pd.StringDtype(),
    ColInternal.SYMBOL: pd.StringDtype(),
    ColInternal.CHR: pd.StringDtype(),
    ColInternal.START: np.uint32,
    ColInternal.END: np.uint32,
    ColInternal.LEAD_SNP_ID: pd.StringDtype(),
    ColInternal.LEAD_SNP_POS: np.uint32,
    ColInternal.WINDOW: np.uint32,
    ColFeatures.GENE: pd.StringDtype(),
    ColScores.CHR: pd.StringDtype(),
    ColScores.START: np.uint32,
    ColScores.END: np.uint32,
    ColScores.GENE: pd.StringDtype(),
    ColScores.SCORE: np.float32,
}


# TODO: switch to py 3.11 generic types
T = TypeVar("T", bound="DataTable")


class DataTable(ABC):
    _required_columns: list[str]
    """List of columns required in the data file."""
    _columns_mapping: dict[str, str] = dict()
    """Mapping of column names between the data file and the internal representation.
    """
    data: pd.DataFrame
    _default_pd_kws: dict[str, Any] = dict()

    def __init__(self, data: pd.DataFrame, **kwargs) -> None:
        self.data = data
        self._validate()

    @classmethod
    def from_path(
        cls: type[T],
        path: str | Path | None,
        *,
        allow_missing: bool = False,
        pd_kws: dict[str, Any] | None = None,
        **kwargs,
    ) -> T:
        logger.debug("Reading data from file: %s", path)

        if (path is None) or (not Path(path).exists()):
            if allow_missing:
                logger.info("File not found: %s", path)
                logger.info("Creating empty data file")
                return cls.create_empty()
            raise FileNotFoundError(f"File does not exist: {path}")

        try:
            data = cls._read_table(
                Path(path),
                **cls._merge_kwargs(
                    dict(
                        dtype=DEFAULT_DTYPES,
                    ),
                    cls._default_pd_kws,
                    pd_kws,
                ),
            )
            data = cls._format_data(data)
        except Exception as e:
            raise ValueError(
                f"Could not create {cls.__name__} from file: {path}"
            ) from e
        return cls(data, **kwargs)

    @staticmethod
    def _read_table(path: Path, **kwargs) -> pd.DataFrame:
        from pandas.api.types import is_string_dtype

        fname = path.name.lower()

        if fname.endswith(EXT_PARQUET):
            # Remove dtype from kwargs as it is not supported by read_parquet
            kwargs.pop("dtype", None)
            df = pd.read_parquet(path, **kwargs)
            assert is_string_dtype(df.index)
            return df
        if any(fname.endswith(e) for e in EXT_CSV):
            read = pd.read_csv
        elif any(fname.endswith(e) for e in EXT_TSV):
            read = pd.read_table
        else:
            logger.warning("Unrecognized file extension: %s", path)
            logger.warning("Trying to read as tsv")
            read = pd.read_table

        try:
            df = read(path, **kwargs)
        except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise ValueError(f"Could not read data from file: {path}") from e
        return df

    @staticmethod
    def _merge_kwargs(
        default: dict[str, Any], *received: dict[str, Any] | None
    ) -> dict:
        """Merges dictionaries of keyword arguments, giving priority to the
        received ones over the default ones.
        """
        kwargs = default.copy()
        for d in received:
            if d is not None:
                kwargs.update(d)
        return kwargs

    @classmethod
    def _format_data(cls, data: pd.DataFrame) -> pd.DataFrame:
        logger.debug("Renaming columns")
        data = data.rename(columns=cls._columns_mapping)

        return cls._drop_extra_cols(data)

    @classmethod
    def _drop_extra_cols(cls, data):
        logger.debug("Limiting data to required columns only.")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Columns present: %s", ", ".join(data.columns))
        return data[cls._required_columns]

    def _validate(self) -> None:
        self._check_columns_exist(self._required_columns)

    def _check_columns_exist(self, requested_columns: list[str]):
        missing_cols = set(requested_columns) - set(self.data.columns)
        if len(missing_cols) > 0:
            raise MissingColumnException(
                f"{self.__class__.__name__} file is missing required "
                f"columns: {','.join(missing_cols)}. "
                f"Columns present: {','.join(self.data.columns)}"
            )

    @classmethod
    def create_empty(
        cls: type[T],
    ) -> T:
        return cls(pd.DataFrame(columns=cls._required_columns))

    def __len__(self) -> int:
        return len(self.data)

    def copy(self: T) -> T:
        return copy.deepcopy(self)


class GenomicData(DataTable):
    """
    Data with genomic coordinates.
    """

    def _validate(self) -> None:
        super()._validate()

        if not all(
            c in self.data.columns
            for c in [ColInternal.CHR, ColInternal.START, ColInternal.END]
        ):
            raise MissingColumnException(
                f"GenomicData objects are expected to have columns "
                f"{ColInternal.CHR}, {ColInternal.START} and {ColInternal.END}. "
                "Check the class implementing GenomicData."
            )

        if (self.data[ColInternal.END] < self.data[ColInternal.START]).any():
            raise ValueError(
                f"Invalid data: {ColInternal.END} < {ColInternal.START} for some rows"
            )

        if not self.data[ColInternal.CHR].str.match(r"^([12]?\d)|[XY]$").all():
            raise ValueError(
                f"Invalid data: {ColInternal.CHR} contains invalid chromosome names. "
                "Expected: 1-22, X or Y"
            )

    def get_region(self, region: Region) -> pd.DataFrame:
        """Subset data to get genes overlapping or contained by the given region.

        Args:
            region (Region): region object defining the region to query

        Returns:
            pd.DataFrame: The subset of the data overlapping the region.
        """
        start, end = region.start, region.end
        if (start is None) or (start < 0):
            raise ValueError(f"Invalid start position: {start}")
        if (end is None) or (end < start):
            raise ValueError(f"Invalid end position: {end}")

        return self.data.loc[
            (self.data[ColInternal.CHR] == region.chrom)
            & (self.data[ColInternal.START] <= end)
            & (self.data[ColInternal.END] >= start)
        ]

    def drop_regions(self, *regions: Region) -> pd.DataFrame:
        """Remove genes overlapping or contained by the given regions.

        Args:
            *regions (Region): region objects defining the regions to remove

        Returns:
            pd.DataFrame: The subset of the data not overlapping the regions.
        """

        # Make a mask for each region
        masks = [
            (self.data[ColInternal.CHR] == region.chrom)
            & (self.data[ColInternal.START] <= region.end)
            & (self.data[ColInternal.END] >= region.start)
            for region in regions
        ]
        # combine the masks to a series indicating if a gene is in either of
        # these regions
        mask = pd.concat(masks, axis=1).any(axis=1)
        # return the genes not in the regions
        return self.data[~mask]


class GeneAnnotations(GenomicData):
    _required_columns: list[str] = [
        ColInternal.GENE,
        ColInternal.CHR,
        ColInternal.START,
        ColInternal.END,
        ColInternal.SYMBOL,
    ]

    def annotate_other(
        self,
        other: DataTable,
        fields: list[str] | None = None,
        check_redundant: str = "raise",  # "raise", "keep_self", "keep_other"
        merge_on: str = ColInternal.GENE,
    ) -> DataTable:
        """
        Annotate the genes in other data file and return a new data file with the
        annotations.

        Args:
            other (GeneData): data file to annotate
            fields (list[str], optional): columns to keep in the other data file.
                Defaults to None (keep all columns).
            check_redundant (str, optional): how to handle columns that already exist
                in the other data file. Defaults to "raise". Can be "raise", "keep_self"
                or "keep_other".
            merge_on (str, optional): column to use for merging. Defaults to "GENE".
        """

        # Check that the merge_on column is present in both data files
        self._check_columns_exist([merge_on])
        other._check_columns_exist([merge_on])

        # Make copies to avoid mutating the original data
        other = other.copy()

        # Check if the other data file already contains some of the annotations columns
        annotations, df_other = self._get_non_redundant_dfs(
            other.data, check_redundant, cols_ignore=[merge_on]
        )

        other.data = df_other.merge(
            annotations,
            how="left",
            on=merge_on,
        )

        other._validate()
        return other

    def get_annotations(self, include: list[str] | None) -> pd.DataFrame:
        """
        Returns the gene annotations. If `include` is not None, only the requested
        columns are returned.

        Args:
            include (list[str], optional): columns to include. Defaults to None.

        Returns:
            pd.DataFrame: dataframe with the gene annotations.
        """

        if include is not None:
            self._check_columns_exist(include)
            return self.data[include]

        return self.data

    def _get_non_redundant_dfs(
        self,
        df_other: pd.DataFrame,
        how: str = "keep_other",  # "raise", "keep_self", "keep_other"
        cols_ignore: Collection[str] | None = None,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Compare the columns in the other data file with the annotations in this data
        file and return a tuple with the annotations that are not already present in
        the other data file. By default, the columns from the other data file are kept.
        """

        cols_ignore = set(cols_ignore) if cols_ignore is not None else set()
        cols_redundant = set(df_other.columns).intersection(self.data.columns)
        cols_pb = cols_redundant - cols_ignore

        if not cols_pb:
            return self.data, df_other

        logger.debug("Some annotations are already present in the other data file")
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Existing fields: %s", ", ".join(cols_pb))

        if how == "raise":
            raise ValueError(f"Dataframe already contains columns {', '.join(cols_pb)}")
        elif how == "keep_self":
            return self.data, df_other.drop(columns=cols_pb)
        elif how == "keep_other":
            return self.data.drop(columns=cols_pb), df_other
        else:
            raise ValueError(f"Unknown value for `how`: {how}")


class GWASLoci(GenomicData):
    _required_columns: list[str] = [
        ColInternal.CHR,
        ColInternal.START,
        ColInternal.END,
        ColInternal.LEAD_SNP_ID,
        ColInternal.LEAD_SNP_POS,
    ]

    @classmethod
    def _format_data(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        If the START and END columns are not present but a WINDOW column is, use the
        lead variant's position +/- the WINDOW value to define the locus start and end.

        Convert the START and END columns to int32 and drop the WINDOW column.
        """

        if (ColInternal.START not in df.columns) or (
            ColInternal.START not in df.columns
        ):
            if ColInternal.WINDOW not in df.columns:
                raise MissingColumnException(
                    "GWAS loci file is missing "
                    f" '{ColInternal.START}' or '{ColInternal.END}' columns "
                    f"and column '{ColInternal.WINDOW}' is also absent."
                    "Provide either the start and end positions of the loci or the "
                    "size of the window around the lead variant."
                    f"Columns present: {', '.join(df.columns)}"
                )
            df[ColInternal.START] = (
                df[ColInternal.LEAD_SNP_POS] - df[ColInternal.WINDOW]
            )
            df[ColInternal.END] = df[ColInternal.LEAD_SNP_POS] + df[ColInternal.WINDOW]
            df = df.drop(columns=[ColInternal.WINDOW])

        df[ColInternal.START] = df[ColInternal.START].astype(np.uint32)
        df[ColInternal.END] = df[ColInternal.END].astype(np.uint32)
        return df[cls._required_columns]


class GWASLociLD(DataTable):
    _required_columns: list[str] = ["SNP_A", "SNP_B", "R2"]
    _default_pd_kws: dict[str, Any] = dict(
        dtype=dict(
            SNP_A=pd.StringDtype(),
            SNP_B=pd.StringDtype(),
            R2=np.float32,
        ),
        sep=r"\s+",
    )

    def get_ld_others(self, variant_id: str) -> pd.DataFrame:
        """
        Returns a series with the LD between the lead variant and all other variants at
        a locus.
        """
        return self.data.query(f"SNP_A == '{variant_id}'").set_index("SNP_B").R2


class ValidationGenes(DataTable):
    _required_columns: list[str] = [
        ColInternal.GENE,
        ColInternal.SYMBOL,
        ColInternal.GENE_SET_SOURCE,
    ]

    def summary(self) -> str:
        n_genes = len(self)
        n_genes_unique = len(self.data[ColInternal.GENE].unique())

        summary = f"Number of validation genes: {n_genes} (unique: {n_genes_unique}"

        if ColInternal.CHR in self.data.columns:
            summary += f"; with annotations: {self.data[ColInternal.CHR].count()}"
        summary += ")"
        return summary


class GeneScores(GenomicData):
    _columns_mapping: dict[str, str] = {
        ColScores.CHR: ColInternal.CHR,
        ColScores.START: ColInternal.START,
        ColScores.END: ColInternal.END,
        ColScores.GENE: ColInternal.GENE,
        ColScores.SCORE: ColInternal.SCORE,
    }
    _required_columns: list[str] = [
        ColInternal.CHR,
        ColInternal.START,
        ColInternal.END,
        ColInternal.GENE,
        ColInternal.SCORE,
    ]

    def get_scores(self, genes: list[str] | None = None) -> pd.Series:
        """
        Returns a series with the scores for the given genes.
        """
        y = self.data.set_index(ColInternal.GENE)[ColInternal.SCORE]
        if genes is not None:
            y = y.loc[genes]
        return y

    def get_genes_loc(self, genes: list[str] | None = None) -> pd.DataFrame:
        """
        Returns a dataframe with the genomic coordinates of the given genes.
        DataFrame is indexed by gene.
        """
        df = self.data.set_index(ColInternal.GENE)[
            [ColInternal.CHR, ColInternal.START, ColInternal.END]
        ]
        if genes is not None:
            df = df.loc[genes]
        return df


# Treating predictions as a type of scores with an additional column
# and methods to update and save the predictions
class PERiGenePredictions(GeneScores):
    _required_columns: list[str] = [
        ColInternal.GENE,
        ColInternal.CHR,
        ColInternal.START,
        ColInternal.END,
        ColInternal.SCORE,
        ColInternal.PRED,
    ]

    def get_predictions(
        self, genes: list[str] | None = None, drop_na: bool = True
    ) -> pd.Series:
        """
        Returns a series with the predictions for the given genes.
        """
        y = self.data.set_index(ColInternal.GENE)[ColInternal.PRED]
        if genes is not None:
            y = y.loc[genes]
        if drop_na:
            y = y.dropna()
        return y

    def update(self, predictions: pd.Series) -> None:
        data = self.data.set_index(ColInternal.GENE)
        data.loc[predictions.index, ColInternal.PRED] = predictions
        self.data = data.reset_index()

    def save(self, path: Path, **kwargs) -> None:
        """
        Save the data to a file.
        """

        fname_lock = f"{path}.lock"
        kwargs_ = dict(
            path_or_buf=path,
            sep="\t",
            index=False,
            na_rep="NA",
            float_format=PD_FLOAT_FORMAT,
        )
        kwargs_.update(kwargs)
        del kwargs

        with filelock.SoftFileLock(fname_lock):
            if not path.is_file():
                logger.debug("Creating new scores file: %s", path)
                self.data.to_csv(**kwargs_)
                return

            logger.info("Updating scores file: %s", path)

            # Quick check that the genes are the same
            existing_scores = PERiGenePredictions.from_path(path)
            genes_in_existing = set(existing_scores.data[ColInternal.GENE])
            genes_in_memory = set(self.data[ColInternal.GENE])

            if genes_in_memory != genes_in_existing:
                str_examples = "e.g. "
                if genes_in_memory_only := genes_in_memory - genes_in_existing:
                    ex_list = ", ".join(list(genes_in_memory_only)[:3])
                    str_examples += f"only in memory: {ex_list}. "
                if genes_in_file_only := genes_in_existing - genes_in_memory:
                    ex_list = ", ".join(list(genes_in_file_only)[:3])
                    str_examples += f"in current file only: {ex_list}. "

                raise ValueError(
                    "Cannot update scores file as it seems to contain different genes "
                    "than the ones in memory. Make sure the scores were computed using "
                    "the same gene annotations. " + str_examples
                )

            # Update non-null scores
            existing_scores.update(self.get_predictions())

            existing_scores.data.to_csv(**kwargs_)


class PERiGeneWeights(DataTable):
    _required_columns: list[str] = [ColInternal.FEATURE]


class Features(DataTable):
    _required_columns: list[str] = []

    @classmethod
    def _drop_extra_cols(cls, data: pd.DataFrame) -> pd.DataFrame:
        # Remove filtering of columns as can contain arbitrary number of columns
        return data


class RawFeatures(Features):
    _required_columns: list[str] = [ColInternal.GENE]
    _columns_mapping: dict[str, str] = {ColFeatures.GENE: ColInternal.GENE}

    def __init__(self, data: pd.DataFrame, col_gene: str = ColInternal.GENE) -> None:
        self.data = data.rename(columns={col_gene: ColInternal.GENE})
        self._validate()


class GMTFeatures(Features):
    _required_columns: list[str] = []

    @staticmethod
    def _iter_gmt(filename: Path) -> Iterator[tuple[str, list[str]]]:
        with open(filename) as f_in:
            for line in f_in:
                gene_set_name, _, *genes = line.strip().split()
                yield gene_set_name, genes

    @staticmethod
    def _read_gmt_matrix(path: Path):
        """
        Creates a matrix of binary values (genes x gene_sets) from a gmt file.
        """
        return (
            pd.concat(
                [
                    pd.Series(1, index=genes, name=gene_set_name, dtype=pd.UInt8Dtype())
                    for gene_set_name, genes in GMTFeatures._iter_gmt(path)
                ],
                axis=1,
            )
            .fillna(0)
            .reset_index(names=ColInternal.GENE)
        )

    @classmethod
    def _read_table(cls, path: Path, **kwargs) -> pd.DataFrame:
        return cls._read_gmt_matrix(path)


class ParquetFeatures(Features):
    _required_columns: list[str] = []

    @classmethod
    def _read_table(cls, path: Path, **kwargs) -> pd.DataFrame:
        return pd.read_parquet(path, **kwargs)

    @classmethod
    def batch_iter(cls, path: Path, chunksize: int = 5000) -> Iterator[ParquetFeatures]:
        """
        Iterates over batches of features (columns) from a parquet file.
        """
        columns = pyarrow.parquet.read_schema(path, memory_map=True).names
        for cols in batched(columns, chunksize):
            yield cls.from_path_subset(path, list(cols))

    @staticmethod
    def from_path_subset(path: Path, columns: list[str]) -> ParquetFeatures:
        """
        Load a subset of the features from a parquet file.
        """
        all_columns = pyarrow.parquet.read_schema(path, memory_map=True).names

        missing_cols = set(columns) - set(all_columns)
        if len(missing_cols) > 0:
            max_shown = 5
            shown_cols = list(missing_cols)[:max_shown]
            n_missing = len(missing_cols)
            str_cols = ", ".join(shown_cols)
            str_cols += "..." if n_missing > max_shown else ""
            raise MissingColumnException(
                f"{n_missing} columns not found in {path}: {str_cols}."
            )

        return ParquetFeatures(ParquetFeatures._read_table(path, columns=columns))

    @staticmethod
    def from_path_match_index(path: Path, index: IndexDict):
        """Reads the all features referenced in either model contained in the passed
        index dict"""
        columns = pd.concat([k.features for k in index.indexes.values()]).unique()

        # TODO: In case features in index are not in parquet file, raise warning
        # need to raise exception indicating some of the missing columns (not all)
        return ParquetFeatures.from_path_subset(path, columns)
