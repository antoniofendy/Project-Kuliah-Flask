from flask import Blueprint, render_template

rental = Blueprint(
    "rental", __name__, template_folder="templates", static_folder="static"
)


@rental.route("/")
def index():
    return "<h1>Rental</h1>"


@rental.route("/rent")
def rent():
    return "<h1>Sewa</h1>"


@rental.route("/return")
def rent_return():
    return "<h1>Kembali</h1>"


@rental.route("/rents")
def rent_list():
    return "<h1>Daftar Sewa</h1>"


@rental.route("/payments")
def payment_list():
    return "<h1>Daftar Pembayaran</h1>"
