from flask import Flask, render_template, request, redirect, session, url_for
from database import db, init_db, Admin, Patient

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# init database
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


# ---------------- DASHBOARD ---------------- #

@app.route("/home")
def home():
    if "admin" not in session:
        return redirect("/login")
    return render_template("home.html")


# ---------------- PATIENT ---------------- #

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        disease = request.form["disease"]

        patient = Patient(
            name=name,
            age=age,
            disease=disease
        )
        db.session.add(patient)
        db.session.commit()

        return redirect("/view_patients")

    return render_template("add_patient.html")


@app.route("/view_patients")
def view_patients():
    if "admin" not in session:
        return redirect("/login")

    patients = Patient.query.all()
    return render_template("view_patients.html", patients=patients)


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
