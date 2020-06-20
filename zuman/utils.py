from flask import request, session, flash, redirect, url_for, abort
from flask_login import logout_user


def validate_session():
    if 'HTTP_USER_AGENT' not in session:
        set_session()
    if session['HTTP_USER_AGENT'] != request.environ['HTTP_USER_AGENT'] or session['REMOTE_ADDR'] != request.environ['REMOTE_ADDR']:
        logout()
        abort(409)


def set_session():
    session['HTTP_USER_AGENT'] = request.environ['HTTP_USER_AGENT']
    session['REMOTE_ADDR'] = request.environ['REMOTE_ADDR']


def logout():
    session.clear()
    logout_user()
