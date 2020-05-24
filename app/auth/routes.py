from flask import render_template, flash, redirect, url_for, request
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, EditProfileForm,ResetPasswordForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form =  LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username_email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username/email or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        token = user.get_token()
        print(token)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.homepage')
        return redirect(next_page) 
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    current_user.revoke_token()
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # create the new user and insert into database
        user = User(username=form.username.data, email=form.email.data, admin=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/profile/<username>/<rank>')
@login_required
def profile(username,rank):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('auth/profile.html', user=user, rank=rank, title='Profile')

@bp.route('/edit_profile/<username>',methods=['GET','POST'])
@login_required
def edit_profile(username):
    user=User.query.filter_by(username=username).first_or_404()
    if username != current_user.username:
        return redirect(url_for('main.homepage'))
    form = EditProfileForm(prefer_language=('py' if current_user.prefLanguage == 'py' else 'cpp'))
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.prefLanguage = form.prefer_language.data
        db.session.commit()
        flash('Your change has been saved')
        return redirect(url_for('main.homepage'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/edit_profile.html', user=user, title='Edit Profile',
                           form=form)

@bp.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        logout_user()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)