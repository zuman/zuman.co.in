import os
import json
from zuman.conf import conf

if 'CONFIG_FILE' in conf:
    with open(conf['CONFIG_FILE']) as config_file:
        conf = json.load(config_file)


class Config:
    SECRET_KEY = conf["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = conf["SQLALCHEMY_DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = conf['MAIL_USERNAME']
    MAIL_PASSWORD = conf['MAIL_PASSWORD']