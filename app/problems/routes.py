from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from app import db
from app.problems import bp
from app.models import Problem, ProblemTestCases
from app.helperFunctions import pandoc
from app.problems.judge import judge, cleanUp, Question, testCase

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
    if request.method == 'POST':
        data = request.get_json()
    problem = Problem.query.filter_by(urlTitle=data['urlTitle']).first()
    testCases = ProblemTestCases.query.filter_by(questionID = problem.id).all()
    question = Question(problem.id, data['language'], data['code'], problem.timeLimit)
    for test in testCases:
        question.testCases.append(testCase(test.input.split("\n"), test.output.split("\n")))
    output = judge(question)
    return jsonify(output)
