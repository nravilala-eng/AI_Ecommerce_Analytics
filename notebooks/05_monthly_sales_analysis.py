
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
orders = pd.read_csv(
    "dataset/raw/olist_orders_dataset.csv"
)

payments = pd.read_csv(
    "dataset/raw/olist_order_payments_dataset.csv"
)

# Convert purchase timestamp
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# Keep delivered orders
delivered_orders = orders[
    orders["order_status"] == "delivered"
].copy()

# Aggregate payment records by order
order_payments = payments.groupby(
    "order_id", as_index=False
)["payment_value"].sum()

# Merge payment totals with orders
sales = delivered_orders.merge(
    order_payments,
    on="order_id",
    how="left"
)

# Extract year and month
sales["year_month"] = (
    sales["order_purchase_timestamp"].dt.to_period("M")
)

# Monthly sales analysis
monthly_sales = sales.groupby(
    "year_month"
).agg(
    total_revenue=("payment_value", "sum"),
    total_orders=("order_id", "nunique")
).reset_index()

monthly_sales["average_order_value"] = (
    monthly_sales["total_revenue"]
    / monthly_sales["total_orders"]
)

print("\nMONTHLY SALES ANALYSIS")
print(monthly_sales.to_string(index=False))

# Highest revenue month
best_month = monthly_sales.loc[
    monthly_sales["total_revenue"].idxmax()
]

print("\nHIGHEST REVENUE MONTH:")
print(best_month)

# Plot monthly revenue
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["year_month"].astype(str),
    monthly_sales["total_revenue"],
    marker="o"
)

plt.title("Monthly E-Commerce Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (BRL)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "reports/monthly_sales_trend.png"
)

plt.show()

print("\nMonthly Sales Analysis Completed!")
