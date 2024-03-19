from __future__ import annotations

import logging
import os
from collections.abc import Generator
from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd

from ..constants import ColScores, ConstantClass
from ..perigene_types import FilePrefix

logger = logging.getLogger(__name__)

# Extensions for the MAGMA output files
EXT_MAGMA_RAW = ".genes.raw"
EXT_MAGMA_OUT = ".genes.out"

# Extensions for the formatted files
EXT_BLOCK_GENES_CORR = ".block_corr.npz"
EXT_COVARIATES = ".covariates.tsv"
EXT_MAGMA_SCORES = ".scores.raw.bed"
EXT_MAGMA_SCORES_PROJ = ".scores.bed"

# Positions of the columns necessary from the .genes.raw MAGMA file
# Note: the MAGMA raw file is headerless
COL_GENE_MAGMA_RAW = 0
COL_CHROM_MAGMA_RAW = 1
COL_NSNPS_MAGMA_RAW = 4
COL_NPARAM_MAGMA_RAW = 5
COL_MAC_MAGMA_RAW = 7
N_INFO_FIELDS_MAGMA_RAW = 9
GENES_INFO_COLS = ["GENE", "NSNPS", "NPARAM", "MAC"]


# Names of the columns necessary from the .genes.out MAGMA file
class _ColMagmaOut(ConstantClass):
    GENE = "GENE"
    ZSTAT = "ZSTAT"
    P = "P"
    CHR = "CHR"
    START = "START"
    END = "STOP"


def iter_file(
    f: str | os.PathLike, sep=" ", comment="#"
) -> Generator[list[str], None, None]:
    with open(f) as f_in:
        for line in f_in:
            # Skip comments
            if line.startswith(comment):
                continue
            yield line.strip().split(sep)


class MAGMARawChromData:
    def __init__(self, chrom: int) -> None:
        self.chrom = chrom
        self.genes_corr: list[npt.NDArray] = []
        self.genes_info: list[list[str | float]] = []

    def append(self, genes_corr: npt.NDArray, genes_info: list[str | float]) -> None:
        self.genes_corr.append(genes_corr)
        self.genes_info.append(genes_info)

    def get_genes_info(self) -> pd.DataFrame:
        return pd.DataFrame(self.genes_info, columns=GENES_INFO_COLS)

    def get_genes_corr(self) -> npt.NDArray:
        """
        Concatenate and pad rows and symmetrize the matrix.

        In terms of padding:

        1. Adds zeros to the left of the row when reaching a gene that is not
        correlated with the first genes of the chromosome. For the Nth gene (on
        line N) in a MAGMA raw file the correlations reported are with the genes
        at lines N-1, N-2, N-3, etc. So the number of zeros to add is equal to N
        minus the number of correlations reported at that row.
        2. Adds zeros to the right of the row to assure that all rowas have the
        same length, equal to the number of genes in the chromosome.
        """
        max_dim = len(self.genes_corr)

        padded_genes_corr = np.vstack(
            [
                np.pad(row, (idx - row.shape[0], max_dim - idx))
                for idx, row in enumerate(self.genes_corr)
            ]
        )
        return padded_genes_corr + padded_genes_corr.T + np.eye(max_dim)


def iter_magma_raw(
    f: str | os.PathLike,
) -> Generator[tuple[npt.NDArray, pd.DataFrame], None, None]:
    chrom_data = MAGMARawChromData(1)
    for line in iter_file(f):
        chrom = int(line[COL_CHROM_MAGMA_RAW])

        if chrom < chrom_data.chrom:
            raise ValueError(
                "ERROR: malformatted file: chromosomes are not sequentially ordered."
            )
        elif chrom > chrom_data.chrom:
            # return data for the current chromosome and reset values with new one
            yield chrom_data.get_genes_corr(), chrom_data.get_genes_info()
            chrom_data = MAGMARawChromData(chrom)

        chrom_data.append(
            np.array(line[N_INFO_FIELDS_MAGMA_RAW:], dtype=np.float64),
            [
                line[COL_GENE_MAGMA_RAW],
                float(line[COL_NSNPS_MAGMA_RAW]),
                float(line[COL_NPARAM_MAGMA_RAW]),
                float(line[COL_MAC_MAGMA_RAW]),
            ],
        )
    # return data from last chromosome
    yield chrom_data.get_genes_corr(), chrom_data.get_genes_info()


