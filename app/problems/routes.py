from flask import render_template, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.problems import bp
from app.models import Problem, ProblemTestCases, User
from app.helperFunctions import pandoc
from app.problems.judge import judge, cleanUp, Question, testCase
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response
from redis import Redis
import rq

@bp.route('/problems')
def problems():
    problems = Problem.query.all()
    return render_template('problems/problems.html', title='Problems', problems=problems)

@bp.route('/problem/<title>')
@login_required
def problem(title):
    problem = Problem.query.filter_by(urlTitle=title).first()
    if problem is None:
        return redirect(url_for("problems"))
    return render_template('problems/problem.html', problem=problem, body=pandoc(problem.body))

@bp.route('/judge', methods=['POST'])
# @token_auth.login_required
@login_required
def judgeSolution():
    if current_user.is_authenticated:
        data = request.get_json()
        if data["code"] == "":
            return jsonify({"error": "Empty Submission"})
        problem = Problem.query.filter_by(urlTitle=data['urlTitle']).first()
        testCases = ProblemTestCases.query.filter_by(questionID = problem.id).all()
        question = Question(problem.id, data['language'], data['code'], problem.timeLimit)
        for test in testCases:
            question.testCases.append(testCase(test.input.split("\n"), test.output.split("\n")))
        job = current_app.task_queue.enqueue(judge,question)
        while job.result == None:
            pass
        output = job.result
        user = User.query.filter_by(id=current_user.id).first()
        if output["pass"] == "yes":
            user.points += int(problem.difficulty) + 1
            problem.numSuccesses += 1
        problem.numAttempts += 1
        db.session.commit()
        return jsonify(output)
    else:
        return jsonify({"error": "You need to login to submit code"})
