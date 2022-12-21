from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.user.forms.user import UserForm
from kelompok_1_uas.user.controllers import user as user_controller

from flask import Blueprint, render_template, request, flash, url_for, redirect

user_main_bp = Blueprint(
    "user_main",
    __name__,
    url_prefix="/",
    template_folder="../templates",
)


@user_main_bp.route("/")
def index():
    return render_template("site/index.html")