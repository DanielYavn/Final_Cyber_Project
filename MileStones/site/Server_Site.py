"""
dependencies: flask, flask_wtf
"""
from flask import Flask, render_template, url_for, flash, redirect

import forms

site = Flask(__name__)
site.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@site.route("/")
def home():
    return render_template("home.html")


@site.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationFrom()
    if form.validate_on_submit():
        flash("created account for {0}".format(form.username.data), "success")
        return redirect(url_for("home"))
    else:
        pass
    return render_template("register.html", form=form)


@site.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginFrom()
    if form.validate_on_submit():
        # validate password
        flash("logged in for {0}".format(form.email.data), "success")
        return redirect(url_for("home"))
    else:
        pass
    return render_template("login.html", form=form)


if __name__ == "__main__":
    site.run(debug=True)
