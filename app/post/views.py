from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Post, db, Comment

post_bp = Blueprint('posts', __name__)


@post_bp.route('', methods=['POST'])
@jwt_required()
def add_post():
    data = request.get_json()
    email = get_jwt_identity()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': '缺少欄位'}), 400

    new_post = Post(title=title, content=content, email=email)

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': '成功'}), 200


@post_bp.route('/<int:post_id>', methods=['PATCH'])
@jwt_required()
def edit_post(post_id):
    data = request.get_json()
    email = get_jwt_identity()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'message': '缺少欄位'}), 400

    post = Post.query.filter_by(id=post_id, email=email).first()

    if not post:
        return jsonify({'message': '沒有此貼文'}), 404

    post.title = title
    post.content = content
    post.updated_time = datetime.now()

    db.session.commit()

    return jsonify({'message': '成功'}), 200


@post_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    email = get_jwt_identity()

    post_to_delete = Post.query.filter_by(id=post_id, email=email).first()

    if not post_to_delete:
        return jsonify({'message': '沒有此貼文'}), 404

    db.session.delete(post_to_delete)
    db.session.commit()

    return jsonify({'message': '成功'}), 200


@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'message': '沒有此貼文'}), 404

    # 返回帖子的信息，例如 title 和 content
    return jsonify({
        'id': post.id,
        'email': post.email,
        'title': post.title,
        'content': post.content,
        'created_time': post.created_time,
        'updated_time': post.updated_time,
        'comment': [
            {
                'id': comment.id,
                'email': comment.email,
                'content': comment.content,
                'created_time': comment.created_time,
                'updated_time': comment.updated_time
            } for comment in Comment.query.filter_by(post_id=post_id)
        ]
    }), 200


@post_bp.route('', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()

    posts_list = [post.as_dict() for post in posts]

    return {'posts': posts_list}, 200