def read_magma_raw(raw_file: str | Path) -> tuple[list[np.ndarray], pd.DataFrame]:
    block_genes_corr = []
    genes_info_all_file = []
    for genes_corr_chrom, genes_info_chrom in iter_magma_raw(raw_file):
        block_genes_corr.append(genes_corr_chrom)
        genes_info_all_file.append(genes_info_chrom)

    return block_genes_corr, pd.concat(genes_info_all_file)


def format_covariates(df: pd.DataFrame) -> pd.DataFrame:
    """Format covariates to match what MAGMA does internally.

    Args:
        df: DataFrame with covariates. Must contain columns GENE, NSNPS, NPARAM, MAC.

    Returns:
        DataFrame with covariates formatted similar to MAGMA

    Notes from MAGMA manual (v1.10):
        "By default the gene set variable is conditioned on the gene size, gene density
        (representing the relative level of LD between SNPs in that gene) and the
        inverse of the mean MAC in the gene (to correct for potential power loss in
        very low MAC SNPs), as well the log value of these three variables"

        "[...] Internal variable names are 'size'/'genesize', 'density', 'mac', and
        'sampsize'/'N', which designate the gene size in number of SNPs, the gene
        density (a measure of within-gene LD), the inverse mean minor allele count, and
        the sample size (if this does not vary across genes, it is disabled
        automatically)"
    """
    logger.info("Formatting covariates")
    return (
        # Add inverse minor allele count and gene density
        df.assign(INV_MAC=1 / df.MAC.values, DENSITY=df.NPARAM / df.NSNPS)
        # Rename NSNPS for consistency with MAGMA
        .rename(columns=dict(NSNPS="GENE_SIZE")).astype({"GENE_SIZE": int})
        # Keep only covariates used in MAGMA gene set analysis
        .set_index(_ColMagmaOut.GENE)[["GENE_SIZE", "INV_MAC", "DENSITY"]]
        # Add log covariates
        .pipe(lambda df: df.join(np.log(df).set_axis("LOG_" + df.columns, axis=1)))
    )


def _regularize_block_genes_corr(
    genes_corr: list[np.ndarray], offset=0.1
) -> list[np.ndarray]:
    """Adds a scalar to the diagnonal of the gene-gene correlation matrix to make sure
    it is positive definite. The scalar is the smallest eigen value of the matrix if it
    is negative + a provided offset to make sure it is positive.

    Args:
        genes_corr: List of gene-gene correlation matrices
        offset: Minimum offset to add to the diagonal of the correlation matrix
            to make sure it is positive definite. Default is 0.1.
    """
    logger.info("Regularizing genes correlation matrices")
    # Get the smallest eigen value. As the gene-gene correlation is a block
    # diagnonal matrix, its eigen values are simply the eigen values of each
    # sub-matrix.
    min_eigen = min([np.linalg.eigvalsh(c).min() for c in genes_corr])

    # Determine constant to add to the diagonal
    const = min(abs(min_eigen), 0) + offset

    # Return regularized matrix with const added to the diagonal
    return [c + np.eye(len(c)) * const for c in genes_corr]


def _process_magma_raw_file(
    path_magma_raw_file: Path,
    *,
    covariates_names: list[str] | None = None,
    min_offset_corr: float = 0.1,
) -> tuple[list[np.ndarray], pd.DataFrame]:
    if not path_magma_raw_file.is_file():
        raise FileNotFoundError(f"File {path_magma_raw_file} not found")

    # Get gene-gene correlation as a block diagonal matrix
    block_genes_corr, covariates = read_magma_raw(path_magma_raw_file)

    # Format the raw data
    block_genes_corr = _regularize_block_genes_corr(block_genes_corr, min_offset_corr)
    covariates = format_covariates(covariates)
    if covariates_names is not None:
        covariates = covariates[covariates_names]

    return block_genes_corr, covariates


def _format_magma_scores(
    path_magma_out_file: Path,
    *,
    covariates: pd.DataFrame | None,
    correlation: npt.NDArray | None,
    transform: str | None = None,
) -> pd.DataFrame:
    """
    Format MAGMA scores for use with perigene

    Args:
        path_magma_out_file: Path to MAGMA output file
        weight: Method used to calculate the gene weights. If None, the gene weights
        are not included in the output file.
    """
    if not path_magma_out_file.is_file():
        raise FileNotFoundError(f"File {path_magma_out_file} not found")

    logger.info("Reading MAGMA scores from %s", path_magma_out_file)
    df_scores = pd.read_table(path_magma_out_file, sep=r"\s+", comment="#")

    df_proj = _project_zscores(df_scores, covariates, correlation)

    y_ = df_proj[ColScores.SCORE].values
    if transform == "log":
        logger.info("Log-transforming MAGMA scores")
        df_proj[ColScores.SCORE] = np.log1p(y_ - y_.min())
    elif transform == "minmax":
        logger.info("Min-max transforming MAGMA scores")
        df_proj[ColScores.SCORE] = (y_ - y_.min()) / (y_.max() - y_.min())
    elif transform is None:
        logger.info("No transformation applied to MAGMA scores")
    else:
        raise ValueError(f"Unknown transformation method: {transform}")

    return df_proj


