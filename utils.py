import hashlib
from database import get_db_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_hash, password):
    return stored_hash == hash_password(password)


def signup(username, password, role='user'):
    """Register a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hash_password(password), role))
        conn.commit()
        conn.close()
        return True
    except:
        return False