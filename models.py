from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    favorite = db.relationship("Favorite", backref='user', lazy=True)
    profile = db.relationship("Profile", backref='user', lazy=True , uselist=False)
    user_comment = db.relationship("Comment", backref='user', lazy=True)
    reservation = db.relationship("Reservation", backref='user', lazy=True)
    def __repr__(self):
        return "<User %r>" % self.email
    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
            'email':self.email,
            'phone':self.phone,
            'password':self.password,
        }
    def serialize_just_username(self):
        return {
            'id':self.id,
            'email':self.email,
        }
        
class Superadmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile = db.relationship("Profile", backref='superadmin', lazy=True , uselist=False)
    user_comment = db.relationship("Comment", backref='superadmin', lazy=True)
    event = db.relationship("Event", backref='superadmin', lazy=True, uselist=False)
    def __repr__(self):
        return "<Superadmin %r>" % self.email
    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
            'email':self.email,
            'phone':self.phone,
            'password':self.password,
        }
    def serialize_just_superadmin(self):
        return {
            'id':self.id,
            'email':self.email,
        }
        
class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    event = db.relationship("Event", backref='user', lazy=True, uselist=False)
    def __repr__(self):
        return "<Availability %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
        }
    def serialize_just_availability(self):
        return{
            'id': self.id,
            "date": self.date
        }
        
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    superadmin_id = db.Column(db.Integer, db.ForeignKey('superadmin.id'), nullable=False)
    def __repr__(self):
        return "<Profile %r>" % self.id_user
    def serialize(self):
        return {
        "id": self.id,
        "role": self.role,                          
        }
    def serialize_just_profile(self):
        return {
        "role": self.role,      
        }
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    thematic = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('availability.id'))
    superadmin_id = db.Column(db.Integer, db.ForeignKey('superadmin.id'))
    def __repr__(self):
        return "<Event %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'thematic': self.thematic,
            'price': self.price,
        }
    def serialize_just_event_name(self):
        return{
            'id': self.id,
            'name': self.name,
        }
        
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_thematic = db.Column(db.String(300), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return "<Favorite %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            'favorite_thematic': self.favorite_thematic,
            'user:name': self.user,
            'user_id': self.user_id,
        }
    def serialize_just_favorite(self):
        return{
            'id': self.id,
            'favorite_thematic': self.favorite_thematic
        }
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_user = db.Column(db.String(300), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    superadmin_id = db.Column(db.Integer, db.ForeignKey('superadmin.id'), nullable=False)
    def __repr__(self):
        return "<Comment %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            'comment_user': self.comment_user,
            "rate": self.rate,
            "user_id" : self.user_id
        }
    def serialize_just_comment(self):
        return{
            'id': self.id,
            'rate': self.rate,
        }
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return "<Reservation %r>" % self.id
    def serialize(self):
        return {
            'id': self.id,
            "date": self.date,
            "event_name": self.event_name,
            "user_id": self.user_id,
        }
    def serialize_just_reservation(self):
        return{
            'id': self.id,
            "user_id": self.user_id
        }


