#!/usr/bin/env python

"""Tests for `perigene` package."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from perigene import data
from perigene.constants import ColInternal


def shuffle_df(old_df: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    new_df = old_df.sample(frac=1)
    # Small number of genes makes it technically not impossible to have same
    # order after shuffling. Make sure it is really shuffled.
    while old_df.index.equals(new_df.index):
        new_df = old_df.sample(frac=1)
    return new_df


@pytest.fixture
def data_cont():
    """Creates a ``Data`` object with a continuous gene score (e.g. zscore)"""
    from io import StringIO

    X = pd.read_table(
        StringIO(
            """ID	f1	f2	f3	f4
            0	0	0	-0.075300	-1.281604
            1	1	0	-1.874237	1.554510
            2	0	0	-1.033161	0.548596
            3	1	0	0.053867	1.513119
            4	1	1	0.176084	-1.528917
            5	0	0	-0.218561	1.875383
            6	1	0	-0.501028	-0.351955
            7	0	0	0.886521	-0.734363
            8	0	0	0.088068	-0.315338
            9	1	0	1.127707	-1.087127
            """
        ),
        index_col=0,
    )
    y = pd.read_table(
        StringIO(
            """ID	score
            0	-2.259
            1	-1.027
            2	-0.504
            3	-0.243
            4	0.761
            5	-1.105
            6	-0.041
            7	0.108
            8	-0.446
            9	-0.337
            """
        ),
        index_col=0,
    )
    genes_loc = pd.read_table(
        StringIO(
            """ID	CHR	START	END
            0	1	1000	2000
            1	1	3000	4000
            2	1	5000	6000
            3	1	7000	8000
            4	2	1000	2000
            5	2	3000	4000
            6	2	5000	6000
            7	3	1000	2000
            8	3	3000	4000
            9	3	5000	6000
            """
        ),
        index_col=0,
    )
    return data.Data(X, y, genes_loc, index=None)


def test_data_init_missing_index_name(data_cont: data.Data):
    """Test that genes ids column name is properly set."""
    # Arrange
    new_name = ""
    expected_name = ColInternal.GENE
    kwargs = dict(
        X=data_cont.X.rename_axis(new_name),
        y=data_cont.y.rename_axis(new_name),
        genes_loc=data_cont.genes_loc.rename_axis(new_name),
    )

    # Act
    new_data = data.Data(**kwargs)

    # Assert
    assert new_data.X.index.name == expected_name
    assert new_data.y.index.name == expected_name
    assert new_data.genes_loc.index.name == expected_name


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_X_with_shuffled_gene_ids(data_cont: data.Data):
    """Test that genes ids are properly reordered to known gene order when
    shuffled.
    """
    # Arrange
    old_X = data_cont.X.copy()
    new_X = shuffle_df(old_X)
    # Act
    data_cont.X = new_X
    # Assert
    assert data_cont.X.index.equals(old_X.index)


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_X_with_previously_unknown_gene(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    old_X = data_cont.X.copy()
    new_gene = pd.Series(np.zeros(old_X.shape[1]), name="4567890", index=old_X.columns)
    new_X = pd.concat([old_X, new_gene.to_frame().T])
    # Act
    with pytest.raises(AssertionError) as excinfo:
        data_cont.X = new_X
    # Assert
    assert new_gene.name in str(excinfo)


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_X_with_missing_gene(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    old_X = data_cont.X.copy()
    missing_gene = old_X.sample(1).index[0]
    new_X = old_X.drop(missing_gene)
    # Act
    with pytest.raises(AssertionError) as excinfo:
        data_cont.X = new_X
    # Assert
    assert str(missing_gene) in str(excinfo)


def test_data_set_X_assert_index_is_renamed(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    new_X = data_cont.X.copy()
    new_X.index.name = ""
    # Act
    data_cont.X = new_X
    # Assert
    assert data_cont.X.index.name == ColInternal.GENE


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_y_with_shuffled_gene_ids(data_cont: data.Data):
    """Test that genes ids are properly reordered to known gene order when
    shuffled.
    """
    # Arrange
    old_y = data_cont.y.copy()
    new_y = shuffle_df(old_y)
    # Act
    data_cont.y = new_y
    # Assert
    assert data_cont.y.index.equals(old_y.index)


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_y_with_previously_unknown_gene(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    old_y = data_cont.y.copy()
    new_gene = pd.Series(np.zeros(old_y.shape[1]), name="4567890", index=old_y.columns)
    new_y = pd.concat([old_y, new_gene.to_frame().T])
    # Act
    with pytest.raises(AssertionError) as excinfo:
        data_cont.y = new_y
    # Assert
    assert new_gene.name in str(excinfo)


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_y_with_missing_gene(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    old_y = data_cont.y.copy()
    missing_gene = old_y.sample(1).index[0]
    new_y = old_y.drop(missing_gene)
    # Act
    with pytest.raises(AssertionError) as excinfo:
        data_cont.y = new_y
    # Assert
    assert str(missing_gene) in str(excinfo)


def test_data_set_y_assert_index_is_renamed(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    new_y = data_cont.y.copy()
    new_y.index.name = ""
    # Act
    data_cont.y = new_y
    # Assert
    assert data_cont.y.index.name == ColInternal.GENE


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_genes_loc_with_shuffled_gene_ids(data_cont: data.Data):
    """Test that genes ids are properly reordered to known gene order when
    shuffled.
    """
    # Arrange
    old_genes_loc = data_cont.genes_loc.copy()
    new_genes_loc = shuffle_df(old_genes_loc)
    # Act
    data_cont.genes_loc = new_genes_loc
    # Assert
    assert data_cont.genes_loc.index.equals(old_genes_loc.index)


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_genes_loc_with_previously_unknown_gene(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    old_genes_loc = data_cont.genes_loc.copy()
    new_gene = pd.Series(
        np.zeros(old_genes_loc.shape[1]), name="4567890", index=old_genes_loc.columns
    )
    new_genes_loc = pd.concat([old_genes_loc, new_gene.to_frame().T])
    # Act
    with pytest.raises(AssertionError) as excinfo:
        data_cont.genes_loc = new_genes_loc
    # Assert
    assert new_gene.name in str(excinfo)


@pytest.mark.skip(reason="May not be necessary following refactoring")
def test_data_set_genes_loc_with_missing_gene(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    old_genes_loc = data_cont.genes_loc.copy()
    missing_gene = old_genes_loc.sample(1).index[0]
    new_genes_loc = old_genes_loc.drop(missing_gene)
    # Act
    with pytest.raises(AssertionError) as excinfo:
        data_cont.genes_loc = new_genes_loc
    # Assert
    assert str(missing_gene) in str(excinfo)


def test_data_set_genes_loc_assert_index_is_renamed(data_cont: data.Data):
    """Test error is raise if trying to set data with a gene that was
    previously not seen.
    """
    # Arrange
    new_genes_loc = data_cont.genes_loc.copy()
    new_genes_loc.index.name = ""
    # Act
    data_cont.genes_loc = new_genes_loc
    # Assert
    assert data_cont.genes_loc.index.name == ColInternal.GENE
