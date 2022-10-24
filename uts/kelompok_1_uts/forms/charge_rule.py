from logging import PlaceHolder
from random import choices
from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    DecimalField,
    SelectField,
    SubmitField,
    StringField
)
from wtforms.validators import DataRequired, Length


class ChargeRuleForm(FlaskForm):
    id = IntegerField("ID Aturan Charge", render_kw={"readonly": True})
    name = StringField("Nama Aturan", validators=[DataRequired(), Length(3, 255)])
    amount = DecimalField("Nilai", places=2, rounding=None, use_locale=False, number_format=None, validators=[DataRequired()])
    type = SelectField("Tipe", choices=[('placeholder', 'Pilih tipe'), ('PERCENTAGE', 'Percentage'), ('NOMINAL', 'Nominal')], validators=[DataRequired()])
    submit = SubmitField("Simpan")
