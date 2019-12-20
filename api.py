from flask import Flask
from flask_restful import Api

from controllers.test_controller import *

app = Flask(__name__)

api = Api(app)

# base
api.add_resource(TestController, "/base")  # 测试接口
# 获取服务器时间

