from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField, StringField, SelectField, FileField
from wtforms.validators import DataRequired, Length, NumberRange


class CarForm(FlaskForm):
    id = IntegerField("ID Mobil", render_kw={"readonly": True})
    model = StringField("Model", validators=[DataRequired(), Length(3, 255)])
    type = StringField("Tipe", validators=[DataRequired(), Length(3, 255)])
    brand = StringField("Brand", validators=[DataRequired(), Length(3, 255)])
    picture = FileField("Gambar", validators=[])
    transmission = SelectField(
        "Transmisi", 
        validators=[DataRequired()], 
        choices=[
            ("manual", "Manual"),
            ("automatic", "Automatic")
        ])
    seats = IntegerField("Maksimal Penumpang", validators=[DataRequired(), NumberRange(2, 6)])
    luggage = IntegerField("Maksimal Bagasi", validators=[DataRequired(), NumberRange(2, 6)])
    fuel = SelectField(
        "Jenis Bahan Bakar", 
        validators=[DataRequired()], 
        choices=[
            ("petrol", "Bensin"),
            ("electric", "Listrik")
        ])
    submit = SubmitField("Simpan")
