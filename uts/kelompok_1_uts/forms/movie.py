from flask_wtf import FlaskForm

from wtforms import (
    StringField, 
    SubmitField, 
    IntegerField, 
    FileField,
    SelectField)
from wtforms.validators import DataRequired


class MovieForm(FlaskForm):
    id_movies = IntegerField("ID Film", render_kw={"readonly": True})
    title = StringField("Judul", validators=[DataRequired()])
    synopsis = StringField("Sinopsis", validators=[DataRequired()])
    picture = FileField("Poster Film")
    category = SelectField("Kategori")
    duration = StringField("Durasi", validators=[DataRequired()])
    actor = StringField("Aktor/Aktris", validators=[DataRequired()])
    submit = SubmitField("Simpan")
