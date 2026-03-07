"""
membership_and_stock_return_analysis.py


Purpose
-------
This script demonstrates applied statistical analysis with Python using
pandas, NumPy, SciPy, and matplotlib.

It performs two separate analyses:

1. Membership term analysis
   - parses membership start and end dates
   - computes membership length in months
   - normalizes gender labels
   - runs a Welch two-sample t-test to compare inactive membership terms
     between male and female members

2. Stock return analysis
   - loads daily price data
   - detects the date column and adjusted close column
   - computes daily returns
   - evaluates skewness, kurtosis, and normality
   - identifies three-sigma outliers
   - exports processed data and outlier reports
   - saves a histogram of daily returns

Expected input files
--------------------
- members.csv
- ORNG1.csv

Generated output files
----------------------
- ORNG_returns_hist.png
- ORNG_returns_with_z.csv
- ORNG_outliers.csv
"""

import re
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, normaltest, skew, kurtosis


# -----------------------------------------------------------
# Membership analysis helpers
# -----------------------------------------------------------
def parse_dates_inplace(df: pd.DataFrame, start_col: str, end_col: str) -> None:
    """
    Convert start and end date columns to datetime in place.

    Parameters
    ----------
    df : pd.DataFrame
        Input membership DataFrame
    start_col : str
        Name of membership start date column
    end_col : str
        Name of membership end date column
    """
    df[start_col] = pd.to_datetime(df[start_col], errors="coerce")
    df[end_col] = pd.to_datetime(df[end_col], errors="coerce")


def compute_membership_term_months(
    df: pd.DataFrame,
    start_col: str,
    end_col: str,
    out_col: str = "term_mo"
) -> pd.DataFrame:
    """
    Compute membership length in months.

    Parameters
    ----------
    df : pd.DataFrame
        Membership dataset
    start_col : str
        Start date column
    end_col : str
        End date column
    out_col : str
        Name of output column for term length in months

    Returns
    -------
    pd.DataFrame
        Copy of the input DataFrame with a term column added
    """
    out = df.copy()
    out[out_col] = (out[end_col] - out[start_col]).dt.days / 30.44
    return out


def normalize_gender(series: pd.Series) -> pd.Series:
    """
    Normalize raw gender labels to Male / Female where possible.

    Parameters
    ----------
    series : pd.Series
        Raw gender column

    Returns
    -------
    pd.Series
        Normalized gender values
    """
    mapping = {
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female"
    }

    return series.apply(
        lambda x: mapping.get(str(x).strip().lower(), np.nan) if pd.notna(x) else np.nan
    )


def welch_ttest_by_gender(df: pd.DataFrame, term_col: str) -> Dict[str, float]:
    """
    Compare membership term length by gender using Welch's t-test.

    Parameters
    ----------
    df : pd.DataFrame
        Membership dataset containing GenderNorm and term column
    term_col : str
        Name of term length column

    Returns
    -------
    Dict[str, float]
        Summary statistics and test results
    """
    males = df.loc[df["GenderNorm"].eq("Male"), term_col].dropna()
    females = df.loc[df["GenderNorm"].eq("Female"), term_col].dropna()

    t_stat, p_val = ttest_ind(
        males,
        females,
        equal_var=False,
        nan_policy="omit"
    )

    return {
        "n_males": int(males.shape[0]),
        "n_females": int(females.shape[0]),
        "mean_males": float(males.mean()),
        "mean_females": float(females.mean()),
        "std_males": float(males.std(ddof=1)),
        "std_females": float(females.std(ddof=1)),
        "t_statistic": float(t_stat),
        "p_value": float(p_val),
        "alpha_0_05_significant": bool(p_val < 0.05)
    }


# -----------------------------------------------------------
# Stock return analysis helpers
# -----------------------------------------------------------
def detect_adj_close_column(df: pd.DataFrame) -> str:
    """
    Detect the adjusted close price column.

    Parameters
    ----------
    df : pd.DataFrame
        Price dataset

    Returns
    -------
    str
        Column name most likely representing adjusted close
    """
    exact_names = [
        "Adj Close",
        "Adj_Close",
        "AdjClose",
        "Adjusted Close",
        "Adjusted_Close",
        "Adj. Close"
    ]

    for name in exact_names:
        if name in df.columns:
            return name

    pattern = re.compile(r"\badj(\.|_)?\s*close|\badjust(ed|ment)?\s*close\b", re.I)
    scored = [(col, 1 if pattern.search(col) else 0) for col in df.columns]
    scored.sort(key=lambda x: x[1], reverse=True)

    best = scored[0][0]

    # Fallback: if no likely adjusted-close label exists,
    # pick the numeric column with the highest standard deviation
    if scored[0][1] == 0:
        numeric_df = df.select_dtypes(include=[float, int])
        best = numeric_df.std().idxmax()

    return best


