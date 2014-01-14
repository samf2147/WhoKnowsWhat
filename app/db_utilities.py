from app import app, db
from hashlib import md5
from models import User, Event, Payment
import re

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
    user = User.query.filter(User.username == username).first()
    db.session.delete(user)
    db.commit()
    
def create_event(event_name, user_id, commit=True):
    '''Create an event with the given event name and user id'''
    event = Event(name = event_name, creator = user_id)
    db.session.add(event)
    if commit:
        db.session.commit()
    return event

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