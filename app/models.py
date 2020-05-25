from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from hashlib import md5
from datetime import datetime, timedelta, date
import base64, os

# Class for the user
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    prefLanguage = db.Column(db.String(10))
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, index=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    problemsCompleted = db.relationship('ProblemsCompleted', backref="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check password    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # generate avater
    def avatar(self,size):
        digest= md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # to dict
    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'points': self.points,
        }
        return data
    
    # from dict
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'admin']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # get token
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token
    
    # revoke token
    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    #check token
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

# load user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# class for Problems
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, index=True)
    urlTitle = db.Column(db.String(100), unique=True)
    difficulty = db.Column(db.Integer)
    numAttempts = db.Column(db.Integer, default=0)
    numSuccesses = db.Column(db.Integer, default=0)
    dateAdded = db.Column(db.String(10), default = date.today().strftime("%d/%m/%Y"))
    body= db.Column(db.Text())
    timeLimit = db.Column(db.Float)
    testCases = db.relationship('ProblemTestCases', backref="problem")
    problemsCompleted = db.relationship('ProblemsCompleted', backref="problem")

    def __repr__(self):
        return '<Problem {}>'.format(self.title)

    # to dict
    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'urlTitle': self.urlTitle,
            'difficulty': self.difficulty,
            'dateAdded': self.dateAdded
        }
        return data

# Class for problem test cases
class ProblemTestCases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('problem.id'))
    input= db.Column(db.Text())
    output= db.Column(db.Text())

    def __repr__(self):
        return '<Problem {}>'.format(self.title)

class ProblemsCompleted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('problem.id'))
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    success = db.Column(db.Boolean)
