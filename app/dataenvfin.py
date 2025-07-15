from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.auth import login_required,admin_required
from app.config import DB_PATH_FIN, CSV_PATH_FIN
from app.services.parameters import get_db_list_connection
import sqlite3


dataenvfin = Blueprint("dataenvfin", __name__)

@dataenvfin.route("/dataenvfin")
@login_required
@admin_required
def dataenvfin_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'type_doc'")
    list_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("dataenvfin.html",list_values=list_values)  # Render the data page

data="entriesfin"

# ------------------ ADD DATA TO FIN DATABASE------------------
@dataenvfin.route("/addfin", methods=["POST"])
@login_required
def add_entry_fin():
    nameAgent = request.form['nameAgent']
    typedoc = request.form['typedoc']
    de = request.form['de']
    au = request.form['au']
    boxNum = request.form['boxNum']
    manque = request.form['manque']
    rmq = request.form['rmq']

    conn = sqlite3.connect(DB_PATH_FIN)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entriesfin (nameAgent, typedoc, de, au, boxNum, manque, rmq) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (nameAgent,typedoc, de, au, boxNum, manque, rmq))
    conn.commit()
    conn.close()

    return redirect(url_for("indexfin.indexfin_view"))

# ------------------ SHOW CSV Inventaire FIN------------------

def get_data_from_table(limit=None):
    conn = sqlite3.connect(DB_PATH_FIN)
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
@dataenvfin.route("/get_data_dataFINTable")
@login_required
@admin_required
def get_data_fin():
    limit = request.args.get("limit", type=int)
    data = get_data_from_table(limit)
    return jsonify(data)

# ------------------ delete a ligne from db------------------
    
@dataenvfin.route('/delete_data_dataFINTable/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_data_fin(id):
     print(f"Received DELETE request for ID: {id}")
     try:
        conn = sqlite3.connect(DB_PATH_FIN)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entriesfin WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
     except Exception as e:
        print("Error deleting:", e)
        return jsonify({"success": False, "error": str(e)})

# ------------------number of FIN doc for dasboard cards ------------------

def get_db_fin():
    conn = sqlite3.connect(DB_PATH_FIN)
    conn.row_factory = sqlite3.Row  
    return conn



