# code based off Miguel's tutorial 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

from flask import jsonify
from flask_login import current_user, login_required
from app import db
from app.api import bp
from app.api.auth import token_auth

@bp.route('/tokens', methods=['POST'])
@login_required
def get_token():
    token = current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204