import hashlib
import datetime
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Users
from blueprints.penerbit.model import Penerbit

from blueprints import db, app, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

from mailjet_rest import Client
import os

# password Encription
from password_strength import PasswordPolicy

bp_user = Blueprint('user', __name__)
api = Api(bp_user)


class AdminUser(Resource):
    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='json', default=1)
        parser.add_argument('rp', type=int, location='json', default=100000)
        parser.add_argument('status_penerbit', location='json')
        parser.add_argument('orderby', location='json',
                            help='invalid order value', choices=('username', 'id'))
        parser.add_argument('sort', location='json',
                            help='invalid sort value', choices=('desc', 'asc'))

        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry = Users.query
        qry_penerbit = Penerbit.query

        # qry = Users.query.filter(Users.title.like("%"+args['name']+"%"))

        if args['status_penerbit'] is not None:
            qry = qry.filter_by(status_penerbit=args['status_penerbit'])

        if args['orderby'] is not None:
            if args['orderby'] == 'id':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.id))
                else:
                    qry = qry.order_by(Users.id)
            elif args['orderby'] == 'username':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Users.username))
                else:
                    qry = qry.order_by(Users.username)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Users.response_fields))

        return rows, 200

    def options(self):
        return {'status': 'oke'}, 200


class UserRegister(Resource):
    def __init__(self):
        pass

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6,
            # uppercase = 2,
            # numbers = 1,
            # special = 1
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        parser.add_argument('email', location='json', required=True)

        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(
                args['password'].encode()).hexdigest()

            user = Users(args['username'], password_digest, args['email'])
            api_key = 'ae7375326b6063793661b40590f4c845'
            api_secret = 'f2a15384f00c5f95a48ca5a5026a261a'
            mailjet = Client(auth=(api_key, api_secret), version='v3.1')
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "easymyid10@gmail.com",
                            "Name": "easy.my.id"
                        },
                        "To": [
                            {
                                "Email": args['email'],
                                "Name": args[username]
                            }
                        ],
                        "Subject": "Welcome aboard {username}".format(username=args['username']),
                        "TextPart": "Thanks for Sign Up",
                        "HTMLPart": "<h3>Hai {username}, Welcome to  <a href='https://www.easy.my.id/'>easy.my.id</a>!</h3><br />Everyone can be smarter. Good Luck!!!!".format(username=args['username']),
                        "CustomID": "Thanks for Sign Up"
                    }
                ]
            }

        result = mailjet.send.create(data=data)

        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

    def options(self):
        return {'status': 'oke'}, 200


class AdminUserId(Resource):
    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self, id):
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def delete(self, id):
        qry = Users.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        # HARD DELETE
        db.session.delete(qry)
        db.session.commit()

        # SOFT DELETE
        # qry.deleted = True
        # db.session.commit()
        return {'status': 'Delete success'}, 200

    def options(self):
        return {'status': 'oke'}, 200


class UserMe(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        claim = get_jwt_claims()
        qry = Users.query.get(claim['id'])
        if qry is not None:
            return marshal(qry, Users.response_fields), 200

    def options(self):
        return {'status': 'oke'}, 200


api.add_resource(AdminUser, '/admin/user')
api.add_resource(AdminUserId, '/admin/user/<id>')
api.add_resource(UserRegister, '/user/register')
api.add_resource(UserMe, '/user/me')
