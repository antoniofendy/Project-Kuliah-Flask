from flask import Blueprint, render_template, url_for

from kelompok_1_uts.forms.movie import MovieForm
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.controllers import movie as movie_controller

bp = Blueprint("stock", __name__, template_folder="templates", static_folder="static")


@bp.route("/")
# rename index to index_stock because of index func already used for movie in this case
def index_stock():
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

## Movies Route

@bp.route("/index")
def index():
    data = movie_controller.get_all()
    return render_template("movie/list.html", data=data)
    

@bp.route("/create", methods=["GET", "POST"])
def create():
    form = MovieForm()
    if request.method == "POST":
        movie_controller.create(
            Movie(
                title=request.form.get("title"),
                synopsis=request.form.get("synopsis"),
                picture=request.form.get("picture"),
                duration=request.form.get("duration"),
                actor=request.form.get("actor"),
            )
        )

        flash("Data staf berhasil ditambahkan.", category="success")
        return redirect(url_for("movie.index"))

    return render_template("movie/form.html", form=form, data=None)


@bp.route("/show")
def show():
    return "<h1>Detail</h1>"


@bp.route("/delete",  methods=["POST"])
def delete():
    movie_controller.delete(request.form.get("id"))

    flash("Data member berhasil dihapus.", category="danger")
    return redirect(url_for("movie.index"))
