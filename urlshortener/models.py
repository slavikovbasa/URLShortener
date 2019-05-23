from urlshortener import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(10), index=True, unique=True)
    full = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Full link: "{self.full}", short: "{self.short}">'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    links = db.relationship('Link', backref = 'author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
