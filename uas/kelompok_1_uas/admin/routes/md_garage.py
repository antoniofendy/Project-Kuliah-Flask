from flask import Blueprint, render_template, request, flash, url_for, redirect

from kelompok_1_uas.admin.forms.garage import GarageForm
from kelompok_1_uas.admin.controllers import garage as garage_controller
from kelompok_1_uas.admin.models.garage import Garage

admin_md_garage_bp = Blueprint(
    "admin_md_garage",
    __name__,
    url_prefix="/admin/master-data/garage",
    template_folder="../templates",
    static_folder="../static",
)


@admin_md_garage_bp.route("/", defaults={"id": None})
@admin_md_garage_bp.route("/<int:id>")
def read(id):
    if id:
        form = GarageForm()
        data = garage_controller.get(id)
        form.address.data = data.address
        form.address()

        return render_template("admin/master-data/garage/form.html", form=form, data=data)

    return render_template(
        "admin/master-data/garage/list.html", data=garage_controller.get_all()
    )


@admin_md_garage_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        garage_controller.create(
            Garage(
                name=request.form.get("name"),
                address=request.form.get("address"),
            )
        )

        flash("Garasi baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_md_garage.read"))

    return render_template(
        "admin/master-data/garage/form.html", form=GarageForm(), data=None
    )


@admin_md_garage_bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "name": request.form.get("name"),
        "address": request.form.get("address"),
    }

    garage_controller.update(data)

    flash("Garasi berhasil diubah.", category="primary")
    return redirect(url_for("admin_md_garage.read"))


@admin_md_garage_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    garage_controller.delete(id_)

    flash("Garasi berhasil dihapus.", category="info")
    return redirect(url_for("admin_md_garage.read"))
