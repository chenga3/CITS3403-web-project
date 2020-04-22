#### TO ADD: Referencing, Login via email

import functools, re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        # Error processing
        if not username:
            error = 'Username required.'
        elif not email:
            error = 'Email required.'
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            error = 'Invalid email format.'
        elif not password:
            error = "Password required."
        elif db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'The username {} has already been taken'.format(username)
        elif db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'The email {} has already been used'.format(email)

        if error is None:
            # make insertion into database and redirect to login page
            db.execute(
                'INSERT INTO user (username, email, password, admin) VALUES (?, ?, ?, ?)',
                (username, email, generate_password_hash(password), 0)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/Register1.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user'] = user['username']
            return redirect(url_for('home'))

        flash(error)

    return render_template('auth/Login1.html')

# load in user for each page visited if logged in
@bp.before_app_request
def load_user():
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE username = ?', (user,)
        ).fetchone()

# logout user
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))