from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), unique = True)
    hashed_password = db.Column(db.String(128), unique = True)
    events = db.relationship('Event', backref='event_creator')
    
    #methods required by flask-login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    payments = db.relationship('Payment', backref='event')


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    payer = db.Column(db.String(128), unique = False)
