from flask import Flask
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_PROVIDERS'] = {
    # Google OAuth 2.0 documentation:
    # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
    'google': {
        'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
        'token_url': 'https://accounts.google.com/o/oauth2/token',
        'userinfo': {
            'url': 'https://www.googleapis.com/oauth2/v3/userinfo',
            'email': lambda json: json['email'],
        },
        'scopes': ['https://www.googleapis.com/auth/userinfo.email'],
    }
}

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

class Shop_button(db.Model):
    __tablename__ = 'shop_button'
    date = db.Column(db.Date, nullable=False, primary_key=True)
    click = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f'Shop button was clicked on {self.date}'

class Shop(db.Model):
    __tablename__ = 'shop_click'
    datetime = db.Column(db.DateTime, nullable=False, primary_key=True)
    click = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f'Shop button was clicked on {self.datetime}'
    

assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

from routes import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    # import json
    # cur_path = os.getcwd()
    # new_path = os.path.relpath('./credentials/openai_key.json', cur_path)

    # with open(new_path) as f:
    #     credentials = json.load(f)
    # file = input('Enter filename: ')
    # whisper_transcribe(file)



# OLD

# import json
# cur_path = os.getcwd()
# csrf_path = os.path.relpath('./credentials/csrf_key.json', cur_path)
# sql_path = os.path.relpath('./credentials/sqlalchemy_uri.json', cur_path)

# with open(csrf_path) as csrf:
#     data = json.load(csrf)
#     app.config['SECRET_KEY'] = data['CSRF_SECRET_KEY']

# with open(sql_path) as sql:
#     data = json.load(sql)
#     app.config['SQLALCHEMY_DATABASE_URI'] = data['SQLALCHEMY_DATABASE_URI']
    
# app.config['SECRET_KEY'] = os.getenv('csrf_key')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('sqlalchemy_uri')
# db = SQLAlchemy(app)