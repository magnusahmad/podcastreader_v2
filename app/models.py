from app import app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Shop(db.Model):
    __tablename__ = 'shop_click'
    datetime = db.Column(db.DateTime, nullable=False, primary_key=True)
    click = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f'Shop button was clicked on {self.datetime}'
    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)