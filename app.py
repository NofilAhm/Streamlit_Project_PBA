#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
# ... (USERS and session state initialization remains the same) ...

# -------------------------
# Login function (REVERTED TO BUTTON & INPUTS)
# -------------------------
def login():
    st.title("Login Page")
    
    # Use simple elements instead of st.form to avoid key conflicts
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully! Redirecting...")
            
            # Use st.rerun() (the modern, stable version) and then return 
            # to ensure the script stops the current execution immediately.
            st.rerun()
            return # This is a failsafe

        else:
            st.error("Invalid username or password")

# -------------------------
# Dashboard function (Using st.rerun() for consistency)
# -------------------------
def main_dashboard():
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun() # Use st.rerun() instead of st.experimental_rerun()

    st.title("Foodpanda Sales Dashboard")
    st.write("Your dashboard content goes here…")
    # ... (Add your dashboard code here) ...

# -------------------------
# App routing (Remains the same)
# -------------------------
def main():
    if not st.session_state["logged_in"]:
        login()
    else:
        main_dashboard()

# -------------------------
# Run app (Remains the same)
# -------------------------
if __name__ == "__main__":
    main()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    main()


# In[ ]:




