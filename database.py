from flask_sqlalchemy import SQLAlchemy
import os

# Initialize SQLAlchemy (do NOT pass app here)
db = SQLAlchemy()


def init_db(app):
    """
    Initialize database with Flask app
    Works for both local & Render deployment
    """

    # Create instance folder if not exists (important for Render)
    instance_path = os.path.join(app.root_path, "instance")
    os.makedirs(instance_path, exist_ok=True)

    # SQLite database path
    db_path = os.path.join(instance_path, "hospital.db")

    # Flask config
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB with app
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()


# ===========================
# MODELS
# ===========================

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10))
    contact = db.Column(db.String(20))
    address = db.Column(db.String(200))


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))
    contact = db.Column(db.String(20))


class Admission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    ward = db.Column(db.String(50))
    admit_date = db.Column(db.String(20))
    discharge_date = db.Column(db.String(20))
