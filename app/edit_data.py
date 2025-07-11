from flask import Blueprint, redirect, url_for, flash
from app.services.data_function import edit_data_generic,update_data_generic
from app.config import TABLE_CONFIG
from app.auth import login_required,admin_required

edit_data_bp = Blueprint("edit_data", __name__)

@edit_data_bp.route("/edit_<idTable>/<int:id>")
@login_required
@admin_required
def dynamic_edit(idTable, id):
    config = TABLE_CONFIG.get(idTable)
    if not config:
        flash("Invalid table", "danger")
        return redirect(url_for("dashboard.dashboard_view"))

    return edit_data_generic(id, config["db_path"], config["table_name"], config["template"], config["redirect"])


@edit_data_bp.route("/update_<idTable>/<int:id>", methods=["POST"])
@login_required
@admin_required
def dynamic_update(idTable, id):
    config = TABLE_CONFIG.get(idTable)
    if not config:
        flash("Table inconnue", "danger")
        return redirect(url_for("dashboard.dashboard_view"))

    return update_data_generic(
        id=id,
        bd_path=config["db_path"],
        table_name=config["table_name"],
        fields=config["fields"],
        redirect_endpoint=config["redirect"]
    )