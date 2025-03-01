import streamlit as st
from login import login, signup
from admin_panel import admin_dashboard
from user_panel import user_dashboard
from database import initialize_database

# Initialize the database
initialize_database()

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

st.sidebar.title("🔗 Navigation")

# Sidebar navigation
if st.session_state.get("user") is None:
    page = st.sidebar.selectbox("Go to", ["Login", "Signup"])
else:
    # Show logout button if the user is logged in
    if st.sidebar.button("Logout"):
        # Clear the session state and redirect to the login page
        st.session_state.clear()
        st.session_state["page"] = "Login"
        st.rerun()  # Rerun the app to reflect the changes

    # Show the appropriate panel based on the user's role
    page = st.session_state["page"]

if page == "Login":
    login()
elif page == "Signup":
    signup()
elif page == "Admin Panel":
    admin_dashboard()
elif page == "User Panel":
    user_dashboard()