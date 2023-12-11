from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Comment, Post, db

comment_bp = Blueprint('comments', __name__)


@comment_bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    email = get_jwt_identity()

    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'message': '缺少欄位'}), 400

    post = Post.query.get(post_id)

    if not post:
        return jsonify({'message': '不存在的貼文'}), 404

    new_comment = Comment(post_id=post_id, content=content, email=email)

    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': '成功'}), 200


@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    email = get_jwt_identity()

    comment = Comment.query.filter_by(id=comment_id, email=email).first()

    if comment:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': '成功'}), 200
    else:
        return jsonify({'message': '沒有此回覆'}), 404


@comment_bp.route('/<int:comment_id>', methods=['PATCH'])
@jwt_required()
def edit_comment(comment_id):
    data = request.get_json()
    email = get_jwt_identity()
    content = data.get('content')

    if not content:
        return jsonify({'message': '缺少欄位'}), 400

    comment = Comment.query.filter_by(id=comment_id, email=email).first()

    if not comment:
        return jsonify({'message': '沒有此回覆'}), 404

    comment.content = content
    comment.updated_time = datetime.now()
    db.session.commit()

    return jsonify({'message': '成功'}), 200


@comment_bp.route('/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        return jsonify({'message': '沒有此回覆'}), 404

    return jsonify({
        'id': comment.id,
        'post_id': comment.post_id,
        'content': comment.content,
        'created_time': comment.created_time,
        'updated_time': comment.updated_time
    }), 200