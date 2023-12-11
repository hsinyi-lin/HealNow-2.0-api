from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..models import User, Verification, db
from ..utils import *


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    gender = data.get('gender')

    if not email or not password or not username or not gender:
        return jsonify({'message': '缺少欄位'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': '已有存在的使用者'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, username=username, gender=gender)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': '成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': '帳號或密碼錯誤'}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token), 200


@auth_bp.route('/send_verification', methods=['POST'])
def send_verification():
    email = request.json.get('email')

    if not email:
        return jsonify({'message': '缺少欄位'}), 401

    verification_code = generate_verification_code()

    send_verification_code(email, verification_code)

    return jsonify({'message': '成功'}), 200


def send_verification_code(email, code):
    mail = current_app.extensions['mail']

    msg = Message('Verification Code', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your verification code is: {code}'

    mail.send(msg)

    verification = Verification(email=email, code=code)

    db.session.add(verification)
    db.session.commit()


@auth_bp.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')

    if not email or not code:
        return jsonify({'message': '缺少欄位'}), 401

    verification = Verification.query.filter_by(email=email).order_by(desc(Verification.created_time)).first()
    print(verification)

    if code == verification.code:
        return jsonify({'message': '成功'}), 200
    else:
        return jsonify({'message': '驗證碼錯誤'}), 401


@auth_bp.route('/change_password', methods=['PATCH'])
@jwt_required()
def change_password():
    data = request.get_json()
    email = get_jwt_identity()
    print(email)
    new_password = data.get('new_password')

    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(new_password)

        db.session.commit()
        return jsonify({'message': '成功'}), 200
    else:
        return jsonify({'message': '沒有此使用者'}), 404