from kelompok_1_uts import db


class MovieCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Category {self.category}>"
