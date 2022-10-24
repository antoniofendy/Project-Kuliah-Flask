from kelompok_1_uts import db
from kelompok_1_uts.models.charge_rule import ChargeRule

def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = ChargeRule.query.order_by(ChargeRule.id.asc()).all()
    return response


def get(id):
    return db.get_or_404(ChargeRule, id)


def create(ChargeRule):
    db.session.add(ChargeRule)
    db.session.commit()


def update(charge_rule):
    cur_charge_rule = db.get_or_404(ChargeRule, charge_rule["id"])
    cur_charge_rule.amount = charge_rule["name"]
    cur_charge_rule.amount = charge_rule["amount"]
    cur_charge_rule.type = charge_rule["type"]

    db.session.commit()


def delete(id):
    cur_charge_rule = db.get_or_404(ChargeRule, id)
    db.session.delete(cur_charge_rule)
    db.session.commit()