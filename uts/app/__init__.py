from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from os import urandom

DB_NAME = "database.db"

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile("config.cfg")
    app.config["SECRET_KEY"] = urandom(32)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFIFACTIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.main import bp as main_bp
    from app.routes.rental import bp as rental_bp
    from app.routes.stock import bp as stock_bp
    from app.errors import bp as errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(rental_bp, url_prefix="/rental")
    app.register_blueprint(stock_bp, url_prefix="/stock")
    app.register_blueprint(errors_bp)

    return app


# app.register_blueprint(main)

# from os import path
# from flask import Flask, render_template, request, flash
# from flask_sqlalchemy import SQLAlchemy

# from routes.main import main
# from routes.rental import rental
# from routes.stock import stock

# from models import Movie, Member

# app = Flask(__name__)
# db = SQLAlchemy()


# app.register_blueprint(main, url_prefix="")
# app.register_blueprint(rental, url_prefix="/rental")
# app.register_blueprint(stock, url_prefix="/stock")


# db.init_app(app)

# with app.app_context():
#     db.create_all()


# if __name__ == "__main__":
#     app.run(debug=True)


# # def create_database(app):
