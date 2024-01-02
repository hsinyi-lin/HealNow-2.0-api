from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from ..models import Post, db, Comment, Like, SavedPost
from ..response_helpers import error_response, success_response
from ..utils import get_tw_time


post_bp = Blueprint('posts', __name__)


@post_bp.route('', methods=['POST'])
@jwt_required()
def add_post():
    data = request.get_json()
    email = get_jwt_identity()
    title = data.get('title')
    content = data.get('content')

    if not all([title, content]):
        return error_response()

    new_post = Post(title=title, content=content, email=email)

    db.session.add(new_post)
    db.session.commit()

    return success_response()


@post_bp.route('/<int:post_id>', methods=['PATCH'])
@jwt_required()
def edit_post(post_id):
    data = request.get_json()
    email = get_jwt_identity()
    title = data.get('title')
    content = data.get('content')

    if not all([title, content]):
        return error_response()

    post = Post.query.filter_by(id=post_id, email=email).first()

    if not post:
        return error_response(msg='沒有此貼文')

    post.title = title
    post.content = content
    post.updated_time = get_tw_time()

    db.session.commit()

    return success_response()


@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    email = get_jwt_identity()

    post_to_delete = Post.query.filter_by(id=post_id, email=email).first()

    if not post_to_delete:
        return error_response(msg='沒有此貼文')

    db.session.delete(post_to_delete)
    db.session.commit()

    return success_response()


@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return error_response(msg='沒有此貼文')

    data = {
        'id': post.id,
        'email': post.email,
        'username': post.user.username,
        'title': post.title,
        'content': post.content,
        'like_cnt': Like.query.filter_by(post_id=post_id).count(),
        'saved_cnt': SavedPost.query.filter_by(post_id=post_id).count(),
        'created_time': post.created_time,
        'updated_time': post.updated_time,
        'comment': [
            {
                'id': comment.id,
                'email': comment.email,
                'username': comment.user.username,
                'content': comment.content,
                'created_time': comment.created_time,
                'updated_time': comment.updated_time
            } for comment in Comment.query.filter_by(post_id=post_id).order_by(desc(Comment.id))
        ]
    }

    return success_response(data=data)


@post_bp.route('', methods=['GET'])
def get_all_posts():
    posts = Post.query.order_by(desc(Post.id)).all()

    posts_list = [post.as_dict() for post in posts]

    return success_response(data=posts_list)


@post_bp.route('/like/<int:post_id>', methods=['POST', 'DELETE'])
@jwt_required()
def post_like(post_id):
    email = get_jwt_identity()

    post = Post.query.get(post_id)

    if not post:
        return error_response('沒有此貼文')

    like = Like.query.filter_by(post_id=post_id, email=email).first()

    if request.method == 'POST':
        if like:
            return error_response('已按過讚')
        new_like = Like(post_id=post_id, email=email)
        db.session.add(new_like)
        db.session.commit()

        return success_response()
    elif request.method == 'DELETE':
        if not like:
            return error_response('尚未按過讚')
        db.session.delete(like)
        db.session.commit()

        return success_response()
