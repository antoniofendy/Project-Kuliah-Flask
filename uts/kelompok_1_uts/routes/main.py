from calendar import c
from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.staff import StaffForm
from kelompok_1_uts.models.staff import Staff
from kelompok_1_uts.controllers import staff as staff_controller

bp = Blueprint("main", __name__)


@bp.route("/index")
@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/settings")
def settings_list():
    return "<h1>Pengaturan</h1>"


@bp.route("/customers")
def customers_list():
    return "<h1>Daftar Pelanggan</h1>"


@bp.route("/staff", defaults={"id": None})
@bp.route("/staff/<int:id>")
def show_staff(id):
    if id:
        form = StaffForm()
        data = staff_controller.get(id)

        return render_template("staff/form.html", form=form, data=data)

    data = staff_controller.get_all()

    return render_template("staff/list.html", data=data)


@bp.route("/staff/new", methods=["GET", "POST"])
def new_staff():
    form = StaffForm()

    if request.method == "POST":
        staff_controller.create(
            Staff(
                name=request.form.get("name"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                phone=request.form.get("phone"),
                address=request.form.get("address"),
                picture=request.form.get("picture"),
            )
        )

        flash("Data staf berhasil ditambahkan.", category="success")
        return redirect(url_for("main.show_staff", id=None))

    return render_template("staff/form.html", form=form, data=None)


@bp.route("/staff/update/<int:id_>", methods=["POST"])
def update_staff(id_):
    staff_controller.update(
        {
            "id": int(id_),
            "name": request.form.get("name"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "picture": request.form.get("picture"),
        }
    )

    flash("Data staf berhasil diubah.", category="primary")
    return redirect(url_for("main.show_staff", id=None))


@bp.route("/staff/delete/<int:id_>", methods=["POST"])
def delete_staff(id_):
    staff_controller.delete({"id": int(id_)})

    flash("Data staf berhasil dihapus.", category="danger")
    return redirect(url_for("main.show_staff", id=None))
