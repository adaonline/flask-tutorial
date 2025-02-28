from waitress import serve
from flaskr import create_app
import logging
# 配置日志
logging.basicConfig(level=logging.DEBUG)
# 创建 Flask 应用实例
app = create_app()

if __name__ == '__main__':
    # 使用 waitress 启动应用
    serve(app, host='0.0.0.0', port=8080)