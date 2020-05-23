from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, index=True, nullable=False)
    points = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self,size):
        digest= md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'admin': self.admin,
            'points': self.points,
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'admin']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, index=True)
    urlTitle = db.Column(db.String(100))
    difficulty = db.Column(db.String(32), index=True)
    numAttempts = db.Column(db.Integer, default=0)
    numSuccesses = db.Column(db.Integer, default=0)
    body= db.Column(db.Text())
    timeLimit = db.Column(db.Integer)
    memoryLimit = db.Column(db.Integer)
    testCases = db.relationship('ProblemTestCases', backref="problem")

    def __repr__(self):
        return '<Problem {}>'.format(self.title)

class ProblemTestCases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('problem.id'))
    input= db.Column(db.Text())
    output= db.Column(db.Text())

    def __repr__(self):
        return '<Problem {}>'.format(self.title)