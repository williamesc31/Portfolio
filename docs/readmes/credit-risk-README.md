# Credit Risk Default Prediction

## Overview

This project predicts loan default using borrower and loan-application information. It compares logistic regression with a tuned Random Forest.

## Data and methods

The project uses the Kaggle Credit Risk Dataset (`credit_risk_dataset.csv`). The target is `loan_status` (0 = non-default, 1 = default). The workflow includes numerical and categorical imputation, log transformations where appropriate, scaling, one-hot encoding, and a scikit-learn ColumnTransformer/pipeline. Engineered features include `loan_to_income` and `emp_to_age`.

## Previously reported evaluation

| Model | Evaluation | Value |
| --- | --- | --- |
| Logistic regression | Test accuracy | 81.8% |
| Logistic regression | Test ROC-AUC | 0.877 |
| Logistic regression | Default-class recall | 79.2% |
| Tuned Random Forest | Five-fold CV ROC-AUC | 0.9331 |
| Tuned Random Forest | Test accuracy | 93.4% |

These values were reported in the earlier project and must be reconciled with the final saved notebook outputs. Cross-validation and test ROC-AUC are different evaluations. Default-class precision, recall, F1-score, and confusion matrices are important because the dataset is imbalanced.

## Reproduction status

The repository URL, dataset source link, notebook path, package versions, and tested commands will be added after the project files are organized and verified. No fresh execution check is claimed by this draft. Preprocessing must be fitted on training data and applied consistently to held-out data.

## Tools

Python, pandas, NumPy, scikit-learn, Matplotlib, Jupyter Notebook.

## Limitations and next steps

Performance on one dataset does not establish reliability on another lending population. Possible extensions include probability calibration, cost-sensitive thresholds, subgroup evaluation, gradient boosting, and explanations of individual predictions.
