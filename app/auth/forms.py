# Reference: The Flask Mega-Tutorial Part III: Web Forms https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

# form for logging in an existing user
# adapted from Miguel's tutorial
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
        # check the two passwords are equal
        user1 = User.query.filter_by(username=self.username_email.data).first()
        user2 = User.query.filter_by(email=self.username_email.data).first()
        if user1 is not None and not user1.check_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        elif user2 is not None and not user2.check_password(self.password.data):
            self.password.errors.append('Incorrect password.')
            return False
        return True
            
# form for a new user to register with the app
# adapted from Miguel's tutorial
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

# form for a user to edit their own file
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    prefer_language= SelectField('Prefer Language',choices=[('cpp','C++'),('py','Python')],validators=[DataRequired()])
    submit = SubmitField('Change Profile')

# form for a user to reset their password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')