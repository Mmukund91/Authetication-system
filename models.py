from enum import unique
from . import db
from flask_login import UserMixin
from dataclasses import dataclass



@dataclass
class User(db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    public_id = db.Column(db.String(50) , unique = True)