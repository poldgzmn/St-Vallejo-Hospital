import os
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            port=int(os.environ.get("DB_PORT", 3306)),
            connection_timeout=10  # This prevents the infinite buffering
        )
        if connection.is_connected():
            return connection
    except Error as e:
        # This will now print to your Render logs instead of hanging
        print(f"❌ Database Error: {e}")
        return None
    return None
