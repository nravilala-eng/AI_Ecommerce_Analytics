# AI E-Commerce Analytics

An end-to-end E-Commerce Data Analytics project using Python, Pandas, Machine Learning, and Streamlit to analyze sales performance, customer behavior, and delivery operations.

## Project Overview

This project analyzes the Brazilian Olist E-Commerce dataset to identify business trends, understand customer purchasing behavior, evaluate delivery performance, and generate actionable business insights.

It includes data exploration, sales analysis, customer segmentation using K-Means clustering, model evaluation, and an interactive Streamlit dashboard.

## Objectives

- Analyze overall e-commerce sales and revenue.
- Identify top-performing states and payment methods.
- Understand monthly sales trends.
- Segment customers using RFM analysis and K-Means clustering.
- Evaluate order delivery performance.
- Present business insights through an interactive dashboard.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data analysis and programming |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Plotly | Interactive charts |
| Scikit-learn | Customer segmentation and machine learning |
| Streamlit | Interactive dashboard |
| SQL | Database and query practice |

## Project Features

### 1. Exploratory Data Analysis
- Dataset structure and quality checks
- Missing-value analysis
- Duplicate-value checks
- Customer location analysis

### 2. Sales Analysis
- Revenue and payment analysis
- Payment method analysis
- Top-performing states
- Monthly sales trends

### 3. Customer Segmentation
- Recency, Frequency, and Monetary (RFM) analysis
- K-Means clustering
- Customer segment comparison
- Cluster visualization

### 4. Order and Delivery Analysis
- Order status analysis
- Average delivery time
- Late delivery identification
- On-time delivery analysis

### 5. Interactive Dashboard

The Streamlit dashboard provides:
- Business overview and KPI cards
- Sales analysis
- Customer segmentation
- Order and delivery performance
- Interactive charts and filters

## Key Analysis Results

| Metric | Result |
|---|---:|
| Average Delivery Time | 12.56 days |
| Late Deliveries | 7,826 |
| On-time or Early Deliveries | 88,644 |
| Customers Analyzed for Segmentation | 93,358 |
| Highest Revenue Month | November 2017 |

*Results are based on the analyzed Olist dataset.*

## Live Dashboard

Explore the deployed application:

[AI E-Commerce Analytics Dashboard](https://aiecommerceanalytics-dninw57x7apimwy9mqfq7z.streamlit.app/)

## Project Structure

```text
AI_Ecommerce_Analytics/
│
├── dashboard/
│   └── app.py
│
├── dataset/
│   ├── raw/
│   ├── processed/
│   └── models/
│
├── notebooks/
│   ├── 01_data_exploration.py
│   ├── 02_order_analysis.py
│   ├── 03_delivery_analysis.py
│   ├── 04_customer_sales_analysis.py
│   ├── 05_monthly_sales_analysis.py
│   ├── 06_customer_segmentation.py
│   └── 07_model_evaluation.py
│
├── reports/
├── sql/
├── requirements.txt
├── test_environment.py
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nravilala-eng/AI_Ecommerce_Analytics.git
```

### 2. Navigate to the project folder

```bash
cd AI_Ecommerce_Analytics
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser.

## Dataset

This project uses the Brazilian E-Commerce Public Dataset by Olist.

The dataset contains information about customers, orders, products, sellers, payments, reviews, and delivery operations.

Dataset source: [Brazilian E-Commerce Public Dataset by Olist – Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Future Improvements

- Add AI-generated business recommendations.
- Improve customer segmentation and model evaluation.
- Add automated data refresh and reporting.
- Develop advanced sales forecasting.

## Author

**Narendra Ravilala**

Computer Science and Engineering Graduate | Aspiring Data Analyst

GitHub: [nravilala-eng](https://github.com/nravilala-eng)

---

If you find this project useful, feel free to explore the repository and its analysis.
