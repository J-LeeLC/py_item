from flask import Blueprint

_main = Blueprint('main', __name__)

from . import views
