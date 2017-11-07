# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/7
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """ 登录Form """

    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
