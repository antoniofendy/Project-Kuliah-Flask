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


@application.route('/members')
def members():
    return render_template('index.html', templates=templates)


# Kosasi
@application.route('/menu-1')
def menu1():
    ganjilGenap = GanjilGenap()
    return render_template('hasil.html', templates=templates, data=data)


# Fendyanto
@application.route('/ganjil-genap', methods=['POST'])
def ganjil_genap():
    if request.method == 'POST':
        ganjilGenap = GanjilGenap(
            request.form['angka_1'], request.form['angka_2'])

    return render_template('hasil.html', templates=templates, ganjilGenap=ganjilGenap)


# Johanes Shane
@application.route('/ganjil-genap/<angka_1>/<angka_2>')
def ganjil_genap_arguments(angka_1, angka_2):
    ganjilGenap = GanjilGenap()
    return render_template('hasil.html', templates=templates, data=data)


if __name__ == '__main__':
    application.run(debug=True)
