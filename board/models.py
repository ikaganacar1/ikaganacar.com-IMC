from board import db, login_manager
from flask import request
from datetime import datetime, date
from sqlalchemy import func
from flask_login import UserMixin
from hashlib import sha256


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    role = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)

    type = db.Column(db.String(20))  # this is the discriminator column

    __mapper_args__ = {
        "polymorphic_on": type,
    }

    def __repr__(self) -> str:
        return f"User('{self.role}','{self.username}')"

class IMC_user(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False) 
    previous_code = db.Column(db.String(65), unique=True, nullable=False) 
    
    following = db.relationship("Followed", backref="imc_user", lazy=True)
    watchlist = db.relationship("Watchlist", backref="imc_user", lazy=True)
    watched = db.relationship("Watched", backref="imc_user", lazy=True)
    
    __mapper_args__ = {"polymorphic_identity": "IMC_user"}


    @property
    def invitation_code_1(self):
        return str(sha256((self.previous_code+"ika").encode('utf-8')).hexdigest())
        
    @property
    def invitation_code_2(self):
        return str(sha256((self.previous_code+"zsk").encode('utf-8')).hexdigest())
    
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
        
    def __repr__(self) -> str:
        return f"User('{self.role}','{self.username}','{self.email}')"


class Followed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("imc_user.id"), nullable=False, index=True)
    followed_user_id = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'followed_user_id', name='uq_user_followed'),)

class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("imc_user.id"), nullable=False, index=True)
    media_type = db.Column(db.String(10), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id'),)

class Watched(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("imc_user.id"), nullable=False, index=True)
    media_type = db.Column(db.String(10), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rated = db.Column(db.Float, nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id'),)
