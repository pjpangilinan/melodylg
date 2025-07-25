import sqlite3
import hashlib
import re

DB_NAME = "users.db"

def is_strong_password(password):
    """Check if password meets strength requirements."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[\W_]", password): 
        return False
    return True

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def user_exists(username):
    """Check if a username already exists in the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def is_correct_password(username, password):
    """Validate if password is correct for the given username."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    return row and verify_password(password, row[0])

def register_user(username, password):
    if user_exists(username):
        return False 
    if not is_strong_password(password):
        return False 
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    """Returns True if login successful, else False."""
    return is_correct_password(username, password)

def reset_password(username, new_password):
    if not user_exists(username):
        return False
    if not is_strong_password(new_password):
        return False
    hashed = hash_password(new_password)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET password=? WHERE username=?", (hashed, username))
    conn.commit()
    conn.close()
    return True
