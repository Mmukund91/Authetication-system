from enum import unique
from . import db
from flask_login import UserMixin





class User(db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    verified =  db.Column(db.Boolean , default = False)
    temp = db.Column(db.Integer)