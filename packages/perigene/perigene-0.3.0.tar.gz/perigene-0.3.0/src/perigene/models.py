#!/usr/bin/python

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial
from typing import Any, ClassVar

import pandas as pd
import xgboost as xgb
from optuna import Trial
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import ElasticNet, Lasso, Ridge
from sklearn.model_selection import KFold, cross_val_score

from .perigene_types import (
    DataSubsetCategory,
    ModelData,
    ModelParameter,
    ModelParametersDict,
    SKModel,
    Task,
)

N_SPLITS_CV = 5


class Model(ABC):
    model: xgb.Booster | SKModel
    _default_model_params: ClassVar[ModelParametersDict]
    _task: ClassVar[Task]

    # property on class methods being deprecated in python 3.11, using old-fashined
    # getters
    @classmethod
    def get_default_model_params(cls) -> ModelParametersDict:
        return cls._default_model_params

    @classmethod
    def get_task(cls) -> Task:
        return cls._task

    @abstractmethod
    def fit(
        self,
        data: ModelData,
        **train_params: ModelParameter,
    ) -> None: ...

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> pd.Series: ...

    @abstractmethod
    def get_weights(self) -> pd.Series: ...

    @staticmethod
    @abstractmethod
    def query_trial_params(trial: Trial) -> ModelParametersDict: ...

    @classmethod
    @abstractmethod
    def get_objective(cls, X: pd.DataFrame, y: pd.Series) -> Callable[..., float]: ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class SklearnModel(Model):
    model: SKModel
    _constructor: ClassVar[type[SKModel]]

    @classmethod
    def make_skmodel(cls, **model_params: ModelParameter) -> SKModel:
        return cls._constructor(**model_params)

    def __init__(self, **model_params: ModelParameter) -> None:
        self.model = self.make_skmodel(**model_params)

    def fit(self, data: ModelData, **_: Any) -> None:
        self.model.fit(*data[DataSubsetCategory.TRAIN])

    def predict(self, X: pd.DataFrame) -> pd.Series:
        return pd.Series(self.model.predict(X), index=X.index)

    def get_weights(self) -> pd.Series:
        try:
            w_intercept = pd.Series(self.model.intercept_, index=["INTERCEPT"])
            w_features = pd.Series(self.model.coef_, index=self.model.feature_names_in_)
        except AttributeError as e:
            raise NotFittedError(
                "Could not get intercept and coefficients from model. "
                "Make sure the model has been fitted before calling this method."
            ) from e
        return pd.concat([w_intercept, w_features])

    @classmethod
    def get_objective(cls, X: pd.DataFrame, y: pd.Series) -> Callable[..., float]:
        def objective(trial: Trial) -> float:
            m = cls.make_skmodel(**cls.query_trial_params(trial))

            score = "neg_root_mean_squared_error"
            cv = KFold

            # Note: Optuna tries to minimize the objective fct
            # -> return the log loss or the RMSE, not the neg of those values
            scores = -cross_val_score(
                m,
                X,
                y,
                scoring=score,
                cv=cv(n_splits=N_SPLITS_CV, shuffle=True),
            )
            return scores.mean()

        return objective


