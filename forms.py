from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])
    
class RegisterForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])

class EventForm(Form):
    name = TextField('event_name', validators=[Required()])