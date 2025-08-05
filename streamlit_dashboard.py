import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="FootWare Sales Dashboard", layout="wide")

# Title
st.title("👟 FootWare Sales Analytics Dashboard")

# Load & preprocess data
df = pd.read_csv("FootWare_Wholesale_Sales_Dataset.csv")

# Cleaning and preprocessing
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)

# Ensure numeric columns are correct
df['Total Revenue (₹)'] = pd.to_numeric(df['Total Revenue (₹)'], errors='coerce')
df['Quantity Sold'] = pd.to_numeric(df['Quantity Sold'], errors='coerce')
df['Unit Price (₹)'] = pd.to_numeric(df['Unit Price (₹)'], errors='coerce')

# KPI Metrics
total_revenue = df['Total Revenue (₹)'].sum()
total_units = df['Quantity Sold'].sum()
avg_order_value = total_revenue / total_units

# Sidebar
chart_type = st.sidebar.radio("📊 Select Visualization", 
                              ["📄 Show Dataset", "📌 KPI Metrics", 
                               "📍 Bar Chart: Sales by City", 
                               "📈 Line Chart: Monthly Sales Trend", 
                               "🥧 Pie Chart: Revenue by Product"])

# Show dataset
if chart_type == "📄 Show Dataset":
    st.subheader("📋 Raw FootWare Sales Data")
    st.dataframe(df)

# KPI Metrics
elif chart_type == "📌 KPI Metrics":
    st.subheader("📊 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("📦 Units Sold", f"{total_units:,}")
    col3.metric("📈 Avg. Order Value", f"₹{avg_order_value:.2f}")

# Bar Chart
elif chart_type == "📍 Bar Chart: Sales by City":
    st.subheader("🏙️ Total Revenue by City")
    city_sales = df.groupby('Dealer Location')['Total Revenue (₹)'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    city_sales.plot(kind='bar', color='cornflowerblue', ax=ax)
    ax.set_title("Total Revenue by Dealer Location", fontsize=14)
    ax.set_xlabel("City")
    ax.set_ylabel("Revenue (₹)")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Line Chart
elif chart_type == "📈 Line Chart: Monthly Sales Trend":
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = df.groupby('YearMonth')['Total Revenue (₹)'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(monthly_sales['YearMonth'], monthly_sales['Total Revenue (₹)'], 
            marker='o', linestyle='-', color='darkorange')
    ax.set_title("Monthly Revenue Trend", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue (₹)")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Pie Chart
elif chart_type == "🥧 Pie Chart: Revenue by Product":
    st.subheader("🥧 Revenue Share by Product Type")
    product_sales = df.groupby('Product')['Total Revenue (₹)'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = plt.cm.viridis(range(100, 100 + len(product_sales)*20, 20))
    ax.pie(product_sales['Total Revenue (₹)'], 
           labels=product_sales['Product'], 
           autopct='%1.1f%%', 
           startangle=140, 
           colors=colors,
           wedgeprops={'edgecolor': 'white'})
    ax.set_title('Revenue Distribution by Product Type', fontsize=14, fontweight='bold')
    st.pyplot(fig)
