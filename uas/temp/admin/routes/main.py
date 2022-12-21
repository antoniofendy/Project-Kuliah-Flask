from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint(
    "admin_main",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="../static",
)


@bp.route("/index")
@bp.route("/")
def index():
    return render_template("admin/index.html")
