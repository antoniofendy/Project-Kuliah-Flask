from kelompok_1_uts import db

import enum

class ChargeType(enum.Enum):
    PERCENTAGE = "Percentage"
    NOMINAL = "Nominal"

class ChargeRule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum(ChargeType), nullable=False)