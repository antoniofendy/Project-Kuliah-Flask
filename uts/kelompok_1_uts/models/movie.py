from kelompok_1_uts import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    synopsis = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(32), nullable=False)
    actor = db.Column(db.String(64), nullable=False)
    picture = db.Column(db.String(64), nullable=False)

    stocks = db.relationship("Stock", backref="movie", lazy=True)

    def __repr__(self) -> str:
        return f"<Movie {self.title}>"
