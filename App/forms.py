from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed
from App.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is already taken.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is already taken.')



class LoginForm(FlaskForm):
    email_username = StringField('Email or Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is already taken.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is already taken.')


class SubjectForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Post')


class ChapterForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    subject_id = IntegerField('Subject Id', validators=[DataRequired()])
    submit = SubmitField('Post')


class QuestionForm(FlaskForm):
    subject_id = IntegerField('Subject Id', validators=[DataRequired()])
    chapter_id = IntegerField('Chapter Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Post')


