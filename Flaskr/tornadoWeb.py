"""
托管flaskr.py
"""
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flaskr import app
from tornado.ioloop import IOLoop
s = HTTPServer(WSGIContainer(app))
s.bind(5000, '0.0.0.0')
s.start(1)
IOLoop.instance().start()
