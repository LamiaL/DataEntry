from flask import Blueprint, render_template,session
from app.auth import login_required,admin_required


data_bp = Blueprint("data", __name__)

@data_bp.route("/data")
@login_required
@admin_required
def data_view():
    user_role = session.get('role')
    return render_template("data.html", role=user_role)