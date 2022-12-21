from flask import render_template
from kelompok_1_uas.admin.errors import admin_error_bp


@admin_error_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@admin_error_bp.app_errorhandler(405)
def method_not_allowed(e):
    return render_template("404.html"), 405
