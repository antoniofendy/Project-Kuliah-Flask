from logging import PlaceHolder
from random import choices
from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    TextAreaField,
    TelField,
    StringField,
    SelectField,
    EmailField,
    DateField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length


class MemberForm(FlaskForm):
    id = IntegerField("ID Member", render_kw={"readonly": True})
    name = StringField("Nama", validators=[DataRequired(), Length(3, 64)])
    gender = SelectField("Gender", choices=[('placeholder', 'Pilih gender'), ('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan')], validators=[DataRequired(), Length(9, 15)])
    birth = DateField("Tanggal Lahir", validators=[DataRequired(), Length(8, 32)])
    address = TextAreaField("Alamat", validators=[DataRequired(), Length(10, 255)])
    phone = TelField("No. Telepon", validators=[DataRequired(), Length(8, 13)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(1, 64)])
    submit = SubmitField("Simpan")
