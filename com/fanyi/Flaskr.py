import os
import time
from functools import reduce

from flask import Flask, render_template, url_for, request, redirect, make_response
from flask_script import Manager
from livereload import Server
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from markdown import markdown
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename


# 制造高级转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
# 转换器名称为regex
app.url_map.converters['regex'] = RegexConverter
Bootstrap(app)
nav = Nav()

manager = Manager(app)

nav.register_element('top', Navbar('Flask入门', View('主页', 'index'), View('关于', 'about'), View('服务', 'services')
                                   , View('项目', 'projects')))

nav.init_app(app)


@app.route('/')
def index():
    # abort(404)
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
def user(user_id=None):
    return 'user_id为：%s' % user_id


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
    else:
        username = request.args["username"]
    return render_template("login.html", method=request.method)


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


@manager.command
def dev():
    app.debug = True
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)


if __name__ == '__main__':
    # app.run()
    manager.run()
