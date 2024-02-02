from datetime import datetime
from app import db

class Shop_Button(db.Model):
    date = db.Column(db.Date, nullable=False, primary_key=True)
    click = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f'Shop button was clicked on {self.date}'