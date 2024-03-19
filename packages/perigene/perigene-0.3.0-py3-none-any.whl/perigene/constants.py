from typing import Any

PD_FLOAT_FORMAT = "%.6g"

__all__ = [
    "ColFeatures",
    "ColInternal",
    "ColScores",
    "FileSuffix",
]


class ImmutableAttributes(type):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise AttributeError(f"Cannot reassign constant {name}")
        super().__setattr__(name, value)


class ConstantClass(metaclass=ImmutableAttributes):
    def __init__(self, **kwargs: Any) -> None:
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)

    @classmethod
    def values(cls) -> list[Any]:
        """Returns all values of the class."""
        return [
            v
            for k, v in cls.__dict__.items()
            if not k.startswith("__") and not callable(v)
        ]

    def __new__(cls):
        raise TypeError(f"{cls.__name__} is not meant to be instantiated.")


class ColFeatures(ConstantClass):
    """Column names of features files accepted by PERiGene."""

    GENE: str = "GENE"


class ColInternal(ConstantClass):
    """Column names used internally by PERiGene."""

    GENE: str = "GENE"
    SYMBOL: str = "SYMBOL"
    CHR: str = "CHR"
    START: str = "START"
    END: str = "END"
    POS: str = "POS"
    SCORE: str = "score"
    PRED: str = "prediction"
    GENE_SET_SOURCE: str = "SOURCE"
    LEAD_SNP_ID: str = "LEAD_VARIANT_ID"
    LEAD_SNP_POS: str = "LEAD_VARIANT_POS"
    WINDOW: str = "WINDOW"
    FEATURE: str = "FEATURE"


class ColScores(ConstantClass):
    """Column names of scores files accepted by PERiGene."""

    CHR: str = "chrom"
    START: str = "start"
    END: str = "end"
    GENE: str = "gene"
    SCORE: str = "score"


class FileSuffix(ConstantClass):
    INFO: str = ".info.json"
    INDEX: str = ".index.gz"
    INDEX_GENES: str = ".genes.gz"
    INDEX_FEATURES: str = ".features.gz"
    OPTUNA_JOURNAL: str = ".optuna.journal"
    PRED_SCORES: str = ".pred.gz"
    WEIGHTS: str = ".weights.gz"
