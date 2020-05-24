from flask import jsonify
from app import db
from app.api import bp
from app.models import Problem, ProblemTestCases
from app.api.errors import bad_request, error_response
from app.api.auth import token_auth

@bp.route('/problems/<urltitle>', methods=['GET'])
def get_problem(urltitle):
    pass

@bp.route('/problems', methods=['GET'])
@token_auth.login_required(role='admin')
def get_problems():
    problems = [problem.to_dict() for problem in Problem.query.all()]
    return jsonify({'problemList': problems})

@bp.route('/problems/<urltitle>', methods=['DELETE'])
@token_auth.login_required(role='admin')
def remove_problem(urltitle):
    p = Problem.query.filter_by(urlTitle=urltitle).first()
    if p is None:
        return bad_request()
    testcases = ProblemTestCases.query.filter_by(questionID=p.id).all()
    for test in testcases:
        db.session.delete(test)
    info = p.to_dict()
    db.session.delete(p)
    db.session.commit()
    return jsonify(info)