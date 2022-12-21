from kelompok_1_uas import db
import enum

class GenderStat(enum.Enum):
    MALE = "Laki-laki"
    FEMALE = "Perempuan"

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(50), unique = True)
    address = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    sex = db.Column(
        db.Enum(GenderStat), nullable=False, default=GenderStat.MALE
    )
    occupation = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))