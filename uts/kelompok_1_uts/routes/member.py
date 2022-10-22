from calendar import c
from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.staff import StaffForm
from kelompok_1_uts.models.member import Member
from kelompok_1_uts.controllers import staff as staff_controller

bp = Blueprint("member", __name__)

@bp.route("/index")
def index():
    return "<h1>Daftar Pelanggan</h1>"

