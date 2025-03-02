from .db import db

# 评论信息
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

def add_comment(content, user_id, post_id, created_at):
    comment = Comment(content=content, user_id=user_id, post_id=post_id, created_at=created_at)
    db.session.add(comment)
    db.session.commit()

def get_comments_by_post_id(post_id):
    return Comment.query.filter_by(post_id=post_id).all()

def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    if comment is None:
        return False
    db.session.delete(comment)
    db.session.commit()
    return True
