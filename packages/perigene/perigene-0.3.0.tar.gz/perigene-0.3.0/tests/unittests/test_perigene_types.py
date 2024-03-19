from __future__ import annotations

from pathlib import Path

import hypothesis.strategies as st
import pytest
from hypothesis import given, settings

from perigene.exceptions import InvalidRegionException
from perigene.perigene_types import FilePrefix, Region


@st.composite
def region_pattern(
    draw: st.DrawFn,
    chrom_range: tuple[int, int] = (1, 10),
    start_range: tuple[int, int] = (1, 50),
    end_range: tuple[int, int] = (50, 100),
    single_pos: bool = False,
) -> str:
    chrom = draw(st.integers(*chrom_range))
    start = draw(st.integers(*start_range))
    if single_pos:
        end = start
    else:
        end = draw(st.integers(*end_range))
    return f"{chrom}:{start}-{end}"


@st.composite
def file_prefix(
    draw: st.DrawFn,
    min_size: int = 0,
    max_size: int = 5,
) -> FilePrefix:
    eles = draw(
        st.lists(
            st.characters(blacklist_characters=["/"]),
            min_size=min_size,
            max_size=max_size,
        )
    )
    root = Path("/", *eles)
    file_prefix = draw(st.characters(blacklist_characters=["/"]))
    return FilePrefix(root, file_prefix)


@given(
    file_prefix(),
    st.characters(),
    st.one_of(st.lists(st.characters(), max_size=5), st.none()),
)
def test_FilePrefix(fp: FilePrefix, suffix: str, subfolders: list[str] | None):
    assert str(fp) == str(fp.parent / fp.file_prefix)
    if subfolders is None:
        expected = fp.parent / (fp.file_prefix + suffix)
    else:
        expected = fp.parent / Path(*subfolders) / (fp.file_prefix + suffix)
    assert fp.join(suffix, subfolders=subfolders) == expected


@given(st.one_of(st.none(), st.integers(), st.floats()))
def test_FilePrefix_raise_ValueError_when_not_str_or_path(
    invalid_value: int | float | None,
):
    valid_value = Path("/foo/bar")

    with pytest.raises(ValueError):
        FilePrefix(valid_value, invalid_value)  # type: ignore

    with pytest.raises(ValueError):
        FilePrefix(invalid_value, valid_value)  # type: ignore


@given(st.characters())
@settings(max_examples=20)
def test_Region_from_str_with_random_patterns(region: str) -> None:
    with pytest.raises(ValueError):
        _ = Region.from_str(region)


@given(st.one_of(region_pattern(), region_pattern(single_pos=True)))
@settings(max_examples=20)
def test_Region_from_str_with_valid_patterns(region):
    r = Region.from_str(region)
    assert r.chrom in list(map(str, range(1, 22))) + ["X", "Y"]
    assert r.start <= r.end


@given(region_pattern(start_range=(51, 100), end_range=(1, 50)))
def test_Region_from_str_pos_is_smaller_than_start(region):
    with pytest.raises(InvalidRegionException):
        _ = Region.from_str(region)


@given(chrom=st.integers(1, 22), start=st.integers(-100, -1), end=st.integers(1, 100))
@settings(max_examples=20)
def test_Region_negative_pos(chrom: int, start: int, end: int) -> None:
    with pytest.raises(InvalidRegionException):
        _ = Region(str(chrom), start, end)


@given(chrom=st.integers(1, 22), start=st.integers(1, 10), end=st.integers(20, 30))
@settings(max_examples=20)
def test_Region_integer_chrom(chrom: int, start: int, end: int) -> None:
    with pytest.raises(InvalidRegionException):
        _ = Region(chrom, start, end)  # type: ignore
