from flask.ext.login import logout_user, login_required, login_user
from flask import redirect, url_for, flash, render_template, request
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from app import app

from models import User


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    email = TextField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


@app.route("/logout")
# FIXME do login check manually?
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)

        if not user:
            flash('That didn\'t work :(. Never seen you before.')
            return render_template('login.html', form=form)

        if user.check_password(form.password.data, request) == False:
            flash('That didn\'t work :(. Check yo self.')
            return render_template('login.html', form=form)

        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("home"))

    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(form.email.data, form.password.data, True)
        user.save()
        flash('Signed up!')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)
