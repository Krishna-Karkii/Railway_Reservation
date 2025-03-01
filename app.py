import streamlit as st
from login import login, signup
from admin_panel import admin_dashboard
from user_panel import user_dashboard

st.sidebar.title("🔗 Navigation")
page = st.sidebar.selectbox("Go to", ["Login", "Signup", "Admin Panel", "User Panel"])


if page == "Login":
    login()
elif page == "Signup":
    signup()
elif page == "Admin Panel":
    admin_dashboard()
elif page == "User Panel":
    user_dashboard()
