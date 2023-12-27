import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import User, db
from ..response_helpers import error_response, success_response
from ..utils import *


user_bp = Blueprint('user', __name__)


@user_bp.route('', methods=['GET'])
@jwt_required()
def get_profile():
    email = get_jwt_identity()
    user = User.query.get(email)

    if user:
        return success_response(user.as_dict())
    else:
        return error_response(msg='沒有此使用者')


@user_bp.route('', methods=['PATCH'])
@jwt_required()
def edit_profile():
    data = request.get_json()
    username = data.get('username')
    gender = data.get('gender')
    photo = data.get('photo')

    email = get_jwt_identity()
    user = User.query.get(email)

    if user:
        user.username = username
        user.gender = gender
        user.photo = photo
        user.updated_time = get_tw_time()

        db.session.commit()
        return success_response()
    else:
        return error_response(msg='沒有此使用者')




