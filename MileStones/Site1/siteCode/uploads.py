from models import Game
from siteCode import db
import os
from datetime import datetime
from PIL import Image

games_folder = "./siteCode/games/"
img_folder = "./siteCode/static/games_img/"


def upload_game(game_file, form, user):
    """
    uploads game and manages db
    :param game_file: game file
    :param form: form
    :param user: user object
    :return: True for success
    """
    args = {}

    if len(form.price.data) > 0:
        args['cost'] = float(form.price.data)
    if not (form.days.data is None and form.hours.data is None and form.minutes.data is None):
        args["trile_time"] = trile_time_sec(form.days.data, form.hours.data, form.minutes.data)
    game = Game(name=form.name.data, description=form.description.data, uploader=user.id, image="unknown", **args)

    user.games_uploaded.append(game)
    db.session.commit()
    game_id = game.id
    image_path = os.path.join(img_folder, str(game_id) + ".png")
    game_path = os.path.join(games_folder, str(game_id) + ".exe")

    game.image = "games_img/" + str(game_id) + ".png"
    db.session.commit()

    game_file.save(game_path)
    save_resized_image(form.img_file.data, image_path)

    return True


def save_resized_image(form_img, path):
    output_size = (125, 125)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(path)


def check_game(game_file):
    extension = game_file.filename.split(".")[1]
    if extension != "exe":
        return {"extension ": "game has to be exe type"}


def trile_time_sec(d=0, h=0, m=0):
    if h is None: h = 0
    if d is None: d = 0
    if m is None: m = 0
    h += d * 24
    m += h * 60
    sec = m * 60
    return sec


def update_my_game(game, file, form):
    """
    update game
    :param game: game file
    :param file: image file
    :param form: form
    :return: True for success
    """
    if form.price.data > 0:
        game.cost = float(form.price.data)
    if not (form.days.data is None and form.hours.data is None and form.minutes.data is None):
        game.trile_time = trile_time_sec(form.days.data, form.hours.data, form.minutes.data)

    game.name = form.name.data
    game.description = form.description.data


    game_id = game.id

    if file is not None:
        file.save(os.path.join(games_folder, str(game_id) + ".exe"))
        game.last_update = datetime.now()
    db.session.commit()
    return True
