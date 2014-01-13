from app import app, db
from hashlib import md5
from models import User

def create_user(username, password, commit=True):
    '''create a user with the given username and plaintext password'''
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