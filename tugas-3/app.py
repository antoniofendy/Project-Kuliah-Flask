from flask import Flask, render_template, request
from GanjilGenap import GanjilGenap

application = Flask(__name__)
application.config.from_pyfile('config.cfg')
header = application.config['HEADER']
footer = application.config['FOOTER']

templates = {
    'header': header,
    'footer': footer
}


@application.route('/')
def index():
    return render_template('index.html', templates=templates)


# Jo Shane
@application.route('/about')
def about():
    return render_template('about.html', templates=templates)


# Jo Shane
@application.route('/members')
def members():
    return render_template('index.html', templates=templates)


# Kosasi
@application.route('/ganjil-genap/<angka_1>/<angka_2>')
def menu1(angka_1, angka_2):
    ganjilGenap = GanjilGenap(angka_1, angka_2)
    return render_template('hasil.html', templates=templates, ganjilGenap=ganjilGenap)


# Fendyanto
@application.route('/ganjil-genap', methods=['POST'])
def ganjil_genap():
    if request.method == 'POST':
        ganjilGenap = GanjilGenap(
            request.form['angka_1'], request.form['angka_2'])

    return render_template('hasil.html', templates=templates, ganjilGenap=ganjilGenap)


if __name__ == '__main__':
    application.run(debug=True)
