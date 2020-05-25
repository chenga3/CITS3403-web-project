from flask import render_template, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.problems import bp
from app.models import Problem, ProblemTestCases, User, ProblemsCompleted
from app.helperFunctions import pandoc
from app.problems.judge import judge, cleanUp, Question, testCase
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response
from redis import Redis
import rq

# Problems page
@bp.route('/problems')
def problems():
    problems = Problem.query.all()
    status = {}
    if current_user.is_active:
        problemscompleted = ProblemsCompleted.query.filter_by(userID=current_user.id)
        for pc in problemscompleted:
            status[pc.questionID] = pc.success
    return render_template('problems/problems.html', title='Problems',
                            problems=problems, status=status)

# Individual Problem page
@bp.route('/problem/<title>')
@login_required
def problem(title):
    problem = Problem.query.filter_by(urlTitle=title).first()
    if problem is None:
        return redirect(url_for("problems"))
    return render_template('problems/problem.html', problem=problem, body=pandoc(problem.body))



# API to judge submission
@bp.route('/judge', methods=['POST'])
@login_required
def judgeSolution():
    # check if current user is authenticated
    if current_user.is_authenticated:
        data = request.get_json()

        # Check for valid inputs
        if data["code"] == "":
            return jsonify({"error": "Empty Submission"})
        problem = Problem.query.filter_by(urlTitle=data['urlTitle']).first()
        testCases = ProblemTestCases.query.filter_by(questionID = problem.id).all()
        question = Question(problem.id, data['language'], data['code'], problem.timeLimit)
        for test in testCases:
            question.testCases.append(testCase(test.input.split("\n"), test.output.split("\n")))

        # queue task in redis queue
        job = current_app.task_queue.enqueue(judge,question)
        while job.result == None:
            pass
        output = job.result

        # get user
        user = User.query.filter_by(id=current_user.id).first()
        pc = ProblemsCompleted.query.filter_by(questionID=problem.id, userID=user.id).first()
        if pc is not None:
            db.session.delete(pc)
        # update relavant stats
        if output["pass"] == "yes":
            newpc = ProblemsCompleted(problem=problem, user=user, success=True)
            user.points += int(problem.difficulty) + 1
            problem.numSuccesses += 1
        else:
            newpc = ProblemsCompleted(problem=problem, user=user, success=False)
        problem.numAttempts += 1
        db.session.add(newpc)
        db.session.commit()
        return jsonify(output)
    else:
        # error
        return jsonify({"error": "You need to login to submit code"})
