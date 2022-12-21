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
                name=request.form.get("name"),
                phone=request.form.get("phone"),
                address=request.form.get("address"),
                date_of_birth=request.form.get("date_of_birth"),
                sex=request.form.get("sex"),
                occupation=request.form.get("occupation"),
                email=request.form.get("email"),
                password=request.form.get("password"),
            )
        )

        flash("Data user baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_admin.read"))

    return render_template("user/user/form.html", form=UserForm(), data=None)

@user_user_bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "name": request.form.get("name"),
        "phone": request.form.get("phone"),
        "date_of_birth": request.form.get("date_of_birth"),
        "sex": request.form.get("sex"),
        "occupation": request.form.get("occupation"),
        "email": request.form.get("email"),
        "address": request.form.get("address"),
        "password": request.form.get("password"),
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