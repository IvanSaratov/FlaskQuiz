from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.main import bp
from app.models import User, Quiz, UserQuizProgress, Answers, Question, Type


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
    quizs = Quiz.query.all()
    return render_template('list.html', title='Список игр', quizs=quizs)


@bp.route('/reload')
@login_required
def reload():
    try:
        db.session.query(UserQuizProgress).delete()
        db.session.query(Answers).delete()
        db.session.query(Question).delete()
        db.session.query(Quiz).delete()
        User.query.update({User.rating: 0})

        answers1 = [Answers(answer="Ответ 1"), Answers(answer="Ответ 2"), Answers(answer="Ответ 3")]
        answers2 = [Answers(answer="Ответ 1"), Answers(answer="Ответ 2"), Answers(answer="Ответ 3")]
        answers3 = [Answers(answer="test")]
        questions = [Question(question="Вопрос 1", type=Type.CHECKBOX, answers=answers1),
                     Question(question="Вопрос 2", type=Type.RADIO, answers=answers2),
                     Question(question="Вопрос 3", type=Type.TEXTFIELD, answers=answers3)]
        quiz = Quiz(name="Тестовый тест", questions=questions)
        db.session.add(quiz)
        db.session.commit()
        flash("База обновлена")
    except Exception as e:
        db.session.rollback()
        flash("База не обновилась: " + e.__str__())

    return redirect(url_for('main.index'))
