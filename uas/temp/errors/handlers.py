from flask import render_template

from flask import Blueprint

error_bp = Blueprint(
    "errors",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@error_bp.errorhandler(404)
def page_not_found(e):
    print(error_bp.root_path)
    return render_template("admin/404.html"), 404


@error_bp.errorhandler(405)
def method_not_allowed(e):
    return render_template("admin/404.html"), 405
