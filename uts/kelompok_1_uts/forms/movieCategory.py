
from flask_wtf import FlaskForm

from wtforms import (
    StringField, 
    SubmitField, 
    IntegerField)
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    id = IntegerField("ID Kategori", render_kw={"readonly": True})
    category_name = StringField("Nama Kategori", validators=[DataRequired()])
    submit = SubmitField("Simpan")
