from flask import Flask, render_template, request, flash

from routes.main import main
from routes.rental import rental
from routes.stock import stock

app = Flask(__name__)
app.config.from_pyfile("config.cfg")

app.register_blueprint(main, url_prefix="")
app.register_blueprint(rental, url_prefix="/rental")
app.register_blueprint(stock, url_prefix="/stock")


if __name__ == "__main__":
    app.run(debug=True)
