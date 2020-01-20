from blueprints import db
from flask_restful import fields
import datetime

class Carts(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    totalprice = db.Column(db.Integer, nullable=False, default=0)
    totalitem = db.Column(db.Integer, nullable=False, default=0)
    payment_method = db.Column(db.String(255), nullable=False, default='')
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'totalprice' : fields.Integer,
        'totalitem' : fields.Integer,
        'payment_method' : fields.String,
        'status' : fields.Boolean
    }

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<Cart %r>' %self.id

class CartsDetail(db.Model):
    __tablename__ = 'cart_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'cart_id' : fields.Integer,
        'book_id' : fields.Integer,
        'price' : fields.Integer
    }

    def __init__(self, cart_id, book_id, price):
        self.cart_id = cart_id
        self.book_id = book_id
        self.price = price


    def __repr__(self):
        return '<CartDetail %r>' %self.id

class Collections(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'book_id' : fields.Integer,
    }

    def __init__(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return '<Collection %r>' %self.id