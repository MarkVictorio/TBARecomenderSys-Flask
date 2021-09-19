from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog.admin.forms import UserInputForm
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
    total = Question.query.filter_by(quiz_id=quiz_id).count()
    form = UserInputForm()
    u_choice = request.form.get("Choice ")
    user_choice = []
    
    for i in range(total):
        index = str(i + 1)
        u_choice = request.form.get("Choice "+ index)
        user_choice.append(u_choice)
    
    if request.method == 'POST':
        return redirect(url_for('admin.results', quiz_id = quiz_id))
    
    return render_template('quiz.html', title = quizzes.title,     
        quizzes = quizzes, questions = questions, total = total ,quiz_id = quiz_id , form = form)

@admin.route("/quiz/<int:quiz_id>/results")
@login_required
def results(quiz_id):
    quizzes = Quiz.query.get_or_404(quiz_id)
    return render_template('results.html', title = 'Quiz Results',quiz_id=quiz_id)