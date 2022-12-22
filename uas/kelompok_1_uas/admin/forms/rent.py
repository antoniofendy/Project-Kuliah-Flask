from flask_wtf import FlaskForm

from wtforms import IntegerField, SelectField, SubmitField, StringField, FileField
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta


class RentForm(FlaskForm):
    id = IntegerField("ID Reservasi", render_kw={"readonly": True})
    user = SelectField("Pelanggan", coerce=int, validators=[DataRequired()])
    admin = StringField("Dibuat oleh", render_kw={"readonly": True})
    reservation = SelectField("Reservasi", validators=[DataRequired()])
    charge_rule = SelectField("Aturan Denda")
    type = SelectField(
        "Tipe Transaksi", choices=[("PAYMENT", "Pembayaran"), ("CHARGE", "Denda")]
    )
    transfer_file = FileField("Bukti Pembayaran")
    total = StringField("Total Dibayar")
    status = SelectField(
        "Status Transaksi",
        choices=[
            ("UNPAID", "Belum Dibayar"),
            ("PENDING", "Menunggu Konfirmasi"),
            ("PAID", "Dibayar"),
        ],
    )

    submit = SubmitField("Simpan")
