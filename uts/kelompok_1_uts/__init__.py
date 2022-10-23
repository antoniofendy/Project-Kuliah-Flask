from flask import Flask
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

    from kelompok_1_uts.routes.main import bp as main_bp
    from kelompok_1_uts.routes.rental import bp as rental_bp
    from kelompok_1_uts.routes.stock import bp as stock_bp
    from kelompok_1_uts.routes.member import bp as member_bp
    from kelompok_1_uts.routes.charge_rule import bp as charge_rule_bp
    from kelompok_1_uts.errors import bp as errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(rental_bp, url_prefix="/rental")
    app.register_blueprint(stock_bp, url_prefix="/stock")
    app.register_blueprint(member_bp, url_prefix="/member")
    app.register_blueprint(charge_rule_bp, url_prefix="/charge-rule")
    app.register_blueprint(errors_bp)

    return app
