
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI E-Commerce | Enterprise Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. ENTERPRISE LIGHT THEME
# =========================================================

st.markdown("""
<style>
    .stApp {
        background-color: #F4F7FB;
        color: #182230;
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E4EAF2;
    }

    [data-testid="stSidebar"] h1 {
        color: #155EEF;
        font-size: 25px;
        font-weight: 800;
    }

    [data-testid="stSidebar"] p {
        color: #667085;
    }

    h1, h2, h3 {
        color: #182230 !important;
        font-weight: 750 !important;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E4EAF2;
        border-radius: 12px;
        padding: 20px 18px;
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.035);
    }

    [data-testid="stMetricLabel"] {
        color: #667085 !important;
        font-size: 14px;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #155EEF !important;
        font-size: 26px;
        font-weight: 750;
    }

    [data-testid="stMetricDelta"] {
        font-size: 12px;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div.stPlotlyChart) {
        background-color: #FFFFFF;
        border: 1px solid #E4EAF2;
        border-radius: 12px;
        padding: 10px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E4EAF2;
        border-radius: 10px;
        overflow: hidden;
    }

    .main-header {
        background: linear-gradient(110deg, #FFFFFF, #EEF4FF);
        padding: 25px 28px;
        border: 1px solid #E4EAF2;
        border-radius: 14px;
        margin-bottom: 22px;
    }

    .main-header h1 {
        margin: 0;
        color: #173B75 !important;
        font-size: 31px;
    }

    .main-header p {
        margin: 8px 0 0 0;
        color: #667085;
        font-size: 14px;
    }

    .section-caption {
        color: #667085;
        font-size: 13px;
        margin-top: -10px;
        margin-bottom: 15px;
    }

    .insight-card {
        background-color: #FFFFFF;
        border: 1px solid #E4EAF2;
        border-left: 4px solid #155EEF;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 8px 0 18px 0;
        color: #344054;
    }

    .sidebar-footer {
        color: #98A2B3;
        font-size: 12px;
        line-height: 1.7;
    }

    hr {
        border-color: #E4EAF2 !important;
    }

    .stButton button {
        border-radius: 8px;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RAW = BASE_DIR / "dataset" / "raw"
PROCESSED = BASE_DIR / "dataset" / "processed"


# =========================================================
# 4. LOAD DATASETS
# =========================================================

@st.cache_data
def load_data():

    customers = pd.read_csv(
        RAW / "olist_customers_dataset.csv"
    )

    orders = pd.read_csv(
        RAW / "olist_orders_dataset.csv"
    )

    payments = pd.read_csv(
        RAW / "olist_order_payments_dataset.csv"
    )

    segments = pd.read_csv(
        PROCESSED / "customer_segmentation_evaluated.csv"
    )

    # Convert date columns

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for column in date_columns:
        if column in orders.columns:
            orders[column] = pd.to_datetime(
                orders[column],
                errors="coerce"
            )

    payments["payment_value"] = pd.to_numeric(
        payments["payment_value"],
        errors="coerce"
    ).fillna(0)

    return customers, orders, payments, segments


try:

    customers, orders, payments, segments = load_data()

except Exception as error:

    st.error(
        f"Dataset loading error: {error}"
    )

    st.info(
        "Please check your dataset/raw and dataset/processed folders."
    )

    st.stop()


# =========================================================
# 5. CHART DESIGN FUNCTION
# =========================================================

BLUE = "#155EEF"
NAVY = "#173B75"
LIGHT_BLUE = "#84CAFF"
GREEN = "#12B76A"
ORANGE = "#F79009"
RED = "#F04438"

def format_chart(fig, height=400):

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            size=12,
            color="#344054"
        ),
        margin=dict(
            l=35,
            r=25,
            t=65,
            b=35
        ),
        title=dict(
            font=dict(
                size=17,
                color="#182230"
            ),
            x=0.02
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        )
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#E4EAF2",
        tickfont=dict(color="#667085")
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EEF2F6",
        zeroline=False,
        tickfont=dict(color="#667085")
    )

    return fig


def show_chart(fig, height=400):

    st.plotly_chart(
        format_chart(fig, height),
        width="stretch",
        config={
            "displaylogo": False,
            "responsive": True
        }
    )


def section_heading(title, description=None):

    st.subheader(title)

    if description:
        st.markdown(
            f'<p class="section-caption">{description}</p>',
            unsafe_allow_html=True
        )


def currency(value):

    return f"R$ {value:,.2f}"


# =========================================================
# 6. SIDEBAR AND FILTERS
# =========================================================

st.sidebar.title("🛒 E-Commerce BI")

st.sidebar.caption(
    "ENTERPRISE ANALYTICS PLATFORM"
)

st.sidebar.divider()

st.sidebar.subheader("Dashboard Navigation")

page = st.sidebar.radio(
    "Select an analytical view",
    [
        "Overview",
        "Sales Analysis",
        "Customer Segmentation",
        "Order & Delivery Analysis"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Global Filters")

valid_dates = orders[
    "order_purchase_timestamp"
].dropna()

if valid_dates.empty:
    st.error("No valid order purchase dates found.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

selected_dates = st.sidebar.date_input(
    "Order purchase date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(selected_dates, (tuple, list)):

    start_date = selected_dates[0]
    end_date = (
        selected_dates[1]
        if len(selected_dates) > 1
        else selected_dates[0]
    )

else:

    start_date = selected_dates
    end_date = selected_dates

if start_date > end_date:
    st.sidebar.error("Please select a valid date range.")
    st.stop()

available_statuses = sorted(
    orders["order_status"].dropna().unique().tolist()
)

selected_status = st.sidebar.selectbox(
    "Order Status",
    ["All"] + available_statuses
)

# Date filter

date_orders = orders[
    orders["order_purchase_timestamp"].dt.date.between(
        start_date,
        end_date
    )
].copy()

# Status filter

if selected_status != "All":

    filtered_orders = date_orders[
        date_orders["order_status"] == selected_status
    ].copy()

else:

    filtered_orders = date_orders.copy()

# Filter payments using selected order IDs

filtered_payments = payments[
    payments["order_id"].isin(
        filtered_orders["order_id"]
    )
].copy()

# Customers with selected orders

filtered_customers = customers[
    customers["customer_id"].isin(
        filtered_orders["customer_id"]
    )
].copy()

# Common KPIs

total_revenue = filtered_payments[
    "payment_value"
].sum()

total_orders = filtered_orders[
    "order_id"
].nunique()

total_customers = filtered_customers[
    "customer_unique_id"
].nunique()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

# Sidebar footer

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div class="sidebar-footer">
    <b>PROJECT INFORMATION</b><br>
    AI E-Commerce Analytics<br>
    Python | Pandas | Plotly<br>
    Machine Learning | KMeans<br><br>
    Enterprise BI Dashboard
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 7. MAIN HEADER
# =========================================================

st.markdown(
    """
    <div class="main-header">
        <h1>🛒 AI E-Commerce Analytics Dashboard</h1>
        <p>
        Business Intelligence &nbsp;|&nbsp;
        Sales Performance &nbsp;|&nbsp;
        Customer Insights &nbsp;|&nbsp;
        Machine Learning
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Reporting period: {start_date} to {end_date}"
    f" | Order status: {selected_status}"
)


