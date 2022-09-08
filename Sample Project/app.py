from tkinter import Menu
from flask import Flask, render_template, redirect
from models import Lingkaran
from logika import Logika

application = Flask(__name__)
application.config.from_pyfile('config.cfg')
menu = application.config['MENU'] 
footer = application.config['FOOTER']


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/indextemplate')
def indextemplate():
    return render_template('index (menu footer).html', menu=menu, footer=footer)

@application.route('/lingkaran')
def lingkaran():

    model = Lingkaran()
    #model.getRadius()
    model.setRadius(14.0)
    
    return render_template('lingkaran.html', model=model)

@application.route('/logika/<a>/<b>')
def logika(a,b):

    return render_template('logika.html', a=a, b=b)

@application.route('/konfigurasi')
def konfigurasi():
    return render_template(\
    'konfigurasi.html',\
    var=application.config['MY_VAR'])


if __name__ == '__main__':
    application.run(debug=True)