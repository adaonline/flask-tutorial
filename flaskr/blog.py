from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.models.post import *
from flaskr.models.user import *
from flaskr.models.comment import *
bp = Blueprint("blog", __name__)

@bp.route('/')
def index():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            add_post(g.user.id, title, body)
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_post_by_id(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

# 要生成一个指向更新页面的 URL ，需要传递 id 参数给 url_for() ： url_for('blog.update', id=post['id']) 
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            update_post(post.id, title, body)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)

    delete_post(post.id)
    return redirect(url_for('blog.index'))

@bp.route('/<int:id>/detail', methods=('GET',))
def detail(id):
    post = get_post_by_id(id)
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    comments = get_comments_by_post_id(post.id)

    return render_template('blog/detail.html', post=post, comments=comments)

@bp.route('/<int:post_id>/add_comment', methods=['POST'])
def add_comment(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        user_id = request.form.get('user_id')

        new_comment = Comment(
            content=content,
            user_id=user_id,
            post_id=post_id,
        )
        db.session.add(new_comment)
        db.session.commit()
        
        return redirect(url_for('blog.detail', id=post_id))