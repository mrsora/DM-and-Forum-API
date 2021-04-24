import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Support for checking messages
    messagesSent = db.relationship('Message',
                                   foreign_keys='Message.senderID',
                                   backref='author', lazy='dynamic')
    messagesReceived = db.relationship('Message',
                                       foreign_keys='Message.recipientID',
                                       backref='recipient', lazy='dynamic')

    def hash_pw(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify_pass(self, pw):
        return check_password_hash(self.password_hash, pw)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderID = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipientID = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posterID = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.datetime.utcnow)
    likes = db.Column(db.Integer)
