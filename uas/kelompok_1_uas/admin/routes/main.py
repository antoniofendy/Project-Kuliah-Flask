from flask import Blueprint, render_template, session
from kelompok_1_uas.admin.models.admin import Admin

admin_main_bp = Blueprint(
    "admin_main",
    __name__,
    url_prefix="/admin",
    template_folder="../templates",
)


@admin_main_bp.route("/")
def index():
    # admin = Admin.query.filter_by(id=session['user']).first()
    if('user' in session):
        return render_template("admin/index.html")

    return render_template("admin/login.html")
