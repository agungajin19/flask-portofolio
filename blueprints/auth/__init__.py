from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..user.model import Users
import json, hashlib

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

###Resource

class CreateTokenResource(Resource):

    def post(self):
        ##Create Token
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()


        ### from database ###
        if args['username'] == 'internal' and args['password'] == 'internal':
            token = create_access_token(identity=args['username'], user_claims={'internal_status' : 'internal'})
            return {'token' : token}, 200
        else:
            qry = Users.query.filter_by(username=args['username']).filter_by(password=password)

            userData = qry.first()
            if userData is not None:
                userData = marshal(userData, Users.jwt_claims_fields)
                userData['internal_status'] = 'noninternal'
                token = create_access_token(identity=args['username'], user_claims=userData)
                return {'token' : token}, 200
            else:
                return {'status' : 'UNAUTHORIZED', 'message' : 'invalid username or password'}, 401

    def options(self, id=None):
        return {'status':'ok'},200


api.add_resource(CreateTokenResource, '')