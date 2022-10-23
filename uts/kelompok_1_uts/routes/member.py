from calendar import c
from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.member import MemberForm
from kelompok_1_uts.models.member import Member
from kelompok_1_uts.controllers import member as member_controller

bp = Blueprint("member", __name__)

@bp.route("/index")
def index():
    data = member_controller.get_all()
    return render_template("member/list.html", data=data)
    

@bp.route("/create", methods=["GET", "POST"])
def create():
    form = MemberForm()
    if request.method == "POST":
        member_controller.create(
            Member(
                name=request.form.get("name"),
                gender=request.form.get("gender"),
                birth=request.form.get("birth"),
                address=request.form.get("address"),
                phone=request.form.get("phone"),
                email=request.form.get("email"),
            )
        )

        flash("Data staf berhasil ditambahkan.", category="success")
        return redirect(url_for("member.index"))

    return render_template("member/form.html", form=form, data=None)


@bp.route("/show")
def show():
    return "<h1>Detail</h1>"


@bp.route("/delete",  methods=["POST"])
def delete():
    member_controller.delete(request.form.get("id"))

    flash("Data member berhasil dihapus.", category="danger")
    return redirect(url_for("member.index"))

