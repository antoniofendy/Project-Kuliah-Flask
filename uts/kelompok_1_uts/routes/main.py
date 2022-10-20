from flask import Blueprint, render_template, request

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


@bp.route("/staffs")
def staffs_list():
    data = staff_controller.get_all()

    return render_template("staff/list.html", data=data)


@bp.route("/staffs/new", methods=["GET", "POST"])
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
        return render_template("staff/form.html")

    return render_template("staff/form.html", form=form, new=True)
