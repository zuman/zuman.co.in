from flask import request, session, flash, redirect, url_for, abort
from flask_login import current_user, logout_user
from zuman import appdata
import uuid
import logging
from datetime import datetime as dt

def validate_session():
    if not current_user.is_authenticated:
        return
    if current_user.id not in appdata['user_sessions']:
        appdata['user_sessions'][current_user.id] = session.sid
    if (appdata['user_sessions'][current_user.id] != session.sid)\
            or ('HTTP_USER_AGENT' not in session)\
            or (session['HTTP_USER_AGENT'] != request.environ['HTTP_USER_AGENT']):
            
        logging.warning("\n\n\n\n> "+str(appdata['token']))
        logging.warning('\n---------------Inside condition------------'+str(dt.now()))
        try:
            logging.warning('---------------Condition 1')
            logging.warning(">"+str(type((appdata['user_sessions'][current_user.id] != session.sid))))
            logging.warning(">\n"+appdata['user_sessions'][current_user.id]+"\n"+session.sid)
            logging.warning(">"+str(appdata['user_sessions'][current_user.id] != session.sid))
        except Exception as e:
            logging.error(e)
        try:
            logging.warning('---------------Condition 2')
            logging.warning(">"+str('HTTP_USER_AGENT' not in session))
        except Exception as e:
            logging.error(e)
        try:
            logging.warning('---------------Condition 3')
            logging.warning(">"+str(type((session['HTTP_USER_AGENT'] != request.environ['HTTP_USER_AGENT']))))
            logging.warning(">\n"+session['HTTP_USER_AGENT']+"\n"+request.environ['HTTP_USER_AGENT'])
            logging.warning(">"+str(session['HTTP_USER_AGENT'] != request.environ['HTTP_USER_AGENT']))
        except Exception as e:
            logging.error(e)
        logout()
        flash("Login detected from another browser or device. 1", "danger")
        flash("Please login again to continue using the site here!", "danger")
        abort(409)


def set_session():
    logging.warning("\n\n> "+str(appdata['token']))
    session.sid = str(uuid.uuid4())
    appdata['user_sessions'][current_user.id] = session.sid
    logging.warning("\n> "+str(appdata['user_sessions']))
    session['HTTP_USER_AGENT'] = request.environ['HTTP_USER_AGENT']
    logging.warning(">\n"+session['HTTP_USER_AGENT'])


def logout():
    session.clear()
    logout_user()
