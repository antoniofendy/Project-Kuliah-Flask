from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.movie_category import CategoryForm
from kelompok_1_uts.models.movie_category import MovieCategory
from kelompok_1_uts.controllers import movie_category as category_controller

bp = Blueprint(
    "movie_category", __name__, template_folder="templates", static_folder="static"
)


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def index(id):
    if id:
        form = CategoryForm()
        data = category_controller.get(id)

        return render_template("movie_category/form.html", form=form, data=data)

    data = category_controller.get_all()

    return render_template("movie_category/list.html", data=data)


@bp.route("/create", methods=["GET", "POST"])
def create():
    form = CategoryForm()
    if request.method == "POST":
        category_controller.create(
            MovieCategory(
                category_name=request.form.get("category_name"),
            )
        )

        flash("Data kategori berhasil ditambahkan.", category="success")
        return redirect(url_for("movie_category.index"))

    return render_template("movie_category/form.html", form=form, data=None)


@bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    category_controller.update(
        {
            "id": int(id),
            "category_name": request.form.get("category_name"),
        }
    )

    flash("Data kategori berhasil diubah.", category="primary")
    return redirect(url_for("movie_category.index"))


@bp.route("/delete", methods=["POST"])
def delete():
    category_controller.delete(request.form.get("id"))
    return redirect(url_for("movie_category.index", id=None))
