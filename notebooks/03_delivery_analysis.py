
import pandas as pd

# Load order dataset
orders = pd.read_csv(
    "dataset/raw/olist_orders_dataset.csv"
)

# Convert date columns into datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(
        orders[col], errors="coerce"
    )

# Select delivered orders
delivered = orders[
    orders["order_status"] == "delivered"
].copy()

# Calculate delivery duration
delivered["delivery_days"] = (
    delivered["order_delivered_customer_date"]
    - delivered["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate estimated delivery difference
delivered["delivery_difference"] = (
    delivered["order_delivered_customer_date"]
    - delivered["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

print("\nDELIVERY PERFORMANCE")

print("\nAverage Delivery Time:")
print(round(delivered["delivery_days"].mean(), 2), "days")

print("\nFastest Delivery:")
print(round(delivered["delivery_days"].min(), 2), "days")

print("\nSlowest Delivery:")
print(round(delivered["delivery_days"].max(), 2), "days")

late = (delivered["delivery_difference"] > 0).sum()
on_time = (delivered["delivery_difference"] <= 0).sum()

print("\nLate Deliveries:", late)
print("On-time or Early Deliveries:", on_time)

print("\nDelivery Analysis Completed!")
