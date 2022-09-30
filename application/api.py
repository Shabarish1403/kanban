from flask_restful import Resource, fields, marshal_with, reqparse
from application.models import User, List, Card
from application.validation import NotFoundError, BusinessValidationError
from .database import db
from datetime import datetime as dt

list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'user_id': fields.Integer
}

list_parser = reqparse.RequestParser()
list_parser.add_argument('name')
list_parser.add_argument('description')

class ListAPI(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            l = []
            for lst in user.lists:
                l.append(lst.name)
            return {'user_id': user_id, 'lists': l}
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(list_fields)
    def post(self, user_id):
        args = list_parser.parse_args()
        name = args.get('name', None)
        description = args.get('description', None)
        update_date = dt.isoformat(dt.now())

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='LIST001', error_message='List Name is required')

        l = List.query.filter_by(name=name,user_id=user_id).first()
        if l is not None:
            raise BusinessValidationError(status_code=400, error_code='LIST002', error_message='List Name already exists')
        
        l = List(name=name, description=description,update_date=update_date ,user_id = user_id)
        db.session.add(l)
        db.session.commit()
        return l, 201

    def delete(self, list_id):
        l = List.query.get(list_id)
        if l is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(l)
            db.session.commit()
            return "Successfully Deleted"

    @marshal_with(list_fields)
    def put(self, list_id):
        l = List.query.get(list_id)
        if l is None:
            raise NotFoundError(status_code=404)

        args = list_parser.parse_args()
        name = args.get('name', None)
        description = args.get('description', None)

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='LIST001', error_message='List Name is required')

        new = List.query.filter_by(name=name,user_id=l.user_id).first()
        if l.name == name or new == None:
            l.name = name
            l.description = description
            db.session.commit()
            return l,200
        else:
            raise BusinessValidationError(status_code=400, error_code='LIST002', error_message='List Name already exists')



card_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'deadline': fields.String,
    'toggle': fields.String,
    'list_id': fields.Integer
}

card_parser = reqparse.RequestParser()
card_parser.add_argument('name')
card_parser.add_argument('content')
card_parser.add_argument('deadline')
card_parser.add_argument('toggle')
card_parser.add_argument('list_id')

class CardAPI(Resource):
    def get(self, list_id):
        l = List.query.get(list_id)
        if l:
            c = []
            for card in l.cards:
                c.append(card.name)
            return {'list_id': list_id, 'cards': c}
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(card_fields)
    def post(self, list_id):
        args = card_parser.parse_args()
        name = args.get('name', None)
        content = args.get('content', None)
        deadline = args.get('deadline', None)
        toggle = False
        create_date = dt.isoformat(dt.now())
        complete_date = 'Not completed'

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='CARD001', error_message='Card Name is required')

        if deadline is None:
            raise BusinessValidationError(status_code=400, error_code='CARD002', error_message='Deadline is required')

        today = dt.today().strftime('%Y-%m-%d')
        if deadline < today:
            raise BusinessValidationError(status_code=400, error_code='CARD003', error_message='The Date must be bigger or Equal to today date')

        card = Card.query.filter_by(name=name,list_id=list_id).first()
        if card is not None:
            raise BusinessValidationError(status_code=400, error_code='CARD004', error_message='Card Name already exists in the given list')
        
        c = Card(name=name, content=content, deadline=deadline, toggle=toggle, create_date=create_date, complete_date=complete_date ,list_id=list_id)
        db.session.add(c)
        db.session.commit()
        return c, 201

    def delete(self, card_id):
        card = Card.query.get(card_id)
        if card is None:
            raise NotFoundError(status_code=404)
        else:
            db.session.delete(card)
            db.session.commit()
            return "Successfully Deleted"

    @marshal_with(card_fields)
    def put(self, card_id):
        card = Card.query.get(card_id)
        if card is None:
            raise NotFoundError(status_code=404)

        args = card_parser.parse_args()
        name = args.get('name', None)
        content = args.get('content', None)
        deadline = args.get('deadline', None)
        toggle = args.get('toggle', None)
        list_id = args.get('list_id', None)

        if list_id is None:
            raise BusinessValidationError(status_code=400, error_code='LIST003', error_message='List Id is required')

        l = List.query.get(list_id)
        if l is None:
            raise NotFoundError(status_code=404)

        if name is None:
            raise BusinessValidationError(status_code=400, error_code='CARD001', error_message='Card Name is required')
        
        if deadline is None:
            raise BusinessValidationError(status_code=400, error_code='CARD002', error_message='Deadline is required')

        today = dt.today().strftime('%Y-%m-%d')
        if deadline < today:
            raise BusinessValidationError(status_code=400, error_code='CARD003', error_message='The Date must be bigger or Equal to today date')

        flag = False
        c = Card.query.filter_by(name=name,list_id=list_id).first()
        if card.list_id == list_id:
            if card.name == name or c == None:
                flag = True
        elif c == None:
            card.list_id = list_id
            flag = True
        
        if flag:
            card.name = name
            card.content = content
            card.deadline = deadline
            card.toggle = toggle
            db.session.commit()
            return card,200
        else:
            raise BusinessValidationError(status_code=400, error_code='CARD004', error_message='Card Name already exists in the given list')