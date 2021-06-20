from flask import Flask, config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import access, path
from authlib.integrations.flask_client import OAuth
import firebase_admin
import json
import pyrebase
from firebase_admin import credentials , auth
import jwt
import datetime

db = SQLAlchemy()
oauth = OAuth()
DBNAME = "database.db"







def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "thisisit"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DBNAME}'
    app.config['GOOGLE_CLIENT_ID'] = "188545127905-e1983c7glrqkmcuieceuhgfuula8tjge.apps.googleusercontent.com"
    app.config['GOOGLE_CLIENT_SECRET'] = "-xKkyfruKZKUN9G5fbfr2PIS"
    app.config['GITHUB_CLIENT_ID'] = "93d70b5f030d88c63a4b"
    app.config['GITHUB_CLIENT_SECRET'] = "ca0aa914048f030e8412ae75c02301fa464f271f"
    app.config['FACEBOOK_CLIENT_ID']= "495664508348182"
    app.config['FACEBOOK_CLIENT_SECRET'] = "2e31a33974154907d5de51c7de2684"
    db.init_app(app)
    oauth.init_app(app)

    google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
    )

    github = oauth.register (
    name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)


    facebook = oauth.register(
        name = 'facebook',
        client_id = app.config["FACEBOOK_CLIENT_ID"],
        client_secret = app.config['FACEBOOK_CLIENT_SECRET'],
        access_token_url = "https://graph.facebook.com/v7.0/oauth/access_token",
        access_token_params = None,
        authorize_url = 'https://www.facebook.com/v7.0/dialog/oauth',
        authorize_params = None,
        api_base_url = 'https://graph.facebook.com/v7.0/',
        client_kwargs = {'scope': 'email public_profile'},


    )



    
    from .auth import auth
    from .main import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    from .models  import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

     
    

    return app

def create_database(app):
    if not path.exists("flask_authapp/"+ DBNAME):
        db.create_all(app=app)
