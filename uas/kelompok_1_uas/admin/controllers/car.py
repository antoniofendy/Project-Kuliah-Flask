from kelompok_1_uas import db
from kelompok_1_uas.admin.models.car import Car


def get_all():
    response = Car.query.order_by(Car.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Car, id)


def create(Car):
    db.session.add(Car)
    db.session.commit()


def update(car):
    cur_car = db.get_or_404(Car, car["id"])
    cur_car.name = car["name"]
    cur_car.address = car["address"]

    db.session.commit()


def delete(id):
    cur_car = db.get_or_404(Car, id)
    db.session.delete(cur_car)
    db.session.commit()
