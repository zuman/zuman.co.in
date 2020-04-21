# zuman.co.in
Source code to my personal website !

[zuman.co.in](https://zuman.co.in)

## Setup notes:
* Create a **conf.py** file in *zuman* directory similar to the one mentioned in the Appendix below.
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

```