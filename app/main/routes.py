from flask import render_template
from flask_login import login_required

from app.main import bp
from app.models import User


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Домашняя страница')

# @bp.route('/rating')
# @login_required
# def rating():
#     users = User.query.order_by(User.score).all()
#     return render_template('rating.html', title='Рейтинг', users=users)
