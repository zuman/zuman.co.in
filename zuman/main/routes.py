import json

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from zuman import appdata, db
from zuman.utils import updateSession

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
@main.route("/index.html")
def home():
    appdata["title"] = None
    no_container = True
    return render_template("home.html", appdata=appdata, no_container=no_container)


@main.route("/.well-known/brave-rewards-verification.txt")
def brave():
    appdata["title"] = None
    return render_template("brave-rewards-verification.txt")


@main.route("/api")
def test():
    if not current_user.is_authenticated:
        return "{ null }"
    q = '''
    select u.username as "user", u.sid as "cookie", count(p.*) as "post_count"
    from public.user u, post p where u.id={}
    group by username, sid
    '''
    js = {}
    db_exec = db.engine.execute(q.format(current_user.id))
    for dt in db_exec:
        js = {key: dt[key] for key in dt.keys()}

    return json.dumps(js)


@main.route("/info")
@login_required
def apiUI():
    updateSession("API test page", js=['apage'])
    return render_template("users/apage.html", appdata=appdata)
