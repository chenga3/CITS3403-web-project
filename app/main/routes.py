from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app.main import bp
from app.models import User

@bp.route('/')
@bp.route('/homepage')
def homepage():
    return render_template('homepage.html', title="YeetCode")
