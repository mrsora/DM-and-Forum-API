import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = 'the fat cat cant jump over the brown fox'
