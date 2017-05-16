from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# local imports
#from config import app_config
    
# db variable initialization

login_manager = LoginManager()
application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)
#application = flask.Flask("application")
#app.config.from_pyfile('config.py')
#db.init_app(application)
login_manager.init_app(application)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"
#migrate = Migrate(app, db)
# from application import models
#Bootstrap(application)
# #from .admin import admin as admin_blueprint
# #application.register_blueprint(admin_blueprint, url_prefix='/admin')
# from .auth import auth as auth_blueprint
# application.register_blueprint(auth_blueprint)
# from .home import home as home_blueprint
# application.register_blueprint(home_blueprint)
