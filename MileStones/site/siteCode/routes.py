from flask import render_template, url_for, flash, redirect, request, send_file
import forms
from uploads import upload_game, update_my_game
from models import Game, User, GameDownload, search_games_downloaded, search_games, search_uploaded_games
from siteCode import app, bcrypt, db, blocker_prep
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from other_functions import download_and_remove



@app.route("/", methods=["GET", "POST"])
def home():
    """
    show home page.
    :return: home page html
    """
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
    """
    register page.
    :return: register page html or redirect to home
    """
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
    """
    login page.
    :return: login page html or redirect to home

    """
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
    """
    logout user.
    :return: redirect to home page.
    """
    logout_user()
    return redirect(url_for("home"))


@app.route("/download_game/<int:gameId>")
def download_game(gameId):
    """
    downlowds the requested game.
    :param gameId: the id of the game
    :return: redirect to home page.
    """
    if current_user.is_authenticated:
        ready_blocker, gamename = blocker_prep.create_new_blocker(current_user, gameId)
        # ready_blocker=blocker_prep.create_new_blocker_no_enc(current_user,game_id)

        return download_and_remove(ready_blocker, gamename + ".exe")
        # return send_from_directory(directory=path_to_dir, filename=filename, as_attachment=True)

    else:
        flash("you are not logged in", "is-danger")
    return redirect(url_for("home"))


@app.route("/run_permission/<int:gameId>")
def run_permission(gameId):
    """
    checks sends keys to blocker.
    :param gameId: the id of the game
    :return: crypto keys or empty string
    """
    try:
        game = GameDownload.query.filter_by(id=gameId).first()
    except AttributeError:
        return ""

    if game.date is not None:  # game is not bought
        if datetime.utcnow() > game.date:
            return ""
    return game.Crypto_key + "\n" + game.Crypto_iv


@app.route("/buy_game/<int:gameId>")
def buy_game(gameId):
    """
    buyes game requested
    :param gameId:  the id of the game
    :return: redirect to home page.
    """
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
    """
    shows all games downloaded by the user
    :return:  my games page html or redirect to home page
    """
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
    """
    uploads game
    :return: redirect to home page
    """
    form = forms.UploadForm()
    if request.method == 'POST':  # and form.validate_on_submit():
        if 'game_file' not in request.files:
            flash('you did not upload the game', "is-danger")
            return redirect(request.url)
        if 'img_file' not in request.files:
            flash('you did not upload the image', "is-danger")
            return redirect(request.url)
        game_file = request.files['game_file']
        image = request.files['img_file']

        if game_file.filename == '':
            flash('you did not upload the game', "is-danger")
            return redirect(request.url)
        if image.filename == '':
            flash('you did not upload the image', "is-danger")
            return redirect(request.url)
        if not image.filename.split(".")[-1] == "png":
            flash('image has to be .png type', "is-danger")
            return redirect(request.url)
        print form.img_file.data

        if upload_game(game_file, form, current_user):
            flash("uploaded Successfully", "is-success")
            return redirect(url_for("home"))

    return render_template("upload.html", form=form)


@app.route("/gamePage:<int:gameId>")
def game_page(gameId):
    """
    page with  all info about the game.
    :param gameId: the id of the game
    :return:
    """
    games = Game.query.filter_by(id=gameId).all()
    if len(games) > 0:
        return render_template("game_page.html", game=games[0])
    else:
        flash('could not find game', "is-danger")
    redirect(url_for("home"))


@app.route("/my_uploads")
def my_uploads():
    """
    page with  all of the users uploaded games.
    :return: uploads page html
    """
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
    """
    removes the game from the stor
    :param gameId: game id
    :return: redirect to my_uploads
    """
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
    """
    undoes removel of game.
    :param gameId: game id
    :return: redirect to my_uploads
    """
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
    """
    updates game
    :param gameId: game id
    :return: redirect to my_uploads or home
    """
    if current_user.is_authenticated:

        game = Game.query.get(gameId)
        uploader = game.uploader
        if current_user.id == uploader:
            form = forms.UpdateForm(game)
            if request.method == "GET":
                form.fill_form()
                return render_template("update.html", form=form)
            file = None
            if request.method == "POST":
                if 'game_file' in request.files:
                    file = request.files['game_file']
                    if file.filename == '':
                        file = None

            update_my_game(game, file, form)
            return redirect(url_for("my_uploads"))
    return redirect(url_for("home", gameId=gameId))