class XGBModel(Model):
    model: xgb.Booster

    def __init__(self, *, num_boost_round: int, **model_params: ModelParameter) -> None:
        self.num_boost_round = num_boost_round
        self.model_params = model_params

    @staticmethod
    def suggest_xgb_params(trial: Trial) -> ModelParametersDict:
        return {
            "eta": trial.suggest_float("eta", 1e-6, 1, log=True),
            "alpha": trial.suggest_float("alpha", 1e-6, 1, log=True),
            "lambda": trial.suggest_float("lambda", 1e-6, 1, log=True),
            "gamma": trial.suggest_float("gamma", 1e-6, 20, log=True),
            "num_boost_round": trial.suggest_int("num_boost_round", 10, 500, step=10),
            "max_depth": trial.suggest_int("max_depth", 3, 12),
            "grow_policy": str(
                trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])
            ),  # force string instead of optuna's CategoricalChoiceType
            "max_leaves": trial.suggest_int("max_leaves", 10, 500),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0, log=True),
            "colsample_bytree": trial.suggest_float(
                "colsample_bytree", 0.6, 1.0, log=True
            ),
        }

    def fit(
        self,
        data: ModelData,
        **train_params: ModelParameter,
    ) -> None:
        X_train, y_train = data[DataSubsetCategory.TRAIN]
        X_eval, y_eval = data[DataSubsetCategory.TEST]

        assert X_train.index.equals(y_train.index)
        assert X_eval.index.equals(y_eval.index)

        D_train = xgb.DMatrix(X_train, y_train)
        D_valid = xgb.DMatrix(X_eval, y_eval)

        m = xgb.train(
            self.model_params,
            D_train,
            num_boost_round=self.num_boost_round,
            evals=[(D_train, "Train"), (D_valid, "Valid")],
            early_stopping_rounds=20,
            verbose_eval=False,
        )
        self.model = m

    def predict(self, X: pd.DataFrame) -> pd.Series:
        D_test = xgb.DMatrix(X)
        return pd.Series(self.model.predict(D_test), index=X.index)

    def get_weights(self) -> pd.Series:
        raise NotImplementedError("XGBModels do not support get_weights() method")

    @classmethod
    def get_objective(cls, X: pd.DataFrame, y: pd.Series) -> Callable[..., float]:
        def objective(trial: Trial, *, X: pd.DataFrame, y: pd.Series) -> float:
            params = cls.get_default_model_params()
            params.update(cls.query_trial_params(trial))
            num_boost_round = params.pop("num_boost_round")

            assert isinstance(num_boost_round, int)
            score = "rmse"
            stratified = False
            D_train = xgb.DMatrix(X, y)
            scores = xgb.cv(
                params,
                D_train,
                metrics=score,
                num_boost_round=num_boost_round,
                nfold=10,
                stratified=stratified,
                early_stopping_rounds=20,
                verbose_eval=False,
            )
            scores_cv = scores[f"test-{score}-mean"]
            return pd.Series(scores_cv).mean()

        return partial(objective, X=X, y=y)


class ElasticNetRegression(SklearnModel):
    _constructor = ElasticNet
    _default_model_params = dict(alpha=10, l1_ratio=0.5)
    _task = Task.REGRESSION

    @staticmethod
    def query_trial_params(trial: Trial) -> ModelParametersDict:
        return dict(
            alpha=trial.suggest_float("alpha", 1e-3, 1e6, log=True),
            l1_ratio=trial.suggest_float("l1_ratio", 1e-4, 1, log=True),
        )


class LassoRegression(SklearnModel):
    _constructor = Lasso
    _default_model_params = dict(alpha=10)
    _task = Task.REGRESSION

    @staticmethod
    def query_trial_params(trial: Trial) -> ModelParametersDict:
        return dict(
            alpha=trial.suggest_float("alpha", 1e-3, 1e6, log=True),
        )


class RidgeRegression(SklearnModel):
    _constructor = Ridge
    _default_model_params = dict(alpha=10)
    _task = Task.REGRESSION

    @staticmethod
    def query_trial_params(trial: Trial) -> ModelParametersDict:
        return dict(alpha=trial.suggest_float("alpha", 1e-3, 1e6, log=True))


class XGBRegression(XGBModel):
    _default_model_params = dict(
        booster="gbtree",
        tree_method="hist",
        objective="reg:squarederror",
        num_boost_round=50,
        eta=0.05,
        max_depth=6,
        verbosity=0,
    )
    _task = Task.REGRESSION

    @staticmethod
    def query_trial_params(trial: Trial) -> ModelParametersDict:
        return XGBRegression.suggest_xgb_params(trial)


# WARNING: remember to update these keys in the shared CLI params!
MODELS_STR_MAP: dict[str, type[Model]] = {
    "reg-lasso": LassoRegression,
    "reg-ridge": RidgeRegression,
    "reg-elasticnet": ElasticNetRegression,
    "reg-gb": XGBRegression,
}
