# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_nav import Nav
from flask_nav.elements import *
from werkzeug.routing import BaseConverter


# 制造高级转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap()
db = SQLAlchemy()
nav = Nav()


def create_app():
    app = Flask(__name__)
    # 转换器名称为regex
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_pyfile('config')
    # 连接SQLITE数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    nav.register_element('top', Navbar(u'Flask入门', View(u'主页', 'index'), View(u'用户', 'user', user_id='aaa')
                                       , View(u'登录', 'login'), View(u'注册', 'register'), View(u'sha256加密', 'sha256'),
                                       View(u'上传文件', 'upload'), View(u'百度SIGN', 'sign_str', qStr='%E4%BC%A0%E6%84%9F'
                                                                                                 '%E5%99%A8%E7%BD%91'
                                                                                                 '%E7%BB%9C')))

    db.init_app(app)
    bootstrap.init_app(app)
    nav.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def get_user(user_id):
        from .models import User
        return User.query.filter_by(name=user_id).first()

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .main import _main as main_blueprint
    app.register_blueprint(main_blueprint, static_folder='static')

    return app
