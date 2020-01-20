import json
from . import *

class TestPenerbitCrud():
    reset_db()
    # def test_post_PenerbitRegister(self, client):
    #     token = create_token(False)

    #     data = {
    #         'nama_penerbit' : 'yudhistira'
    #     }

    #     res = client.post('/penerbit/register',
    #                         json = data,
    #                         headers={'Authorization' : 'Bearer ' + token}
    #                         )
    #     res_json = json.loads(res.data)
    #     assert res.status_code == 200

    def test_post_PenerbitRegister2(self, client):
        token = create_token(False)

        data = {
            'nama_penerbit' : 'yudhistira'
        }

        res = client.post('/penerbit/register',
                            query_string = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
    
    def test_user_getall_internal(self, client):
        token = create_token(True)

        data = {
            'p' : 1,
            'rp' : 25,
            'orderby' : 'id',
            'sort' : 'asc'
        }

        res = client.get('/admin/penerbit',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_getall_internal2(self, client):
        token = create_token(True)

        data = {
            'p' : 1,
            'rp' : 25,
            'orderby' : 'id',
            'sort' : 'desc'
        }

        res = client.get('/admin/penerbit',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_getid_adminPenerbit(self, client):
        token = create_token(True)

        res = client.get('/admin/penerbit/1',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getid_adminPenerbit2(self, client):
        token = create_token(True)

        res = client.get('/admin/penerbit/100',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_delete_adminPenerbit2(self, client):
        token = create_token(True)

        res = client.delete('/admin/penerbit/2',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_delete_adminPenerbit3(self, client):
        token = create_token(True)

        res = client.delete('/admin/penerbit/100',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404