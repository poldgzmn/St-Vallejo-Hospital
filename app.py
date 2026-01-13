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
        # Kinukuha ang inputs mula sa HTML
        p_name = request.form.get("name") 
        p_age = request.form.get("age")
        p_disease = request.form.get("disease")
        p_doctor = request.form.get("doctor")

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                
                sql = "INSERT INTO patients (name, age, disease, doctor) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (p_name, p_age, p_disease, p_doctor))
                conn.commit()
                return render_template("success.html", patient_name=p_name)
            except Exception as e:
                return f"Database Error: {e}"
            finally:
                cursor.close()
                conn.close()
        return "Database connection failed."
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
