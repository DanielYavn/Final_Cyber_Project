from siteCode import db, login_manager, free_secounds
from flask_login import UserMixin
from datetime import datetime, timedelta


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def trile_end_time(self):
    return datetime.utcnow() + timedelta(seconds=free_secounds)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    games_downloaded = db.relationship('GameDownload', backref="user")
    games_uploaded = db.relationship('Game', backref="user")

    def __repr__(self):
        return "User({0},{1})".format(self.username, self.email)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    description = db.Column(db.Text, default="")


    # categort
    # rating
    # pictuer

    uploader = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    games_downloaded = db.relationship('GameDownload', backref="game")  # lazy=True

    def __repr__(self):
        return "Game({0},{1})".format(self.id, self.name)


class GameDownload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True, default=trile_end_time)
    Crypto_key = db.Column(db.String(100), nullable=False)
    Crypto_iv = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    def __repr__(self):
        return "GameDownload({0},{1},{2})".format(self.id, self.date, self.user_id)


def serch_games_downloaded(search, user):
    if not search:
        return GameDownload.query.filter_by(user_id=user.id).all()
    return GameDownload.query.filter_by(user_id=user.id).join(Game).filter(Game.name.ilike("%{}%".format(search))).all()
