import json
from . import *

class TestUserCrud():
    reset_db()
    def test_post_userregister(self, client):
        # token = create_token(False)

        data = {
            'username' : 'agungajin',
            'password' : '230710680c3f7eca1f694231180e58d1',
            'email' : 'agungajin@gmail.com'
        }

        res = client.post('/user/register',
                            json = data,
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getid_admin(self, client):
        token = create_token(True)

        res = client.get('/admin/user/1',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_getid_admin3(self, client):
        token = create_token(True)

        res = client.get('/admin/user/100',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_getid_admin2(self, client):
        token = create_token()

        res = client.get('/admin/user/1',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 403

    def test_delete_admin(self, client):
        token = create_token(True)

        res = client.delete('/admin/user/3',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_delete_admin2(self, client):
        token = create_token(True)

        res = client.delete('/admin/user/100',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    

    #GET
    def test_user_getall_internal(self, client):
        token = create_token(True)

        data = {
            'p' : 1,
            'rp' : 25,
            'status_penerbit' : True,
            'orderby' : 'id',
            'sort' : 'asc'
        }

        res = client.get('/admin/user',
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
            'status_penerbit' : False,
            'orderby' : 'username',
            'sort' : 'desc'
        }

        res = client.get('/admin/user',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_getall_internal3(self, client):
        token = create_token(True)

        data = {
            'p' : 1,
            'rp' : 25,
            'status_penerbit' : False,
            'orderby' : 'id',
            'sort' : 'desc'
        }

        res = client.get('/admin/user',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_getall_internal4(self, client):
        token = create_token(True)

        data = {
            'p' : 1,
            'rp' : 25,
            'status_penerbit' : False,
            'orderby' : 'username',
            'sort' : 'asc'
        }

        res = client.get('/admin/user',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getme(self, client):
        token = create_token(False)

        res = client.get('/user/me',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getme(self, client):
        token = create_token(False)

        res = client.get('/user/me',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200