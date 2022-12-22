from flask import Blueprint, render_template, request, flash, url_for, redirect

from kelompok_1_uas import db

from kelompok_1_uas.admin.forms.rent import RentForm
from kelompok_1_uas.admin.controllers import rent as rent_controller
from kelompok_1_uas.admin.models.rent import Rent, RentStatus

from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.admin.models.car import Car
from kelompok_1_uas.admin.models.stock import Stock
from kelompok_1_uas.admin.models.garage import Garage

from datetime import datetime

admin_rent_bp = Blueprint(
    "admin_rent",
    __name__,
    url_prefix="/admin/rent",
    template_folder="../templates",
)


@admin_rent_bp.route("/", defaults={"id": None})
@admin_rent_bp.route("/<int:id>")
def read(id):
    if id:
        form = RentForm()

        return render_template("admin/rent/form.html", form=form, data=data)

    return render_template("admin/rent/list.html", data=rent_controller.get_all())


@admin_rent_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # selected_car = request.form.get("car")
        # selected_pickup_garage = request.form.get("pickup_location")

        # stock = (
        #     db.session.query(Stock)
        #     .where(Stock.car_id == selected_car)
        #     .where(Stock.garage_id == selected_pickup_garage)
        #     .first()
        # )

        # pickup_date = request.form.get("pickup_date")
        # pickup_time = request.form.get("pickup_time")
        # pickup_datetime = datetime.strptime(
        #     f"{pickup_date} {pickup_time}", "%Y-%m-%d %H:%M"
        # )

        # dropoff_date = request.form.get("dropoff_date")
        # dropoff_date = datetime.strptime(dropoff_date, "%Y-%m-%d")

        rent_controller.create(
            Rent(
                # user_id=request.form.get("user"),
                # stock_id=stock.id,
                # pickup_garage_id=int(request.form.get("pickup_location")),
                # dropoff_garage_id=int(request.form.get("dropoff_location")),
                # pickup_datetime=pickup_datetime,
                # dropoff_datetime=dropoff_date,
                # note=request.form.get("note"),
                # status=RentStatus.OPEN,
                # created_at=datetime.now(),
                # updated_at=datetime.now(),
            )
        )

        flash("Sewa baru berhasil ditambahkan.", category="success")
        return redirect(url_for("admin_rent.read"))

    form = RentForm()

    users = get_user_selections()
    form.user.choices = users
    cars = get_car_selections()
    form.car.choices = cars

    return render_template("admin/rent/form.html", form=form, data=None)


@admin_rent_bp.route("/update", methods=["POST"])
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

    rent_controller.update(data)

    flash("Sewa berhasil diubah.", category="primary")
    return redirect(url_for("admin_rent.read"))


@admin_rent_bp.route("/delete", methods=["POST"])
def delete():
    id_ = request.form.get("id")

    rent_controller.delete(id_)

    flash("Sewa berhasil dihapus.", category="info")
    return redirect(url_for("admin_rent.read"))


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
