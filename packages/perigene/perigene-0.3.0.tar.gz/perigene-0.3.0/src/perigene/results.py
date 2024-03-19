from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pysam

from . import constants as pg_const
from . import data_tables
from . import perigene_types as pg_types

logger = logging.getLogger(__name__)

MAX_VALIDATION_SETS = 4

COL_START = pg_const.ColInternal.START
COL_END = pg_const.ColInternal.END
COL_SYMBOL = pg_const.ColInternal.SYMBOL
COL_SOURCE = pg_const.ColInternal.GENE_SET_SOURCE
COL_POS = "POS"


def get_percentiles(d, pct=None, cols=None):
    if pct is None:
        pct = [2.5, 50, 97.5]
    if cols is None:
        cols = ["ci_low", "pct_50", "ci_high"]
    return pd.DataFrame(np.percentile(d, pct, axis=1).T, columns=cols, index=d.index)


def get_gene_labels(s: pd.Series, n: int = 5, vmin: float = 0, gs=None) -> pd.Series:
    if gs is None:
        gs = set()
    top_genes = s.loc[s > vmin].nlargest(n).index
    labels = s.copy()
    labels.loc[:] = labels.index.array
    labels.loc[~(labels.index.isin(top_genes) | labels.index.isin(gs))] = np.nan
    return labels


class GWASSumstat:
    """Interface to query tabix-indexed gwas summary statistics."""

    def __init__(
        self,
        f_sumstats: Path | str,
        col_id: str = "ID",
        col_chr: str = "CHR",
        col_p: str = "PVAL",
        col_pos: str = "POS",
    ) -> None:
        self.f_sumstats = str(f_sumstats)
        self.cols_map = {col_id: "ID", col_chr: "CHR", col_p: "PVAL", col_pos: "POS"}

    @staticmethod
    def _readline(s: str) -> list[str]:
        return s.strip().split()

    def _query_tabix_file(self, locus: pg_types.Locus) -> pd.DataFrame:
        # Creating TabixFile object in method scope rather than making it an object
        # attribute as overhead is small and avoids cursor issues with multiprocessing
        tabix_sumstats = pysam.TabixFile(self.f_sumstats)
        return (
            pd.DataFrame(
                map(
                    self._readline,
                    tabix_sumstats.fetch(str(locus.chrom), locus.start, locus.end),
                ),
                columns=self._readline(tabix_sumstats.header[0]),
            )
            .rename(columns=self.cols_map)
            .dropna(subset=["ID", "CHR", "PVAL", "POS"])
            .astype(dict(CHR=int, POS=int, PVAL=float))
            .set_index("ID")
        )

    def get(self, locus: pg_types.Locus) -> pd.DataFrame:
        assert all(
            isinstance(arg, int) for arg in [locus.chrom, locus.start, locus.end]
        )
        assert locus.start >= 0
        assert locus.end >= locus.start

        sumstats_locus = self._query_tabix_file(locus)
        with np.errstate(divide="ignore"):
            sumstats_locus["LOG10P"] = -np.log10(sumstats_locus.PVAL)
        return sumstats_locus


