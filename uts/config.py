from os import urandom

# Konfigurasi
# DEBUG = True
# MY_VAR = "Konfigurasi Pemrograman WEB"


class Config:
    SECRET_KEY = urandom(32)

    DB_NAME = "kelompok_1_uts"
    SQLALCHEMY_DATABASE_URI = f"mysql://root:@localhost/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFIFACTIONS = False
