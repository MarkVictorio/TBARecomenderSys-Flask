from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, Form
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired


class QuestionForm(Form):
    question = StringField('Question',validators=[DataRequired()])
    choice_1 = StringField('Choice 1',validators=[DataRequired()])
    choice_2 = StringField('Choice 2',validators=[DataRequired()])
    choice_3 = StringField('Choice 3',validators=[DataRequired()])
    choice_4 = StringField('Choice 4',validators=[DataRequired()])
    answer = IntegerField('Answer',validators=[DataRequired()])

class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Quiz Desciption', validators=[DataRequired()])
    items = FieldList(FormField(QuestionForm),min_entries=2)
    submit = SubmitField('Create')
