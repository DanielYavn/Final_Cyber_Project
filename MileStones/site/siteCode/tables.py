from flask_table import Table, Col, LinkCol, BoolCol, DateCol
from flask import url_for
from models import Game


class MyGamesTable(Table):
    def __init__(self, games, **kwargs):
        game_dicts = []
        for game in games:
            game_dicts.append(
                {"is_bought": not game.date,
                 "cost": game.game.cost,
                 "game_name": game.game.name,
                 "game_id": game.id
                 })
        Table.__init__(self, game_dicts, **kwargs)

    game_name = Col("game name")
    cost = Col("cost")
    is_bought = BoolCol("bout")
    buy_link = LinkCol("Buy", "buy_game", url_kwargs=dict(gameId='game_id'))

    def __repr__(self):
        return "MyGamesTable object"


class AllGamesTable(Table):
    def __init__(self, games, **kwargs):
        game_dicts = []
        for game in games:
            game_dicts.append(
                {"game_name": game.name,
                 "creator": game.user.username,
                 "rating": game.convert_rating(game.rating),
                 "upload_date": game.upload_date.date(),
                 "game_id": game.id})
        Table.__init__(self, game_dicts, **kwargs)

    # game_id = Col("id", show=False)
    game_name = Col("game name")
    creator = Col("Creator")
    rating = Col("Rating")
    upload_date = DateCol("upload date", date_format="d.M.Y")
    download_link = LinkCol("download here", "download_game", url_kwargs=dict(gameId='game_id'))

    def __repr__(self):
        return "MyGamesTable object"
