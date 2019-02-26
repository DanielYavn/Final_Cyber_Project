from siteCode import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    games_downloaded = db.relationship('GameDownload', backref="user", lazy=True)

    def __repr__(self):
        return "User({0},{1})".format(self.username, self.email)


class GameDownload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Crypto_key = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # org game

    def __repr__(self):
        return "GameDownload({0},{1},{2})".format(self.id, self.date, self.user_id)
