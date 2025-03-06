from .db import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

def add_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def delete_user(username):
    user = get_user_by_username(username)
    if user is None:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

def change_user_password(username, password):
    user = get_user_by_username(username)
    if user is None:
        return False
    user.password = password
    db.session.commit()
    return True
