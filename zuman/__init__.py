from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from zuman.conf import conf
from zuman.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
sess = Session()
csrf = CSRFProtect()

login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
appdata = {"website_name": "Zuman's", "user_sessions": {}}


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    sess.init_app(app)
    csrf.init_app(app)

    from zuman.main.routes import main
    from zuman.users.routes import users
    from zuman.posts.routes import posts
    from zuman.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
