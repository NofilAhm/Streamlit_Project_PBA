#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Foodpanda Theme
# -------------------------
# Set the background color to a Foodpanda-like magenta/pink
# We target the main block and the sidebar block.
FOODPANDA_THEME = """
<style>
/* Change the primary background color */
.stApp {
    background-color: #D70F64; /* A vibrant magenta/pink */
    color: white; /* Ensure text is readable against the dark background */
}

/* Style the login box container (if we use a container/form) */
/* This targets the container holding the login elements for better contrast */
.stTextInput > div > div > input, .stButton > button, .stMarkdown {
    color: #444444; /* Dark text for inputs/buttons */
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
# Hardcoded users
# -------------------------
USERS = {
    "nofil": "12345",
    "admin": "admin123"
}

# -------------------------
# Initialize session state (Keep this at the top for first run setup)
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# -------------------------
# Login function
# -------------------------
def login():
    # Use empty space and columns to center the login block and push it down
    # The 'st.empty()' call below acts as the 1.5-inch vertical space
    st.empty() # Top vertical space
    st.empty() 
    
    # Create a layout with columns to center the login box
    col1, col2, col3 = st.columns([1, 1, 1]) 
    
    with col2:
        # 1. Add the small Foodpanda logo image (replace URL with your actual image/path)
        # Placeholder image URL for demonstration. In a real project, use a local file path 
        # (e.g., 'foodpanda_logo.png') and upload it to your GitHub repo.
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Foodpanda_logo.svg/320px-Foodpanda_logo.svg.png", 
                 width=100) # Adjusted for a small logo

        st.markdown("<h2 style='text-align: center; color: white;'>Dashboard Login</h2>", unsafe_allow_html=True)
        
        # We will use st.container to make the login box visually separate
        with st.container(border=True): # Use border for a distinct box
            # We use an alternative background color for the container 
            # by styling the inputs and title inside it to keep it legible.

            # Input fields inside the container
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
                    
    # The login page is complete within col2
    

# -------------------------
# Dashboard function
# -------------------------
def main_dashboard():
    # We must reset the background style for the dashboard content, 
    # otherwise it will inherit the Foodpanda pink background.
    st.markdown("""
        <style>
        .stApp {
            background-color: white; /* Set background back to white for dashboard */
            color: #333333;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # The sidebar will retain the original pink background due to the initial CSS, 
    # but the main canvas is set to white here for better data visualization contrast.
    
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")

    if st.sidebar.button("Logout"):
        st.session_state.clear() 
        st.rerun() 

    st.title("Foodpanda Sales Dashboard")
    st.write("Your dashboard content goes here…")
    # Add your data visualization code here

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
