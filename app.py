from flask import Flask, render_template, request, redirect, session, url_for
from database import db, init_db, Admin, Patient, Staff, Admission

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

init_db(app)


# ---------------- LOGIN ---------------- #

@app.route("/", methods=["GET"])
def index():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # ✅ hardcoded credentials
        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect("/home")
        else:
            return "Invalid credentials"

    return render_template("login.html")




@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


# ---------------- HOME ---------------- #

@app.route("/home")
def home():
    if "admin" not in session:
        return redirect("/login")
    return render_template("home.html")


# ---------------- PATIENT ---------------- #

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        disease = request.form.get("disease")
        contact = request.form.get("contact")

        if not all([name, age, gender, disease, contact]):
            return "All fields are required"

        patient = Patient(
            name=name,
            age=int(age),
            gender=gender,
            disease=disease,
            contact=contact
        )

        db.session.add(patient)
        db.session.commit()

        print("Patient added:", name)  # for Render logs

        return redirect("/view_patients")

    return render_template("add_patient.html")


@app.route("/view_patients")
def view_patients():
    patients = Patient.query.all()
    return render_template("view_patients.html", patients=patients)


@app.route("/search_patient", methods=["GET", "POST"])
def search_patient():
    patient = None

    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        patient = Patient.query.get(patient_id)

    return render_template("search_patient.html", patient=patient)




# ---------------- STAFF ---------------- #

@app.route("/add_staff", methods=["GET", "POST"])
def add_staff():
    if request.method == "POST":
        name = request.form.get("name")
        role = request.form.get("role")
        contact = request.form.get("contact")

        if not name or not role or not contact:
            return "All fields required"

        staff = Staff(
            name=name,
            role=role,
            contact=contact
        )

        db.session.add(staff)
        db.session.commit()

        return redirect("/view_staff")

    return render_template("add_staff.html")


@app.route("/view_staff")
def view_staff():
    staff_list = Staff.query.all()
    return render_template("view_staff.html", staff_list=staff_list)


# ---------------- ADMISSION ---------------- #

@app.route("/admission", methods=["GET", "POST"])
def admission():
    if request.method == "POST":
        try:
            patient_id = request.form.get("patient_id")
            room_no = request.form.get("room_no")
            admit_date = request.form.get("admit_date")

            admission = Admission(
                patient_id=patient_id,
                room_no=room_no,
                admit_date=admit_date
            )

            db.session.add(admission)
            db.session.commit()

            return redirect("/admissions")

        except Exception as e:
            return f"Error occurred: {e}"

    return render_template("admission.html")



@app.route("/view_admission")
def view_admission():
    admissions = Admission.query.all()
    return render_template("view_admission.html", admissions=admissions)


@app.route("/update_discharge", methods=["GET", "POST"])
def update_discharge():
    message = ""

    if request.method == "POST":
        patient_id = request.form.get("patient_id")

        patient = Patient.query.get(patient_id)

        if patient:
            patient.discharged = True
            db.session.commit()
            message = "Patient discharged successfully"
        else:
            message = "Patient not found"

    return render_template("update_discharge.html", message=message)


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

