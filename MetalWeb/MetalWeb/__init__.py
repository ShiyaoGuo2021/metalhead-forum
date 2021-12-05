from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


MetalWeb = Flask(__name__)
MetalWeb.config.from_object(Config)
db = SQLAlchemy(MetalWeb)
migrate = Migrate(MetalWeb, db)
login = LoginManager(MetalWeb)
login.login_view = 'login'

from MetalWeb import routes, models

