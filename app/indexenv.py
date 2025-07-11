from flask import Blueprint, render_template
from app.auth import login_required
from app.services.parameters import get_db_list_connection

indexenv_bp = Blueprint("indexenv", __name__)

@indexenv_bp.route("/indexenv")
@login_required
def indexenv_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'structures2'")
    list_values = [row['value'] for row in cursor.fetchall()]
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'conditionnement'")
    list2_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("indexenv.html",list_values=list_values,list2_values=list2_values)  # Render the data page