#!/usr/bin/env python
# coding: utf-8

# In[1]:


# app.py
import streamlit as st
from login_module import login  # your login code in a separate file

# --------------------------
# Main dashboard function
# --------------------------
def main_dashboard():
    st.sidebar.title("Dashboard Menu")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    st.title("Sales Dashboard")
    st.write("This is your main dashboard content…")
    st.write("You can add charts, KPIs, filters here.")

# --------------------------
# Routing logic
# --------------------------
def main():
    if "logged_in" not in st.session_state:
        login()  # show login page
    else:
        main_dashboard()  # show dashboard

if __name__ == "__main__":
    main()


# In[ ]:




