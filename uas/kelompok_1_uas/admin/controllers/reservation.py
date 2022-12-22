from kelompok_1_uas import db
from kelompok_1_uas.admin.models.reservation import Reservation

from datetime import datetime


def get_all():
    response = Reservation.query.order_by(Reservation.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Reservation, id)


def create(Reservation):
    db.session.add(Reservation)
    db.session.commit()


def update(reservation):
    cur_reservation = db.get_or_404(Reservation, reservation["id"])
    cur_reservation.dropoff_garage_id = reservation["dropoff_location"]
    cur_reservation.dropoff_datetime = reservation["dropoff_datetime"]
    cur_reservation.note = reservation["note"]
    cur_reservation.status = reservation["status"]
    cur_reservation.updated_at = datetime.now()

    db.session.commit()


def delete(id):
    cur_reservation = db.get_or_404(Reservation, id)
    db.session.delete(cur_reservation)
    db.session.commit()
    pass
