from flask import jsonify, render_template
from app.api import bp
from app.models import User

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get(id).to_dict())

@bp.route('/users', methods=['GET'])
def get_users():
    u = User.query.all()
    users = [user.to_dict() for user in User.query.all()]
    print(users)
    return jsonify({'userList': users})