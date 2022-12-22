from flask import Flask, render_template, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Login manager
    login_manager = LoginManager()
    login_manager.login_message = "Anda harus login untuk bisa menggunakan layanan kami!"
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    from kelompok_1_uas.user.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # Admin side blueprints
    from kelompok_1_uas.admin import routes as admin_routes
    from kelompok_1_uas.user import routes as user_routes

    # Site side blueprints
    from kelompok_1_uas.site import routes as site_routes

    # Admin side blueprint registers
    app.register_blueprint(admin_routes.main.admin_main_bp)
    app.register_blueprint(admin_routes.admin.admin_admin_bp)
    app.register_blueprint(admin_routes.charge_rule.admin_charge_rule_bp)
    app.register_blueprint(admin_routes.md_garage.admin_md_garage_bp)
    app.register_blueprint(admin_routes.md_car.admin_md_car_bp)
    app.register_blueprint(admin_routes.md_stock.admin_md_stock_bp)
    app.register_blueprint(admin_routes.reservation.admin_reservation_bp)
    app.register_blueprint(admin_routes.rent.admin_rent_bp)
    app.register_blueprint(admin_routes.reporting.admin_reporting_bp)

    # User side blueprint registers
    app.register_blueprint(user_routes.user.user_user_bp)
    app.register_blueprint(user_routes.main.user_main_bp)

    # Site side blueprint registers
    app.register_blueprint(site_routes.main.site_main_bp)

    @app.template_filter()
    def currency_format(value):
        value = value or 0
        value = float(value)
        return f"Rp {value:,.0f}"

    return app
