import os
from flask import Flask, render_template, request, redirect, url_for
from db_config import create_connection

# Explicitly setting static folder helps Render find your CSS
app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get inputs from HTML form
        p_name = request.form.get("name") 
        p_age = request.form.get("age")
        p_disease = request.form.get("disease")
        p_doctor = request.form.get("doctor")

        try:
            # Attempt database connection
            conn = create_connection()
            if conn:
                cursor = conn.cursor()
                sql = "INSERT INTO patients (name, age, disease, doctor) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (p_name, p_age, p_disease, p_doctor))
                conn.commit()
                cursor.close()
                conn.close()
                return render_template("success.html", patient_name=p_name)
            else:
                # This prevents the 'buffering' if the connection is null
                return "<h1>Connection Failed</h1><p>Check your Railway/Render Environment Variables.</p>"
        except Exception as e:
            # If there is a timeout or error, this displays it immediately
            return f"<h1>Database Error</h1><p>{str(e)}</p>"
            
    return render_template("register.html")

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
