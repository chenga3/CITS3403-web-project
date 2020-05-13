from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username_email = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username_email(self, username_email):
        user1 = User.query.filter_by(username=username_email.data).first()
        user2 = User.query.filter_by(email=username_email.data).first()
        if user1 is None and user2 is None:
            raise ValidationError('Incorrect username or email.')

    def validate(self):
        response = FlaskForm.validate(self)
        if not response:
            return False
        user1 = User.query.filter_by(username=self.username_email.data).first()
        user2 = User.query.filter_by(email=self.username_email.data).first()
        if user1 is not None and not user1.check_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        elif user2 is not None and not user2.check_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        return True
            

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