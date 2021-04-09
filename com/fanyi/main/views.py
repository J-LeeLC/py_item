# -*- coding: utf-8 -*-
import os
import time
from functools import reduce
import hashlib
import js2py

from flask import render_template, redirect, make_response, flash
from flask_nav.elements import *
from markdown import markdown
from werkzeug.utils import secure_filename
from . import _main


@_main.route('/')
def index():
    response = make_response(render_template("index.html", title="<h1>这是首页</h1>", body='## header'))
    response.set_cookie('username', '')
    return response


@_main.template_filter('md')
def markdown_to_html(text):
    return markdown(text)


def read_md(filename):
    with open(filename) as md_f:
        content = reduce(lambda x, y: x+y, md_f.readlines())
    return content.encode("gbk").decode('utf-8')


@_main.context_processor
def inject_methods():
    return dict(read_md=read_md)


@_main.template_test('current_link')
def is_current_link(link):
    return link['href'] == request.path


@_main.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'user_id为：%s' % user_id


@_main.route('/sha256/')
def sha256():
    s = hashlib.sha256()
    s.update(u'$d6eb7ff91ee257475%1016174405633722393vqXujyqidsMC7WpK'.encode('utf-8'))
    return s.hexdigest()


@_main.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        ex = os.path.splitext(f.filename)[-1]
        t = time.time()
        prev = int(round(t * 1000))
        filename = secure_filename(str(prev) + ex)
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, r'../static/uploads/')
        f.save(os.path.join(upload_path, filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


@_main.route('/translate/sign?qStr=<qStr>')
def sign_str(qStr):
    base_path = os.path.abspath(os.path.dirname(__file__))
    js_path = os.path.join(base_path, r'../static/js/sign.js')
    if qStr.find("%@F") != -1:
        q = qStr.replace("%@F", "/")
    else:
        q = qStr
    with open(js_path, 'r', encoding='utf-8') as f:
        content = js2py.EvalJs()  # 实例化解析js对象
        content.execute(f.read())  # js转python代码
        n = content.pro(q)
        sign_c = content.e(n, "320305.131321201")
        return sign_c


@_main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
