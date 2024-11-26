# app.py
from flask import Flask, render_template

# 创建Flask实例
app = Flask(__name__)


# 定义一个路由
@app.route('/')
def index():
    return "Hello, Flask!"


# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
