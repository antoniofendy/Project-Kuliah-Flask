from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    SelectField,
    DateField,
    SubmitField,
    StringField,
    TimeField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta


class RentForm(FlaskForm):
    id = IntegerField("ID Reservasi", render_kw={"readonly": True})
    user = SelectField("Pelanggan", coerce=int, validators=[DataRequired()])
    car = SelectField("Mobil", coerce=int, validators=[DataRequired()])
    pickup_location = SelectField(
        "Lokasi Pengambilan", coerce=int, validators=[DataRequired()]
    )
    dropoff_location = SelectField(
        "Lokasi Pengembalian", coerce=int, validators=[DataRequired()]
    )
    pickup_date = DateField(
        "Tanggal Pengambilan", validators=[DataRequired()], default=datetime.now()
    )
    pickup_time = TimeField(
        "Waktu Pengambilan", validators=[DataRequired()], default=datetime.now()
    )
    dropoff_date = DateField(
        "Tanggal Pengembalian", validators=[DataRequired()], default=datetime.now()
    )
    note = TextAreaField("Catatan")
    status = SelectField(
        "Status Reservasi",
        choices=[
            ("OPEN", "Menunggu Konfirmasi"),
            ("RENTED", "Disewa"),
            ("RETURN", "Dikembalikan"),
            ("FAIL", "Gagal"),
        ],
    )
    submit = SubmitField("Simpan")
