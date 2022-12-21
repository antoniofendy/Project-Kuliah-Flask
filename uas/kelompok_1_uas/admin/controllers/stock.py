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


def update(car):
    cur_car = db.get_or_404(Stock, car["id"])
    cur_car.name = car["name"]
    cur_car.address = car["address"]

    db.session.commit()


def delete(id):
    cur_car = db.get_or_404(Stock, id)
    db.session.delete(cur_car)
    db.session.commit()
