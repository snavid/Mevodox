from websites import db
from flask_login import UserMixin
from datetime import datetime


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    filedata = db.Column(db.LargeBinary)
    data = db.Column(db.String(10000))
    title = db.Column(db.String(200))
    date = db.Column(db.Date, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(300))
    gender = db.Column(db.Integer)
    notes = db.relationship('Note', backref='owner')
    
    