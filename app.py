#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
import pandas as pd
from pathlib import Path

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Reliable Styling
# -------------------------
# This CSS is designed to be highly specific to fix the input box readability.
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

/* 3. INPUT FIELD STYLING: FIXING READABILITY */
/* Target the immediate container around the input */
.stTextInput > div:first-child {
    background-color: white !important; /* Solid white background for clear readability */
    border-radius: 0.25rem; 
    padding: 0.5rem; 
}

/* Targets the actual input element */
.stTextInput > div > div > input {
    color: black !important; /* Input text is BLACK */
    background-color: transparent !important; /* Make the input field transparent to show white container */
    border: none !important; 
}

/* 4. Ensure input labels (Username/Password) are white */
.stTextInput > label {
    color: white !important;
}

/* 5. General Styling for Buttons and Titles */
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
h1, h2, h3, h4, .stMarkdown {
    color: white !important;
}
</style>
"""

# Apply the custom CSS
st.markdown(FOODPANDA_THEME, unsafe_allow_html=True)

# -------------------------
# Hardcoded users
# -------------------------
USERS = {
    "nofil": "12345",
    "admin": "admin123"
}

# -------------------------
# Initialize session state
# -------------------------
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
        # Placeholder for Image: Use a public URL for reliable loading
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
# Data Loading Function (FIXED PATH)
# -------------------------
@st.cache_data
def load_data():
    """Loads the CSV data using an absolute path relative to the script location."""
    
    # 🚨 FIX: Use pathlib to construct the absolute path relative to app.py
    DATA_FILE = Path(__file__).parent / "dataset" 

    try:
        df = pd.read_csv(DATA_FILE)
        
        # -------------------
        # DATA PREP PLACEHOLDER
        # -------------------
        # Example: Convert relevant columns to correct types
        # if 'OrderDate' in df.columns:
        #     df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

        return df

    except Exception as e:
        st.error(f"Failed to load data from {DATA_FILE}. Please ensure 'dataset.csv' is in the same folder as app.py.")
        # st.exception(e) # Uncomment this if you want to see the full Python error
        return pd.DataFrame() # Return empty DataFrame on failure

# -------------------------
# Dashboard function (KPIs Included)
# -------------------------
def main_dashboard():
    # Reset background theme for the main dashboard content area
    st.markdown("""
        <style>
        /* Reset main area to solid white */
        [data-testid="stAppViewContainer"] {
            background-color: white !important; 
            color: #333333 !important;
        }
        /* Keep sidebar pink */
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
    
    # Check if the DataFrame loaded successfully
    if df.empty:
        st.warning("Cannot display dashboard content without data.")
        return

    # ------------------------------------
    # KPI Implementation
    # ------------------------------------
    ORDER_COL = 'Order ID'  # 🚨 REPLACE with your actual Order ID column name
    PRICE_COL = 'Total Price'     # 🚨 REPLACE with your actual Price/Amount column name

    if ORDER_COL in df.columns and PRICE_COL in df.columns:
        
        # Data Cleaning for calculation robustness
        df_clean = df.dropna(subset=[ORDER_COL, PRICE_COL]).copy()
        # Ensure Price column is numeric (important for calculation)
        df_clean[PRICE_COL] = pd.to_numeric(df_clean[PRICE_COL], errors='coerce').fillna(0) 

        # Calculate metrics
        total_revenue = df_clean[PRICE_COL].sum()
        total_orders = df_clean[ORDER_COL].nunique()
        average_order_value = total_revenue / total_orders if total_orders else 0
        
        st.header("Key Performance Indicators (KPIs) for All Time")
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        
        with kpi_col1:
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
        st.warning(f"Required columns ('{ORDER_COL}' or '{PRICE_COL}') not found in the dataset. Please update the column names in the code.")
        
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
