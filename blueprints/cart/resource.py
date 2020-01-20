import hashlib, datetime
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Carts, CartsDetail, Collections
from blueprints.user.model import Users
from blueprints.book.model import Books
from blueprints.penerbit.model import Penerbit

from blueprints import db,app, internal_required
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', location='json', required=True)

        args = parser.parse_args()
        claim = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id=claim['id']).filter_by(status=False)
        qry_book = Books.query.filter_by(id=args['book_id']).first()
        if qry_cart.first() is not None:
            qry_cart_detail = CartsDetail.query.filter_by(cart_id=qry_cart.first().id).filter_by(book_id=args['book_id']).first()
            qry_collection = Collections.query.filter_by(user_id=claim['id']).filter_by(book_id=args['book_id']).first()
            if qry_cart_detail is None and qry_collection is None:
                cart_detail = CartsDetail(qry_cart.first().id, args['book_id'], qry_book.harga)
                db.session.add(cart_detail)
                db.session.commit()
                marshalCartDetail = marshal(cart_detail, CartsDetail.response_fields)
                qry_penerbit = Penerbit.query.get(qry_book.penerbit_id)
                marshalCartDetail['judul'] = qry_book.judul
                marshalCartDetail['penerbit'] = qry_penerbit.nama_penerbit
                return marshalCartDetail, 200
            else:
                return{'message' : 'You have already added this item in your cart or collection'}, 404

        else:
            cart = Carts(claim['id'])
            db.session.add(cart)
            db.session.commit()
            qry_cart_detail = CartsDetail.query.filter_by(cart_id=qry_cart.first().id).filter_by(book_id=args['book_id']).first()
            qry_collection = Collections.query.filter_by(user_id=claim['id']).filter_by(book_id=args['book_id']).first()
            if qry_cart_detail is None and qry_collection is None:
                cart_detail = CartsDetail(qry_cart.first().id, args['book_id'], qry_book.harga)
                db.session.add(cart_detail)
                db.session.commit()
                marshalCartDetail = marshal(cart_detail, CartsDetail.response_fields)
                qry_penerbit = Penerbit.query.get(qry_book.penerbit_id)
                marshalCartDetail['judul'] = qry_book.judul
                marshalCartDetail['penerbit'] = qry_penerbit.nama_penerbit
                return marshalCartDetail, 200
            else:
                return{'message' : 'You have added this item in your cart or have already in your collection'}, 404
        
        

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=100000)

        args = parser.parse_args()
        offset = (args['p']*args['rp'])-args['rp']

        claim = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id=claim['id']).filter_by(status=False).first()
        if qry_cart is not None:
            qry_cartdetail = CartsDetail.query.filter_by(cart_id=qry_cart.id)

            dic = {}
            dic['page'] = args['p']
            dic['per_page'] = args['rp']
            rows = []
            for row in qry_cartdetail.limit(args['rp']).offset(offset).all():
                marshalCartDetail = marshal(row, CartsDetail.response_fields)
                qry_book = Books.query.get(row.book_id)
                qry_penerbit = Penerbit.query.get(qry_book.penerbit_id)
                marshalCartDetail['judul'] = qry_book.judul
                marshalCartDetail['penerbit'] = qry_penerbit.nama_penerbit
                marshalCartDetail['url_picture'] = qry_book.url_picture
                rows.append(marshalCartDetail)
            dic['data'] = rows

            # add total price to database
            total_price = 0
            total_item = len(qry_cartdetail.all())
            for qry in qry_cartdetail:
                total_price += qry.price
            qry_cart.totalprice = total_price
            qry_cart.totalitem = total_item
            db.session.commit()

            dic['totalprice'] = qry_cart.totalprice
            dic['totalitem'] = qry_cart.totalitem
            
            return dic, 200
        else:
            return {'status' : 'You have added this item in your cart or have already in your collection'}, 404

    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('book_id', location='json', required=True)

        args = parser.parse_args()
        claim = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id=claim['id']).filter_by(status=False).first()
        qry_cartdetail = CartsDetail.query.get(args['book_id'])
        # qry_cartdetail = CartsDetail.query.get(id)
        if qry_cartdetail is None:
            return {'status' : 'NOT_FOUND'}, 404
        else:
            if qry_cartdetail.cart_id == qry_cart.id:
                # HARD DELETE
                db.session.delete(qry_cartdetail)
                db.session.commit()

                #SOFT DELETE
                # qry.deleted = True
                # db.session.commit()
                return {'status' : 'Delete success'}, 200
            else:
                return {'status' : 'UNAUTHORIZED', 'message' : 'BOOK ID NOT YOURS'}, 401
                
    def options (self):
        return {'status' : 'oke'}, 200

