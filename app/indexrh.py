from flask import Blueprint, render_template
from app.auth import login_required
from app.services.parameters import get_db_list_connection

indexrh_bp = Blueprint("indexrh", __name__)

@indexrh_bp.route("/indexrh")
@login_required
def indexrh_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'motif_depart'")
    list_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("indexrh.html",list_values=list_values )  # Render the data page