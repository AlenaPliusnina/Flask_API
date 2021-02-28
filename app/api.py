from datetime import datetime

from flask import request
from flask_restful import Resource, Api
from flask import g

from app import app, db
from flask_httpauth import HTTPBasicAuth

from app.models import User, Post, Comment
from app.schemes import posts_schema, post_schema, comment_schema, comments_schema, users_schema, user_schema

api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()

    if not user or not user.verify_password(password):
        return False

    g.user = user

    return True


class UserListResource(Resource):
    @auth.login_required
    def get(self):
        if g.user.username == 'admin':
            users = User.query.all()
            return users_schema.dump(users)
        else:
            return {'error': 'HTTP 403: Forbidden',
                    'message': 'Only the superuser can access.'}, 403

    def post(self):
        body = request.get_json()
        user = User(**body)
        exist_email = User.query.filter_by(email=user.email).first()
        exist_username = User.query.filter_by(username=user.username).first()

        if not exist_email and not exist_username:
            try:
                user.hash_password()
                user.save()
                return {'message': 'You registered successfully. Please log in.'}, 201

            except Exception as e:
                return {'message': str(e)}, 401

        else:
            return {'message': 'User already exists. Please login.'}, 202


class UserResource(Resource):
    @auth.login_required
    def get(self, user_id):
        if g.user.username == 'admin' or g.user.id == user_id:
            try:
                user = User.query.get_or_404(user_id)
                return user_schema.dump(user)
            except Exception as e:
                return {'message': str(e)}, 404
        else:
            return {'error': 'HTTP 403: Forbidden',
                    'message': 'You can only access your registration information.'}, 403

    @auth.login_required
    def delete(self, user_id):
        try:
            user = User.query.get_or_404(user_id)

            if user.id == g.user.id or g.user.username == 'admin':
                db.session.delete(user)
                db.session.commit()
                return {'message': 'The user was successfully deleted.'}, 200
            else:
                return {'error': 'HTTP 403: Forbidden',
                        'message': 'You can only delete your account.'}, 403

        except Exception as e:
            return {'message': str(e)}, 404


class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return posts_schema.dump(posts)

    @auth.login_required
    def post(self):
        new_post = Post(
            author_id=g.user.id,
            title=request.json['title'],
            content=request.json['content'],
            publication_datetime=datetime.now(),
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)


class PostResource(Resource):
    def get(self, post_id):
        try:
            post = Post.query.get_or_404(post_id)
            return post_schema.dump(post)
        except Exception as e:
            return {'message': str(e)}, 404

    @auth.login_required
    def patch(self, post_id):
        try:
            post = Post.query.get_or_404(post_id)

            if post.author_id == g.user.id:
                if 'title' in request.json:
                    post.title = request.json['title']
                if 'content' in request.json:
                    post.content = request.json['content']

                db.session.commit()
                return post_schema.dump(post)
            else:
                return {'error': 'HTTP 403: Forbidden',
                        'message': 'You can only edit your posts.'}, 403

        except Exception as e:
            return {'message': str(e)}, 404

    @auth.login_required
    def delete(self, post_id):
        try:
            post = Post.query.get_or_404(post_id)

            if post.author_id == g.user.id:
                db.session.delete(post)
                db.session.commit()
                return {'message': 'The post was successfully deleted.'}, 200
            else:
                return {'error': 'HTTP 403: Forbidden',
                        'message': 'You can only delete your posts.'}, 403

        except Exception as e:
            return {'message': str(e)}, 404


class CommentListResource(Resource):
    def get(self):
        comments = Comment.query.all()
        return comments_schema.dump(comments)

    @auth.login_required
    def post(self):
        new_comment = Comment(
            author_id=g.user.id,
            post_id=request.json['post_id'],
            title=request.json['title'],
            content=request.json['content'],
            publication_datetime=datetime.now()
        )

        post = Post.query.filter_by(id=request.json['post_id']).first()

        if post:
            db.session.add(new_comment)
            db.session.commit()
            return comment_schema.dump(new_comment)

        else:
            return {'error': 'HTTP 404: Not Found',
                    'message': 'Post with this id was not found.'}, 404


class CommentResource(Resource):
    def get(self, comment_id):
        try:
            comment = Comment.query.get_or_404(comment_id)
            return comment_schema.dump(comment)
        except Exception as e:
            return {'message': str(e)}, 404

    @auth.login_required
    def patch(self, comment_id):
        try:
            comment = Comment.query.get_or_404(comment_id)

            if comment.author_id == g.user.id:
                if 'title' in request.json:
                    comment.title = request.json['title']
                if 'content' in request.json:
                    comment.content = request.json['content']

                db.session.commit()
                return comment_schema.dump(comment)
            else:
                return {'error': 'HTTP 403: Forbidden',
                        'message': 'You can only edit your comments.'}, 403

        except Exception as e:
            return {'message': str(e)}, 404

    @auth.login_required
    def delete(self, comment_id):
        try:
            comment = Comment.query.get_or_404(comment_id)

            if comment.author_id == g.user.id:
                db.session.delete(comment)
                db.session.commit()
                return {'message': 'The comment was successfully deleted.'}, 200
            else:
                return {'error': 'HTTP 403: Forbidden',
                        'message': 'You can only delete your comments.'}, 403

        except Exception as e:
            return {'message': str(e)}, 404


api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/posts/<int:post_id>')
api.add_resource(CommentListResource, '/comments')
api.add_resource(CommentResource, '/comments/<int:comment_id>')



