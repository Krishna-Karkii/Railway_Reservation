import streamlit as st
import pandas as pd
from database import get_db_connection

def admin_dashboard():
    """Admin Panel for Train & Reservation Management"""
    if "user" not in st.session_state or st.session_state["user"]["role"] != "admin":
        st.warning("Unauthorized! Please log in as admin.")
        return

    st.sidebar.title("🛠 Admin Panel")
    action = st.sidebar.selectbox("Choose Action", ["Manage Trains", "Manage Reservations"])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if action == "Manage Trains":
        st.header("🚆 Train Management")

        trains = pd.read_sql("SELECT * FROM trains", conn)
        st.dataframe(trains)

        train_name = st.text_input("Train Name")
        source = st.text_input("Source")
        destination = st.text_input("Destination")
        seats = st.number_input("Seats Available", min_value=1)
        fare = st.number_input("Fare per Seat", min_value=1)

        if st.button("Add Train"):
            cursor.execute(
                "INSERT INTO trains (train_name, source, destination, seats, fare) VALUES (%s, %s, %s, %s, %s)",
                (train_name, source, destination, seats, fare)
            )
            conn.commit()
            st.success("Train added successfully!")

        train_id = st.number_input("Train ID to Update/Delete", min_value=1)
        update_field = st.selectbox("Field to Update", ["Train Name", "Source", "Destination", "Seats", "Fare"])
        update_value = st.text_input("New Value")

        if st.button("Update Train"):
            cursor.execute(f"UPDATE trains SET {update_field.lower().replace(' ', '_')} = %s WHERE id = %s", (update_value, train_id))
            conn.commit()
            st.success("Train updated successfully!")

        if st.button("Delete Train"):
            cursor.execute("DELETE FROM trains WHERE id = %s", (train_id,))
            conn.commit()
            st.warning("Train deleted!")

    elif action == "Manage Reservations":
        st.header("🎫 Reservation Management")

        reservations = pd.read_sql("""
            SELECT reservations.id, users.username, trains.train_name, reservations.seats_booked, reservations.total_fare 
            FROM reservations 
            JOIN users ON reservations.user_id = users.id 
            JOIN trains ON reservations.train_id = trains.id
        """, conn)
        st.dataframe(reservations)

        res_id = st.number_input("Enter Reservation ID to Delete", min_value=1)
        if st.button("Delete Reservation"):
            cursor.execute("DELETE FROM reservations WHERE id = %s", (res_id,))
            conn.commit()
            st.warning("Reservation deleted!")

    conn.close()
