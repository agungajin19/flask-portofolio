# test/__init__.py

import pytest, json, logging, hashlib
from flask import Flask, request

from blueprints import app, db
from app import cache
from blueprints.book.model import Books
from blueprints.user.model import Users
from blueprints.penerbit.model import Penerbit
from blueprints.cart.model import Carts, CartsDetail, Collections
from blueprints.like.model import Likes

def reset_db():
    db.drop_all()
    db.create_all()

    user = Users("agungajin","230710680c3f7eca1f694231180e58d1","agung@gmail.com")
    db.session.add(user)
    user = Users("agungajin2","dc9e31b613620bf7ac0a59f36c9cc0c3","agung@gmail.com")
    db.session.add(user)
    qry_user = Users.query.get(1)
    qry_user.status_penerbit = True
    db.session.commit()

    penerbit = Penerbit('erlangga',1)
    db.session.add(penerbit)
    penerbit = Penerbit('tigaserangkai',2)
    db.session.add(penerbit)
    db.session.commit()

    book = Books('sejarah matematika dasar', 'matematika', 5000, 10, 'SMA', '11', 'njoansflaksn', 'nsandskan',1)
    db.session.add(book)
    book = Books('sejarah kehidupan', 'biologi', 3000, 5, 'SMA', '11', 'njoansflaksn', 'nsandskan',2)
    db.session.add(book)
    db.session.commit()

    # cart = Carts(1)
    # db.session.add(cart)
    # cart = Carts(2)
    # db.session.add(cart)
    # db.session.commit()

    # # cart_detail = CartsDetail(1, 1, 2000)
    # # db.session.add(cart_detail)
    # cart_detail = CartsDetail(2, 1, 2000)
    # db.session.commit()



def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

def create_token(isinternal=False):
    if isinternal:
        cachename = 'test-internal-token'
        data = {
            'username' : 'internal',
            'password' : 'internal'
        }
    else:
        cachename = 'test-token'
        data = {
            'username' : 'agungajin',
            'password' : 'agungajin'
        }

    token = cache.get(cachename)
    if token is None:
    ## prepare request input
        

        ## do request
        req = call_client(request)
        res = req.post('/user/login', json = data)

        ## store response
        res_json = json.loads(res.data)

        logging.warning('RESULT : %s', res_json)

        ## assert /  compare with expected result
        assert res.status_code == 200

        ## save token into cache ## 'test-token' untuk internal dan noninternal client dibedakan
        cache.set(cachename, res_json['token'], timeout=60)

        ##return, because it usefull for other test
        return res_json['token']
    else:
        return token
         