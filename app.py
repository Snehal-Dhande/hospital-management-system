import webbrowser

from flask import Flask, render_template, request, redirect, session
from database import get_connection

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_connection()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        db.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ================= HOME =================
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template('home.html')


# ================= PATIENT =================
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        db = get_connection()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO patients (name, age, gender, disease) VALUES (%s,%s,%s,%s)",
            (name, age, gender, disease)
        )
        db.commit()
        db.close()

        return redirect('/view_patients')

    return render_template('add_patient.html')


@app.route('/view_patients')
def view_patients():
    if 'user' not in session:
        return redirect('/login')

    db = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    db.close()

    return render_template('view_patients.html', patients=patients)


@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if 'user' not in session:
        return redirect('/login')

    patient = None
    if request.method == 'POST':
        pid = request.form['patient_id']
        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM patients WHERE patient_id=%s", (pid,))
        patient = cur.fetchone()
        db.close()

    return render_template('search_patient.html', patient=patient)


# ================= STAFF =================
@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        contact = request.form['contact']

        db = get_connection()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO staff (name, role, contact) VALUES (%s,%s,%s)",
            (name, role, contact)
        )
        db.commit()
        db.close()

        return redirect('/view_staff')

    return render_template('add_staff.html')


@app.route('/view_staff')
def view_staff():
    if 'user' not in session:
        return redirect('/login')

    db = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM staff")
    staff = cur.fetchall()
    db.close()

    return render_template('view_staff.html', staff=staff)


# ================= ADMISSION =================
@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        admit_date = request.form['admit_date']
        discharge_date = request.form['discharge_date']

        db = get_connection()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO admission (patient_id, admit_date, discharge_date) VALUES (%s,%s,%s)",
            (patient_id, admit_date, discharge_date)
        )
        db.commit()
        db.close()

        return redirect('/view_admission')

    return render_template('admission.html')


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

    return render_template('view_admission.html', admission=admissions)


@app.route('/update_discharge', methods=['GET', 'POST'])
def update_discharge():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        admit_id = request.form['admit_id']
        discharge_date = request.form['discharge_date']

        db = get_connection()
        cur = db.cursor()
        cur.execute(
            "UPDATE admission SET discharge_date=%s WHERE admit_id=%s",
            (discharge_date, admit_id)
        )
        db.commit()
        db.close()

        return redirect('/view_admission')

    return render_template('update_discharge.html')


# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

    
   