def detect_date_column(df: pd.DataFrame) -> str:
    """
    Detect the date column in a price dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Price dataset

    Returns
    -------
    str
        Date column name
    """
    for candidate in ["Date", "date"]:
        if candidate in df.columns:
            return candidate

    for col in df.columns:
        if "date" in col.lower():
            return col

    raise KeyError("No date column found in the dataset.")


def analyze_orng_returns(csv_path: str) -> Tuple[pd.DataFrame, Dict[str, float], pd.DataFrame]:
    """
    Load price data, compute daily returns, evaluate distribution shape,
    identify outliers, and export results.

    Parameters
    ----------
    csv_path : str
        Path to stock price CSV

    Returns
    -------
    Tuple[pd.DataFrame, Dict[str, float], pd.DataFrame]
        Full processed dataset, summary metrics, and outlier dataset
    """
    price_df = pd.read_csv(csv_path)

    date_col = detect_date_column(price_df)
    adj_col = detect_adj_close_column(price_df)

    price_df[date_col] = pd.to_datetime(price_df[date_col], errors="coerce")
    price_df = price_df.sort_values(date_col).reset_index(drop=True)

    # Compute daily percentage returns
    price_df["daily_return"] = price_df[adj_col].pct_change()
    return_series = price_df["daily_return"].dropna()

    # Save histogram of returns
    plt.figure()
    return_series.hist(bins=50)
    plt.title("Histogram of ORNG Daily Returns")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig("ORNG_returns_hist.png", bbox_inches="tight")
    plt.close()

    # Distribution summary statistics
    return_skew = float(skew(return_series, bias=False))
    return_kurtosis = float(kurtosis(return_series, fisher=True, bias=False))
    normality_stat, normality_p = normaltest(return_series)

    mean_return = float(return_series.mean())
    std_return = float(return_series.std(ddof=1))

    lower_bound = mean_return - 3 * std_return
    upper_bound = mean_return + 3 * std_return

    # Flag three-sigma outliers
    outliers = price_df.loc[
        (price_df["daily_return"] < lower_bound) |
        (price_df["daily_return"] > upper_bound),
        [date_col, "daily_return"]
    ].copy()

    outliers = outliers.rename(
        columns={
            date_col: "Date",
            "daily_return": "DailyReturn"
        }
    )

    # Z-score for each return
    price_df["zscore"] = (price_df["daily_return"] - mean_return) / std_return

    # Export outputs
    price_df.to_csv("ORNG_returns_with_z.csv", index=False)
    outliers.to_csv("ORNG_outliers.csv", index=False)

    metrics = {
        "date_column": date_col,
        "adj_close_column": adj_col,
        "skewness": return_skew,
        "kurtosis_fisher": return_kurtosis,
        "normaltest_stat": float(normality_stat),
        "normaltest_p": float(normality_p),
        "mean_return": mean_return,
        "std_return": std_return,
        "lower_3sigma": lower_bound,
        "upper_3sigma": upper_bound,
        "outlier_count": int(outliers.shape[0])
    }

    return price_df, metrics, outliers


# -----------------------------------------------------------
# Main workflow
# -----------------------------------------------------------
if __name__ == "__main__":
    # -------------------------
    # Q1: Membership term analysis
    # -------------------------
    members = pd.read_csv("members.csv")

    parse_dates_inplace(members, "visitDate", "endDate")

    members = compute_membership_term_months(
        members,
        "visitDate",
        "endDate",
        out_col="term_mo"
    )

    inactive_members = members.loc[
        members["status"].astype(str).str.lower().eq("inactive")
    ].copy()

    inactive_members["GenderNorm"] = normalize_gender(inactive_members["gender"])

    q1_results = welch_ttest_by_gender(inactive_members, "term_mo")

    print("Q1 RESULTS: MEMBERSHIP TERM COMPARISON")
    print(q1_results)

    # -------------------------
    # Q2: ORNG stock return analysis
    # -------------------------
    _, q2_results, _ = analyze_orng_returns("ORNG1.csv")

    print("\nQ2 RESULTS: ORNG RETURN ANALYSIS")
    print(q2_results)
