from flask import Flask
from zuman.conf import conf
from zuman.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
appdata = {"website_name": "Zuman's"}


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from zuman.models import User, Post

    from zuman.main.routes import main
    from zuman.users.routes import users
    from zuman.posts.routes import posts
    from zuman.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app