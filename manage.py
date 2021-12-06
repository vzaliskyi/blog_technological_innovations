from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# from flask_script import Command, prompt_bool
from app import db
from flask import current_app as app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
