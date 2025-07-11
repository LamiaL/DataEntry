from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.auth import login_required,admin_required
from app.config import DB_PATH_USERS
import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

# Create a bp for login
auth_login_bp = Blueprint("auth_login_bp", __name__)
# ------------------ LOGIN ROUTE ------------------
@auth_login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH_USERS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):  # Assuming password is in column 3
            session["logged_in"] = True 
            session["user_id"] = user[0]
            session["username"] = user[1]  # Store username in session
            session["role"] = user[3]  # Store role in session
            return redirect(url_for("dashboard.dashboard_view"))

        flash("Invalid username or password", "error")
    return render_template("login.html")

# ------------------ LOGOUT ROUTE ------------------
@auth_login_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)  # Remove only the username from session
    session.clear()  # Clear session data
    return redirect(url_for("auth_login_bp.login"))

# ------------------ ADD USER------------------
@auth_login_bp.route("/users")
@login_required
@admin_required
def users():
    conn = sqlite3.connect(DB_PATH_USERS, timeout=10)  # Increase timeout to 10 seconds
    #conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users)

@auth_login_bp.route("/add_user", methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(DB_PATH_USERS)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
        conn.commit()
        conn.close()

        return redirect(url_for("auth_login_bp.users"))

    return render_template("add_user.html")

# ------------------ DELETE USER------------------
@auth_login_bp.route("/delete_user/<int:user_id>")
@login_required
@admin_required
def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("auth_login_bp.users"))

# ------------------ CHANGE USER PASSSWORD------------------
@auth_login_bp.route("/change_password/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def change_password(user_id):
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = generate_password_hash(new_password)

        conn = sqlite3.connect(DB_PATH_USERS)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
        conn.commit()
        conn.close()
        flash("Password updated successfully!", "success")
        return redirect(url_for("auth_login_bp.users"))

    # Get user details (username + role)
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template("changepw.html", user=user)

# ------------------ user own profile------------------
@auth_login_bp.route("/profileuser", methods=["GET", "POST"])
@login_required
def profileuser():
    user_id = session["user_id"]

    # Fetch user details from DB
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("auth_login_bp.login"))

    return render_template("profileuser.html", user=user)

@auth_login_bp.route("/change_own_password", methods=["POST"])
def change_own_password():
    if "username" not in session:
        print("Redirecting: Not logged in")
        return redirect(url_for("auth_login_bp.login"))  # Redirect to login if not logged in

    user_id = session["user_id"]
    new_password = request.form["new_password"]
    hashed_password = generate_password_hash(new_password)

    # Update password in the DB
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
    conn.commit()
    conn.close()

    flash("Password updated successfully!", "success")
    return redirect(url_for("auth_login_bp.profileuser"))