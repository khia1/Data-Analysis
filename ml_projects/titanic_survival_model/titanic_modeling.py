"""
Titanic Survival Modeling Project
Author: Kati

Goal:
Clean the dataset, perform basic exploratory checks, and compare:
- K-Nearest Neighbors
- Logistic Regression
- Decision Tree

NOTE:
The dataset (TrainData.csv) is intentionally NOT included in this repository.
To run locally, place TrainData.csv in the same folder as this script.
"""

from pathlib import Path
import pandas as pd
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


def load_data(filename: str = "TrainData.csv") -> pd.DataFrame:
    """Load dataset from current directory. Raises a helpful error if missing."""
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {filename}\n"
            "Place TrainData.csv in this folder to run this script."
        )
    df = pd.read_csv(path)
    print("Initial shape:", df.shape)
    return df


def basic_inspection(df: pd.DataFrame) -> None:
    """Print basic structural info useful for portfolio documentation."""
    print("\nINFO")
    print(df.info())

    print("\nDESCRIBE")
    print(df.describe())

    print("\nMISSING VALUES PER COLUMN")
    print(df.isnull().sum())

    print("\nUNIQUE VALUES PER COLUMN")
    print(df.nunique())

    if "station" in df.columns:
        print("\nSTATION VALUE COUNTS")
        print(df["station"].value_counts())


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning rules:
    - Drop rows with missing station (small count, categorical key feature)
    - Fill missing age with median (robust to skew)
    """
    if "station" in df.columns:
        df = df.dropna(subset=["station"])

    if "age" in df.columns:
        median_age = df["age"].median()
        df["age"] = df["age"].fillna(median_age)

    print("\nShape after cleaning:", df.shape)
    print("Missing values after cleaning:\n", df.isnull().sum())
    return df


def treat_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Outlier handling:
    - Cap fare at 99th percentile to reduce extreme leverage
    """
    if "fare" in df.columns:
        fare_cap = df["fare"].quantile(0.99)
        df["fare"] = df["fare"].clip(upper=fare_cap)
        print("\nFare cap value used:", fare_cap)

    return df


def plot_outliers(df: pd.DataFrame) -> None:
    """Optional visuals to quickly validate outlier handling."""
    if "age" in df.columns and "fare" in df.columns:
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        sns.boxplot(x=df["age"])
        plt.title("Age Outliers")

        plt.subplot(1, 2, 2)
        sns.boxplot(x=df["fare"])
        plt.title("Fare Outliers")

        plt.tight_layout()
        plt.show()


def build_preprocessor():
    """Build preprocessing pipeline for categorical and numeric features."""
    cat_cols = ["sex", "station"]
    num_cols = ["pclass", "age", "sibsp", "parch", "fare"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), cat_cols),
            ("num", "passthrough", num_cols),
        ]
    )
    return preprocessor


def split_data(df: pd.DataFrame):
    """Split dataset into train and test sets."""
    X = df.drop("survived", axis=1)
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=12345
    )

    print("\nTraining set size:", X_train.shape)
    print("Testing set size:", X_test.shape)
    return X_train, X_test, y_train, y_test


def evaluate_knn(preprocessor, X_train, X_test, y_train, y_test) -> float:
    """Test k from 1 to 30 and return best accuracy."""
    accuracies = {}

    for k in range(1, 31):
        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("knn", KNeighborsClassifier(n_neighbors=k)),
            ]
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracies[k] = accuracy_score(y_test, y_pred)

    best_k = max(accuracies, key=accuracies.get)
    best_acc = accuracies[best_k]

    print("\nBest k:", best_k)
    print("Best KNN accuracy:", best_acc)
    return best_acc


def evaluate_logistic(preprocessor, X_train, X_test, y_train, y_test) -> float:
    """Train Logistic Regression and return accuracy."""
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("logreg", LogisticRegression(max_iter=1000)),
        ]
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print("\nLogistic Regression accuracy:", acc)
    return acc


def evaluate_tree(preprocessor, X_train, X_test, y_train, y_test) -> float:
    """Test tree depth 1..20 and return best accuracy."""
    accuracies = {}

    for depth in range(1, 21):
        model = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("tree", DecisionTreeClassifier(max_depth=depth, random_state=12345)),
            ]
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracies[depth] = accuracy_score(y_test, y_pred)

    best_depth = max(accuracies, key=accuracies.get)
    best_acc = accuracies[best_depth]

    print("\nBest tree depth:", best_depth)
    print("Best Decision Tree accuracy:", best_acc)
    return best_acc


def main():
    df = load_data("TrainData.csv")
    basic_inspection(df)

    df = clean_data(df)
    plot_outliers(df)

    df = treat_outliers(df)

    preprocessor = build_preprocessor()
    X_train, X_test, y_train, y_test = split_data(df)

    knn_acc = evaluate_knn(preprocessor, X_train, X_test, y_train, y_test)
    log_acc = evaluate_logistic(preprocessor, X_train, X_test, y_train, y_test)
    tree_acc = evaluate_tree(preprocessor, X_train, X_test, y_train, y_test)

    print("\nMODEL ACCURACY SUMMARY")
    print("------------------------")
    print("KNN Best Accuracy:", knn_acc)
    print("Logistic Regression Accuracy:", log_acc)
    print("Decision Tree Best Accuracy:", tree_acc)


if __name__ == "__main__":
    main()
