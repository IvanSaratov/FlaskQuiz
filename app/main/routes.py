from flask import render_template
from flask_login import login_required

from app.main import bp
from app.models import User, Quiz


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Главная страница')


@bp.route('/rating')
@login_required
def rating():
    users = User.query.order_by(User.rating).all()
    return render_template('rating.html', title='Счет', users=users)


@bp.route('/quizs')
@login_required
def list():
    quizs = Quiz.query.order_by(Quiz.name).all()
    return render_template('list.html', title='Список игр', quizs=quizs)
