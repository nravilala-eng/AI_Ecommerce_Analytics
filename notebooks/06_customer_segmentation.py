
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 1. Load datasets
orders = pd.read_csv(
    "dataset/raw/olist_orders_dataset.csv"
)

customers = pd.read_csv(
    "dataset/raw/olist_customers_dataset.csv"
)

payments = pd.read_csv(
    "dataset/raw/olist_order_payments_dataset.csv"
)

# 2. Convert purchase timestamp
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# 3. Keep delivered orders
orders = orders[
    orders["order_status"] == "delivered"
].copy()

# 4. Calculate order payment totals
order_payments = payments.groupby(
    "order_id", as_index=False
)["payment_value"].sum()

# 5. Merge datasets
data = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

data = data.merge(
    order_payments,
    on="order_id",
    how="left"
)

data["payment_value"] = data["payment_value"].fillna(0)

# 6. Reference date for Recency
reference_date = (
    data["order_purchase_timestamp"].max()
    + pd.Timedelta(days=1)
)

# 7. Calculate RFM
rfm = data.groupby("customer_unique_id").agg(
    Recency=(
        "order_purchase_timestamp",
        lambda x: (reference_date - x.max()).days
    ),
    Frequency=("order_id", "nunique"),
    Monetary=("payment_value", "sum")
).reset_index()

# 8. Display RFM data
print("\nCUSTOMER RFM ANALYSIS")
print(rfm.head())

print("\nRFM SUMMARY")
print(rfm[["Recency", "Frequency", "Monetary"]].describe())

# 9. Prepare data for clustering
features = rfm[
    ["Recency", "Frequency", "Monetary"]
].copy()

# Reduce skewness
features["Recency"] = np.log1p(features["Recency"])
features["Frequency"] = np.log1p(features["Frequency"])
features["Monetary"] = np.log1p(features["Monetary"])

# 10. Standardize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# 11. Apply K-Means
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

rfm["Cluster"] = kmeans.fit_predict(scaled_features)

# 12. Cluster summary
cluster_summary = rfm.groupby("Cluster").agg(
    Customers=("customer_unique_id", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean")
).round(2)

print("\nCUSTOMER SEGMENT SUMMARY")
print(cluster_summary)

# 13. Save results
rfm.to_csv(
    "dataset/processed/customer_segments.csv",
    index=False
)

# 14. Visualize clusters
plt.figure(figsize=(10, 6))

plt.scatter(
    rfm["Recency"],
    rfm["Monetary"],
    c=rfm["Cluster"],
    alpha=0.5
)

plt.title("AI Customer Segmentation - KMeans")
plt.xlabel("Recency (Days)")
plt.ylabel("Monetary Value (BRL)")
plt.colorbar(label="Customer Cluster")
plt.tight_layout()

plt.savefig(
    "reports/customer_segmentation.png"
)

plt.show()

print("\nCustomer Segmentation Completed!")
