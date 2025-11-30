#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st

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
    st.title("Login Page")
    
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully! Redirecting...")
            
            # Use st.rerun() and return for a clean transition
            st.rerun()
            return 

        else:
            st.error("Invalid username or password")

# -------------------------
# Dashboard function
# -------------------------
def main_dashboard():
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")

    if st.sidebar.button("Logout"):
        # This clears all keys, including 'logged_in' and 'username'
        st.session_state.clear() 
        st.rerun() # Forces the script to rerun from the top

    st.title("Foodpanda Sales Dashboard")
    st.write("Your dashboard content goes here…")

# -------------------------
# App routing (FIXED)
# -------------------------
def main():
    # 💡 THE FIX: Use .get() to safely check the state.
    # If 'logged_in' is missing (like after a logout/clear), it defaults to False,
    # preventing the KeyError and correctly sending the user to the login page.
    if not st.session_state.get("logged_in", False):
        login()
    else:
        main_dashboard()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    main()

