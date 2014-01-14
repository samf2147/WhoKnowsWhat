from app import app, db
from hashlib import md5
from models import User, Event, Payment
import re
import pdb

def create_user(username, password, commit=True):
    '''Create a user with the given username and plaintext password'''
    #for security reasons, don't store plain text password
    m = md5()
    m.update(password)
    hashed_pass = unicode(m.hexdigest())
    
    user = User(username=username, hashed_password=hashed_pass)
    
    db.session.add(user)
    
    if commit:
        db.session.commit()
    
    return user

def remove_user(username):
    '''
    Remove the user with the given username
    Return True if the user is deleted
    '''
    user = User.query.filter(User.username == username).first()
    if user:
        db.session.delete(user)
        db.commit()
        return True
    else:
        return False
    
def create_event(event_name, user_id, commit=True):
    '''Create an event with the given event name and user id'''
    event = Event(name = event_name, creator = user_id)
    db.session.add(event)
    if commit:
        db.session.commit()
    return event

def remove_event(event_id):
    '''
    Remove an event with the given id
    Return True if the event is deleted
    '''
    event = Event.query.filter(Event.id == event_id).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return True
    else:
        return False

def create_payment(event_id, payer, amount, commit=True):
    '''
    Create a payment for a given event
    amount can be passed as either a string or a float
    '''
    amount = payment_to_float(amount) 
    payment = Payment(payer=payer, amount=amount, event_id=event_id)   
    db.session.add(payment)
    if commit:
        db.session.commit()
    return payment

def payment_to_float(amount):
    '''Convert a payment into a float'''
    if isinstance(amount, basestring):
        money_pattern = re.compile(r'(?:[^0-9]*)([0-9]*)(.?)([0-9]*)')
        result = money_pattern.match(amount)
        return float(''.join([group for group in result.groups()]))
    else:
        return float(amount)

def remove_payment(id):
    '''
    Remove the payment with the given id
    Return True if payment is removed
    '''
    payment = Payment.query.filter(Payment.id == id).first()
    if payment:
        db.session.delete(payment)
        db.session.commit()
        return True
    else:
        return False

#utilities to check if the currently logged in owner has access to items
def owns_event(user_id, event_id):
    '''Return True if the user with user_id created event with event_id'''
    event = Event.query.filter(Event.id == event_id).first()
    if event and event.creator == user_id:
        return True
    else:
        return False

def owns_payment(user_id, payment_id):
    '''
    Returns true if the user with user_id owns the event
    that payment_id is for
    '''
    payment = Payment.query.filter(Payment.id == payment_id).first()
    if not payment:
        return False
    else:
        return owns_event(user_id, payment.event_id)
        