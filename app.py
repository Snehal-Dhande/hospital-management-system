from flask import Flask, render_template, request, redirect, session, url_for
from database import db, init_db, Admin, Patient, Staff, Admission

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Initialize DB
init_db(app)

# ---------------- HOME & AUTH ---------------- #

@app.route("/")
def index():
    return redirect(url_for("login"))

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
            return redirect(url_for("home"))
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/home")
def home():
    if "admin" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

# ---------------- PATIENT ---------------- #

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        patient = Patient(
            name=request.form["name"],
            age=request.form["age"],
            gender=request.form["gender"],
            disease=request.form["disease"]
        )
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for("view_patients"))

    return render_template("add_patient.html")

@app.route("/view_patients")
def view_patients():
    if "admin" not in session:
        return redirect(url_for("login"))

    patients = Patient.query.all()
    return render_template("view_patients.html", patients=patients)

# ---------------- STAFF ---------------- #

@app.route("/add_staff", methods=["GET", "POST"])
def add_staff():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        staff = Staff(
            name=request.form["name"],
            role=request.form["role"]
        )
        db.session.add(staff)
        db.session.commit()
        return redirect(url_for("view_staff"))

    return render_template("add_staff.html")

@app.route("/view_staff")
def view_staff():
    if "admin" not in session:
        return redirect(url_for("login"))

    staff = Staff.query.all()
    return render_template("view_staff.html", staff=staff)

# ---------------- ADMISSION ---------------- #

@app.route("/admission", methods=["GET", "POST"])
def admission():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        admission = Admission(
            patient_id=request.form["patient_id"],
            room=request.form["room"]
        )
        db.session.add(admission)
        db.session.commit()
        return redirect(url_for("view_admission"))

    return render_template("admission.html")

@app.route("/view_admission")
def view_admission():
    if "admin" not in session:
        return redirect(url_for("login"))

    admissions = Admission.query.all()
    return render_template("view_admission.html", admissions=admissions)

# ---------------- SEARCH ---------------- #

@app.route("/search_patient", methods=["GET", "POST"])
def search_patient():
    if "admin" not in session:
        return redirect(url_for("login"))

    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        results = Patient.query.filter(
            Patient.name.like(f"%{keyword}%")
        ).all()

    return render_template("search_patient.html", results=results)

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
