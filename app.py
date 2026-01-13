import os
from flask import Flask, render_template, request, redirect, url_for
from db_config import create_connection

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        patient_name = request.form.get("patient_name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        blood_type = request.form.get("blood_type")
        contact = request.form.get("contact")

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = """INSERT INTO patients (patient_name, age, gender, blood_type, contact) 
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (patient_name, age, gender, blood_type, contact))
                conn.commit()
                return render_template("success.html", name=patient_name)
            except Exception as e:
                return f"Error: {e}"
            finally:
                cursor.close()
                conn.close()
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))