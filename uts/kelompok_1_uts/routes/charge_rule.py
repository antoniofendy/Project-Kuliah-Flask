from calendar import c
from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts.forms.charge_rule import ChargeRuleForm
from kelompok_1_uts.models.charge_rule import ChargeRule
from kelompok_1_uts.controllers import charge_rule as charge_rule_controller

bp = Blueprint(
    "charge_rule", __name__, template_folder="templates", static_folder="static"
)


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def show(id):
    if id:
        form = ChargeRuleForm()
        data = charge_rule_controller.get(id)

        form.type.choices = [("PERCENTAGE", "Persentase"), ("NOMINAL", "Nominal")]
        form.type.default = data.type.name

        form.process()

        return render_template("charge_rule/form.html", form=form, data=data)

    data = charge_rule_controller.get_all()
    return render_template("charge_rule/list.html", data=data)


@bp.route("/create", methods=["GET", "POST"])
def create():
    form = ChargeRuleForm()
    if request.method == "POST":
        charge_rule_controller.create(
            ChargeRule(
                name=request.form.get("name"),
                amount=request.form.get("amount"),
                type=request.form.get("type"),
            )
        )

        flash("Aturan denda baru berhasil ditambahkan.", category="success")
        return redirect(url_for("charge_rule.show"))

    return render_template("charge_rule/form.html", form=form, data=None)


@bp.route("/update/<int:id>", methods=["POST"])
def update(id):
    charge_rule_controller.update(
        {
            "id": int(id),
            "name": request.form.get("name"),
            "amount": request.form.get("amount"),
            "type": request.form.get("type"),
        }
    )

    flash("Aturan denda berhasil diubah.", category="primary")
    return redirect(url_for("charge_rule.show"))


@bp.route("/delete", methods=["POST"])
def delete():
    charge_rule_controller.delete(request.form.get("id"))

    flash("Aturan denda berhasil dihapus.", category="info")
    return redirect(url_for("charge_rule.show"))
