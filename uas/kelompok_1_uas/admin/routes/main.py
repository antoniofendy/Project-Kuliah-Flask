from flask import Blueprint, render_template
from flask_login import login_required

admin_main_bp = Blueprint(
    "admin_main",
    __name__,
    url_prefix="/admin",
    template_folder="../templates",
)


@admin_main_bp.route("/")
@login_required
def index():
    return render_template("admin/index.html")
