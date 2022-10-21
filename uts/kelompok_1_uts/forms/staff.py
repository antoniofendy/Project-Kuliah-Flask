from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    TextAreaField,
    TelField,
    StringField,
    PasswordField,
    EmailField,
    FileField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length


class StaffForm(FlaskForm):
    id = IntegerField("ID Staf", render_kw={"readonly": True})
    name = StringField("Nama", validators=[DataRequired(), Length(3, 64)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8, 32)])
    phone = TelField("No. Telepon", validators=[Length(8, 13)])
    address = TextAreaField("Alamat", validators=[Length(0, 255)])
    picture = FileField("Foto")
    submit = SubmitField("Simpan")
