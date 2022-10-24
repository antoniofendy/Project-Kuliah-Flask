import os

from flask import Blueprint, flash, redirect, render_template, request, url_for

from werkzeug.utils import secure_filename

from kelompok_1_uts.forms.staff import StaffForm
from kelompok_1_uts.models.staff import Staff
from kelompok_1_uts.controllers import staff as staff_controller

from random import *

bp = Blueprint("main", __name__)

UPLOAD_FOLDER = "kelompok_1_uts/static/upload/staff"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/index")
@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/settings")
def settings_list():
    return "<h1>Pengaturan</h1>"


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

        unique_pic_name = randint(100, 99999)

        file_ext = None
        file = request.files["picture"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    "{fname}{fext}".format(fname=unique_pic_name, fext=file_ext),
                )
            )

        staff_controller.create(
            Staff(
                name=request.form.get("name"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                phone=request.form.get("phone"),
                address=request.form.get("address"),
                picture="{fname}{fext}".format(fname=unique_pic_name, fext=file_ext),
            )
        )

        flash("Data staf berhasil ditambahkan.", category="success")
        return redirect(url_for("main.show_staff", id=None))

    return render_template("staff/form.html", form=form, data=None)


@bp.route("/staff/update/<int:id_>", methods=["POST"])
def update_staff(id_):

    old_data = staff_controller.get(id_)

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
                        fname=old_data.picture.partition(".")[0], fext=file_ext
                    ),
                )
            )

        staff_controller.update(
            {
                "id": int(id_),
                "name": request.form.get("name"),
                "phone": request.form.get("phone"),
                "address": request.form.get("address"),
                "picture": "{fname}{fext}".format(
                    fname=old_data.picture.partition(".")[0], fext=file_ext
                ),
            }
        )

    else:
        staff_controller.update(
            {
                "id": int(id_),
                "name": request.form.get("name"),
                "phone": request.form.get("phone"),
                "address": request.form.get("address"),
                "picture": old_data.picture,
            }
        )

    flash("Data staf berhasil diubah.", category="primary")
    return redirect(url_for("main.show_staff", id=None))


@bp.route("/staff/delete/", methods=["POST"])
def delete_staff():

    old_data = staff_controller.get(request.form.get("id"))

    os.remove(os.path.join(UPLOAD_FOLDER, old_data.picture))
    staff_controller.delete(request.form.get("id"))

    flash("Data staf berhasil dihapus.", category="danger")
    return redirect(url_for("main.show_staff", id=None))
