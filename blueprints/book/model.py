from blueprints import db
from flask_restful import fields
import datetime

class Books(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judul = db.Column(db.String(30), nullable=False)
    penerbit_id = db.Column(db.Integer, db.ForeignKey('penerbit.id', ondelete='CASCADE'), nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    matapelajaran = db.Column(db.String(255), nullable=False, default='')
    jumlah_soal = db.Column(db.Integer, nullable=False)
    jenjang = db.Column(db.String(30), nullable=False)
    kelas = db.Column(db.String(30), nullable=False)
    url_picture = db.Column(db.String(255), default='')
    deskripsi = db.Column(db.String(255))
    nama_penerbit = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'judul' : fields.String,
        'matapelajaran' : fields.String,
        'penerbit_id' : fields.Integer,
        'harga' : fields.Integer,
        'jumlah_soal' : fields.Integer,
        'jenjang' : fields.String,
        'kelas': fields.String,
        'url_picture' : fields.String,
        'deskripsi' : fields.String,
        'nama_penerbit' :fields.String
    }

    def __init__(self, judul, matapelajaran, harga, jumlah_soal, jenjang, kelas, url_picture, deskripsi, penerbit_id):
        self.judul = judul
        self.matapelajaran = matapelajaran
        self.harga = harga
        self.jumlah_soal = jumlah_soal
        self.jenjang = jenjang
        self.kelas = kelas
        self.url_picture = url_picture
        self.deskripsi = deskripsi
        self.penerbit_id = penerbit_id

    def __repr__(self):
        return '<Book %r>' %self.id