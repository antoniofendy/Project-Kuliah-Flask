from flask import flash
from flask_wtf import FlaskForm
from kelompok_1_uas.user.models.user import GenderStat

from wtforms import (
    StringField, 
    SubmitField, 
    IntegerField,
    SelectField,
    DateField,
    EmailField,
    PasswordField
    )
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    id = IntegerField("ID", render_kw={"readonly": True})
    name = StringField("Nama", validators=[DataRequired(), Length(3, 255)])
    phone = StringField("No. Telepon", validators=[DataRequired()])
    address = StringField("Alamat", validators=[DataRequired(), Length(3, 255)])
    date_of_birth = DateField("Tanggal Lahir", format="%Y-%m-%d", validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired()])
    password = PasswordField("Password")
    sex = SelectField("Jenis Kelamin",
        choices=[
            ("MALE", "Laki-laki"),
            ("FEMALE", "Perempuan"),
        ],
        validators=[DataRequired(), Length(9, 15)],
    )
    submit = SubmitField("Simpan")