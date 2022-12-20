from flask import Blueprint, render_template

site_main_bp = Blueprint(
    "site_main",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@site_main_bp.route("/")
def index():
    return render_template("site/index.html")
