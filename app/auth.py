#### TO ADD: Referencing

import functools, re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        db = get_db()
        error = None

        # Error processing
        if not username:
            error = 'Username required.'
        elif db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'The username {} has already been taken'.format(username)
        elif not email:
            error = 'Email required.'
        elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            error = 'Invalid email format.'
        elif db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'The email {} has already been used'.format(email)
        elif not password:
            error = "Password required."
        elif not confirm:
            error = "Please confirm password."
        elif password != confirm:
            error = "Passwords did not match."

        if error is None:
            # make insertion into database and redirect to login page
            db.execute(
                'INSERT INTO user (username, email, password, admin) VALUES (?, ?, ?, ?)',
                (username, email, generate_password_hash(password), 0)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
        return render_template('auth/register.html', username=username, email=email)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        login = request.form['email/username']
        password = request.form['password']
        db = get_db()
        error = None

        # check if login identification provided was a username
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (login,)
        ).fetchone()
        if user is None:
            # check if a correct email was provided
            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (login,)
            ).fetchone()


        if user is None:
            error = 'Incorrect username/email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user'] = user['username']
            return redirect(url_for('home'))

        flash(error)

    return render_template('auth/login.html')

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