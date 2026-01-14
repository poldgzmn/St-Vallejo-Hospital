import sqlite3

def create_connection():
    try:
        return sqlite3.connect("patients.db", check_same_thread=False)
    except Exception as e:
        print("SQLite error:", e)
        return None
