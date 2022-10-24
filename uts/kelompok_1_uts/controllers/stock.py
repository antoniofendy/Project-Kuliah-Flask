from kelompok_1_uts import db
from kelompok_1_uts.models.stock import Stock
from kelompok_1_uts.models.movie import Movie


def create(stock):
    db.session.add(stock)
    db.session.commit()


def update(stock):
    cur_stock = db.get_or_404(Stock, stock["id"])
    cur_stock.qty = stock["qty"]
    cur_stock.price = stock["price"]

    db.session.commit()


def delete(id):
    cur_stock = db.get_or_404(Stock, id)
    db.session.delete(cur_stock)
    db.session.commit()


def get(id):
    return db.get_or_404(Stock, id)


def get_all():
    # response = db.session.execute(db.select(Staff).order_by(Staff.name)).scalars().all()
    response = (
        Stock.query.order_by(Stock.id.asc())
        .join(Movie, Stock.movie_id == Movie.id)
        .add_columns(Stock.id, Stock.qty, Stock.price, Movie.title)
    )
    return response
