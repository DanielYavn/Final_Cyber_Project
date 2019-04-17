from models import Game
from siteCode import db
import os

games_folder = "./siteCode/games/"


def upload_game(file, form, user):
    # check game
    print "uploading"
    game = Game(name=form.name.data, description="", uploader=user.id)
    user.games_uploaded.append(game)
    db.session.commit()

    game_id = game.id

    file.save(os.path.join(games_folder, str(game_id)+".exe"))
