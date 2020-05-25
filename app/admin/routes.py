from flask import render_template, flash, url_for, request, redirect
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.admin.forms import AddUserForm, EditUserForm
from app.models import User, Problem, ProblemTestCases
from functools import wraps

# decorator for admin-only pages
# checks if the current user has admin=True in their db entry
def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not current_user.admin:
            flash("You must be an admin to access this page.")
            return redirect(url_for('main.homepage'))
        return view(**kwargs)
    return wrapped_view

# default admin page displaying a list of users/problems in AJAX
@bp.route('/manage', methods=['GET', 'POST'])
@login_required
@admin_required
def manage():
    return render_template('admin/manage.html', title="Admin")

# page for adding a new user into the db
@bp.route('/adduser', methods=['GET', 'POST'])
@login_required
@admin_required
def adduser():
    form = AddUserForm()
    if form.validate_on_submit():
        # create user and insert into database
        user = User(username=form.username.data, email=form.email.data,
            admin=(True if form.role.data=='admin' else False), prefLanguage=form.prefer_language.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User successfully added.")
        return redirect(url_for('admin.adduser'))
    return render_template('admin/adduser.html', form=form)

# page for editing an existing user
@bp.route('/<int:id>/edituser', methods=['GET', 'POST'])
@login_required
@admin_required
def edituser(id):
    # get the user row entry using id in url
    user = User.query.filter_by(id=id).first()
    if user is None:
        flash("User does not exist.")
        return redirect(url_for('admin.manage'))
    # initialise form with correct default value for role selector
    form = EditUserForm(user=user, role=('admin' if user.admin else 'user'),
        prefer_language=('py' if user.prefLanguage == 'py' else 'cpp'))
    if form.validate_on_submit():
        # update row entry in database
        user.username = form.username.data
        user.email = form.email.data
        user.admin = (True if form.role.data == 'admin' else False)
        user.prefLanguage = form.prefer_language.data
        db.session.commit()
        flash("User successfully updated.")
    return render_template('admin/edituser.html', user=user, form=form)

# page for adding a new problem into the db
@bp.route('/submitquestion', methods=['GET', 'POST'])
@login_required
@admin_required
def submitquestion():
    return render_template('admin/submitquestion.html')

# api-based function for adding a problem to the db
@bp.route('/addquestion', methods=['POST'])  
@login_required
@admin_required
def addquestion():
    data = request.get_json()
    # input validation
    if data["question"] == "":
        return ("ERROR: Empty Question")
    try:
        if float(data["time"]) <= 0:
            return ("ERROR: Please enter time > 0")
    except:
        return ("ERROR: Invalid time please enter a positive real number > 0")

    problem = Problem.query.filter_by(title=data["title"]).first()
    if problem is not None:
        return ("ERROR: Problem Already Exists")

    urltitle = ''.join((data["title"]).split()).lower()
    problem = Problem.query.filter_by(urlTitle=urltitle).first()
    if problem is not None:
        return ("ERROR: Problem Name to Similar to Another Problem")

    # add the problem
    p = Problem(\
        title=data["title"],\
        urlTitle=''.join((data["title"]).split()).lower(),\
        body=data["question"],\
        difficulty = data["diff"],\
        timeLimit = float(data["time"]),\
    )
    db.session.add(p)
    # add all its test cases
    tests = data["testcases"]
    for i in tests:
        if i["input"] == "" or i["output"] == "":
            return ("ERROR: Empty Test Case")
        testcase = ProblemTestCases(\
            problem = p,\
            input = i["input"],\
            output = i["output"],
        )
        db.session.add(testcase)
    db.session.commit()
    return ("Succesfully Added Question")

# page for editing a problem, displays the problem and its test cases
@bp.route('/editquestion/<urltitle>', methods=['GET', 'POST'])
@login_required
@admin_required
def editquestion(urltitle):
    problem = Problem.query.filter_by(urlTitle=urltitle).first()
    testcases = ProblemTestCases.query.filter_by(questionID=problem.id).all()
    return render_template('admin/editquestion.html', problem=problem, testcases = testcases)

# api-based function for deleting a problem
@bp.route('/question', methods=['DELETE'])
def delete_question():
    data = request.get_json()
    if data["urltitle"] == "":
        return ("ERROR: Some Empty Inputs")
    problem = Problem.query.filter_by(urlTitle=data["urltitle"]).first()
    if Problem.query.filter_by(urlTitle=data["urltitle"]) is not None:
        testcases = ProblemTestCases.query.filter_by(questionID = problem.id).all()
        for test in testcases:
            db.session.delete(test)
        db.session.delete(problem)
        db.session.commit()
        return "Succesfully Deleted"
    else:
        return ("SOMETHING WENT WRONG")

# api-based function for updating a problem
@bp.route('/question', methods=['PUT'])
def updatequestion():
    data = request.get_json()
    # input validation
    if data["question"] == "":
        return ("ERROR: Empty Question")
    try:
        if float(data["time"]) <= 0:
            return ("ERROR: Please enter time > 0")
    except:
        return ("ERROR: Invalid time please enter a positive real number > 0")

    urltitle = ''.join((data["title"]).split()).lower()
    problem = Problem.query.filter_by(urlTitle=urltitle).first()
    if problem is not None and urltitle != data["oldurltitle"]:
        print("trete")
        return ("ERROR: Problem Name to Similar to Another Problem")

    # update entry in db
    problem = Problem.query.filter_by(urlTitle=data["oldurltitle"]).first()
    if Problem.query.filter_by(title=data["title"]) is None or problem.title == data["title"]:
        problem.title=data["title"]
        problem.urlTitle=''.join((data["title"]).split()).lower()
        problem.body=data["question"]
        problem.difficulty = data["diff"]
        problem.timeLimit = float(data["time"])
        tests = data["testcases"]
        oldtestcases = ProblemTestCases.query.filter_by(questionID = problem.id).all()
        for old in oldtestcases:
            db.session.delete(old)
        for i in tests:
            if i["input"] == "" or i["output"] == "":
                return ("ERROR: Empty Test Case")
            testcase = ProblemTestCases(\
                problem = problem,\
                input = i["input"],\
                output = i["output"],
            )
            db.session.add(testcase)
        db.session.commit()
        return ("Succesfully Updated Question")
    else:
        return ("Title Already Exists")