from blueprints import db
from flask_restful import fields
import datetime

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30),  nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    status_penerbit = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'email' : fields.String,
        'status_penerbit' : fields.Boolean,
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'email' : fields.String,
        'status_penerbit' : fields.Boolean,
        'internal_status' : fields.String
    }

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' %self.id