# =========================================================
# 8. PAGE 1: OVERVIEW
# =========================================================

if page == "Overview":

    section_heading(
        "Business Performance Overview",
        "Monitor the overall business performance and key financial indicators."
    )

    # KPI ROW

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Revenue",
        currency(total_revenue)
    )

    c2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    c3.metric(
        "Unique Customers",
        f"{total_customers:,}"
    )

    c4.metric(
        "Average Order Value",
        currency(average_order_value)
    )

    st.divider()

    # MONTHLY REVENUE

    section_heading(
        "Revenue Performance",
        "Track monthly revenue generated from customer payments."
    )

    monthly_data = filtered_payments.merge(
        filtered_orders[
            ["order_id", "order_purchase_timestamp"]
        ],
        on="order_id",
        how="inner"
    )

    monthly_data["Month"] = (
        monthly_data["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        monthly_data.groupby("Month")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    if not monthly_sales.empty:

        fig = px.line(
            monthly_sales,
            x="Month",
            y="payment_value",
            markers=True,
            title="Monthly Revenue Trend",
            labels={
                "Month": "Month",
                "payment_value": "Revenue (BRL)"
            }
        )

        fig.update_traces(
            line=dict(
                color=BLUE,
                width=3
            ),
            marker=dict(
                size=8,
                color=BLUE
            ),
            fill="tozeroy",
            fillcolor="rgba(21,94,239,0.07)"
        )

        show_chart(fig)

    else:

        st.info("No revenue data available for this filter.")

    # REVENUE BY STATE

    section_heading(
        "Geographical Revenue Analysis",
        "Identify the top-performing customer states."
    )

    state_data = filtered_customers.merge(
        filtered_orders[
            ["customer_id", "order_id"]
        ],
        on="customer_id",
        how="inner"
    ).merge(
        filtered_payments,
        on="order_id",
        how="inner"
    )

    state_sales = (
        state_data.groupby("customer_state")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
        .head(10)
    )

    if not state_sales.empty:

        fig = px.bar(
            state_sales,
            x="customer_state",
            y="payment_value",
            title="Top 10 States by Revenue",
            labels={
                "customer_state": "Customer State",
                "payment_value": "Revenue (BRL)"
            },
            color_discrete_sequence=[BLUE],
            text_auto=".2s"
        )

        show_chart(fig)

    else:

        st.info("No state revenue data available.")

    # QUICK BUSINESS INSIGHT

    if not state_sales.empty:

        top_state = state_sales.iloc[0]

        st.markdown(
            f"""
            <div class="insight-card">
            <b>Business Insight</b><br>
            The highest revenue among the displayed states
            comes from <b>{top_state['customer_state']}</b>,
            with revenue of
            <b>{currency(top_state['payment_value'])}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 9. PAGE 2: SALES ANALYSIS
# =========================================================

elif page == "Sales Analysis":

    section_heading(
        "Sales Performance Analysis",
        "Understand payment behavior, revenue distribution and monthly sales."
    )

    # PAYMENT METHOD SUMMARY

    method_data = (
        filtered_payments.groupby("payment_type")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("payment_value", ascending=False)
    )

    total_payment_revenue = method_data[
        "payment_value"
    ].sum()

    payment_methods = method_data[
        "payment_type"
    ].nunique()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Payment Revenue",
        currency(total_payment_revenue)
    )

    c2.metric(
        "Payment Methods",
        f"{payment_methods}"
    )

    c3.metric(
        "Total Transactions",
        f"{len(filtered_payments):,}"
    )

    st.divider()

    # PAYMENT CHART

    section_heading(
        "Payment Method Distribution",
        "Compare the contribution of different payment methods."
    )

    if not method_data.empty:

        fig = px.pie(
            method_data,
            names="payment_type",
            values="payment_value",
            hole=0.58,
            title="Revenue Share by Payment Method",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Revenue: R$ %{value:,.2f}<br>"
                "Share: %{percent}<extra></extra>"
            )
        )

        show_chart(fig)

    else:

        st.info("No payment data available.")

    # MONTHLY SALES

    section_heading(
        "Monthly Sales Performance",
        "Compare revenue across months."
    )

    sales_monthly = filtered_payments.merge(
        filtered_orders[
            ["order_id", "order_purchase_timestamp"]
        ],
        on="order_id",
        how="inner"
    )

    sales_monthly["Month"] = (
        sales_monthly["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_summary = (
        sales_monthly.groupby("Month")["payment_value"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    if not monthly_summary.empty:

        fig = px.bar(
            monthly_summary,
            x="Month",
            y="payment_value",
            title="Monthly Revenue Comparison",
            labels={
                "Month": "Month",
                "payment_value": "Revenue (BRL)"
            },
            color_discrete_sequence=[BLUE]
        )

        show_chart(fig)

    else:

        st.info("No monthly sales data available.")

    # PAYMENT TABLE

    section_heading(
        "Payment Method Details",
        "Detailed revenue contribution by payment type."
    )

    if not method_data.empty:

        payment_table = method_data.copy()

        payment_table["Revenue Share"] = (
            payment_table["payment_value"]
            / total_payment_revenue * 100
            if total_payment_revenue
            else 0
        )

        payment_table["payment_value"] = (
            payment_table["payment_value"]
            .map(currency)
        )

        payment_table["Revenue Share"] = (
            payment_table["Revenue Share"]
            .map(lambda x: f"{x:.2f}%")
        )

        payment_table.columns = [
            "Payment Method",
            "Total Revenue",
            "Revenue Share"
        ]

        st.dataframe(
            payment_table,
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "Download Payment Report",
            data=payment_table.to_csv(index=False),
            file_name="payment_analysis_report.csv",
            mime="text/csv"
        )


# =========================================================
# 10. PAGE 3: CUSTOMER SEGMENTATION
# =========================================================

elif page == "Customer Segmentation":

    section_heading(
        "AI-Powered Customer Segmentation",
        "Understand customer behavior using KMeans clustering and RFM metrics."
    )

    st.markdown(
        """
        <div class="insight-card">
        <b>Machine Learning Model: KMeans Clustering</b><br>
        Customers are grouped using Recency, Frequency and Monetary
        values to identify different purchasing behavior patterns.
        The segmentation results shown below come from your existing
        evaluated dataset.
        </div>
        """,
        unsafe_allow_html=True
    )

    # SEGMENTATION DATA

    required_columns = [
        "customer_unique_id",
        "Cluster",
        "Recency",
        "Frequency",
        "Monetary"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in segments.columns
    ]

    if missing_columns:

        st.error(
            f"Missing segmentation columns: {missing_columns}"
        )

        st.stop()

    segment_data = segments.dropna(
        subset=required_columns
    ).copy()

    # KPI METRICS

    cluster_summary = (
        segment_data.groupby("Cluster")
        .agg(
            Customers=("customer_unique_id", "nunique"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean")
        )
        .reset_index()
    )

    segmented_count = segment_data[
        "customer_unique_id"
    ].nunique()

    number_of_clusters = segment_data[
        "Cluster"
    ].nunique()

    largest_cluster = (
        cluster_summary.sort_values(
            "Customers",
            ascending=False
        ).iloc[0]
        if not cluster_summary.empty
        else None
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Segmented Customers",
        f"{segmented_count:,}"
    )

    c2.metric(
        "Number of Clusters",
        f"{number_of_clusters}"
    )

    c3.metric(
        "Largest Cluster Size",
        f"{int(largest_cluster['Customers']):,}"
        if largest_cluster is not None
        else "0"
    )

    st.divider()

    # CLUSTER DISTRIBUTION

    section_heading(
        "Customer Cluster Distribution",
        "Compare the number of customers assigned to each cluster."
    )

    if not cluster_summary.empty:

        cluster_plot = cluster_summary.copy()

        cluster_plot["Cluster"] = (
            cluster_plot["Cluster"].astype(str)
        )

        fig = px.bar(
            cluster_plot,
            x="Cluster",
            y="Customers",
            color="Cluster",
            text="Customers",
            title="Customer Count by Cluster",
            labels={
                "Cluster": "Customer Cluster",
                "Customers": "Number of Customers"
            },
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        show_chart(fig)

    # RFM SCATTER PLOT

    section_heading(
        "RFM Customer Behavior Analysis",
        "Explore how customer recency and spending differ between clusters."
    )

    plot_data = segment_data.sample(
        n=min(12000, len(segment_data)),
        random_state=42
    )

    fig = px.scatter(
        plot_data,
        x="Recency",
        y="Monetary",
        color=plot_data["Cluster"].astype(str),
        size="Frequency",
        size_max=13,
        opacity=0.65,
        title="Customer Segments: Recency vs Monetary Value",
        labels={
            "Recency": "Recency (Days)",
            "Monetary": "Monetary Value (BRL)",
            "color": "Cluster",
            "Frequency": "Purchase Frequency"
        },
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    show_chart(fig, height=500)

    # CLUSTER SUMMARY TABLE

    section_heading(
        "Cluster Performance Summary",
        "Compare average RFM metrics across customer groups."
    )

    display_cluster = cluster_summary.copy()

    display_cluster.columns = [
        "Cluster",
        "Customers",
        "Average Recency",
        "Average Frequency",
        "Average Monetary Value"
    ]

    st.dataframe(
        display_cluster.round(2),
        width="stretch",
        hide_index=True
    )

    st.download_button(
        "Download Customer Segmentation Report",
        data=display_cluster.to_csv(index=False),
        file_name="customer_segmentation_report.csv",
        mime="text/csv"
    )


# =========================================================
# 11. PAGE 4: ORDER & DELIVERY ANALYSIS
# =========================================================

elif page == "Order & Delivery Analysis":

    section_heading(
        "Order & Delivery Performance",
        "Monitor order statuses, delivery efficiency and customer fulfillment."
    )

    # ORDER STATUS ANALYSIS
    # Use date-filtered orders before the optional status filter.

    status_data = (
        date_orders["order_status"]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Order Status",
        "Orders"
    ]

    total_date_orders = date_orders[
        "order_id"
    ].nunique()

    c1, c2 = st.columns(2)

    c1.metric(
        "Orders in Selected Period",
        f"{total_date_orders:,}"
    )

    delivered_count = (
        date_orders["order_status"] == "delivered"
    ).sum()

    c2.metric(
        "Delivered Orders",
        f"{delivered_count:,}"
    )

    st.divider()

    section_heading(
        "Order Status Distribution",
        "Understand the distribution of orders by fulfillment status."
    )

    if not status_data.empty:

        fig = px.bar(
            status_data,
            x="Order Status",
            y="Orders",
            color="Orders",
            text="Orders",
            title="Orders by Status",
            color_continuous_scale="Blues"
        )

        show_chart(fig)

    # DELIVERY CALCULATIONS

    delivered = filtered_orders[
        filtered_orders["order_status"] == "delivered"
    ].copy()

    if not delivered.empty:

        delivered["delivery_days"] = (
            delivered["order_delivered_customer_date"]
            - delivered["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400

        delivered["estimated_days"] = (
            delivered["order_estimated_delivery_date"]
            - delivered["order_purchase_timestamp"]
        ).dt.total_seconds() / 86400

        delivered = delivered.dropna(
            subset=[
                "delivery_days",
                "estimated_days"
            ]
        )

        delivered = delivered[
            (delivered["delivery_days"] >= 0)
            & (delivered["estimated_days"] >= 0)
        ]

    # DELIVERY KPIs

    st.divider()

    section_heading(
        "Delivery Performance Indicators",
        "Evaluate delivery speed and fulfillment reliability."
    )

    if not delivered.empty:

        late_count = (
            delivered["delivery_days"]
            > delivered["estimated_days"]
        ).sum()

        on_time_count = len(delivered) - late_count

        average_delivery = delivered[
            "delivery_days"
        ].mean()

        on_time_rate = (
            on_time_count / len(delivered) * 100
        )

        late_rate = (
            late_count / len(delivered) * 100
        )

    else:

        late_count = 0
        on_time_count = 0
        average_delivery = 0
        on_time_rate = 0
        late_rate = 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Average Delivery Time",
        f"{average_delivery:.2f} Days"
    )

    c2.metric(
        "On-Time Deliveries",
        f"{on_time_count:,}"
    )

    c3.metric(
        "Late Deliveries",
        f"{late_count:,}"
    )

    c4.metric(
        "On-Time Delivery Rate",
        f"{on_time_rate:.2f}%"
    )

    # ON-TIME VS LATE CHART

    if not delivered.empty:

        delivery_summary = pd.DataFrame({
            "Delivery Status": [
                "On Time",
                "Late"
            ],
            "Orders": [
                on_time_count,
                late_count
            ]
        })

        section_heading(
            "On-Time vs Late Deliveries",
            "Compare successful and delayed deliveries."
        )

        fig = px.pie(
            delivery_summary,
            names="Delivery Status",
            values="Orders",
            hole=0.55,
            color="Delivery Status",
            color_discrete_map={
                "On Time": GREEN,
                "Late": RED
            },
            title="Delivery Reliability"
        )

        fig.update_traces(
            textinfo="percent+label"
        )

        show_chart(fig)

        # DELIVERY TIME DISTRIBUTION

        section_heading(
            "Delivery Time Distribution",
            "Understand how many days customers wait for their orders."
        )

        fig = px.histogram(
            delivered,
            x="delivery_days",
            nbins=30,
            title="Orders by Delivery Duration",
            labels={
                "delivery_days": "Delivery Time (Days)",
                "count": "Number of Orders"
            },
            color_discrete_sequence=[BLUE]
        )

        show_chart(fig)

        # DELIVERY DATA TABLE

        section_heading(
            "Delivery Performance Summary"
        )

        delivery_table = delivered[
            [
                "order_id",
                "delivery_days",
                "estimated_days"
            ]
        ].copy()

        delivery_table["Delivery Status"] = (
            delivery_table["delivery_days"]
            > delivery_table["estimated_days"]
        ).map({
            True: "Late",
            False: "On Time"
        })

        delivery_table.columns = [
            "Order ID",
            "Actual Delivery Days",
            "Estimated Delivery Days",
            "Delivery Status"
        ]

        st.dataframe(
            delivery_table.round(2).head(1000),
            width="stretch",
            hide_index=True
        )

        st.download_button(
            "Download Delivery Report",
            data=delivery_table.to_csv(index=False),
            file_name="delivery_performance_report.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No completed delivery records are available "
            "for the selected filters."
        )


# =========================================================
# 12. PROFESSIONAL FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        background-color:#FFFFFF;
        border:1px solid #E4EAF2;
        border-radius:10px;
        padding:18px;
        text-align:center;
        color:#667085;
        font-size:12px;
    ">
        <b style="color:#173B75;">
            AI E-COMMERCE ANALYTICS
        </b>
        <br><br>
        Enterprise Business Intelligence Dashboard
        <br>
        Developed using Python | Pandas | Plotly |
        Streamlit | KMeans Machine Learning
        <br><br>
        Data Analytics & Customer Intelligence
    </div>
    """,
    unsafe_allow_html=True
)
