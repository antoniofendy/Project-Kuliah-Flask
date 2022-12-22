import os

from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from kelompok_1_uas.user.models.user import User

admin_member_bp = Blueprint(
    "admin_member",
    __name__,
    url_prefix="/admin/member",
    template_folder="../templates",
)


@admin_member_bp.route("/")
def read():
    member = User.query.all()
    return render_template("admin/member/list.html", member=member)
