import mysql.connector

def get_db_connection():
    """Connects to MySQL Database"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="krishna10",
        database="railway_reservation"
    )

def initialize_database():
    """Creates tables if they don’t exist"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('user', 'admin') NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trains (
            id INT AUTO_INCREMENT PRIMARY KEY,
            train_name VARCHAR(100) NOT NULL,
            source VARCHAR(50) NOT NULL,
            destination VARCHAR(50) NOT NULL,
            seats INT NOT NULL,
            fare INT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            train_id INT NOT NULL,
            seats_booked INT NOT NULL,
            total_fare INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (train_id) REFERENCES trains(id)
        )
    """)

    # Add default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
            ('admin', 'hashed_admin_password_here', 'admin')
        )
        conn.commit()

    conn.close()
