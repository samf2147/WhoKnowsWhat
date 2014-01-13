from app import app, db
from hashlib import md5
from models import User, Event, Payment

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