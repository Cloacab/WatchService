from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Flask app:
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
# app.config.from_pyfile('config.py')

# Data base:
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, routes, scheduler
