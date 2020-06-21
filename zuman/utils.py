from flask import request, session, flash, redirect, url_for, abort
from flask_login import current_user, logout_user
from zuman import appdata


def validate_session():
    if 'HTTP_USER_AGENT' not in session:
        set_session()
    if current_user.is_authenticated and (current_user.id not in appdata['user_sessions']):
        appdata['user_sessions'][current_user.id] = session.sid
    if (current_user.is_authenticated and (appdata['user_sessions'][current_user.id] != session.sid)) or session['HTTP_USER_AGENT'] != request.environ['HTTP_USER_AGENT']:
        logout()
        flash("Login detected from another browser or device.", "danger")
        flash("Please login again to continue using the site here!", "danger")
        abort(409)


def set_session():
    session['HTTP_USER_AGENT'] = request.environ['HTTP_USER_AGENT']


def logout():
    session.clear()
    logout_user()
