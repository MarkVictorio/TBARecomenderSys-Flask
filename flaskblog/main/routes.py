from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog.admin.forms import UserInputForm
from flaskblog.models import Quiz, Question, Quiz_user_answer, Quiz_user_taken
from flaskblog import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    quizzes = Quiz.query.order_by(Quiz.id.asc()).paginate(page=page, per_page=10)
    return render_template('home.html', title='Quiz List', quizzes = quizzes)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/quiz/<int:quiz_id>", methods=['GET','POST'])
@login_required
def quiz(quiz_id):
    taken = Quiz_user_taken.query.filter_by(user_id = current_user.id).first()
    try:
        if taken.is_taken == 1:
            return redirect(url_for('main.results', quiz_id = quiz_id))
    except AttributeError:
        pass
    quizzes = Quiz.query.get_or_404(quiz_id)
    page = request.args.get('page', 1, type=int)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.quiz_id.asc()).paginate(page=page, per_page=30)
    total = Question.query.filter_by(quiz_id=quiz_id).count()
    form = UserInputForm()
    u_choice = request.form.get("Choice ")
    user_choice = []
    answer = request.form.get("answer ")
    answers = []
    for i in range(total):
        index = str(i + 1)
        u_choice = request.form.get("Choice "+ index)
        user_choice.append(u_choice)

    for y in range(total):
        index = str(y + 1)
        answer = request.form.get("answer "+ index)
        answers.append(answer)

    if request.method == 'POST':
        total_score = 0
        for j in range(len(user_choice)):
            user_choice[j] = int(user_choice[j])
            answers[j] = int(answers[j])
            correct = False
            if user_choice[j] == answers[j]:
                correct = True
                total_score += 1
            user_answer = Quiz_user_answer(user_id = current_user.id, question_id = j+1, user_answer = user_choice[j], is_correct = correct, quiz_id = quiz_id)
            db.session.add(user_answer)
            db.session.commit()
        taken = Quiz_user_taken(user_id = current_user.id, quiz_id = quiz_id, is_taken = True, total = total_score)
        db.session.add(taken)
        db.session.commit()
        return redirect(url_for('main.results', quiz_id = quiz_id))
    
    return render_template('quiz.html', title = quizzes.title,     
        quizzes = quizzes, questions = questions, total = total ,quiz_id = quiz_id , form = form, taken = taken)

@main.route("/quiz/<int:quiz_id>/results")
@login_required
def results(quiz_id):
    quizzes = Quiz.query.get_or_404(quiz_id)
    user_results = (db.session.query(Question, Quiz_user_answer).join(Quiz_user_answer).filter_by(quiz_id = quiz_id).filter_by(user_id = current_user.id).all())
    return render_template('results.html', title = 'Quiz Results', quiz_id=quiz_id, quizzes=quizzes, user_results = user_results)

