# __init__.py 有两个作用：一是包含应用工厂； 二是告诉 Python flaskr 文件夹应当视作为一个包。

import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    # 加载默认配置
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    from . import db
    db.init_app(app)

    # 使用 app.register_blueprint() 导入并注册 蓝图。新的代码放在工厂函数的尾部返回应用之前。
    from . import auth
    app.register_blueprint(auth.bp)


    # 博客蓝图没有 url_prefix 。因此 index 视图会用于 / ， create 会用于 /create ，以此类推。博客是 Flaskr 的主要 功能，因此把博客索引作为主索引是合理的
    # 我们使用 app.add_url_rule() 关联端点名称 'index' 和 / URL ，这样 url_for('index') 或 url_for('blog.index') 都会有效，会生成同样的 / URL 。
    from . import blog
    app.register_blueprint(blog.bp) 
    app.add_url_rule('/', endpoint='index')

    return app

# flask --app flaskr run --debug
