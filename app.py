#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Foodpanda Theme
# -------------------------
# The background color is now RGBA: rgb(215, 15, 100) with 80% opacity (0.8 alpha)
FOODPANDA_THEME = """
<style>
/* Change the primary background color */
.stApp {
    background-color: rgba(215, 15, 100, 0.8); /* Foodpanda Pink (80% opacity) */
    color: white; /* Ensure general text is white */
}

/* 💡 CHANGE 1: Make input text white (Targets the actual input field) */
.stTextInput > div > div > input {
    color: white !important; 
    background-color: rgba(255, 255, 255, 0.1); /* Slightly transparent background for fields */
    border: 1px solid white; 
}

/* Style for the labels and general markdown text */
.stMarkdown {
    color: white !important; 
}

/* Style the buttons */
.stButton > button {
    background-color: #FFFFFF; /* White button */
    border: 1px solid #D70F64;
    color: #D70F64 !important; /* Foodpanda pink text */
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #FF5A93; /* Lighter pink on hover */
    color: white !important; 
}
</style>
"""

# Apply the custom CSS
st.markdown(FOODPANDA_THEME, unsafe_allow_html=True)


# -------------------------
# Hardcoded users (UNCHANGED)
# -------------------------
USERS = {
    "nofil": "12345",
    "admin": "admin123"
}

# -------------------------
# Initialize session state (UNCHANGED)
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# -------------------------
# Login function (SLIGHTLY MODIFIED INPUT STYLING)
# -------------------------
def login():
    # Use empty space and columns to center the login block and push it down
    st.empty() # Top vertical space
    st.empty() 
    
    # Create a layout with columns to center the login box
    col1, col2, col3 = st.columns([1, 1, 1]) 
    
    with col2:
        # Placeholder image URL 
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Foodpanda_logo.svg/320px-Foodpanda_logo.svg.png", 
                 width=100) 

        # Title is now white thanks to global CSS
        st.markdown("<h2 style='text-align: center;'>Dashboard Login</h2>", unsafe_allow_html=True)
        
        with st.container(border=True): 
            # Input fields are here - text color is controlled by CSS above
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
# Dashboard function (UNCHANGED)
# -------------------------
def main_dashboard():
    # Reset the background style for the dashboard content
    st.markdown("""
        <style>
        .stApp {
            background-color: white; /* Set dashboard background back to solid white */
            color: #333333;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")

    if st.sidebar.button("Logout"):
        st.session_state.clear() 
        st.rerun() 

    st.title("Foodpanda Sales Dashboard")
    st.write("Your dashboard content goes here…")
    # Add your data visualization code here

# -------------------------
# App routing (UNCHANGED)
# -------------------------
def main():
    if not st.session_state.get("logged_in", False):
        login()
    else:
        main_dashboard()

# -------------------------
# Run app (UNCHANGED)
# -------------------------
if __name__ == "__main__":
    main()
