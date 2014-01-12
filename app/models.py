from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    
    payments = db.relationship('Payment', backref='event')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Float)
    event_id = db.Column(db.Integer, db.ForeignKey('even.id'))