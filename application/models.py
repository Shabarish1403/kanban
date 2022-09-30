from .database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)
    lists = db.relationship('List', backref='user')
    
class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    update_date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Card',backref='list',cascade='all,delete-orphan')

class Card(db.Model):
    __tablename__ = 'card'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.String, nullable=False)
    toggle = db.Column(db.String, nullable=False)
    create_date = db.Column(db.String, nullable=False)
    complete_date = db.Column(db.String, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)