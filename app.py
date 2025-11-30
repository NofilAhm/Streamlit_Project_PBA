#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt
import numpy as np

# Initialize session state for navigation
if "current_tab" not in st.session_state:
    st.session_state["current_tab"] = "Sales Overview" # Default tab

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Styling and Readability
# -------------------------
FOODPANDA_THEME = """
<style>
/* 1. MAIN BACKGROUND: Transparent Foodpanda Pink */
[data-testid="stAppViewContainer"] {
    background-color: rgba(215, 15, 100, 0.8) !important; 
    color: #D70F64 !important; 
}

/* 2. PUSH CONTENT DOWN (Top Space Reduction on Main Content) */
[data-testid="stApp"] {
    padding-top: 0px !important; 
}

/* AGGRESSIVE FIX: Target the main content container to remove built-in padding */
[data-testid="stVerticalBlock"] {
    padding-top: 0px !important;
    margin-top: 0px !important;
}

/* 3. INPUT FIELD STYLING: FIXING READABILITY (White Box, Black Text) */
.stTextInput > div:first-child {
    background-color: white !important; 
    border-radius: 0.25rem; 
    padding: 0.5rem; 
}
.stTextInput > div > div > input {
    color: black !important; 
    background-color: transparent !important; 
    border: none !important; 
}

/* 4. Ensure input labels and titles are visible (Set to brand pink on pink background) */
.stTextInput > label, h1, h2, h3, h4, .stMarkdown {
    color: #D70F64 !important; 
}

/* 5. General Button Styling (Default) */
.stButton > button {
    background-color: #FFFFFF;
    border: 1px solid #D70F64;
    color: #D70F64 !important;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #FF5A93;
    color: white !important; 
}

/* KPI LABEL FIX: Large, bold titles for metrics */
[data-testid="stMetricLabel"] {
    font-size: 1.35rem !important; 
    font-weight: bold !important; 
    color: #333333 !important; 
}
[data-testid="stMetricLabel"] div {
    font-size: 1.35rem !important; 
    font-weight: bold !important; 
    color: #333333 !important; 
}

/* Sidebar Styling for Spacing and Font Color */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 10px !important; 
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4, 
[data-testid="stSidebar"] .stMarkdown {
    color: white !important; 
}

/* Login Dashboard Title Styling (White text on pink background) */
.login-title {
    color: white !important; 
    text-align: center;
    font-size: 2em;
    font-weight: bold;
}

</style>
"""
st.markdown(FOODPANDA_THEME, unsafe_allow_html=True)

# -------------------------
# Hardcoded users & Session State
# -------------------------
USERS = {
    "nofil": "12345",
    "admin": "admin123"
}

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# -------------------------
# Login function 
# -------------------------
def login():
    col1, col2, col3 = st.columns([1, 1, 1]) 
    
    with col2:
        st.markdown("<h2 class='login-title'>FOODPANDA SALES DASHBOARD</h2>", unsafe_allow_html=True)
        
        with st.container(border=True): 
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login", use_container_width=True):
                if username in USERS and USERS[username] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("Logged in successfully! Redirecting...")
                    st.rerun()
                    return 
                else:
                    st.error("Invalid username or password")
                    
# -------------------------
# Data Loading and Preparation Function
# -------------------------
@st.cache_data
def load_data():
    """Loads, cleans, and engineers features for the sales dashboard."""
    
    DATA_FILE = Path(__file__).parent / "dataset" 

    try:
        df = pd.read_csv(DATA_FILE)
        
        # --- DATA CLEANING & FEATURE ENGINEERING ---
        DATE_COLUMNS = ['signup_date', 'order_date', 'last_order_date', 'rating_date']
        for col in DATE_COLUMNS:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
        
        # Age column is treated as text/categorical data (Age Groups)
            
        df['sales'] = df['quantity'] * df['price']
        
        df['Order_Day'] = df['order_date'].dt.normalize()
        df['DayOfWeek'] = df['order_date'].dt.day_name()
        
        # Ensure essential columns are clean
        df.dropna(subset=['order_id', 'order_date', 'sales', 'customer_id'], inplace=True)
        
        return df

    except Exception as e:
        st.error(f"Failed to load or process data from '{DATA_FILE}'. Error: {e}")
        return pd.DataFrame() 

# -------------------------
# Tab Content Functions
# -------------------------

