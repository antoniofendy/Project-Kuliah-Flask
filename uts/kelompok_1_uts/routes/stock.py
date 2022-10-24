from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts import db
from kelompok_1_uts.models.movie import Movie

from kelompok_1_uts.controllers import stock as stock_controller
from kelompok_1_uts.forms.stock import StockForm
from kelompok_1_uts.models.stock import Stock


bp = Blueprint("stock", __name__, template_folder="templates", static_folder="static")


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def show(id):
    if id:
        form = StockForm()
        data = stock_controller.get(id)

        movies = db.session.query(Movie)
        movies_list = [(m.id, m.title) for m in movies]

        form.movie.choices = movies_list
        form.movie.default = data.movie_id

        title = [title for title in movies_list if title[0] == data.movie_id][0][1]

        form.process()

        # form.gender.choices = [("laki-laki", "Laki-laki"), ("perempuan", "Perempuan")]

        return render_template("stock/form.html", form=form, data=data, title=title)

    data = stock_controller.get_all()
    return render_template("stock/list.html", data=data)


@bp.route("/create", methods=["GET", "POST"])
def create():
    form = StockForm()

    movies = db.session.query(Movie)
    movies_list = [(m.id, m.title) for m in movies]

    form.movie.choices = movies_list

    if request.method == "POST":
        print(request.form)
        stock_controller.create(
            Stock(
                qty=request.form.get("qty"),
                price=request.form.get("price"),
                movie_id=request.form.get("movie"),
            )
        )

        flash("Data stok berhasil ditambahkan.", category="success")
        return redirect(url_for("stock.show"))

    return render_template("stock/form.html", form=form, data=None)


@bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    stock_controller.update(
        {
            "id": int(id),
            "qty": request.form.get("qty"),
            "price": request.form.get("price"),
        }
    )

    flash("Data stok berhasil diubah.", category="primary")
    return redirect(url_for("stock.show"))


@bp.route("/delete", methods=["POST"])
def delete():
    stock_controller.delete(request.form.get("id"))

    flash("Data stok berhasil dihapus.", category="danger")
    return redirect(url_for("stock.show"))
