
import pandas as pd

# Load order dataset
orders = pd.read_csv(
    "dataset/raw/olist_orders_dataset.csv"
)

print("\nFIRST 5 ORDERS")
print(orders.head())

print("\nDATASET INFORMATION")
orders.info()

print("\nDATASET SHAPE")
print(orders.shape)

print("\nMISSING VALUES")
print(orders.isnull().sum())

# Order status analysis
print("\nORDER STATUS DISTRIBUTION")
print(orders["order_status"].value_counts())

# Total orders
print("\nTOTAL ORDERS")
print(orders["order_id"].nunique())

# Delivered orders
print("\nDELIVERED ORDERS")
print(
    (orders["order_status"] == "delivered").sum()
)

# Cancelled orders
print("\nCANCELLED ORDERS")
print(
    (orders["order_status"] == "canceled").sum()
)
