from flask import flash, redirect, url_for
from kelompok_1_uts import db
from kelompok_1_uts.models.stock import Stock
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.models.transaction import Transaction


def create(stock):
    db.session.add(stock)
    db.session.commit()


def update(stock):
    cur_stock = db.get_or_404(Stock, stock["id"])
    cur_stock.qty = stock["qty"]
    cur_stock.price = stock["price"]

    db.session.commit()


def delete(id):
    cur_stock = db.get_or_404(Stock, id)

    transaction_of_stock = Transaction.query.where(Transaction.stock_id == id).all()
    if transaction_of_stock:
        flash(
            f"Stok {cur_stock.movie.title} tidak dapat dihapus karena terkait dengan data Transaksi.",
            category="danger",
        )
        return redirect(url_for("stock.show")) and False

    db.session.delete(cur_stock)
    db.session.commit()
    return True


def get(id):
    return db.get_or_404(Stock, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Stock.query.order_by(Stock.id.asc()).all()
    return response
