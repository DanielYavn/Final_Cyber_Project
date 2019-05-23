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
    search_bar = StringField('search', render_kw={"placeholder": "Search here"})
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

    name = StringField("game name", render_kw={"placeholder": "Game Name"})  # , validators=[DataRequired()])
    game_file = FileField("your game")  # , validators=[DataRequired()])
    description = TextAreaField("description", render_kw={"placeholder": "Please add a description"})
    days = IntegerField("days", render_kw={"placeholder": "days"})
    hours = IntegerField("hours", render_kw={"placeholder": "hours"})
    minutes = IntegerField("minutes", render_kw={"placeholder": "minutes"})
    price = StringField("price", render_kw={"placeholder": "Price"})  # , validators=[validate_price], )

    upload = SubmitField("upload")


class UpdateForm(UploadForm):
    def __init__(self, game):
        self.game=game
        UploadForm.__init__(self)

    def fill_form(self):
        self.name.data = self.game.name
        self.description.data = self.game.description
        self.price.data = self.game.cost
        self.days.data, self.hours.data, self.minutes.data = self.break_trile_time(self.game.trile_time)

    def break_trile_time(self, t):
        d = t // (24 * 60 * 60)
        t %= (24 * 60 * 60)
        h = t // (60 * 60)
        t %= (60 * 60)
        m = t // 60
        return d, h, m

    upload = SubmitField("Update")
