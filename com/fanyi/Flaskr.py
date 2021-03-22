from flask import Flask, render_template, url_for, send_from_directory, request, redirect
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
import os
import time


# 制造高级转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
# 转换器名称为regex
app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def index():
    return render_template("index.html", name="首页")


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
        ex = "." + f.filename.split(".")[-1]
        t = time.time()
        prev = int(round(t * 1000))
        filename = secure_filename(str(prev) + ex)
        base_path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(base_path, r'static/uploads/')
        f.save(os.path.join(upload_path, filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
