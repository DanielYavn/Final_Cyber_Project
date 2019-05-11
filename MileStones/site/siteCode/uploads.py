from models import Game
from siteCode import db
import os

games_folder = "./siteCode/games/"


def upload_game(file, form, user):
    print "uploading"
    if form.days.data is None and form.hours.data is None and form.minutes.data is None:
        game = Game(name=form.name.data, description=form.description.data, uploader=user.id, cost=0)
    else:
        trile_time = trile_time_sec(form.days.data, form.hours.data, form.minutes.data)
        game = Game(name=form.name.data, description=form.description.data, uploader=user.id, date=trile_time, cost=0)

    user.games_uploaded.append(game)
    db.session.commit()

    game_id = game.id

    file.save(os.path.join(games_folder, str(game_id) + ".exe"))
    return True


def check_game(game_file):
    extension = game_file.filename.split(".")[1]
    if extension != "exe":
        return {"extension ": "game has to be exe type"}


def trile_time_sec(d=0, h=0, m=0):
    h += d * 24
    m += h * 60
    sec = m * 60
    return sec
