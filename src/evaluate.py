"""
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Module: Evaluate
Metrics, Jensen's inequality multiplier adjustment, and log-space ensemble blending.
"""

import numpy as np
from sklearn.metrics import mean_squared_log_error


def calculate_rmsle(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Computes Root Mean Squared Logarithmic Error (RMSLE).
    Ensures negative predictions are clipped to 0.
    """
    y_pred_clipped = np.clip(y_pred, 0, None)
    return float(np.sqrt(mean_squared_log_error(y_true, y_pred_clipped)))


def blend_predictions(
    preds_xgb: np.ndarray,
    preds_lgb: np.ndarray,
    preds_cat: np.ndarray,
    weights: Tuple[float, float, float] = (0.45, 0.35, 0.20)
) -> np.ndarray:
    """
    Blends predictions across models in log-space to optimize RMSLE objective.
    """
    w1, w2, w3 = weights
    log_xgb = np.log1p(np.clip(preds_xgb, 0, None))
    log_lgb = np.log1p(np.clip(preds_lgb, 0, None))
    log_cat = np.log1p(np.clip(preds_cat, 0, None))

    blended_log = w1 * log_xgb + w2 * log_lgb + w3 * log_cat
    return np.expm1(blended_log)


def apply_jensens_multiplier(preds: np.ndarray, multiplier: float = 1.001300) -> np.ndarray:
    """
    Applies empirical Jensen's Inequality bias adjustment multiplier (1.001300)
    for log-transformed variance restoration before final output formatting.
    """
    return np.clip(preds * multiplier, 0, None)
