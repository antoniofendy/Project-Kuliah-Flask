from flask import Blueprint, render_template, request, flash, url_for, redirect

from kelompok_1_uas import db

from kelompok_1_uas.admin.forms.reservation import ReservationForm
from kelompok_1_uas.admin.controllers import reservation as reservation_controller
from kelompok_1_uas.admin.models.reservation import Reservation, ReservationStatus

from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.admin.models.car import Car
from kelompok_1_uas.admin.models.stock import Stock
from kelompok_1_uas.admin.models.garage import Garage

from datetime import datetime

admin_reservation_bp = Blueprint(
    "admin_reservation",
    __name__,
    url_prefix="/admin/reservation",
    template_folder="../templates",
)


@admin_reservation_bp.route("/", defaults={"id": None})
@admin_reservation_bp.route("/<int:id>")
def read(id):
    if id:
        form = ReservationForm()
        data = reservation_controller.get(id)

        users = get_user_selections()
        form.user.choices = users
        form.user.default = data.user_id
        cars = get_car_selections()
        form.car.choices = cars
        form.car.default = data.stock.car.id
        garages = Garage.query.all()
        form.pickup_location.choices = [(g.id, g.name) for g in garages]
        form.dropoff_location.choices = [(g.id, g.name) for g in garages]
        form.pickup_location.default = data.pickup_garage_id
        form.dropoff_location.default = data.dropoff_garage_id

        form.pickup_date.default = data.pickup_datetime
        form.pickup_time.default = data.pickup_datetime
        form.dropoff_date.default = data.dropoff_datetime

        form.status.default = data.status.name

        form.process()

        return render_template("admin/reservation/form.html", form=form, data=data)

    return render_template(
        "admin/reservation/list.html", data=reservation_controller.get_all()
    )


@admin_reservation_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        selected_car = request.form.get("car")
        selected_pickup_garage = request.form.get("pickup_location")

        stock = (
            db.session.query(Stock)
            .where(Stock.car_id == selected_car)
            .where(Stock.garage_id == selected_pickup_garage)
            .first()
        )

        pickup_date = request.form.get("pickup_date")
        pickup_time = request.form.get("pickup_time")
        pickup_datetime = datetime.strptime(
            f"{pickup_date} {pickup_time}", "%Y-%m-%d %H:%M"
        )

        dropoff_date = request.form.get("dropoff_date")
        dropoff_date = datetime.strptime(dropoff_date, "%Y-%m-%d")

        reservation_controller.create(
            Reservation(
                user_id=request.form.get("user"),
                stock_id=stock.id,
                pickup_garage_id=int(request.form.get("pickup_location")),
                dropoff_garage_id=int(request.form.get("dropoff_location")),
                pickup_datetime=pickup_datetime,
                dropoff_datetime=dropoff_date,
                note=request.form.get("note"),
                status=ReservationStatus.OPEN,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )

        flash("Reservasi baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_reservation.read"))

    form = ReservationForm()

    users = get_user_selections()
    form.user.choices = users
    cars = get_car_selections()
    form.car.choices = cars

    return render_template("admin/reservation/form.html", form=form, data=None)


@admin_reservation_bp.route("/update", methods=["POST"])
def update():
    dropoff_date = request.form.get("dropoff_date")
    dropoff_date = datetime.strptime(dropoff_date, "%Y-%m-%d")

    data = {
        "id": request.form.get("id"),
        "dropoff_location": request.form.get("dropoff_location"),
        "dropoff_datetime": dropoff_date,
        "note": request.form.get("note"),
        "status": request.form.get("status"),
    }

    reservation_controller.update(data)

    flash("Reservasi berhasil diubah.", category="primary")
    return redirect(url_for("admin_reservation.read"))


@admin_reservation_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    reservation_controller.delete(id_)

    flash("Reservasi berhasil dihapus.", category="info")
    return redirect(url_for("admin_reservation.read"))


def get_user_selections():
    users = User.query.order_by(User.name.asc()).all()

    return [(u.id, u.name) for u in users]


def get_car_selections():
    cars = (
        Car.query.join(Stock)
        .where(Car.id == Stock.car_id)
        .where(Stock.quantity > 0)
        .order_by(Car.brand)
        .all()
    )

    return [(c.id, f"{c.brand} {c.model} ({c.type})") for c in cars]
