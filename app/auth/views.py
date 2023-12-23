from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..models import User
from ..response_helpers import error_response, success_response
from ..utils import *


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    gender = data.get('gender')

    if not all([email, password, username, gender]):
        return error_response()

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return error_response(msg='已有存在的使用者')

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, username=username, gender=gender)

    db.session.add(new_user)
    db.session.commit()

    return success_response()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return error_response(msg='帳號或密碼錯誤')

    access_token = create_access_token(identity=user.email)
    return jsonify({'success': True, 'msg': '成功', 'access_token': access_token}), 200


@auth_bp.route('/send_verification', methods=['POST'])
def send_verification():
    email = request.json.get('email')

    if not email:
        return error_response()

    verification_code = generate_verification_code()

    send_verification_code(email, verification_code)

    return success_response()


@auth_bp.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if not all([email, code]):
        return error_response()

    verification = Verification.query.filter_by(email=email).order_by(desc(Verification.id)).first()
    print(verification)

    if code == verification.code:
        return success_response()
    else:
        return error_response(msg='驗證碼錯誤')


@auth_bp.route('/change_password', methods=['PATCH'])
def change_password():
    data = request.get_json()
    is_login = data.get('is_login')
    new_password = data.get('new_password')

    if is_login:
        @jwt_required()
        def get_email_from_jwt():
            return get_jwt_identity()

        email = get_email_from_jwt()
    else:
        try:
            email = data['email']
        except:
            return error_response(msg='非登入狀態，缺少email欄位')

    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password)
        db.session.commit()

        return success_response()
    else:
        return error_response(msg='沒有此使用者')