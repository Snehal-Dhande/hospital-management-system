from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

# =========================
# Initialize Database
# =========================
def init_db(app):
    # Ensure instance folder exists (important for Render)
    instance_path = os.path.join(app.root_path, "instance")
    os.makedirs(instance_path, exist_ok=True)

    # SQLite database path
    db_path = os.path.join(instance_path, "hospital.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()


# =========================
# Models
# =========================
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))
    phone = db.Column(db.String(15))


class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    ward = db.Column(db.String(50))
    admit_date = db.Column(db.String(20))
    discharge_date = db.Column(db.String(20))
