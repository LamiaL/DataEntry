from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.auth import login_required,admin_required
from app.config import DB_PATH, CSV_PATH
from app.services.parameters import get_db_list_connection
import sqlite3

dataenv = Blueprint("dataenv", __name__)

@dataenv.route("/dataenv")
@login_required
@admin_required
def dataenv_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'structures'")
    list_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("dataenv.html",list_values=list_values) 


# ------------------ ADD DATA TO INVENTORY ------------------

@dataenv.route("/add", methods=["POST"])
@login_required
def add_entry():
    nameAgent = request.form['nameAgent']
    boxNum = request.form['boxNum']
    strc = request.form['strc']
    exr = request.form['exr']
    intl = request.form['intl']
    addTopo = request.form['addTopo']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entries (nameAgent, boxNum, strc, exr, intl, addTopo) VALUES (?, ?, ?, ?, ?, ?)",
                   (nameAgent, boxNum, strc, exr, intl, addTopo))
    conn.commit()
    conn.close()

    return redirect(url_for("index.index_view"))

# ------------------ SHOW CSV Inventaire ------------------
data="entries"
def get_data_from_table(limit=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This lets us return dict-like rows
    cursor = conn.cursor()

    query = f"SELECT * FROM {data}"
    if limit and limit != -1:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

# API route to get data
@dataenv.route("/get_data_dataENVTable")
@login_required
@admin_required
def get_data_env():
    limit = request.args.get("limit", type=int)
    data = get_data_from_table(limit)
    return jsonify(data)

@dataenv.route("/delete_data_dataENVTable/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def delete_data_env(id):
    print(f"Received DELETE request for ID: {id}")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entries WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        print("Error deleting:", e)
        return jsonify({"success": False, "error": str(e)})

# ------------------number of inventory doc for dasboard cards ------------------

def get_db_inv():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn