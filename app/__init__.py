from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') #use config.py file
db = SQLAlchemy(app)

#import routes last b/c routes imports app
from app import routes