from app import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
