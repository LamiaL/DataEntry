from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "danger")
            return redirect(url_for("auth_login_bp.login"))  # Adjust route name
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Accès refusé. Seuls les admins peuvent accéder à cette page.", "danger")
            return redirect(url_for("dashboard.dashboard_view"))
        return f(*args, **kwargs)
    return decorated_function