import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from zuman import bcrypt, db, appdata
from zuman.models import User, default_pic
from zuman.users.forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from zuman.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    appdata["title"] = "Log In"
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(
                url_for("posts.inclause"))
        else:
            flash("Login Unsuccessful. Please check email and password",
                  "danger")
    return render_template("users/login.html", appdata=appdata, form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    appdata["title"] = "Register new account"
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! Please log in.",
              "info")
        return redirect(url_for("users.login"))
    return render_template("users/register.html", appdata=appdata, form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        old_pic = current_user.image_file
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        if old_pic != default_pic:
            old_pic = os.path.join(
                os.path.abspath(__file__ + "../../.."), 'static/profile_pics',
                old_pic)
            os.remove(old_pic)
        flash('Your account is updated', 'success')
        return redirect(url_for("users.account"))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    appdata["title"] = "Account"
    appdata['image_file'] = image_file
    return render_template("users/account.html", appdata=appdata, form=form)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email is sent with Password Reset link. Please check your Spam folder if you did not receive the email in your inbox.', 'info')
        return redirect(url_for('users.login'))
    appdata["title"] = "Reset Password"
    return render_template(
        'users/reset_request.html', appdata=appdata, form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Password updated successfully", "info")
        return redirect(url_for("users.login"))
    appdata["title"] = "Reset Password"
    return render_template('users/reset_token.html', appdata=appdata, form=form)
