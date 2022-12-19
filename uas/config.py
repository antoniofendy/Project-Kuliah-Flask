from os import urandom

# Konfigurasi
# DEBUG = True
# MY_VAR = "Konfigurasi Pemrograman WEB"


class Config:
    SECRET_KEY = urandom(32)

    UPLOAD_FOLDER = "static/upload"

    DB_NAME = "sewamobil1"
    SQLALCHEMY_DATABASE_URI = f"mysql://root:@localhost/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFIFACTIONS = False
