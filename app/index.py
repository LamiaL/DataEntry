from flask import Blueprint, render_template
from app.auth import login_required
from app.services.parameters import get_db_list_connection


index_bp = Blueprint("index", __name__) 

@index_bp.route("/inventaire")
@login_required
def index_view():
    conn = get_db_list_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM parameters WHERE list_name = 'structures'")
    list_values = [row['value'] for row in cursor.fetchall()]
    conn.close()
    return render_template("index.html",list_values=list_values)

