from app import db


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(32))
    phone = db.Column(db.String(13))
    address = db.Column(db.String(255))
    picture = db.Column(db.String(64))

    def __repr__(self) -> str:
        return f"<Staff {self.id}:{self.email}>"
