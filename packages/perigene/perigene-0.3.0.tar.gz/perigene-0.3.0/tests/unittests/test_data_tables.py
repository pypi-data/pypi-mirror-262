from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra import pandas as pdst

import perigene.data_tables as pg_tables
from perigene.constants import ColInternal as Col
from perigene.exceptions import MissingColumnException

from ..helpers import strategies as stg


def mock_read_csv(df: pd.DataFrame, **_):
    return df


########################################################################################
# ABSTRACT BASE CLASS


class ConcreteDataTable(pg_tables.DataTable):
    _required_columns = ["column1", "column2"]


concrete_data_table_strategies = stg.perigene_table_data_strategy(
    std_columns=[],
    extra_columns=[
        pdst.column("column1", dtype=int),
        pdst.column("column2", dtype=int),
    ],
    min_size=0,
    max_size=50,
)


@given(data=concrete_data_table_strategies)
@settings(max_examples=5)
def test_len(data: pd.DataFrame):
    table = ConcreteDataTable(data)
    assert len(table) == len(data)


def test_missing_column_exception():
    data = pd.DataFrame({"column1": [1, 2, 3]})
    with pytest.raises(MissingColumnException):
        ConcreteDataTable(data)


@given(data=concrete_data_table_strategies)
@settings(max_examples=5)
def test_copy(data: pd.DataFrame):
    table1 = ConcreteDataTable(data)
    table2 = table1.copy()
    assert table1 is not table2
    assert table1.data.equals(table2.data)


def test_from_path(monkeypatch):
    # Arange
    path = "file.tsv"
    data_mock = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})

    # Mock function to replace Path.exists (to avoid FileNotFoundError)
    def mock_exists(*args):
        return True

    monkeypatch.setattr(Path, "exists", mock_exists)

    # Mock function to replace pd.read_table
    def mock_read_table(*args, **kwargs):
        return data_mock

    monkeypatch.setattr(pd, "read_table", mock_read_table)

    # Act
    table = ConcreteDataTable.from_path(path)

    # Assert
    assert table.data.equals(data_mock)


def test_from_path_file_not_found():
    with pytest.raises(FileNotFoundError):
        ConcreteDataTable.from_path("non_existent_file.csv")


def test_from_path_pandas_read_table_error(monkeypatch):
    # Mock function to replace Path.exists
    def mock_exists(*args):
        return True

    monkeypatch.setattr(Path, "exists", mock_exists)

    # Mock function to replace pd.read_table
    def mock_read_table(*args, **kwargs):
        raise pd.errors.ParserError("Mocked error")

    with pytest.raises(ValueError):
        monkeypatch.setattr(pd, "read_table", mock_read_table)
        ConcreteDataTable.from_path("any_path")


def test_from_path_allow_missing():
    table = ConcreteDataTable.from_path(None, allow_missing=True)
    assert table.data is not None
    assert table.data.empty
    assert set(table.data.columns) == set(ConcreteDataTable._required_columns)


########################################################################################
# TEST CONCRETE CLASSES


COLS_ANNOTS = [
    Col.GENE,
    Col.CHR,
    Col.START,
    Col.END,
    Col.SYMBOL,
]
COLS_LOCI = [
    Col.CHR,
    Col.START,
    Col.END,
    Col.LEAD_SNP_ID,
    Col.LEAD_SNP_POS,
]
COLS_LOCI_LD = ["SNP_A", "SNP_B", "R2"]
COLS_VALIDATION_GENES = [
    Col.GENE,
    Col.SYMBOL,
    Col.GENE_SET_SOURCE,
]
COLS_PRED = [
    Col.GENE,
    Col.CHR,
    Col.START,
    Col.END,
    Col.SCORE,
    Col.PRED,
]


@given(data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS))
@settings(max_examples=1)
def test_GeneAnnotations_init(data: pd.DataFrame):
    gene_annotations = pg_tables.GeneAnnotations(data)
    assert isinstance(gene_annotations, pg_tables.GeneAnnotations)
    assert isinstance(gene_annotations.data, pd.DataFrame)
    assert gene_annotations.data.equals(data)
    assert len(gene_annotations) == len(data)


