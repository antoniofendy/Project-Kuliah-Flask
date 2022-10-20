from flask import Blueprint, render_template, url_for

bp = Blueprint("stock", __name__, template_folder="templates", static_folder="static")


@bp.route("/")
def index():
    return "<h1>Stok</h1>"


@bp.route("/movie", defaults={"id": None})
@bp.route("/movie/<int:id>")
def movie(id):
    if id:
        return "<h1>Tampil Film</h1>"

    return "<h1>Daftar Film</h1>"


@bp.route("/movie_category", defaults={"id": None})
@bp.route("/movie_category/<int:id>")
def movie_category(id):
    if id:
        return "<h1>Tampil Kategori Film</h1>"

    return "<h1>Daftar Kategori Film</h1>"
