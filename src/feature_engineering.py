"""
🄯 Copyleft 2026 Ramrup Satpati | All Rights Reversed.
Released under the GNU General Public License v3.0 (GPLv3).

Module: Feature Engineering
Extracts temporal features, regex physical spec sizing (HP, tonnage, yardage), and non-linear depreciation ratios.
"""

import re
import numpy as np
import pandas as pd
from typing import Tuple


def extract_date_features(X: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extracts temporal features (Sale Year, Sale Month, Unix Epoch) from datetime columns.
    """
    X = X.copy()
    X_test = X_test.copy()

    for col in X.columns:
        if col.lower() in ['saledate', 'date', 'time'] or 'date' in col.lower() or 'time' in col.lower():
            try:
                train_date = pd.to_datetime(X[col], errors='coerce')
                test_date = pd.to_datetime(X_test[col], errors='coerce')
                if train_date.notnull().sum() > 0:
                    for df, date_series in [(X, train_date), (X_test, test_date)]:
                        df[f'{col}_year'] = date_series.dt.year
                        df[f'{col}_epoch'] = pd.to_numeric(date_series, errors='coerce') // 10**9
            except Exception:
                pass
    return X, X_test


def extract_capacity_metrics(X: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parses physical machinery sizing indicators (horsepower, tonnage, yardage) using regular expressions.
    """
    X = X.copy()
    X_test = X_test.copy()

    cat_cols = list(X.select_dtypes(exclude=[np.number]).columns)
    for col in cat_cols:
        sample_vals = X[col].dropna().unique()[:1000].astype(str).tolist()
        has_sizing = any(re.search(r'\b\d+(?:\.\d+)?\s*(?:hp|horsepower|metric tons|tons|lbs|yards|yd|kw|lbs)\b', val.lower()) for val in sample_vals)
        if has_sizing:
            for df in [X, X_test]:
                first_num = df[col].astype(str).str.extract(r'(\d+(?:\.\d+)?)\s*(?:to|-|\b)').astype(float)
                second_num = df[col].astype(str).str.extract(r'(?:to|-)\s*(\d+(?:\.\d+)?)').astype(float)
                df[f'{col}_size_min'] = first_num[0]
                df[f'{col}_size_max'] = second_num[0]
                df[f'{col}_size_mean'] = df[[f'{col}_size_min', f'{col}_size_max']].mean(axis=1)
    return X, X_test


def build_depreciation_interactions(X: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculates physical depreciation metrics and non-linear age/usage interactions.
    """
    X = X.copy()
    X_test = X_test.copy()

    for df in [X, X_test]:
        df['missing_count'] = df.isnull().sum(axis=1)
        
        if 'age_at_sale' in df.columns and 'OperationalHoursMeter' in df.columns:
            hours = df['OperationalHoursMeter'].clip(0, 1e9)
            age = df['age_at_sale'].clip(0, 100)
            decade = df.get('machine_decade', 2000).clip(1800, 2100)
            
            df['hours_age_ratio'] = hours / (age + 1)
            df['log_hours_age_ratio'] = np.log1p(hours) / (age + 1)
            df['age_hours_sq'] = (age ** 2) * hours
            df['hours_per_year'] = hours / (age + 1)
            df['high_usage'] = (hours > 5000).astype(int)
            df['log_hours'] = np.log1p(hours)
            df['log_age'] = np.log1p(age)
            df['age_sq'] = age ** 2
            df['age_cu'] = age ** 3
            df['hours_sq'] = hours ** 2
            df['utilization_density'] = hours / (decade - 1800 + 1)
            df['log_hours_per_year'] = np.log1p(df['hours_per_year'])
            
        if 'fiModelDesc' in df.columns:
            df['model_size'] = df['fiModelDesc'].astype(str) + '_' + df.get('ProductSize', 'NA').astype(str)
            
    return X, X_test
