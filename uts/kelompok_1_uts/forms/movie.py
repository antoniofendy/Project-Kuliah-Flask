from flask_wtf import FlaskForm

from wtforms import (
    StringField, 
    SubmitField, 
    IntegerField,
    TextAreaField,
    FileField,
    SelectField)
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    id = IntegerField("ID Film", render_kw={"readonly": True})
    title = StringField("Judul", validators=[DataRequired()])
    synopsis = TextAreaField("Sinopsis", validators=[DataRequired()])
    picture = FileField("Poster Film")
    category = SelectField("Kategori")
    duration = IntegerField("Durasi (menit)", validators=[DataRequired()])
    actor = StringField("Aktor/Aktris", validators=[DataRequired()])
    submit = SubmitField("Simpan")
