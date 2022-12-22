from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify, session

from kelompok_1_uas import db
from kelompok_1_uas.admin.models.car import Car
from kelompok_1_uas.admin.models.garage import Garage

from kelompok_1_uas.admin.forms.stock import StockForm
from kelompok_1_uas.admin.controllers import stock as stock_controller
from kelompok_1_uas.admin.models.stock import Stock

admin_md_stock_bp = Blueprint(
    "admin_md_stock",
    __name__,
    url_prefix="/admin/master-data/stock",
    template_folder="../templates",
)


@admin_md_stock_bp.route("/", defaults={"id": None})
@admin_md_stock_bp.route("/<int:id>")
def read(id):
    if('user' in session):
        if id:
            form = StockForm()
            data = stock_controller.get(id)

            car = db.session.query(Car).all()

            if not car:
                flash("Tidak ada Mobil untuk dijadikan Stok.", category="info")
                return redirect(url_for("admin_md_stock.read"))

            car_list = [
                (
                    c.id,
                    "{cbrand} {cmodel} ({ctype})".format(
                        cbrand=c.brand, cmodel=c.model, ctype=c.type
                    ),
                )
                for c in car
            ]

            form.car_id.choices = car_list

            garage = db.session.query(Garage).all()

            if not garage:
                flash("Tidak ada garasi untuk dijadikan Stok.", category="info")
                return redirect(url_for("admin_md_stock.read"))

            garage_list = [(g.id, g.name) for g in garage]

            stock = db.session.query(Stock).filter_by(car_id=data.car_id).all()

            for s in stock:
                for g in garage_list:
                    if g[0] == s.garage_id and g[0] != data.garage_id:
                        garage_list.remove(g)

            form.garage_id.choices = garage_list

            form.car_id.default = data.car_id
            form.garage_id.default = data.garage_id

            form.process()

            return render_template(
                "admin/master-data/stock/form.html", form=form, data=data
            )

        return render_template(
            "admin/master-data/stock/list.html", data=stock_controller.get_all()
        )
    return render_template("admin/login.html")


@admin_md_stock_bp.route("/create", methods=["GET", "POST"])
def create():
    if('user' in session):
        form = StockForm()

        car = db.session.query(Car).all()

        if not car:
            flash("Tidak ada Mobil untuk dijadikan Stok.", category="info")
            return redirect(url_for("admin_md_stock.read"))

        car_list = [
            (
                c.id,
                "{cbrand} {cmodel} ({ctype})".format(
                    cbrand=c.brand, cmodel=c.model, ctype=c.type
                ),
            )
            for c in car
        ]

        form.car_id.choices = car_list

        garage = db.session.query(Garage).all()

        if not garage:
            flash("Tidak ada garasi untuk dijadikan Stok.", category="info")
            return redirect(url_for("admin_md_stock.read"))

        garage_list = [(g.id, g.name) for g in garage]

        form.garage_id.choices = garage_list

        if request.method == "POST":

            stock_controller.create(
                Stock(
                    car_id=request.form.get("car_id"),
                    garage_id=request.form.get("garage_id"),
                    price_per_day=request.form.get("price_per_day"),
                    quantity=request.form.get("quantity"),
                )
            )

            flash("Stok baru berhasil ditambahkan.", category="success")
            return redirect(url_for("admin_md_stock.read"))

        return render_template("admin/master-data/stock/form.html", form=form, data=None)
    return render_template("admin/login.html")


@admin_md_stock_bp.route("/update", methods=["POST"])
def update():
    if('user' in session):
        data = {
            "id": request.form.get("id"),
            "car_id": request.form.get("car_id"),
            "garage_id": request.form.get("garage_id"),
            "price_per_day": request.form.get("price_per_day"),
            "quantity": request.form.get("quantity"),
        }

        stock_controller.update(data)

        flash("Stok berhasil diubah.", category="primary")
        return redirect(url_for("admin_md_stock.read"))
    return render_template("admin/login.html")


@admin_md_stock_bp.route("/delete", methods=["POST"])
def delete():
    if('user' in session):
        id_ = request.form.get("id")

        stock_controller.delete(id_)

        flash("Stok berhasil dihapus.", category="info")
        return redirect(url_for("admin_md_stock.read"))
    return render_template("admin/login.html")


@admin_md_stock_bp.route("/form-api", methods=["POST"])
def form_api():
    if('user' in session):
        req_car_id = request.form["car_id"]

        garage = db.session.query(Garage).all()
        stock = db.session.query(Stock).filter_by(car_id=req_car_id).all()
        cols = ["id", "name", "address"]
        data = [{col: getattr(g, col) for col in cols} for g in garage]

        print(stock)
        for s in stock:
            for d in data:
                if d["id"] == s.garage_id:
                    data.remove(d)

        return jsonify(garage_list=data)
    return render_template("admin/login.html")


@admin_md_stock_bp.route("/get-available-garage", methods=["POST"])
def get_available_garage():
    if('user' in session):
        car_id = request.form.get("car_id")

        available_garage = db.session.query(Stock).filter_by(car_id=car_id).all()
        return jsonify(
            [{"id": s.garage.id, "name": s.garage.name} for s in available_garage]
        )
    return render_template("admin/login.html")
