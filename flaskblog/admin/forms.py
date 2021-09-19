from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, RadioField
from wtforms.fields.core import BooleanField, IntegerField
from wtforms.validators import DataRequired

class UserInputForm(FlaskForm):
    user_answer = IntegerField('Answer',validators=[DataRequired()])
