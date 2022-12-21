import os

from flask import Blueprint, render_template, request, flash, url_for, redirect

from werkzeug.utils import secure_filename

from kelompok_1_uas.admin.forms.car import CarForm
from kelompok_1_uas.admin.controllers import car as car_controller
from kelompok_1_uas.admin.models.stock import Stock

admin_md_stock_bp = Blueprint(
    "admin_md_stock",
    __name__,
    url_prefix="/admin/master-data/car",
    template_folder="../templates",
)

UPLOAD_FOLDER = "kelompok_1_uas/admin/static/upload/car"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_md_stock_bp.route("/", defaults={"id": None})
@admin_md_stock_bp.route("/<int:id>")
def read(id):
    if id:
        form = CarForm()
        data = car_controller.get(id)
        form.transmission.default = data.transmission.name
        form.fuel.default = data.fuel.name

        form.process()

        return render_template("admin/master-data/car/form.html", form=form, data=data)

    return render_template(
        "admin/master-data/car/list.html", data=car_controller.get_all()
    )


@admin_md_stock_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        file_ext = None
        file = request.files["picture"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    "{fbrand}-{fmodel}-{ftype}{fext}".format(
                        fbrand=request.form.get("brand"), 
                        fmodel=request.form.get("model"),
                        ftype=request.form.get("type"),
                        fext=file_ext
                    ),
                )
            )

        car_controller.create(
            Stock(
                model=request.form.get("model"),
                type=request.form.get("type"),
                brand=request.form.get("brand"),
                picture="{fbrand}-{fmodel}-{ftype}{fext}".format(
                        fbrand=request.form.get("brand"), 
                        fmodel=request.form.get("model"),
                        ftype=request.form.get("type"),
                        fext=file_ext
                    ),
                transmission=request.form.get("transmission"),
                seats=request.form.get("seats"),
                luggage=request.form.get("luggage"),
                fuel=request.form.get("fuel"),
            )
        )

        flash("Mobil baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_md_stock.read"))

    return render_template(
        "admin/master-data/car/form.html", form=CarForm(), data=None
    )


@admin_md_stock_bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "name": request.form.get("name"),
        "address": request.form.get("address"),
    }

    car_controller.update(data)

    flash("Mobil berhasil diubah.", category="primary")
    return redirect(url_for("admin_md_stock.read"))


@admin_md_stock_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    car_controller.delete(id_)

    flash("Mobil berhasil dihapus.", category="info")
    return redirect(url_for("admin_md_stock.read"))
