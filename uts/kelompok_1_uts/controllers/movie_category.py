from kelompok_1_uts import db
from kelompok_1_uts.models.movie_category import MovieCategory


def create(category):
    db.session.add(category)
    db.session.commit()


def update(category):
    cur_category = db.get_or_404(MovieCategory, category["id"])
    cur_category.category = category["category_name"]

    db.session.commit()


def delete(category):
    print(category)
    cur_category = db.get_or_404(MovieCategory, id)
    db.session.delete(cur_category)
    db.session.commit()


def get(id):
    return db.get_or_404(MovieCategory, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = MovieCategory.query.order_by(MovieCategory.id.asc()).all()
    return response
