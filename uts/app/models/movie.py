from app import db


class Movie(db.Model):
    judul = db.Column(db.String(64), primary_key=True)

    def __repr__(self) -> str:
        return f"<Movie {self.judul}>"
