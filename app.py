from flask import Flask, render_template, request, redirect, url_for, session
from database import db, init_db, Patient, Staff, Admission

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Initialize database
init_db(app)

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("dashboard"))

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")


# ---------------------------
# Patient
# ---------------------------

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        patient = Patient(
            name=request.form["name"],
            age=request.form["age"],
            gender=request.form["gender"],
            contact=request.form["contact"]
        )
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for("view_patients"))

    return render_template("add_patient.html")


@app.route("/view_patients")
def view_patients():
    patients = Patient.query.all()
    return render_template("view_patients.html", patients=patients)


# ---------------------------
# Staff
# ---------------------------

@app.route("/add_staff", methods=["GET", "POST"])
def add_staff():
    if request.method == "POST":
        staff = Staff(
            name=request.form["name"],
            role=request.form["role"],
            contact=request.form["contact"]
        )
        db.session.add(staff)
        db.session.commit()
        return redirect(url_for("view_staff"))

    return render_template("add_staff.html")


@app.route("/view_staff")
def view_staff():
    staff = Staff.query.all()
    return render_template("view_staff.html", staff=staff)


# ---------------------------
# Admission
# ---------------------------

@app.route("/admission", methods=["GET", "POST"])
def admission():
    if request.method == "POST":
        admission = Admission(
            patient_id=request.form["patient_id"],
            ward=request.form["ward"],
            admit_date=request.form["admit_date"],
            discharge_date=""
        )
        db.session.add(admission)
        db.session.commit()
        return redirect(url_for("view_admission"))

    return render_template("admission.html")


@app.route("/view_admission")
def view_admission():
    admissions = Admission.query.all()
    return render_template("view_admission.html", admissions=admissions)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
