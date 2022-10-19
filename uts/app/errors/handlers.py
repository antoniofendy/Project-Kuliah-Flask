from flask import render_template
from app.errors import bp


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
