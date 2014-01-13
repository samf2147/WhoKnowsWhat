from flask import url_for, render_template, g, request, redirect, session
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User
from forms import LoginForm
import hashlib
import pdb

def hash_password(password):
    '''Hash a password'''
    m = hashlib.md5()
    m.update(password)
    return unicode(m.hexdigest())

@app.before_request
def before_request():
    '''Before every request, update the current user'''
    g.user = current_user

@lm.user_loader
def load_user(id):
    '''Get the user with the specified id - required by Flask-Login'''
    return User.query.get(int(id))

@app.route('/')
@app.route('/home')
def home():
    '''Show home screen'''
    user = g.user
    return render_template('home.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    '''
    Handle login functions
    This function handles both the initial login page and the results
    '''
    
#     pdb.set_trace()
    
    #if the user is already logged, redirect them to the homepage
    if g.user is not None and g.user.is_authenticated() and \
                                     len(g.user.username) > 0:
        return redirect(url_for('home'))
    
    else:
        form = LoginForm()
        #if they've submitted it with valid credentials, try to log in the user
        #whether or not we can log them in, redirect them home
        if form.validate_on_submit():
		    user = User.query.filter(User.username == form.username.data).first()
		    if user is not None and user.hashed_password == \
		                                        hash_password(form.password.data):
		        login_user(user)
		    return render_template('home.html', user = user)
		
		#otherwise, show them the form
        else:
            return render_template('login.html', form = form)
		        
		    
@app.route('/logout', methods=['GET','POST'])
def logout():
    '''Log user out'''
    logout_user()
    return redirect(url_for('home'))