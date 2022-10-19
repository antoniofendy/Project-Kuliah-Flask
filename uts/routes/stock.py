from flask import Blueprint, render_template, url_for

stock = Blueprint(
    "stock", __name__, template_folder="templates", static_folder="static"
)

# @stok.route("/daftar")
@stock.route("/")
def index():
    return "<h1>Stok</h1>"


@stock.route("/film")
def film_list():
    return "<h1>Daftar Film</h1>"


@stock.route("/film/<int:id>")
def show_film(id):
    if id:
        return "<h1>Tampil Film</h1>"


@stock.route("/film-category")
def film_category_list():
    return "<h1>Daftar Kategori Film</h1>"


@stock.route("/film-category/<int:id>")
def show_film_category(id):
    if id:
        return "<h1>Tampil Kategori Film</h1>"
