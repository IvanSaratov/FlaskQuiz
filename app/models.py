from enum import Enum

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Type(Enum):
    CHECKBOX = 1
    RADIO = 2
    TEXTFIELD = 3


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(256), index=True, unique=True, nullable=False)
    questions = db.relationship("Question")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    question = db.Column(db.String(256), nullable=False)
    type = db.Column(db.Enum(Type))
    answers = db.relationship("Answers")
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))


class Answers(db.Model):
    quest_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class Progress(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.Integer, nullable=False)


association_progress_table = db.Table('association_progress_table',
                                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                      db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
                                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    rating = db.Column(db.Integer, default=0)
    progress = db.relationship('Progress', secondary=association_progress_table,
                               backref=db.backref('progress', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
