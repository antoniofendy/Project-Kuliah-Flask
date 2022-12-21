from kelompok_1_uas import db

class Garage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)

    # stock = db.relationship("Stock", backref="garage", lazy=True)
