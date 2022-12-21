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
    nameUser = StringField("Nama", validators=[DataRequired(), Length(3, 255)])
    phoneUser = StringField("No. Telepon", validators=[DataRequired()])
    addressUser = StringField("Alamat", validators=[DataRequired(), Length(3, 255)])
    date_of_birthUser = DateField("Tanggal Lahir", format="%Y-%m-%d", validators=[DataRequired()])
    emailUser = EmailField("Email",validators=[DataRequired()])
    occupationUser = StringField("Status Pekerjaan", validators=[DataRequired()])
    passwordUser = PasswordField("Password")
    sexUser = SelectField("Jenis Kelamin",
        choices=[
            ("MALE", "Laki-laki"),
            ("FEMALE", "Perempuan"),
        ],
        validators=[DataRequired(), Length(9, 15)],
    )
    submit = SubmitField("Simpan")