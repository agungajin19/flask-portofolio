import json
from . import *

class TestCartCrud():
    reset_db()
    def test_post_additemtocart(self, client):
        token = create_token(False)
        data = {
            'book_id' : 1,
        }

        res = client.post('/user/cart',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_additemtocart2(self, client):
        token = create_token(False)
        data = {
            'book_id' : 1,
        }

        res = client.post('/user/cart',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_post_additemtocart3(self, client):
        token = create_token(False)
        data = {
            'book_id' : 2,
        }

        res = client.post('/user/cart',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_cartitem(self, client):
        token = create_token(False)
        res = client.delete('/user/cart/2',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_cartitem(self, client):
        token = create_token(False)
        data = {
            'p' : 1,
            'rp': 25
        }

        res = client.get('/user/cart',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_cartitem2(self, client):
        token = create_token(False)
        data = {
            'p' : 1,
            'rp': 25
        }

        res = client.get('/user/cart',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_Payment(self, client):
        token = create_token(False)
        data = {
            'payment_method' : "transfer bank BNI",
        }

        res = client.post('/user/payment',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_get_collection2(self, client):
        token = create_token(False)
        data = {
            'p' : 1,
            'rp': 25
        }

        res = client.get('/user/collection',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_collection(self, client):
        token = create_token(False)
        data = {
            'p' : 1,
            'rp': 25
        }

        res = client.get('/user/collection',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_PublisherTransaction(self, client):
        token = create_token(False)
        data = {
            'p' : 1,
            'rp': 25
        }

        res = client.get('/penerbit/transaction',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

