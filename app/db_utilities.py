from app import app, db
from hashlib import md5

def create_user(username, password):
    '''create a user with the given username and plaintext password'''
    #for security reasons, don't store plain text password
    m = md5()
    m.update(password)
    hashed_pass = unicode(m.hexdigest())
    
    user = User(username=username, hashed_password=hashed_pass)
    
    db.session.add(user)
    db.session.commit()
    