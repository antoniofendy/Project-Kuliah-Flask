from flask import Blueprint, redirect, render_template, url_for, request, flash

from kelompok_1_uas.admin.forms.charge_rule import ChargeRuleForm
from kelompok_1_uas.admin.controllers import charge_rule as charge_rule_controller
from kelompok_1_uas.admin.models.charge_rule import ChargeRule

bp = Blueprint(
    "admin_charge_rule",
    __name__,
    url_prefix="/admin/charge_rule",
    template_folder="templates",
    static_folder="../static",
)


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def read(id):
    if id:
        form = ChargeRuleForm()
        data = charge_rule_controller.get(id)

        # Remove default "empty" choice
        form.type.choices = [("PERCENTAGE", "Persentase"), ("NOMINAL", "Nominal")]

        # Set selected charge rule type
        form.type.default = data.type.name

        form.process()

        return render_template("admin/charge_rule/form.html", form=form, data=data)

    return render_template(
        "admin/charge_rule/list.html", data=charge_rule_controller.get_all()
    )


@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        charge_rule_controller.create(
            ChargeRule(
                name=request.form.get("name"),
                amount=request.form.get("amount"),
                type=request.form.get("type"),
            )
        )

        flash("Aturan denda baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_charge_rule.read"))

    return render_template(
        "admin/charge_rule/form.html", form=ChargeRuleForm(), data=None
    )


@bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "name": request.form.get("name"),
        "amount": request.form.get("amount"),
        "type": request.form.get("type"),
    }

    charge_rule_controller.update(data)

    flash("Aturan denda berhasil diubah.", category="primary")
    return redirect(url_for("admin_charge_rule.read"))


@bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    charge_rule_controller.delete(id_)

    flash("Aturan denda berhasil dihapus.", category="info")
    return redirect(url_for("admin_charge_rule.read"))
