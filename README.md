# zuman.co.in
Source code to my personal website !

This repository is the old one. Further development will be done on docker based setup found below:

* Source code:
[GitHub](https://github.com/zuman/zuman.in)

* Updated Website
[zuman.in](https://zuman.in)

# This setup
## Setup notes:
* Create a **conf.py** file in *zuman* directory similar to the one mentioned in the Appendix below.
* Setup a sessions manager such as Redis or Memcached to store session data in server.
* Fulfill pip requirements as needed.


## Appendix

>**conf.py**
```
import os

conf = {}
conf['SECRET_KEY'] = "..."
conf["SQLALCHEMY_DATABASE_URI"] = '...'
conf['MAIL_USERNAME'] = '...'
conf['MAIL_PASSWORD'] = '...'
conf['LOG_LEVEL'] = '...'
conf['SESSION_TYPE'] = '...'
conf['SESSION_COOKIE_NAME'] = '...'
conf['SESSION_COOKIE_SECURE'] = False  # True for Production
conf['PERMANENT_SESSION_LIFETIME'] = 100  # Any integer to denote seconds
conf['REMEMBER_COOKIE_DURATION'] = 100  # Any integer to denote seconds
conf['REMEMBER_COOKIE_HTTPONLY'] = True
conf['REMEMBER_COOKIE_SECURE'] = False  # True for Production

```
