from flask_wtf import FlaskForm

from wtforms import IntegerField, SelectField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta


class TransactionForm(FlaskForm):
    today = datetime.today()
    two_weeks = today + timedelta(days=14)

    id = IntegerField("ID Transaksi", render_kw={"readonly": True})
    member = SelectField(
        "Member",
        coerce=int,
        validators=[DataRequired()],
    )
    movie = SelectField(
        "Film",
        coerce=int,
        validators=[DataRequired()],
    )
    rental_start = DateField(
        "Tanggal Sewa",
        validators=[DataRequired()],
    )
    rental_end = DateField(
        "Tanggal Akhir Sewa",
        validators=[DataRequired()],
    )
    charge = SelectField("Aturan Denda", coerce=int, validators=[DataRequired()])
    staff = SelectField("Staf", coerce=int)
    status = StringField(render_kw={"readonly": True})
    rental_return = DateField("Tanggal Pengembalian")

    submit = SubmitField("Simpan")
