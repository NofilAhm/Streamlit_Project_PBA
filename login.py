#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st

# -------------------------
# Hardcoded users (can expand later)
# -------------------------
USERS = {
    "nofil": "12345",   # username: password
    "admin": "admin123"
}

# -------------------------
# Login function
# -------------------------
def login():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

# -------------------------
# Main protected dashboard
# -------------------------
def main_dashboard():
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    st.title("Sales Dashboard")
    st.write("Your dashboard goes here...")

# -------------------------
# Page router
# -------------------------
def main():
    if "logged_in" not in st.session_state:
        login()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()


# In[ ]:




