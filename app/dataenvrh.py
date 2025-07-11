from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.services.data_function import download_csv
from app.auth import login_required,admin_required
from app.config import DB_PATH_RH, CSV_PATH_RH
from app.services.parameters import get_db_list_connection
import sqlite3

dataenvrh = Blueprint("dataenvrh", __name__)

@dataenvrh.route("/dataenvrh")
@login_required
@admin_required
def dataenvrh_view(): 
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'motif_depart'")
    list_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("dataenvrh.html",list_values=list_values)  # Render the data page

# ------------------ ADD DATA TO RH DATABASE------------------
@dataenvrh.route("/addrh", methods=["POST"])
@login_required
def add_entry_rh():
    nameAgent = request.form['nameAgent']
    mtl = request.form['mtl']
    name = request.form['name']
    fname = request.form['fname']
    bday = request.form['bday']
    fonction = request.form['fonction']
    dent = request.form['dent']
    dsor = request.form['dsor']
    motifdepart = request.form['motifdepart']
    boxNum = request.form['boxNum']
    addTopo = request.form['addTopo']
    rmq = request.form['rmq']

    conn = sqlite3.connect(DB_PATH_RH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entriesrh (nameAgent, mtl, name, fname, bday, fonction, dent, dsor, motifdepart, boxNum, addTopo, rmq) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (nameAgent, mtl, name, fname, bday, fonction, dent, dsor, motifdepart, boxNum, addTopo, rmq))
    conn.commit()
    conn.close()

    return redirect(url_for("indexrh.indexrh_view"))

# ------------------ DOWNLOAD CSV inventaire RH------------------
@dataenvrh.route("/downloadenvrh")
@login_required
@admin_required
def download_entries():
    return download_csv(
        db_path=DB_PATH_RH,
        table_name="entrieserh",
        csv_path= CSV_PATH_RH
    )

# ------------------ SHOW CSV Inventaire RH------------------
data="entriesrh"
def get_data_from_table(limit=None):
    conn = sqlite3.connect(DB_PATH_RH)
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
@dataenvrh.route("/get_data_dataRHTable")
@login_required
@admin_required
def get_data_rh():
    limit = request.args.get("limit", type=int)
    data = get_data_from_table(limit)
    return jsonify(data)

@dataenvrh.route("/delete_data_dataRHTable/<int:id>", methods=["DELETE"])
@login_required
@admin_required
def delete_data_rh(id):
    print(f"Received DELETE request for ID: {id}")
    try:
        conn = sqlite3.connect(DB_PATH_RH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entriesrh WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        print("Error deleting:", e)
        return jsonify({"success": False, "error": str(e)})

# ------------------number of RH doc for dasboard cards ------------------

def get_db_rh():
    conn = sqlite3.connect(DB_PATH_RH)
    conn.row_factory = sqlite3.Row  
    return conn