# -*- coding: utf-8 -*-

from flask import render_template, redirect, make_response, flash
from . import auth


@auth.route('/register/')
def register():
    return '注册页面'


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    from .forms import LoginForm
    form = LoginForm()
    flash(u'Please Login')
    return render_template("login.html", form=form)
