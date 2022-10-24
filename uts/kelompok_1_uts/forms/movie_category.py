
from flask_wtf import FlaskForm

from wtforms import (
    StringField, 
    SubmitField, 
    IntegerField, 
    FileField)
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    id_category = IntegerField("ID Film", render_kw={"readonly": True})
    category_name = StringField("Nama Kategori", validators=[DataRequired()])
    submit = SubmitField("Simpan")
