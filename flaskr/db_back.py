import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def update_db():
    db = get_db()
    with current_app.open_resource('update.sql') as f:
        db.executescript(f.read().decode('utf8'))     
# click.command() 定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的消息。更多关于如何写命令行的 内容请参阅 doc:/cli 。
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
    'timestamp', lambda value: datetime.fromisoformat(value.decode())
)
# 在工厂中导入并调用这个函数。在工厂函数中把新的代码放到函数的尾部，返 回应用代码的前面。
def init_app(app):
    # 告诉 Flask 在返回响应后进行清理的时候调用此函数。
    app.teardown_appcontext(close_db)
    # 添加一个新的 可以与 flask 一起工作的命令。
    app.cli.add_command(init_db_command)