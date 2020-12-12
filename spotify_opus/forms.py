from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from wtforms_components import DateField

from spotify_opus.models.Work import Genre


class WorkForm(FlaskForm):
    work = StringField(u"Type of work", validators=[DataRequired()], default="Piano Concerto")
    choices = [(member, member.name) for member in Genre]
    date_written = DateField("Date of composition")
    genre = SelectField(u"Genre", choices=choices)
    submit = SubmitField("Create")
