#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
import pandas as pd
from pathlib import Path
import altair as alt

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
    padding-top: 20px !important; 
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
    padding-top: 10px !important; /* Reduced top space */
}
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4, 
[data-testid="stSidebar"] .stMarkdown {
    color: white !important; /* White font color */
}

/* The styling for the active tab button will be applied dynamically in Python */

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
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Foodpanda_logo.svg/320px-Foodpanda_logo.svg.png", 
                 width=100) 

        st.markdown("<h2 style='text-align: center;'>Dashboard Login</h2>", unsafe_allow_html=True)
        
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
            
        df['sales'] = df['quantity'] * df['price']
        
        df['Order_Day'] = df['order_date'].dt.normalize()
        df['DayOfWeek'] = df['order_date'].dt.day_name()
        
        df.dropna(subset=['order_id', 'order_date', 'sales'], inplace=True)
        
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
        
        # KPI Calculations
        total_revenue = df[PRICE_COL].sum()
        total_orders = df[ORDER_COL].nunique()
        average_order_value = total_revenue / total_orders if total_orders else 0
        
        # KPI Display
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
    st.title("Customer Overview Dashboard 👥")
    st.write("---")
    st.info("Content coming soon! This tab will analyze customer segments and lifetime value.")

def show_product_overview(df):
    st.title("Product Overview Dashboard 🍔")
    st.write("---")
    st.info("Content coming soon! This tab will analyze best-selling items and categories.")


# -------------------------
# Main Dashboard Function (FIXED ROUTING LOGIC)
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
    
    # --- Tab Buttons (STABLE LOGIC) ---
    TAB_NAMES = ["Sales Overview", "Customer Overview", "Product Overview"]
    current_tab = st.session_state["current_tab"]
    
    # Function to create a standard Streamlit button and apply custom styling based on state
    def nav_button(label, current_tab):
        # 1. Check if the button is clicked
        if st.sidebar.button(label, use_container_width=True, key=f"nav_{label}"):
            st.session_state["current_tab"] = label
            st.rerun()
            
        # 2. If it's the current active tab, inject CSS to change its appearance
        if current_tab == label:
            st.sidebar.markdown(
                f"""
                <style>
                    /* Target the specific button by its key (used in st.button) */
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

    # Render the navigation buttons using the stable function
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
