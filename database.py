from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# ---------------------------
# Initialize Database
# ---------------------------
def init_db(app):
    # Ensure instance folder exists (important on Render)
    instance_path = os.path.join(os.getcwd(), "instance")
    os.makedirs(instance_path, exist_ok=True)

    # SQLite database path
    db_path = os.path.join(instance_path, "hospital.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()


# ---------------------------
# Database Models
# ---------------------------

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    contact = db.Column(db.String(20))


class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    ward = db.Column(db.String(50))
    admit_date = db.Column(db.String(20))
    discharge_date = db.Column(db.String(20))
