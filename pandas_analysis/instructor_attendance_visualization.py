"""
instructor_attendance_visualization.py
Author: Kia

Description
-----------
Visualizes attendance counts by instructor and class type using a stacked bar chart.

The script demonstrates:
- loading tabular data with pandas
- pivot table transformation
- stacked bar chart visualization
- labeled bar segments using matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------------------------
# Load dataset
# -----------------------------------------------------------
df = pd.read_csv("T2.csv")


# -----------------------------------------------------------
# Transform data into pivot format
# Rows: instructors
# Columns: class types
# Values: attendance counts
# -----------------------------------------------------------
pivot = df.pivot(
    index="instructor",
    columns="class_type",
    values="attendance_count"
).fillna(0)


# -----------------------------------------------------------
# Create stacked bar chart
# -----------------------------------------------------------
ax = pivot.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6),
    colormap="tab20"
)


# -----------------------------------------------------------
# Add value labels to each bar segment
# -----------------------------------------------------------
for container in ax.containers:
    ax.bar_label(container, label_type="center", fontsize=8)


# -----------------------------------------------------------
# Chart formatting
# -----------------------------------------------------------
plt.title("Attendance by Instructor and Class Type")
plt.xlabel("Instructor")
plt.ylabel("Attendance Count")

plt.legend(
    title="Class Type",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()
