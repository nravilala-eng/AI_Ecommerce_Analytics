
import pandas as pd

# Load datasets
customers = pd.read_csv(
    "dataset/raw/olist_customers_dataset.csv"
)

orders = pd.read_csv(
    "dataset/raw/olist_orders_dataset.csv"
)

payments = pd.read_csv(
    "dataset/raw/olist_order_payments_dataset.csv"
)

# Merge orders with customers
customer_orders = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

# Merge payment information
sales = customer_orders.merge(
    payments,
    on="order_id",
    how="left"
)

# Analyse delivered orders
sales = sales[
    sales["order_status"] == "delivered"
]

print("\nCUSTOMER SALES ANALYSIS")

# Total revenue
print("\nTotal Revenue:")
print(round(sales["payment_value"].sum(), 2))

# Total payment transactions
print("\nTotal Payment Records:")
print(len(sales))

# Average payment value
print("\nAverage Payment Value:")
print(round(sales["payment_value"].mean(), 2))

# Top 10 states by revenue
print("\nTOP 10 STATES BY REVENUE:")
print(
    sales.groupby("customer_state")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Payment method distribution
print("\nPAYMENT METHODS:")
print(sales["payment_type"].value_counts())

print("\nCustomer Sales Analysis Completed!")