def show_sales_overview(df):
    """Generates the content for the Sales Overview tab."""
    ORDER_COL = 'order_id' 
    PRICE_COL = 'sales'

    st.title("Foodpanda Sales Overview Dashboard 🐼")
    st.write("---")
    
    if ORDER_COL in df.columns and PRICE_COL in df.columns:
        
        total_revenue = df[PRICE_COL].sum()
        total_orders = df[ORDER_COL].nunique()
        average_order_value = total_revenue / total_orders if total_orders else 0
        
        st.header("Sales Overview")
        st.subheader("Key Performance Indicators (KPIs) for All Time")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
        with kpi_col2:
            st.metric(label="📦 Total Orders", value=f"{total_orders:,}")
        with kpi_col3:
            st.metric(label="💸 Average Order Value (AOV)", value=f"${average_order_value:,.2f}")
        
        st.write("---")
    
    # MONTH-WISE SALES CHART
    if 'order_date' in df.columns and PRICE_COL in df.columns:
        st.subheader("Monthly Revenue Trend (Month and Year)")
        
        df['Order_Month_Date'] = df['order_date'].dt.to_period('M').dt.start_time
        
        monthly_sales = df.groupby('Order_Month_Date')[PRICE_COL].sum().reset_index()
        monthly_sales.columns = ['Month', 'Total Sales']

        chart = alt.Chart(monthly_sales).mark_line(point=True, color='#D70F64').encode(
            x=alt.X('Month:T', 
                    axis=alt.Axis(title='Month and Year', format='%b %Y')),
            y=alt.Y('Total Sales:Q', axis=alt.Axis(title='Total Revenue ($)')),
            tooltip=[alt.Tooltip('Month', format='%b %Y'), alt.Tooltip('Total Sales', format='$,.2f')]
        ).properties(
            title='Monthly Revenue Over Time'
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        st.write("---")
    else:
        st.warning("Cannot generate monthly sales chart. Check 'order_date' and 'sales' columns.")

def show_customer_overview(df):
    """Generates the content for the Customer Overview tab, including KPIs and Charts."""
    CUST_COL = 'customer_id' 
    PRICE_COL = 'sales'
    DATE_COL = 'order_date'
    AGE_GROUP_COL = 'age' 

    st.title("Customer Overview Dashboard 👥")
    st.write("---")
    
    if CUST_COL in df.columns and PRICE_COL in df.columns and DATE_COL in df.columns:
        
        # --- KPI Calculations ---
        total_customers = df[CUST_COL].nunique()
        total_revenue = df[PRICE_COL].sum()
        
        sales_per_customer = total_revenue / total_customers if total_customers else 0
        
        present_date = df[DATE_COL].max()
        last_order_df = df.groupby(CUST_COL)[DATE_COL].max().reset_index()
        last_order_df['days_since_last_order'] = (present_date - last_order_df[DATE_COL]).dt.days
        CHURN_THRESHOLD_DAYS = 180
        churned_customers = last_order_df[last_order_df['days_since_last_order'] > CHURN_THRESHOLD_DAYS][CUST_COL].count()
        churn_rate_percent = (churned_customers / total_customers) * 100 if total_customers else 0
        
        # --- KPI Display ---
        st.header("Customer KPIs")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            st.metric(label="👥 Total Customers", value=f"{total_customers:,}")
        with kpi_col2:
            st.metric(label="💸 Sales Per Customer (ACV)", value=f"${sales_per_customer:,.2f}")
        with kpi_col3:
            st.metric(
                label="📉 Customer Churn Rate", 
                value=f"{churn_rate_percent:.2f}%",
                help=f"Customers are considered churned if they have not ordered in the last {CHURN_THRESHOLD_DAYS} days."
            )
        
        st.write("---")

        # --- Chart Section ---
        st.header("Customer Demographics and Payment Analysis")
        chart_col1, chart_col2 = st.columns(2)

        # 1. Bar Chart: Payment Method Analysis (Left Column)
        with chart_col1:
            if 'payment_method' in df.columns and PRICE_COL in df.columns:
                payment_sales = df.groupby('payment_method')[PRICE_COL].sum().reset_index()
                payment_sales.columns = ['Payment Method', 'Total Sales']
                
                st.subheader("Total Sales by Payment Method")
                
                bar_chart = alt.Chart(payment_sales).mark_bar(color='#D70F64').encode(
                    x=alt.X('Total Sales:Q', title='Total Revenue ($)'),
                    y=alt.Y('Payment Method:N', title='Payment Method', sort='-x'),
                    tooltip=['Payment Method', alt.Tooltip('Total Sales', format='$,.0f')]
                ).properties(
                    height=300
                ).interactive()
                st.altair_chart(bar_chart, use_container_width=True)
            else:
                st.info("Cannot show Payment Method chart. Missing 'payment_method' column.")


        # 2. Pie Chart: Age Distribution (Right Column) - ENHANCED
        with chart_col2:
            if AGE_GROUP_COL in df.columns and CUST_COL in df.columns:
                
                customer_age = df[[CUST_COL, AGE_GROUP_COL]].drop_duplicates(subset=[CUST_COL]).dropna(subset=[AGE_GROUP_COL])
                
                if not customer_age.empty:
                    
                    age_counts = customer_age.groupby(AGE_GROUP_COL)[CUST_COL].count().reset_index()
                    age_counts.columns = ['Age Group', 'Customer Count']
                    
                    # Calculate Percentage
                    total_customers_in_chart = age_counts['Customer Count'].sum()
                    age_counts['Percentage'] = (age_counts['Customer Count'] / total_customers_in_chart) * 100
                    
                    st.subheader("Customer Distribution by Age Group")

                    pie_chart = alt.Chart(age_counts).encode(
                        theta=alt.Theta("Customer Count", stack=True)
                    ) 
                    
                    color_scale = alt.Scale(range=['#D70F64', '#FF5A93', '#FF8CC6', '#6A053F', '#9C0A52'])

                    arc = pie_chart.mark_arc(outerRadius=120, innerRadius=30).encode(
                        color=alt.Color("Age Group:N", scale=color_scale),
                        order=alt.Order("Customer Count", sort="descending"),
                        # 🚨 FIX APPLIED HERE: Using alt.Tooltip correctly with format and title
                        tooltip=[
                            "Age Group", 
                            "Customer Count", 
                            alt.Tooltip('Percentage', format='.2f', title='Contribution (%)') # Using title to add clarity to the percentage
                        ] 
                    )
                    
                    # Create the formatted label for the chart text
                    age_counts['formatted_label'] = age_counts.apply(
                        lambda row: f"{row['Customer Count']} ({row['Percentage']:.1f}%)", axis=1
                    )
                    
                    text = alt.Chart(age_counts).mark_text(radius=140, fill="black", fontSize=14).encode(
                        text=alt.Text("formatted_label:N"),
                        order=alt.Order("Customer Count", sort="descending"),
                        color=alt.value("black")
                    )

                    final_pie = arc + text
                    
                    st.altair_chart(final_pie, use_container_width=True)
                    
                else:
                    st.info(f"Age Group data is missing for unique customers.")
            else:
                st.info(f"Cannot show Age Distribution chart. Missing '{AGE_GROUP_COL}' or '{CUST_COL}' column.")
        
        st.write("---") 
    else:
        st.warning("Customer KPIs cannot be calculated. Ensure 'customer_id', 'sales', and 'order_date' columns exist.")


def show_product_overview(df):
    st.title("Product Overview Dashboard 🍔")
    st.write("---")
    st.info("Content coming soon! This tab will analyze best-selling items and categories.")


# -------------------------
# Main Dashboard Function
# -------------------------
def main_dashboard():
    # Reset background theme for the main dashboard content area
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: white !important; 
            color: #333333 !important;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(215, 15, 100, 0.8) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    df = load_data() 
    if df.empty:
        st.warning("Data loading failed. Please check file path and data format.")
        return

    # --- Sidebar Setup ---
    st.sidebar.title("Dashboard Menu")
    st.sidebar.markdown(f"**Welcome, {st.session_state['username']}**")
    
    # Logout Button
    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.clear() 
        st.rerun() 
        
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    
    # --- Tab Buttons ---
    TAB_NAMES = ["Sales Overview", "Customer Overview", "Product Overview"]
    current_tab = st.session_state["current_tab"]
    
    def nav_button(label, current_tab):
        if st.sidebar.button(label, use_container_width=True, key=f"nav_{label}"):
            st.session_state["current_tab"] = label
            st.rerun()
            
        if current_tab == label:
            st.sidebar.markdown(
                f"""
                <style>
                    [data-testid="stSidebar"] button[kind="secondary"][key="nav_{label}"] {{
                        background-color: white !important;
                        color: #D70F64 !important;
                        border: 2px solid white !important;
                        font-weight: bold;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )

    for tab in TAB_NAMES:
        nav_button(tab, current_tab)


    # --- Content Routing ---
    if st.session_state["current_tab"] == "Sales Overview":
        show_sales_overview(df)
    elif st.session_state["current_tab"] == "Customer Overview":
        show_customer_overview(df)
    elif st.session_state["current_tab"] == "Product Overview":
        show_product_overview(df)


# -------------------------
# App routing
# -------------------------
def main():
    if not st.session_state.get("logged_in", False):
        login()
    else:
        main_dashboard()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    main()
