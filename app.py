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
    st.title("Login Page")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully! Redirecting...")
            
            # 💡 THE FIX: Removed st.experimental_rerun() and added 'return'.
            # By adding 'return', we stop the current function execution 
            # after the state update. Streamlit will naturally trigger a rerun 
            # with the new state, which will take the user to the dashboard.
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
        st.session_state.clear()
        # You can keep st.experimental_rerun() for logout as it's a cleaner full reset
        # but a simple return here also usually works since the main logic handles the state.
        st.experimental_rerun()

    st.title("Foodpanda Sales Dashboard")
    st.write("Your dashboard content goes here…")
    # You can add charts, KPIs, filters here

# -------------------------
# App routing
# -------------------------
def main():
    if not st.session_state["logged_in"]:
        login()
    else:
        main_dashboard()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    main()


# In[ ]:




