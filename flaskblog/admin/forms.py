from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, RadioField
from wtforms.fields.core import BooleanField, IntegerField
from wtforms.validators import DataRequired

class UserInputForm(FlaskForm):
    radio = RadioField(label='label',choices=[])
    user_answer = IntegerField('Answer',validators=[DataRequired()])
    is_correct = BooleanField('Correct', validators=[DataRequired()])
