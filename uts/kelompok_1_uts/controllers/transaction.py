from datetime import datetime
from flask import flash, redirect, url_for
from kelompok_1_uts import db
from kelompok_1_uts.models.transaction import Transaction
from kelompok_1_uts.models.stock import Stock
from kelompok_1_uts.models.charge_rule import ChargeRule
from kelompok_1_uts.models.member import Member
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.models.payment import Payment
from kelompok_1_uts.models.transaction import TransactionStatus


def create(transaction):
    if transaction.rental_end_date <= transaction.rental_start_date:
        return "Tanggal Sewa tidak bisa lebih awal dari atau sama dengan Tanggal Akhir Sewa."

    db.session.add(transaction)

    stock = db.session.get(Stock, transaction.stock_id)
    if stock.qty < 1:
        return f"Stok {stock.movie.title} tidak cukup."

    stock.qty = stock.qty - 1

    db.session.commit()
    db.session.refresh(transaction)

    return False


def update(stock):
    cur_stock = db.get_or_404(Transaction, stock["id"])
    cur_stock.qty = stock["qty"]
    cur_stock.price = stock["price"]

    db.session.commit()


def delete(id):
    cur_transaction = db.get_or_404(Transaction, id)
    transaction_payment = Payment.query.where(Payment.transaction_id == id).all()
    if transaction_payment:
        flash(
            f"Transaksi {cur_transaction.id} tidak dapat dihapus karena terkait dengan data Pembayaran",
            category="danger",
        )
        return redirect(url_for("rental.show_transaction")) and False

    db.session.delete(cur_transaction)
    db.session.commit()
    return True
    # db.session.delete(cur_stock)
    # db.session.commit()

    # cur_movie = db.get_or_404(Movie, id)


def get(id):
    return db.get_or_404(Transaction, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Transaction.query.order_by(Transaction.id).all()
    return response


def get_all_non_returned():
    response = (
        Transaction.query.order_by(Transaction.id)
        .where(Transaction.status == TransactionStatus.RENT)
        .all()
    )
    return response


def return_(id):
    transaction = Transaction.query.where(
        Transaction.id == id and Transaction.status == TransactionStatus.RENT
    ).all()

    transaction = transaction[0]

    if (
        transaction.rental_end_date < datetime.now().date()
        and transaction.charge_rule.amount > 0
    ):
        return False

    transaction.status = TransactionStatus.RETURNED
    transaction.stock.qty = transaction.stock.qty + 1
    db.session.commit()
    return True
