from kelompok_1_uts import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(13), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    transaction = db.relationship("Transaction", backref="member", lazy=True)
