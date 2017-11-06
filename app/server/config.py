# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/6
"""
工程配置文件,分开发环境/测试环境/生成环境的配置.
"""
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
database_url = 'mysql://root:root@localhost/'


class BaseConfig:
    """ 通用配置 """
    # 默认从环境变量中获取,没有设置环境变量的使用此默认值
    SECRET_KEY = os.getenv('SECRET_KEY','my@secret')
    DEBUG = False
    # bcrypt加密
    BCRYPT_LOG_ROUNDS = 13
    # 默认是TRUE model变更发通知信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_NAME = 'example'
    SQLALCHEMY_DATABASE_URI = database_url + DATABASE_NAME


class TestingConfig(BaseConfig):
    """测试环境配置"""

    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_NAME = 'example_test'
    SQLALCHEMY_DATABASE_URI = database_url + DATABASE_NAME
    # 异常信息的显示方式 参见Flask 配置处理
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductConfig(BaseConfig):
    """生产环境配置"""

    SECRET_KEY = 'my@secret'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/prodcut'