@given(data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=0))
@settings(max_examples=1)
def test_GeneAnnotations_init_fails_when_missing_columns(data: pd.DataFrame):
    for column in COLS_ANNOTS:
        with pytest.raises(MissingColumnException):
            pg_tables.GeneAnnotations(data.drop(columns=[column]))


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=0),
)
@settings(max_examples=1)
def test_GeneAnnotations_get_non_redundant_dfs_raises(
    data: pd.DataFrame,
) -> None:
    # Arange
    cols_other: list[str] = ["column1"] + COLS_ANNOTS
    to_ignore: list[str] = list()
    redundant_cols = set(COLS_ANNOTS) & set(cols_other) - set(to_ignore)
    gene_annotations = pg_tables.GeneAnnotations(data)
    data_other = pd.DataFrame(columns=cols_other)
    how = "raise"

    # Act
    with pytest.raises(ValueError) as excinfo:
        gene_annotations._get_non_redundant_dfs(data_other, how=how)

    # Assert
    # Check that a minimally informative error message is raised
    # Should show the redundant columns (order doesn't matter)
    assert all(col in str(excinfo.value) for col in redundant_cols)


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=5),
)
@settings(max_examples=3)
def test_GeneAnnotations_get_non_redundant_dfs_keeps_other(
    data: pd.DataFrame,
) -> None:
    # Arange
    cols_other: list[str] = ["column1"] + COLS_ANNOTS
    to_ignore: list[str] = list()
    redundant_cols = set(COLS_ANNOTS) & set(cols_other) - set(to_ignore)
    gene_annotations = pg_tables.GeneAnnotations(data)
    data_other = pd.DataFrame(columns=cols_other)
    how = "keep_other"

    # Act
    new_data, new_data_other = gene_annotations._get_non_redundant_dfs(
        data_other, how=how, cols_ignore=to_ignore
    )

    # Assert
    assert new_data_other.equals(data_other)
    assert all(col not in new_data.columns for col in redundant_cols)
    assert all(col in new_data_other.columns for col in to_ignore)
    assert all(col in new_data.columns for col in to_ignore)


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=5),
)
@settings(max_examples=3)
def test_GeneAnnotations_get_non_redundant_dfs_keeps_annot(
    data: pd.DataFrame,
) -> None:
    # Arange
    cols_other: list[str] = ["column1"] + COLS_ANNOTS
    to_ignore: list[str] = list()
    redundant_cols = set(COLS_ANNOTS) & set(cols_other) - set(to_ignore)
    gene_annotations = pg_tables.GeneAnnotations(data)
    data_other = pd.DataFrame(columns=cols_other)
    how = "keep_self"

    # Act
    new_data, new_data_other = gene_annotations._get_non_redundant_dfs(
        data_other, how=how, cols_ignore=to_ignore
    )

    # Assert
    assert new_data.equals(data)
    assert all(col not in new_data_other.columns for col in redundant_cols)
    assert all(col in new_data_other.columns for col in to_ignore)
    assert all(col in new_data.columns for col in to_ignore)


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=5),
)
@settings(max_examples=3)
def test_GeneAnnotations_get_non_redundant_dfs_ignore_redundant(
    data: pd.DataFrame,
) -> None:
    # Arange
    cols_other: list[str] = ["column1"] + COLS_ANNOTS
    to_ignore: list[str] = COLS_ANNOTS[:2]
    redundant_cols = set(COLS_ANNOTS) & set(cols_other) - set(to_ignore)
    gene_annotations = pg_tables.GeneAnnotations(data)
    data_other = pd.DataFrame(columns=cols_other)
    how = "keep_self"

    # Act
    new_data, new_data_other = gene_annotations._get_non_redundant_dfs(
        data_other, how=how, cols_ignore=to_ignore
    )

    # Assert
    assert new_data.equals(data)
    assert all(col not in new_data_other.columns for col in redundant_cols)
    assert all(col in new_data_other.columns for col in to_ignore)
    assert all(col in new_data.columns for col in to_ignore)


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=0),
)
@settings(max_examples=1)
def test_GeneAnnotations_get_non_redundant_dfs_raises_when_unknown_param(
    data: pd.DataFrame,
) -> None:
    # Arange
    cols_other: list[str] = ["column1"] + COLS_ANNOTS
    to_ignore: list[str] = list()
    gene_annotations = pg_tables.GeneAnnotations(data)
    data_other = pd.DataFrame(columns=cols_other)
    how = "unknown"
    gene_annotations = pg_tables.GeneAnnotations(data)

    # Act
    with pytest.raises(ValueError) as excinfo:
        gene_annotations._get_non_redundant_dfs(
            data_other, how=how, cols_ignore=to_ignore
        )

    # Assert
    # Check that a minimally informative error message is raised
    # with the unknown parameter value
    assert how in str(excinfo.value)


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_ANNOTS, max_size=0),
    cols_other=st.lists(stg.simple_str_strategy, min_size=0, max_size=5),
)
@settings(max_examples=5)
def test_GeneAnnotations_get_non_redundant_dfs_does_nothing_when_no_overlap(
    data: pd.DataFrame,
    cols_other: list[str],
) -> None:
    # Arange
    cols_other = list(set(cols_other) - set(COLS_ANNOTS))
    gene_annotations = pg_tables.GeneAnnotations(data)
    data_other = pd.DataFrame(columns=cols_other)
    how = "raise"

    # Act
    new_data, new_data_other = gene_annotations._get_non_redundant_dfs(
        data_other, how=how
    )

    # Assert
    assert new_data.equals(data)
    assert new_data_other.equals(data_other)


