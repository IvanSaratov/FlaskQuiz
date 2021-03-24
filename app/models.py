from enum import Enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Type(Enum):
    CHECKBOX = 1
    RADIO = 2
    TEXTFIELD = 3


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True, nullable=False)
    questions = db.relationship("Question")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    type = db.Column(db.Enum(Type))
    answers = db.relationship("Answers")
    quiz_id = db.Column(db.Integer, db.ForeignKey(Quiz.id))


class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))
    answer = db.Column(db.String, nullable=False)
    isAnswer = db.Column(db.Boolean, default=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    rating = db.Column(db.Integer, default=1)
    progress = db.relationship("UserQuizProgress")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class UserQuizProgress(db.Model):
    db.__tablename__ = 'user_quiz'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    quiz_id = db.Column(db.Integer, db.ForeignKey(Quiz.id))
    quiz = db.relationship(Quiz)
    progress = db.Column(db.Integer)
