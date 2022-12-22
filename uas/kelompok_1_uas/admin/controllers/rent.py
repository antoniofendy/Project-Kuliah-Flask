from kelompok_1_uas import db
from kelompok_1_uas.admin.models.rent import Rent

from datetime import datetime


def get_all():
    response = Rent.query.order_by(Rent.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Rent, id)


def create(Rent):
    db.session.add(Rent)
    db.session.commit()


def update(rent):
    cur_rent = db.get_or_404(Rent, rent["id"])
    cur_rent.dropoff_garage_id = rent["dropoff_location"]
    cur_rent.dropoff_datetime = rent["dropoff_datetime"]
    cur_rent.note = rent["note"]
    cur_rent.status = rent["status"]
    cur_rent.updated_at = datetime.now()

    db.session.commit()


def delete(id):
    cur_rent = db.get_or_404(Rent, id)
    db.session.delete(cur_rent)
    db.session.commit()
    pass
