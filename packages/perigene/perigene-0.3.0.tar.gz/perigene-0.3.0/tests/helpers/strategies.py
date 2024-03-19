"""
General strategies shared by multiple testing modules.
"""

from collections.abc import Sequence
from pathlib import Path
from random import shuffle
from string import printable
from typing import Any, cast

import hypothesis.strategies as st
import pandas as pd
from hypothesis.extra import pandas as pdst

from perigene.constants import ColInternal

chromosome_strategy = (
    st.builds(lambda x: str(x), st.integers(min_value=1, max_value=22))
    | st.just("X")
    | st.just("Y")
)
position_strategy = st.integers(min_value=1, max_value=10_000_000)
simple_str_strategy = st.text(printable, min_size=1, max_size=10)


@st.composite
def path_strategy(
    draw: st.DrawFn,
    min_size: int = 0,
    max_size: int = 5,
    is_absolute: bool = False,
) -> Path:
    """Generates a `Path` object with elements.

    Args:
        draw: A function provided by the `hypothesis` library that is used to draw
              values from the strategies.
        min_size: The minimum size of the Path` to be generated.
        max_size: The maximum size of the Path` to be generated.
        is_absolute: Whether the generated `Path` object should be absolute or not.

    Returns:
        A `Path` object with random elements.
    """
    eles = draw(
        st.lists(
            st.from_regex(r"[\w\.-]{1,10}|\.\.|\."),
            min_size=min_size,
            max_size=max_size,
        )
    )
    return Path("/" if is_absolute else "./", *eles)


@st.composite
def str_region_pattern_strategy(
    draw: st.DrawFn,
    start_range: tuple[int, int] = (1, 50),
    end_range: tuple[int, int] = (50, 100),
    single_pos: bool = False,
) -> str:
    """Generates a random string in the format "chrom:start-end".

    Args:
        draw: A function provided by the `hypothesis` library that is used to draw
              values from the strategies.
        chrom_range: The range of possible values for the `chrom` element in the
                     generated string.
        start_range: The range of possible values for the `start` element in the
                     generated string.
        end_range: The range of possible values for the `end` element in the
                   generated string.
        single_pos: Whether the `start` and `end` elements should be the same.

    Returns:
        A string in the format "chrom:start-end".
    """
    chrom = draw(chromosome_strategy)
    start = draw(st.integers(*start_range))
    if single_pos:
        end = start
    else:
        end = draw(st.integers(*end_range))
    return f"{chrom}:{start}-{end}"


BASE_COL_STRATEGIES = {
    ColInternal.GENE: pdst.column(
        ColInternal.GENE,
        dtype=str,
        unique=True,
        elements=simple_str_strategy,
    ),
    ColInternal.SYMBOL: pdst.column(
        ColInternal.SYMBOL,
        dtype=str,
        unique=True,
        elements=simple_str_strategy,
    ),
    ColInternal.CHR: pdst.column(
        ColInternal.CHR,
        elements=chromosome_strategy,
    ),
    ColInternal.POS: pdst.column(
        ColInternal.POS,
        dtype=int,
        elements=position_strategy,
    ),
    ColInternal.SCORE: pdst.column(
        ColInternal.SCORE,
        dtype=float,
    ),
    ColInternal.PRED: pdst.column(
        ColInternal.PRED,
        dtype=float,
    ),
    ColInternal.GENE_SET_SOURCE: pdst.column(
        ColInternal.GENE_SET_SOURCE,
        dtype=str,
        elements=simple_str_strategy,
    ),
    ColInternal.LEAD_SNP_ID: pdst.column(
        ColInternal.LEAD_SNP_ID,
        dtype=str,
        elements=simple_str_strategy,
    ),
    ColInternal.LEAD_SNP_POS: pdst.column(
        ColInternal.LEAD_SNP_POS,
        dtype=int,
        elements=position_strategy,
    ),
    ColInternal.WINDOW: pdst.column(
        ColInternal.WINDOW,
        dtype=int,
        elements=st.integers(min_value=1, max_value=500_000),
    ),
}


