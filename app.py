from flask import Flask, render_template, request, redirect, session
from database import db, init_db, Admin

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

init_db(app)

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:
            session["admin"] = username
            return redirect("/home")
        else:
            return "Invalid credentials"

    return render_template("login.html")


# ---------------- HOME ----------------

@app.route("/home")
def home():
    if "admin" not in session:
        return redirect("/login")
    return render_template("home.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
