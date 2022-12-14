from kelompok_1_uas import db
from kelompok_1_uas.admin.models.garage import Garage


def get_all():
    response = Garage.query.order_by(Garage.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Garage, id)


def create(Garage):
    db.session.add(Garage)
    db.session.commit()


def update(garage):
    cur_garage = db.get_or_404(Garage, garage["id"])
    cur_garage.name = garage["name"]
    cur_garage.address = garage["address"]

    db.session.commit()


def delete(id):
    cur_garage = db.get_or_404(Garage, id)
    db.session.delete(cur_garage)
    db.session.commit()
