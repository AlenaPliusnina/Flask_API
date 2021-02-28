from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    posts = db.relationship('Post', backref='user', lazy='dynamic', cascade="all,delete")
    comments = db.relationship('Comment', backref='user', lazy='dynamic', cascade="all,delete")

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    publication_datetime = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return '<Post %s>' % self.title


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    publication_datetime = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    def __repr__(self):
        return '<Comment %s>' % self.title