from flask import render_template, flash, url_for, request, redirect
from app import db
from app.admin import bp
from app.admin.forms import AddUserForm, EditUserForm
from app.models import User

@bp.route('/users', methods=['GET', 'POST'])
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page, 25, False)
    return render_template('admin/user.html', users=users.items)

@bp.route('/adduser', methods=['GET', 'POST'])
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        # create user and insert into database
        user = User(username=form.username.data, email=form.email.data, admin=(True if form.role.data=='admin' else False))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User successfully added.")
        return redirect(url_for('admin.users'))
    return render_template('admin/adduser.html', form=form)

@bp.route('/<int:id>/edituser', methods=['GET', 'POST'])
def edituser(id):
    # get the user row entry using id in url
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash("User does not exist.")
        return redirect(url_for('admin.users'))
    # initialise form with correct default value for role selector
    form = EditUserForm(user=user, role=('admin' if user.admin else 'user'))
    if form.validate_on_submit():
        # update row entry in database
        user.username = form.username.data
        user.email = form.email.data
        user.admin = (True if form.role.data == 'admin' else False)
        print(form.role.data)
        db.session.commit()
        flash("User successfully updated.")
    return render_template('admin/edituser.html', user=user, form=form) 