from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.movie_category import CategoryForm
from kelompok_1_uts.models.movie_category import MovieCategory
from kelompok_1_uts.controllers import movie as category_controller

bp = Blueprint("category", __name__, template_folder="templates", static_folder="static")

@bp.route("/")
def index():
    
    ##data = movie_controller.get_all()
    return "<h2>category List</h2>" ##render_template("movie/list.html", data=data)
    

@bp.route("/create", methods=["GET", "POST"])
def create():
    form = CategoryForm()
    if request.method == "POST":
        category_controller.create(
            MovieCategory(
                name=request.form.get(""),
            )
        )

        flash("Data staf berhasil ditambahkan.", category="success")
        return redirect(url_for("category.index"))

    return render_template("category/form.html", form=form, data=None)


@bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    category_controller.update(
        {
            "id": int(id),
            "name": request.form.get("name"),
        }
    )

    flash("Data kategori berhasil diubah.", category="primary")
    return redirect(url_for("category.index"))

@bp.route("/show")
def show():
    return "<h1>Detail</h1>"


@bp.route("/delete",  methods=["POST"])
def delete():
    category_controller.delete(request.form.get("id"))

    flash("Data kategori berhasil dihapus.", category="danger")
    return redirect(url_for("category.index"))
