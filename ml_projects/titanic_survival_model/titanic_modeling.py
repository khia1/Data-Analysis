"""
Titanic Survival Modeling Project
Author: Khia1

Goal:
Clean dataset, perform exploratory analysis, and compare:
- K Nearest Neighbors
- Logistic Regression
- Decision Tree

NOTE:
The dataset (TrainData.csv) is intentionally NOT included in this repository.
To run locally, place TrainData.csv in the same folder as this script.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


# -------------------------
# Utility Functions
# -------------------------

def load_data(filepath: str) -> pd.DataFrame:
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"\nMissing dataset: {filepath}\n"
            "This repository does not include the CSV dataset.\n"
            "Place TrainData.csv in this folder to run the project.\n"
        )

    df = pd.read_csv(path)
    print("Shape of data:", df.shape)
    return df


def save_plot(filename: str):
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(outputs_dir / filename, dpi=300, bbox_inches="tight")


# -------------------------
# Data Cleaning
# -------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["station"])

    median_age = df["age"].median()
    df["age"] = df["age"].fillna(median_age)

    print("New shape after cleaning:", df.shape)
    print("Missing values after cleaning:\n", df.isnull().sum())
    return df


def treat_outliers(df: pd.DataFrame) -> pd.DataFrame:
    fare_cap = df["fare"].quantile(0.99)
    df["fare"] = df["fare"].clip(upper=fare_cap)

    print("Fare cap value used:", fare_cap)
    return df


# -------------------------
# Preprocessing + Split
# -------------------------

def build_preprocessor():
    cat_cols = ["sex", "station"]
    num_cols = ["pclass", "age", "sibsp", "parch", "fare"]

    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )


def split_data(df: pd.DataFrame):
    X = df.drop("survived", axis=1)
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=12345
    )

    print("Training set size:", X_train.shape)
    print("Testing set size:", X_test.shape)

    return X_train, X_test, y_train, y_test


# -------------------------
# Model Evaluation
# -------------------------

def evaluate_knn(preprocessor, X_train, X_test, y_train, y_test):
    accuracies = {}

    for k in range(1, 31):
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("knn", KNeighborsClassifier(n_neighbors=k))
        ])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracies[k] = accuracy_score(y_test, y_pred)

    best_k = max(accuracies, key=accuracies.get)
    print("Best k:", best_k)
    print("Best KNN accuracy:", accuracies[best_k])
    return accuracies[best_k]


def evaluate_logreg(preprocessor, X_train, X_test, y_train, y_test):
    model = Pipeline([
        ("preprocessor", preprocessor),
        ("logreg", LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("Logistic Regression accuracy:", acc)
    return acc


def evaluate_tree(preprocessor, X_train, X_test, y_train, y_test):
    accuracies = {}

    for depth in range(1, 21):
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("tree", DecisionTreeClassifier(max_depth=depth, random_state=12345))
        ])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracies[depth] = accuracy_score(y_test, y_pred)

    best_depth = max(accuracies, key=accuracies.get)
    print("Best tree depth:", best_depth)
    print("Best Decision Tree accuracy:", accuracies[best_depth])
    return accuracies[best_depth]


# -------------------------
# EDA Plots
# -------------------------

def eda_plots(df: pd.DataFrame):

    plt.figure(figsize=(7,5))
    sns.histplot(df["age"], bins=30, kde=True)
    plt.title("Age Distribution")
    plt.xlabel("Age")
    plt.ylabel("Count")
    save_plot("age_distribution.png")
    plt.show()

    plt.figure(figsize=(7,5))
    sns.histplot(df["fare"], bins=30, kde=True)
    plt.title("Fare Distribution")
    plt.xlabel("Fare")
    plt.ylabel("Count")
    save_plot("fare_distribution.png")
    plt.show()

    plt.figure(figsize=(7,5))
    sns.countplot(x="survived", data=df)
    plt.title("Survival Count")
    plt.xlabel("Survived (0 = No, 1 = Yes)")
    plt.ylabel("Count")
    save_plot("survival_count.png")
    plt.show()

    plt.figure(figsize=(7,5))
    sns.countplot(x="pclass", hue="survived", data=df)
    plt.title("Survival by Passenger Class")
    plt.xlabel("Passenger Class")
    plt.ylabel("Count")
    save_plot("survival_by_class.png")
    plt.show()

    plt.figure(figsize=(7,5))
    sns.countplot(x="sex", hue="survived", data=df)
    plt.title("Survival by Sex")
    plt.xlabel("Sex")
    plt.ylabel("Count")
    save_plot("survival_by_sex.png")
    plt.show()


# -------------------------
# Main Execution
# -------------------------

def main():

    df = load_data("TrainData.csv")

    print("\nINFO")
    print(df.info())

    print("\nDESCRIBE")
    print(df.describe())

    print("\nUNIQUE VALUES PER COLUMN")
    print(df.nunique())

    print("\nMost common station:")
    print(df["station"].value_counts())

    df = clean_data(df)

    # Outlier visualization
    plt.figure(figsize=(12,5))

    plt.subplot(1,2,1)
    sns.boxplot(x=df["age"])
    plt.title("Age Outliers")

    plt.subplot(1,2,2)
    sns.boxplot(x=df["fare"])
    plt.title("Fare Outliers")

    save_plot("outlier_check.png")
    plt.show()

    df = treat_outliers(df)

    preprocessor = build_preprocessor()
    X_train, X_test, y_train, y_test = split_data(df)

    knn_acc = evaluate_knn(preprocessor, X_train, X_test, y_train, y_test)
    log_acc = evaluate_logreg(preprocessor, X_train, X_test, y_train, y_test)
    tree_acc = evaluate_tree(preprocessor, X_train, X_test, y_train, y_test)

    print("\nMODEL ACCURACY SUMMARY")
    print("------------------------")
    print("KNN Best Accuracy:", knn_acc)
    print("Logistic Regression Accuracy:", log_acc)
    print("Decision Tree Best Accuracy:", tree_acc)

    eda_plots(df)


if __name__ == "__main__":
    main()
