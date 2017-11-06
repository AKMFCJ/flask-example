# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/6
"""Flask app 配置"""
import os


from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
# 跨域资源共享
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.server.config.DevelopmentConfig'
)
# 从对象/文件/字符串中
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# 路由配置