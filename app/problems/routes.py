from flask import render_template, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.problems import bp
from app.models import Problem, ProblemTestCases
from app.helperFunctions import pandoc
from app.problems.judge import judge, cleanUp, Question, testCase
from redis import Redis
import rq

@bp.route('/problems')
def problems():
    problems = Problem.query.all()
    return render_template('problems/problems.html', title='Problems', problems=problems)

@bp.route('/problem/<title>')
def problem(title):
    problem = Problem.query.filter_by(urlTitle=title).first()
    if problem is None:
        return redirect(url_for("problems"))
    return render_template('problems/problem.html', problem=problem, body=pandoc(problem.body))

@bp.route('/judge', methods=['POST'])
def judgeSolution():
    data = request.get_json()
    if data["code"] == "":
        return jsonify({"error": "Empty Submission"})
    problem = Problem.query.filter_by(urlTitle=data['urlTitle']).first()
    testCases = ProblemTestCases.query.filter_by(questionID = problem.id).all()
    question = Question(problem.id, data['language'], data['code'], problem.timeLimit)
    print(question)
    for test in testCases:
        question.testCases.append(testCase(test.input.split("\n"), test.output.split("\n")))
    job = current_app.task_queue.enqueue(judge,question)
    while job.result == None:
        pass
    output = job.result
    if output["pass"] == "yes":
        problem.numSuccesses += 1
    problem.numAttempts += 1
    db.session.commit()

    return jsonify(output)
