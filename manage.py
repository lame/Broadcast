from flask_script import Manager
from flask_migrate import MigrateCommand

from app import app

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('run', app.run(debug=True))

if __name__ == '__main__':
    manager.run()
