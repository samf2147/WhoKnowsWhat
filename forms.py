from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])