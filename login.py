import mysql.connector
import streamlit as st
from database import get_db_connection
from utils import hash_password, check_password


def login():
    """User & Admin Login"""
    st.subheader("Railway Reservation System")
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password(user["password_hash"], password):
            st.session_state["user"] = user
            st.success(f"Welcome, {username}!")

            # Redirect based on role
            if user["role"] == "admin":
                st.session_state["page"] = "Admin Panel"
            else:
                st.session_state["page"] = "User Panel"

            st.rerun()
        else:
            st.error("Invalid username or password!")

def signup():

    st.title("📝Signup")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, hash_password(password), 'user')  # Role is always 'user'
            )
            conn.commit()
            st.success("Signup successful! Please log in.")

        except mysql.connector.Error as err:
            if err.errno == 1062:
                st.error("Username already exists!")
            else:
                st.error(f"An error occurred: {err}")
        finally:
            conn.close()