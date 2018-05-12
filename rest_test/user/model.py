from rest_test.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.Binary(128))
    active = db.Column(db.Boolean())
    password_reset_token = db.Column(db.String(255), unique=True, nullable=True)
