"""
Project: Booking Funnel & Operational Metrics Analysis
Tools: Pandas, Matplotlib

Objective:
Analyze booking funnel conversion, payment reliability,
and attendance performance using aggregated metrics.
"""

import pandas as pd
import matplotlib.pyplot as plt


# -------------------------------
# Booking Funnel Analysis
# -------------------------------

cart_items = 1411
orders_within_7_days = 0

conversion_rate = (
    orders_within_7_days / cart_items * 100
    if cart_items > 0 else 0
)

booking_df = pd.DataFrame({
    "Stage": ["Cart items", "Orders within 7 days"],
    "Count": [cart_items, orders_within_7_days]
})

print("Booking Conversion Rate:", round(conversion_rate, 2), "%")

plt.figure()
plt.bar(booking_df["Stage"], booking_df["Count"])
plt.title("Booking Funnel: Cart vs Orders")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("booking_funnel.png", dpi=300)
plt.show()


# -------------------------------
# Payment Outcome Analysis
# -------------------------------

payment_df = pd.DataFrame({
    "Outcome": ["Succeeded", "Failed"],
    "Percent": [98.70, 1.30]
})

failure_rate = payment_df.loc[
    payment_df["Outcome"] == "Failed", "Percent"
].values[0]

print("Payment Failure Rate:", failure_rate, "%")

plt.figure()
plt.bar(payment_df["Outcome"], payment_df["Percent"])
plt.title("Credit Card Payment Outcomes")
plt.ylabel("Percent")
plt.tight_layout()
plt.savefig("payment_outcomes.png", dpi=300)
plt.show()


# -------------------------------
# Attendance Analysis
# -------------------------------

attendance_df = pd.DataFrame({
    "Attendance": ["Show", "No show"],
    "Percent": [79.03, 20.97]
})

no_show_rate = attendance_df.loc[
    attendance_df["Attendance"] == "No show", "Percent"
].values[0]

print("No-Show Rate:", no_show_rate, "%")

plt.figure()
plt.bar(attendance_df["Attendance"], attendance_df["Percent"])
plt.title("Class Attendance Outcomes")
plt.ylabel("Percent")
plt.tight_layout()
plt.savefig("attendance_outcomes.png", dpi=300)
plt.show()
