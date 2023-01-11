from datetime import datetime
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Table User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    # nickname = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    time_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # time_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().strftime('%Y %B %d - %H:%M'))
    posts = db.relationship('Post', backref='user', passive_deletes=True)

# Table Post 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # time_created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow().strftime('%Y %B %d - %H:%M'))