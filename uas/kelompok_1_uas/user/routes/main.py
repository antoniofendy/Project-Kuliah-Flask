from kelompok_1_uas.admin.controllers import stock as stock_controller
from kelompok_1_uas.admin.controllers import car as car_controller
from kelompok_1_uas.admin.models.stock import Stock
from kelompok_1_uas import db

from flask import Blueprint, render_template, request, flash, url_for, redirect

user_main_bp = Blueprint(
    "user_main",
    __name__,
    url_prefix="/",
    template_folder="../templates",
)

@user_main_bp.route("/")
def index():
    # stock = stock_controller.get_all_available()
    stock_start_price = db.session.query(Stock).order_by(Stock.price_per_day.asc()).first()

    # tampilkan data mobil dengan stok/quantity > 0

    # for s in stock:
    #     duplicate = False
    #     if len(car_list) != 0:
    #         for c in car_list:
    #             if s.car_id == c.id :
    #                 duplicate = True
    #                 break
    #     if not duplicate:
    #         car_list.append(car_controller.get(s.car_id))

    # print(stock)
    return render_template("site/index.html", data=car_controller.get_all(), start_price = stock_start_price.price_per_day)