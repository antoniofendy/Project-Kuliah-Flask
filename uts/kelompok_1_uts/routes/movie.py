import os

from flask import Blueprint, flash, redirect, render_template, request, url_for

from werkzeug.utils import secure_filename

from kelompok_1_uts.forms.movie import MovieForm
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.models.movie_category import MovieCategory
from kelompok_1_uts.controllers import movie as movie_controller

from kelompok_1_uts import db

bp = Blueprint("movie", __name__, template_folder="templates",
               static_folder="static")

UPLOAD_FOLDER = "kelompok_1_uts/static/upload/movie"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def index(id):
    if id:
        form = MovieForm()
        data = movie_controller.get(id)

        movie_category = (
            db.session.query(MovieCategory).order_by(
                MovieCategory.category_name).all()
        )
        form.category.choices = [(c.id, c.category_name)
                                for c in movie_category]

        for c in movie_category:
            if c.id == data.movie_category_id:
                form.category.default = c.id

        form.process()

        return render_template("movie/form.html", form=form, data=data)

    data = movie_controller.get_all()

    return render_template("movie/list.html", data=data)


@bp.route("/create", methods=["GET", "POST"])
def create():
    form = MovieForm()
    if request.method == "POST":

        file_ext = None
        file = request.files["picture"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    "{fname}{fext}".format(
                        fname=request.form.get("title"), fext=file_ext
                    ),
                )
            )

        movie_controller.create(
            Movie(
                title=request.form.get("title"),
                synopsis=request.form.get("synopsis"),
                picture="{fname}{fext}".format(
                    fname=request.form.get("title"), fext=file_ext
                ),
                duration=request.form.get("duration"),
                actor=request.form.get("actor"),
                movie_category_id=request.form.get("category"),
            )
        )

        flash("Data film berhasil ditambahkan.", category="success")
        return redirect(url_for("movie.index"))

    movie_category = (
        db.session.query(MovieCategory).order_by(
            MovieCategory.category_name).all()
    )

    if not movie_category:
        flash("Tidak ada data kategori film.", category="info")
        return redirect(url_for("movie.index", id=None))

    form.category.choices = [(c.id, c.category_name) for c in movie_category]

    return render_template("movie/form.html", form=form, data=None)


@bp.route("/update/<int:id>", methods=["POST"])
def update(id):

    old_data = movie_controller.get(id)

    file = request.files["picture"]

    if file.filename != "":
        file_ext = None

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    "{fname}{fext}".format(
                        fname=old_data.title, fext=file_ext),
                )
            )

        movie_controller.update(
            {
                "id": int(id),
                "title": request.form.get("title"),
                "synopsis": request.form.get("synopsis"),
                "duration": request.form.get("duration"),
                "actor": request.form.get("actor"),
                "picture": "{fname}{fext}".format(fname=old_data.title, fext=file_ext),
                "movie_category_id": request.form.get("category"),
            }
        )
    else:
        movie_controller.update(
            {
                "id": int(id),
                "title": request.form.get("title"),
                "synopsis": request.form.get("synopsis"),
                "duration": request.form.get("duration"),
                "actor": request.form.get("actor"),
                "picture": old_data.picture,
                "movie_category_id": request.form.get("category"),
            }
        )

    flash("Data film berhasil diubah.", category="primary")
    return redirect(url_for("movie.index"))


@bp.route("/delete", methods=["POST"])
def delete():
    old_data = movie_controller.get(request.form.get("id"))
    ##os.remove(os.path.join(UPLOAD_FOLDER, old_data.picture))

    if movie_controller.delete(request.form.get("id")):
        flash("Data Film berhasil dihapus.", category="info")

    return redirect(url_for("movie.index", id=None))
