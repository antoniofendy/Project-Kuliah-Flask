
from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.movie import MovieForm
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.controllers import movie as movie_controller

bp = Blueprint("movie", __name__)

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