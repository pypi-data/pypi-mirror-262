from __future__ import annotations

import logging
from collections.abc import Iterable, Iterator, Sequence
from itertools import islice
from pathlib import Path
from typing import TypeVar

import pandas as pd

logger = logging.getLogger(__name__)

T = TypeVar("T")


# ############################## IO ##########################################
def is_gzipped(path: str | Path) -> bool:
    """Uses magic numbers to test whether file is gzipped. c.f.
    https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
    """
    with open(path, "rb") as f:
        return f.read(2) == b"\x1f\x8b"


def save_multi_model_df(df: pd.DataFrame, path: Path, na_fill="NA") -> None:
    """Appends columns of df to existing dataframe. This is done with a lock as
    multiple processes may append columns to the same file. If the file already
    contains some of the columns of df, they are overwritten.
    """

    import filelock

    from . import constants as pg_const

    logger.debug("Saving dataframe with %d columns to %s", len(df.columns), path)

    fname_lock = path.parent / f"{path.name}.lock"
    with filelock.SoftFileLock(fname_lock):
        if path.is_file():
            logger.debug("Found existing file %s. Loading it...", path)
            df_existing = pd.read_csv(path, sep="\t", index_col=0)
            logger.debug(
                "Existing file contains columns for models: %s",
                ", ".join(df_existing.columns),
            )

            overlap = natural_sort(list(set(df_existing.columns) & set(df.columns)))

            if overlap:
                logger.warning(
                    "Some models's columns already exist in %s "
                    "and will be overwritten: %s",
                    path,
                    ", ".join(overlap),
                )

            logger.debug("Merging dataframes...")
            df = pd.concat([df_existing.drop(columns=overlap), df], axis=1)

        logger.debug("Re-ordering columns...")
        # sort columns
        df = df.reindex(natural_sort(df.columns), axis=1)

        logger.debug("Saving dataframe to %s...", path)
        (
            df.to_csv(
                path,
                sep="\t",
                index=True,
                float_format=pg_const.PD_FLOAT_FORMAT,
                na_rep=na_fill,
            )
        )


def read_multi_model_df(path: Path, **kwargs) -> pd.DataFrame:
    """Reads dataframe containing info for multiple models, with one column per model.
    Using a lock as multiple processes may read/modify the same file.
    """
    import filelock

    if not path.is_file():
        raise FileNotFoundError(f"File {path} does not exist.")

    fname_lock = path.parent / f"{path.name}.lock"
    with filelock.SoftFileLock(fname_lock):
        df = pd.read_csv(path, sep="\t", **kwargs)
        return df


# ############################## MISC ########################################
def identity(x: T, *args, **kwargs) -> T:
    return x


def natural_sort(elements: Iterable[str]) -> list[str]:
    """Sorts a list of strings in natural order, i.e. 1, 2, 10, 11, 20, 21, 100,
    101, 110, 111, etc."""
    import re

    def convert(text: str) -> int | str:
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        return [convert(c) for c in re.split(r"([0-9]+)", key)]

    return sorted(elements, key=alphanum_key)


def batched(iterable: Sequence[T], n: int) -> Iterator[tuple[T, ...]]:
    """From itertools recipes. From python 3.12 onwards, we can use
    itertools.batched instead.
    """
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch
