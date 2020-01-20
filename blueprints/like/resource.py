import hashlib, datetime
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Likes
from blueprints.user.model import Users
from blueprints.book.model import Books

from blueprints import db,app, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_like = Blueprint('like', __name__)
api = Api(bp_like)

class LikeResource(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', location='json', required=True)

        args = parser.parse_args()
        claim = get_jwt_claims()
        qry_like = Likes.query.filter_by(book_id=args['book_id']).filter_by(user_id=claim['id']).first()
        if qry_like is None:
            like = Likes(args['book_id'], claim['id'])

            db.session.add(like)
            db.session.commit()
            return marshal(like, Likes.response_fields)
        else:
            return{'messsage' : 'You have liked this item'}
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', location='json', required=True)

        args = parser.parse_args()
        qry_like = Likes.query.filter_by(book_id=args['book_id'])

        total_like = len(qry_like.all())
        like_dict = {}

        like_dict['book_id'] = qry_like.first().book_id
        like_dict['judul'] = Books.query.get(qry_like.first().book_id).judul
        like_dict['total_like'] = total_like

        return like_dict, 200
    def options (self):
        return {'status' : 'oke'}, 200

api.add_resource(LikeResource, '/user/like', '/public/like')                
