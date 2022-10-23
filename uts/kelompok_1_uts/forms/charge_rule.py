from logging import PlaceHolder
from random import choices
from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    DecimalField,
    SelectField,
    SubmitField,
)
from wtforms.validators import DataRequired


class ChargeRuleForm(FlaskForm):
    id = IntegerField("ID Aturan Charge", render_kw={"readonly": True})
    amount = DecimalField("Nilai", places=2, rounding=None, use_locale=False, number_format=None, validators=[DataRequired()])
    type = SelectField("tipe", choices=[('placeholder', 'Pilih tipe'), ('percentage', 'Percentage'), ('nominal', 'Nominal')], validators=[DataRequired()])
    submit = SubmitField("Simpan")
