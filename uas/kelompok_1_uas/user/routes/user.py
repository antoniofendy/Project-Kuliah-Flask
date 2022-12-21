from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.user.forms import UserForm
from kelompok_1_uas.user.controllers import user as user_controller

from flask import Blueprint, render_template, request, flash, url_for, redirect

user_user_bp = Blueprint(
    "user_user",
    __name__,
    url_prefix="/user/user",
    template_folder="../templates",
)

@user_user_bp.route("/", defaults={"id": None})
@user_user_bp.route("/<int:id>")
def read(id):
    if id:
        form = UserForm()
        data = user_controller.get(id)
        
        return render_template("user/user/form.html", form=form, data=data)
    
    return render_template("user/user/list.html", data=user_controller.get_all())


@user_user_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        user_controller.create(
            User(
                name=request.form.get("nameUser"),
                phone=request.form.get("phoneUser"),
                address=request.form.get("addressUser"),
                date_of_birth=request.form.get("date_of_birthUser"),
                sex=request.form.get("sexUser"),
                occupation=request.form.get("occupationUser"),
                email=request.form.get("emailUser"),
                password=request.form.get("passwordUser"),
            )
        )

        flash("Data user baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_admin.read"))

    return render_template("user/user/form.html", form=UserForm(), data=None)

@user_user_bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "nameUser": request.form.get("nameUser"),
        "phoneUser": request.form.get("phoneUser"),
        "date_of_birthUser": request.form.get("date_of_birthUser"),
        "sexUser": request.form.get("sexUser"),
        "occupationUser": request.form.get("occupationUser"),
        "emailUser": request.form.get("emailUser"),
        "addressUser": request.form.get("addressUser"),
        "passwordUser": request.form.get("passwordUs"),
    }

    user_controller.update(data)

    flash("Data user berhasil diubah.", category="primary")
    return redirect(url_for("user_user.read"))



@user_user_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")
    user_controller.delete(id_)
    
    flash("Data user berhasil dihapus", category="info")
    return redirect(url_for("user_user.read"))