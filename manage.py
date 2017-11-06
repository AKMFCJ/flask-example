#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/6
"""
工程引导文件
开发运行
数据库创建更新
工程自定义命令
"""
import os
import unittest
# 代码覆盖率测量库
import coverage

# 自定义命令库
from flask_script import Manager
# 数据库表结构迁移库(将model修改同步修改数据库表结构)
from flask_migrate import Migrate, MigrateCommand


COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*',
        'app/server/config.py',
        'app/*/__init__.py'
    ]
)

COV.start()

from app.server import app, db

migrate = Migrate(app, db)
manager = Manager(app)

# migrations 将db 相关的命令作为manager的子命令
manager.add_command('db', MigrateCommand)


# 自定义命令
@manager.command
def test():
    """单执行单元测试,不跑代码覆盖率"""
    tests = unittest.TestLoader.discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """执行单元测试的同时执行代码覆盖率检查"""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful:
        COV.stop()
        COV.start()
        print('Coverage Summary:')
        COV.report()
        base_dir = os.path.abspath(os.path.dirname(__file__))
        cov_dir = os.path.join(base_dir, 'tmp/coverage')
        COV.html_report(directory=cov_dir)
        print('HTML version: file://%s//index.html' % cov_dir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """创建数据库"""

    database_uri = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'])
    database_name = app.config['DATABASE_NAME']
    engine = db.create_engine(database_uri)
    engine.execute("CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci" % database_name)


@manager.command
def drop_db():
    """删除数据库"""

    database_uri = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'])
    database_name = app.config['DATABASE_NAME']
    engine = db.create_engine(database_uri)
    engine.execute("DROP DATABASE %s" % database_name)


@manager.command
def create_tables():
    """创建空表"""

    db.create_all()


@manager.command
def drop_tables():
    """删除所有的表"""

    db.drop_all()


@manager.command
def init_data():
    """初始化数据"""
    pass


if __name__ == '__main__':
    manager.run()