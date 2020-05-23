from flask import render_template, flash, url_for, request, redirect
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.admin.forms import AddUserForm, EditUserForm
from app.models import User, Problem, ProblemTestCases
from functools import wraps

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not current_user.admin:
            flash("You must be an admin to access this page.")
            return redirect(url_for('homepage'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page, 25, False)
    return render_template('admin/user.html', users=users.items)

@bp.route('/adduser', methods=['GET', 'POST'])
@login_required
@admin_required
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
@login_required
@admin_required
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

@bp.route('/<int:id>/deleteuser', methods=['GET'])
@login_required
@admin_required
def deleteuser(id):
    user = User.query.get(id)
    if user is None:
        flash("User does not exist.")
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.users'))

@bp.route('/questions', methods=['GET', 'POST'])
@login_required
@admin_required
def questions():
    problems = Problem.query.all()
    return render_template('admin/question.html', problems=problems)

@bp.route('/submitquestion', methods=['GET', 'POST'])
@login_required
@admin_required
def submitquestion():
    return render_template('admin/submitquestion.html')

@bp.route('/addquestion', methods=['POST'])  
@login_required
@admin_required
def addquestion():
    if request.method == 'POST':
        data = request.get_json()
    if data["body"] == "":
        return ("ERROR: Some Empty Inputs")
    problem = Problem.query.filter_by(title=data["title"]).first()
    if problem is not None:
        return ("ERROR: Problem Already Exists")
    else:
        p = Problem(\
            title=data["title"],\
            urlTitle=''.join((data["title"]).split()).lower(),\
            body=data["question"],\
            difficulty = data["diff"],\
            timeLimit = int(data["time"]),\
        )
        db.session.add(p)
        tests = data["testcases"]
        for i in tests:
            if i["input"] == "" or i["output"] == "":
                return ("ERROR: Some Empty Inputs")
            testcase = ProblemTestCases(\
                problem = p,\
                input = i["input"],\
                output = i["output"],
            )
            db.session.add(testcase)
        db.session.commit()
        return ("SUCCESS")

@bp.route('/editquestion', methods=['GET', 'POST'])
@login_required
@admin_required
def editquestion():
    return render_template('admin/editquestion.html')


@bp.route('/assess', methods=['GET', 'POST'])
@login_required
@admin_required
def assess():
    return render_template('admin/assess.html')