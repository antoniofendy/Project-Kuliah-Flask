from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.member import MemberForm
from kelompok_1_uts.models.member import Member
from kelompok_1_uts.controllers import member as member_controller

bp = Blueprint("member", __name__, template_folder="templates", static_folder="static")


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def show(id):
    if id:
        form = MemberForm()
        data = member_controller.get(id)

        form.gender.choices = [("laki-laki", "Laki-laki"), ("perempuan", "Perempuan")]
        form.gender.default = data.gender

        form.process()

        return render_template("member/form.html", form=form, data=data)

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
        return redirect(url_for("member.show"))

    return render_template("member/form.html", form=form, data=None)


@bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    member_controller.update(
        {
            "id": int(id),
            "name": request.form.get("name"),
            "gender": request.form.get("gender"),
            "birth": request.form.get("birth"),
            "address": request.form.get("address"),
            "phone": request.form.get("phone"),
            "email": request.form.get("email"),
        }
    )

    flash("Data member berhasil diubah.", category="primary")
    return redirect(url_for("member.show"))


@bp.route("/delete", methods=["POST"])
def delete():
    member_controller.delete(request.form.get("id"))

    flash("Data member berhasil dihapus.", category="danger")
    return redirect(url_for("member.show"))
