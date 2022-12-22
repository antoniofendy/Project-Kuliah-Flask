import os

from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from werkzeug.utils import secure_filename

from kelompok_1_uas import db

from kelompok_1_uas.admin.forms.rent import RentForm
from kelompok_1_uas.admin.controllers import rent as rent_controller
from kelompok_1_uas.admin.models.rent import Rent, RentStatus, PaymentType

from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.admin.models.charge_rule import ChargeRule, ChargeType
from kelompok_1_uas.admin.models.car import Car
from kelompok_1_uas.admin.models.stock import Stock
from kelompok_1_uas.admin.models.garage import Garage
from kelompok_1_uas.admin.models.reservation import Reservation, ReservationStatus

from datetime import datetime

admin_rent_bp = Blueprint(
    "admin_rent",
    __name__,
    url_prefix="/admin/rent",
    template_folder="../templates",
)

UPLOAD_FOLDER = "kelompok_1_uas/static/upload/receipt"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_rent_bp.route("/", defaults={"id": None})
@admin_rent_bp.route("/<int:id>")
def read(id):
    if id:
        form = RentForm()
        data = rent_controller.get(id)

        charge_rule = get_charge_rule_selections()
        form.charge_rule.choices = charge_rule
        users = get_user_selections()
        form.user.choices = users
        form.user.default = data.user_id
        form.reservation.choices = [
            (
                data.reservation_id,
                f"Reservasi {data.reservation_id}: {data.reservation.stock.car.brand} {data.reservation.stock.car.model}",
            )
        ]
        form.reservation.default = data.reservation_id
        form.type.default = data.type.name
        form.charge_rule.default = data.charge_rule_id
        form.status.default = data.status.name
        form.process()

        return render_template("admin/rent/form.html", form=form, data=data)

    return render_template("admin/rent/list.html", data=rent_controller.get_all())


@admin_rent_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        reservation = db.get_or_404(Reservation, request.form.get("reservation"))

        file_ext = None
        file = request.files["transfer_file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    "{fdate}-{fuser}-{fres}{fext}".format(
                        fdate=datetime.now().date(),
                        fuser=request.form.get("user"),
                        fres=request.form.get("reservation"),
                        fext=file_ext,
                    ),
                )
            )

        rent_controller.create(
            Rent(
                user_id=request.form.get("user"),
                stock_id=reservation.stock.id,
                reservation_id=request.form.get("reservation"),
                charge_rule_id=request.form.get("charge_rule") or None,
                type=request.form.get("type"),
                transfer_file="{fdate}-{fuser}-{fres}{fext}".format(
                    fdate=datetime.now().date(),
                    fuser=request.form.get("user"),
                    fres=request.form.get("reservation"),
                    fext=file_ext,
                ),
                total=request.form.get("total"),
                status=RentStatus.UNPAID.name,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )

        flash("Sewa baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_rent.read"))

    form = RentForm()

    charge_rule = get_charge_rule_selections()
    form.charge_rule.choices = charge_rule
    users = get_user_selections()
    form.user.choices = users

    return render_template("admin/rent/form.html", form=form, data=None)


@admin_rent_bp.route("/update", methods=["POST"])
def update():
    data = {
        "id": request.form.get("id"),
        "status": request.form.get("status"),
    }

    rent_controller.update(data)

    flash("Sewa berhasil diubah.", category="primary")
    return redirect(url_for("admin_rent.read"))


@admin_rent_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    rent_controller.delete(id_)

    flash("Sewa berhasil dihapus.", category="info")
    return redirect(url_for("admin_rent.read"))


@admin_rent_bp.route("/get-total", methods=["POST"])
def get_total():
    reservation_id = request.form.get("reservation_id")

    reservation = db.get_or_404(Reservation, reservation_id)

    date_range = (reservation.dropoff_datetime - reservation.pickup_datetime).days + 1

    total = (
        reservation.stock.price_per_day * date_range
    ) or reservation.stock.price_per_day

    rent = Rent.query.where(Rent.reservation_id == reservation_id).first()

    if rent and reservation.dropoff_datetime < datetime.now():
        amount = rent.charge_rule.amount

        if rent.charge_rule.type == ChargeType.NOMINAL:
            total = amount * (datetime.now() - reservation.dropoff_datetime).days
        elif rent.charge_rule.type == ChargeType.PERCENTAGE:
            total = (total * amount / 100) * (
                datetime.now() - reservation.dropoff_datetime
            ).days

    return jsonify(
        {
            "total": total,
            "type": PaymentType.CHARGE.name if rent else PaymentType.PAYMENT.name,
        }
    )


def get_user_selections():
    users = User.query.order_by(User.name.asc()).all()

    return [(u.id, u.name) for u in users]


def get_charge_rule_selections():
    rules = ChargeRule.query.all()

    return [(cr.id, cr.name) for cr in rules]
