# Titanic Survival Modeling Project

## Objective
This project demonstrates a complete supervised machine learning workflow:
- Data inspection
- Missing value treatment
- Outlier handling
- Feature preprocessing
- Model comparison

The goal is to predict passenger survival using structured features.

---

## Dataset

The dataset file (TrainData.csv) is not included in this repository
for licensing and class policy reasons.

To run locally:
1. Place TrainData.csv in this folder.
2. Run: python titanic_modeling.py

---

## Data Cleaning Strategy

• Dropped rows with missing station values (very small count)  
• Filled missing age values with the median (robust to skew)  
• Capped fare values at the 99th percentile to reduce extreme outlier influence  

---

## Feature Engineering

Categorical:
- sex
- station

Numerical:
- pclass
- age
- sibsp
- parch
- fare

OneHotEncoding was applied to categorical variables with drop='first'
to avoid multicollinearity.

---

## Models Compared

1. K Nearest Neighbors (k = 1 to 30 tested)
2. Logistic Regression
3. Decision Tree (depth = 1 to 20 tested)

Accuracy was used as the evaluation metric.

---

## Output

Charts are automatically saved in the /outputs folder:
- Age distribution
- Fare distribution
- Survival count
- Survival by class
- Survival by sex

---

## Key Insight

Tree-based and linear models provide different bias-variance tradeoffs.
Comparing multiple model types helps validate robustness of findings.

---

Author: Khia1
