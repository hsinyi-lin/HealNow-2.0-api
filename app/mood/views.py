from datetime import datetime

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Mood, db

import openai


mood_bp = Blueprint('mood', __name__)


@mood_bp.route('', methods=['POST'])
@jwt_required()
def add_mood():
    data = request.get_json()
    email = get_jwt_identity()
    content = data.get('content')

    if not content:
        return 'Title and content are required', 400

    openai.api_key = current_app.config['OPENAI_API_KEY']

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一位會用一句話給予鼓勵的心理諮商師"},
            {"role": "user", "content": content}
        ]
    )

    response_message = completion['choices'][0]['message']['content'].strip()

    new_post = Mood(content=content, email=email, ai_reply=response_message)

    db.session.add(new_post)
    db.session.commit()

    return 'Post added successfully', 200


@mood_bp.route('/<int:mood_id>', methods=['DELETE'])
@jwt_required()
def delete_mood(mood_id):
    email = get_jwt_identity()

    mood = Mood.query.filter_by(id=mood_id, email=email).first()

    if mood:
        db.session.delete(mood)
        db.session.commit()
    else:
        return '不存在', 404

    return 'Post added successfully', 200


@mood_bp.route('', methods=['GET'])
@jwt_required()
def get_mood_list():
    email = get_jwt_identity()

    moods = Mood.query.filter_by(email=email)

    return jsonify({
        'success': True,
        'msg': '成功',
        'data': [
            {
                'id': mood.id,
                'email': mood.email,
                'content': mood.content,
                'ai_reply': mood.ai_reply,
                'created_time': mood.created_time
            } for mood in moods
        ]
    }), 200

