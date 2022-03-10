from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_restful import Resource, Api
from flask_mail import Mail


MetalWeb = Flask(__name__)
MetalWeb.config.from_object(Config)
db = SQLAlchemy(MetalWeb)
migrate = Migrate(MetalWeb, db)
login = LoginManager(MetalWeb)
login.login_view = 'login'
api = Api(MetalWeb)
mail = Mail(MetalWeb)

from MetalWeb import routes, models

