
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score
)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "dataset" / "raw"

# Load datasets
customers = pd.read_csv(DATA_PATH / "olist_customers_dataset.csv")
orders = pd.read_csv(DATA_PATH / "olist_orders_dataset.csv")
payments = pd.read_csv(DATA_PATH / "olist_order_payments_dataset.csv")

# Convert dates
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# Merge datasets
data = orders.merge(customers, on="customer_id")
data = data.merge(payments, on="order_id")

# Keep delivered orders
data = data[data["order_status"] == "delivered"].copy()

# Calculate RFM
reference_date = data["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

rfm = data.groupby("customer_unique_id").agg(
    Recency=("order_purchase_timestamp",
             lambda x: (reference_date - x.max()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("payment_value", "sum")
).reset_index()

# Prepare features
features = rfm[["Recency", "Frequency", "Monetary"]]

# Scale features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Train KMeans
kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

clusters = kmeans.fit_predict(scaled_features)

# Evaluate model
print("\nCUSTOMER SEGMENTATION MODEL EVALUATION")

print("\nSilhouette Score:")
print(round(silhouette_score(
    scaled_features,
    clusters,
    sample_size=min(10000, len(scaled_features)),
    random_state=42
), 4))

print("\nDavies-Bouldin Score:")
print(round(davies_bouldin_score(
    scaled_features, clusters
), 4))

print("\nCalinski-Harabasz Score:")
print(round(calinski_harabasz_score(
    scaled_features, clusters
), 4))

# Cluster distribution
rfm["Cluster"] = clusters

print("\nCUSTOMER CLUSTER DISTRIBUTION")
print(rfm["Cluster"].value_counts().sort_index())

# Save results
output_path = BASE_DIR / "dataset" / "processed"
output_path.mkdir(parents=True, exist_ok=True)

rfm.to_csv(
    output_path / "customer_segmentation_evaluated.csv",
    index=False
)

print("\nModel Evaluation Completed Successfully!")
print("Evaluation dataset saved successfully!")
