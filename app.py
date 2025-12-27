from flask import Flask, render_template, request, redirect, session, url_for
from database import db, init_db, Admin

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Initialize database
init_db(app)

# ---------------- AUTH ---------------- #

@app.route("/")
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:
            session["admin"] = admin.username
            return redirect("/home")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


# ---------------- PAGES ---------------- #

@app.route("/home")
def home():
    if "admin" not in session:
        return redirect("/login")
    return render_template("home.html")


@app.route("/add_patient")
def add_patient():
    if "admin" not in session:
        return redirect("/login")
    return render_template("add_patient.html")


@app.route("/add_staff")
def add_staff():
    if "admin" not in session:
        return redirect("/login")
    return render_template("add_staff.html")


@app.route("/admission")
def admission():
    if "admin" not in session:
        return redirect("/login")
    return render_template("admission.html")


@app.route("/view_patients")
def view_patients():
    if "admin" not in session:
        return redirect("/login")
    return render_template("view_patients.html")


@app.route("/view_staff")
def view_staff():
    if "admin" not in session:
        return redirect("/login")
    return render_template("view_staff.html")


@app.route("/search_patient")
def search_patient():
    if "admin" not in session:
        return redirect("/login")
    return render_template("search_patient.html")


@app.route("/update_discharge")
def update_discharge():
    if "admin" not in session:
        return redirect("/login")
    return render_template("update_discharge.html")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
