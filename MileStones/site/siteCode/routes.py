from flask import render_template, url_for, flash, redirect
from forms import RegistrationFrom, LoginFrom
from siteCode import app


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        flash("created account for {0}".format(form.username.data), "success")
        return redirect(url_for("home"))
    else:
        pass
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        # validate password
        flash("logged in for {0}".format(form.email.data), "success")
        return redirect(url_for("home"))
    else:
        pass
    return render_template("login.html", form=form)
