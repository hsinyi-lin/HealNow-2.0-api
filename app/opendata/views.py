from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models import Pharmacy, Med, Clarification, News, SavedMed, SavedNew, SavedClarification, db

from ..response_helpers import error_response, success_response


opendata_bp = Blueprint('opendatas', __name__)


@opendata_bp.route('/<int:class_id>/<int:data_id>', methods=['GET'])
def get_opendata(class_id, data_id):
    if class_id == 1:
        data = Med.query.get(data_id)
    elif class_id == 2:
        data = News.query.get(data_id)
    elif class_id == 3:
        data = Clarification.query.get(data_id)
    elif class_id == 4:
        data = Pharmacy.query.get(data_id)
    else:
        return error_response('類型編號錯誤')

    return success_response(data=data.as_dict())


@opendata_bp.route('/<int:class_id>', methods=['GET'])
def get_opendata_list(class_id):
    if class_id == 1:
        data = Med.query.all()
    elif class_id == 2:
        data = News.query.all()
    elif class_id == 3:
        data = Clarification.query.all()
    elif class_id == 4:
        data = Pharmacy.query.all()
    else:
        return error_response('類型編號錯誤')

    data_list = [d.as_dict() for d in data]

    return success_response(data=data_list)


@opendata_bp.route('/save_class/<int:class_id>/<int:data_id>', methods=['POST'])
@jwt_required()
def save_opendata_info(class_id, data_id):
    email = get_jwt_identity()

    if class_id == 1:
        data = SavedMed(med_id=data_id, email=email)
    elif class_id == 2:
        data = SavedNew(news_id=data_id, email=email)
    elif class_id == 3:
        data = SavedClarification(clarification_id=data_id, email=email)
    else:
        return error_response('類型編號錯誤')

    try:
        db.session.add(data)
        db.session.commit()
    except:
        return error_response('已加入')

    return success_response()


@opendata_bp.route('/save_class/<int:class_id>/<int:data_id>', methods=['DELETE'])
@jwt_required()
def unsave_opendata_info(class_id, data_id):
    email = get_jwt_identity()

    if class_id == 1:
        data = SavedMed.query.filter_by(med_id=data_id, email=email).first()
    elif class_id == 2:
        data = SavedNew.query.filter_by(news_id=data_id, email=email).first()
    elif class_id == 3:
        data = SavedClarification.query.filter_by(clarification_id=data_id, email=email).first()
    else:
        return error_response('類型編號錯誤')

    if data:
        db.session.delete(data)
        db.session.commit()
        return success_response()
    else:
        return error_response('已刪除')


@opendata_bp.route('/save_class/<int:class_id>', methods=['GET'])
@jwt_required()
def saved_opendata_list(class_id):
    email = get_jwt_identity()

    if class_id == 1:
        data = SavedMed.query.filter_by(email=email).all()
    elif class_id == 2:
        data = SavedNew.query.filter_by(email=email).all()
    elif class_id == 3:
        data = SavedClarification.query.filter_by(email=email).all()
    else:
        return error_response('類型編號錯誤')

    data_list = [d.as_dict() for d in data]

    return success_response(data=data_list)

