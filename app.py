from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from database import get_connection


app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# MODELS
# ==========================

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    disease = db.Column(db.String(100))
    contact = db.Column(db.String(20))


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    contact = db.Column(db.String(20))


class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    room_no = db.Column(db.String(20))
    doctor = db.Column(db.String(100))
    admit_date = db.Column(db.String(20))
    discharge_date = db.Column(db.String(20), nullable=True)


# ==========================
# LOGIN
# ==========================

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["user"] = "admin"
            return redirect("/home")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ==========================
# HOME
# ==========================

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html")


# ==========================
# PATIENT
# ==========================

@app.route("/add_patient", methods=["GET", "POST"])
def add_patient():
    if request.method == "POST":
        p = Patient(
            name=request.form["name"],
            age=request.form["age"],
            gender=request.form["gender"],
            disease=request.form["disease"],
            contact=request.form["contact"]
        )
        db.session.add(p)
        db.session.commit()
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
        name = request.form["name"]
        patient = Patient.query.filter_by(name=name).first()

    return render_template("search_patient.html", patient=patient)


# ==========================
# STAFF
# ==========================

@app.route("/add_staff", methods=["GET", "POST"])
def add_staff():
    if request.method == "POST":
        s = Staff(
            name=request.form["name"],
            role=request.form["role"],
            contact=request.form["contact"]
        )
        db.session.add(s)
        db.session.commit()
        return redirect("/view_staff")

    return render_template("add_staff.html")


@app.route("/view_staff")
def view_staff():
    staff_list = Staff.query.all()
    return render_template("view_staff.html", staff_list=staff_list)



# ==========================
# ADMISSION
# ==========================

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if 'user' not in session:
        return redirect('/login')

    db = get_connection()
    cur = db.cursor()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        admit_date = request.form['admit_date']
        discharge_date = request.form['discharge_date']

        cur.execute(
            "INSERT INTO admission (patient_id, admit_date, discharge_date) VALUES (%s,%s,%s)",
            (patient_id, admit_date, discharge_date)
        )
        db.commit()
        db.close()
        return redirect('/view_admission')

    # GET request → fetch patients
    cur.execute("SELECT patient_id, name FROM patients")
    patients = cur.fetchall()
    db.close()

    return render_template('admission.html', patients=patients)










@app.route('/view_admission')
def view_admission():
    if 'user' not in session:
        return redirect('/login')

    db = get_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT a.admit_id, p.name, a.admit_date, a.discharge_date
        FROM admission a
        JOIN patients p ON a.patient_id = p.patient_id
    """)
    admissions = cur.fetchall()
    db.close()

    return render_template('view_admission.html', admissions=admissions)


# ==========================
# DISCHARGE
# ==========================

@app.route("/update_discharge", methods=["GET", "POST"])
def update_discharge():
    message = ""
    if request.method == "POST":
        pid = request.form["patient_id"]
        admission = Admission.query.filter_by(patient_id=pid, discharge_date=None).first()

        if admission:
            admission.discharge_date = str(date.today())
            db.session.commit()
            message = "Discharge updated successfully"
        else:
            message = "Admission not found"

    return render_template("update_discharge.html", message=message)


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
