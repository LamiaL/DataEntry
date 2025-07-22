from flask import Blueprint, jsonify, render_template, session
from app.auth import login_required
from app.dataenvd import get_db_envd
from app.users import get_db
from app.dataenvrh import  get_db_rh
from app.dataenv import  get_db_inv
from app.dataenvm import  get_db_envm
from app.dataenvfin import  get_db_fin
from app.services.dashboard_data import get_entries_by_date,get_entries_by_agent
from app.config import DB_PATH_D, DB_PATH_RH, DB_PATH_FIN, DB_PATH, DB_PATH_M


dashboard_bp = Blueprint("dashboard", __name__)  

# Route to view dashboard
@dashboard_bp.route("/dashboard")
@login_required
def dashboard_view():
    
    user_role = session.get('role')  # Assuming role is stored in session

    db= get_db()
    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    db_rh = get_db_rh()
    RH_NB = db_rh.execute("SELECT COUNT(*) FROM entriesrh").fetchone()[0]

    db_fin = get_db_fin()
    FIN_NB = db_fin.execute("SELECT COUNT(*) FROM entriesfin").fetchone()[0]

    db_inv = get_db_inv()
    INV_NB = db_inv.execute("SELECT COUNT(*) FROM entries").fetchone()[0]

    db_invm = get_db_envm()
    INVM_NB = db_invm.execute("SELECT COUNT(*) FROM entriesenvm").fetchone()[0]

    db_invd = get_db_envd()
    INVD_NB = db_invd.execute("SELECT COUNT(*) FROM entriesenvd").fetchone()[0]
    
    return render_template("dashboard.html", total_users=total_users, RH_NB=RH_NB, INV_NB=INV_NB, FIN_NB=FIN_NB ,INVM_NB=INVM_NB, INVD_NB=INVD_NB , role=user_role)

@dashboard_bp.route("/api/entriesrh_by_date")
@login_required
def entriesrh_by_date():
    return jsonify(get_entries_by_date(DB_PATH_RH,"entriesrh"))

@dashboard_bp.route("/api/entriesrh_by_agent")
@login_required
def entriesrh_by_agent():
    return jsonify(get_entries_by_agent(DB_PATH_RH,"entriesrh"))

@dashboard_bp.route("/api/entriesfin_by_date")
@login_required
def entriesfin_by_date():
    return jsonify(get_entries_by_date(DB_PATH_FIN,"entriesfin"))

@dashboard_bp.route("/api/entriesfin_by_agent")
@login_required
def entriesfin_by_agent():
    return jsonify(get_entries_by_agent(DB_PATH_FIN,"entriesfin"))

@dashboard_bp.route("/api/entries_by_date")
@login_required
def entries_by_date():
    return jsonify(get_entries_by_date(DB_PATH,"entries"))

@dashboard_bp.route("/api/entries_by_agent")
@login_required
def entries_by_agent():
    return jsonify(get_entries_by_agent(DB_PATH,"entries"))

@dashboard_bp.route("/api/entriesm_by_date")
@login_required
def entriesm_by_date():
    return jsonify(get_entries_by_date(DB_PATH_M,"entriesenvm"))

@dashboard_bp.route("/api/entriesm_by_agent")
@login_required
def entriesm_by_agent():
    return jsonify(get_entries_by_agent(DB_PATH_M,"entriesenvm"))

@dashboard_bp.route("/api/entriesd_by_date")
@login_required
def entriesd_by_date():
    return jsonify(get_entries_by_date(DB_PATH_D,"entriesenvd"))

@dashboard_bp.route("/api/entriesd_by_agent")
@login_required
def entriesd_by_agent():
    return jsonify(get_entries_by_agent(DB_PATH_D,"entriesenvd"))