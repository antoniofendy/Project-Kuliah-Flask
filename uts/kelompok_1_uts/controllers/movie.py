from flask import flash, redirect, url_for
from kelompok_1_uts import db
from kelompok_1_uts.models.movie import Movie
from kelompok_1_uts.models.movie_category import MovieCategory
from kelompok_1_uts.models.stock import Stock


def create(movie):
    db.session.add(movie)
    db.session.commit()


def update(movie):
    cur_movie = db.get_or_404(Movie, movie["id"])
    cur_movie.title = movie["title"]
    cur_movie.synopsis = movie["synopsis"]
    cur_movie.duration = movie["duration"]
    cur_movie.actor = movie["actor"]
    cur_movie.picture = movie["picture"]

    db.session.commit()


def delete(id):
    cur_movie = db.get_or_404(Movie, id)

    stock_of_movie = Stock.query.where(Stock.movie_id == id).all()
    if stock_of_movie:
        flash(
            f"Film {cur_movie.title} tidak dapat dihapus karena terkait dengan data Stok",
            category="danger",
        )
        return redirect(url_for("movie.index")) and False

    db.session.delete(cur_movie)
    db.session.commit()
    return True


def get(id):
    return db.get_or_404(Movie, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = db.session.query(Movie).join(MovieCategory).where(Movie.movie_category_id == MovieCategory.id).all()
    return response
