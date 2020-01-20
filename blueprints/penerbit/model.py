from blueprints import db
from flask_restful import fields
import datetime

class Penerbit(db.Model):
    __tablename__ = 'penerbit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)
    nama_penerbit = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'nama_penerbit' : fields.String
    }

    def __init__(self, nama_penerbit, user_id):
        self.nama_penerbit = nama_penerbit
        self.user_id = user_id

    def __repr__(self):
        return '<Penerbit %r>' %self.id