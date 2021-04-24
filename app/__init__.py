from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)   # for login managing

# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'the fat cat cant jump over the brown fox'

# Avoid circular import
from app import models, routes