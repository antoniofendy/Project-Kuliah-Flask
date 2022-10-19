from flask import Blueprint, render_template, request

from app.forms import staff

bp = Blueprint("main", __name__)


@bp.route("/index")
@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/settings")
def settings_list():
    return "<h1>Pengaturan</h1>"


@bp.route("/customers")
def customers_list():
    return "<h1>Daftar Pelanggan</h1>"


@bp.route("/staffs")
def staffs_list():
    return "<h1>Daftar Staf</h1>"
