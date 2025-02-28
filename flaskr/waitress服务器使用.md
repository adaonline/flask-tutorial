waitress 是一个纯 Python 实现的 WSGI 服务器，用于在生产环境中运行 Python Web 应用程序（如 Flask、Django 等）。它是一个轻量级、高性能的服务器，适合部署中小型 Web 应用。

在开发环境中，Flask 自带的开发服务器（通过 flask run 启动）非常适合调试和测试，但它不适合生产环境，因为：
- 它是单线程的，无法处理高并发。
- 缺乏安全性优化。
- 性能较差。
waitress 是一个适合生产环境的替代方案，它：
- 支持多线程，可以处理并发请求。
- 更加稳定和安全。
- 配置简单，易于集成到现有项目中。
  

安装
```
pip install waitress
```

启动 flaskr这个应用
```
waitress-serve --call 'flaskr:create_app'
```