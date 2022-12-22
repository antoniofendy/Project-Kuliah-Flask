import os, json
from flask_login import login_required

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
    jsonify,
)
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
from kelompok_1_uas.admin.controllers import reservation as reservation_controller

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
@login_required
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
@login_required
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

    prefil = {}
    # If url has ID, validate rents
    if id_ := request.args.get("id"):
        reservation = db.get_or_404(Reservation, id_)
        if reservation and reservation.status in [
            ReservationStatus.OPEN,
            ReservationStatus.RENTED,
        ]:
            # Validate reservation payments
            payment_paid = validate_payments(id_)

            if not isinstance(payment_paid, bool):
                return redirect(url_for("admin_rent.read", id=payment_paid))

            # Fill standard values
            form.user.default = reservation.user_id
            form.reservation.choices = [
                (
                    reservation.id,
                    f"Reservasi {reservation.id}: {reservation.stock.car.brand} {reservation.stock.car.model}",
                )
            ]
            form.reservation.default = reservation.id

            # Standard rent cost
            standard_amount = reservation.stock.price_per_day

            # Calculate reservation length
            date_range = (
                reservation.dropoff_datetime - reservation.pickup_datetime
            ).days + 1

            # Create new payment if none is paid
            if not payment_paid:
                prefil["total"] = (date_range * standard_amount) or standard_amount
                form.type.default = PaymentType.PAYMENT.name
            else:
                # Validate reservation charges
                charge_paid = validate_charges(id_)

                last_payment = (
                    Rent.query.where(Rent.reservation_id == id_)
                    .where(Rent.type == PaymentType.PAYMENT)
                    .order_by(Rent.id.desc())
                    .first()
                )

                if not isinstance(charge_paid, bool):
                    return redirect(url_for("admin_rent.read", id=charge_paid))

                # Create new charge if none is paid, last payment has a charge rule, and dropoff date exceeded
                if (
                    last_payment.charge_rule
                    and reservation.dropoff_datetime < datetime.now()
                    and not charge_paid
                ):
                    total = (standard_amount * date_range) or standard_amount
                    late_days = (datetime.now() - reservation.dropoff_datetime).days

                    if last_payment.charge_rule.type == ChargeType.NOMINAL:
                        prefil["total"] = (
                            late_days * last_payment.charge_rule.amount
                        ) or last_payment.charge_rule.amount
                    elif last_payment.charge_rule.type == ChargeType.PERCENTAGE:
                        standard_charge = total * last_payment.charge_rule.amount
                        prefil["total"] = (
                            standard_charge * late_days
                        ) or standard_charge

                    form.type.default = PaymentType.CHARGE.name

                else:
                    reservation_controller.return_reservation(id_)
                    return redirect(url_for("admin_reservation.read", id=id_))

            form.process()

    return render_template("admin/rent/form.html", form=form, data=None, prefil=prefil)


@admin_rent_bp.route("/update", methods=["POST"])
@login_required
def update():
    data = {
        "id": request.form.get("id"),
        "status": request.form.get("status"),
    }

    rent_controller.update(data)

    flash("Sewa berhasil diubah.", category="primary")
    return redirect(url_for("admin_rent.read"))


@admin_rent_bp.route("/delete", methods=["POST"])
@login_required
def delete():
    id_ = request.form.get("id")

    rent_controller.delete(id_)

    flash("Sewa berhasil dihapus.", category="info")
    return redirect(url_for("admin_rent.read"))


@admin_rent_bp.route("/get-total", methods=["POST"])
@login_required
def get_total():
    reservation_id = request.form.get("reservation_id")

    reservation = db.get_or_404(Reservation, reservation_id)

    date_range = (reservation.dropoff_datetime - reservation.pickup_datetime).days + 1

    total = (
        reservation.stock.price_per_day * date_range
    ) or reservation.stock.price_per_day

    rent = (
        Rent.query.where(Rent.reservation_id == reservation_id)
        .where(Rent.type == PaymentType.PAYMENT.name)
        .first()
    )

    if charged := rent and reservation.dropoff_datetime < datetime.now():
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
            "type": PaymentType.CHARGE.name if charged else PaymentType.PAYMENT.name,
        }
    )


@admin_rent_bp.route("/make-rent/<int:id>")
@login_required
def make_rent(id):

    return redirect(url_for("admin_rent.create", id=id))


def get_user_selections():
    users = User.query.order_by(User.name.asc()).all()

    return [(u.id, u.name) for u in users]


def get_charge_rule_selections():
    rules = ChargeRule.query.all()

    return [(cr.id, cr.name) for cr in rules]


def validate_payments(reservation_id):
    reservation = db.get_or_404(Reservation, reservation_id)

    payment_rents = (
        Rent.query.where(Rent.reservation_id == reservation_id)
        .where(Rent.type == PaymentType.PAYMENT)
        .all()
    )

    for pr in payment_rents:
        print(pr.status)
        if pr.status != RentStatus.PAID:
            return pr.id
    return bool(payment_rents)


def validate_charges(reservation_id):
    reservation = db.get_or_404(Reservation, reservation_id)

    charge_rents = (
        (
            Rent.query.where(Rent.reservation_id == reservation_id).where(
                Rent.type == PaymentType.CHARGE
            )
        )
        .order_by(Rent.updated_at.desc())
        .all()
    )

    for cr in charge_rents:
        if cr.status != RentStatus.PAID:
            return cr.id
            return redirect(url_for("admin_rent.read", id=cr.id))

    return bool(charge_rents)
