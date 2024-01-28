from extensions import db
from flask_login import  UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

# Database models
class User(UserMixin,TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    hash_password = db.Column(db.String(255), nullable=False)
    emojis = db.relationship('Emoji', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)



class Emoji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    group = db.Column(db.String(255))
    html_code = db.Column(db.String(255))
    unicode = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Emoji {self.name}>'