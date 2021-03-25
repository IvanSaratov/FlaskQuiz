from flask import render_template, redirect, url_for, flash, request
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
    class Prog:
        def __init__(self, id, com, total):
            self.quiz_id = id
            self.completed = com
            self.total = total

    quizs = Quiz.query.all()
    progress = UserQuizProgress.query.filter_by(user_id=current_user.id)
    prog = []
    for quiz in quizs:
        a = [x.progress for x in progress if x.id == quiz.id]
        if not a:
            prog.append(Prog(quiz.id, 0, len(quiz.questions)))
        else:
            prog.append(Prog(quiz.id, a.pop() - 1, len(quiz.questions)))

    return render_template('list.html', title='Список игр', quizs=quizs, progress=prog)


@bp.route('/card/<int:quiz_id>/<int:question_id>', methods=['GET', 'POST'])
@login_required
def card(quiz_id, question_id):
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if quiz is None:
        flash('Такой игры не найдено')
        return redirect(url_for('main.list'))

    p = UserQuizProgress.query.filter_by(user_id=current_user.id, quiz_id=quiz.id).first()
    if p is None:
        p = UserQuizProgress(user=current_user, quiz=quiz, progress=quiz.questions[0].id)
        db.session.add(p)
        db.session.commit()

    if p.progress > quiz.questions[-1].id:
        flash('Опросник завершен')
        return redirect(url_for('main.list'))

    if p.progress != question_id:
        return redirect(url_for('main.card', quiz_id=quiz_id, question_id=p.progress))

    question = Question.query.get(p.progress)

    if request.method == 'POST':
        true_answer = [str(x.id) for x in question.answers if x.isAnswer]

        if question.type == Type.CHECKBOX:
            a = request.form.getlist('answer_check')
            if set(a) == set(true_answer):
                current_user.rating += 1
        elif question.type == Type.RADIO:
            a = request.form.get('answer_radio')
            if a == str(true_answer.pop()):
                current_user.rating += 1
        elif question.type == Type.TEXTFIELD:
            a = request.form.get('answer_string')
            if a == question.answers.pop().answer:
                current_user.rating += 1
        else:
            flash('Неправильный тип')
            return redirect(url_for('main.card', quiz_id=quiz_id, question_id=p.progress))

        if p.progress == quiz.questions[-1].id:
            p.progress += 1
        else:
            for i, x in enumerate(quiz.questions):
                if x.id == p.progress:
                    p.progress = quiz.questions[i + 1].id
                    break

        db.session.commit()
        return redirect(url_for('main.card', quiz_id=quiz_id, question_id=p.progress))

    return render_template('card.html', title='Играем!', question=question)


@bp.route('/reload')
@login_required
def reload():
    try:
        db.session.query(UserQuizProgress).delete()
        db.session.query(Answers).delete()
        db.session.query(Question).delete()
        db.session.query(Quiz).delete()
        User.query.update({User.rating: 0})

        answers1 = [Answers(answer="Ответ 1"), Answers(answer="Ответ 2", isAnswer=True), Answers(answer="Ответ 3")]
        answers2 = [Answers(answer="Ответ 1"), Answers(answer="Ответ 2", isAnswer=True), Answers(answer="Ответ 3")]
        answers3 = [Answers(answer="test", isAnswer=True)]
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
