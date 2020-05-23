from flask import render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.solve import bp
from app.models import User, Problem

@bp.route('/problems')
def problems():
    problems = Problem.query.all()
    return render_template('solve/problems.html', title='Problems', problems=problems)

@bp.route('/rankings')
def rankings():
    users = User.query.all()
    users.sort(key=lambda x:x.points, reverse=True)
    return render_template('solve/rankings.html', title='Rankings', users=users)