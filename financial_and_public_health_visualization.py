#  Data Visualization Project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# helper to save figures
def kati_save_fig(path: str):
    """Save matplotlib figure nicely"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()

def kati_make_month_label(series):
    """Convert dates into 'YYYY-MM' """
    dates = pd.to_datetime(series, errors="coerce")
    return dates.dt.to_period("M").astype(str)

def kati_sort_months(labels):
    """Sort 'YYYY-MM' chronologically"""
    return sorted(labels, key=lambda s: pd.to_datetime(s, format="%Y-%m", errors="coerce"))



# Income statements

sheet_divA = pd.read_csv("IncStmt-DivA.csv", skiprows=5, header=0)
sheet_divB = pd.read_csv("IncStmt-DivB.csv", skiprows=5, header=0)

# remove ghost columns
sheet_divA = sheet_divA.loc[:, ~sheet_divA.columns.str.contains("^Unnamed")]
sheet_divB = sheet_divB.loc[:, ~sheet_divB.columns.str.contains("^Unnamed")]

# numeric fix
for table in (sheet_divA, sheet_divB):
    for col in ["Act2019", "Act2020", "Proj2021"]:
        table[col] = pd.to_numeric(table[col], errors="coerce")

# locate sales rows
for _tbl in (sheet_divA, sheet_divB):
    if "Description" in _tbl.columns:
        _tbl["Description"] = _tbl["Description"].astype(str)
    if "CODE" in _tbl.columns:
        _tbl["CODE"] = _tbl["CODE"].astype(str)

maskA = sheet_divA["Description"].fillna("").str.contains(r"\bSales\b", case=False, na=False)
if not maskA.any() and "CODE" in sheet_divA.columns:
    maskA = sheet_divA["CODE"].fillna("").str.upper().eq("SALE")
row_sales_A = sheet_divA.loc[maskA].iloc[0]

maskB = sheet_divB["Description"].fillna("").str.contains(r"\bSales\b", case=False, na=False)
if not maskB.any() and "CODE" in sheet_divB.columns:
    maskB = sheet_divB["CODE"].fillna("").str.upper().eq("SALE")
row_sales_B = sheet_divB.loc[maskB].iloc[0]

years_axis = ["2019", "2020", "2021"]
val_sales_A = [row_sales_A["Act2019"], row_sales_A["Act2020"], row_sales_A["Proj2021"]]
val_sales_B = [row_sales_B["Act2019"], row_sales_B["Act2020"], row_sales_B["Proj2021"]]

# stacked bar chart
plt.figure(figsize=(9,5))
plt.bar(years_axis, val_sales_A, label="Division A")
plt.bar(years_axis, val_sales_B, bottom=val_sales_A, label="Division B")
plt.title("Stacked Sales : DivA + DivB")
plt.ylabel("Sales ($M)")
plt.xlabel("Year")
plt.legend()
k_save_fig("figs/kati_Q1a_stacked_sales.png")

# clustered comparison
xpos = np.arange(len(years_axis))
bar_width = 0.35
plt.figure(figsize=(9,5))
plt.bar(xpos - bar_width/2, val_sales_A, bar_width, label="Division A")
plt.bar(xpos + bar_width/2, val_sales_B, bar_width, label="Division B")
plt.xticks(xpos, years_axis)
plt.title("Sales Comparison (Clustered)")
plt.ylabel("Sales ($M)")
plt.xlabel("Year")
plt.legend()
k_save_fig("figs/kati_Q1b_clustered_sales.png")

# expense pies
target_expense_labels = [
    "Selling, General, and Admin", "Advertising",
    "Depreciation", "Rental Expense", "Other Expense"
]

expense_A = sheet_divA[sheet_divA["Description"].isin(target_expense_labels)][["Description","Proj2021"]]
expense_B = sheet_divB[sheet_divB["Description"].isin(target_expense_labels)][["Description","Proj2021"]]

plt.figure(figsize=(7,7))
plt.pie(expense_A["Proj2021"], labels=expense_A["Description"], autopct="%1.1f%%")
plt.title("2021 Forecasted Expenses Div A")
k_save_fig("figs/kati_Q1c_expenses_A.png")

plt.figure(figsize=(7,7))
plt.pie(expense_B["Proj2021"], labels=expense_B["Description"], autopct="%1.1f%%")
plt.title("2021 Forecasted Expenses Div B")
k_save_fig("figs/kati_Q1c_expenses_B.png")



# Health & population analysis

health_raw = pd.read_csv("HealthData.csv")
pop_raw = pd.read_csv("PopulationData.csv")

health_raw["Cases"] = pd.to_numeric(health_raw["Cases"], errors="coerce")
pop_raw["Population"] = pd.to_numeric(pop_raw["Population"], errors="coerce")

merged_health_pop = health_raw.merge(pop_raw, on="Towncode", how="left")

merged_health_pop["Date"] = pd.to_datetime(merged_health_pop["Date"], errors="coerce")
merged_health_pop["Month"] = k_make_month_label(merged_health_pop["Date"])


# cases over time
plt.figure(figsize=(10,6))
for city in merged_health_pop["Townname"].dropna().unique():
    slice_city = merged_health_pop[merged_health_pop["Townname"] == city].sort_values("Date")
    plt.plot(slice_city["Date"], slice_city["Cases"], marker="o", label=city)

plt.title("Infections Over Time")
plt.ylabel("Cases")
plt.xlabel("Date")
plt.legend()
k_save_fig("figs/kati_Q2a_cases_over_time.png")


# percent of population
merged_health_pop["PctOfPop"] = (merged_health_pop["Cases"] / merged_health_pop["Population"]) * 100

plt.figure(figsize=(10,6))
for city in merged_health_pop["Townname"].dropna().unique():
    slice_city = merged_health_pop[merged_health_pop["Townname"] == city].sort_values("Date")
    plt.plot(slice_city["Date"], slice_city["PctOfPop"], marker="o", label=city)

plt.title("Infections as % of Population  City Comparison")
plt.ylabel("% Infected")
plt.xlabel("Date")
plt.legend()
k_save_fig("figs/kati_Q2b_cases_percent.png")


# stacked monthly infections
infection_month_city_rollup = merged_health_pop.groupby(["Month","Townname"])["Cases"].sum().reset_index()

monthly_stacked_infections = infection_month_city_rollup.pivot(index="Month", columns="Townname", values="Cases").fillna(0)

monthly_stacked_infections = monthly_stacked_infections.loc[k_sort_months(monthly_stacked_infections.index)]

plt.figure(figsize=(10,6))

bottom = np.zeros(len(monthly_stacked_infections))

for city in monthly_stacked_infections.columns:
    vals = monthly_stacked_infections[city].values
    plt.bar(monthly_stacked_infections.index, vals, bottom=bottom, label=city)
    bottom += vals

plt.title("Monthly Infection Counts (Stacked by City)")
plt.ylabel("Cases")
plt.xlabel("Month")
plt.legend()

k_save_fig("figs/kati_Q2c_stacked_monthly.png")

print("Figures generated in /figs")