class BootstrapResults:
    # Map gene symbols -> gene set
    gene_sets_map: dict[str, str]
    gs_cats: tuple[str, ...]
    df_val_genes_sets: pd.DataFrame

    def __init__(
        self,
        df_results: pd.DataFrame,
        df_val_genes_sets: pd.DataFrame | None,
    ) -> None:
        if COL_POS not in df_results.columns:
            df_results[COL_POS] = df_results[[COL_START, COL_END]].mean(axis=1)

        for col in data_tables.PERiGenePredictions._required_columns:
            assert col in df_results.columns, f"Missing column in dataframe: {col}"
        self.genes = df_results

        self._set_val_genes_sets(df_val_genes_sets)

    def _set_val_genes_sets(self, df_val_genes_sets: pd.DataFrame | None) -> None:
        if df_val_genes_sets is None:
            self.df_val_genes_sets = pd.DataFrame(columns=[COL_SYMBOL, COL_SOURCE])
            self.gs_cats = tuple()
            self.gene_sets_map = dict()
            return

        self.df_val_genes_sets = df_val_genes_sets
        gs_cats = tuple(df_val_genes_sets[COL_SOURCE].unique())
        if len(gs_cats) > MAX_VALIDATION_SETS:
            raise ValueError(
                f"Please provide at most {MAX_VALIDATION_SETS} validation gene sets."
            )
        self.gs_cats = gs_cats
        self.gene_sets_map = df_val_genes_sets.set_index(COL_SYMBOL)[
            COL_SOURCE
        ].to_dict()

    def get_locus(self, locus: pg_types.Locus) -> pd.DataFrame:
        """Subset dataframe to get genes contained in the given window. Genes
        are considered in the window if their position falls in the window.
        If no position is provided, the center of the gene is used
        (mean(END, START)).

        Args:
            locus (Locus): locus object defining the region to query

        Returns:
            pd.DataFrame: _description_
        """
        assert locus.start >= 0
        assert locus.end >= locus.start
        return self.genes.loc[
            (self.genes.CHR == locus.chrom)
            & (self.genes[COL_POS] >= locus.start)
            & (self.genes[COL_POS] <= locus.end)
        ]

    def get_locus_summary(
        self, locus: pg_types.Locus
    ) -> tuple[dict[str, Any], pd.DataFrame]:
        scores_locus = self.get_locus(locus)
        magma = scores_locus[pg_const.ColInternal.SCORE].rename("MAGMA z-score")

        pred_scores = scores_locus.drop(
            columns=[c for c in pg_const.ColInternal.values()]
        )
        n_boots = pred_scores.shape[1]

        stats = dict()
        genes = scores_locus.index
        gs_genes = genes.to_series().map(self.gene_sets_map)
        annot = gs_genes.fillna("")
        annot.name = ""
        gs_genes = gs_genes.dropna().index.tolist()
        n_genes = len(genes)

        # Distance to lead SNP
        distance = (scores_locus.POS - locus.lead_snp.pos).rename(
            "Distance to lead SNP"
        )
        stats["distance"] = dict(
            var=distance,
            ci=None,
            labels=None,
            annot=annot,
        )

        # Magma z score
        stats["score_magma"] = dict(
            var=magma,
            ci=None,
            labels=get_gene_labels(magma, vmin=2, gs=gs_genes),
            annot=annot,
        )

        # Magma ranks
        # Note: use -rank to get labels
        magma_rank = magma.rank(ascending=False)
        magma_rank.name = "Rank by MAGMA z-score"
        stats["rank_magma"] = dict(
            var=magma_rank,
            ci=None,
            labels=get_gene_labels(-magma_rank, vmin=-10, gs=gs_genes),
            annot=annot,
        )

        # Median and 95% CI of scores
        df_pred = get_percentiles(pred_scores)
        stats["pred"] = dict(
            var=df_pred.pct_50.rename("Predicted score"),
            ci=df_pred[["ci_low", "ci_high"]],
            labels=None,
            annot=annot,
        )

        # Median and 95% CI of ranks
        pred_ranks = pred_scores.rank(ascending=False)
        df_rank = get_percentiles(pred_ranks)
        stats["rank"] = dict(
            var=df_rank.pct_50.rename("Rank by predicted score"),
            ci=df_rank[["ci_low", "ci_high"]],
            labels=None,
            annot=annot,
        )

        # Fraction of bootstrap where gene has highest score of the locus
        # Use rank<2 instead rank == 1 in case of ties
        v_top = (pred_ranks < 2).sum(axis=1) / n_boots
        v_top.name = "Frac. highest predicted score"
        stats["frac_top"] = dict(
            var=v_top,
            ci=None,
            labels=get_gene_labels(v_top, vmin=0.1, gs=gs_genes),
            annot=annot,
        )

        # Fraction of bootstrap where gene is in top decile
        v_top_decile = (pred_ranks <= np.ceil(n_genes / 10)).sum(axis=1) / n_boots
        v_top_decile.name = "Frac. predicted in top decile"
        stats["frac_top_decile"] = dict(
            var=v_top_decile,
            ci=None,
            labels=get_gene_labels(v_top_decile, vmin=0.1, gs=gs_genes),
            annot=annot,
        )

        stats["info"] = dict(n_genes=n_genes, n_boots=n_boots)
        return stats, scores_locus

    def get_merged_locus_summary(self, locus: pg_types.Locus):
        assert isinstance(locus, pg_types.Locus)
        stats, df_locus = self.get_locus_summary(locus)

        # As genes may be in different sets, keep only 1st one for annotations
        genes_sets = self.df_val_genes_sets.drop_duplicates(COL_SYMBOL).set_index(
            COL_SYMBOL
        )
        df_locus = df_locus.join(genes_sets)
        df = pd.DataFrame(
            [
                pd.Series(
                    data=locus.id,
                    index=df_locus.index,
                    name="locus",
                ),
                df_locus[COL_SOURCE].rename("Gene set").fillna("Other genes"),
            ]
            + [v["var"] for k, v in stats.items() if (k != "info")]
        ).T.infer_objects()
        for s in [
            "MAGMA z-score",
            "Rank by MAGMA z-score",
            "Predicted score",
            "Rank by predicted score",
        ]:
            df[f"Scaled {s if s.startswith('MAGMA') else s[0].lower() + s[1:]}"] = (
                min_max_scale(df[s])
            )

        return df


def min_max_scale(x):
    return (x - x.min()) / (x.max() - x.min())
