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

    # Admin side blueprints
    from kelompok_1_uas.admin import routes as admin_routes

    # Site side blueprints
    from kelompok_1_uas.site import routes as site_routes

    # Admin side blueprint registers
    app.register_blueprint(admin_routes.main.admin_main_bp)
    app.register_blueprint(admin_routes.admin.admin_admin_bp)
    app.register_blueprint(admin_routes.charge_rule.admin_charge_rule_bp)

    # Site side blueprint registers
    app.register_blueprint(site_routes.main.site_main_bp)

    return app
