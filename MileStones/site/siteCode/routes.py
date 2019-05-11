from flask import render_template, url_for, flash, redirect, request, send_file
from forms import RegistrationFrom, LoginFrom, SearchForm, UploadForm  # , GameForm
from tables import MyGamesTable, AllGamesTable
from uploads import upload_game
from models import Game, User, GameDownload, search_games_downloaded, search_games
from siteCode import app, bcrypt, db, blocker_prep
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from other_functions import download_and_remove
from sqlalchemy import update


@app.route("/", methods=["GET", "POST"])
def home():
    search = SearchForm()
    if request.method == 'POST':
        games = search_games(search.search_bar.data)
    else:
        games = search_games("")

    table = AllGamesTable(games)
    return render_template("home.html", form=search, all_games_table=table)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("created account for {0}".format(form.username.data), "success")
        return redirect(url_for("home"))
    else:
        pass
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("logged in for {0}".format(form.email.data), "success")
            return redirect(url_for("home"))
        else:
            flash("log in for {0} was unsucsesfull".format(form.email.data), "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/download_game/<int:gameId>")
def download_game(gameId):
    if current_user.is_authenticated:
        ready_blocker, gamename = blocker_prep.create_new_blocker(current_user, gameId)
        # ready_blocker=blocker_prep.create_new_blocker_no_enc(current_user,game_id)

        return download_and_remove(ready_blocker, gamename + ".exe")
        # return send_from_directory(directory=path_to_dir, filename=filename, as_attachment=True)

    else:
        flash("you are not loggd in", "danger")
    return redirect(url_for("home"))


@app.route("/run_permission/<int:gameId>")
def run_permission(gameId):
    print "requested game id: ", gameId
    try:
        game = GameDownload.query.filter_by(id=gameId).first()
    except AttributeError:
        print "failed to find game"
        return ""
    print game.date
    if game.date is not None:
        if datetime.utcnow() > game.date:
            print "time passed by ", datetime.utcnow() - game.date
            return ""
    return game.Crypto_key + "\n" + game.Crypto_iv


@app.route("/buy_game/<int:gameId>")
def buy_game(gameId):
    if not current_user.is_authenticated:
        flash("you are not loggd in", "danger")
        redirect(url_for("home"))

    game_type_id = GameDownload.query.filter_by(id=gameId).first().game_id
    for game in current_user.games_downloaded:
        if game.game_id == game_type_id:
            game.date = None
    db.session.commit()
    flash("game bought successfully", "success")
    return redirect(url_for("home"))


@app.route("/my_games", methods=['GET', 'POST'])
def my_games():
    if current_user.is_authenticated:
        search = SearchForm()
        if request.method == 'POST':
            games = search_games_downloaded(search.search_bar.data, current_user)
        else:
            games = search_games_downloaded("", current_user)

        table = MyGamesTable(games)

        return render_template("my_games.html", form=search, table=table)

    else:
        flash("you have to login", "danger")


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    print request.method
    if request.method == 'POST':  # and form.validate_on_submit():
        # check if the post request has the file part
        if 'game_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['game_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        # check file
        print "trying"
        if upload_game(file, form, current_user):
            flash("Sucsess")

    return render_template("upload.html", form=form)


@app.route("/gamePage:<int:gameId>")
def game_page(gameId):
    # if game is user's give more buttons
    games = Game.query.filter_by(id=gameId).all()
    if len(games) > 0:

        return render_template("game_page.html", game=games[0])
    else:
        return "no game founde"


@app.route("/my_uploads")
def my_uploads():
    pass


@app.route("/profile", methods=["GET", "POST"])
def profile():
    pass
