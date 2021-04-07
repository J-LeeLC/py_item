from flask_script import Manager
from fanyi import create_app, db
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


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
    from fanyi.models import Role
    upgrade()
    Role.seed()


if __name__ == '__main__':
    manager.run()
