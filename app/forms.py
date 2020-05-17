from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Problem, ProblemTestCases

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ProblemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=100)])
    body = TextAreaField('Description', validators=[DataRequired(), Length(min=0, max=9999)])
    timeLimit = IntegerField('Time Limit (s)', validators=[DataRequired()])
    memoryLimit = IntegerField('Memory Limit (MB)', validators=[DataRequired()])
    testCaseInput = TextAreaField('Test Case Input', validators=[DataRequired(), Length(min=0, max=9999)])
    testCaseOutput = TextAreaField('Test Case Output', validators=[DataRequired(), Length(min=0, max=9999)])
    submit = SubmitField('Add Problem')

    def validate_title(self, title):
        problem = Problem.query.filter_by(title=title.data).first()
        if problem is not None:
            raise  ValidationError('Please use a different title. This problem already exists!')

class ProblemSubmitForm(FlaskForm):
    language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python')]) 
    code = TextAreaField('Code', validators=[DataRequired(), Length(min=0, max=99999)])
    submit = SubmitField('Submit Solution')