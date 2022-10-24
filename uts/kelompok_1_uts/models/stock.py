from kelompok_1_uts import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer)
    price = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Stock {self.id}:Movie {self.movie_id}>"
