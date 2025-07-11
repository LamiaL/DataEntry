from flask import Blueprint, request,render_template,session,flash
from app.auth import login_required, admin_required
from app.config import DB_PATH_LISTES
import sqlite3

parameters_bp = Blueprint('parameters', __name__)

@parameters_bp.route("/parameters")
@login_required
@admin_required
def parameters_view():
    user_role = session.get('role')
    return render_template("parameters.html", role=user_role)

def get_db_list_connection():
    conn = sqlite3.connect(DB_PATH_LISTES)
    conn.row_factory = sqlite3.Row
    return conn


@parameters_bp.route('/parameters/liste/<list_name>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_list(list_name):
    conn = get_db_list_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
       # get new list values
        new_values = request.form.getlist('values')

        # delete the old list
        cursor.execute("DELETE FROM parameters WHERE list_name = ?", (list_name,))

        # add new values
        for val in new_values:
            if val.strip():  # no nulls values
                cursor.execute(
                    "INSERT INTO parameters (list_name, value) VALUES (?, ?)",
                    (list_name, val.strip())
                )

        conn.commit()
        flash("Liste mise à jour avec succès", "success")

        # Relaod the new list
        cursor.execute("SELECT value FROM parameters WHERE list_name = ?", (list_name,))
        values = [row[0] for row in cursor.fetchall()]
        conn.close()
        return render_template('edit_list.html', list_name=list_name, values=values)
        pass

    # GET all values of a specific list
    cursor.execute("SELECT value FROM parameters WHERE list_name = ?", (list_name,))
    values = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template('edit_list.html', list_name=list_name, values=values)