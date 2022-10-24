from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    SubmitField,
    SelectField,
    DecimalField,
)
from wtforms.validators import DataRequired, Email, Length


class StockForm(FlaskForm):
    id = IntegerField("ID Stok", render_kw={"readonly": True})
    movie = SelectField("Film", coerce=int, validators=[DataRequired()])
    price = DecimalField("Harga per Hari", validators=[DataRequired()])
    qty = IntegerField("Qty", validators=[DataRequired()])

    submit = SubmitField("Simpan")
