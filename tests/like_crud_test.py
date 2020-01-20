import json
from . import *

class TestLikeCrud():
    reset_db()
    def test_post_addlike(self, client):
        token = create_token(False)

        data = {
            'book_id' : 1,
        }

        res = client.post('/user/like',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_post_addlike2(self, client):
        token = create_token(False)

        data = {
            'book_id' : 1,
        }

        res = client.post('/user/like',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        # assert res.status_code == 200

    def test_get_like(self, client):
        data = {
            'book_id' : 1,
        }

        res = client.get('/user/like',
                            json = data,
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200