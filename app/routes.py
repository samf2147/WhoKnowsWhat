from flask import flash, url_for, render_template, g, request, redirect, session
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, Event, Payment
from forms import LoginForm, RegisterForm, EventForm, PaymentForm
import db_utilities
import hashlib
import pdb
import payment_math

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

#user account handling functions

@app.route('/login', methods=['GET','POST'])
def login():
    '''
    Handle login functions
    This function handles both the initial login page and the results
    '''
        
    #if the user is already logged, redirect them to the homepage
    if g.user is not None and g.user.is_authenticated() and \
                                     len(g.user.username) > 0:
        return redirect(url_for('home'))
    
    else:
        form = LoginForm(request.form)
        #if they've submitted it with valid credentials, try to log in the user
        #whether or not we can log them in, redirect them home
        if form.validate_on_submit():
            user = User.query.filter(User.username == form.username.data).first()
            hashed_password = hash_password(form.password.data)
            if user is not None and user.hashed_password == hashed_password:
                login_user(user)
            return redirect(url_for('home'))
		
		#otherwise, show them the form
        else:
            return render_template('login.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    '''
    Handle registering
    Use get requests to handle registering page
    Use post requests to handle creation of accounts
    '''
    form = RegisterForm()
    
    #if they haven't filled out the form, send them the form with a reminder
    if not form.validate_on_submit() and request.method == 'POST':
        return render_template('register.html', form=form, message='Please'
	                                        ' enter username and password.')
    elif not form.validate_on_submit():
        return render_template('register.html', form=form, message=None)
	
    #don't let the user create a duplicate username
    else:
	    attempted_name = form.username.data
	    if User.query.filter(User.username == attempted_name).first():
	        return render_template('register.html', form=form, 
	                                message='Username already taken.')
	    else:
	        user = db_utilities.create_user(form.username.data, form.password.data)
	        login_user(user)
	        return redirect(url_for('home'))
		    
@app.route('/logout', methods=['GET','POST'])
def logout():
    '''Log user out'''
    logout_user()
    return redirect(url_for('home'))



#event functions
@app.route('/events', methods=['GET'], defaults={'message':None})
@login_required
def events(message):
    '''View the user's events'''
    form = EventForm()
    return render_template('events.html', user = g.user, form=form,
                             message=message)

@app.route('/create-event', methods=['POST'])
@login_required
def create_event():
    '''Create the event the user posted'''
    form = EventForm(request.form)
        
    #only create the event if they entered in a name for it
    if not form.validate_on_submit():
        return render_template('events.html', user=g.user, form=form, 
                             message='Please enter name for event')
    
    #user can't create two events with the same name
    elif Event.query.filter(
               Event.name == form.name.data and Event.creator == g.user.id
               ).first():
        return render_template('events.html', user=g.user, form=form,
                             message='Event name already exists.')
    else:
        db_utilities.create_event(event_name = form.name.data, user_id = g.user.id)
        return redirect(url_for('events'))

@app.route('/delete-event/<event_id>', methods=['GET'])
@login_required
def delete_event(event_id):
    '''Delete the event the user requested'''
    #only delete the event if the user owns it
    if db_utilities.owns_event(g.user.id,event_id):
        db_utilities.remove_event(event_id)
    else:
        flash('You do not have permission to delete that event.')
    return redirect(url_for('events'))


#payment functions
@app.route('/payments/<event_id>', methods=['GET'])
@login_required
def payments(event_id):
    '''Display payments for the given event'''
    event = Event.query.filter(Event.id == event_id).first()
    
    #users can only view payments for events they created
    if event.creator != g.user.id:
        return redirect(url_for('events'))
    else:
        form = PaymentForm()
        if len(event.payments) == 0:
            payment_list = None
        else:
            payment_list = payment_math.payment_list(event)
        return render_template('payments.html', event = event, form=form,
                            payment_list = payment_list)
    
@app.route('/make-payment/<event_id>', methods=['POST'])
@login_required
def make_payment(event_id):
    '''Make a payment on the given event'''

    event = Event.query.filter(Event.id == event_id).first()
    
    form = PaymentForm(request.form)
    
    #users can only view payments for events they created
    if event.creator != g.user.id:
        return redirect(url_for('events'))
    elif not form.validate_on_submit():
        return render_template('payments.html', event=event,
                               message='Please enter payer and amount',
                               form=form)
    else:
        db_utilities.create_payment(payer=form.payer.data, 
                                    amount=form.amount.data,
                                    event_id=event_id)
        return redirect(url_for('payments',event_id = event_id))

@app.route('/delete-payment/<event_id>/<payment_id>', methods=['GET'])
@login_required
def delete_payment(event_id,payment_id):
    '''Delete the payment with the given payment_id'''
    #only delete the payment if the user owns the corresponding event
    payment = Payment.query.filter(Payment.id == payment_id).first()
    if payment and db_utilities.owns_payment(g.user.id, payment.id):
        db_utilities.remove_payment(payment.id)
    else:
        flash('You do not have permission to delete that payment')
    return redirect(url_for('payments',event_id=event_id))