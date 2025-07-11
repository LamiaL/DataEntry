from flask import Blueprint, render_template
from app.auth import login_required
from app.services.parameters import get_db_list_connection

indexfin_bp = Blueprint("indexfin", __name__)

@indexfin_bp.route("/indexfin")
@login_required
def indexfin_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'type_doc'")
    list_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("indexfin.html",list_values=list_values)  # Render the data page