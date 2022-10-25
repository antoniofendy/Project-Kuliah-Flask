from kelompok_1_uts import db
from kelompok_1_uts.models.movie_category import MovieCategory
from kelompok_1_uts.models.movie import Movie
from flask import flash, redirect, url_for


def create(category):
    db.session.add(category)
    db.session.commit()


def update(category):
    cur_category = db.get_or_404(MovieCategory, category["id"])
    
    cur_category.category_name = category["category_name"]

    db.session.commit()


def delete(id):
    cur_category = db.get_or_404(MovieCategory, id)
    
    category_movie = Movie.query.where(Movie.movie_category_id == id).all()
    if category_movie:
        flash(
            f"Kategori {cur_category.category_name} tidak dapat dihapus karena terkait dengan data Film ",
            category="danger",
        )
        return redirect(url_for("movie_category.index")) and False
    
    flash("Data kategori berhasil dihapus.", category="info")
    db.session.delete(cur_category)
    db.session.commit()


def get(id):
    return db.get_or_404(MovieCategory, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = MovieCategory.query.order_by(MovieCategory.id.asc()).all()
    return response
