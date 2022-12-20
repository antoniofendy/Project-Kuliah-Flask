from flask import Blueprint, render_template, request, flash, url_for, redirect

from kelompok_1_uas.admin.forms.car import CarForm
from kelompok_1_uas.admin.controllers import car as car_controller
from kelompok_1_uas.admin.models.car import Car

admin_md_car_bp = Blueprint(
    "admin_md_car",
    __name__,
    url_prefix="/admin/master-data/car",
    template_folder="../templates",
    static_folder="../static",
)


@admin_md_car_bp.route("/", defaults={"id": None})
@admin_md_car_bp.route("/<int:id>")
def read(id):
    if id:
        form = CarForm()
        data = car_controller.get(id)
        form.address.data = data.address
        form.address()

        return render_template("admin/master-data/car/form.html", form=form, data=data)

    return render_template(
        "admin/master-data/car/list.html", data=car_controller.get_all()
    )


@admin_md_car_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        car_controller.create(
            Car(
                name=request.form.get("name"),
                address=request.form.get("address"),
            )
        )

        flash("Garasi baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_md_car.read"))

    return render_template(
        "admin/master-data/car/form.html", form=CarForm(), data=None
    )


@admin_md_car_bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "name": request.form.get("name"),
        "address": request.form.get("address"),
    }

    car_controller.update(data)

    flash("Garasi berhasil diubah.", category="primary")
    return redirect(url_for("admin_md_car.read"))


@admin_md_car_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    car_controller.delete(id_)

    flash("Garasi berhasil dihapus.", category="info")
    return redirect(url_for("admin_md_car.read"))
