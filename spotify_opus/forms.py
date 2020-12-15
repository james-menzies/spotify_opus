from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms_components import DateField, ModelForm

from spotify_opus.models.Composer import Composer
from spotify_opus.models.Work import Genre


# class ComposerForm(FlaskForm):
#
#     name = StringField(u"Name", validators=[DataRequired()])
#     birth_year = IntegerField(u"Year of Birth", validators=[Length(min=4, max=4)])
#     death_year = IntegerField(u"Year of Death", validators=[Length(min=4, max=4)])
#
#


class ComposerForm(ModelForm):

    class Meta:
        model = Composer
        include_primary_keys = False
        exclude = ["image_url", "type", ]

class WorkForm(FlaskForm):


    work = StringField(u"Type of work", validators=[DataRequired()], default="Piano Concerto")
    choices = [(member, member.name) for member in Genre]
    date_written = DateField("Date of composition")
    genre = SelectField(u"Genre", choices=choices)
    submit = SubmitField("Create")
