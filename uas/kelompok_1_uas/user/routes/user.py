import os

from werkzeug.utils import secure_filename

from kelompok_1_uas.user.models.user import User
from kelompok_1_uas.user.forms.user import UserForm
from kelompok_1_uas.user.controllers import user as user_controller

from kelompok_1_uas.admin.models.stock import Stock
from kelompok_1_uas.admin.controllers import car as car_controller
from kelompok_1_uas.admin.controllers import reservation as reservation_controller
from kelompok_1_uas.admin.controllers import rent as rent_controller
from kelompok_1_uas.admin.models.reservation import Reservation, ReservationStatus
from kelompok_1_uas.admin.models.rent import Rent

from kelompok_1_uas import db

from sqlalchemy import exc, or_

from flask_login import login_user, login_required, logout_user, current_user

import hashlib

from datetime import datetime

from flask import Blueprint, render_template, request, flash, url_for, redirect

user_user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user",
    template_folder="../templates",
)

UPLOAD_FOLDER = "kelompok_1_uas/static/upload/receipt"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@user_user_bp.route("/", defaults={"id": None})
@user_user_bp.route("/<int:id>")
def read(id):
    if id:
        form = UserForm()
        data = user_controller.get(id)
        
        return render_template("user/user/form.html", form=form, data=data)
    
    return render_template("user/user/list.html", data=user_controller.get_all())


@user_user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        md5_password = hashlib.md5(request.form.get("password").encode())
        md5_password_confirm = hashlib.md5(request.form.get("password_confirm").encode())

        if md5_password.hexdigest() == md5_password_confirm.hexdigest():
            try:
                user_controller.create(
                    User(
                        name=request.form.get("name"),
                        phone=request.form.get("phone"),
                        address=request.form.get("address"),
                        date_of_birth=request.form.get("date_of_birth"),
                        sex=request.form.get("sex"),
                        occupation=request.form.get("occupation"),
                        email=request.form.get("email"),
                        password=md5_password.hexdigest(),
                    )
                )
                flash("Berhasil registrasi, silahkan login.", category="success")
                return redirect(url_for("user.login"))

            except exc.SQLAlchemyError:
                flash("Terjadi kesalahan sistem.", category="danger")
                return redirect(url_for("user.register"))

        flash("Password dan password konfirmasi tidak sama.", category="danger")
        return redirect(url_for("user.register"))

    return render_template("site/registerUser.html")


@user_user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        md5_password = hashlib.md5(password.encode())

        user = db.session.query(User).filter_by(email=email, password=md5_password.hexdigest()).first()

        # cek kredensial user
        if not user:
            flash('Email atau password tidak sesuai.', category="warning")
            return redirect(url_for('user.login'))

        # jika user terdaftar
        login_user(user, remember=True)
        # print(current_user.name)
        return redirect(url_for("user_main.index"))

    if not current_user.is_authenticated:
        return render_template("site/loginUser.html")

    return redirect(url_for("user_main.index"))


@user_user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user_main.index"))


@user_user_bp.route("/reservation/<int:id>", methods=["GET", "POST"])
@login_required
def reservation(id):
    if request.method == "POST":
        selected_car = request.form.get("car_id")
        selected_pickup_garage = request.form.get("pickup_garage_id")
        print('garage_id:')
        print(request.form.get("pickup_garage_id"))

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
                user_id=current_user.id,
                stock_id=stock.id,
                pickup_garage_id=int(request.form.get("pickup_garage_id")),
                dropoff_garage_id=int(request.form.get("dropoff_garage_id")),
                pickup_datetime=pickup_datetime,
                dropoff_datetime=dropoff_date,
                note=request.form.get("note"),
                status=ReservationStatus.OPEN,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )

        flash("Reservasi baru berhasil ditambahkan.", category="success")
        return redirect(url_for("user.transaction"))
    car = car_controller.get(id)
    stock = Stock.query.where(Stock.car_id == id).where(Stock.quantity >= 0).all()

    print(stock)

    return render_template("site/reservation.html", car=car, stock=stock)

@user_user_bp.route("/transaction", methods=["GET"])
@login_required
def transaction():

    reservation = (Reservation.query
        .where(Reservation.user_id == current_user.id)
        .where(
            or_(Reservation.status == 'OPEN', Reservation.status == 'Fail'))
        .all()
    )

    rent = (Rent.query
        .where(Rent.user_id == current_user.id)
        .where(
            or_(Rent.status == 'UNPAID', Rent.status == 'PENDING'))
        .all()
    )


    return render_template("site/transaction.html", reservation = reservation, rent = rent)

@user_user_bp.route("/pay-rent/<int:id>", methods=["GET", "POST"])
@login_required
def pay_rent(id):
    if request.method == "POST":

        rent = Rent.query.where(Rent.id == id).first()

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
                        fuser=rent.user_id,
                        fres=rent.reservation_id,
                        fext=file_ext,
                    ),
                )
            )

            data = {
                "id": request.form.get("id"),
                "transfer_file": "{fdate}-{fuser}-{fres}{fext}".format(
                        fdate=datetime.now().date(),
                        fuser=rent.user_id,
                        fres=rent.reservation_id,
                        fext=file_ext,
                    ),
                "status": "PENDING",
            }

            rent_controller.user_pay_rent(data)
            flash("Pembayaran berhasil dilakukan dan akan segera diproses admin.", category="success")
            return redirect(url_for("user.transaction"))

        flash("Format foto hanya bisa berupa PNG, JPG, dan JPEG.", category="error")
        return redirect(url_for("user.pay_rent", id=id))

    rent = Rent.query.where(Rent.id == id).first()

    return render_template("site/payRent.html", rent=rent)
    