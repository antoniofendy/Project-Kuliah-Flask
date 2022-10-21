from flask import render_template
from kelompok_1_uts.errors import bp


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@bp.app_errorhandler(405)
def method_not_allowed(e):
    return render_template("404.html"), 405
