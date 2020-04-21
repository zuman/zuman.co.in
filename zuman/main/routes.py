from flask import Blueprint
from flask import render_template
from zuman import appdata

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
