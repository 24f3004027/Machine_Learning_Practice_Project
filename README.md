# 🚜 Heavy Equipment Price Prediction: Multi-Seed GBDT Ensemble Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-Hist%20GBDT-111111?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-Leaf--Wise-28A745?style=for-the-badge&logo=lightgbm&logoColor=white)](https://lightgbm.readthedocs.io)
[![CatBoost](https://img.shields.io/badge/CatBoost-Ordered%20Encoding-000000?style=for-the-badge&logo=catboost&logoColor=white)](https://catboost.ai)
[![Grade](https://img.shields.io/badge/Final%20Score-90.00%20%2F%20100-success?style=for-the-badge&logo=iitm&color=10b981)](https://study.iitm.ac.in)
[![Grade Letter](https://img.shields.io/badge/Grade-S%20(10.0%20GPA)-gold?style=for-the-badge)](https://study.iitm.ac.in)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)

An end-to-end Machine Learning pipeline designed to predict heavy machinery auction selling prices. Developed as part of the **Machine Learning Practice (MLP) Project** course in the **IIT Madras BS in Data Science & Applications** program, achieving a final course score of **90.00/100 (Grade S - 10.0 GPA)**.

---

## 📌 Executive Summary

Predicting heavy equipment valuation requires modeling non-linear physical depreciation, temporal economic shifts, and high-cardinality nominal descriptions. This repository implements:

1. **Domain-Specific Feature Engineering**: Temporal extraction (epochs/years), regex-based physical capacity parsing (horsepower, tonnage, yardage), and non-linear usage-to-age depreciation ratios.
2. **Native Categorical Processing**: Frequency encoding and pandas `category` dtype mapping for memory-efficient GBDT binning without high-cardinality dimensionality explosion.
3. **5-Seed Multifold GBDT Ensembling**: A 3-way weighted ensemble combining **Deep XGBoost** ($75\%$), **LightGBM** ($10\%$), and **CatBoost** ($15\%$) trained across 5 random seeds to cancel out tree variance.
4. **Jensen's Inequality Bias Correction**: Log-space prediction averaging followed by exponential transformation (`expm1`) and scalar multiplier tuning (`1.001300`) to correct for the systematic downward prediction bias of log-transformed targets.

---

## 🏗️ Pipeline Architecture

```mermaid
graph TD
    subgraph 1. Raw Dataset & Preprocessing
        RawData["Raw Heavy Machinery Dataset"] --> DateParse["1. Temporal Extractor<br/>(Year & Unix Epoch)"]
        DateParse --> CapacityParse["2. Regex Sizing Parser<br/>(Horsepower, Tons, Yardage)"]
        CapacityParse --> DepRatios["3. Depreciation Ratios<br/>(Hours/Age, Log Ratios, Quadratic Age)"]
        DepRatios --> CatFreq["4. Frequency & Category Dtype Encoding"]
    end

    subgraph 2. Validation & Model Training
        CatFreq --> ValSplit["85 / 15 Train-Validation Split"]
        ValSplit --> SeedLoop["5-Seed Training Loop<br/>(Seeds: 42, 2025, 7, 999, 1984)"]
        
        SeedLoop --> DeepXGB["Deep XGBoost (75%)<br/>(Max Depth 11, lr 0.025, reg_lambda 5.0)"]
        SeedLoop --> LGBM["LightGBM Regressor (10%)<br/>(Max Depth 9, num_leaves 128)"]
        SeedLoop --> CatB["CatBoost Regressor (15%)<br/>(Depth 6, l2_leaf_reg 5)"]
    end

    subgraph 3. Blending & Bias Correction
        DeepXGB --> LogBlend["Weighted Log-Space Average"]
        LGBM --> LogBlend
        CatB --> LogBlend
        
        LogBlend --> Antilog["expm1 Inverse Transformation"]
        Antilog --> Multiplier["Jensen's Inequality Multiplier<br/>(1.001300)"]
        Multiplier --> BoundaryClip["Boundary Envelope Clipping"]
        BoundaryClip --> FinalSub["Final Submission Output<br/>(submission.csv)"]
    end
```

---

## 📊 Key Results & Model Performance

| Model Architecture | Features Used | Validation RMSLE | Kaggle Public Leaderboard |
| :--- | :--- | :---: | :---: |
| **Baseline LightGBM** | Default features | `0.19420` | ~`0.1925` |
| **Shallow XGBoost (Depth 13)** | Basic ratios + frequency | `0.19050` | ~`0.1895` |
| **LightGBM (Depth 14, Leaves 512)** | Full interaction set | `0.18950` | ~`0.1888` |
| **Deep XGBoost (Depth 17)** | High-depth interaction trees | `0.18880` | ~`0.1872` |
| **Production 3-Way GBDT Ensemble** | 5-seed blend + multiplier | **`0.18663`** | **`0.1855`** |

---

## 🛠️ Repository Structure

```text
Machine_Learning_Practice_Project/
├── README.md                           # Main Project Documentation
├── LICENSE                             # GNU GPLv3 Copyleft License
├── requirements.txt                    # Python dependencies
├── docs/                               # GitHub Pages Landing Page
│   ├── index.html
│   └── style.css
├── notebooks/                          # Production Jupyter Notebooks
│   └── MLP_Production_Pipeline.ipynb   # Complete 5-Stage GBDT Ensemble Notebook
└── src/                                # Modular Python Source Code
    ├── __init__.py
    ├── feature_engineering.py          # Temporal & Capacity extraction logic
    ├── preprocessing.py                # Categorical encoding & cleaning
    ├── models.py                       # GBDT hyperparameter dictionaries
    └── evaluate.py                     # Metric calculation & multiplier tuning
```

---

## ⚙️ Environment Setup & Installation

```bash
# Clone the repository
git clone https://github.com/24f3004027/Machine_Learning_Practice_Project.git
cd Machine_Learning_Practice_Project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🄯 License & Open Source Ethos

Released under the **GNU General Public License v3.0 (GPLv3)**.

```text
🄯 Copyleft 2026 Ramrup Satpati (Roll No: 24f3004027). All Rights Reversed.
Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies of this license document.
```
