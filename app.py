import os
import sqlite3   # <-- SQLITE3 INCLUDED HERE
from flask import Flask, render_template, request
from db_config import create_connection

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ---------- CREATE DATABASE + TABLE ----------
def init_db():
    conn = create_connection()
    if conn is None:
        print("Failed to connect to SQLite")
        return

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            disease TEXT,
            doctor TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()
# --------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        p_name = request.form.get("name")
        p_age = request.form.get("age")
        p_disease = request.form.get("disease")
        p_doctor = request.form.get("doctor")

        try:
            conn = create_connection()
            if conn is None:
                return "<h1>Database Connection Failed</h1>"

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO patients (name, age, disease, doctor) VALUES (?, ?, ?, ?)",
                (p_name, p_age, p_disease, p_doctor)
            )
            conn.commit()
            conn.close()

            return render_template("success.html", patient_name=p_name)

        except Exception as e:
            return f"<h1>SQLite Error</h1><p>{str(e)}</p>"

    return render_template("register.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
