from kelompok_1_uas import db
from kelompok_1_uas.admin.models.rent import Rent, RentStatus
from kelompok_1_uas.admin.models.reservation import ReservationStatus
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
    cur_rent.status = rent["status"]
    cur_rent.updated_at = datetime.now()

    if cur_rent.status == RentStatus.PAID.name:
        cur_rent.reservation.status = ReservationStatus.RENTED.name
        cur_rent.reservation.stock.quantity -= 1

    db.session.commit()


def user_pay_rent(rent):
    cur_rent = db.get_or_404(Rent, rent["id"])
    cur_rent.transfer_file = rent["transfer_file"]
    cur_rent.status = rent["status"]
    cur_rent.updated_at = datetime.now()

    db.session.commit()


def delete(id):
    cur_rent = db.get_or_404(Rent, id)
    db.session.delete(cur_rent)
    db.session.commit()
    pass
