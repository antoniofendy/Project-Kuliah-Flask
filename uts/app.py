from flask import *

application = Flask(__name__)
application.config.from_pyfile('config.cfg')


@application.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True)
