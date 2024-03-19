#!/usr/bin/python

from __future__ import annotations

import logging
from pathlib import Path

import optuna
import pandas as pd
from optuna import Study
from sklearn.exceptions import NotFittedError

from perigene.tuning import get_study, tune_model_params

from . import constants as pg_const
from . import models
from . import perigene_types as pg_types
from .data import Data
from .data_tables import PERiGenePredictions
from .exceptions import MissingTargetDataException
from .info import PERiGeneInfo
from .utils import read_multi_model_df, save_multi_model_df

logger = logging.getLogger(__name__)
IS_DEBUG_ON = logger.isEnabledFor(logging.DEBUG)


class TrainingManager:
    info: PERiGeneInfo
    prefix: pg_types.FilePrefix

    data: Data

    models_dict: dict[str, models.Model]

    @classmethod
    def new(
        cls,
        prefix: pg_types.FilePrefix,
        data: Data,
        info: PERiGeneInfo,
    ) -> TrainingManager:
        manager = cls(
            prefix=prefix,
            data=data,
            info=info,
            overwrite_existing=True,
        )
        return manager

    @classmethod
    def load(
        cls,
        prefix: pg_types.FilePrefix,
    ) -> TrainingManager:
        info = PERiGeneInfo.read(prefix)

        data = Data.load(
            path_features=info.paths.features,
            path_scores=info.paths.scores,
            prefix=prefix,
        )

        manager = cls(
            data=data,
            info=info,
            overwrite_existing=True,
            prefix=prefix,
        )
        manager.info = info

        f_pred = prefix.join(pg_const.FileSuffix.PRED_SCORES)

        if not f_pred.is_file():
            # Don't try to load predictions if they don't exist
            return manager

        logger.info(
            "PERiGene scores were already computed for this analysis. Loading them..."
        )

        y_pred = pd.read_table(f_pred, index_col=0)[pg_const.ColInternal.PRED]
        y_pred.index = y_pred.index.astype(str)
        manager.data.y_pred = y_pred

        return manager

    def __init__(
        self,
        *,
        prefix: pg_types.FilePrefix,
        data: Data,
        info: PERiGeneInfo,
        overwrite_existing: bool = False,
    ) -> None:
        # Check that all required paths exist
        for p in (prefix.parent, info.paths.features, info.paths.scores):
            if not p.exists():
                raise FileNotFoundError(f"Could not find path {p}.")

        # Don't overwrite existing folder
        if prefix.join(pg_const.FileSuffix.INFO).is_file() and (not overwrite_existing):
            raise ValueError(
                f"A study already exists in {prefix.parent}. "
                "Set overwrite_existing to True to overwrite it. "
                "Otherwise, use the class method to load an existing study."
            )
        self.prefix = prefix

        self.data = data
        self.models_dict = dict()
        self.info = info

    def hyperparameter_tuning(
        self,
        ntrials: int = 20,
        storage: str | None = None,
        overwrite_study: bool = False,
    ) -> TrainingManager:
        assert self.info.model_params is not None

        if storage is None:
            storage = str(self.prefix.join(pg_const.FileSuffix.OPTUNA_JOURNAL))

        for key_model, data in self.data:
            X_train, y_train = data[pg_types.DataSubsetCategory.TRAIN]

            if IS_DEBUG_ON:
                logger.debug("Tuning hyperparameters for model %s ...", key_model)
                logger.debug("Train data shape %i rows, %i columns", *X_train.shape)

            objective = self.info.model.get_objective(X_train, y_train)

            # Load existing parameter values if pre-tuned otherwise use default
            if key_model in self.info.model_params:
                base_params = self.info.model_params[key_model]
            else:
                base_params = self.info.model.get_default_model_params()
                self.info.model_params[key_model] = base_params

            study_name = f"{self.info.model.__name__}_{key_model}"

            new_params = tune_model_params(
                storage=storage,
                study_name=study_name,
                objective=objective,
                base_params=base_params,
                ntrials=ntrials,
                reset_study=overwrite_study,
            )

            logger.debug("Updating parameters to %s", new_params)
            self.info.model_params[key_model] = new_params

        return self

    def get_study(self, key_model: str, storage: str | None = None) -> Study:
        optuna.logging.enable_propagation()
        optuna.logging.disable_default_handler()

        study_name = f"{self.info.model.__name__}_{key_model}"
        if storage is None:
            storage = str(self.prefix.join(pg_const.FileSuffix.OPTUNA_JOURNAL))

        return get_study(storage, study_name)

    def predict_from_models(self) -> TrainingManager:
        logger.info("Predictions ...")
        predictions = []
        for name, model in self.models_dict.items():
            if name not in self.info.model_params:
                raise ValueError("Missing model. Cannot make predictions for %s", name)

            try:
                X_test = self.data.get(name, pg_types.DataSubsetCategory.TEST)[0]
                if IS_DEBUG_ON:
                    logger.debug("--> Chromosome %s", name)
                    logger.debug(
                        "test features shape %i rows, %i columns", *X_test.shape
                    )

                y_pred = model.predict(X_test)
                predictions.append(y_pred)
            except MissingTargetDataException:
                logger.warning(
                    "No test data for model %s. Skipping it...",
                    name,
                )
            except NotFittedError:
                logger.warning(
                    "Cannot make predictions for model %s: the model has not been "
                    "trained yet. Skipping it...",
                    name,
                )
                continue
        if len(predictions) < 1:
            logger.warning(
                "No predictions were made. Make sure that all models have been "
                "trained and that test data is available."
            )
            return self

        # Reindex predictions to match order of features + add nans if predictions are
        # missing for a chromosome
        y_pred = pd.concat(predictions).reindex(self.data.X.index)
        y_pred.name = None
        self.data.y_pred = y_pred
        return self

    def predict_from_weights(self, model_name: str, X: pd.DataFrame) -> pd.Series:
        df_weights = self._load_models_weights(
            self.prefix.join(pg_const.FileSuffix.WEIGHTS)
        )
        weights = df_weights[model_name].dropna()
        y_pred = (
            X
            # Add intercept
            .assign(INTERCEPT=1)
            # Reorder to match weights
            [weights.index]
            # dot product to get predictions per gene (row)
            .dot(weights)
        )
        return y_pred

    def save(self, prefix: pg_types.FilePrefix | None = None) -> TrainingManager:
        if prefix is None:
            prefix = self.prefix

        self._save_models_weights(prefix)

        # If models were used to make predictions, save those
        self._save_models_predicted_scores(prefix)
        return self

    def _save_models_weights(self, prefix: pg_types.FilePrefix) -> None:
        # Get all weights
        df_weights = self._extract_models_weights()

        # TODO: needs to be combined with existing weights

        if df_weights.empty:
            logger.warning("No weights were found. Skipping weights saving...")

        fname_weights = prefix.join(pg_const.FileSuffix.WEIGHTS)
        logger.info("Saving models weights to %s", fname_weights)

        save_multi_model_df(df_weights, fname_weights)

    def _extract_models_weights(self) -> pd.DataFrame:
        """
        Reads weights from the trained models in memory and returns them as a
        dataframe.
        """
        list_weights = []
        for name, model in self.models_dict.items():
            try:
                list_weights.append(model.get_weights().rename(name))
            except NotImplementedError:
                logger.warning(
                    "Model %s does not implement get_weights. Skipping it ...",
                    self.info.model.__name__,
                )
            except NotFittedError:
                logger.warning(
                    "Model %s has not been fitted. Skipping it ...",
                    self.info.model.__name__,
                )
        if len(list_weights) < 1:
            return pd.DataFrame(columns=self.models_dict.keys())
        df_weights = pd.concat(list_weights, axis=1)
        df_weights.index.name = pg_const.ColInternal.FEATURE
        return df_weights

    @staticmethod
    def _load_models_weights(f_existing_weights: Path) -> pd.DataFrame:
        if not f_existing_weights.is_file():
            raise FileNotFoundError(
                f"Could not find existing weights file {f_existing_weights}."
            )
        logger.info("Loading existing weights ...")
        return read_multi_model_df(
            f_existing_weights, index_col=pg_const.ColInternal.FEATURE
        )

    def _save_models_predicted_scores(self, prefix: pg_types.FilePrefix) -> None:
        if self.data.y_pred is None or self.data.y_pred.isna().all():
            logger.info("No models were used to calculate predicted score.")
            logger.info("Skipping predicted scores saving...")
            return

        data = self.data.genes_loc.join(
            pd.DataFrame(
                {
                    pg_const.ColInternal.SCORE: self.data._y,
                    pg_const.ColInternal.PRED: self.data.y_pred,
                }
            )
        ).reset_index()

        PERiGenePredictions(data).save(prefix.join(pg_const.FileSuffix.PRED_SCORES))

    def set_model_params_from_trial(
        self, trial_number: int, key_model: str
    ) -> TrainingManager:
        study = self.get_study(key_model)
        t = study.trials[trial_number]
        self.info.model_params[key_model] = t.params
        return self

    def train(self) -> TrainingManager:
        logger.info("Training models ...")
        for key_model, data in self.data:
            if IS_DEBUG_ON:
                logger.debug("--> Chromosome %s", key_model)
                X_train, _ = data[pg_types.DataSubsetCategory.TRAIN]
                logger.debug("Train features shape %i rows, %i columns", *X_train.shape)

            if key_model not in self.info.model_params:
                logger.warning(
                    "*** No parameters found for model %s in info file. ***", key_model
                )
                logger.warning(
                    "*** Hyperparameter tuning should be run before training. ***"
                )
                logger.warning("*** Using default parameters for now. ***")

                params = self.info.model.get_default_model_params()
                self.info.model_params[key_model] = params
            else:
                params = self.info.model_params[key_model]
            model = self.info.model(**params)
            model.fit(data)
            self.models_dict[key_model] = model

        return self
