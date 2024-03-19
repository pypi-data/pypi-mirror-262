from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Protocol

import pandas as pd
from numpy.typing import ArrayLike

from .exceptions import InvalidRegionException

__all__ = [
    "FilePrefix",
    "Region",
    "SNP",
    "Locus",
    "DataSubsetCategory",
    "Task",
    "ModelParameter",
    "ModelParametersDict",
    "SKModel",
]


# ##########################################
# ################# Objects ################
# ##########################################


@dataclass
class FilePrefix:
    parent: Path
    file_prefix: str

    def __init__(self, parent: Path | str, file_prefix: str) -> None:
        if not isinstance(parent, (Path, str)):
            raise ValueError("Prefix parent should be a string or a path")
        if not isinstance(file_prefix, str):
            raise ValueError("Prefix parent should be a string or a path")
        self.parent = Path(parent)
        self.file_prefix = file_prefix

    def join(self, f_suffix: str, subfolders: list[str] | None = None) -> Path:
        if subfolders is None:
            dir_out = self.parent
        else:
            dir_out = self.parent / Path(*subfolders)
        return dir_out / (self.file_prefix + f_suffix)

    def __str__(self) -> str:
        return str(self.parent / self.file_prefix)


@dataclass
class Region:
    chrom: str
    start: int
    end: int

    def __post_init__(self):
        if isinstance(self.start, str | float):
            self.start = int(self.start)
        if isinstance(self.end, str | float):
            self.end = int(self.end)

        self._validate()

    @classmethod
    def from_str(cls, region: str, regex: re.Pattern | str | None = None) -> Region:
        # Set default regex
        if regex is None:
            regex = re.compile(r"^([12]?\d|[XY]):(\d+)-(\d+)$")
        # Compile regex if needed
        if isinstance(regex, str):
            regex = re.compile(regex)
        match = regex.match(region)

        if match is None:
            raise ValueError(
                "Region expected to have format chr:start-end or to match the provided "
                "regex. Received %s and reg %s",
                region,
                regex.pattern,
            )
        # Extract chromosome, start and end (start and end can be integers, chr
        # should be a string contained in 1-22, X or Y)
        chr, str_start, str_end = match.groups()
        start, end = int(str_start), int(str_end)

        return cls(chr, start, end)

    def _validate(self):
        try:
            if not isinstance(self.chrom, str):
                raise ValueError("Chromosome should be a string.")

            if self.chrom not in ["X", "Y"] and not (1 <= int(self.chrom) <= 22):
                raise ValueError(
                    "Chromosome should be a string contained in 1-22, X or Y.",
                    self,
                )

            if not all([isinstance(x, int) for x in (self.start, self.end)]):
                raise ValueError("Positions should be integers.")

            if any([x < 0 for x in (self.start, self.end)]):
                raise ValueError("Positions can not be negative.", self)
            if self.start > self.end:
                raise ValueError("End position should be greater or equal to start.")
        except ValueError as e:
            raise InvalidRegionException("Region not properly set: %s", self) from e

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.chrom}:{self.start}-{self.end}"


@dataclass
class SNP:
    rsid: str = "NA"
    pos: int = -1

    def __post_init__(self):
        pos, rsid = self.pos, self.rsid
        err_template = (
            f"Invalid value for `{{name}}`. Received id={rsid} ({type(rsid)}) "
            f"and pos={pos} ({type(pos)})."
        )

        for name, value, type_ in zip(["rsid", "pos"], [rsid, pos], [str, int]):
            if not isinstance(value, type_):
                raise ValueError(err_template.format(name=name))

    def __str__(self) -> str:
        return self.rsid

    def __repr__(self) -> str:
        return f"SNP({self.__str__()})"


@dataclass
class Locus(Region):
    lead_snp: SNP = SNP()
    ld: pd.Series = field(default_factory=lambda: pd.Series(dtype=float))

    @property
    def id(self):
        return f"{self.chrom}_{self.start}_{self.end}_{self.lead_snp}"

    def __str__(self) -> str:
        return f"Chromosome {self.chrom}: {self.start:,}-{self.end:,} ({self.lead_snp})"

    def __repr__(self) -> str:
        return f"Locus({self.__str__()})"


# ##########################################
# ################# Enums ##################
# ##########################################


class DataSubsetCategory(Enum):
    ALL = "ALL"
    TRAIN = "TRAIN"
    TEST = "TEST"
    MASKED = "MASKED"


class Task(Enum):
    REGRESSION = auto()
    CLASSIFICATION = auto()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.name


# ##########################################
# ############## Type hints ################
# ##########################################


ModelParameter = float | int | str | None
ModelParametersDict = dict[str, ModelParameter]
ModelData = dict[DataSubsetCategory, tuple[pd.DataFrame, pd.Series]]


class SKModel(Protocol):
    intercept_: float
    coef_: ArrayLike
    feature_names_in_: ArrayLike

    def fit(self, X: ArrayLike, y: ArrayLike) -> None: ...

    def predict(self, X: ArrayLike) -> ArrayLike: ...

    def score(self, X: ArrayLike, y: ArrayLike) -> float: ...

    def set_params(self, **params: ModelParameter) -> SKModel: ...
