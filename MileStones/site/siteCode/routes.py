from flask import render_template, url_for, flash, redirect, send_file
from forms import RegistrationFrom, LoginFrom
from models import User, GameDownload
from siteCode import app, bcrypt, db, blocker_prep
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from other_functions import download_and_remove
from sqlalchemy import update


@app.route("/")
def home():
    return render_template("home.html")


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


@app.route("/download_game")
def download_game():
    if current_user.is_authenticated:
        game_id = 1
        #ready_blocker = blocker_prep.create_new_blocker(current_user, game_id)
        ready_blocker=blocker_prep.create_new_blocker_no_enc(current_user,game_id)

        return download_and_remove(ready_blocker, "game.exe")
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
    if game.date != None:
        if datetime.utcnow() > game.date:
            print "time passed by ", datetime.utcnow() - game.date
            return ""
    return game.Crypto_key + "\n" + game.Crypto_iv


@app.route("/buy_game")
def buy_game():
    GameDownload.query.order_by('-id').first().date = None
    db.session.commit()
    flash("game bought successfully", "success")
    return redirect(url_for("home"))
