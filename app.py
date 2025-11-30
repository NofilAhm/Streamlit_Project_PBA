#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
import pandas as pd
from pathlib import Path

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Reliable Styling and Readability (FINAL FIX)
# -------------------------
FOODPANDA_THEME = """
<style>
/* 1. MAIN BACKGROUND: Transparent Foodpanda Pink */
[data-testid="stAppViewContainer"] {
    background-color: rgba(215, 15, 100, 0.8) !important; 
    color: white !important; 
}

/* 2. PUSH CONTENT DOWN (1.5 inches) */
[data-testid="stApp"] {
    padding-top: 80px; 
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

/* 4. Ensure input labels and titles are visible (White text on pink background) */
.stTextInput > label, h1, h2, h3, h4, .stMarkdown {
    color: white !important;
}

/* 5. General Button Styling */
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

/* 🚨 FINAL FIX: Increase size and bold the KPI metric labels (Targets the label element) */
[data-testid="stMetricLabel"] {
    font-size: 1.35rem !important; /* Forces a larger size */
    font-weight: bold !important; 
    color: #333333 !important; /* Dark text for visibility on the white dashboard background */
}
/* Targets the inner div holding the label text as a secondary measure */
[data-testid="stMetricLabel"] div {
    font-size: 1.35rem !important; 
    font-weight: bold !important; 
    color: #333333 !important; 
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
# Data Loading and Preparation Function (ROBUST & CLEANED)
# -------------------------
@st.cache_data
def load_data():
    """Loads, cleans, and engineers features for the sales dashboard."""
    
    # Assumes file is named EXACTLY 'dataset' and is in the same folder.
    DATA_FILE = Path(__file__).parent / "dataset" 

    try:
        df = pd.read_csv(DATA_FILE)
        
        # --- DATA CLEANING & FEATURE ENGINEERING ---
        
        # 1. Date Conversions
        DATE_COLUMNS = ['signup_date', 'order_date', 'last_order_date', 'rating_date']
        for col in DATE_COLUMNS:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
        # 2. Ensure Price and Quantity are numeric
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
            
        # 3. Calculate Sales (Revenue per item)
        df['sales'] = df['quantity'] * df['price']
        
        # 4. Create Time-Based Features for Charts
        df['Order_Day'] = df['order_date'].dt.normalize() # Day only (no time component)
        df['Order_Month'] = df['order_date'].dt.to_period('M').astype(str)
        df['DayOfWeek'] = df['order_date'].dt.day_name()
        
        # 5. Drop rows where essential data is missing
        df.dropna(subset=['order_id', 'order_date', 'sales'], inplace=True)
        
        return df

    except Exception as e:
        st.error(f"Failed to load or process data from '{DATA_FILE}'. Error: {e}")
        return pd.DataFrame() 

# -------------------------
# Dashboard function
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
    
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        st.session_state.clear() 
        st.rerun() 

    st.title("Foodpanda Sales Overview Dashboard 🐼")
    st.write("---")

    # Load the data
    df = load_data() 
    
    if df.empty:
        st.warning("Data loading failed. Please check file path and data format.")
        return

    # ------------------------------------
    # KPI Implementation
    # ------------------------------------
    ORDER_COL = 'order_id' 
    PRICE_COL = 'sales'

    if ORDER_COL in df.columns and PRICE_COL in df.columns:
        
        # Calculate metrics
        total_revenue = df[PRICE_COL].sum()
        total_orders = df[ORDER_COL].nunique()
        average_order_value = total_revenue / total_orders if total_orders else 0
        
        st.header("Key Performance Indicators (KPIs) for All Time")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
            # The label here will be styled by the new CSS rule
            st.metric(
                label="💰 Total Revenue", 
                value=f"${total_revenue:,.2f}"
            )
        
        with kpi_col2:
            st.metric(
                label="📦 Total Orders", 
                value=f"{total_orders:,}"
            )

        with kpi_col3:
            st.metric(
                label="💸 Average Order Value (AOV)", 
                value=f"${average_order_value:,.2f}"
            )
        
        st.write("---")
    
    else:
        st.warning(f"Required columns ('{ORDER_COL}' or '{PRICE_COL}') not found after data loading. Check your file.")
        
    # Display raw data preview 
    st.subheader("Raw Data Preview")
    st.write(f"Rows: **{df.shape[0]}**, Columns: **{df.shape[1]}**")
    st.dataframe(df.head(), use_container_width=True)

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
