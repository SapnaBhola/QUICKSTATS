 
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# Load Data from Google Sheets
# ------------------------------
sheet_url = "https://docs.google.com/spreadsheets/d/1OsIgKuF8GUKn4QmpBSxTjcB6u2Iww03p/export?format=csv"

# Load with memory optimization
df = pd.read_csv(sheet_url, low_memory=False)

# ------------------------------
# Basic Cleaning (optional safety)
# ------------------------------
df = df.dropna(how="all")  # Drop completely empty rows
df.columns = df.columns.str.strip()  # Clean column names

# ------------------------------
# Streamlit Page Config
# ------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Excel-Style Interactive Dashboard")

# ------------------------------
# Sidebar Filters (like Excel Slicers)
# ------------------------------
st.sidebar.header("🔍 Filter Data")

# Create slicers dynamically (only for columns that exist)
year_col = 'Year' if 'Year' in df.columns else None
region_col = 'Region' if 'Region' in df.columns else None
category_col = 'Category' if 'Category' in df.columns else None

# Slicer 1 - Year
if year_col:
    selected_years = st.sidebar.multiselect(
        "Select Year:",
        sorted(df[year_col].dropna().unique()),
        default=sorted(df[year_col].dropna().unique())
    )
    df = df[df[year_col].isin(selected_years)]

# Slicer 2 - Region
if region_col:
    selected_regions = st.sidebar.multiselect(
        "Select Region:",
        sorted(df[region_col].dropna().unique()),
        default=sorted(df[region_col].dropna().unique())
    )
    df = df[df[region_col].isin(selected_regions)]

# Slicer 3 - Category
if category_col:
    selected_categories = st.sidebar.multiselect(
        "Select Category:",
        sorted(df[category_col].dropna().unique()),
        default=sorted(df[category_col].dropna().unique())
    )
    df = df[df[category_col].isin(selected_categories)]

# ------------------------------
# KPI Cards Section
# ------------------------------
st.markdown("### 🧮 Key Performance Indicators")
col1, col2, col3 = st.columns(3)

if 'Sales' in df.columns and 'Profit' in df.columns:
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_profit_margin = (df['Profit'].sum() / df['Sales'].sum()) * 100 if df['Sales'].sum() != 0 else 0

    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
    col3.metric("🧾 Avg Profit Margin", f"{avg_profit_margin:.2f}%")

# ------------------------------
# Charts Section
# ------------------------------
st.markdown("### 📊 Visual Analysis")

chart1, chart2, chart3 = st.columns(3)

# Chart 1 - Sales by Year
if year_col and 'Sales' in df.columns:
    fig1 = px.bar(df, x=year_col, y='Sales', title="Sales by Year", color='Sales')
    chart1.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Sales by Region
if region_col and 'Sales' in df.columns:
    fig2 = px.pie(df, names=region_col, values='Sales', title="Sales by Region")
    chart2.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Profit by Category
if category_col and 'Profit' in df.columns:
    fig3 = px.bar(df, x=category_col, y='Profit', title="Profit by Category", color='Profit')
    chart3.plotly_chart(fig3, use_container_width=True)

# ------------------------------
# Display Filtered Data Table
# ------------------------------
st.markdown("### 📄 Filtered Data Preview")
st.dataframe(df, use_container_width=True)

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.caption("📅 Data Source: Google Sheets | Developed by Sapna | Streamlit Dashboard")
