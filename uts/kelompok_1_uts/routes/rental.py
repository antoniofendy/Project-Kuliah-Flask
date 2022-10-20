from flask import Blueprint, render_template

bp = Blueprint("rental", __name__, template_folder="templates", static_folder="static")


@bp.route("/")
def index():
    return "<h1>Daftar Sewa</h1>"


@bp.route("/new")
def new_rent():
    return "<h1>Sewa Baru</h1>"


@bp.route("/return")
def rent_return():
    return "<h1>Kembali</h1>"


@bp.route("/payments")
def payment_list():
    return "<h1>Daftar Pembayaran</h1>"
