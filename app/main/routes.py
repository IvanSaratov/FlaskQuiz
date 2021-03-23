from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

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
    progress = UserQuizProgress.query.filter_by(user_id=current_user.id)
    return render_template('list.html', title='Список игр', quizs=quizs, progress=progress)


@bp.route('/card/<int:quiz_id>/<int:question_id>')
@login_required
def card(quiz_id, question_id):
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    return render_template('card.html', title='Играем!', question=quiz.questions[question_id])


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
