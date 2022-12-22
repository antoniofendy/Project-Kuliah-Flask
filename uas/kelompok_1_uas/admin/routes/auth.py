from flask import Blueprint, render_template, request, flash, url_for, redirect, session

from kelompok_1_uas.admin.forms.admin import AdminForm
from kelompok_1_uas.admin.controllers import admin as admin_controller
from kelompok_1_uas.admin.models.admin import Admin

auth_bp = Blueprint(
    "admin_auth",
    __name__,
    url_prefix="/admin/auth",
    template_folder="../templates",
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        admin = Admin.query.filter_by(email=email).first()

        # Check if user exists
        if not admin or not (password == admin.password) and False:
            flash("Periksa kembali email dan password Anda.", category="danger")
            return redirect(url_for("admin_auth.login"))

        session['user'] = admin.id
        return redirect(url_for("admin_main.index"))

    return render_template("admin/login.html")


@auth_bp.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for("admin_main.index"))
