from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import desc

from app.models import SavedPost, db
from ..response_helpers import error_response, success_response


save_bp = Blueprint('saves', __name__)


@save_bp.route('/<int:post_id>', methods=['POST'])
@jwt_required()
def save_post(post_id):
    email = get_jwt_identity()

    new_post = SavedPost(post_id=post_id, email=email)

    try:
        db.session.add(new_post)
        db.session.commit()
    except:
        return error_response('已新增')

    return success_response()


@save_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def unsave_post(post_id):
    email = get_jwt_identity()

    saved_post = SavedPost.query.filter_by(post_id=post_id, email=email).first()

    if saved_post:
        db.session.delete(saved_post)
        db.session.commit()
        return success_response()
    else:
        return error_response('已取消')


@save_bp.route('', methods=['GET'])
@jwt_required()
def get_saved_posts_list():
    email = get_jwt_identity()

    saved_posts = SavedPost.query.filter_by(email=email).order_by(desc(SavedPost.id))

    data = [
        {
            'post_id': saved_post.post_id,
            'email': saved_post.email,
            'title': saved_post.post.title,
            'content': saved_post.post.content,
            'created_time': saved_post.post.created_time,
            'updated_time': saved_post.post.updated_time,
        } for saved_post in saved_posts
    ]

    return success_response(data=data)