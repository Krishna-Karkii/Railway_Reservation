import streamlit as st
import pandas as pd
from database import get_db_connection

def user_dashboard():
    """User Panel for Viewing, Booking & Cancelling Reservations"""
    if "user" not in st.session_state or st.session_state["user"]["role"] != "user":
        st.warning("Unauthorized! Please log in as a user.")
        return

    st.sidebar.title("🚆 User")
    action = st.sidebar.selectbox("Choose Action", ["View Trains", "Book a Train", "Cancel Reservation"])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if action == "View Trains":
        st.header("🚄 Available Trains")
        trains = pd.read_sql("SELECT * FROM trains", conn)
        st.dataframe(trains)

    elif action == "Book a Train":
        st.header("🎫 Book a Train Ticket")

        trains = pd.read_sql("SELECT * FROM trains", conn)
        st.dataframe(trains)

        train_id = st.number_input("Enter Train ID", min_value=1)
        seats_to_book = st.number_input("Seats to Book", min_value=1)

        if st.button("Book Ticket"):
            cursor.execute("SELECT * FROM trains WHERE id = %s", (train_id,))
            train = cursor.fetchone()

            if train:
                if train["seats"] >= seats_to_book:
                    total_fare = train["fare"] * seats_to_book

                    cursor.execute(
                        "INSERT INTO reservations (user_id, train_id, seats_booked, total_fare) VALUES (%s, %s, %s, %s)",
                        (st.session_state["user"]["id"], train_id, seats_to_book, total_fare)
                    )
                    cursor.execute("UPDATE trains SET seats = seats - %s WHERE id = %s", (seats_to_book, train_id))
                    conn.commit()
                    st.rerun()
                else:
                    st.error("Not enough seats available.")
            else:
                st.error("Invalid Train ID.")

    elif action == "Cancel Reservation":
        st.header("❌ Cancel Reservation")

        reservations = pd.read_sql(f"SELECT * FROM reservations WHERE user_id = {st.session_state['user']['id']}", conn)
        st.dataframe(reservations)

        res_id = st.number_input("Enter Reservation ID", min_value=1)

        if st.button("Cancel Reservation"):
            cursor.execute("SELECT * FROM reservations WHERE id = %s AND user_id = %s", (res_id, st.session_state["user"]["id"]))
            reservation = cursor.fetchone()

            if reservation:
                cursor.execute("UPDATE trains SET seats = seats + %s WHERE id = %s", (reservation["seats_booked"], reservation["train_id"]))
                cursor.execute("DELETE FROM reservations WHERE id = %s", (res_id,))
                conn.commit()

                st.rerun()
            else:
                st.error("Invalid Reservation ID.")

    conn.close()
