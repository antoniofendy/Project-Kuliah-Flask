from kelompok_1_uas import db

import enum


class ChargeType(enum.Enum):
    PERCENTAGE = "Persentase"
    NOMINAL = "Nominal"


class ChargeRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum(ChargeType), nullable=False)

    # transaction = db.relationship("Transaction", backref="charge_rule", lazy=True)
