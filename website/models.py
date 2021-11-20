from datetime import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id')) # reference to id of user, one-many relationship
    

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key =True)
    email = db.Column(db.String(150),nullable=False,unique=True)
    firstName = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(150),nullable=False)
    notes = db.relationship('Note') # list of notes 
    