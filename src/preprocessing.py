"""
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Module: Preprocessing
Handles categorical frequency encoding, NaN/Inf cleaning, scaling, and array alignment.
"""

import numpy as np
import pandas as pd
from typing import List, Tuple, Dict


def clean_missing_values(df: pd.DataFrame, num_cols: List[str]) -> pd.DataFrame:
    """
    Replaces infinity values with NaN and fills missing values in numeric columns with median.
    """
    df = df.copy()
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].replace([np.inf, -np.inf], np.nan)
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val if pd.notna(median_val) else 0)
    return df


def apply_frequency_encoding(
    train_df: pd.DataFrame, 
    test_df: pd.DataFrame, 
    cat_cols: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Dict]]:
    """
    Applies frequency encoding (out-of-fold safe representation) for categorical variables.
    """
    train_df = train_df.copy()
    test_df = test_df.copy()
    freq_maps = {}

    for col in cat_cols:
        if col in train_df.columns:
            freq = train_df[col].value_counts(normalize=True).to_dict()
            freq_maps[col] = freq
            
            train_df[f"{col}_freq"] = train_df[col].map(freq).fillna(0).astype(np.float32)
            test_df[f"{col}_freq"] = test_df[col].map(freq).fillna(0).astype(np.float32)

    return train_df, test_df, freq_maps


def convert_categories(df: pd.DataFrame, cat_cols: List[str]) -> pd.DataFrame:
    """
    Converts object columns to pandas category dtype for native tree handling (LightGBM/CatBoost).
    """
    df = df.copy()
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")
    return df
