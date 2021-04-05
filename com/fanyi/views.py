# -*- coding: utf-8 -*-
import os
import time
from functools import reduce
import hashlib

from flask import render_template, redirect, make_response, flash
from flask_nav.elements import *
from markdown import markdown
from werkzeug.utils import secure_filename


def init_views(app):
    @app.route('/')
    def index():
        response = make_response(render_template("index.html", title="<h1>这是首页</h1>", body='## header'))
        response.set_cookie('username', '')
        return response

    @app.template_filter('md')
    def markdown_to_html(text):
        return markdown(text)

    def read_md(filename):
        with open(filename) as md_f:
            content = reduce(lambda x, y: x+y, md_f.readlines())
        return content.encode("gbk").decode('utf-8')

    @app.context_processor
    def inject_methods():
        return dict(read_md=read_md)

    @app.template_test('current_link')
    def is_current_link(link):
        return link['href'] == request.path

    @app.route('/user/<regex("[a-z]{3}"):user_id>')
    def user(user_id):
        return 'user_id为：%s' % user_id

    @app.route('/sha256/')
    def sha256():
        s = hashlib.sha256()
        s.update(u'$d6eb7ff91ee257475%1016174405633722393vqXujyqidsMC7WpK'.encode('utf-8'))
        return s.hexdigest()

    @app.route('/register/')
    def register():
        return '注册页面'

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        from .forms import LoginForm
        form = LoginForm()
        flash(u'Please Login')
        return render_template("login.html", form=form)

    @app.route('/upload/', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            f = request.files['file']
            ex = os.path.splitext(f.filename)[-1]
            t = time.time()
            prev = int(round(t * 1000))
            filename = secure_filename(str(prev) + ex)
            base_path = os.path.abspath(os.path.dirname(__file__))
            upload_path = os.path.join(base_path, r'static/uploads/')
            f.save(os.path.join(upload_path, filename))
            return redirect(url_for('upload'))
        return render_template('upload.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
