from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.main import bp
from app.models import User

# Route for the Homepage
@bp.route('/')
@bp.route('/homepage')
def homepage():
    return render_template('homepage.html', title="YeetCode")

# Route for the rankings
@bp.route('/rankings')
def rankings():
    # get users for the rankings
    users = User.query.all()
    users.sort(key=lambda x:x.points, reverse=True)
    return render_template('rankings.html', title='Rankings', users=users)