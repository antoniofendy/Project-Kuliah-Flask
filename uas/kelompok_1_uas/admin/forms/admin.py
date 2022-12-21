from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    EmailField,
    SelectField,
    SubmitField,
    StringField,
    TelField,
    TextAreaField,
    PasswordField,
)
from wtforms.validators import DataRequired, Length, Email


class AdminForm(FlaskForm):
    id = IntegerField("ID Admin", render_kw={"readonly": True})
    name = StringField("Nama Lengkap", validators=[DataRequired(), Length(0, 255)])
    phone = TelField("No. Telepon", validators=[Length(8, 13)])
    address = TextAreaField("Alamat", validators=[Length(0, 255)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField("Password", validators=[])
    submit = SubmitField("Simpan")
