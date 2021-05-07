from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import InputRequired, Optional, ValidationError, URL

def species_check(form, field):
    """checks if species if cat, dog , or porcupine"""
    if not (field.data in ['cat', 'dog', 'porcupine']):
        raise ValidationError('Species must be a cat, dog, or porcupine')

def age_check(form, field):
    """checks if age is between 0 and 30"""
    if field.data > 30  or field.data < 0:
        raise ValidationError('Age must be between 0 and 30')

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField('Pet Name', [InputRequired()])
    species = StringField('Species', [InputRequired(), species_check])
    photo_url = StringField('Photo URL', [Optional(), URL()])
    age = IntegerField('Age', [age_check])
    notes = StringField('Notes')
    available = BooleanField('Available')

class EditPetForm(FlaskForm):
    """Form for editting pets."""

    photo_url = StringField('Photo URL', [Optional(), URL()])
    notes = StringField('Notes')
    available = BooleanField('Available')

