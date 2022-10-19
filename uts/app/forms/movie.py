from ast import Sub
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    title = StringField("Judul", validators=[DataRequired()])
    submit = SubmitField("Simpan")
