import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # tempfile.mkstemp() 创建并打开一个临时文件，返回该文件描述符和路径。
    #  DATABASE 路径被重载，这样它会指向临时路径，而不是实例文件夹。
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

# TESTING 告诉 Flask 应用处在测试模式下。 Flask 会改变一些内部行为 以方便测试。其他的扩展也可以使用这个标志方便测试。
@pytest.fixture
def client(app):
    return app.test_client()

# runner 固件类似于 client 。 app.test_cli_runner() 创建一个运行器， 可以调用应用注册的 Click 命令。
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
    