#!/usr/bin/env python
# coding: utf-8

# In[1]:
import streamlit as st

# Set the page configuration to wide layout
st.set_page_config(layout="wide") 

# -------------------------
# Custom CSS for Foodpanda Theme (Revised Text Color)
# -------------------------
FOODPANDA_THEME = """
<style>
/* 1. AGGRESSIVE BACKGROUND COLOR FIX (20% transparent Foodpanda Pink) */
[data-testid="stAppViewContainer"] {
    background-color: rgba(215, 15, 100, 0.8) !important; 
    color: white !important; /* General text remains white for contrast */
}

/* 2. CENTER THE MAIN CONTENT VERTICALLY AND HORIZONTALLY */
[data-testid="stApp"] {
    padding-top: 80px; /* Pushes content down about 1.5 inches */
}

/* 3. INPUT FIELD STYLING */
/* Targets the actual input element */
.stTextInput > div > div > input {
    color: black !important; /* 💡 FIX: Forces input text to be BLACK */
    background-color: transparent !important; /* Makes input field background transparent */
    border: 1px solid white !important; 
}

/* 4. Ensure input labels (Username, Password) are white */
.stTextInput > label {
    color: white !important;
}

/* 5. Style the login button */
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

/* 6. Ensure titles and general text remain white */
h1, h2, h3, h4, .stMarkdown {
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
# Login function (UNCHANGED)
# -------------------------
def login():
    # Create a layout with columns to center the login box
    col1, col2, col3 = st.columns([1, 1, 1]) 
    
    with col2:
        # 1. Add the small Foodpanda logo image
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
# Dashboard function (UNCHANGED)
# -------------------------
def main_dashboard():
    # RESET THEME FOR DASHBOARD CONTENT
    st.markdown("""
        <style>
        /* Set background back to solid white for the dashboard */
        [data-testid="stAppViewContainer"] {
            background-color: white !important; 
            color: #333333 !important;
        }
        /* Ensure sidebar keeps the pink color if you want it */
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

    st.title("Foodpanda Sales Dashboard")
    st.write("Your dashboard content goes here…")

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