class Payment(Resource):
    def __init__(self):
        pass

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('payment_method', location='json', required=True)

        args = parser.parse_args()
        claim = get_jwt_claims()
        qry_cart = Carts.query.filter_by(user_id=claim['id']).filter_by(status=False).first()
        if qry_cart is not None:
            qry_cart.payment_method = args['payment_method']
            qry_cart_detail = CartsDetail.query.filter_by(cart_id=qry_cart.id)
            for each in qry_cart_detail:
                collection = Collections(qry_cart.user_id, each.book_id)
                db.session.add(collection)

            qry_cart.status = True
            db.session.commit()
            marshalCart = marshal(qry_cart, Carts.response_fields)
            marshalCart['message'] = 'Payment Success'
            return marshalCart, 200
        else:
            return{'message' : 'You do not have any transaction'}

    def options (self):
        return {'status' : 'oke'}, 200

class CollectionResource(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='json', default=1)
        parser.add_argument('rp', type=int, location='json', default=100000)

        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        claim = get_jwt_claims()
        qry_collection = Collections.query.filter_by(user_id=claim['id'])
        if len(qry_collection.all()) != 0:
            dic = {}
            dic['page'] = args['p']
            dic['per_page'] = args['rp']
            rows = []
            for row in qry_collection:
                marshalCollection = marshal(row, Collections.response_fields)
                qry_book = Books.query.get(row.book_id)
                qry_penerbit = Penerbit.query.get(qry_book.penerbit_id)
                marshalCollection['judul'] = qry_book.judul
                marshalCollection['url_picture'] = qry_book.url_picture
                marshalCollection['penerbit'] = qry_penerbit.nama_penerbit
                marshalCollection['jenjang'] = qry_book.jenjang
                marshalCollection['kelas'] = qry_book.kelas
                marshalCollection['jumlah_soal'] = qry_book.jumlah_soal
                rows.append(marshalCollection)
            
            dic['data'] = rows
            dic['total_item'] = len(rows)
            return dic, 200
        else:
            return {'message' : 'You do not have any collection'}, 404
    def options (self):
        return {'status' : 'oke'}, 200


class PublisherTracnsaction(Resource):
    def __init__(self):
        pass

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='json', default=1)
        parser.add_argument('rp', type=int, location='json', default=1000000)

        args = parser.parse_args()

        offset = (args['p']*args['rp'])-args['rp']

        claim = get_jwt_claims()
        qry_user = Users.query.get(claim['id'])
        
        json={}
        data = []
        
        if qry_user.status_penerbit == True:
            qry_penerbit = Penerbit.query.filter_by(user_id=claim['id']).first()
            qry_book = Books.query.filter_by(penerbit_id=qry_penerbit.id)
            list_id = [eachbook.id for eachbook in qry_book]
            print(list_id)
            qry_cart = Carts.query.filter_by(status=True)
            total_harga = 0
            for each in qry_cart:
                qry_cart_detail = CartsDetail.query.filter_by(cart_id=each.id)
                for qry in qry_cart_detail:
                    book_id = qry.book_id
                    buku = Books.query.get(book_id)
                    harga = buku.harga
                    marhsalTransaction = {}
                    if qry.book_id in list_id:
                        marhsalTransaction['book_id'] = qry.book_id
                        marhsalTransaction['user_id'] = each.user_id
                        marhsalTransaction['price'] = harga
                        marhsalTransaction['judul'] = buku.judul
                        marhsalTransaction['jenjang'] = buku.jenjang
                        marhsalTransaction['kelas'] = buku.kelas
                        marhsalTransaction['url_picture'] = buku.url_picture
                        total_harga +=  harga
                        data.append(marhsalTransaction)
            json['transactions'] = data
            json['total_revenue'] = total_harga
            total_harga = 0
            return json, 200
        else:
            return {'status' : 'UNAUTHORIZED', 'message' : 'You are not a publisher'}, 401
    def options (self):
        return {'status' : 'oke'}, 200


api.add_resource(CartResource, '/user/cart', '/user/cart/<id>')                
api.add_resource(Payment, '/user/payment')                
api.add_resource(PublisherTracnsaction, '/penerbit/transaction') 
api.add_resource(CollectionResource, '/user/collection') 

