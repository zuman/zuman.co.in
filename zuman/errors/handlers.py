from flask import Blueprint, render_template, flash
from zuman import appdata

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(403)
def error_403(error):
    appdata['title'] = '403'
    return render_template('errors/403.html', appdata=appdata), 403


@errors.app_errorhandler(404)
def error_404(error):
    appdata['title'] = '404'
    return render_template('errors/404.html', appdata=appdata), 404


@errors.app_errorhandler(405)
def error_405(error):
    appdata['title'] = '405'
    flash("Please check if you are logged in with correct user.", "danger")
    return render_template('errors/405.html', appdata=appdata), 405


@errors.app_errorhandler(500)
def error_500(error):
    appdata['title'] = '500'
    return render_template('errors/500.html', appdata=appdata), 500
