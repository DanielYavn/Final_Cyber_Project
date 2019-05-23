from siteCode import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta

free_secounds = 60


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def trile_end_time(self):
    user = User.query.filter_by(id=self.get_current_parameters()["user_id"]).first()
    current_game = Game.query.filter_by(id=self.get_current_parameters()["game_id"]).first()
    for game_downloaded in user.games_downloaded:
        if game_downloaded.game is current_game:
            return game_downloaded.date


    trile_time = current_game.trile_time
    return datetime.utcnow() + timedelta(seconds=trile_time)


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
    cost = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, default="")

    trile_time = db.Column(db.Integer, default=free_secounds)  # in secounds

    rating = db.Column(db.Integer, default=None)

    uploader = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    games_downloaded = db.relationship('GameDownload', backref="game")  # lazy=True

    removed = db.Column(db.Boolean, default=False)

    downloads = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "Game(id:{0}, name4:{1}, cost:{2}, removed:{3})".format(self.id, self.name, self.cost, self.removed)

    def convert_rating(self, rating):
        if rating is None:
            return "No votes"
        return str(rating)


class GameDownload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True, default=trile_end_time)
    Crypto_key = db.Column(db.String(100), nullable=False)
    Crypto_iv = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    def __repr__(self):
        return "GameDownload({0},{1},{2})".format(self.id, self.date, self.user_id)


def search_games_downloaded(search, user, page, per_page=20):
    if not search:
        games = GameDownload.query.filter_by(user_id=user.id)
    else:
        games = GameDownload.query.filter_by(user_id=user.id).join(Game).filter(Game.name.ilike("%{}%".format(search)))
    games = games.group_by(GameDownload.game_id)
    n = games.count()
    max_page = int(n / per_page) + (n % per_page > 0)
    if max_page == 0:
        max_page = 1
    if max_page < page:
        page = max_page
    return games.paginate(page=page, per_page=per_page)


def search_games(search, page, per_page=20):
    games = Game.query.filter_by(removed=False)
    if search:
        games = games.filter(Game.name.ilike("%{}%".format(search)))
    n = games.count()
    max_page = int(n / per_page) + (n % per_page > 0)
    if max_page == 0:
        max_page = 1
    if max_page < page:
        page = max_page

    return games.paginate(page=page, per_page=per_page)


def search_uploaded_games(search, user, page, per_page=20):
    games = Game.query.filter_by(uploader=user.id)
    if search:
        games = games.filter(Game.name.ilike("%{}%".format(search)))
    n = games.count()
    max_page = int(n / per_page) + (n % per_page > 0)
    if max_page == 0:
        max_page = 1
    if max_page < page:
        page = max_page

    return games.paginate(page=page, per_page=per_page)
