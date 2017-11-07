# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/6
from flask import Blueprint, request,  make_response, jsonify
from .login_views import *

login_views = Login.as_view('login_views')

# add Rules
auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule('/auth/login', view_func=login_views, methods=['GET', 'POST'])