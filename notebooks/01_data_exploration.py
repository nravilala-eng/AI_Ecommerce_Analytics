import pandas as pd
import os

# Dataset location
path = "dataset/raw/"

# Load customer data
customers = pd.read_csv(
    path + "olist_customers_dataset.csv"
)

# Display first 5 records
print("\nCUSTOMER DATA")
print(customers.head())

# Dataset information
print("\nDATASET INFORMATION")
customers.info()

# Number of rows and columns
print("\nDATASET SHAPE")
print(customers.shape)

# Missing values
print("\nMISSING VALUES")
print(customers.isnull().sum())



# =====================================
# CUSTOMER DATA QUALITY ANALYSIS
# =====================================

print("\nCUSTOMER DATA QUALITY ANALYSIS")

# 1. Check duplicate rows
print("\nDuplicate Rows:")
print(customers.duplicated().sum())

# 2. Check duplicate customer IDs
print("\nDuplicate Customer IDs:")
print(customers["customer_id"].duplicated().sum())

# 3. Count unique customers
print("\nUnique Customer Identities:")
print(customers["customer_unique_id"].nunique())

# 4. Number of cities
print("\nTotal Cities:")
print(customers["customer_city"].nunique())

# 5. Number of states
print("\nTotal States:")
print(customers["customer_state"].nunique())

# 6. Top 10 customer cities
print("\nTop 10 Customer Cities:")
print(customers["customer_city"].value_counts().head(10))

# 7. Customers by state
print("\nCustomers by State:")
print(customers["customer_state"].value_counts().head(10))
