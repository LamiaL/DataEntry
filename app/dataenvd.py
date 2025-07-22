from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.auth import login_required,admin_required
from app.config import DB_PATH_D
from app.services.parameters import get_db_list_connection
import sqlite3

dataenvd = Blueprint("dataenvd", __name__)

@dataenvd.route("/dataenvd")
@login_required
@admin_required
def dataenvd_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'structures2'")
    list_values = [row['value'] for row in cursor.fetchall()]
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'conditionnement'")
    list2_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("dataenvd.html",list_values=list_values,list2_values=list2_values)

# ------------------ ADD DATA TO INVENTAIRE MADJID DATABASE------------------

@dataenvd.route("/addenvd", methods=["POST"])
@login_required
def add_entry_envd():
    nameAgent = request.form['nameAgent']
    boxCote = request.form['boxCote']
    boxNum = request.form['boxNum']
    strc = request.form['strc']
    intl = request.form['intl']
    typeDoc = request.form.get('typeDoc','')
    Ref = request.form.get('Ref', '') 
    catg = request.form.get('catg','')
    anne = request.form['anne']
    format = request.form.get('format', '') 
    cond = request.form['cond']
    comtr = request.form['comtr']

    conn = sqlite3.connect(DB_PATH_D)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entriesenvd (nameAgent, boxCote, boxNum, strc, intl, typeDoc, Ref, catg, anne, format, cond, comtr) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
                   (nameAgent, boxCote, boxNum, strc, intl, typeDoc, Ref, catg, anne, format, cond, comtr))
    conn.commit()
    conn.close()

    return redirect(url_for("indexenvd.indexenvd_view"))


# ------------------ SHOW CSV Inventaire -----------------
data="entriesenvd"
def get_data_from_table(limit=None):
    conn = sqlite3.connect(DB_PATH_D)
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
@dataenvd.route("/get_data_dataENVDTable")
@login_required
@admin_required
def get_data_envd():
    limit = request.args.get("limit", type=int)
    data = get_data_from_table(limit)
    return jsonify(data)

@dataenvd.route("/delete_data_dataENVDTable/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def delete_data_envd(id):
    print(f"Received DELETE request for ID: {id}")
    try:
        conn = sqlite3.connect(DB_PATH_D)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entriesenvd WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        print("Error deleting:", e)
        return jsonify({"success": False, "error": str(e)})
    
# ------------------number of RH doc for dasboard cards ------------------

def get_db_envd():
    conn = sqlite3.connect(DB_PATH_D)
    conn.row_factory = sqlite3.Row  
    return conn