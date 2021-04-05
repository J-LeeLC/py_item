from flask_script import Manager
from fanyi import create_app

app = create_app()
manager = Manager(app)


@manager.command
def dev():
    from livereload import Server
    app.debug = True
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)


@manager.command
def test():
    pass


@manager.command
def deploy():
    pass


if __name__ == '__main__':
    manager.run()
