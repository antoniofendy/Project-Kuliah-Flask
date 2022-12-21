from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class StockForm(FlaskForm):
    id = IntegerField("ID Stok", render_kw={"readonly": True})
    car_id = SelectField("Mobil", validators=[DataRequired()])
    garage_id = SelectField("Garasi Mobil", validators=[DataRequired()])
    price_per_day = IntegerField("Biaya Sewa Per Hari", validators=[DataRequired(), NumberRange(1, 10000000)])
    quantity = IntegerField("Jumlah Mobil", validators=[DataRequired(), NumberRange(1, 1000)])
    submit = SubmitField("Simpan")
