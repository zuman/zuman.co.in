import logging
from datetime import datetime as dt
from uuid import uuid4

from flask import abort, flash, request, session
from flask_login import current_user, logout_user

from zuman import db, appdata


def validate_session():
    if not current_user.is_authenticated:
        return
    if (current_user.sid != session.sid)\
            or ('HTTP_USER_AGENT' not in session)\
            or (session['HTTP_USER_AGENT'] != request.environ['HTTP_USER_AGENT']):

        logging.debug("> current_user.sid\t"+current_user.sid)
        logging.debug("> session.sid\t\t"+session.sid)
        logging.info(f"> extra-session-logout {current_user.username} ...")
        logout()
        flash("Login detected from another browser or device. 1", "danger")
        flash("Please login again to continue using the site here!", "danger")
        abort(409)


def set_session():
    session.sid = str(uuid4())
    current_user.sid = session.sid
    db.session.commit()
    session['HTTP_USER_AGENT'] = request.environ['HTTP_USER_AGENT']


def logout():
    session.clear()
    logout_user()


def create_str(object, exclude):
    ret = '{'
    for key, value in object.__dict__.items():
        if key in exclude:
            continue
        ret += f'"{key}":"{value}",'
    ret = ret[:-1] + '}'
    return ret
