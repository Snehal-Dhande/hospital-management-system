from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    # SQLite database (works on Render)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "hospital.db")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        create_default_admin()


# ---------------- MODELS ----------------

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


def create_default_admin():
    # Create admin user if not exists
    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin", password="admin123")
        sneha = Admin(username="sneha", password="sneha@123")
        db.session.add(admin)
        db.session.add(sneha)
        db.session.commit()
