from flask import jsonify, render_template
from app import db
from app.api import bp
from app.api.errors import bad_request, error_response
from app.api.auth import token_auth
from app.models import User

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required(role='admin')
def get_user(id):
    return jsonify(User.query.get(id).to_dict())

@bp.route('/users', methods=['GET'])
@token_auth.login_required(role='admin')
def get_users():
    users = [user.to_dict() for user in User.query.all()]
    return jsonify({'userList': users})

@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required(role='admin')
def remove_user(id):
    u = User.query.get(id)
    if u is None:
        return bad_request('User does not exist')
    db.session.delete(u)
    db.session.commit()
    users = [user.to_dict() for user in User.query.all()]
    return jsonify({'userList': users})