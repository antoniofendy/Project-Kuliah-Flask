from flask import Blueprint, render_template, request, flash, url_for, redirect,session

from kelompok_1_uas.admin.forms.charge_rule import ChargeRuleForm
from kelompok_1_uas.admin.controllers import charge_rule as charge_rule_controller
from kelompok_1_uas.admin.models.charge_rule import ChargeRule

admin_charge_rule_bp = Blueprint(
    "admin_charge_rule",
    __name__,
    url_prefix="/admin/charge_rule",
    template_folder="../templates",
)


@admin_charge_rule_bp.route("/", defaults={"id": None})
@admin_charge_rule_bp.route("/<int:id>")
def read(id):
    if('user' in session):
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
    return render_template("admin/login.html")


@admin_charge_rule_bp.route("/create", methods=["GET", "POST"])
def create():
    if('user' in session):
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
    return render_template("admin/login.html")


@admin_charge_rule_bp.route("/update", methods=["POST"])
def update():
    if('user' in session):
        data = {
            "id": request.form.get("id"),
            "name": request.form.get("name"),
            "amount": request.form.get("amount"),
            "type": request.form.get("type"),
        }

        charge_rule_controller.update(data)

        flash("Aturan denda berhasil diubah.", category="primary")
        return redirect(url_for("admin_charge_rule.read"))
    return render_template("admin/login.html")


@admin_charge_rule_bp.route("/delete", methods=["POST"])
def delete():
    if('user' in session):
        id_ = request.form.get("id")

        charge_rule_controller.delete(id_)

        flash("Aturan denda berhasil dihapus.", category="info")
        return redirect(url_for("admin_charge_rule.read"))
    return render_template("admin/login.html")
