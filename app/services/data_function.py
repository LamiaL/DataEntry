from flask import Blueprint, session, request, redirect, url_for, flash, send_file, render_template,jsonify
from app.auth import login_required,admin_required
from app.config import DB_PATH_USERS
import pandas as pd
import sqlite3
import csv
from app.services.parameters import get_db_list_connection

app_bp = Blueprint("app", __name__)

# download CSV function
def download_csv(db_path, table_name, csv_path):
    # Fetch data from the specified table
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()

    # Check if there's data
    if df.empty:
        return "Aucune donnée disponible"
    
     # Sanitize line breaks in all string columns
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.replace('\r', ' ', regex=False).str.replace('\n', ' ', regex=False)

    # Export to CSV
    df.to_csv(csv_path, index=False, quoting=csv.QUOTE_ALL)
    return send_file(csv_path, as_attachment=True)

# Edit fuction
def edit_data_generic(id, bd_path, table_name, template_name, redirect_endpoint, lists_config=None):
    conn = sqlite3.connect(bd_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (id,))
    row = cursor.fetchone()

    context = {"row": row}

    # Dynamically fetch dropdown lists
    if lists_config:
        list_conn = get_db_list_connection()
        list_cursor = list_conn.cursor()
        for lst in lists_config:
            list_cursor.execute("SELECT value FROM parameters WHERE list_name = ?", (lst["list_name"],))
            context[lst["key"]] = [r["value"] for r in list_cursor.fetchall()]
        list_conn.close()

    conn.close()

    if row:
        return render_template(template_name, **context)
    else:
        flash("Data not found", "danger")
        return redirect(url_for(redirect_endpoint))


# update fuction   
def update_data_generic(id, bd_path, table_name, fields, redirect_endpoint):
    if "username" not in session:
        return redirect(url_for("auth_login_bp.login"))
    if session.get("role") != "admin":
        flash("Accès refusé. Seuls les admins peuvent accéder à cette page.", "danger")
        return redirect(url_for("dashboard.dashboard_view"))

    # Dynamically get values from form
    values = [request.form[field] for field in fields]

    # Build SET clause dynamically
    set_clause = ", ".join(f"{field} = ?" for field in fields)

    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {table_name} SET 
            {set_clause}
        WHERE id = ?
    """, (*values, id))
    conn.commit()
    conn.close()

    flash("Data updated successfully!", "success")
    return redirect(url_for(redirect_endpoint))

# get a liste with all users 
@app_bp.route('/get_usernames')
@login_required
@admin_required
def get_usernames():
    import sqlite3
    conn = sqlite3.connect(DB_PATH_USERS)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY username ASC")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)