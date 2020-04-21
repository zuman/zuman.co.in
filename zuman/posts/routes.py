from datetime import datetime

from flask import (Blueprint, abort, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required

from zuman import db, appdata
from zuman.models import Post
from zuman.posts.forms import EditClauseForm, InclauseForm
from zuman.posts.utils import inclauserator

posts = Blueprint('posts', __name__)


@posts.route("/inclause", methods=["GET", "POST"])
def inclause():
    page = request.args.get('page', 1, type=int)
    form = InclauseForm()
    appdata["title"] = "In-Clause App"
    op = None
    if form.validate_on_submit():
        op = inclauserator(form.inputdata.data)
    if current_user.is_authenticated:
        appdata['posts']=Post.query\
            .filter_by(author=current_user)\
            .order_by(Post.date_accessed.desc())\
            .paginate(per_page=5, page=page)
    else:
        flash("Consider logging in to save your in-clause history.", "info")
    return render_template("posts/inclause.html", data=op, form=form, appdata=appdata)


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    form = EditClauseForm()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_accessed = datetime.utcnow()
        db.session.commit()
        flash("This inclause has been updated.", "success")
        return redirect(url_for('posts.inclause'))
    appdata['title'] = post.title
    appdata['legend'] = 'Update clause'
    form.title.data = post.title
    form.content.data = post.content
    return render_template('posts/post.html', appdata=appdata, form=form, post=post)


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("This inclause has been deleted.", "success")
    return redirect(url_for('posts.inclause'))