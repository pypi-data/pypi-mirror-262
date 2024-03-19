import logging
import warnings
from collections.abc import Callable
from functools import partial
from typing import Any

import optuna
from optuna import Study, Trial

logger = logging.getLogger(__name__)
optuna.logging.enable_propagation()
optuna.logging.disable_default_handler()

STR_OPTUNA_COMPLETE = "COMPLETE"
COL_OPTUNA_DATETIME_COMPLETE = "datetime_complete"


def get_storage(fname_storage: str) -> optuna.storages.BaseStorage:
    from optuna.storages import JournalFileStorage, JournalStorage

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=optuna.exceptions.ExperimentalWarning)
        storage = JournalStorage(JournalFileStorage(fname_storage))
    logger.debug("Using storage %s", fname_storage)
    return storage


def get_study(fname_storage: str, study_name: str) -> Study:
    optuna.logging.enable_propagation()
    optuna.logging.disable_default_handler()

    storage = get_storage(fname_storage)
    logger.info("Accessing study %s in %s", study_name, fname_storage)
    study = optuna.create_study(
        study_name=study_name,
        storage=storage,
        load_if_exists=True,
    )
    return study


def delete_study(fname_storage: str, study_name: str) -> None:
    optuna.logging.enable_propagation()
    optuna.logging.disable_default_handler()

    storage = get_storage(fname_storage)
    try:
        study_id = storage.get_study_id_from_name(study_name)
        logger.debug("Deleting study %s in %s", study_name, fname_storage)
        storage.delete_study(study_id)
    except KeyError:
        # Do nothing if study does not exist
        ...


def check_early_stop(
    study: Study, trial: Trial, early_stopping_rounds: int = 50
) -> None:
    """
    Callback to stop the study if no progress has been made in the last
    `early_stopping_rounds` trials.
    """
    best_trial_nb = study.best_trial.number
    if trial.number == best_trial_nb:
        return

    # Get info on completed trials only
    d = study.trials_dataframe()
    d = (
        d.loc[d.state == STR_OPTUNA_COMPLETE]
        .sort_values(COL_OPTUNA_DATETIME_COMPLETE)
        .reset_index(drop=True)
    )

    # Not using d.value.idx_min() as it depends whether the study
    # minimizes or maximizes the objective value
    n_elapsed = d.index[-1] - d.index[d.number == best_trial_nb][0]

    if n_elapsed > early_stopping_rounds:
        logger.info("No progress in hyperparameter search, exiting early.")
        study.stop()


def tune_model_params(
    storage: str,
    study_name: str,
    objective: Callable,
    base_params: dict[str, Any],
    ntrials: int,
    reset_study: bool = False,
) -> dict[str, Any]:
    optuna.logging.enable_propagation()
    optuna.logging.disable_default_handler()

    if reset_study:
        delete_study(storage, study_name)

    study = get_study(storage, study_name)

    # Use default parameters as starting point for optimization
    study.enqueue_trial(base_params, skip_if_exists=True)
    study.optimize(
        objective,
        n_trials=ntrials,
        callbacks=[partial(check_early_stop, early_stopping_rounds=50)],
    )

    if logger.isEnabledFor(logging.INFO):
        logger.info("Best parameters after tuning:")
        for param, value in study.best_params.items():
            value = f"{value:.3e}" if isinstance(value, float) else value
            logger.info("%s: %s", param, value)

    return study.best_trial.params
