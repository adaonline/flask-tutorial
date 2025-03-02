from .db import db
from .post import Post

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


def add_tag(name):
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

def get_tag_by_name(name):
    return Tag.query.filter_by(name=name).first()

def add_tag_to_post_by_name(tag_name, post_id):
    post = Post.query.filter_by(id=post_id).first()
    tag = Tag.query.filter_by(name=tag_name).first()
    post.tags.append(tag)

def add_tage_with_post(tag_name, post_id):
    add_tag(tag_name)
    add_tag_to_post_by_name(tag_name, post_id)