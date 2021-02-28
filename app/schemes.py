from flask_marshmallow import Marshmallow
from app import app
from app.models import User, Post, Comment

ma = Marshmallow(app)


class CommentSchema(ma.Schema):
    class Meta:
        fields = ("id",  "post_id", "author_id", "title", "content", "publication_datetime")
        model = Comment
        ordered = True


class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content", "author_id", "publication_datetime", "comments")
        model = Post
        ordered = True

    comments = ma.Nested(CommentSchema, many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "password", "posts", "comments")
        model = User
        ordered = True

    posts = ma.Nested(CommentSchema, many=True)
    comments = ma.Nested(CommentSchema, many=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
comment_schema = PostSchema()
comments_schema = PostSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)