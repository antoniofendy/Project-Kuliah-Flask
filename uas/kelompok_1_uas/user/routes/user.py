from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.user.forms.user import UserForm
from kelompok_1_uas import db
from kelompok_1_uas.user.controllers import user as user_controller
from sqlalchemy import exc

import hashlib

from flask import Blueprint, render_template, request, flash, url_for, redirect

user_user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user",
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


@user_user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        md5_password = hashlib.md5(request.form.get("password").encode())
        md5_password_confirm = hashlib.md5(request.form.get("password_confirm").encode())

        if md5_password.hexdigest() == md5_password_confirm.hexdigest():
            try:
                user_controller.create(
                    User(
                        name=request.form.get("name"),
                        phone=request.form.get("phone"),
                        address=request.form.get("address"),
                        date_of_birth=request.form.get("date_of_birth"),
                        sex=request.form.get("sex"),
                        occupation=request.form.get("occupation"),
                        email=request.form.get("email"),
                        password=md5_password.hexdigest(),
                    )
                )
                flash("Berhasil registrasi, silahkan login.", category="success")
                return redirect(url_for("user.login"))

            except exc.SQLAlchemyError:
                flash("Terjadi kesalahan sistem.", category="danger")
                return redirect(url_for("user.register"))

        flash("Password dan password konfirmasi tidak sama.", category="danger")
        return redirect(url_for("user.register"))

    return render_template("site/registerUser.html")


@user_user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        md5_password = hashlib.md5(password.encode())

        user = db.session.query(User).filter_by(email=email, password=md5_password.hexdigest()).first()

        # cek kredensial user
        if not user:
            flash('Email atau password tidak sesuai.', category="warning")
            return redirect(url_for('user.login'))

        # jika user terdaftar
        return redirect(url_for("user_main.index"))

    return render_template("site/loginUser.html")
