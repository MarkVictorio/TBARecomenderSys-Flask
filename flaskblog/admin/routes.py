from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog.admin.forms import (QuestionForm, QuizForm)
from flaskblog.models import Quiz, Question
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
    page = request.args.get('page', 1, type=int)
    quizzes = Quiz.query.order_by(Quiz.id.asc()).paginate(page=page, per_page=10)
    return render_template('show_quiz.html', title='Quiz List', quizzes = quizzes)

@admin.route("/quiz/<int:quiz_id>", methods=['GET','POST'])
@login_required
def quiz(quiz_id):
    quizzes = Quiz.query.get_or_404(quiz_id)
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.quiz_id.asc()).paginate(page=page, per_page=20)
    u_choice = request.form.get('choices')
    return render_template('quiz.html', title = quizzes.title ,     
    u_choice = u_choice, quizzes = quizzes, questions = questions)

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
            question = Question(item_desc = field.question.data,answer = field.answer.data,     
            choice_1 = field.choice_1.data, choice_2 = field.choice_2.data,    
            choice_3 = field.choice_3.data, choice_4 = field.choice_4.data)
            db.session.add(question)
        
        db.session.commit()
        flash('Your quiz has been created!', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('create_quiz.html', title='New Quiz',
                           form=form, legend='New Quiz')