# ValidationGenes
@given(data=stg.perigene_table_data_strategy(std_columns=COLS_VALIDATION_GENES))
@settings(max_examples=5)
def test_ValidationGenes_init(data: pd.DataFrame):
    validation_genes = pg_tables.ValidationGenes(data)

    assert isinstance(validation_genes, pg_tables.ValidationGenes)
    assert isinstance(validation_genes.data, pd.DataFrame)
    assert validation_genes.data.equals(data)
    assert len(validation_genes) == len(data)


@given(
    data=stg.perigene_table_data_strategy(std_columns=COLS_VALIDATION_GENES, max_size=0)
)
@settings(max_examples=1)
def test_ValidationGenes_init_fails_when_missing_columns(data: pd.DataFrame):
    for column in COLS_VALIDATION_GENES:
        with pytest.raises(MissingColumnException):
            pg_tables.ValidationGenes(data.drop(columns=[column]))


def test_ValidationGenes_summary_not_annotated():
    n_sources = 2
    n_genes_per_source = 3
    n_genes = n_sources * n_genes_per_source
    data = pd.DataFrame(
        {
            Col.GENE: [f"gene{i}" for i in range(1, 1 + n_genes)],
            Col.SYMBOL: [f"symbol{i}" for i in range(1, 1 + n_genes)],
            Col.GENE_SET_SOURCE: [f"source{i}" for i in range(1, 1 + n_sources)]
            * n_genes_per_source,
        }
    )
    validation_genes = pg_tables.ValidationGenes(data)
    assert validation_genes.summary() == (
        f"Number of validation genes: {n_genes} (unique: {n_genes})"
    )


def test_ValidationGenes_summary_not_annotated_repeated_gene():
    n_sources = 2
    n_genes_per_source = 3
    n_genes = n_sources * n_genes_per_source
    data = pd.DataFrame(
        {
            Col.GENE: [f"gene{i}" for i in range(1, 1 + n_genes_per_source)]
            * n_sources,
            Col.SYMBOL: [f"symbol{i}" for i in range(1, 1 + n_genes)],
            Col.GENE_SET_SOURCE: [f"source{i}" for i in range(1, 1 + n_sources)]
            * n_genes_per_source,
        }
    )
    validation_genes = pg_tables.ValidationGenes(data)
    assert validation_genes.summary() == (
        f"Number of validation genes: {n_genes} (unique: {n_genes_per_source})"
    )


@st.composite
def annotated_gene_sets_strategy(draw):
    data = draw(
        stg.perigene_table_data_strategy(
            std_columns=list(set(COLS_VALIDATION_GENES + COLS_ANNOTS)),
            min_size=5,
            max_size=10,
        )
    )
    # Used to narrow down type for mypy
    assert isinstance(data, pd.DataFrame)

    # Replace some genes with repeated genes
    ids = data[Col.GENE].sample(frac=0.5).unique()
    data[Col.GENE] = draw(
        st.lists(st.sampled_from(ids), min_size=len(data), max_size=len(data))
    )

    # Set some random annotations to NaN
    annot_specific_cols = list(set(COLS_ANNOTS) - set(COLS_VALIDATION_GENES))
    n_masked = 5
    data.loc[data.sample(n_masked).index, annot_specific_cols] = np.nan
    return data


@given(data=annotated_gene_sets_strategy())
@settings(max_examples=3)
def test_ValidationGenes_summary_with_annotations(data: pd.DataFrame):
    validation_genes = pg_tables.ValidationGenes(data)

    expected_n_genes = len(data)
    expected_n_genes_unique = data[Col.GENE].nunique()
    # Gene locations should be in annotations only
    expected_n_genes_annotated = data[[Col.START, Col.END]].notna().all(axis=1).sum()

    summary = validation_genes.summary()

    assert summary == (
        f"Number of validation genes: {expected_n_genes} (unique: "
        f"{expected_n_genes_unique}; with annotations: {expected_n_genes_annotated})"
    )


# PERiGenePredictions
@given(data=stg.perigene_table_data_strategy(std_columns=COLS_PRED))
@settings(max_examples=5)
def test_PERiGenePredictions_init(data: pd.DataFrame):
    perigene_predictions = pg_tables.PERiGenePredictions(data)

    assert isinstance(perigene_predictions, pg_tables.PERiGenePredictions)
    assert isinstance(perigene_predictions.data, pd.DataFrame)
    assert perigene_predictions.data.equals(data)
    assert len(perigene_predictions) == len(data)


@given(data=stg.perigene_table_data_strategy(std_columns=COLS_PRED, max_size=0))
@settings(max_examples=1)
def test_PERiGenePredictions_init_fails_when_missing_columns(data: pd.DataFrame):
    for column in COLS_PRED:
        with pytest.raises(MissingColumnException):
            pg_tables.PERiGenePredictions(data.drop(columns=[column]))
