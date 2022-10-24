from kelompok_1_uts import db
from kelompok_1_uts.models.movie_category import Category

def create(category):
    db.session.add(category)
    db.session.commit()


def update(category):
    cur_category = db.get_or_404(Category, category["id"])
    cur_category.category = category["category name"]

    db.session.commit()


def delete(category):
    print(category)
    cur_movie = db.get_or_404(Category, category["id"])
    db.session.delete(cur_category)
    db.session.commit()


def get(id):
    return db.get_or_404(Category, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = Category.query.order_by(Category.id.asc()).all()
    return response