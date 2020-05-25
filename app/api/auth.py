# code based off Miguel's tutorial 
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

from flask_httpauth import HTTPTokenAuth
from app.models import User
from app.api.errors import error_response

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

# for further privileged token auth
@token_auth.get_user_roles
def get_user_roles(user):
    if user.admin:
        return 'admin'
    else:
        return 'user'