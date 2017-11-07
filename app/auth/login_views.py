# -*- coding: utf-8 -*-
# Created by AKM_FAN@163.com on 2017/11/7
from flask import render_template, redirect, flash
from flask.views import MethodView
from .models import User
from .forms import LoginForm

class Login(MethodView):

    def get(self):

        return render_template('auth/login.html', form=LoginForm())


    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            flash('Error', 'warning')
            return redirect('/success')
        return render_template('auth/login.html', form=LoginForm())
