from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField, Form
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired


class QuestionForm(Form):
    question = StringField('Question',validators=[DataRequired()])
    choices1 = StringField('Choice 1',validators=[DataRequired()])
    choices2 = StringField('Choice 2',validators=[DataRequired()])
    choices3 = StringField('Choice 3',validators=[DataRequired()])
    choices4 = StringField('Choice 4',validators=[DataRequired()])
    answer = IntegerField('Answer',validators=[DataRequired()])

class QuizForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Quiz Desciption', validators=[DataRequired()])
    total_score = IntegerField('Number of Items', validators=[DataRequired()])
    items = FieldList(FormField(QuestionForm),min_entries=2)
    submit = SubmitField('Create')
