from zuman import db, mail
from zuman.models import User, Post
from flask_login import current_user


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def batchify(data):
    i = 0
    tmp_set = set()
    out_str = ''
    for var in data:
        i = i + 1
        tmp_set.add(var)
        if i % 1000 == 0:
            out_str = out_str + ' or in ' + str(tuple(tmp_set))
            tmp_set = set()
    out_str = out_str + ' or in ' + str(tuple(tmp_set))
    return out_str[4:]


def make_inclause(data):
    info = data.strip().split("\n")
    ret = set()
    for field in info:
        field = field.strip()
        if len(field) == 0:
            continue
        if isint(field):
            ret.add(int(field))
        elif isfloat(field):
            ret.add(float(field))
        else:
            ret.add(field)
    if len(ret) > 1000:
        ret = batchify(ret)
    else:
        ret = 'in ' + str(tuple(ret))
    return ret


def inclauserator(data):
    content = make_inclause(data)
    available_post = Post.query.filter_by(content=content).first()
    if available_post or current_user.is_anonymous:
        pass
    else:
        post = Post(content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        post.title = post.id
        db.session.commit()
    return content
