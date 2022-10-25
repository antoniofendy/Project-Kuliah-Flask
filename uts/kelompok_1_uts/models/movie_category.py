from kelompok_1_uts import db


class MovieCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=False, unique=True)

    # movie = db.relationship("Movie", backref="movie_category", lazy=True)

    def __repr__(self) -> str:
        return f"<Category {self.category_name}>"
