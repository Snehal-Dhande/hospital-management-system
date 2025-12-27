from flask import Flask, render_template, request, redirect, session, url_for
from database import db, init_db, Admin

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Initialize database
init_db(app)


# ---------------- ROUTES ---------------- #

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


@app.route("/home")
def home():
    if "admin" not in session:
        return redirect("/login")
    return render_template("home.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
