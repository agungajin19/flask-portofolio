from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Books

from blueprints.user.model import Users
from blueprints.penerbit.model import Penerbit

from blueprints import db,app, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_book = Blueprint('book', __name__)
api = Api(bp_book)

class BookPenerbit(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=1000000)
        parser.add_argument('jenjang', location='args')
        parser.add_argument('matapelajaran', location='args')
        parser.add_argument('kelas', location='args')
        parser.add_argument('search', location='args')

        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry = Books.query

        if args['search'] is not None:
            qry = qry.filter(Books.judul.like('%'+args['search']+'%') | Books.nama_penerbit.like('%'+args['search']+'%'))

        if args['jenjang'] is not None:
            qry = qry.filter_by(jenjang=args['jenjang'])

        if args['matapelajaran'] is not None:
            qry = qry.filter_by(matapelajaran=args['matapelajaran'])
        
        if args['kelas'] is not None:
            qry = qry.filter_by(kelas=args['kelas'])


        dic = {}
        dic['page'] = args['p']
        dic['per_page'] = args['rp']
        rows = []
        claim = get_jwt_claims()
        qry_user = Users.query.get(claim['id'])
        if qry_user.status_penerbit == True:
            qry_penerbit = Penerbit.query.filter_by(user_id=claim['id']).first()
            qry = qry.filter_by(penerbit_id=qry_penerbit.id).limit(args['rp']).offset(offset)
            for each in qry:
                marshalBook = marshal(each, Books.response_fields)
                marshalBook['penerbit'] = qry_penerbit.nama_penerbit
                rows.append(marshalBook)
        
            dic['data'] = rows

            return dic, 200, {'Content-Type':'application/json'}
        else:
            return {'status' : 'UNAUTHORIZED', 'message' : 'you are not a publisher'}, 401
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('judul', location='json', required=True)
        parser.add_argument('matapelajaran', location='json', required=True)
        parser.add_argument('harga', location='json', required=True)
        parser.add_argument('jumlah_soal', location='json', required=True)
        parser.add_argument('jenjang', location='json', required=True)
        parser.add_argument('kelas', location='json', required=True)
        parser.add_argument('url_picture', location='json', required=True)
        parser.add_argument('deskripsi', location='json', required=True)

        args = parser.parse_args()
        claim = get_jwt_claims()
        qry_user = Users.query.get(claim['id'])
        if qry_user.status_penerbit == True:
            qry = Penerbit.query.filter_by(user_id=claim['id']).first()
            book = Books(args['judul'], args['matapelajaran'], args['harga'], args['jumlah_soal'], args['jenjang'],args['kelas'], args['url_picture'], args['deskripsi'], qry.id)
            db.session.add(book)
            db.session.commit()
            qry_book = Books.query.filter_by(judul=args['judul']).filter_by(penerbit_id=qry.id).first()
            qry_book.nama_penerbit = qry.nama_penerbit
            db.session.commit()

            app.logger.debug('DEBUG : %s', book)
            marshalBook = marshal(book, Books.response_fields)
            # marshalBook['penerbit'] = qry.nama_penerbit

            return marshalBook, 200, {'Content-Type':'application/json'}
        else:
            return {'status' : 'UNAUTHORIZED', 'message' : 'Your are not a publisher'}, 401

    def options (self):
        return {'status' : 'oke'}, 200




class BookPenerbitId(Resource):
    def __init__(self):
        pass

    def options (self):
        return {'status' : 'oke'}, 200

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', location='json', required=True)

        args = parser.parse_args()
        claim = get_jwt_claims()
        qry_penerbit = Penerbit.query.filter_by(user_id=claim['id']).first()
        qry = Books.query.get(args['book_id'])
        if qry is not None:
            if qry.penerbit_id == qry_penerbit.id:
                return marshal(qry, Books.response_fields), 200
            return {'status' : 'UNAUTHORIZED', 'message' : 'ID NOT YOURS'}, 401
        else:
            return {'status': 'NOT_FOUND'}, 404
    
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', location='json', required=True)
        parser.add_argument('judul', location='json')
        parser.add_argument('matapelajaran', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('jumlah_soal', location='json')
        parser.add_argument('jenjang', location='json')
        parser.add_argument('kelas', location='json')
        parser.add_argument('url_picture', location='json')
        parser.add_argument('deskripsi', location='json')


        args = parser.parse_args()

        claim = get_jwt_claims()
        qry_penerbit = Penerbit.query.filter_by(user_id=claim['id']).first()
        qry = Books.query.get(args['book_id'])

        if qry is not None:
            if qry.penerbit_id == qry_penerbit.id:
                if args['judul'] is not None:
                    qry.judul = args['judul']
                if args['matapelajaran'] is not None:
                    qry.matapelajaran = args['matapelajaran']
                if args['harga'] is not None:
                    qry.harga = args['harga']
                if args['jumlah_soal'] is not None:
                    qry.jumlah_soal = args['jumlah_soal']
                if args['jenjang'] is not None:
                    qry.jenjang = args['jenjang']
                if args['kelas'] is not None:
                    qry.kelas = args['kelas']
                if args['url_picture'] is not None:
                    qry.url_picture = args['url_picture']
                if args['deskripsi'] is not None:
                    qry.deskripsi = args['deskripsi']
                db.session.commit()
                return marshal(qry, Books.response_fields), 200, {'Content-Type':'application/json'}
            return {'status' : 'UNAUTHORIZED', 'message' : 'ID NOT YOURS'}, 401
        else:
            return {'status': 'NOT_FOUND'}, 404

    
    
        

class BookPublic(Resource):
    def __init__(self):
        pass
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=10000000)
        parser.add_argument('jenjang', location='args')
        parser.add_argument('matapelajaran', location='args')
        parser.add_argument('kelas', location='args')
        parser.add_argument('search', location='args')


        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        qry = Books.query

        if args['search'] is not None:
            qry = qry.filter(Books.judul.like('%'+args['search']+'%') | Books.nama_penerbit.like('%'+args['search']+'%'))

        if args['jenjang'] is not None:
            qry = qry.filter_by(jenjang=args['jenjang'])

        if args['matapelajaran'] is not None:
            qry = qry.filter_by(matapelajaran=args['matapelajaran'])
        
        if args['kelas'] is not None:
            qry = qry.filter_by(kelas=args['kelas'])


        dic = {}
        dic['page'] = args['p']
        dic['per_page'] = args['rp']
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            qry_penerbit = Penerbit.query.filter_by(id=row.penerbit_id).first()
            marshalBook = marshal(row, Books.response_fields)
            marshalBook['penerbit'] = qry_penerbit.nama_penerbit
            rows.append(marshalBook)
        
        dic['data'] = rows
        
        return dic, 200
        
    def options (self):
        return {'status' : 'oke'}, 200

class BookPublicId(Resource):
    def __init__(self):
        pass

    def get(self, id):
        qry = Books.query.get(id)
        if qry is not None:
            qry_penerbit = Penerbit.query.filter_by(id=qry.penerbit_id).first()
            marshalBook = marshal(qry, Books.response_fields)
            marshalBook['penerbit'] = qry_penerbit.nama_penerbit
            return marshalBook, 200
        else:
            return {'status': 'NOT_FOUND'}, 404
    def options (self):
        return {'status' : 'oke'}, 200


api.add_resource(BookPenerbit, '/penerbit/book')
api.add_resource(BookPenerbitId, '/penerbit/bookid/')
api.add_resource(BookPublic, '/public/book','/user/book')
api.add_resource(BookPublicId, '/public/book/<id>','/user/book/<id>')


