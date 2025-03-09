from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import logging

def init_app(app):
    # 设置 SQLALCHEMY_ECHO 为 True，开启 SQL 语句输出
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            logging.info("All database tables have been created successfully.")
        except Exception as e:
            logging.error(f"Failed to create database tables: {e}")
def get_db():
    return db
    