from flask import Blueprint, render_template, jsonify
from app.auth import login_required,admin_required
from app.config import DB_PATH_USERS
import sqlite3

users = Blueprint("users", __name__)

@users.route("/add_user")
@login_required
@admin_required
def add_user_view():
    return render_template("add_user.html")  # Render the dashboard page

# ------------------ SHOW users------------------
# Function to fetch all users
@users.route("/get_users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")  # Fetch without passwords
    users = cursor.fetchall()
    conn.close()
    
    # Convert list of tuples into a list of dictionaries
    users_list = [{"id": user[0], "username": user[1], "role": user[2]} for user in users]
    
    return jsonify(users_list)

# ------------------ users number for dasboard cards ------------------
def get_db():
    conn = sqlite3.connect(DB_PATH_USERS)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn