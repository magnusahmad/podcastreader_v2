from app import app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Shop_Button(db.Model):
    __tablename__ = 'shopbutton'
    date = db.Column(db.Date, nullable=False, primary_key=True)
    click = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f'Shop button was clicked on {self.date}'
    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)