import hashlib, datetime
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Penerbit
from blueprints.user.model import Users

from blueprints import db,app, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_penerbit = Blueprint('penerbit', __name__)
api = Api(bp_penerbit)


class PenerbitRegister(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_penerbit', location='json', required=True)

        args = parser.parse_args()

        claim = get_jwt_claims()
        qry = Users.query.get(claim['id'])
        if qry.status_penerbit == False:
            penerbit = Penerbit(args['nama_penerbit'], claim['id'])
            
            qry.status_penerbit = True

            db.session.add(penerbit)
            db.session.commit()

            app.logger.debug('DEBUG : %s', penerbit)

            return marshal(penerbit, Penerbit.response_fields), 200, {'Content-Type':'application/json'}
        else:
            return {'status' : 'anda sudah menjadi penerbit'}, 404
    def options (self):
        return {'status' : 'oke'}, 200

class AdminPenerbit(Resource):
    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='json', default=1)
        parser.add_argument('rp', type=int, location='json', default=25)

        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry = Penerbit.query
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Penerbit.response_fields))
        
        return rows, 200
    def options (self):
        return {'status' : 'oke'}, 200

class AdminPenerbitId(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self, id):
        qry = Penerbit.query.get(id)
        if qry is not None:
            return marshal(qry, Penerbit.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    
    @jwt_required
    @internal_required
    def delete(self, id):
        qry = Penerbit.query.get(id)
        if qry is None:
            return {'status' : 'NOT_FOUND'}, 404
        # HARD DELETE
        db.session.delete(qry)
        db.session.commit()

        #SOFT DELETE
        # qry.deleted = True
        # db.session.commit()
        return {'status' : 'Delete success'}, 200
    def options (self):
        return {'status' : 'oke'}, 200

api.add_resource(PenerbitRegister, '/penerbit/register')
api.add_resource(AdminPenerbit, '/admin/penerbit')
api.add_resource(AdminPenerbitId, '/admin/penerbit/<id>')



