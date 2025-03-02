from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import logging

def init_app(app):
    print("init_app")
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            logging.info("All database tables have been created successfully.")
        except Exception as e:
            logging.error(f"Failed to create database tables: {e}")
def get_db():
    return db
    