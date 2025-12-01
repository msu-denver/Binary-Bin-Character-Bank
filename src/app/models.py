from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # store hashed passwords
    characters = db.relationship('Character', backref='owner', lazy=True)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    character_class = db.Column(db.String(50), nullable=False)
    race = db.Column(db.String(50), nullable=False)
    background = db.Column(db.String(50), nullable=False)
    backstory = db.Column(db.String(1000))
    is_public = db.Column(db.Boolean, default=False)
    
    # Ability scores
    strength = db.Column(db.Integer, nullable=False, default=10)
    dexterity = db.Column(db.Integer, nullable=False, default=10)
    constitution = db.Column(db.Integer, nullable=False, default=10)
    intelligence = db.Column(db.Integer, nullable=False, default=10)
    wisdom = db.Column(db.Integer, nullable=False, default=10)
    charisma = db.Column(db.Integer, nullable=False, default=10)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
