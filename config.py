import os

basedir = os.path.abspath(os.path.dirname(__file__))

#required variable
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

BASE_URL = 'http://localhost:5000'
