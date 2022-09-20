from tkinter import CASCADE
from .database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, unique=True)
    lists = db.relationship('List', backref='user')
    
class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Card',backref='list',cascade='all,delete-orphan')

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    toggle = db.Column(db.String, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)