import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ---- SQLITE CONNECTION ----
def create_connection():
    return sqlite3.connect("patients.db", check_same_thread=False)

# ---- CREATE DB + TABLE ----
def init_db():
    conn = create_connection()
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (name, age, disease, doctor) VALUES (?, ?, ?, ?)",
            (
                request.form.get("name"),
                request.form.get("age"),
                request.form.get("disease"),
                request.form.get("doctor"),
            )
        )
        conn.commit()
        conn.close()
        return "Saved to SQLite ✅"

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
