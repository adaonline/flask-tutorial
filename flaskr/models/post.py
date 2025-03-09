from .db import db

# 博文信息
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String, nullable=False)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary='post_tag', backref='related_posts', lazy=True)
    
    # 建立与 User 模型的反向引用
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))


def add_post(author_id, title, content):
    post = Post(author_id=author_id, title=title, content=content)
    db.session.add(post)
    db.session.commit()

def update_post(id, title, content):
    post = get_post_by_id(id)
    if post is None:
        return False
    post.title = title
    post.content = content
    db.session.commit()

def get_post_by_id(id):
    return Post.query.filter_by(id=id).first()

def get_posts_by_author_id(author_id):
    return Post.query.filter_by(author_id=author_id).all()

def get_posts_by_title(title):
    return Post.query.filter(Post.title.like('%' + title + '%')).all()

def get_posts_by_content(content):
    return Post.query.filter(Post.content.like('%' + content + '%')).all()

def delete_post(id):
    post = get_post_by_id(id)
    if post is None:
        return False
    db.session.delete(post)
    db.session.commit()
    return True

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Dislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