def _project_zscores(
    df: pd.DataFrame,
    covariates: pd.DataFrame | None,
    correlation: npt.NDArray | None,
) -> pd.DataFrame:
    import statsmodels.api as sm

    zscores = df.set_index(_ColMagmaOut.GENE)[_ColMagmaOut.ZSTAT].copy()

    # Scale MAGMA scores to have mean 0 and std 1
    zscores = (zscores - zscores.mean()) / zscores.std()

    if covariates is None or covariates.empty:
        logger.info("No covariates provided. Using transformed MAGMA scores directly")
        zscores_proj = zscores
    else:
        logger.info("Projecting covariates and gene-gene correlation matrix")
        zscores_proj = sm.GLS(zscores, covariates, sigma=correlation).fit().resid

    df[ColScores.SCORE] = zscores_proj.values
    return df


def _save_magma_scores(
    df_scores: pd.DataFrame, prefix_out: FilePrefix, save_raw: bool
) -> None:
    cols_out = [
        ColScores.CHR,
        ColScores.START,
        ColScores.END,
        ColScores.GENE,
        ColScores.SCORE,
    ]
    cols_mapping = {
        _ColMagmaOut.CHR: ColScores.CHR,
        _ColMagmaOut.GENE: ColScores.GENE,
        _ColMagmaOut.START: ColScores.START,
        _ColMagmaOut.END: ColScores.END,
    }

    # Use colnames matching perigene's expected input
    df_scores = df_scores.copy().rename(columns=cols_mapping)

    # Save to file (limiting float precision to 5 significant digits)
    save_kwargs = dict(sep="\t", index=False, float_format="%.5g")

    # save the processed MAGMA scores
    fname_out = prefix_out.join(EXT_MAGMA_SCORES_PROJ)
    logger.info("Saving projected MAGMA scores to %s", fname_out)
    df_scores[cols_out].to_csv(fname_out, **save_kwargs)

    if not save_raw:
        return

    df_scores = (
        df_scores
        # drop the processed MAGMA scores
        .drop(columns=ColScores.SCORE)
        # and rename the raw scores to match the bed format
        .rename(columns={_ColMagmaOut.ZSTAT: ColScores.SCORE})
    )

    fname_out = prefix_out.join(EXT_MAGMA_SCORES)
    logger.info("Saving raw MAGMA scores to %s", fname_out)
    df_scores[cols_out].to_csv(fname_out, **save_kwargs)


def format_magma_output(
    *,
    magma_prefix: FilePrefix,
    prefix_out: FilePrefix,
    covariates_names: list[str] | None = None,
    min_offset_covariance: float = 0.5,
    transform: str | None = None,
    save_raw: bool = True,
    save_covariates: bool = True,
    save_correlation: bool = True,
) -> None:
    """Format MAGMA output for use with perigene

    Args:

    """
    import scipy

    logger.info("Formatting MAGMA output")
    block_genes_corr, covariates = _process_magma_raw_file(
        magma_prefix.join(EXT_MAGMA_RAW),
        covariates_names=covariates_names,
        min_offset_corr=min_offset_covariance,
    )

    gene_gene_corr = scipy.linalg.block_diag(*block_genes_corr)

    df_scores = _format_magma_scores(
        magma_prefix.join(EXT_MAGMA_OUT),
        correlation=gene_gene_corr,
        covariates=covariates,
        transform=transform,
    )

    # Save formatted data
    _save_magma_scores(df_scores, prefix_out, save_raw)
    if save_correlation:
        f_block_corr = prefix_out.join(EXT_BLOCK_GENES_CORR)
        logger.info("Saving gene-gene correlation to %s", f_block_corr)
        np.savez_compressed(f_block_corr, *block_genes_corr)
    if save_covariates:
        f_covariates = prefix_out.join(EXT_COVARIATES)
        logger.info("Saving covariates to %s", f_covariates)
        covariates.to_csv(f_covariates, sep="\t", float_format="%.5g", index=True)
