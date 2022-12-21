from kelompok_1_uas import db
from kelompok_1_uas.admin.models.reservation import Reservation


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Reservation.query.order_by(Reservation.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(Reservation, id)
    pass


def create(Reservation):
    db.session.add(Reservation)
    db.session.commit()
    pass


def update(reservation):
    # cur_charge_rule = db.get_or_404(ChargeRule, charge_rule["id"])
    # cur_charge_rule.amount = charge_rule["name"]
    # cur_charge_rule.amount = charge_rule["amount"]
    # cur_charge_rule.type = charge_rule["type"]

    # db.session.commit()
    pass


def delete(id):
    # cur_charge_rule = db.get_or_404(ChargeRule, id)
    # db.session.delete(cur_charge_rule)
    # db.session.commit()
    pass
