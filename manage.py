from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask_script import Command, prompt_bool
from app.blog.models import *
from app.user.models import *
from app import db, app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
