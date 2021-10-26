from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    # favorite = db.relationship('Favorite', backref='user', cascade='all, delete', lazy=True)
    # event = db.relationship('Event', backref='user', cascade='all, delete', lazy=True)
    # comment = db.relationship('Comment', backref='user', cascade='all, delete', lazy=True)
    # reservation = db.relationship('Reservation', backref='user', cascade='all, delete', lazy=True)

    def __repr__(self):
        return "<User %r>" % self.name
    
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
            'name':self.name,
        }
        
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    thematic = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    frecuent_question = db.Column(db.String(300), nullable=False)
    # availability = db.relationship('Availability', backref='event', cascade='all, delete', lazy=True)
    # reservation = db.relationship('Reservation', backref='event', cascade='all, delete', lazy=True)
    # user = db.relationship('User', backref='event', cascade='all, delete', lazy=True)

    def __repr__(self):
        return "<Event %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'thematic': self.thematic,
            'price': self.price,
            'frecuent_question': self.frecuent_question,
        }

    def serialize_just_event_name(self):
        return{
            'id': self.id,
            'name': self.name,
        }
        
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    favorite_thematic = db.Column(db.String(300), nullable=False)
    # user = db.relationship('User', backref='favorite', cascade='all, delete', lazy=True)

    def __repr__(self):
        return "<Favorite %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user,
            'favorite_thematic': self.favorite_thematic
        }

    def serialize_just_favorite(self):
        return{
            'id': self.id,
            'favorite_thematic': self.favorite_thematic
        }
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(300), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    # user = db.relationship('User', backref='comment', cascade='all, delete', lazy=True)

    def __repr__(self):
        return "<Comment %r>" % self.id

    def serialize_comment(self):
        return {
            'id': self.id,
            'user': self.user,
            'comment': self.comment,
            "rate": self.rate
        }

    def serialize_just_comment(self):
        return{
            'id': self.id,
            'user': self.user,
            'comment': self.comment
        }
  
        
class Availability(db.Model):
    _tablename_ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    #user = db.Column(db.String(30), db.ForeignKey("user.name", ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.Integer, nullable=False)
    # id_user = db.Column(db.String(30), db.ForeignKey("user.name", ondelete='CASCADE'), nullable=False)

    def _repr_(self):
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

        
class Reservation(db.Model):

    date = db.Column(db.Integer, primary_key=True)
    # event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
    # event_name = db.Column(db.String(30), primary_key=True)
    # user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    def __repr__(self):
        return "<Reservation %r>" % self.id

    
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'event_id': self.event_id,
            "event_name": self.event_name,
            "user_id": self.user_id
        }

    def serialize_just_reservation(self):
        return{
            'id': self.id,
            'date': self.date,
            "event_name": self.event_name
        }
