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
        # Kinukuha ang 'name' mula sa HTML input
        patient_name = request.form.get("name") 
        age = request.form.get("age")
        disease = request.form.get("disease")
        doctor = request.form.get("doctor")

        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Dapat tugma ang columns sa SQL table mo
                sql = "INSERT INTO patients (name, age, disease, doctor) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (patient_name, age, disease, doctor))
                conn.commit()
                # Ipapasa ang patient_name sa success page
                return render_template("success.html", patient_name=patient_name)
            except Exception as e:
                return f"Error: {e}"
            finally:
                cursor.close()
                conn.close()
    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
