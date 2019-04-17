from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, Length, Email, ValidationError
from models import User


class RegistrationFrom(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("username is taken")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("email is taken")


class LoginFrom(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("keep me loggd in")
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    search_bar = StringField('search')
    submit = SubmitField('Search')


class UploadForm(FlaskForm):
    name = StringField("game name", validators=[DataRequired()])
    game_file = FileField("your game")#, validators=[DataRequired()])
    upload = SubmitField("upload")
