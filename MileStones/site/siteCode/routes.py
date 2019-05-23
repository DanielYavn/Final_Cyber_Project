from flask import render_template, url_for, flash, redirect, request, send_file
import forms
from tables import MyGamesTable, AllGamesTable
from uploads import upload_game, update_my_game
from models import Game, User, GameDownload, search_games_downloaded, search_games, search_uploaded_games
from siteCode import app, bcrypt, db, blocker_prep
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from other_functions import download_and_remove
from sqlalchemy import update


@app.route("/", methods=["GET", "POST"])
def home():
    page = request.args.get('page', 1, type=int)
    prev_search = request.args.get('prev_search', "", type=str)
    search = forms.SearchForm()

    if request.method == 'POST':
        return redirect(url_for('home', page=page, prev_search=search.search_bar.data))

    if prev_search:
        search.search_bar.data = prev_search
        games = search_games(prev_search, page)
    else:
        games = search_games("", page)
    return render_template("home.html", form=search, games=games)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationFrom()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("created account for {0}".format(form.username.data), "is-success")
        login_user(new_user)
        return redirect(url_for("home"))
    else:
        pass
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("logged in for {0}".format(form.email.data), "is-success")
            return redirect(url_for("home"))
        else:
            flash("log in for {0} was unsucsesfull".format(form.email.data), "is-danger")
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
        flash("you are not loggd in", "is-danger")
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
        flash("you are not loggd in", "is-danger")
        redirect(url_for("home"))

    game_type_id = GameDownload.query.filter_by(id=gameId).first().game_id
    for game in current_user.games_downloaded:
        if game.game_id == game_type_id:
            game.date = None
    db.session.commit()
    flash("game bought successfully", "is-success")
    return redirect(url_for("home"))


@app.route("/my_games", methods=['GET', 'POST'])
def my_games():
    page = request.args.get('page', 1, type=int)
    prev_search = request.args.get('prev_search', "", type=str)
    if current_user.is_authenticated:
        search = forms.SearchForm()
        if request.method == 'POST':
            return redirect(url_for('my_games', page=page, prev_search=search.search_bar.data))
        if prev_search:
            search.search_bar.data = prev_search
            games = search_games_downloaded(prev_search, user=current_user, page=page)
        else:
            games = search_games_downloaded("", user=current_user, page=page)

        return render_template("my_games.html", form=search, games=games, utcnow=datetime.utcnow())

    else:
        flash("you have to login", "is-danger")
        return redirect(url_for("home"))


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = forms.UploadForm()
    if request.method == 'POST':  # and form.validate_on_submit():
        if 'game_file' not in request.files:
            flash('No file part', "is-danger")
            return redirect(request.url)
        file = request.files['game_file']

        if file.filename == '':
            flash('No selected file', "is-danger")
        if upload_game(file, form, current_user):
            flash("uploaded Successfully", "is-success")
            return redirect(url_for("home"))

    return render_template("upload.html", form=form)


@app.route("/download_check_game/<int:gameId>")
def download_check_game(gameId):
    if current_user.is_authenticated:
        game = Game.queue.get(gameId)
        if current_user.id == game.uploader.id:
            ready_blocker, gamename = blocker_prep.create_new_blocker_no_enc(current_user, gameId)
            # ready_blocker=blocker_prep.create_new_blocker_no_enc(current_user,game_id)

            return download_and_remove(ready_blocker, gamename + ".exe")
            # return send_from_directory(directory=path_to_dir, filename=filename, as_attachment=True)
    else:
        flash("you are not loggd in", "is-danger")
    return redirect(url_for("home"))


@app.route("/gamePage:<int:gameId>")
def game_page(gameId):
    # if game is user's give more buttons
    games = Game.query.filter_by(id=gameId).all()
    if len(games) > 0:

        return render_template("game_page.html", game=games[0])
    else:
        return "no game found"


@app.route("/my_uploads")
def my_uploads():
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        prev_search = request.args.get('prev_search', "", type=str)

        search = forms.SearchForm()
        if request.method == 'POST':
            return redirect(url_for('my_uploads', page=page, prev_search=search.search_bar.data))
        if prev_search:
            search.search_bar.data = prev_search
            games = search_uploaded_games(prev_search, current_user, page)
        else:
            games = search_uploaded_games("", current_user, page)
        return render_template("my_uploads.html", form=search, games=games)
    return "you must login"


@app.route("/remove_game/<int:gameId>")
def remove_game(gameId):
    print "remove"
    if current_user.is_authenticated:
        game = Game.query.filter_by(id=gameId).first()
        uploader = game.uploader
        if current_user.id == uploader:
            game.removed = True
            db.session.commit()
            flash("removed Successfully", "is-success")
        else:
            flash("you have to be the uploader of the game", "is-danger")
    else:
        flash("you have to login", "is-danger")

    return redirect("my_uploads")


@app.route("/unremove_game/<int:gameId>")
def unremove_game(gameId):
    print "undo"
    if current_user.is_authenticated:
        game = Game.query.get(gameId)
        uploader = game.uploader
        if current_user.id == uploader:
            game.removed = False
            db.session.commit()
            flash("returned Successfully", "is-success")
        else:
            flash("you have to be the uploader of the game", "is-danger")
    else:
        flash("you have to login", "is-danger")

    return redirect("my_uploads")


@app.route("/update_game/<int:gameId>", methods=["GET", "POST"])
def update_game(gameId):
    if current_user.is_authenticated:

        game = Game.query.get(gameId)
        uploader = game.uploader
        if current_user.id == uploader:
            form = forms.UpdateForm(game)
            if request.method == "GET":
                form.fill_form()
                return render_template("update.html", form=form)

            if request.method == "POST":
                if 'game_file' in request.files:
                    file = request.files['game_file']
                    if file.filename != '':
                        if update_my_game(game, file, form):
                            flash("uploaded Successfully", "is-success")
                            return redirect(url_for("uploaded_games"))
            update_my_game(game, None, form)
            return redirect(url_for("my_uploads"))
    return redirect(url_for("home", gameId=gameId))
