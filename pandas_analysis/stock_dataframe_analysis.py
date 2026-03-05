# -----------------------------------------------------------
# Stock DataFrame Analysis with Pandas
# Author: Kia
#
# Description
# This script demonstrates practical data manipulation using
# the pandas library. It loads stock metadata and stock price
# information from CSV files, performs inspection and filtering
# operations, and joins both datasets before exporting the
# final result to a new CSV file.
#
# Skills demonstrated
# - reading CSV data
# - setting DataFrame indexes
# - inspecting structure and missing values
# - filtering and selecting columns
# - sorting DataFrames
# - joining datasets
# - exporting processed data
# -----------------------------------------------------------

import pandas as pd


# -----------------------------------------------------------
# File paths
# -----------------------------------------------------------
stocks_path = "StocksKati.csv"
prices_path = "Stock-PricesKati.csv"


# -----------------------------------------------------------
# Load the stock metadata dataset
# -----------------------------------------------------------
df = pd.read_csv(stocks_path)

# Use the stock symbol as the DataFrame index
df = df.set_index("Symbol")

print("FULL DATAFRAME")
print(df)


# -----------------------------------------------------------
# Inspect the dataset
# -----------------------------------------------------------

# Count non-null values per column
print("\nNON-NULL COUNTS PER COLUMN")
print(df.notna().sum())

# Show data types
print("\nDATA TYPES")
print(df.dtypes)


# -----------------------------------------------------------
# Display shape information
# -----------------------------------------------------------
rows, cols = df.shape

print("\nDATAFRAME SHAPE")
print(f"Rows: {rows}, Columns: {cols}")
print(f"len(df): {len(df)}   len(df.columns): {len(df.columns)}")


# -----------------------------------------------------------
# Show first and last rows
# -----------------------------------------------------------
print("\nFIRST 10 ROWS")
print(df.head(10))

print("\nLAST 10 ROWS")
print(df.tail(10))


# -----------------------------------------------------------
# Column selection examples
# -----------------------------------------------------------

print("\nCompany column:")
print(df["Company"])

print("\nCompany and Industry columns:")
print(df[["Company", "Industry"]])


# -----------------------------------------------------------
# Row lookup example
# -----------------------------------------------------------
print("\nRow for AAPL")

if "AAPL" in df.index:
    print(df.loc["AAPL"])
else:
    print("AAPL not found in dataset")


# -----------------------------------------------------------
# Retrieve specific field
# -----------------------------------------------------------
print("\nExchange for AAPL")

if "AAPL" in df.index and "Exchange" in df.columns:
    print(df.loc["AAPL", "Exchange"])
else:
    print("Exchange information unavailable.")


# -----------------------------------------------------------
# Sorting example
# -----------------------------------------------------------
print("\nSorted by Industry and Company")

sorted_df = df.sort_values(by=["Industry", "Company"])
print(sorted_df)


# -----------------------------------------------------------
# Filtering example
# -----------------------------------------------------------
print("\nRows where Industry == Information Technology")

it_rows = df[df["Industry"] == "Information Technology"]
print(it_rows)


# -----------------------------------------------------------
# Rows where Notes column is not missing
# -----------------------------------------------------------
print("\nRows where 'Notes' is NOT missing")

if "Notes" in df.columns:
    notes_present = df[df["Notes"].notna()]
    print(notes_present)
else:
    print("Notes column not found")


# -----------------------------------------------------------
# Create version without Notes column
# -----------------------------------------------------------
print("\nDataFrame WITHOUT the Notes column")

if "Notes" in df.columns:
    df_no_notes = df.drop(columns=["Notes"])
    print(df_no_notes)
else:
    df_no_notes = df.copy()
    print(df_no_notes)


# -----------------------------------------------------------
# Join stock metadata with price data
# -----------------------------------------------------------
print("\nJoining with stock price dataset")

prices = pd.read_csv(prices_path)

prices = prices.set_index("Symbol")

df_with_prices = df.join(prices[["Price"]], how="left")

print(df_with_prices)


# -----------------------------------------------------------
# Export the result
# -----------------------------------------------------------
output_path = "Stocks_with_Prices.csv"

df_with_prices.to_csv(output_path)

print(f"\nSaved joined DataFrame to: {output_path}")
