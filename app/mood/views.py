from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from ..models import Mood, db
from ..response_helpers import error_response, success_response
from ..utils import call_chatgpt, azure_text_analysis

mood_bp = Blueprint('mood', __name__)


@mood_bp.route('', methods=['POST'])
@jwt_required()
def add_mood():
    data = request.get_json()
    email = get_jwt_identity()
    content = data.get('content')

    if not content:
        return error_response()

    ai_reply = call_chatgpt(content)
    analysis = azure_text_analysis(content)

    new_post = Mood(content=content, email=email, ai_reply=ai_reply,
                    positive=analysis['positive'], neutral=analysis['neutral'], negative=analysis['negative'],
                    sentiment=analysis['sentiment'])

    db.session.add(new_post)
    db.session.commit()

    return success_response()


@mood_bp.route('/<int:mood_id>', methods=['DELETE'])
@jwt_required()
def delete_mood(mood_id):
    email = get_jwt_identity()

    mood = Mood.query.filter_by(id=mood_id, email=email).first()

    if mood:
        db.session.delete(mood)
        db.session.commit()
    else:
        return error_response(msg='不存在')

    return success_response()


@mood_bp.route('', methods=['GET'])
@jwt_required()
def get_mood_list():
    email = get_jwt_identity()

    moods = Mood.query.filter_by(email=email).order_by(desc(Mood.id))

    moods_list = [mood.as_dict() for mood in moods]

    return success_response(data=moods_list)

