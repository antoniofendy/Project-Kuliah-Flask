from kelompok_1_uas import db
from kelompok_1_uas.admin.models.stock import Stock


def get_all():
    response = Stock.query.order_by(Stock.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Stock, id)


def create(Stock):
    db.session.add(Stock)
    db.session.commit()


def update(stock):
    cur_stock = db.get_or_404(Stock, stock["id"])
    cur_stock.car_id = stock["car_id"]
    cur_stock.garage_id = stock["garage_id"]
    cur_stock.price_per_day = stock["price_per_day"]
    cur_stock.quantity = stock["quantity"]

    db.session.commit()


def delete(id):
    cur_stock = db.get_or_404(Stock, id)
    db.session.delete(cur_stock)
    db.session.commit()
