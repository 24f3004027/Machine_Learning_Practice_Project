"""
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Module: Models
Defines gradient boosting configurations for XGBoost, LightGBM, and CatBoost.
"""

from typing import Dict, Any


def get_xgb_params(seed: int = 42) -> Dict[str, Any]:
    """Returns production hyperparameters for Deep XGBoost Regressor."""
    return {
        "n_estimators": 2500,
        "learning_rate": 0.015,
        "max_depth": 9,
        "subsample": 0.85,
        "colsample_bytree": 0.75,
        "min_child_weight": 5,
        "gamma": 0.1,
        "reg_alpha": 0.5,
        "reg_lambda": 1.5,
        "random_state": seed,
        "n_jobs": -1,
        "tree_method": "hist"
    }


def get_lgb_params(seed: int = 42) -> Dict[str, Any]:
    """Returns production hyperparameters for LightGBM Regressor."""
    return {
        "n_estimators": 3000,
        "learning_rate": 0.012,
        "num_leaves": 127,
        "max_depth": -1,
        "subsample": 0.80,
        "colsample_bytree": 0.70,
        "min_child_samples": 20,
        "reg_alpha": 0.8,
        "reg_lambda": 2.0,
        "random_state": seed,
        "n_jobs": -1,
        "verbose": -1
    }


def get_catboost_params(seed: int = 42) -> Dict[str, Any]:
    """Returns production hyperparameters for CatBoost Regressor."""
    return {
        "iterations": 2500,
        "learning_rate": 0.02,
        "depth": 8,
        "l2_leaf_reg": 3.0,
        "random_strength": 0.1,
        "bagging_temperature": 0.2,
        "random_seed": seed,
        "verbose": 0
    }
