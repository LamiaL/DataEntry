from flask import Blueprint, render_template, session
from app.auth import login_required

form_bp = Blueprint("form", __name__)  # Renaming the blueprint to avoid confusion

@form_bp.route("/form")
@login_required
def form_view():
    user_role = session.get('role')  # Assuming role is stored in session
    return render_template("form.html", role=user_role)  # Render the dashboard page