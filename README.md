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
3. **5-Seed Multifold GBDT Ensembling**: A 3-way weighted ensemble combining **Deep XGBoost** ($45\%$), **LightGBM** ($35\%$), and **CatBoost** ($20\%$) trained across 5 random seeds to cancel out tree variance.
4. **Jensen's Inequality Bias Correction**: Log-space prediction averaging followed by exponential transformation (`expm1`) and scalar multiplier tuning (`1.001300`) to correct for the systematic downward prediction bias of log-transformed targets.

---

## 🏗️ Milestone Development & Git Branch History

| Milestone | Feature Branch | Notebook File | Objective |
| :--- | :--- | :--- | :--- |
| **Milestone 1** | `feature/milestone-1-eda` | [`01_Exploratory_Data_Analysis.ipynb`](notebooks/01_Exploratory_Data_Analysis.ipynb) | Exploratory Data Analysis & Target Log-Distribution Modeling |
| **Milestone 2** | `feature/milestone-2-spec-parsing` | [`02_Spec_Parsing_And_Baselines.ipynb`](notebooks/02_Spec_Parsing_And_Baselines.ipynb) | Regex Physical Specification Parsing & Baseline Models |
| **Milestone 3** | `feature/milestone-3-feature-engineering` | [`03_Feature_Engineering_And_Encoding.ipynb`](notebooks/03_Feature_Engineering_And_Encoding.ipynb) | Domain Feature Engineering & Out-of-Fold Frequency Encoding |
| **Milestone 4** | `feature/milestone-4-model-tuning` | [`04_Multi_Model_Gradient_Boosting.ipynb`](notebooks/04_Multi_Model_Gradient_Boosting.ipynb) | Multi-Model GBDT Hyperparameter Tuning (XGBoost, LGBM, CatBoost) |
| **Milestone 5** | `feature/milestone-5-ensemble-jensen` | [`05_Production_Ensemble_And_Jensens_Multiplier.ipynb`](notebooks/05_Production_Ensemble_And_Jensens_Multiplier.ipynb) | 5-Seed Log-Space Blending & Jensen's Multiplier (`1.001300`) |

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
        ValSplit --> SeedLoop["5-Seed Training Loop<br/>(Seeds: 42, 100, 2026, 777, 999)"]
        
        SeedLoop --> DeepXGB["Deep XGBoost (45%)<br/>(Max Depth 9, lr 0.015)"]
        SeedLoop --> LGBM["LightGBM Regressor (35%)<br/>(Num Leaves 127, lr 0.012)"]
        SeedLoop --> CatB["CatBoost Regressor (20%)<br/>(Depth 8, lr 0.02)"]
    end

    subgraph 3. Blending & Bias Correction
        DeepXGB --> LogBlend["Weighted Log-Space Average"]
        LGBM --> LogBlend
        CatB --> LogBlend
        
        LogBlend --> Antilog["expm1 Inverse Transformation"]
        Antilog --> Multiplier["Jensen's Inequality Multiplier<br/>(1.001300)"]
        Multiplier --> BoundaryClip["Boundary Envelope Clipping"]
        BoundaryClip --> FinalSub["Final Submission Output"]
    end
```

---

## 📊 Key Results & Model Performance

| Model Architecture | Features Used | Validation RMSLE | Status |
| :--- | :--- | :---: | :---: |
| **Baseline Random Forest** | Default features | `0.24510` | Baseline |
| **Tuned LightGBM (Single Seed)** | Basic ratios + frequency | `0.19840` | Single Model |
| **Deep XGBoost Regressor (Depth 9)** | Full interaction set | `0.19120` | Single Model |
| **Production 3-Way 5-Seed Ensemble** | 5-seed blend + Jensen multiplier | **`0.18663`** | **Production Best** |

---

## 🛠️ Repository Structure

```text
Machine_Learning_Practice_Project/
├── README.md                           # Main Project Documentation
├── LICENSE                             # GNU GPLv3 Copyleft License
├── .gitignore                          # Git Exclusion Rules
├── requirements.txt                    # Python dependencies
├── docs/                               # GitHub Pages Landing Page
│   ├── index.html
│   └── style.css
├── notebooks/                          # Production Jupyter Notebooks (Milestones 1-5)
│   ├── 01_Exploratory_Data_Analysis.ipynb
│   ├── 02_Spec_Parsing_And_Baselines.ipynb
│   ├── 03_Feature_Engineering_And_Encoding.ipynb
│   ├── 04_Multi_Model_Gradient_Boosting.ipynb
│   ├── 05_Production_Ensemble_And_Jensens_Multiplier.ipynb
│   └── MLP_Production_Pipeline.ipynb
└── src/                                # Modular Python Source Code
    ├── __init__.py
    ├── feature_engineering.py          # Temporal & Capacity extraction logic
    ├── preprocessing.py                # Categorical encoding & cleaning
    ├── models.py                       # GBDT hyperparameter dictionaries
    └── evaluate.py                     # Metric calculation & multiplier tuning
```

---

## 📜 Copyleft License

🄯 **Copyleft 2026 Ramrup Satpati | All Rights Reversed**  
This project is released under the **GNU General Public License v3.0 (GPLv3)**. You are free to inspect, run, modify, and distribute this codebase as long as all derived works remain open-source under GPLv3.