@st.composite
def start_end_strategy(
    draw: st.DrawFn, length: int = 20, min_delta: int = 0, max_delta: int = 500_000
):
    """
    Strategy to generate a dataframe with START and END columns.

    Args:
        draw: A function provided by the `hypothesis` library that is used to draw
              values from the strategies.
        length: The number of rows in the dataframe.
        min_delta: The minimum distance between START and END.
        max_delta: The maximum distance between START and END.
    """
    # Enforce start as a Series before sorting to avoid type errors
    start = cast(
        pd.Series,
        draw(
            pdst.series(
                dtype=int,
                elements=position_strategy,
                index=pdst.range_indexes(min_size=length, max_size=length),
            )
        ),
    ).sort_values()

    end = start + cast(int, draw(st.integers(min_value=min_delta, max_value=max_delta)))
    return pd.DataFrame({ColInternal.START: start, ColInternal.END: end})


@st.composite
def perigene_table_data_strategy(
    draw: st.DrawFn,
    std_columns: list[str],
    extra_columns: list[pdst.column] | None = None,
    min_size: int = 0,
    max_size: int = 20,
):
    """
    Strategy for generating valid data tables.
    """

    # Remove duplicates from `std_columns`
    std_columns = list(set(std_columns))

    length = draw(st.integers(min_value=min_size, max_value=max_size))

    # Cast to DataFrame to avoid type errors
    df_base = cast(
        pd.DataFrame,
        draw(
            pdst.data_frames(
                [
                    BASE_COL_STRATEGIES[col]
                    for col in std_columns
                    if col in BASE_COL_STRATEGIES
                ],
                index=pdst.range_indexes(min_size=length, max_size=length),
            )
        ),
    )

    # Add START and END columns if requested
    if ColInternal.START in std_columns or ColInternal.END in std_columns:
        start_end = cast(pd.DataFrame, draw(start_end_strategy(length=length)))
        if ColInternal.START in std_columns:
            df_base[ColInternal.START] = start_end[ColInternal.START]
        if ColInternal.END in std_columns:
            df_base[ColInternal.END] = start_end[ColInternal.END]

    # Re-order columns to match the order in `std_columns`
    df_base = df_base[std_columns]

    # Add extra columns if requested
    if extra_columns is not None:
        df_extra = draw(
            pdst.data_frames(
                extra_columns,
                index=pdst.range_indexes(min_size=length, max_size=length),
            )
        )

        df_base = df_base.join(df_extra)
    return df_base


@st.composite
def subset_sequence(
    draw: st.DrawFn,
    elements: Sequence[Any],
    min_size: int = 0,
    max_size: int | None = None,
    with_replacement: bool = False,
) -> Sequence[Any]:
    if max_size is None:
        max_size = len(elements)
    elif max_size > len(elements):
        raise ValueError("max_size cannot be greater than the number of elements")

    subset_size = draw(st.integers(min_value=min_size, max_value=max_size))
    subset_values = []
    index_pool = list(range(len(elements)))
    for _ in range(subset_size):
        idx_picked = draw(st.sampled_from(index_pool))
        if not with_replacement:
            index_pool.pop(idx_picked)

        subset_values.append(elements[idx_picked])
    return subset_values


@st.composite
def simple_mixed_dataframe_strategy(
    draw: st.DrawFn,
    min_length: int = 0,
    max_length: int = 20,
    n_floats: int = 3,
    n_str: int = 3,
    n_int: int = 3,
    additional_columns: list[pdst.column] | None = None,
) -> pd.DataFrame:
    length = draw(st.integers(min_value=min_length, max_value=max_length))

    index = pdst.range_indexes(min_size=length, max_size=length)

    float_cols = [
        pdst.column(
            dtype=float,
        )
        for _ in range(n_floats)
    ]
    int_cols = [pdst.column(dtype=int) for _ in range(n_int)]
    str_cols = [
        pdst.column(dtype=str, elements=simple_str_strategy) for _ in range(n_str)
    ]

    cols = float_cols + int_cols + str_cols
    if additional_columns is not None:
        cols += additional_columns

    shuffle(cols)

    return draw(pdst.data_frames(cols, index=index))
