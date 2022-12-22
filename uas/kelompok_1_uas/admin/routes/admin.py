from flask import Blueprint, render_template, request, flash, url_for, redirect, session

from kelompok_1_uas.admin.forms.admin import AdminForm
from kelompok_1_uas.admin.controllers import admin as admin_controller
from kelompok_1_uas.admin.models.admin import Admin

admin_admin_bp = Blueprint(
    "admin_admin",
    __name__,
    url_prefix="/admin/admin",
    template_folder="../templates",
)


@admin_admin_bp.route("/", defaults={"id": None})
@admin_admin_bp.route("/<int:id>")
def read(id):
    if('user' in session):
        if id:
            form = AdminForm()
            data = admin_controller.get(id)

            return render_template("admin/admin/form.html", form=form, data=data)

        return render_template("admin/admin/list.html", data=admin_controller.get_all())
    return render_template("admin/login.html")


@admin_admin_bp.route("/create", methods=["GET", "POST"])
def create():
    if('user' in session):
        if request.method == "POST":
            admin_controller.create(
                Admin(
                    name=request.form.get("name"),
                    phone=request.form.get("phone"),
                    address=request.form.get("address"),
                    email=request.form.get("email"),
                    password=request.form.get("password"),
                )
            )

            flash("Admin baru berhasil ditambahkan.", category="success")
            return redirect(url_for("admin_admin.read"))

        return render_template("admin/admin/form.html", form=AdminForm(), data=None)
    return render_template("admin/login.html")


@admin_admin_bp.route("/update", methods=["POST"])
def update():
    if('user' in session):
        data = {
            "id": request.form.get("id"),
            "name": request.form.get("name"),
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "password": request.form.get("password"),
        }

        admin_controller.update(data)

        flash("Admin berhasil diubah.", category="primary")
        return redirect(url_for("admin_admin.read"))
    return render_template("admin/login.html")

@admin_admin_bp.route("/delete", methods=["POST"])
def delete():
    if('user' in session):
        id_ = request.form.get("id")

        admin_controller.delete(id_)

        flash("Admin berhasil dihapus.", category="info")
        return redirect(url_for("admin_admin.read"))
    return render_template("admin/login.html")
