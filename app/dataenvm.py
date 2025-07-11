from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.data_function import download_csv
from app.auth import login_required,admin_required
from app.config import DB_PATH_M,CSV_PATH_M
from app.services.parameters import get_db_list_connection
import sqlite3

dataenvm = Blueprint("dataenvm", __name__)

@dataenvm.route("/dataenvm")
@login_required
@admin_required
def dataenvm_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'structures2'")
    list_values = [row['value'] for row in cursor.fetchall()]
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'conditionnement'")
    list2_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("dataenvm.html",list_values=list_values,list2_values=list2_values)

# ------------------ ADD DATA TO INVENTAIRE MADJID DATABASE------------------

@dataenvm.route("/addenvm", methods=["POST"])
@login_required
def add_entry_envm():
    nameAgent = request.form['nameAgent']
    boxCote = request.form['boxCote']
    boxNum = request.form['boxNum']
    strc = request.form['strc']
    intl = request.form['intl']
    mois = request.form.get('mois', '') 
    anne = request.form['anne']
    typeDoc = request.form['typeDoc']
    cond = request.form['cond']
    comtr = request.form['comtr']

    conn = sqlite3.connect(DB_PATH_M)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entriesenvm (nameAgent, boxCote, boxNum, strc, intl, mois, anne, typeDoc, cond, comtr) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,? )",
                   (nameAgent, boxCote, boxNum, strc, intl, mois, anne,typeDoc, cond, comtr))
    conn.commit()
    conn.close()

    return redirect(url_for("indexenv.indexenv_view"))
# ------------------ DOWNLOAD CSV inventaire------------------

@dataenvm.route("/downloadenvm")
@login_required
@admin_required
def download_entries():
    return download_csv(
        db_path=DB_PATH_M,
        table_name="entriesenvm",
        csv_path= CSV_PATH_M
    )

# ------------------ SHOW CSV Inventaire RH-----------------
data="entriesenvm"
def get_data_from_table(limit=None):
    conn = sqlite3.connect(DB_PATH_M)
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
@dataenvm.route("/get_data_dataENVMTable")
@login_required
@admin_required
def get_data_envm():
    limit = request.args.get("limit", type=int)
    data = get_data_from_table(limit)
    return jsonify(data)

@dataenvm.route("/delete_data_dataENVMTable/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def delete_data_envm(id):
    print(f"Received DELETE request for ID: {id}")
    try:
        conn = sqlite3.connect(DB_PATH_M)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entriesenvm WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        print("Error deleting:", e)
        return jsonify({"success": False, "error": str(e)})
    
# ------------------number of RH doc for dasboard cards ------------------

def get_db_envm():
    conn = sqlite3.connect(DB_PATH_M)
    conn.row_factory = sqlite3.Row  
    return conn