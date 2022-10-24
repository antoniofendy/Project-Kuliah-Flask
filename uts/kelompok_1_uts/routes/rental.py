from flask import Blueprint, flash, redirect, render_template, request, url_for

from kelompok_1_uts import db

from kelompok_1_uts.models.member import Member
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.models.stock import Stock
from kelompok_1_uts.models.charge_rule import ChargeRule
from kelompok_1_uts.models.staff import Staff

from kelompok_1_uts.controllers import transaction as transaction_controller
from kelompok_1_uts.models.transaction import Transaction
from kelompok_1_uts.forms.transaction import TransactionForm

from kelompok_1_uts.controllers import payment as payment_controller
from kelompok_1_uts.models.payment import Payment
from kelompok_1_uts.forms.payment import PaymentForm
from kelompok_1_uts.models.payment import PaymentStatus


bp = Blueprint("rental", __name__, template_folder="templates", static_folder="static")


@bp.route("/", defaults={"id": None})
@bp.route("/<int:id>")
def show_transaction(id):
    if id:
        form = TransactionForm()
        data = transaction_controller.get(id)

        members = db.session.query(Member).order_by(Member.name).all()
        stocks = (
            db.session.query(Stock).join(Movie).where(Stock.movie_id == Movie.id).all()
        )
        charges = db.session.query(ChargeRule).order_by(ChargeRule.id).all()
        staffs = db.session.query(Staff).order_by(Staff.name).all()

        if not members:
            flash("Tidak ada data Member.", category="info")
            return redirect(url_for("member.show", id=None))
        members_list = [(m.id, m.name) for m in members]

        if not stocks:
            flash("Tidak ada data Stok.", category="info")
            return redirect(url_for("stock.show"))
        stocks_list = [(s.id, s.movie.title) for s in stocks]

        if not charges:
            flash("Tidak ada data aturan denda.", category="info")
            return redirect(url_for("charge_rule.show"))
        charges_list = [(c.id, c.name) for c in charges]

        staffs_list = []
        if staffs:
            staffs_list = [(s.id, s.name) for s in staffs]

        form.member.choices = members_list
        form.movie.choices = stocks_list
        form.charge.choices = charges_list
        form.staff.choices = staffs_list

        form.member.default = data.member_id
        form.movie.default = data.stock_id
        form.charge.default = data.charge_id
        form.staff.default = data.staff_id

        form.process()

        return render_template("rental/form.html", form=form, data=data)

    data = transaction_controller.get_all()

    return render_template("rental/rental_list.html", data=data)


@bp.route("/new", methods=["GET", "POST"])
def new_transaction():
    form = TransactionForm()
    if request.method == "POST":
        transaction = Transaction(
            stock_id=request.form.get("movie"),
            member_id=request.form.get("member"),
            staff_id=request.form.get("staff"),
            charge_id=request.form.get("charge"),
            rental_start_date=request.form.get("rental_start"),
            rental_end_date=request.form.get("rental_end"),
        )

        message = transaction_controller.create(transaction)
        if message:
            flash(message, category="danger")
            return redirect(url_for("rental.new_transaction"))

        flash("Transaksi berhasil ditambahkan.", category="success")
        return redirect(url_for("rental.show_transaction", id=transaction.id))

    members = db.session.query(Member).order_by(Member.name).all()
    stocks = db.session.query(Stock).join(Movie).where(Stock.movie_id == Movie.id).all()
    charges = db.session.query(ChargeRule).order_by(ChargeRule.id).all()
    staffs = db.session.query(Staff).order_by(Staff.name).all()

    if not members:
        flash("Tidak ada data Member.", category="info")
        return redirect(url_for("member.show", id=None))
    members_list = [(m.id, m.name) for m in members]

    if not stocks:
        flash("Tidak ada data Stok.", category="info")
        return redirect(url_for("stock.show"))
    stocks_list = [(s.id, s.movie.title) for s in stocks]

    if not charges:
        flash("Tidak ada data Aturan Denda.", category="info")
        return redirect(url_for("charge_rule.show"))
    charges_list = [(c.id, c.name) for c in charges]

    staffs_list = []
    if staffs:
        staffs_list = [(s.id, s.name) for s in staffs]

    form.member.choices = members_list
    form.movie.choices = stocks_list
    form.charge.choices = charges_list
    form.staff.choices = staffs_list

    return render_template("rental/form.html", form=form, data=None)


@bp.route("/return", defaults={"id": None})
@bp.route("/return/<int:id>")
def return_transaction(id):
    if id:
        return_ = transaction_controller.return_(id)

        if return_:
            return redirect(url_for("rental.show_transaction"))
        else:
            return redirect(url_for("rental.show_payment", id=id, charge=1))

    data = transaction_controller.get_all_non_returned()

    return render_template("rental/return_list.html", data=data)


@bp.route("/delete/", methods=["POST"])
def delete_transaction():
    if transaction_controller.delete(request.form.get("id")):
        flash("Data transaksi berhasil dihapus.", category="danger")

    return redirect(url_for("rental.show_transaction", id=None))


@bp.route("/payment", defaults={"id": None, "charge": 0})
@bp.route("/payment/<int:id>/<int:charge>")
def show_payment(id, charge):
    if id:
        form = PaymentForm()

        data = payment_controller.get(id, charge)

        form.type.default = data.transaction_type.name
        print(data.transaction_type)
        form.process()

        print(data.transaction_type)
        form.process()

        return render_template("rental/payment.html", form=form, data=data)

    data = payment_controller.get_all()

    return render_template("rental/payment_list.html", data=data)


@bp.route("payment/pay", methods=["POST"])
def pay():
    print(request.form.get("transaction_id"))
    print(request.form.get("type"))
    print(request.form.get("amount"))
    payment = Payment(
        transaction_id=request.form.get("transaction_id"),
        transaction_type=request.form.get("type"),
        amount=request.form.get("amount"),
        status=PaymentStatus.PAID,
    )

    payment_controller.pay(payment)

    return redirect(url_for("rental.show_transaction"))


@bp.route("payment/delete/<int:id>", methods=["POST"])
def delete_payment(id):
    return ""
