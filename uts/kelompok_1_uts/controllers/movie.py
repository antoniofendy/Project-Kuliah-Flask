from kelompok_1_uts import db
from kelompok_1_uts.models.movie import Movie

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


def delete(movie):
    print(movie)
    cur_movie = db.get_or_404(Movie, id)
    db.session.delete(cur_movie)
    db.session.commit()


def get(id):
    return db.get_or_404(Movie, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Movie.query.order_by(Movie.id.asc()).all()
    return response
