from flask import Blueprint, render_template

main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route("/index")
@main.route("/")
def index():
    return render_template("index.html")


@main.route("/settings")
def settings_list():
    return "<h1>Pengaturan</h1>"


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
