import json
from . import *

class TestBookCrud():
    def test_post_BookPenerbit(self, client):
        token = create_token(False)

        data = {
            'jenjang' : 'SMA',
            'matapelajaran' : 'Fisika',
            'kelas' : '11',
            'harga' : 4000,
            'judul' : 'fisika',
            'url_picture' : 'fdsfmkmksd',
            'deskripsi' : 'nsndkjandka',
            'jumlah_soal' : 100
        }

        res = client.post('/penerbit/book',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_user_getall_BookPenerbit(self, client):
        token = create_token()

        data = {
            'p' : 1,
            'rp' : 25,
            'jenjang' : 'SMA',
            'matapelajaran' : 'Fisika',
            'kelas' : '11',
            'sort' : 'asc'
        }
        item = {
            'search' : 'sejarah'
        }

        res = client.get('/penerbit/book',
                            json = data,
                            query_string = item,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getid_BookPenerbit(self, client):
        token = create_token()

        res = client.get('/penerbit/book/1',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_getid_BookPenerbit2(self, client):
        token = create_token()

        res = client.get('/penerbit/book/100',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_getid_BookPenerbit3(self, client):
        token = create_token()

        res = client.get('/penerbit/book/2',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 401

    def test_patch_BookPenerbit(self, client):
        token = create_token(False)

        data = {
            'jenjang' : 'SMA',
            'matapelajaran' : 'Fisika',
            'kelas' : '11',
            'harga' : 4000,
            'judul' : 'fisika',
            'url_picture' : 'fdsfmkmksd',
            'deskripsi' : 'nsndkjandka',
            'jumlah_soal' : 100
        }

        res = client.patch('/penerbit/book/1',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_patch_BookPenerbi2(self, client):
        token = create_token(False)

        data = {
            'jenjang' : 'SMA',
            'matapelajaran' : 'Fisika',
            'kelas' : '11',
            'harga' : 4000,
            'judul' : 'fisika',
            'url_picture' : 'fdsfmkmksd',
            'deskripsi' : 'nsndkjandka',
            'jumlah_soal' : 100
        }

        res = client.patch('/penerbit/book/100',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

    def test_patch_BookPenerbit3(self, client):
        token = create_token(False)

        data = {
            'jenjang' : 'SMA',
            'matapelajaran' : 'Fisika',
            'kelas' : '11',
            'harga' : 4000,
            'judul' : 'fisika',
            'url_picture' : 'fdsfmkmksd',
            'deskripsi' : 'nsndkjandka',
            'jumlah_soal' : 100
        }

        res = client.patch('/penerbit/book/2',
                            json = data,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 401

    def test_user_getall_BookPublic(self, client):
        token = create_token()

        data = {
            'p' : 1,
            'rp' : 25,
            'jenjang' : 'SMA',
            'matapelajaran' : 'Fisika',
            'kelas' : '11',
            'sort' : 'asc'
        }
        item = {
            'search' : 'sejarah'
        }

        res = client.get('/public/book',
                            json = data,
                            query_string = item,
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getid_BookPublic(self, client):
        token = create_token()

        res = client.get('/public/book/1',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_getid_BookPublic2(self, client):
        token = create_token()

        res = client.get('/public/book/10',
                            headers={'Authorization' : 'Bearer ' + token}
                            )
        res_json = json.loads(res.data)
        assert res.status_code == 404

