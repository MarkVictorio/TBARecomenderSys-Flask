from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog.admin.forms import (QuestionForm, QuizForm)
from flaskblog.models import Quiz, Question, Choices
from flaskblog import db

admin = Blueprint('admin', __name__)

@admin.route("/administrator")
@login_required
def administrator():
    if current_user.admin != 1:
        return redirect(url_for('main.home'))
    
    return render_template('admin.html', title='Administrator Options')

@admin.route("/administrator/show_quiz")
@login_required
def show_quiz():
    if current_user.admin != 1:
        return redirect(url_for('main.home'))
    return render_template('show_quiz.html', title='Quiz List')

@admin.route("/quiz", methods=['GET','POST'])
@login_required
def quiz():
    choice = request.form.get('choices')
    return render_template('quiz.html', title = 'Quiz',choice = choice)

@admin.route("/create_quiz" , methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.admin != 1:
        return redirect(url_for('main.home'))
    
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(title = form.title.data, description = form.description.data, total_score = 10) 
        db.session.add(quiz)
        
        for field in form.items():
            question = Question(item_desc = field.question.data, answer = field.answer.data)
            choice1 = Choices(choice = field.choices1.data)
            choice2 = Choices(choice = field.choices2.data)
            choice3 = Choices(choice = field.choices3.data)
            choice4 = Choices(choice = field.choices4.data)

            db.session.add(question)
            db.session.add(choice1)
            db.session.add(choice2)
            db.session.add(choice3)
            db.session.add(choice4)
        
        db.session.commit()
        flash('Your quiz has been created!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('create_quiz.html', title='New Quiz',
                           form=form, legend='New Quiz')

