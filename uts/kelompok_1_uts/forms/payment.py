from flask_wtf import FlaskForm

from wtforms import IntegerField, SelectField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta


class PaymentForm(FlaskForm):
    id = IntegerField("ID Pembayaran", render_kw={"readonly": True})
    transaction_id = IntegerField("Atas Transaksi", render_kw={"readonly": True})
    type = SelectField(
        "Tipe Transaksi",
        render_kw={"readonly": True},
        choices=[
            ("PAYMENT", "Pembayaran"),
            ("CHARGE", "Denda"),
        ],
    )
    amount = IntegerField("Jumlah Harus Dibayar", render_kw={"readonly": True})
    status = StringField("Status", render_kw={"readonly": True})

    submit = SubmitField("Bayar")
