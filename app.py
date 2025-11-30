#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st
import pandas as pd

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Foodpanda Theme (Restored Simple Styling)
# -------------------------
# Restored simple CSS based on your last working version, 
# ensuring basic Foodpanda theme is applied.
FOODPANDA_THEME = """
<style>
/* Main app background (Simple Pink/Magenta) */
[data-testid="stAppViewContainer"] {
    background-color: rgba(215, 15, 100, 0.8) !important; 
    color: white !important; 
}

/* Pushes content down about 1.5 inches */
[data-testid="stApp"] {
    padding-top: 80px; 
}

/* Input labels (Username/Password) */
.stTextInput > label {
    color: white !important;
}

/* General button styling */
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

/* Titles and general text */
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
        # Placeholder for Image: Use a public URL or your local path "images/foodpanda_logo.png"
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
# Data Loading Function
# -------------------------
@st.cache_data
def load_data(file_path):
    """Loads the CSV data and performs initial cleaning."""
    df = pd.read_csv(file_path)
    
    # --- IMPORTANT DATA PREP ---
    # Convert date/time columns if they exist in your dataset
    # Example:
    # if 'Order Date' in df.columns:
    #     df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    
    # Ensure sales/revenue columns are numeric
    # Example:
    # if 'Total Price' in df.columns:
    #     df['Total Price'] = pd.to_numeric(df['Total Price'], errors='coerce')
        
    return df

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
    # 🚨🚨🚨 CHANGE THIS PATH TO YOUR ACTUAL CSV FILE PATH 🚨🚨🚨
    FILE_PATH = "/dataset.csv" 
    
    try:
        df = load_data(FILE_PATH)
        
        # ------------------------------------
        # SALES OVERVIEW CONTENT STARTS HERE
        # ------------------------------------
        
        st.subheader("Dataset Structure")
        st.write(f"Rows: **{df.shape[0]}**, Columns: **{df.shape[1]}**")
        st.dataframe(df.head(), use_container_width=True)
        
        # --- Add your KPIs and Charts below ---
        
        # st.header("Key Performance Indicators (KPIs)")
        # col_kpi_1, col_kpi_2, col_kpi_3 = st.columns(3)
        # 
        # with col_kpi_1:
        #     st.metric(label="Total Revenue", value=f"${df['Price'].sum():,.2f}")
            
    except FileNotFoundError:
        st.error(f"Error: The data file '{FILE_PATH}' was not found. Please check your file path.")
    except Exception as e:
        st.error(f"An unexpected error occurred during data processing: {e}")

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
