from flask_wtf import FlaskForm

from wtforms import IntegerField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class GarageForm(FlaskForm):
    id = IntegerField("ID Garasi", render_kw={"readonly": True})
    name = StringField("Nama Garasi", validators=[DataRequired(), Length(3, 255)])
    address = TextAreaField("Alamat", validators=[DataRequired(), Length(3, 255)])
    submit = SubmitField("Simpan")
