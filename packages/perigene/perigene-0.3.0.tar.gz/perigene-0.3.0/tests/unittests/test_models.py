#!/usr/bin/env python

from perigene import models
from perigene.perigene_types import Task


def test_ElasticNetRegression_valid_class_attributes():
    # arrange
    cls_ = models.ElasticNetRegression
    # act
    default_params = cls_.get_default_model_params()
    task = cls_.get_task()
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "alpha" in default_params


def test_ElasticNetRegression_init():
    from sklearn.linear_model import ElasticNet

    # arrange
    expected_alpha = 0.5
    m = models.ElasticNetRegression(alpha=expected_alpha)
    # act
    default_params = m.get_default_model_params()
    task = m.get_task()
    model = m.model
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "alpha" in default_params
    assert isinstance(model, ElasticNet)
    assert model.alpha == expected_alpha


def test_LassoRegression_valid_class_attributes():
    # arrange
    cls_ = models.LassoRegression
    # act
    default_params = cls_.get_default_model_params()
    task = cls_.get_task()
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "alpha" in default_params


def test_LassoRegression_init():
    from sklearn.linear_model import Lasso

    # arrange
    expected_alpha = 0.5
    m = models.LassoRegression(alpha=expected_alpha)
    # act
    default_params = m.get_default_model_params()
    task = m.get_task()
    model = m.model
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "alpha" in default_params
    assert isinstance(model, Lasso)
    assert model.alpha == expected_alpha


def test_RidgeRegression_valid_class_attributes():
    # arrange
    cls_ = models.RidgeRegression
    # act
    default_params = cls_.get_default_model_params()
    task = cls_.get_task()
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "alpha" in default_params


def test_RidgeRegression_init():
    from sklearn.linear_model import Ridge

    # arrange
    expected_alpha = 0.5
    # act
    m = models.RidgeRegression(alpha=expected_alpha)
    default_params = m.get_default_model_params()
    task = m.get_task()
    model = m.model
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "alpha" in default_params
    assert isinstance(model, Ridge)
    assert model.alpha == expected_alpha


def test_XGBRegression_valid_class_attributes():
    # arrange
    cls_ = models.XGBRegression
    # act
    default_params = cls_.get_default_model_params()
    task = cls_.get_task()
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "num_boost_round" in default_params


def test_XGBRegression_init():
    # arrange
    expected_num_boost_round = 1
    m = models.XGBRegression(num_boost_round=expected_num_boost_round)
    # act
    default_params = m.get_default_model_params()
    task = m.get_task()
    # assert
    assert task == Task.REGRESSION
    assert isinstance(default_params, dict)
    assert "num_boost_round" in default_params
    assert m.num_boost_round == expected_num_boost_round
