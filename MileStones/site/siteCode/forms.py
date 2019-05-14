from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, \
    DecimalField
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

    def validate_game_file(self, field):
        extension = field.data.filename.split(".")[1]
        if extension != "exe":
            raise ValidationError('game has to be a exe file')

    def validate_price(self, field):
        price = field.data
        if price is not None:
            try:
                f_price = float(price)
            except ValueError:
                print "err"
                raise ValidationError("has to be float")
            if price < 0.0:
                print "err"
                raise ValidationError("has to be a positive float")

    def to_float(x):
        print "-",x
        if x is None:
            return x
        return float(x)

    name = StringField("game name")#, validators=[DataRequired()])
    game_file = FileField("your game")#, validators=[DataRequired()])
    upload = SubmitField("upload")
    description = TextAreaField("description")
    days = IntegerField("days")
    hours = IntegerField("hours")
    minutes = IntegerField("minutes")
    price = StringField("price",filters=[to_float])#, validators=[validate_price], )
