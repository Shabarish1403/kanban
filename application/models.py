from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, unique=True)
    #lists = db.relationship('List', secondary='user_list')
    
class List(db.Model):
    __tablename__ = 'list'
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, db.ForeignKey('user.user_name'), nullable=False)
    list_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    #cards = db.relationship('Card', secondary='list_card')

class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.list_id'), nullable=False)
    card_name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)