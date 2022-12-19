from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint(
    "user_main",
    __name__,
    template_folder="../templates",
    static_folder="../static",
)


@bp.route("/index")
@bp.route("/")
def index():
    return render_template("site/main.html")
