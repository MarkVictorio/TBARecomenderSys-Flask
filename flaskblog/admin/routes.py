from flaskblog.main.routes import quiz
from functools import reduce
from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog.models import Quiz, Question, Quiz_user_answer, Quiz_user_taken
from flaskblog import db
from flaskblog.admin.utils import (collabFilter) 

admin = Blueprint('admin', __name__)

@admin.route("/administrator")
@login_required
def administrator():
    if current_user.admin != 1:
        return redirect(url_for('main.home'))
    return render_template('admin.html', title='Administrator Options')

@admin.route("/show_results")
@login_required
def result_list():
    if current_user.admin != 1:
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    quizzes = Quiz.query.order_by(Quiz.id.asc()).paginate(page=page, per_page=10)
    return render_template('result_list.html', title='Result List', quizzes = quizzes)

@admin.route("/CFTesting", methods=['GET','POST'])
@login_required
def cftest():
    page = request.args.get('page', 1, type=int)
    taken = Quiz_user_taken.query.order_by(Quiz_user_taken.user_id.asc()).filter_by(is_taken = 1).paginate(page=page, per_page=50)
    if request.method == 'POST':
        collabFilter()
    return render_template('cftest.html', title='Central Fiction', taken = taken)

