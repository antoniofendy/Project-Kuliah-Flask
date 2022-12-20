from flask import Flask, render_template, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from kelompok_1_uas.admin import routes as admin_routes
    from kelompok_1_uas.site import routes as site_routes

    app.register_blueprint(admin_routes.main.admin_main_bp)
    app.register_blueprint(site_routes.main.site_main_bp)

    # from kelompok_1_uas.admin.routes.main import bp as admin_main_bp
    # from kelompok_1_uas.admin.routes.charge_rule import bp as admin_charge_rule
    # from kelompok_1_uas.admin.errors import bp as admin_error_bp

    # from kelompok_1_uas.site.routes.main import bp as user_main_bp

    # app.register_blueprint(admin_main_bp)
    # app.register_blueprint(admin_charge_rule)
    # app.register_blueprint(admin_error_bp)

    # app.register_blueprint(user_main_bp)

    return app
