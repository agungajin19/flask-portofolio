from blueprints import db
from flask_restful import fields
import datetime

class Likes(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now(), default=datetime.datetime.now())


    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'book_id' : fields.Integer
    }

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

    def __repr__(self):
        return '<Like %r>' %self.id