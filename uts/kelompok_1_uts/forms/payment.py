from flask_wtf import FlaskForm

from wtforms import IntegerField, SelectField, DateField, SubmitField, StringField

from kelompok_1_uts.models.payment import PaymentType


class PaymentForm(FlaskForm):
    id = IntegerField("ID Pembayaran", render_kw={"readonly": True})
    transaction_id = IntegerField("Atas Transaksi", render_kw={"readonly": True})
    type = SelectField(
        "Tipe Transaksi",
        render_kw={"readonly": True},
        choices=[
            (PaymentType.PAYMENT.name, "Pembayaran"),
            (PaymentType.CHARGE.name, "Denda"),
        ],
    )
    amount = IntegerField("Jumlah Harus Dibayar", render_kw={"readonly": True})
    status = StringField("Status", render_kw={"readonly": True})

    submit = SubmitField("Bayar")
